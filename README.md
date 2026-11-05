# Runbook Mailflow Landgoed De Wielsche Dreef

Mozi Flow / 3-7-30-methode. Zelfde opzet als de Frankrijk-mailflow van Maison Pure.

**Live preview:** https://rubenkraan-droid.github.io/mailflow-wielsche-dreef/

---

## 1. Structuur

15 mails over 35 dagen, elk met een A- en een B-variant (splittest uitsluitend op onderwerpregel).

Mail 09 is herschreven. De oude mail 09 was een geschreven getuigenis van hetzelfde echtpaar
dat nu in de video van mail 03 aan het woord komt. Op dag 14 staat nu een nieuwe mail over de
aanname dat een eigen villa er niet in zit. Deze versie staat sinds 5 november 2026 ook in
ActiveCampaign.

Mails 01 tot en met 09 staan in ActiveCampaign, mails 10 tot en met 15 nog niet. Bij de mails
02, 04, 07 en 09 draagt elke variant zijn eigen HTML, dus ook zijn eigen `utm_content` (`...a`
respectievelijk `...b`). Bij 01, 03, 05, 06 en 08 bevat de B-variant nog de HTML van de
A-variant; daar is de splittest alleen in ActiveCampaign zelf meetbaar en niet verderop in de
attributie.

| Fase | Dagen | Ritme | Inhoud |
|---|---|---|---|
| Fase 1 | 1, 2, 3 | dagelijks | beste bewijs |
| Fase 2 | 5, 7, 9, 11, 13 | om de dag | een bezwaar per mail |
| Fase 3 | 14, 17, 21, 24, 28, 31, 35 | 2x per week | afwisselend verhaal en inzicht |

| # | Dag | Fase | Onderwerp A | Onderwerp B |
|---|---|---|---|---|
| 01 | 1 | 1 | Welkom bij Landgoed De Wielsche Dreef | Uw kennismaking met Landgoed De Wielsche Dreef |
| 02 | 2 | 1 | Waarom Landgoed De Wielsche Dreef direct aanspreekt | Niet alleen een villa, maar een plek die iets met u doet |
| 03 | 3 | 1 | Waarom zij drie parken vergeleken en hier bleven | Hoenderloo, Twente of de Betuwe? |
| 04 | 5 | 2 | Zullen we kennismaken op het Landgoed? | Ervaar zelf de sfeer, ligging en mogelijkheden |
| 05 | 7 | 2 | Hoe verloopt zo'n traject eigenlijk? | Van eerste gesprek tot de sleutel |
| 06 | 9 | 2 | Wat kost het onderhoud eigenlijk? | Wie regelt het beheer als u er niet bent? |
| 07 | 11 | 2 | Kan ik er zelf ook gewoon verblijven? | Hoeveel weken houdt u zelf beschikbaar? |
| 08 | 13 | 2 | Waarom de Betuwe, en niet de kust? | Wat maakt deze ligging bijzonder? |
| 09 | 14 | 3 | Zij dachten eerst dat het niets voor hen was | Wat als u denkt dat het er voor u niet in zit? |
| 10 | 17 | 3 | Wat een VvE-constructie voor u betekent | Hoe het beheer op het Landgoed is geregeld |
| 11 | 21 | 3 | Een dag op het Landgoed | Hoe een weekend hier eruitziet |
| 12 | 24 | 3 | Hoe de verhuur via Landal werkt | Wie zorgt er voor de vakantiegangers? |
| 13 | 28 | 3 | Niet elke plek op het Landgoed is hetzelfde | Waarom de ene kavel anders ligt dan de andere |
| 14 | 31 | 3 | Wat vakantiegangers zoeken in een villa | Waarom het type villa uitmaakt |
| 15 | 35 | 3 | Een laatste uitnodiging | Zullen we het gesprek plannen? |

---

## 2. Build-script

