# CohenStore optional grouped titles (staged)

This adds only `linked_source_id` metadata to seven developer-published direct items. The original 207 direct items remain in their order; all 12,205 store reference records and 18,046 additional source reference records remain unchanged.

The 0.5.16 console build ignores the new field. An independent private source patch implements **L2: Direct files / All listings / Grouped titles**. Both existing views remain intact. Only the optional Grouped titles view hides an explicitly paired source-page card and shows the original URL on the direct package card.

Exact source IDs prevent guessing pairings based on similar titles; source category must match and the original item must remain source-only. The separate RetroArch packages have no exact source pairing and are not combined.

Publisher release hashes and sizes were recorded, and header checks passed. Complete files and real console installation remain unverified. Do not advertise as console-tested and do not modify the public signing/feed keys.

No installed game, original source catalog, settings, saves, queues, or PKGs are altered. To roll back this metadata change, revert only the seven optional fields.
