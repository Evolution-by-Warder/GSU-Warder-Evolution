# GSU Warder Evolution — retencia vydaní (23.11.2026)

**Záväzné pravidlo vlastníka:** ponechať aktuálnu ostrú verziu a maximálne tri predchádzajúce ostré verzie. Žiadne rozšírenie na päť vydaní. Maž iba súbory či Releases bez aktívnych aktualizačných odkazov a po overení obnovy; historické commity/tagy, schválené podklady a používateľské údaje sa neprepisujú.

## Ostré vydania, ktoré zostávajú

- `v13.41-r4` (aktuálne)
- `v13.40-r95`
- `v13.40-r94`
- `v13.40-r93`

Sú to presne štyri aktuálne GitHub Releases. `plugin/update/stable.json` smeruje na r4; `plugin/update/candidate.json` **stále smeruje na r93** ako kompatibilný prechod zo starej opkg identity. Preto je r93 nielen historickým rollbackom, ale aj chráneným migračným medzistupňom. Bez jeho testovanej náhrady ho neodstraňuj.

V `main` nie sú historické inštalačné IPK v `packages/`, `build/` ani `dist/`; balíky patria do GitHub Releases, a `plugin/resources.tar.gz` je **funkčný zdrojový asset**, nie starý inštalačný balík. Existujúce `.github/workflows/cleanup-releases.yml` pracuje iba s explicitnou žiadosťou a kontrolami; jeho automatiku nerozširovať bez overeného návratového postupu.

Nové vydávanie musí rešpektovať maximálne štyri ostré verzie a zároveň migration exceptions, verzované URL, SHA, opkg identitu a používané súbory. Git história, testy, zdrojový kód, nastavenia a schválené CAM správanie zostávajú zachované.

Spoločný checkpoint: [FullHDGlass/docs/ECOSYSTEM-CLEANUP-CHECKPOINT-20261123.md](https://github.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/blob/main/docs/ECOSYSTEM-CLEANUP-CHECKPOINT-20261123.md).