```bash
cd ~/Documents/Recraparcs/02\ Parken\ Nederland/Wielsche\ Dreef/Mailflows/Mailflow-WD-HTML/
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

## 3. Mailplatform en merge-tags

Deze flow draait in **ActiveCampaign**. In `build_mails.py` staat bovenaan `PLATFORM = "activecampaign"`;
zet die op `"ghl"` als de flow ooit naar HighLevel verhuist en draai het script opnieuw.

| Veld | ActiveCampaign | HighLevel |
|---|---|---|
| Voornaam | `%FIRSTNAME%` | `{{contact.first_name}}` |
| Achternaam | `%LASTNAME%` | `{{contact.last_name}}` |
| E-mail | `%EMAIL%` | `{{contact.email}}` |
| Telefoon | `%PHONE%` | `{{contact.phone}}` |
| Uitschrijven | `%UNSUBSCRIBELINK%` | `{{unsubscribe_url}}` |

`%UNSUBSCRIBELINK%` rendert in AC als een complete link, dus niet zelf in een `<a>` wikkelen.
Controleer in een testverzending hoe de link eruitziet.

## 4. Tracking en CTA

Elke CTA-link bevat:

```
?utm_source=email
&utm_medium=mailflow
&utm_campaign=wielsche-dreef
&utm_content=wd-mail-01a          (t/m wd-mail-15b, zonder 09)
&email={{contact.email}}
&first_name={{contact.first_name}}
&last_name={{contact.last_name}}
&phone={{contact.phone}}
```

Landingspagina: **https://invest.recraparcs.nl/wd-mailflow-lp-page** (live, in GHL).

Uitzondering: mail 03 wijst naar de videopagina **https://invest.recraparcs.nl/videopagina-page**.
Zowel de videoafbeelding als de knop linken daarheen, met dezelfde utm-opzet en prefill.
De still met afspeelknop (`video-eigenaren.jpg`) wordt gemaakt door `prep_images.py` en via
GitHub Pages gehost; e-mailclients spelen geen video af, dus het is een afbeelding met een link.
 De lokale `gesprek.html` is de bronversie/preview en geeft de querystring door aan het ingebedde GHL-formulier.

GHL-formulier `WD - Gesprek - Mail`, form-ID `gO63rpRMVuuC5mc2uFXc`, is ingebouwd in `gesprek.html`.

---

## 5. Automation (ActiveCampaign)

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

## 6. Pipedrive-koppeling via n8n

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

## 7. Afspraak-sequence

Naast deze nurture-flow draait een tweede, losse sequence: vier mails nadat er een
afspraak is gepland, verdeeld over drie takken op basis van de tijd tot de
afspraakdatum. Zelfde template en hetzelfde build-script, eigen nummering
(`afspraak-01.html` t/m `afspraak-04b.html`), staat als aparte sectie op de
indexpagina.

De takverdeling, de wait-stappen en de benodigde ActiveCampaign-velden staan in
[`docs/afspraak-mails-wielsche-dreef.md`](docs/afspraak-mails-wielsche-dreef.md).
Die logica valt niet uit de HTML af te lezen.

Extra merge-tags, alleen in deze sequence:

| Veld | ActiveCampaign | Default in AC |
|---|---|---|
| Adviseur | `%BETROKKEN_MAKELAAR%` | `Uw Landgoedadviseur` |
| Afspraakdatum | `%AFSPRAAKDATUM%` | leeg |

Het mailadres in de voettekst is geen merge-tag maar staat vast op
`willem@recravas.nl`, net als in de nurture-flow. De adviseur ondertekent de
mail; de voettekst blijft het algemene bedrijfsblok.

---

## 8. Stijlregels

- Geen emdashes in copy of onderwerpregels.
- Ondertekening zonder persoonsnaam ("Met vriendelijke groet, De Wielsche Dreef").
- Praat over vakantiegangers, niet over gezinnen.
- Geen kwantitatieve rendementsbeloftes.
- Disclaimer-footer in elke mail.
- Na elke wijziging: `python3 build_mails.py` en preview controleren.
