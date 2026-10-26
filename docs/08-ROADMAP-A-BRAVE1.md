# H5N1 – vývojový plán a podklady pro inovační partnery

## Fáze 0: bezpečný základ

Cílem je lokálně spustitelný projekt s českým manuálem, typově bezpečným webovým rozhraním, jednoduchým simulačním jádrem a testy. Status hotovo až po úspěšném CI; samotná existence souborů nestačí.

Akceptace: tři virtuální drony, šest scénářů, 3D budovy jako jednoduché objemy, risk report, audit a testovací příkazy.

## Fáze 1: robustní simulace

- Přidat realistický, ověřený fyzikální model nebo adaptér na oficiální SITL.
- Scénáře poruch motorů, ztráty GNSS, větru a energetických limitů.
- Nejistotní obálky, časové predikce střetu a ochranné zóny obytných budov.
- Model výšky, dynamické překážky, kontrola kolizí Guardianů.
- Reproducibilní generátor scénářů a export porovnávacího reportu.
- Oddělené riziko pro civilní okolí a dostupné nouzové přistání.

## Fáze 2: datová a kybernetická odolnost

- Identita a rotace klíčů vlastních uzlů; end-to-end šifrování vhodného datového kanálu.
- Sensor Trust Engine a validace freshness každého datového pole.
- Read-only audit vlastní avioniky přes explicitní allowlist.
- Incident report, archiv vstupů, offline replay.
- Simulátor nestabilního spoje, změn latence, výpadků a duplicit.
- Upevnit hranici mezi AI doporučením a safety engine.

## Fáze 3: pasivní vnímání

- Akustický detektor civilních dronů, s unknown kategorií.
- Katalog známých zvuků, licenční metadata, reprodukovatelná trénovací pipeline.
- Vizuální detektor dronu v offline testovacích záznamech.
- Pasivní RF modul jen s autorizovanými a legálními daty.
- Porovnání různých zdrojů s přiznanou mírou nejistoty.
- Máša vysvětluje výstupy, ale neurčuje nepřátelskost ani nepřebírá řízení.

## Fáze 4: hardware read-only

- Zvolit otevřený autopilot a ověřit dostupnost bezpečně čtené telemetrie.
- Sledovat latence, výpadky, výkon a přesnost senzorů na stole.
- Ověřit, že unplug senzoru přejde do degradovaného bezpečného stavu.
- Externí bezpečnostní revize, provozní postupy a právní posouzení.
- Žádné fyzické lety ve zástavbě během prototypování.

## Fáze 5: kontrolovaný terénní pilot

Teprve s příslušným povolením, pojistným a provozním rámcem; definovaná testovací oblast, kvalifikovaný pilot, nezávislé failsafe a evidence. Především měřit spolehlivost, nikoliv demonstrovat dramatické situace nad lidmi.

## BRAVE1 a evropské obranné inovace – prezentační rámec

H5N1 lze popisovat jako Drone Safety & Cyber Resilience Research Platform. Není vhodné jej označovat jako ověřenou vojenskou technologii, aktivní EW systém či funkční protivzdušnou obranu, dokud neexistuje nezávislé ověření a právní posouzení.

### Co přiložit k případné žádosti

1. Jednostránkový anglický executive summary zaměřený na bezpečnost a kybernetickou odolnost.
2. Architektonický diagram se zřetelnými safety hranicemi.
3. Reprodukovatelná demonstrace simulace, video i zdrojový kód.
4. Matice ověřených a dosud chybějících funkcí.
5. Naměřené metriky false alarm / detection recall a limitů modelu.
6. Postup bezpečného testování a rozhodování bez závislosti na AI.
7. Dokumentace autonomie systému, případných exportních omezení a odpovědnosti.
8. Jasně určené TRL, finanční plán a konkrétní kroky k testování, bez přikrášlování.

Podmínky konkrétní grantové výzvy se mění. Před podáním je třeba ověřit oficiální pravidla BRAVE1 a příslušnou legislativu, nikoliv se spoléhat na starší popis programu.

## Priorita

Nejdříve věrohodnost safety enginu, pak robustní infrastruktura, následně pasivní senzory a až jako poslední integrace reálného hardware. Žádný systém nejde prohlásit za „100 % bezpečný“.
