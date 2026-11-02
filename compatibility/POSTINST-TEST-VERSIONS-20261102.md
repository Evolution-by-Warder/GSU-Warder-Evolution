# Test-version installation repair — 2 November 2026

The owner reproduced PiconHub postinst status 1: `Invalid plugin version`. The 0.1.39-test1 runtime version was rejected by its own updater parser. The exact extracted published verifier reproduced the error. Earlier checks compiled package files but did not execute the installed-version parser; that coverage was insufficient.

PiconHub test2 accepts -testN for installed payload and updater checks. GSU test3 fixes the same parser gap in startup checks; its file-only installer check already passed. Production feeds still reject test releases, and a stable release with the same base version is not offered as a downgrade. Future normal versions remain PiconHub >=0.1.40 and GSU >=13.40-r96.

Both builders now execute their actual runtime version parser before packaging. Candidate workflows extract the final IPK and execute the exact shipped postinst verifier plus installed-version/update checks before publishing. The new gate reproduces the failed old PiconHub package and passes the repaired payload. No validation is skipped and no force installation is used. FullHDGlass 1.0.62-test2 needs no replacement for this issue.

Install the exact repaired filenames rather than every old IPK left in /tmp; restart GUI after both installers complete successfully. Public existing artifacts remain immutable. Previous PiconHub 0.1.39-test1 and GSU 13.40-r95-test1/test2 are superseded.
