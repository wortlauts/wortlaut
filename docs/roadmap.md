# Roadmap

Phase 1 ends with a live search. Each milestone ends with something that can be shown. Status is tracked on the GitHub Project board; this page is the overview.

## Phase 1

| # | Step | Result | Status |
| --- | --- | --- | --- |
| 1 | Organisation and meta repo | org `wortlauts`, repo `wortlaut` with README, architecture, `docs/adr`, project board | done |
| 2 | Look at the data first | XML of legislative period 21 read by hand, small samples in `wortlaut-indexer/testdata`, structure of periods 19 and 20 compared | done |
| 3 | Local stack | `wortlaut-infra` with `compose/dev`: Elasticsearch (single node) and Kibana, pinned versions, health checks | done |
| 4 | **M1, data in the index** | indexer with parser tests, index template `speeches-v1`, bulk import, alias `speeches`; speeches searchable in Kibana | done, periods 19 to 21 |
| 5 | **M2, API** | search and detail endpoints, Swagger UI, Testcontainers tests, CI with image to ghcr.io | done |
| 6 | **M3, frontend** | search page, hits with highlights, filters, trend chart, client generated from `openapi.json` | done, tests follow |
| 7 | **M4, live** | first deployment on the owner's own server with Compose, domain, HTTPS, licence and source page | live; legal pages and licences open |

In every repo from day one: GitHub Actions for build and test, Dependabot or Renovate, semver tags, and a README that explains what the repo is and how to run it locally.

## After phase 1

One milestone each, in this order:

1. Shareable quote card (image with sentence, speaker, date, source)
2. Older legislative periods (1 to 18) via prepared corpora such as CPP-BT or Open Discourse (check each licence first)
3. Observability: Kibana dashboards, OpenTelemetry, uptime checks
4. Kubernetes and infrastructure as code: Helm, Terraform, GitOps in `wortlaut-infra`
5. Postgres and CMS (`wortlaut-cms`) for curated collections
6. Audio from freely licensed sources only

## Open decisions

CMS product, older corpora licences (see [data-sources.md](data-sources.md)), Mediathek deep links, trademark and domain check, and the licences of the code and of the brand assets.
