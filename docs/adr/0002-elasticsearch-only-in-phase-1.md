# 0002: Elasticsearch only in phase 1

Date: 2026-11-24
Status: accepted

## Context

Phase 1 is a read-only search over Bundestag speeches. There are no user accounts, collections or editorial content yet. Elasticsearch is needed for phrase, fuzzy and stemmed search with highlighting. A relational database would only add operations work without a use case.

## Decision

Phase 1 uses Elasticsearch as the only data store. Postgres is introduced in phase 2 together with the CMS (`wortlaut-cms`), when curated collections and other real application data appear.

## Consequences

- Less infrastructure to run and secure in the first live deployment.
- Everything in phase 1 must be derivable from the source protocols, so the index can be rebuilt at any time.
- When phase 2 starts, the CMS product (Payload, Strapi or Directus) and the Postgres setup need their own ADR.
