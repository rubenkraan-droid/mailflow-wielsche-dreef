# Runbook Mailflow Landgoed De Wielsche Dreef

Mozi Flow / 3-7-30-methode. Zelfde opzet als de Frankrijk-mailflow van Maison Pure.

**Live preview:** https://rubenkraan-droid.github.io/mailflow-wielsche-dreef/

---

## 1. Structuur

15 mails over 35 dagen, elk met een A- en een B-variant (splittest uitsluitend op onderwerpregel).

| Fase | Dagen | Ritme | Inhoud |
|---|---|---|---|
| Fase 1 | 1, 2, 3 | dagelijks | beste bewijs |
| Fase 2 | 5, 7, 9, 11, 13 | om de dag | een bezwaar per mail |
| Fase 3 | 14, 17, 21, 24, 28, 31, 35 | 2x per week | afwisselend verhaal en inzicht |

| # | Dag | Fase | Onderwerp A | Onderwerp B |
|---|---|---|---|---|
| 01 | 1 | 1 | Welkom bij Landgoed De Wielsche Dreef | Uw kennismaking met Landgoed De Wielsche Dreef |
| 02 | 2 | 1 | Waarom Landgoed De Wielsche Dreef direct aanspreekt | Niet alleen een villa, maar een plek die iets met u doet |
| 03 | 3 | 1 | Comfort, eigen gebruik en professioneel beheer | Een sterk concept begint met rust en duidelijkheid |
| 04 | 5 | 2 | Zullen we kennismaken op het Landgoed? | Ervaar zelf de sfeer, ligging en mogelijkheden |
| 05 | 7 | 2 | Een eerste selectie van beschikbare mogelijkheden | Een aantal kavels binnen fase 2 is nu in beeld |
| 06 | 9 | 2 | Wat kost het onderhoud eigenlijk? | Wie regelt het beheer als u er niet bent? |
| 07 | 11 | 2 | Kan ik er zelf ook gewoon verblijven? | Hoeveel weken houdt u zelf beschikbaar? |
| 08 | 13 | 2 | Waarom de Betuwe, en niet de kust? | Wat maakt deze ligging bijzonder? |
| 09 | 14 | 3 | Het verhaal van een eigenaar van het eerste uur | Waarom zij drie parken vergeleken en hier bleven |
| 10 | 17 | 3 | Wat een VvE-constructie voor u betekent | Hoe het beheer op het Landgoed is geregeld |
| 11 | 21 | 3 | Een dag op het Landgoed | Hoe een weekend hier eruitziet |
| 12 | 24 | 3 | Hoe de verhuur via Landal werkt | Wie zorgt er voor de vakantiegangers? |
| 13 | 28 | 3 | Waarom fase 2 andere kansen biedt | De kavels die nu vrijkomen |
| 14 | 31 | 3 | Wat vakantiegangers zoeken in een villa | Waarom het type villa uitmaakt |
| 15 | 35 | 3 | Een laatste uitnodiging | Zullen we het gesprek plannen? |

---

## 2. Build-script

```bash
cd ~/Documents/Recraparcs/Wielsche\ Dreef/Mailflow-WD-HTML/
python3 build_mails.py
```

Genereert `mail-01.html` t/m `mail-15b.html` plus `index.html`.

- Merk-instellingen staan in `BRAND`, per-mail content in `MAILS`, hero-foto's in `IMG` en `HERO`.
- Output is 100% ASCII (accenten als HTML-entities), voorkomt tekencorruptie bij plakken in GHL.
- E-mail-veilige HTML: table-based, 600px, mobiel-responsive via media query.
- **Wijzig nooit de gegenereerde HTML rechtstreeks.** Pas het script aan en draai het opnieuw.

### Huisstijl

| Rol | Kleur |
|---|---|
| Primair (header, koppen) | `#1f524d` |
| Footer | `#123330` |
| Accent (kicker, CTA) | `#be5748` |
| Accent hover | `#9e4438` |
| Paginakleur | `#f0ebe3` |
| Tekst | `#374151` |

Koppen: Playfair Display 600. Body: Inter 400/600/700.
Logo: `https://dewielschedreef.nl/wp-content/uploads/2024/09/Logo-wit.svg`

---

## 3. Tracking en CTA

Elke CTA-link bevat:

```
?utm_source=email
&utm_medium=mailflow
&utm_campaign=wielsche-dreef
&utm_content=wd-mail-01a          (t/m wd-mail-15b)
&email={{contact.email}}
&first_name={{contact.first_name}}
&last_name={{contact.last_name}}
&phone={{contact.phone}}
```

Landingspagina: `gesprek.html` geeft de querystring door aan het ingebedde GHL-formulier.

**Openstaand:** het GHL-form-ID in `gesprek.html` staat nog op `VERVANG-DOOR-GHL-FORM-ID`. Vul het echte ID in zodra het formulier is aangemaakt.

---

## 4. GHL-workflow

- Wait-stappen volgens het dagschema (1, 2, 3, 5, 7, 9, 11, 13, 14, 17, 21, 24, 28, 31, 35).
- Time Window: werkdagen, rond 19:00.
- Allow re-entry: **uit**.
- Lange wait-stap achter mail 15 als vangnet.
- Exit-tag zodra iemand het formulier invult.
- Pre-Header in GHL leeg laten (zit al in de HTML).
- Splittest: alleen op onderwerpregel, zelfde HTML voor A en B.

### Formulier

Hidden field `utm_content`, Query Key exact `utm_content`.

### Instroom bestaande leads

Drip-modus met opwarmcurve: start rond 8 per dag, verdubbel elke paar dagen.
Rekenregel: leads per dag x 15 = mails per dag structureel.

---

## 5. Pipedrive-koppeling via n8n

Nieuwe webhook-tak in de bestaande workflow **"Notion CSV Ad Stats Import v3"** (n8n cloud, account mabekra), naar het voorbeeld van de bestaande mailflow-tak `ghl-vdc-lead`.

De WD-tak moet:
- de lead opzoeken in Pipedrive (Exact Match, Limit 1, Retry On Fail aan),
- de deal-stage bijwerken,
- een notitie toevoegen met bron-mail (`utm_content`) en voorkeurstijdstip.

**Openstaand:**
- De n8n-connector was tijdens het bouwen niet verbonden, dus de tak is nog niet aangemaakt.
- Pipedrive-pipeline en stage-ID's voor Wielsche Dreef moeten nog worden opgezocht en hier vastgelegd.

| Veld | Waarde |
|---|---|
| Webhook-pad | `ghl-wd-lead` (voorstel) |
| Pipedrive pipeline-ID | _nog invullen_ |
| Stage-ID bij formulierinvulling | _nog invullen_ |

---

## 6. Stijlregels

- Geen emdashes in copy of onderwerpregels.
- Ondertekening zonder persoonsnaam ("Met vriendelijke groet, De Wielsche Dreef").
- Praat over vakantiegangers, niet over gezinnen.
- Geen kwantitatieve rendementsbeloftes.
- Disclaimer-footer in elke mail.
- Na elke wijziging: `python3 build_mails.py` en preview controleren.
