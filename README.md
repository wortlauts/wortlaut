# Wortlaut

Wortlaut ("exact wording") is a search engine over German Bundestag speeches: type a word or a sentence and see where, when and by whom it was said before.

This repository is the **meta repo**. It holds the overview, architecture, decisions (ADRs), roadmap and a VS Code workspace. The code lives in separate repos under the [`wortlauts`](https://github.com/wortlauts) organisation.

> **Status (2026-11-24):** planning is done, phase 1 is starting. Nothing is deployed yet. The repositories are private for now.

## Repositories

| Repo | Content | Technology | When |
| --- | --- | --- | --- |
| `wortlaut` (this repo) | README, architecture, ADRs, roadmap, workspace | Markdown | phase 1 |
| `wortlaut-indexer` | load protocols, parse, write to Elasticsearch, own the index template and document schema | .NET worker / CLI | phase 1 |
| `wortlaut-api` | search, trend and speaker endpoints, OpenAPI contract | .NET web API | phase 1 |
| `wortlaut-frontend` | search, trend chart, speech detail, quote card | Next.js | phase 1 |
| `wortlaut-infra` | Docker Compose for local use, later Terraform, Helm, GitOps | Compose, Terraform, Helm | Compose in phase 1 |
| `wortlaut-cms` | collections, word of the day, editing | headless CMS | phase 2 |

Rule of thumb: one repo equals one deployable artifact with its own release cadence. See [docs/architecture.md](docs/architecture.md) for how they fit together.

## Documentation

- [docs/architecture.md](docs/architecture.md): repos, data flow and the contracts between them
- [docs/adr](docs/adr): architecture decision records
- [docs/roadmap.md](docs/roadmap.md): milestones for phase 1 and what comes after
- [docs/data-sources.md](docs/data-sources.md): data sources, licences and legal notes
- [brand](brand): corporate design with logos, icons, colours, fonts and usage rules (see [brand/README.md](brand/README.md))

## Working on all repos at once

Clone the repos as siblings into one folder and open `wortlaut/wortlaut.code-workspace` in VS Code:

```text
<workspace>/
  wortlaut/            this repo
  wortlaut-indexer/
  wortlaut-api/
  wortlaut-frontend/
  wortlaut-infra/
```

The workspace file lists only the repos that exist; add a folder entry when you clone another repo.

## Data and legal notes

Source data are the official plenary protocols of the Bundestag, which are official works and not protected by copyright (section 5 UrhG). Bundestag audio and video are only ever linked, never hosted. Details and sources are in [docs/data-sources.md](docs/data-sources.md). This is not legal advice.

## Language

Everything technical (repo names, code, routes, JSON fields, commits, issues, ADRs, READMEs) is in English. Only the user interface is German.
