# 0001: Multiple repos instead of a monorepo

Date: 2026-11-24
Status: accepted

## Context

Wortlaut consists of an indexer (.NET job), an API (.NET service), a frontend (Next.js), infrastructure code and, later, a CMS. They use different technology, run differently and release at different speeds. The project is also a public showcase, so the interfaces between the parts should be visible and testable.

## Decision

Use several small repos under the GitHub organisation `wortlauts`, plus a meta repo `wortlaut` as entry point. Rule of thumb: one repo equals one deployable artifact with its own release cadence.

The repos are connected by versioned contracts, not by shared code:

- the indexer publishes the index template and document schema as a release,
- the API pins a template version and tests against it,
- the API publishes `openapi.json`, and the frontend generates its client from it.

There is no shared NuGet package between indexer and API. One GitHub Project board spans all repos, and `wortlaut.code-workspace` opens them side by side in VS Code.

## Consequences

- Each repo can be built, tested and released on its own.
- Contracts must be versioned and covered by contract tests, otherwise drift goes unnoticed.
- Cross-repo changes need several pull requests and some coordination.
- Setup is more work than a monorepo, for example CI per repo.
