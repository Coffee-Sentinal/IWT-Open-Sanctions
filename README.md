# IWT Open Sanctions

**Open-source intelligence on wildlife trafficking networks.** A free, independent, static screening index for people and entities reported in connection with illegal wildlife trade. It is not affiliated with the OpenSanctions project and is not a legal authority. Inclusion is not proof of guilt.

## V1 capabilities

- Search 125 workbook-derived subjects across names, aliases, roles, jurisdictions, cases and commodities, with eight filters and careful fuzzy scoring.
- Permanent hash profile links with differentiated legal-status badges, events, source links and caveats.
- Local paste/file document screening, local bulk name checks and CSV result export. TXT/CSV/TSV and conservative text-based PDF extraction are supported. Image OCR is intentionally not bundled in stable V1; see the roadmap.
- Downloadable entities/sources/relationships CSV and JSON, cases, metadata and a complete dataset.
- Human-reviewed public GitHub candidate workflow; issues never modify data automatically.
- No backend, account, analytics, tokens, paid API, query transmission or remote document storage.

> A potential match is an investigative lead, not confirmation of identity. Absence is not clearance. Verify identifiers and cited sources.

## Architecture

The application is a dependency-free, responsive ES-module single-page application with hash routing, suitable for the `/IWT-Open-Sanctions/` GitHub Pages project path. Static JSON is loaded once and all search/document work occurs in browser memory. This keeps hosting at €0 and makes a later precomputed/chunked/Web Worker index possible. `scripts/build.mjs` copies the reviewed application and data to `dist/`; GitHub Actions validates, tests, builds and deploys it.

## Local development

Node.js 20+ is required. There are currently no third-party runtime packages.

```bash
npm install
npm run dev
# open http://localhost:5173/IWT-Open-Sanctions/
npm test
npm run validate-data
npm run build
```

## Data and workbook import

The original `iwt_named_entities_2010_2026.xlsx` is preserved as the seed. Inspection found `Summary` (34 rows), `IWT Entities` (one header plus 125 records), and `Methodology` (18 rows). The actual 22-column entity header is mapped by name, not position.

```bash
npm run import-xlsx
```

The dependency-free OOXML importer creates `public/data/{entities,cases,sources,relationships,metadata,complete}.json`, CSV exports and updates `data/id-registry.json`. Registry normalized-name keys retain permanent IDs. Repeated seed names merge into one entity; explicit aliases remain attached to it. The importer reports counts and writes no inferred relationships.

**Maintenance safety:** generated JSON becomes reviewed canonical data after import. Never delete/regenerate the ID registry. The importer cannot understand every real-world identity collision and does not silently merge merely similar names. Review generated diffs, probable identity questions, status normalization, preserved caveats, and curated additions before commit. Because import output can replace generated files, manually curated aliases/relationships must first be reconciled into the maintained source or reapplied during review. Issues are never import input.

Data model and validation cover entity, case/event, source and relationship references. Validation rejects missing/duplicate IDs or names, invalid statuses, broken references, malformed JSON, missing source URLs and missing relationship endpoints.

## Contribution and moderation

The **Contribute** page opens a structured public candidate issue. Everything in a public issue is visible before review. Candidate → human evidence/identity/duplicate/status review → approve/reject → curated pull request → validation → merge → rebuild. No automation promotes issues. Read [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/MODERATION.md](docs/MODERATION.md), including correction/removal handling.

## Deployment

1. Push the approved commit to `main`.
2. In GitHub, open **Settings → Pages → Build and deployment → Source** and select **GitHub Actions**. This is the one required manual setting.
3. Ensure Actions are enabled. The `Validate, test and deploy Pages` workflow publishes `dist/`.

The route and asset design is static-safe at `https://coffee-sentinal.github.io/IWT-Open-Sanctions/`.

## Privacy, security and limitations

Documents and queries stay in the browser. Uploaded content is read as inert text and is never rendered as HTML, uploaded, logged, or sent to OCR/AI/analytics services. There are no secrets. Text-based PDF support is deliberately conservative; compressed/complex PDFs may yield no text, and scanned PDFs/images need user-supplied local OCR text in V1. Coverage is incomplete, subjects can share names, public sources can change, and statuses can evolve.

## Licensing

Software code is MIT licensed. **The dataset is not assigned a license:** the repository owner must make and document that separate decision after reviewing compilation rights and source terms. Source content remains subject to its publishers' rights. Downloads must not be treated as legally authoritative.

See [ROADMAP.md](ROADMAP.md) for private submissions, richer data quality/provenance, source-backed networks, robust PDF/OCR, internationalization, enrichment and monitoring.
