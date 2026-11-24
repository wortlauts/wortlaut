# 0003: English for everything technical, German for the UI

Date: 2026-11-24
Status: accepted

## Context

The product serves a German-speaking audience and quotes German text. The code and repos are also meant to be read by other developers as a portfolio. Mixing languages in identifiers and documentation makes both harder to read.

## Decision

Everything on the technical level is English: repo names, routes, query parameters, JSON fields, variables, identifiers, commit messages, issues, ADRs and READMEs. Only user-facing UI text is German. Frontend routes stay English (for example `/search` and `/speeches/[id]`), the texts shown on them are German.

The indexed speech text is German by nature and is stored and analysed as such (German analyzer for stemming).

## Consequences

- Code and documentation are readable for an international audience.
- UI strings are kept apart from code (for example in message files) so they can be edited without touching logic.
- Domain terms without a good English equivalent, such as Wahlperiode, are mapped to a fixed English name (`legislative_period`) and used consistently.
