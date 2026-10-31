# CohenStore 0.5.11 Archive support test

Internet Archive links and redirects are now accepted, following the user's
updated source preference. HTTPS downgrade and credential-in-URL checks remain.
The desktop and PS4 network adapters allow a 30-second connection setup and
60-second stalled receive interval. Interrupted downloads retain their existing
validated resume/retry flow; host authorization failures still stop promptly.
Existing shared installer-folder permissions remain unchanged (0.5.10 repair).

FPKGi JSON import preserves title IDs, game versions and regions, and percent-
encodes reserved path characters. This source repeats the same firmware and
release-date values for every entry; those values are not treated as verified
compatibility. Missing publisher SHA-256 values remain unknown.

Install 0.5.11 from Store Updates: R3, X, then close CohenStore and install
/data/pkg/CohenStore-61.pkg in GoldHEN. From 0.5.10 this uses its repaired
updater and does not require another USB transfer. Reopen and refresh Games
with R3 to load the filtered live catalog. GoldHEN installation stays manual.

Validation: 84 app tests pass. The native executable builds and its PKG passes
package validation. A real full desktop transfer of Webbed completed at
166,002,688 bytes, matched the Archive-listed MD5 and its catalog title ID,
and produced SHA-256 62cea09319376f5e49f293cf451a40bd02a36cf86e35f3f80308fb0fe809ec68.
This is not a publisher-authenticated digest or proof of PS4 installation.
Other catalog checks cover public metadata and bounded file prefixes only.
Private entries and failed HTTP checks are held out of the added catalog.


Packaging note: the 003/004 compressed-part boundary contains a five-byte overlap, which the workflow removes. A separate internal corruption remains in 003.gzpart (decompression fails about 12 KiB into that chunk), so publication is intentionally blocked until the staged archive is replaced and its signed package hash verifies.
