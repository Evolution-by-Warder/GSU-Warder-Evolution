# GSU-Warder-Evolution – pravidlá pre prácu

Tieto bezpečnostné pravidlá dopĺňajú existujúcu dokumentáciu projektu a chránia produkčné súbory. Rozsah úloh a vlastníctvo príslušných komponentov zostávajú nezmenené.

## Bezpečnosť GitHub prístupu, autentifikácie a nahrávania

- Na všetky projektové repozitáre používaj iba už schválené a autorizované GitHub pripojenia a podporované operácie. Bez výslovného predchádzajúceho súhlasu vlastníka nemeň spôsob autentifikácie, neprechádzaj na nové webové prihlasovanie, nevytváraj tokeny a nežiadaj heslá, jednorazové 2FA kódy ani iné prihlasovacie tajomstvá.
- Ak narazíš na obmedzenie prenosu veľkých alebo binárnych súborov, zastav len dotknutý prenos, zaznamenaj presnú príčinu, chybu a možné bezpečné riešenia. Nový spôsob prihlasovania či prenosu vyžaduje predchádzajúce výslovné schválenie vlastníka. Bežné technické rozhodnutia v rámci už povoleného spojenia môžu pokračovať.
- Neopakuj bez konca zlyhávajúce Base64 uploady ani autentifikačné pokusy. Ak nie je dostupný bezpečný schválený prenos, zachovaj existujúce výsledky a jasne odlíš lokálne pripravené archívy od skutočne nahraných a overených súborov.
- Pracuj na oddelených vetvách a pred každým zásahom over cieľovú vetvu, SHA-256 a integritu už schválených súborov. Nečakaná zmena hashov je blokácia, nie dôvod na automatické prepísanie. Produkčné zlúčenie a publikovanie vyžadujú výslovný súhlas.
- Po každej bezpečne dokončenej dávke ulož overiteľný commit a aktualizuj príslušný projektový register s presným SHA, rozsahom testov, stavom uploadu a zostávajúcimi nespracovanými výstupmi. Bez overenia vzdialeného súboru a hashov netvrď, že upload bol úspešný.
