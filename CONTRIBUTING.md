# Contributing

Search existing entities and issues first. Candidate records must use the structured public [issue form](https://github.com/Coffee-Sentinal/IWT-Open-Sanctions/issues/new?template=candidate-record.yml). **Issues are public.** Do not include confidential material, unnecessary personal data, or unsupported allegations. Submission does not imply acceptance and cannot update production data.

## Approval workflow

Candidate issue → pending human review → evidence and identity check → duplicate/alias check → legal-status check → reliability check → approve or reject → maintainer updates curated static data → pull request validation → merge and site rebuild.

Maintainers should edit the workbook only when it remains the agreed seed source, run `npm run import-xlsx`, carefully review every generated diff, then validate and test. The stable `data/id-registry.json` must be committed and never regenerated. The import is deliberately not connected to issues or deployment.

For corrections, open an issue naming the entity ID, disputed statement, requested outcome, and authoritative evidence. See [moderation guidance](docs/MODERATION.md).
