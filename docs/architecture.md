# Architecture

Wortlaut is split into several small repos so each can be built, tested and released on its own. The document schema is owned by `wortlaut-indexer`, the HTTP contract by `wortlaut-api`; this page is the overview.

```text
 Bundestag Open Data            (outside the repos)
 plenary protocols as XML
          |
          v
 wortlaut-indexer  --(1)-->  Elasticsearch
 parses and indexes          alias speeches -> speeches-v1
                                   |
                                  (2)
                                   v
 visitor (browser)  <--  wortlaut-frontend  <--(3)--  wortlaut-api
                         search, trend chart,          search, trends,
                         detail                        openapi
```

## Contracts between the repos

1. The indexer publishes the index template (`index-template.json`) and the document schema as a versioned release.
2. The API pins a template version. A contract test starts Elasticsearch with that template.
3. The API publishes `openapi.json` with every release. The frontend generates its typed client from it.

There is no shared code package between the repos. The contracts are files, and CI catches drift.

## Access rules

- Only the indexer writes to Elasticsearch.
- The API reads only (read-only role).
- The frontend talks only to the API.

## Deployment

`wortlaut-infra` is the single source of truth for what runs in production: the Compose stack, the image versions and the encrypted secrets. Releases flow in one direction:

```text
 application repo                 wortlaut-infra                host
 Deploy to PROD  --(tag)-->  compose/prod/versions.env  --(pull)-->  deploy.sh
 CI, arm64 image             pull request protected                  decrypts secrets,
 to ghcr.io                  main, deploy key pins                   compose up, result
                                                                      reported back
```

- Each application repo has a manual **Deploy to PROD** workflow. It runs the CI, publishes an image tagged `sha-<commit>` and commits that tag to `compose/prod/versions.env` in the infra repo.
- The host pulls the infra repo on a timer and runs `compose/prod/deploy.sh`. Nothing connects into the host, and the host holds no GitHub credentials besides a key that only writes the result.
- Secrets are stored in the infra repo encrypted with SOPS and age. The host decrypts them into memory for the duration of a deployment.
- After a deployment the host reports the result as an info commit on the branch `prod-status`, which turns into the commit status `deploy/prod` and into the result of the **Deploy to PROD** run.

The decisions behind this are ADR [0005](adr/0005-first-deployment-on-a-raspberry-pi.md) and [0006](adr/0006-pull-based-deployment-from-the-infra-repo.md).

## Versioning

- Semver tags per repo.
- Index versions: `speeches-v1`, `speeches-v2`. A breaking mapping change means a new index and an alias switch without downtime.
- API paths: `/v1`, `/v2`. Additive changes stay in `/v1`.

## Why these boundaries

- **Indexer separate from API:** the indexer runs as a job (nightly or on demand), the API as a long-running service. They scale, deploy and fail differently. The indexer owns the data model, which keeps the API small.
- **Frontend separate from API:** different technology and release cadence, and the OpenAPI contract between them is a visible, testable interface.

See the ADRs in [adr](adr) for the decisions behind this.
