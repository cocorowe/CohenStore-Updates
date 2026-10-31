# P1 reliability review, based on CohenStore 0.5.16

This development branch preserves main commit `8c17fa074db2e16001e2c43d63352da134184b34`. Both updater manifests remain at 0.5.16/code516/revision11. This PR does not publish an installer, a signed feed or private app source.

## Confirmed failures and changes

| Finding | Evidence | Change/status |
| --- | --- | --- |
| Optional full transfers ran on pushes | Actions run41245085899 executed the full-transfer step and downloaded16 files before HTTP500 for Quake | Fixed on this branch: explicit manual-event/Boolean guard and independent CLI event-file guard |
| Another automatic full-file workflow used 0.5.8 app code | check-game-download.yml unpacked the old public source ZIP on release pushes | Replaced with manual-only pinned 2048 file verification; it explicitly does not test the current native app |
| Host failure was indistinguishable from a bad package in overall failure reporting | Existing script returned one generic failure for HTTP500 and SHA mismatch | Separate source status, evidence, summary and exit policy: integrity error1; strict host-health failure2 |
| PR1's informational manifest is obsolete | It advertises0.5.15; main already has0.5.16 | Omitted; only still-relevant guard/classification/test ideas were ported |
| Public history includes two older source ZIPs | 71 reachable commits,274 non-PKG blobs and both ZIP contents were scanned | No credential patterns found in this bounded scan; no files/history were deleted or rewritten |

31 repository tests and actionlint1.7.12 pass locally. Tests check the manual-event matrix, missing/malformed input, CLI refusal before catalog/network access, metadata-only records, temporary HTTP/network errors, corruption, source-local404 and agreement between manifests. Existing format checks remain intact.

The external-host job deliberately uses `--strict-host-health`: temporary failures remain visible and fail that dedicated job with exit2. They are not silently suppressed or called corrupt packages. Catalog validation has its own workflow. Reports are always uploaded; a Markdown summary distinguishes unresolved hosts from integrity failures.

Only the first direct URL per record is probed at this milestone. A header success is Unverified. Working requires a completed transfer matching the catalog SHA-256, and still does not mean it installed on PS4. A404/410 applies to the checked URL, not other mirrors or the game. No commercial binary links or packages are added by this PR.

## Native work stays private

A matching private0.5.17-dev1 candidate adds PKG CUSA/content-ID checks, preserves content-ID metadata in saved queues, rejects existing zero-length destination collisions, and reuses an identical already-staged updater package instead of overwriting an unrelated file. Seven added native regression cases bring the local app suite to131 tests. The native source and candidate PKG are saved separately for the owner; they are not in this public PR. PS4 launch, filesystem calls, current menus and patches require console testing before release.

P0 rollback source/installer/feed snapshots were saved privately. No `/data/pkg` folder logic, custom `/data/FPKGi` data, signing identity, queue schema, menu configuration or existing catalog feeds are reset by the repository changes. Main is unchanged until the owner approves merging. New signed releases require separate approval.

## Remaining work

P2-P6 remain planned: normalized title grouping/provenance, launch refresh/change detection, lazy art cache, deeper mirror/storage work, dual layouts, expanded version-aware mod recovery and the optional AI/editor service. Do not label these completed from this PR. No live PS4 session or configured external AI/build service is available here.

References: [GitHub manual inputs and Boolean behavior](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow), [HTTP range and validator semantics](https://www.rfc-editor.org/rfc/rfc9110.html).
