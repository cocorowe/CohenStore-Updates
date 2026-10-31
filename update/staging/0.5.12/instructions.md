# CohenStore 0.5.12 update test

This is a newly compiled 0.5.12 executable, not a renamed 0.5.11 package.
It uses update version code 512 and PS4 APP_VER 01.12 so that existing 0.5.11
and Windows-test 1.11 installs can receive a newer release. The title/content
identity and update signing identity are unchanged. Future version codes must
remain greater than 512.

On the console open Store Updates, press R3 and then X. After Update ready,
close CohenStore and install /data/pkg/CohenStore-512.pkg using GoldHEN's HDD
Package Installer. Reopen and confirm 0.5.12, then refresh Games with R3.
Game installation remains manual. The 0.5.10 shared-folder fix and 0.5.11
Archive support, longer receive timeout and validated resume/retry flow remain.

The live catalog has 119 entries, including 101 public Archive games.
The catalog uses checked public mirrors; restricted files are excluded.
Header, title-ID, byte-size and range checks do not prove a complete download
or PS4 launch compatibility. A full 166,002,688-byte Webbed transfer was verified
on the desktop engine in 0.5.11; the download engine is unchanged in this build.

Validation: 84 desktop app tests pass. The PS4 executable compiles, its package
passes digest/signature validation, and generated SFO metadata confirms APP_VER
01.12 and CHST00001. Actual installation and updater behavior require a PS4 test.
The current application source and private signing key are not included in the
public release upload. Older source archives already exist in repository history.
