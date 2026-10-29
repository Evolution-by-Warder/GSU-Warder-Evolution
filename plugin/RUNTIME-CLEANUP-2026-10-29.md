# GSU — kontrola prevádzkových zápisov, 29. 10. 2026

Prejdený celý inštalovaný zdrojový runtime: **47 Python modulov**, inštalačné skripty a pomocné procesy. Pre každý modul je uložený SHA256 v sprievodnom JSON zázname. Kontrola zahŕňa výstup do konzoly, súborové logy, atómové zápisy, pracovné priečinky a správanie pri chybe. Vývojové skripty bežiace na PC/CI nie sú diagnostika prijímača.

- Writelog a log_event sú tiché; nevytvárajú gsu.log ani gsu-softcam-autostart.log a rutinné udalosti neposielajú do konzoly.
- Odstránené všetky tri zápisy gsu-bitrate.log: štart merania, príkaz helperu aj úvodné vzorky. Výstup merania do GUI ostáva.
- df a dmesg používajú pamäť procesu bez tempinfo.tmp. Chybné alebo prázdne riadky df sa bezpečne preskočia.
- Automatická kontrola aktualizácie neprodukuje rutinný konzolový log; ručne vyvolaná chyba je naďalej zobrazená používateľovi.
- Skontrolované atómové zápisy CAM štartu, feedu, fstab a diagnostického exportu vrátane cleanup po chybe. Zálohy konfigurácie, session guard a zámky sú potrebné prevádzkové dáta.
- Diagnostický archív vzniká iba po ručnom vyžiadaní v menu; ide o používateľský export. Automatické diagnostické súbory sa nevytvárajú.

Inštalačné kroky odstránia iba presne pomenované vlastné staré logy, ak ide o bežné súbory a nie symbolické odkazy. Neodstraňujú cudzie logy ani všeobecné priečinky. Nastavenia, nainštalované picony a používateľské obrázky zostávajú zachované.

Kandidát je určený na overenie v prijímači. Statická kontrola a simulované Enigma2 rozhrania nepotvrdzujú fyzické správanie na všetkých boxoch. Produkčné aktualizačné feedy zostávajú nezmenené. Žiadne tvrdenie o čistení už bežiaceho prijímača: zmeny sa uplatnia po inštalácii nového balíka.
