# GSU — správne zaradenie balíka, 30. október 2026

Cieľová identita je `enigma2-plugin-extensions-gsu-warder-evolution`. Správca OpenATV rozdelí tento názov na kategóriu `extensions` a položku `gsu-warder-evolution`. PiconHub je už v rozšíreniach a FullHDGlass vo vzhľadoch; ich vnútorné identity sa nemenia.

Staré aktualizátory kontrolujú presný názov súboru aj vnútorný Package. Preto pôvodné adresy `plugin/update/candidate.json` a `restoration/update/candidate.json` zostanú na kompatibilnom r93 s pôvodnou identitou. Jeho aktualizátor číta nový `plugin/update/stable.json`, ktorý ponúkne r94 s požadovanou identitou. Inštalácia z r92: aktualizovať na r93, reštartovať GUI, otvoriť GSU a aktualizovať na r94. Nepreskakovať tento prechod ručnou inštaláciou r94 cez starší balík.

Aktualizátor r93 pred výmenou overí Package, verziu, veľkosť a SHA256, skontroluje verziu starej inštalácie a vytvorí iba dočasný stavový príznak migrácie. Pôvodný prerm r93 vtedy neobnovuje spravované nastavenia štartu CAM-u. Pri bežnom odstránení zostáva obnova aktívna. Po dokončení aj pri chybe sa príznak odstráni. Oba IPK sa overia pred odstránením starej identity. Pri zlyhaní sa odstráni nedokončená nová inštalácia a obnoví overený r93; ak zlyhá aj obnova, jej IPK zostane v stavovom priečinku pre opravu. Odstránenie a inštaláciu vykonáva opkg; databáza sa ručne neupravuje, aktualizátor nepoužíva force ani nereštartuje prijímač.

Pri čerstvej inštalácii sa použije `enigma2-plugin-extensions-gsu_13.40-r94_all.ipk`. Adresár `/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil` a existujúce používateľské konfigurácie zostávajú. Automatizované kontroly a verejné súbory sú v `reports/plugin-groups-20261030.json`; fyzické potvrdenie nového prechodu na boxe sa netvrdí.
