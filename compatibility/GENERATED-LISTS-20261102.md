# Generated plugin list fixes — 2 November 2026

These are new source changes after the 1 November compatibility work. FullHDGlass 1.0.61 remains the production skin; 1.0.62-test1 is unchanged. This branch is not a published plugin release and does not change installed versions, production feeds, package identities or artwork.

Lists now end on complete rows calculated from the actual rounded pixel row height. Merely shrinking the font does not remove a partly visible extra row. Tests cover 1280×720, 1366×768, 1920×1080, 2560×1440 and 3840×2160; main/settings/popups also cover 1920×1200. These checks validate generated XML and Python controllers, not physical receiver/GLES rendering.

History implements the owner's pending request: five installed version entries with at most two description lines each. Localized text and English fallback are retained; the complete source notes file is untouched.

## Changed behavior

- Main list: FHD viewport 759/58 formerly left five pixels of an extra row; it now ends at 754/58. Rounded HD rows are fitted within the existing allocation.
- Settings list: FHD viewport 650/48 now ends at 624/48, preserving its 25-pixel font, title, help area and footer.
- Embedded tools/swap lists now use the same 40-pixel reference row height as their controller, instead of XML 42/controller 40. Embedded config and editor lists also end on whole rows.
- History retains dates, localization and installed-version validation while showing five entries with two description lines.

## Verification

396 plugin tests pass locally. The existing OpenATV export/controller guard passes against official `8.0-next` commit `da455f57dda38b5f0de0744c913ee2270b7dc2ba` (40 exports, 33 contracts). CI additionally runs the complete suite on Python 3.9 and 3.14 alongside the existing stable 8.0 / 8.0-next / master interface matrix.

## Remaining scope

CAM workspace lists use the legacy `fhd()` sizing path, and OSCam log rows change height after receiving data. They need separate controller/row geometry work; this patch does not claim them fixed. Global legacy XML constants and helper-generated field bindings remain outside the literal AST audit. A uniquely versioned receiver candidate and receiver acceptance are still required before a functional release.
