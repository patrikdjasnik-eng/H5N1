# H5N1 – přejímací testy a metriky

## Princip

Modul není hotový tím, že má na dashboardu kartu. Musí mít reálný vstup, reprodukovatelnou implementaci, negativní scénář, chybové reakce a výsledky měření. Každý test zaznamená verzi softwaru, parametry, seed (pokud existuje), zdroj dat, očekávanou toleranci a log událostí.

## Regresní testy v simulačním jádru

Soubor backend/tests/test_h5n1.py kontroluje:

1. Předpověď střetu přímočaré trajektorie s 3D budovou.
2. Žádné hlášení kolize při letu směrem od překážky.
3. HIGH a doporučené přerušení při krátkém TTC.
4. UNKNOWN při stáří telemetrie přesahujícím limit.
5. HIGH při nízké baterii.
6. CRITICAL při poruše motoru.
7. Kontrolu nebezpečné vzdálenosti dvou vlastních dronů.
8. Výpočet jednoduché brzdné dráhy a validaci parametrů.
9. Ověření podpisu zprávy a zablokování přehrání stejného nonce.
10. Odmítnutí upravené zprávy a neznámé identity.
11. Scénář blízkosti budovy a negativní výsledek předletové kontroly při poruše.
12. Deterministický časový krok a odmítnutí neplatné délky kroku.
13. Odmítnutí nedefinovaného scénáře.
14. Ověření auditního řetězu a odhalení změny záznamu.

Tato sada testuje jednoduchou matematickou abstrakci a ochranu dat; **nedokazuje bezpečný let skutečného dronu**.

## Bezpečnostní scénáře – plán pokrytí

| Scénář | Měřená veličina | Očekávané pravidlo |
|---|---|---|
| Přímý let na budovu | čas do průniku 3D objemu | výstraha před překážkou |
| Let mimo budovu | falešná výstraha | neeskalovat bez důvodu |
| Sblížení Guardianů | minimální rozestup | dodržet konfigurovanou rezervu |
| Zastaralé údaje | stáří telemetrie | UNKNOWN |
| Slabý link | link quality | konzervativní výstraha |
| Porucha motoru | health flag | kritické upozornění |
| Vítr a turbulence | odchylka predikce | zatím není modelováno |
| Pád při výpadku napájení | oblast dopadu | zatím není modelováno |
| Neznámý zvuk | unknown detection | žádná vymyšlená značka |
| Ztráta Máši | dostupnost safety enginu | safety engine nesmí záviset na LLM |

## Metriky predikce

- TTC absolute error v sekundách oproti referenčnímu simulátoru.
- False alarm rate na hodinu testované simulace.
- Collision-risk recall nad registrem scénářů.
- Minimum separation v metrech; worst-case across all guardians.
- Latence vyhodnocení a deadline miss ratio.
- Počet nezpracovaných bezpečnostních výjimek.
- Chybovost stavu UNKNOWN a důvodů degradace.
- Konzistence auditního záznamu a reprodukovatelnost stejného scénáře.

Brzdná dráha používá přibližný vzorec v * t_reaction + v²/(2 * a). Není to záruka pro vícerotorový let ve větru ani při selhání aktuátorů.

## Akustická AI

Dvě oddělené úlohy: DRONE / NON-DRONE a klasifikace rodiny či typu. Obě vyžadují vlastní validační sadu. Měřit precision, recall, F1, confusion matrix, unknown rate a kalibraci confidence. Testovací data dělit podle nezávislých letových sezení, nikoli podle fragmentů stejné nahrávky. V závěrečném reportu oddělit pozemní mikrofon od mikrofonu na aktivně letícím Guardianu.

## Cybersecurity

Ověř odmítnutí neznámých identit, chybných podpisů, expirovaných časových značek a přehrávaných zpráv. Doplň test limitů velikosti vstupů, správy klíčů, autentizace API, dostupnosti offline a degradace spoje. HMAC v prototypu nepředstavuje kompletní produkční identitu.

## Vydávací brána

- Backend testy projdou.
- Frontend strict TypeScript kontrola a Vite build projdou.
- Žádné tajné přihlašovací údaje v repozitáři.
- Rozhraní nezobrazuje fiktivní data jako LIVE.
- Žádný modul nevysílá RF signály, neruší okolí ani nespouští fyzický útok.
- Nehotové schopnosti jsou výslovně označené jako PLANNED / HW REQUIRED.
- Změny kritických pravidel mají negativní regresní testy.
