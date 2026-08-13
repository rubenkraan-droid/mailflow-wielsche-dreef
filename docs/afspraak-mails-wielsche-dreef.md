# Afspraak-sequence Landgoed De Wielsche Dreef

Vier mails die pas gaan lopen nadat er een afspraak is gepland. Losse automation,
staat naast de nurture-flow van 15 mails en heeft niets met die nummering te maken.

Bron voor de opmaak: `build_mails.py`, lijst `AFSPRAAK_MAILS`. Output:
`afspraak-01.html` t/m `afspraak-04b.html`. **Wijzig nooit de gegenereerde HTML
rechtstreeks.**

---

## 1. Flowlogica

De tak volgt uit de tijd tussen instap en de afspraakdatum.

| Mail | Tak A (>= 14 dgn) | Tak B (7-13 dgn) | Tak C (2-6 dgn) |
|---|---|---|---|
| 1. Waar u straks staat | D+1 | | |
| 2. Maak er een dag van | T-10 | D+1 | |
| 3. Praktisch | T-3 | T-3 | D+1 |
| 4. Tot morgen | T-1 | T-1 | T-1 |

- **T-x** is een ActiveCampaign-wait op het datumveld `Afspraakdatum`, x dagen
  ervoor, om 19:00.
- **D+1** is een gewone wait van een dag na instap.
- Bij een afspraak **binnen 2 dagen** gaat er niets uit.

Dit is de enige plek waar de takverdeling staat; uit de HTML valt hij niet af te
lezen.

## 2. Velden in ActiveCampaign

Twee losse velden, geen samengestelde tag. Het mailadres afleiden uit de naam
(`%BETROKKEN_MAKELAAR%@recravas.nl`) breekt zodra het naamveld uit meer dan een
woord bestaat of op de default terugvalt.

| Veld | Default | Vulling per adviseur |
|---|---|---|
| `BETROKKEN_MAKELAAR` | `Uw Landgoedadviseur` | volledige naam |
| `MAKELAAR_EMAIL` | `willem@recravas.nl` | `voornaam@recravas.nl` |
| `Afspraakdatum` | leeg | datum van de afspraak, stuurt de T-x waits |

Verder gebruikt de sequence `%FIRSTNAME%` en `%UNSUBSCRIBELINK%`.
`%BETROKKEN_MAKELAAR%` staat in de ondertekening, `%MAKELAAR_EMAIL%` in de
voettekst. `%AFSPRAAKDATUM%` staat alleen in mail 3.

## 3. Vaste gegevens

| | |
|---|---|
| Adres | Kalverlandseweg 3, 4024 BT Eck en Wiel |
| Routelink | https://maps.app.goo.gl/tHEn4XUbYo5wUER5A |
| Telefoon dag zelf | 06 45657185 |
| Telefoon kantoor (voettekst) | 085 - 303 28 44 |
| Duur bezichtiging | twee uur |

## 4. Onderwerpregels en preheaders

Splittest uitsluitend op de onderwerpregel, zoals in de nurture-flow. De vier
mails delen per stuk een preheader tussen A en B.

| # | Onderwerp A | Onderwerp B | Preheader |
|---|---|---|---|
| 01 | Straks staat u er zelf | Uw bezoek aan het Landgoed nadert | Drie vragen om vast over na te denken |
| 02 | Maakt u er een dag van? | De Betuwe rondom het Landgoed | Ervaar ook de omgeving waarin het Landgoed ligt |
| 03 | Praktische informatie voor uw bezoek | Alles wat u vooraf wilt weten over uw bezoek | Route, parkeren en wat handig is om aan te trekken |
| 04 | Tot morgen op het Landgoed | Morgen ontvangen wij u op De Wielsche Dreef | Route en telefoonnummer, voor het geval dat |

## 5. Schrijfregels

- Consequent de u-vorm, `u` en `uw` met kleine letter.
- Aanhef `Beste %FIRSTNAME%,`, afsluiting `Met vriendelijke groet,`.
- Ondertekening met `%BETROKKEN_MAKELAAR%`, niet met het Landgoed. Dit wijkt
  bewust af van de nurture-flow: op dit punt kent de ontvanger de adviseur.
- Geen em-dashes, nergens.
- Nergens een tijdstip van de afspraak in de mails, alleen de datum.

---

## 6. Teksten

De opmaak komt uit de gedeelde template in `build_mails.py`; hieronder staat de
kale tekst per mail.

### Mail 1, Waar u straks staat

Kicker: Uw afspraak. Kop: Straks staat u er zelf.

