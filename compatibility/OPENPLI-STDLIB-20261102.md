# GSU 13.41-r3 — OpenPLi crash repair TEST

The reported OpenPLi 9.2 startup failure called eLabel.setWrap(0), which this image does not provide. Use setNoWrap(1), present in both OpenPLi and OpenATV, for ECM OSD, channel information and OSCam client details. No startup or validation checks are skipped.

Regression tests use strict labels without setWrap; the native matrix additionally checks these calls against the actual selected image C++ header. Existing no-dataclasses repair and all prior changes remain included. Production feeds unchanged. Receiver validation pending. Future normal GSU releases must be at least 13.41-r4.
