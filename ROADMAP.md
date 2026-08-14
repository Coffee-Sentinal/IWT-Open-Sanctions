# Roadmap

## V1.1 — Data quality and curation
Strengthen deduplication, aliases/transliterations, nationality versus jurisdiction, structured addresses, public company numbers, lawful/relevant birth dates, domains and relevant social handles, confidence scoring, source archiving, correction history, duplicate reports, and moderator tooling.

## V1.2 — Private contribution workflow
Move from public GitHub Issues to `public form → private pending queue → moderator review → approved record`. Evaluate only sustainable free options such as an owner-controlled Google Form or private moderation repository. Do not expose allegations before review or auto-publish submissions.

## V1.3 — Relationship/network intelligence
Add source-backed relationship types and client-side Cytoscape.js visualization. Nodes link to profiles; edges require citations. Cover ownership, directorship, employment, trade, co-defendants, networks, facilities, addresses and related companies without inference.

## V1.4 — Improved document intelligence
Add field-aware shipper, consignee, notify party, exporter/importer, permit holder, applicant, director/owner, address, port, country and registration-number extraction. Score corroborating attributes separately and explain overall confidence. Add robust bundled PDF.js and lazy local OCR when maintainable.

## V1.5 — Internationalization
Localize UI and normalization for major IWT-relevant languages/scripts while preserving proper names and avoiding corrupting automatic translation.

## V1.6 — Provenance and audit history
Expose first-added, last-updated, status, source and correction histories, using Git history where practical.

## V1.7 — Static public API/schema
Formalize versioned `/data/*.json` endpoints, JSON Schema and consumer documentation.

## V1.8 — OSINT enrichment
Add source-backed registries, trade names, businesses, domains, operationally relevant public contact points, addresses, routes, commodities and CITES case information. Never publish private data automatically.

## V1.9 — Automated source monitoring
Explore free public-source monitoring into a private candidate queue. Preserve sources, check legal status, keep resolution reviewable, and never auto-publish discoveries.

## V2 — Mature global IWT entity intelligence platform
Support customs, CITES, NGO, enforcement, journalism and academic research with global identity resolution and network analysis: prior appearances, aliases, jurisdictions, cases/statuses, species, connections and their sources, document matches, and transparent confidence.
