# H5N1 – model hrozeb, bezpečnost a právní hranice

## Co chráníme

1. Bezpečnost osob, obydlí a jiných letadel v okolí.
2. Vlastní bezpilotní systémy a jejich aktualizace, telemetrii a řídicí integritu.
3. Důvěryhodnost senzorových dat a predikcí.
4. Dokumentované, reprodukovatelné výsledky testování.

## Co považujeme za hrozbu

- Narušené nebo degradované spojení s vlastním dronem.
- Falešné/stará/podvržená telemetrická zpráva vůči vlastnímu testovacímu systému.
- Záměna identity mezi našimi virtuálními drony.
- Opotřebení motoru, napěťový pokles, nežádoucí vibrace.
- Nesoulad GNSS a inerciálních/optických senzorů.
- Špatná lokalizace a zastaralé mapové podklady.
- Kolize s překážkami nebo mezi vlastními Guardiany.
- Nezabezpečené API, neoprávněná změna konfigurace, ztráta auditních záznamů.
- Nesprávný závěr AI i při přesvědčivě znějícím vysvětlení.

Klasifikátor zvuku jiného dronu je **jen detektor technické třídy**, nikoli detektor nepřátel nebo oprávnění někoho napadat.

## Threat model – STRIDE zjednodušeně

| Hrozba | Typický případ | Ochrana | Měření |
|---|---|---|---|
| Spoofing | zpráva vydávána za Guardiana | autentizace uzlu + allowlist | procento odmítnutých nepovolených zpráv |
| Tampering | změněná telemetrie | podpis/HMAC zprávy | test integrity |
| Repudiation | zpětně popřené rozhodnutí | evidence událostí, korelace | úplnost a integrita logů |
| Information disclosure | uniklá poloha flotily | zabezpečený přenos a přístup | review oprávnění |
| Denial of service | zahlcený ingest | limity, backpressure, lokální fail-safe | chování při degradaci |
| Elevation of privilege | AI zasáhne do bezpečnostního jádra | striktní oddělení pravomocí | test nepovoleného přístupu |

## Prevence kolizí

Model může odhadnout vzdálenost do zastavení jako `v * t_reakce + v²/(2a)` pro jednoduchý přímočarý pohyb; to není garance zastavení multirotoru ve větru. Včetně GNSS, senzorové chyby, latence, výšky, mapové nepřesnosti a zbytkové energie musí být počítána **nejistotní obálka**. Detekce s nízkou důvěrou vede k omezení, nikoliv k prohlášení, že prostor je bezpečný.

Pro obytné budovy mají být zóny vyhýbání aktivní i tehdy, když mapa neobsahuje detailní model každé střechy. V testech rozlišuj budovu, rizikovou oblast pro lidi a známý bezpečný koridor.

### Priorita reakcí

1. Předej aktuální riziko bezpečnostnímu subsystému, nikoliv volně interpretované AI.
2. Pokus o bezpečné vyhnutí, pokud je řízení k dispozici a manévr zvyšuje celkovou bezpečnost.
3. Podle ověřené strategie přeruš misi nebo udržuj bezpečný stav.
4. Nepřikazuj pád či vypnutí motorů jako univerzální reakci nad obydleným územím.
5. Při vážné nejistotě nic neslibuj: zaznamenej omezení a vyžádej kontrolu operátora.

V prvním prototypu jsou tyto reakce **doporučení na obrazovce**, ne fyzické příkazy.

## Akustika a CV

Bezpečnostní data musí rozlišovat:
- false positive: zvuk techniky považovaný za dron;
- false negative: dron nezachycen;
- unknown: důkazy nestačí pro rozumný odhad modelu;
- known unknown: model není v trénovacím katalogu;
- out-of-distribution: zvuk je mimo zkušenost modelu.

Při tréninku odděl testovací data podle konkrétních nahrávacích sezení a dronů, nikoli jen po náhodných krátkých úsecích stejného záznamu. Měř F1, recall, precision, kalibraci confidence a výsledky dle prostředí. Omez uchovávání nahrávek, zejména pokud obsahují řeč osob.

## Rádio a elektronické působení

- **Přípustný produktový směr:** monitorování vlastního linku, kvalita komunikace, anomálie, pasivní sledování, šifrování a fail-safe při výpadku.
- **Laboratorní simulace:** softwarově simulovaný pokles kvality signálu, ztráta rámců, latence a oddělené testy anti-replay.
- **Mimo produkt:** reálné aktivní rušení jiných dronů, podvrhování jejich signálu, získávání cizího řídicího přístupu, přesměrování letové trasy cizího dronu.

Fyzikálně nelze spolehlivě zaručit, že vysílané rušení zasáhne výhradně určitý dron a nikdy telefony, navigaci či další komunikaci. Proto modul simulace elektronických hrozeb neobsahuje vysílací funkce.

## Rizika nasazení

- V ČR/EU platí pravidla UAS, provozní kategorie a omezení prostoru. U více dronů, autonomního provozu, BVLOS a rizikových scénářů se mohou uplatnit přísnější požadavky a povolení.
- Případný vývoz nebo transfer dvojího užití či obranné technologie vyžaduje právní posouzení. Vývoj pro inovativní program není sám o sobě povolením k provozu nebo exportu.
- Akustické/radio pozorování může podléhat pravidlům pro soukromí, frekvence a ochranu dat.
- Nástroj není certifikovaným řešením pro prevenci střetů, provoz v obytné zástavbě nebo navigaci.
- Před jakýmkoli reálným letem je nutné posoudit provozní rizika, pojištění, osoby na zemi, nouzové scénáře a vhodný testovací prostor.

## Kritické přejímací zkoušky

1. Nikdy neoznačit data za LIVE při simulačním zdroji.
2. Výpadek AI nesmí vypnout bezpečnostní logiku.
3. Neplatný podpis, neznámá identita, expirovaný čas nebo replay jsou odmítnuty.
4. Chybějící poloha/senzor znamená UNKNOWN, ne LOW.
5. Dráha předpokládaná modelem přetínající budovu vede k výstraze.
6. Výstup konkrétního modelu ze zvuku je dostupný jen s validovaným klasifikátorem; jinak UNKNOWN.
7. Žádná část systému nesmí spouštět skutečnou rušičku, aktivní protidronový zásah nebo útočný příkaz.
8. Každá bezpečnostní reakce musí mít stručně vysvětlený důvod a dohledatelný záznam.

## Politika vydání

Tým může veřejně zveřejnit otevřený zdrojový kód simulace, ale nesmí popisovat neotestované funkce jako nasazené. Kritické bezpečnostní změny musí projít code review, regresními testy a negativními scénáři.

Doporučené zdroje k ověření před fyzickým nasazením: oficiální dokumentace EASA, ÚCL a ČTÚ, aktuální dokumentace PX4/ArduPilot a bezpečnostní dokumentace konkrétního hardware. Zdroje a pravidla ověřovat při každém kroku reálného nasazení.
