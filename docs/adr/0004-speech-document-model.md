# 0004: Speech document model

Date: 2026-11-24
Status: accepted

## Context

The first look at the Bundestag protocols (see `wortlaut-indexer/docs/source-format.md`) showed that a `rede` element is not the same as the speech of one person: it contains the interjections of the presiding officer, questions of other members and the reactions of the house. The XML also knows parliamentary groups, not parties. The initial field proposal had to be adjusted.

## Decision

- **One document is the text of one speaker within one `rede`.** Words of the presiding officer and of other members who ask intervening questions are not part of the document. Their reactions are not either: only reactions during the speaker's own words belong to the speech.
- **`speaker.faction` instead of `speaker.party`.** The source provides the parliamentary group (`fraktion`), normalised to one canonical spelling per group. It is `null` for members of the government without a group. A `party` field can be added once the member master data is used.
- **`text` is one field with a sub-field `text.exact`.** `text` uses the German analyzer (stemming) and `text.exact` the standard analyzer for exact phrases. A sub-field avoids storing the text twice and keeps highlighting working on both.
- **`reactions` are nested objects** with `type` (`applause`, `laughter`, `heckle`, `objection`), `source` and `text`, so a query can combine type, source and words of one reaction.
- **`delivery`** tells plenary speeches from written statements given to the record (`plenary`, `written_statement`).
- **The mapping is strict** (`dynamic: strict`). An unknown field is rejected instead of being mapped by guess, which turns schema drift into a failing import.
- **One shard, no replica** in the index template, because the first deployment is a single server.
- **Idempotency** works through the speech id (`<period>-<session>-<number>`) as document id and a SHA-256 `content_hash`. Unchanged speeches are not written again.

## Consequences

- Questions of other members and the words of the presiding officer cannot be searched yet. This can be added later as further documents without changing the existing ones.
- The API filter that was planned as `party` is called `faction` until a real party field exists.
- Changing a field type means a new index (`speeches-v2`) and an alias switch, as planned.
