#!/usr/bin/env python3
"""Dependency-free OOXML importer. Registry makes IDs stable; review diffs before commit."""
import zipfile, xml.etree.ElementTree as ET, json, re, csv, io, hashlib, datetime, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]; BOOK=ROOT/'iwt_named_entities_2010_2026.xlsx'; DATA=ROOT/'public/data'; DATA.mkdir(parents=True,exist_ok=True)
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def rows():
 z=zipfile.ZipFile(BOOK); ss=[]
 if 'xl/sharedStrings.xml' in z.namelist(): ss=[''.join(t.text or '' for t in x.findall('.//m:t',NS)) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
 wb=ET.fromstring(z.read('xl/workbook.xml')); rel=ET.fromstring(z.read('xl/_rels/workbook.xml.rels')); targets={x.attrib['Id']:x.attrib['Target'] for x in rel}
 sheet=next(x for x in wb.findall('.//m:sheet',NS) if x.attrib['name']=='IWT Entities'); target=targets[sheet.attrib['{'+NS['r']+'}id']].lstrip('/'); target=target if target.startswith('xl/') else 'xl/'+target
 for row in ET.fromstring(z.read(target)).findall('.//m:row',NS):
  vals={}
  for c in row.findall('m:c',NS):
   col=re.match(r'[A-Z]+',c.attrib['r']).group(); v=c.find('m:v',NS); val='' if v is None else v.text or ''
   if c.attrib.get('t')=='s' and val: val=ss[int(val)]
   elif c.attrib.get('t')=='inlineStr': val=''.join(t.text or '' for t in c.findall('.//m:t',NS))
   vals[col]=val.strip()
  yield vals
def key(s): return re.sub(r'[^a-z0-9]','',s.casefold())
def split(s): return [x.strip() for x in re.split(r'\s*(?:/|;|\|)\s*',s) if x.strip()]
def status(s,d):
 x=(s+' '+d).lower()
 if 'withdraw' in x or 'dismiss' in x:return 'Charges Withdrawn / Dismissed'
 if 'pleaded guilty' in x or 'plead guilty' in x:return 'Pleaded Guilty'
 if 'sentenc' in x or 'convict' in x:return 'Convicted / Sentenced'
 if 'charg' in x or 'indict' in x:return 'Charged / Indicted'
 if 'arrest' in x or 'detain' in x:return 'Arrested / Detained'
 if 'wanted' in x or 'reward' in x:return 'Wanted / Reward'
 if 'investigat' in x or 'alleg' in x:return 'Under Investigation / Alleged'
 if 'connect' in x:return 'Connected Entity'
 return 'Unknown / Other'
def typ(s):
 x=s.lower(); return 'Person' if 'person' in x else 'Business' if any(a in x for a in ['business','company']) else 'Facility' if 'facilit' in x else 'Network' if 'network' in x else 'Organization'
raw=list(rows()); headers=raw[0]; cols={v:k for k,v in headers.items()}; get=lambda r,n:r.get(cols.get(n,''),'')
registry_path=ROOT/'data/id-registry.json'; registry=json.load(open(registry_path)) if registry_path.exists() else {}; counters={c:max([int(v.rsplit('-',1)[1]) for v in registry.values() if f'IWT-{c}-' in v] or [0]) for c in 'PBFNO'}
entities=[]; cases=[]; sources=[]; source_by={}
for i,r in enumerate(raw[1:],1):
 name=get(r,'Subject Name');
 if not name: continue
 t=typ(get(r,'Subject Category')); rk=key(name); code={'Person':'P','Business':'B','Facility':'F','Network':'N','Organization':'O'}[t]
 if rk not in registry: counters[code]+=1; registry[rk]=f'IWT-{code}-{counters[code]:06d}'
 eid=registry[rk]; url=get(r,'Source URL'); sk=url or '|'.join([get(r,'Source Publisher'),get(r,'Source Title')])
 if sk not in source_by:
  sid=f'SRC-{len(source_by)+1:06d}'; source_by[sk]=sid; sources.append({'source_id':sid,'publisher':get(r,'Source Publisher'),'title':get(r,'Source Title'),'url':url,'publication_date':get(r,'Source Date'),'language':get(r,'Source Language'),'source_type':get(r,'Source Type'),'confidence':get(r,'Confidence'),'notes':get(r,'Legal Caveat / Notes')})
 sid=source_by[sk]; cid=f'CASE-{i:06d}'; st=status(get(r,'Status Group'),get(r,'Legal / Investigative Status Detail'))
 cases.append({'case_id':cid,'entity_ids':[eid],'date':get(r,'Source Date'),'year':get(r,'Year'),'jurisdiction':get(r,'Country / Jurisdiction'),'status':st,'status_detail':get(r,'Legal / Investigative Status Detail'),'outcome':get(r,'Outcome / Sentence'),'description':get(r,'Conduct Summary'),'species_or_commodities':split(get(r,'Species / Commodity')),'network_or_case_name':get(r,'Case / Network / Connected Entity'),'source_ids':[sid]})
 entities.append({'entity_id':eid,'canonical_name':name,'entity_type':t,'aliases':split(get(r,'Alias / Alternate Name')),'countries':split(get(r,'Country / Jurisdiction')),'regions':split(get(r,'Region')),'addresses':[],'identifiers':[],'websites':[],'status_summary':st,'roles':split(get(r,'Role / Connection')),'species_or_commodities':split(get(r,'Species / Commodity')),'case_ids':[cid],'source_ids':[sid],'relationship_ids':[],'caveats':list(filter(None,[get(r,'Legal Caveat / Notes')])),'last_updated':get(r,'Source Date')})
# merge repeated normalized subjects, preserving first canonical ID
merged={}
for e in entities:
 if e['entity_id'] not in merged: merged[e['entity_id']]=e
 else:
  m=merged[e['entity_id']]
  for f in ['aliases','countries','regions','roles','species_or_commodities','case_ids','source_ids','caveats']: m[f]=list(dict.fromkeys(m[f]+e[f]))
  m['last_updated']=max(m['last_updated'],e['last_updated'])
entities=list(merged.values()); relationships=[]; generated='2026-08-13'
meta={'data_version':'1.0.0','schema_version':'1.0.0','generated_date':generated,'source_workbook':BOOK.name,'counts':{'entities':len(entities),'cases':len(cases),'sources':len(sources),'relationships':0}}
for n,o in [('entities',entities),('cases',cases),('sources',sources),('relationships',relationships),('metadata',meta)]: (DATA/f'{n}.json').write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
for n,items in [('entities',entities),('sources',sources),('relationships',relationships)]:
 keys=list(items[0]) if items else ['relationship_id','source_entity_id','target_entity_id','relationship_type','description','source_ids']; out=io.StringIO(); w=csv.DictWriter(out,keys); w.writeheader(); w.writerows({k:'; '.join(v) if isinstance(v,list) else v for k,v in x.items()} for x in items); (DATA/f'{n}.csv').write_text(out.getvalue())
(DATA/'complete.json').write_text(json.dumps({'metadata':meta,'entities':entities,'cases':cases,'sources':sources,'relationships':relationships},ensure_ascii=False,indent=2)+'\n'); registry_path.parent.mkdir(exist_ok=True); registry_path.write_text(json.dumps(registry,indent=2,sort_keys=True)+'\n')
print(f"Imported {len(entities)} entities, {len(cases)} cases, {len(sources)} sources. Review generated diffs before committing; curated relationships are not overwritten by this seed import.")