> Beste %FIRSTNAME%,
>
> Uw afspraak op Landgoed De Wielsche Dreef staat gepland. Binnenkort staat u er zelf.
>
> De rust, de ruimte en de ligging aan de Nederrijn laten zich ter plaatse nu eenmaal beter ervaren dan in woorden of beelden. Op de plek zelf merkt u binnen een minuut of het klopt: hoe de zon staat, wat u hoort en hoeveel ruimte er werkelijk om u heen is.
>
> Het helpt wanneer u van tevoren weet waar u op let. Drie vragen die de meeste bezoekers pas achteraf stellen:
>
> - hoe u er wilt zitten, met de middagzon in de tuin of juist beschut,
> - wie er straks komen, alleen u samen of ook kinderen en kleinkinderen die blijven slapen,
> - hoe vaak u er denkt te zijn, enkele weekenden per jaar of om de week.
>
> De eerste bepaalt welke kavels voor u afvallen, nog voordat u naar de prijs kijkt. De tweede bepaalt hoeveel ruimte u nodig heeft, buiten net zozeer als binnen.
>
> U hoeft hierover nog geen besluit te hebben genomen. Maar wanneer u met deze vragen in gedachten over het terrein loopt, haalt u aanzienlijk meer uit uw bezoek.

### Mail 2, Maak er een dag van

Kicker: De omgeving. Kop: Maakt u er een dag van?

> Beste %FIRSTNAME%,
>
> U komt binnenkort naar Eck en Wiel. Uw bezoek gaat over de kavel en de opzet van het Landgoed, maar uiteindelijk brengt u uw tijd door in de omgeving eromheen. Daarom is dit een goed moment om ook die te leren kennen.
>
> Een aantal suggesties die u eenvoudig aan uw bezoek verbindt:
>
> **De veerpont naar Amerongen**
> Vanaf Eck en Wiel steekt u in enkele minuten de Nederrijn over. Aan de overzijde ligt Amerongen, met het kasteel en de bossen van de Utrechtse Heuvelrug. Een korte oversteek die telkens weer de moeite waard is.
>
> **Het Eiland van Maurik**
> Recreatiegebied met water, op korte afstand van het Landgoed. Een goede gelegenheid om te zien wat de omgeving te bieden heeft wanneer u hier met kinderen of kleinkinderen verblijft.
>
> **De uiterwaarden en de boomgaarden**
> De Betuwe is fietsland bij uitstek. De knooppuntenroutes langs de Nederrijn en door de fruitteelt lopen vlak langs het terrein. In het voorjaar staat alles in bloei, in het najaar kunt u bij de telers zelf terecht.
>
> **Rhenen**
> Iets verder weg, maar met Ouwehands Dierenpark en de Grebbeberg een dagvullende bestemming wanneer u met het hele gezin komt.
>
> Valt uw afspraak in de ochtend, dan houdt u de rest van de dag over om rond te kijken.

### Mail 3, Praktisch

Kicker: Praktisch. Kop: Praktische informatie voor uw bezoek.

> Beste %FIRSTNAME%,
>
> Uw afspraak op het Landgoed nadert. Hieronder vindt u de praktische informatie op een rij, zodat u daar verder niet over hoeft na te denken.
>
> **ADRES**
> Kalverlandseweg 3
> 4024 BT Eck en Wiel
>
> [knop: Bekijk de route]
>
> U kunt op het terrein parkeren; er is voldoende parkeergelegenheid.
>
> **DUUR**
> Houdt u rekening met ongeveer twee uur.
>
> **WIE U ONTVANGT**
> %BETROKKEN_MAKELAAR% is uw aanspreekpunt en beantwoordt al uw vragen. Geen standaardrondleiding, maar een persoonlijk gesprek: wij lopen samen over het terrein en u stelt onderweg uw vragen.
>
> **KLEDING EN SCHOEISEL**
> Wij adviseren stevige schoenen. Een deel van de kavels is nog niet ontwikkeld, waardoor u niet overal over verharde paden loopt.
>
> **KINDEREN**
> Kinderen zijn van harte welkom. Er is voldoende ruimte en zij mogen overal komen.
>
> **VERHINDERD?**
> Belt of appt u naar 06 45657185. Verzetten is snel geregeld en voorkomt dat er een plek in de agenda onbenut blijft.
>
> Tot %AFSPRAAKDATUM%.

### Mail 4, Tot morgen

Kicker: Morgen. Kop: Tot morgen op het Landgoed.

> Beste %FIRSTNAME%,
>
> Morgen bent u welkom op Landgoed De Wielsche Dreef. %BETROKKEN_MAKELAAR% ontvangt u ter plaatse.
>
> Kalverlandseweg 3
> 4024 BT Eck en Wiel
>
> [knop: Bekijk de route]
>
> Wij adviseren stevige schoenen; een deel van de kavels is nog niet ontwikkeld.
>
> Mocht er onverwacht iets tussenkomen, dan kunt u bellen of appen naar 06 45657185.

Elke mail sluit af met:

> Met vriendelijke groet,
> **%BETROKKEN_MAKELAAR%**
> Landgoed De Wielsche Dreef

---

## 7. Openstaande punten in de copy

Twee dingen die bij het overnemen opvielen en bewust zijn blijven staan:

- **Mail 1** kondigt drie vragen aan en licht er daarna twee toe ("De eerste
  bepaalt... De tweede bepaalt..."). De derde vraag, hoe vaak u er denkt te zijn,
  krijgt geen vervolg.
- **Mail 2** eindigt met "wanneer u met het hele gezin komt". De stijlregel in
  `README.md` schrijft voor om over vakantiegangers te praten en niet over
  gezinnen.
