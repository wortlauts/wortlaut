# Data sources and legal notes

Wortlaut is hosted publicly, so every data source has to be safe to redistribute. This page records what is allowed and what is not. It is not legal advice; check each source before adding it.

## Allowed

- **Plenary protocols (text).** Drucksachen and Plenarprotokolle are official works (amtliche Werke) and not protected by copyright under section 5 UrhG. See the [Bundestag imprint](https://www.bundestag.de/services/impressum). Machine-readable XML of all protocols is published on the [Bundestag Open Data page](https://www.bundestag.de/services/opendata). The CPP-BT corpus on [Zenodo](https://zenodo.org/records/18177196) is a ready-made compilation (1949 to 2026).
- **DIP API.** Needs an API key and a source attribution ("Deutscher Bundestag/Bundesrat - DIP"). See the [DIP API info sheet](https://dip.bundestag.de/documents/informationsblatt_zur_dip_api.pdf). The key is never committed.

## Link only

- **Bundestag audio and video.** The Bundestag owns the usage rights, and changes beyond the terms need its written approval ([Mediathek terms](https://www.bundestag.de/mediathek/nutzungsbedingungen-247892)). This material is never hosted, served for download, cut or re-encoded; it is only linked.

## Later

- **Freely licensed media** (public domain, CC BY and similar) may be used for listening, download and clipping, with automatic attribution.
- **Older corpora** (CPP-BT, Open Discourse and similar): check the licence of each corpus before use.

## Rules in the product

- Every indexed document carries a `rights` object (`license`, `attribution`, `allowed_actions`). The UI shows a download or clip action only if `allowed_actions` permits it.
- A quote is always shown with speaker, date and source, so it is not taken out of context.
