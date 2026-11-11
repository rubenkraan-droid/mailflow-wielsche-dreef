#!/usr/bin/env python3
"""Genereert de tweede mailflow (15 mails) plus de conversiepagina.

Gebruik:  python3 build_v2.py

Bron: "De Wielsche Dreef - themas en mails final.docx". Tien themas, elk met
een eigen anker op de conversiepagina. Elke mail leidt naar het bijbehorende
thema en daar naar een uitklapformulier.

Deze flow staat los van build_mails.py: die blijft de huidige, in
ActiveCampaign draaiende reeks genereren. Alleen de template en de
opmaakhelpers worden hergebruikt, zodat beide reeksen er identiek uitzien.

Output staat in v2/ en is 100% ASCII.
"""
import pathlib

import build_mails as bm

BRAND = bm.BRAND
M = bm.M
P = bm.P
HI = bm.HI
IMG = bm.IMG

OUT_DIR = pathlib.Path(__file__).parent / "v2"

# De conversiepagina. Zolang de pagina niet in GoHighLevel staat, wijzen de
# mails naar de versie op GitHub Pages. Eenmaal in GHL: alleen deze regel
# aanpassen en het script opnieuw draaien.
CONV_URL = "https://rubenkraan-droid.github.io/mailflow-wielsche-dreef/v2/conversiepagina.html"

# Waar het uitklapformulier zijn inzending naartoe stuurt. Leeg betekent
# preview: het formulier toont dan een melding in plaats van te versturen.
FORM_ENDPOINT = ""


# ---------------------------------------------------------------- mail-helpers

def tracked(anchor, variant):
    """Utm-parameters en prefill achter de conversiepagina, met het anker
    erachter. De query moet voor het hekje staan, anders leest de browser hem
    als onderdeel van het anker."""
    return (CONV_URL + "?utm_source=email&utm_medium=mailflow"
            + "&utm_campaign=" + BRAND["campaign"]
            + "&utm_content=" + variant + "&" + BRAND["cta_prefill"]
            + "&thema=" + anchor.lstrip("#")
            + anchor)


def cta(label, anchor, variant):
    url = tracked(anchor, variant)
    return ('   <table role="presentation" cellpadding="0" cellspacing="0" style="margin:6px 0 20px 0;">'
            '<tr><td align="center" style="border-radius:4px; background-color:' + BRAND["accent"] + ';">'
            '<a class="btn" href="' + url + '" target="_blank" '
            'style="display:inline-block; padding:15px 32px; font-family:\'Inter\',Arial,sans-serif; '
            'font-size:16px; font-weight:bold; color:#ffffff; text-decoration:none; border-radius:4px;">'
            + label + ' &rarr;</a></td></tr></table>\n')


def bezoekregel(variant):
    """Vaste afsluiting onder de knop: de uitnodiging om langs te komen. Gaat
    naar het thema Aankoopproces, waar het bezoek wordt ingepland."""
    url = tracked('#aankoopproces', variant)
    return (P + 'U bent ook welkom om samen te komen kijken. '
            '<a href="' + url + '" target="_blank" style="color:' + BRAND["primary"]
            + '; font-weight:bold; text-decoration:underline;">Ik laat u graag het landgoed zien</a>.</p>\n')


SIGN = ('   <p style="margin:0;">Met vriendelijke groet,<br>'
        '<strong>Willem van de Griend</strong><br>'
        + BRAND["name"] + ' | ' + BRAND["contact_party"] + '<br>'
        '<a href="' + BRAND["phone_href"] + '" style="color:' + BRAND["primary"] + ';">'
        + BRAND["phone"] + '</a> | '
        '<a href="' + BRAND["email_href"] + '" style="color:' + BRAND["primary"] + ';">'
        + BRAND["email"] + '</a></p>\n')

quote = bm.quote
quote_person = bm.quote_person
bullets = bm.bullets
subhead = bm.subhead


# ------------------------------------------------------------------ de 15 mails

MAILS = [
 dict(n=1, hero="villa_avond", kicker="Beschikbare woningen",
  anchor="#beschikbare-woningen", link="Vraag de actuele beschikbaarheid aan",
  title='Welke villa past bij uw plannen?',
  preheader='Welkom op De Wielsche Dreef. Ontdek de woningtypen en de beschikbare plekken.',
  h1='Een eigen plek die bij u beiden past',
  body=(P + 'Hartelijk dank voor uw interesse in Landgoed De Wielsche Dreef. Misschien zag u in de brochure al een villa waarin u zichzelf ziet thuiskomen. Samen een paar dagen weg, de kinderen of vrienden erbij, en de ruimte om even niet met het werk bezig te zijn.</p>\n'
   + P + 'Bij Eck en Wiel, achter de dijk van de Nederrijn, ontstaat een landgoed waar rust, ruimte en comfort samenkomen. De vraag is niet alleen welke villa u mooi vindt, maar ook welke plek en indeling passen bij de manier waarop u uw vrije tijd wilt doorbrengen.</p>\n'
   + P + 'In fase 1 zijn er woningtypen voor 2 tot 12 personen, van comfort tot extra luxe en met bijzondere wellnessvarianten. Elk woningtype is gekoppeld aan een perceel. U kiest dus een woning &eacute;n de plek die daarbij hoort.</p>\n'
   + P + 'We verkopen wekelijks woningen, dus het aanbod verandert mee. We kijken graag met u naar de actuele beschikbaarheid, de ligging en de bijbehorende prijsinformatie. Zo krijgt u een concreet beeld van wat bij uw wensen past.</p>\n')),

 dict(n=2, hero="terras", kicker="Eigen gebruik",
  anchor="#eigen-gebruik-verhuur", link="Bespreek uw wensen voor eigen gebruik",
  title='Een eigen villa: wanneer zou u er samen naartoe gaan?',
  preheader='Van een paar dagen met z&rsquo;n twee&euml;n tot tijd met familie en vrienden.',
  h1='Vrije tijd die echt van u is',
  body=(P + 'Als u veel verantwoordelijkheid draagt, is vrije tijd niet altijd vanzelfsprekend. Juist dan kan een vaste plek prettig zijn: u hoeft niet steeds opnieuw een verblijf te zoeken en weet waar u samen naartoe kunt.</p>\n'
   + P + 'Misschien denkt u aan een lang weekend na een drukke periode. Of aan een week met familie, met genoeg ruimte voor iedereen. Hoe u de villa wilt gebruiken, is een goed vertrekpunt voor uw keuze.</p>\n'
   + P + 'Op De Wielsche Dreef kunt u kiezen voor uitsluitend recreatief eigen gebruik, of voor een combinatie met verhuur via Landal. Bij die combinatie kunt u maximaal 90 dagen per jaar voor eigen gebruik blokkeren, volgens de reserveringsvoorwaarden. Tijdig plannen is daarbij belangrijk: bestaande boekingen en reserveringsafspraken tellen mee.</p>\n'
   + bullets([
       'In welke periodes wilt u graag zelf kunnen komen?',
       'Met wie wilt u de villa delen?',
       'Wilt u daarnaast verhuren, of juist niet?',
   ])
   + P + 'We bespreken graag wat uw antwoorden betekenen voor de mogelijkheden, de kosten en de eventuele verhuur. Permanente bewoning is niet toegestaan.</p>\n')),

 dict(n=3, hero="villa_water", kicker="Verhuur en rendement",
  anchor="#eigen-gebruik-verhuur", link="Meer over rendement",
  title='Zelf genieten en verhuren: hoe werkt dat in de praktijk?',
  preheader='Landal verzorgt de verhuurbemiddeling. U wilt weten wat dat voor u betekent.',
  h1='Een eigen plek, met een helder verhuurconcept',
  body=(P + 'Uw villa zelf gebruiken en in andere periodes laten verhuren: die combinatie kan aantrekkelijk zijn. Maar u wilt vooraf wel weten wie wat regelt en hoe opbrengsten en kosten samenhangen.</p>\n'
   + P + 'Bij verhuur op De Wielsche Dreef verzorgt Landal de exclusieve verhuurbemiddeling en promotie. Woningen van hetzelfde type worden samen in een verhuurpool ondergebracht. De opbrengsten van die pool worden na aftrek van kosten verdeeld over de deelnemende woningen.</p>\n'
   + P + 'Dat betekent niet dat u ieder verblijf zelf hoeft te organiseren. Het betekent w&eacute;l dat u duidelijke afspraken maakt over verhuur, eigen gebruik en de bijbehorende dienstverlening.</p>\n'
   + P + 'Ook het participatierendement hoort in dat gesprek thuis: het verwachte rendement uit deelname aan de verhuur, in verhouding tot uw investering. Het is geen vaste of gegarandeerde opbrengst. Kosten, verhuurresultaten en uw eigen gebruik hebben er invloed op.</p>\n'
   + P + 'Wilt u de villa vooral voor uzelf, of zoekt u juist een combinatie? Ik neem de mogelijkheden en uitgangspunten graag met u door. Zo kunt u thuis samen verder praten op basis van een helder verhaal.</p>\n')),

 dict(n=4, hero="keuken", kicker="Kosten",
  anchor="#werkelijke-kosten", link="Meer inzicht in de kosten",
  title='Wat kost een eigen villa, ook na de aankoop?',
  preheader='Een overzicht van de investering, de terugkerende kosten en eventuele verhuur.',
  h1='Het hele plaatje op tafel',
  body=(P + 'Een villa kan u direct aanspreken. Toch wilt u pas verder kijken als ook het kostenplaatje klopt. Zeker als u samen beslist, is het prettig om allebei dezelfde informatie te hebben.</p>\n'
   + P + 'De tuin, het terras en de parkeerplaats worden aangelegd en zijn inbegrepen in de koopsom. De koopsommen zijn exclusief btw en vrij op naam. Voor verhuur is daarnaast een compleet inventarispakket nodig dat voldoet aan de eisen van Landal.</p>\n'
   + P + 'Bij een zorgvuldige afweging kijkt u naar:</p>\n'
   + bullets([
       'de koopsom en de onderdelen die wel en niet zijn inbegrepen,',
       'de inrichting en eventuele keuzemogelijkheden,',
       'de parkbijdrage, het onderhoud en de reserveringen,',
       'energie, verzekeringen en lokale lasten,',
       'bij verhuur: de kosten van verhuur en dienstverlening.',
   ])
   + P + 'We nemen dit graag voor de villa van uw voorkeur met u door. Niet alleen de losse bedragen, maar ook wat uw manier van gebruik betekent voor het totaal. Financi&euml;le en fiscale vragen kunt u vervolgens met uw eigen adviseur beoordelen.</p>\n')),

 dict(n=5, hero="betuwe", kicker="Park en omgeving",
  anchor="#park-omgeving", link="Meer weten over de fasen van het park",
  title='Een plek om naar terug te keren, midden in de Betuwe',
  preheader='Ruimte, rivierlandschap en tijd samen, bij Eck en Wiel.',
  h1='Even uit de dagelijkse verantwoordelijkheid',
  body=(P + 'Na een volle week wilt u niet per se een volle agenda. Misschien wilt u eerst gewoon aankomen. De deur open, samen iets drinken en weten dat er even niets hoeft.</p>\n'
   + P + 'De Wielsche Dreef ligt bij Eck en Wiel, achter de dijk van de Nederrijn. Boomgaarden, uiterwaarden en water geven de omgeving haar karakter. U kunt er wandelen en fietsen, of juist bij uw villa blijven. Aan de overkant van de rivier liggen onder meer Amerongen en de Utrechtse Heuvelrug.</p>\n'
   + P + 'Een eigenaar beschreef het zo:</p>\n'
   + quote('We fietsen regelmatig, lekker de omgeving verkennen. Het voelt als een stukje thuiskomen met familie en vrienden.')
   + P + 'Juist die afwisseling maakt de plek interessant: tijd met z&rsquo;n twee&euml;n, een verblijf met familie en ruimte om uw eigen ritme te volgen.</p>\n'
   + P + 'Het landgoed wordt in fasen ontwikkeld. We laten u daarom niet alleen zien hoe het is bedoeld, maar bespreken ook wat er op dit moment is en wat nog volgt. Dan weet u wat u tijdens een bezoek of verblijf kunt verwachten.</p>\n')),

 dict(n=6, hero="water_villas", kicker="Eigenaren aan het woord",
  anchor="#park-omgeving", link="Meer lezen over hun verhaal",
  title='Waarom deze eigenaren voor een villa aan het water kozen',
  preheader='Hun ervaring met de natuur, het uitzicht en het verblijf zelf.',
  h1='Hoe een plek een eigen plek wordt',
  body=(P + 'Een brochure laat u zien hoe een villa eruitziet. Eigenaren kunnen vertellen wat een verblijf er voor hen bijzonder maakt. De eigenaren van een vierpersoonswoning aan het water verwoorden hun eerste indruk zo:</p>\n'
   + quote_person(
       'Prachtig gebied. Echt heel natuurvriendelijk en vogelrijk. We zijn allebei gek op vogels, '
       'maar ook op het landschap en de manier waarop het park zich daarin ontwikkelt.',
       'eigenaren', 'Eigenaren op Landgoed De Wielsche Dreef',
       'Eigenaren van een vierpersoonswoning aan het water')
   + P + 'En over hun uitzicht vertellen zij:</p>\n'
   + quote('We kijken zo uit over het water. Vanmorgen deden we de gordijnen open en zwom er een meerkoet met kleintjes voorbij. Dat is toch een cadeautje? Zo begin je je dag.')
   + P + 'Hun verhaal maakt concreet wat op een plattegrond minder zichtbaar is: de ligging bepaalt mede hoe u uw villa beleeft. Misschien zoekt u net als zij uitzicht op het water. Misschien vindt u vooral privacy of ruimte voor uw gezelschap belangrijk.</p>\n'
   + P + 'Wat zou voor u beiden de doorslag geven? We laten u graag zien welke plekken bij die wensen aansluiten.</p>\n')),

 dict(n=7, hero="villa_parasol", kicker="Aankoopproces",
  anchor="#aankoopproces", link="Bekijk de stappen van het aankoopproces",
  title='Van kennismaking tot sleutel: zo verloopt de aankoop',
  preheader='Overzichtelijke stappen, met ruimte om samen af te wegen.',
  h1='Weten waar u aan begint',
  body=(P + 'Een eigen vakantievilla koopt u niet tussen twee afspraken door. U wilt de plek ervaren, de mogelijkheden begrijpen en samen kunnen afwegen of de aankoop bij uw plannen past.</p>\n'
   + P + 'Daarom maken we het traject graag overzichtelijk:</p>\n'
   + bullets([
       'Kennismaken: uw wensen, vragen en manier van gebruik bespreken.',
       'Het landgoed bezoeken en de ligging van de beschikbare villa&rsquo;s bekijken.',
       'Een voorstel doornemen, met prijs, uitvoering, keuzes en kosten.',
       'Uw financi&euml;le mogelijkheden beoordelen, zo nodig met uw eigen adviseur.',
       'De koopafspraken vastleggen en de notari&euml;le overdracht voorbereiden.',
       'Tussentijdse updates over de bouw en de ontwikkelingen ontvangen.',
       'De oplevering en het eigen gebruik of de verhuur voorbereiden.',
   ])
   + P + 'Welke keuzes in uitvoering of inrichting mogelijk zijn, hangt af van de villa en de gemaakte afspraken. Die nemen we mee voordat u beslist.</p>\n'
   + P + 'U hoeft bij een eerste gesprek nog niet te weten welke woning het moet worden. Het is juist een moment om te ontdekken of een volgende stap zinvol is. Ik begeleid u daarbij persoonlijk, met ruimte voor uw vragen en die van uw partner.</p>\n')),

 dict(n=8, hero="wandelen", kicker="Uitnodiging", geen_bezoekregel=True,
  anchor="#aankoopproces", link="Plan een bezoek of een online kennismaking",
  title='Kom samen kijken: wat wilt u ter plekke weten?',
  preheader='Ervaar de ligging en bespreek direct de vragen die voor u tellen.',
  h1='Een bezoek maakt uw keuze concreter',
  body=(P + 'Op foto&rsquo;s ziet u de uitstraling. Op locatie merkt u hoe de ruimte voelt, wat de ligging voor u doet en of u zichzelf hier samen ziet terugkomen.</p>\n'
   + P + 'Daarom nodigen we u graag uit voor een persoonlijke kennismaking op De Wielsche Dreef. Neem gerust uw partner mee. Juist als uw aandachtspunten verschillen, is het waardevol om dezelfde plek te zien en uw vragen samen te bespreken.</p>\n'
   + P + 'Tijdens het bezoek vertellen we onder meer over:</p>\n'
   + bullets([
       'de opzet van het landgoed en de actuele fase van ontwikkeling,',
       'de beschikbare woningtypen, percelen en, waar mogelijk, een villa,',
       'uw plannen voor eigen gebruik en eventuele verhuur,',
       'inzicht in de opbrengsten en het rendement,',
       'de kosten en de vervolgstappen die u wilt verkennen.',
   ])
   + P + 'U hoeft niets te beslissen tijdens de rondleiding. Het doel is dat u met een duidelijker beeld naar huis gaat: van de plek, van de mogelijkheden en van de vragen die nog openstaan.</p>\n'
   + P + 'Wilt u liever eerst kort telefonisch of online kennismaken? Dat kan ook. Ik stem graag met u af wat op dit moment het prettigst is.</p>\n')),

 dict(n=9, hero="woonkamer", kicker="Persoonlijke match",
  anchor="#persoonlijke-match", link="Bespreek wat bij u beiden past",
  title='Wat moet een eigen villa u beiden brengen?',
  preheader='Niet alleen een mooie woning, maar een keuze die bij uw leven past.',
  h1='Uw wensen hoeven niet hetzelfde te zijn',
  body=(P + 'Misschien kijkt u eerst naar de investering, terwijl uw partner zich afvraagt hoe vaak u er samen echt naartoe gaat. Of is het precies andersom. Voor een goede keuze zijn beide vragen belangrijk.</p>\n'
   + P + 'Wat zoekt u in een eigen vakantievilla? Een vaste plek om afstand te nemen van het werk? Meer tijd met familie en vrienden? Of een combinatie van zelf genieten en verhuur?</p>\n'
   + P + 'De antwoorden helpen om gericht te kijken:</p>\n'
   + bullets([
       'Met wie wilt u er verblijven en hoeveel ruimte heeft u nodig?',
       'Welke ligging en welk comfort zijn voor u belangrijk?',
       'Welke periodes wilt u zelf gebruiken?',
       'Wat wilt u uit handen geven en wat wilt u financieel helder hebben?',
   ])
   + P + 'U hoeft uw plannen nog niet volledig uitgedacht te hebben. Een gesprek kan juist helpen om uw wensen naast elkaar te leggen en te zien waar ze samenkomen.</p>\n'
   + P + 'Ik denk graag met u mee over woningtype, ligging, gebruik en kosten. Niet vanuit de vraag welke villa er verkocht moet worden, maar of er een villa is die bij uw plannen past.</p>\n')),

 dict(n=10, hero="villa_riet", kicker="Uw vragen",
  anchor="#persoonlijke-match", link="Stel uw vraag",
  title='U hoeft nog niet te weten of het kan',
  preheader='Een eerste gesprek is er juist voor de vragen die nog openstaan.',
  h1='Eerst uitzoeken, dan samen beslissen',
  body=(P + 'Soms spreekt een plek u meteen aan, terwijl u nog niet weet of een aankoop past: qua gebruik, qua moment of financieel. Dat is geen reden om uw vragen voor u te houden.</p>\n'
   + P + 'In het verhaal van de eigenaren van een vierpersoonswoning aan het water begon het ook met belangstelling &eacute;n twijfel over de mogelijkheden. Zij gingen in gesprek en bekeken het landgoed. Over de plek zeggen zij:</p>\n'
   + quote('Vanaf het eerste moment heeft het ons niet meer losgelaten. En ook de zonsopgang is hier prachtig.')
   + P + 'Hun ervaring zegt natuurlijk niet wat voor u haalbaar of passend is. Dat hangt af van uw eigen situatie, de villa en de manier waarop u die wilt gebruiken. Maar u hoeft ook niet alles al te weten voordat u contact opneemt.</p>\n'
   + P + 'Misschien wilt u eerst &eacute;&eacute;n vraag beantwoord hebben. Over de investering, de voorwaarden voor eigen gebruik of de vraag wat er nog beschikbaar is. Daar begin ik graag mee.</p>\n'
   + P + 'Een vraag stellen is nog geen aankoopbeslissing. U krijgt informatie, bespreekt die samen en bepaalt vervolgens zelf of u verder wilt kijken.</p>\n')),

 dict(n=11, hero="villa_vijver", kicker="Service en beheer",
  anchor="#privileges", link="Ontdek hoe service en beheer zijn geregeld",
  title='Een eigen villa, zonder alles zelf te organiseren',
  preheader='Wie regelt de verhuur, het groen en het gezamenlijke onderhoud?',
  h1='Geen tweede agenda vol beheertaken',
  body=(P + 'Een eigen villa moet u ontspanning opleveren, geen extra werk. Daarom is het belangrijk om vooraf te weten wat er wordt geregeld en wat bij u blijft liggen.</p>\n'
   + P + 'Op De Wielsche Dreef zijn verhuur en gezamenlijk beheer georganiseerd:</p>\n'
   + bullets([
       'Bij verhuur verzorgt Landal de exclusieve verhuurbemiddeling en promotie.',
       'Via de Vereniging van Eigenaars worden gezamenlijke belangen en onderhoud georganiseerd.',
       'Ook het onderhoud aan de buitenzijde van de woning, het terras en de tuin loopt via de VvE.',
   ])
   + P + 'Dat neemt praktische werkzaamheden uit handen. Tegelijk blijft u eigenaar, met de bijbehorende bijdragen, verantwoordelijkheden en afspraken. Dienstverlening betekent dus niet dat alles kosteloos of onbeperkt inbegrepen is.</p>\n'
   + P + 'Ik licht graag toe hoe de taken zijn verdeeld, welke kosten erbij horen en hoe eigen gebruik wordt gepland. Zo weet u vooraf wat u kunt uitbesteden en waarover u zelf beslissingen neemt.</p>\n'
   + P + 'Het uitgangspunt is eenvoudig: meer ruimte om van uw villa te genieten, met heldere afspraken over wat daarvoor nodig is.</p>\n')),

 dict(n=12, hero="slaapkamer", kicker="Uitvoering",
  anchor="#duurzaamheid", link="Meer over uitvoering en duurzaamheid",
  title='Comfort ziet u. De uitvoering wilt u ook begrijpen.',
  preheader='Over gasloos bouwen, installaties en de groene opzet van het landgoed.',
  h1='Prettig verblijven, verder kijken dan de inrichting',
  body=(P + 'Een mooie afwerking valt direct op. Maar als u samen een villa overweegt, wilt u ook weten hoe het binnen voelt in verschillende seizoenen en welke keuzes achter dat comfort zitten.</p>\n'
   + P + 'De villa&rsquo;s zijn gasloos en worden uitgevoerd met triple glas, een warmtepomp en zonnepanelen. Dat zijn relevante onderdelen wanneer u kijkt naar comfort en energiegebruik. Wat dit voor de energiekosten betekent, hangt onder meer af van het woningtype, het gebruik en de tarieven.</p>\n'
   + P + 'Ook de omgeving hoort bij die afweging. Bestaande bomen en karakteristieke watergangen blijven zoveel mogelijk behouden. Waterpartijen versterken het groene karakter van het landgoed.</p>\n'
   + P + 'Voor u zijn misschien juist het binnenklimaat, het onderhoud of de technische uitvoering doorslaggevend. Die vragen bespreken we graag aan de hand van de villa die u overweegt. Dan blijft duurzaamheid niet bij een algemene belofte, maar wordt duidelijk waar u naar kijkt.</p>\n'
   + P + 'Ik neem de uitvoering en de beschikbare specificaties graag met u door. Zo kunt u uitstraling &eacute;n praktische kwaliteit meenemen in uw keuze.</p>\n')),

 dict(n=13, hero="badkamer", kicker="Eigendom",
  anchor="#waarde-kwaliteit", link="Meer over eigendom en kwaliteit",
  title='Wat koopt u precies, en wat regelt u samen?',
  preheader='Meer over het appartementsrecht, uw priv&eacute;gedeelte en de VvE.',
  h1='Een eigen plek, met duidelijke eigendomsafspraken',
  body=(P + 'De sfeer en de ligging kunnen u overtuigen om verder te kijken. Maar voordat u koopt, wilt u ook begrijpen wat u juridisch in bezit krijgt en hoe het landgoed op langere termijn wordt onderhouden.</p>\n'
   + P + 'De Wielsche Dreef wordt gesplitst in appartementsrechten. Daarbij hoort het exclusieve gebruik van uw priv&eacute;gedeelte: de recreatiewoning met bijbehorende tuin, terras en parkeerplaats(en). Daarnaast deelt u volgens de splitsingsstukken in de gemeenschappelijke delen.</p>\n'
   + P + 'Als eigenaar wordt u automatisch lid van de Vereniging van Eigenaars. Via de VvE worden gezamenlijke belangen, bijdragen en onderhoud georganiseerd. Denk aan het groen, de wegen, de waterpartijen en de gemeenschappelijke voorzieningen.</p>\n'
   + P + 'Dat is niet alleen een juridisch onderwerp. Het gaat ook over hoe de plek waar u graag komt verzorgd blijft, en welke afspraken en reserveringen daarvoor nodig zijn.</p>\n'
   + P + 'Een goede ligging en verzorgd onderhoud zijn relevante aandachtspunten, maar garanderen geen toekomstige verkoopprijs. Ik neem de eigendomsstructuur en de beschikbare stukken graag met u door, zodat u weet wat u koopt en welke verplichtingen erbij horen.</p>\n')),

 dict(n=14, hero="fietsen", kicker="Vergelijken",
  anchor="#waarde-kwaliteit", link="Bekijk wat u koopt en hoe kwaliteit wordt beheerd",
  title='Waarom zij meerdere parken vergeleken en voor deze plek kozen',
  preheader='Een eigenaar over de uitstraling die voor hen het verschil maakte.',
  h1='Vergelijken helpt om te weten wat u belangrijk vindt',
  body=(P + 'Als u samen een vakantievilla overweegt, is vergelijken logisch. Niet alleen op prijs of aantal slaapkamers, maar ook op uitstraling, ligging en het gevoel dat u bij een plek krijgt.</p>\n'
   + P + 'Een echtpaar dat op De Wielsche Dreef kocht, bekeek eerst parken bij Hoenderloo, in Twente en in Belgi&euml;. Voor hen gaf de uitstraling van de villa&rsquo;s hier de doorslag. Een van hen verwoordt het zo:</p>\n'
   + quote('Ik vond het park er eigenlijk heel erg uitspringen.')
   + P + 'Dat is hun persoonlijke ervaring. Uw eigen vergelijking kan op andere punten uitkomen. Daarom helpt het om samen een paar vragen op een rij te zetten:</p>\n'
   + bullets([
       'Past de woning bij de manier waarop u wilt verblijven?',
       'Spreken de ligging en de opzet van het park u beiden aan?',
       'Zijn de kosten, gebruiksvoorwaarden en het beheer voldoende duidelijk?',
       'Kunt u zich voorstellen hier ook over een paar jaar graag te komen?',
   ])
   + P + 'Een keuze die bij u past, vraagt ruimte voor de uitstraling &eacute;n de praktische kant. We laten u graag zien hoe die op De Wielsche Dreef samenkomen, zonder een toekomstige waarde te beloven.</p>\n')),

 dict(n=15, hero="fietsers_najaar", kicker="Fase 2",
  anchor="#fase-2", link="Bespreek de mogelijkheden van fase 2",
  title='Past fase 2 beter bij uw plannen?',
  preheader='Een andere ligging of een later aankoopmoment: laten we uw wensen bespreken.',
  h1='Ook uw timing telt mee',
  body=(P + 'Misschien spreekt De Wielsche Dreef u aan, maar is de juiste villa er op dit moment niet voor u bij. Of wilt u eerst ruimte maken om de aankoop samen goed te bekijken. Ook dat is een helder vertrekpunt.</p>\n'
   + P + 'Het landgoed wordt in vijf fasen ontwikkeld, met in totaal circa 245 recreatiewoningen. Een volgende fase kan interessant zijn als u een andere ligging zoekt of aan een later aankoopmoment denkt. Welke mogelijkheden er zijn, hangt af van de ontwikkeling en de verkoopstatus.</p>\n'
   + P + 'We bespreken graag wat u zoekt:</p>\n'
   + bullets([
       'welk woningtype en welke ligging uw voorkeur hebben,',
       'hoe u de villa zelf wilt gebruiken of wilt laten verhuren,',
       'welk aankoopmoment bij uw plannen past.',
   ])
   + P + 'Ik kan u vervolgens de stand van zaken toelichten. Een informatieaanvraag is geen reservering en geeft geen voorrang of garantie op beschikbaarheid.</p>\n'
   + P + 'Zo houdt u zicht op de mogelijkheden, zonder nu een beslissing te hoeven nemen. En mocht een villa uit de huidige fase toch beter aansluiten, dan kunt u die afweging ook meenemen.</p>\n')),
]


# -------------------------------------------------------- de tien paginathemas
#
# Blokken: ('p', tekst) | ('h3', kopje) | ('ul', [items]) | ('quote', tekst)

THEMES = [
 dict(nr=1, anchor="beschikbare-woningen", foto=("villa_avond", "Recreatievilla in de avondzon met gasten op het terras"), naam="Beschikbare woningen",
  lead="Een villa &eacute;n een plek die bij u passen.",
  knop="Ik wil graag meer weten over de actuele beschikbaarheid",
  blocks=[
   ('p', 'Misschien ziet u uzelf al op De Wielsche Dreef verblijven. Om samen te ontspannen, met familie bij elkaar te komen of vrije dagen af te wisselen met verhuur. Uw plannen helpen om gericht naar een woningtype en ligging te kijken.'),
   ('h3', 'Van samen weg tot ruimte voor de hele familie'),
   ('p', 'In fase 1 zijn verschillende woningtypen voorzien voor 2 tot 12 personen, met de uitrustingsniveaus comfort, luxe en extra luxe. Er zijn ook bijzondere wellnessvarianten. De woningen liggen op royale percelen aan of nabij de aangelegde natuurvennen. Elk woningtype is vooraf aan een perceel gekoppeld.'),
   ('h3', 'Wat we met u bekijken'),
   ('ul', ['Het woningtype en de indeling die passen bij uw gezelschap.',
           'De ligging, het uitzicht en de ruimte rondom de villa.',
           'De actuele beschikbaarheid en bijbehorende prijsinformatie.']),
   ('p', 'We verkopen wekelijks woningen, dus het aanbod verandert mee. Willem bespreekt daarom de actuele mogelijkheden met u, in plaats van u op basis van een eerder overzicht te laten kiezen. U bent ook welkom om de plek samen te komen ervaren.'),
  ]),

 dict(nr=2, anchor="eigen-gebruik-verhuur", foto=("terras", "Terras met ligbedden bij een villa"), naam="Eigen gebruik &amp; verhuur",
  lead="Uw eigen vakanties, met duidelijke keuzes over verhuur.",
  knop="Ik wil graag meer weten over eigen gebruik, verhuur en rendement",
  blocks=[
   ('p', 'Een vaste plek voor uw vrije dagen kan samengaan met verhuur in andere periodes. U kunt ook kiezen voor uitsluitend recreatief eigen gebruik. Wat past bij de manier waarop u samen van de villa wilt genieten?'),
   ('h3', 'Eigen gebruik bij verhuur'),
   ('p', 'Bij verhuur kunt u maximaal 90 dagen per jaar blokkeren voor eigen gebruik via de eigenarensite, volgens de reserveringsvoorwaarden. Tijdig reserveren is belangrijk. Na de reserveringsdeadline is eigen gebruik afhankelijk van bestaande boekingen, opties en andere reserveringsafspraken. Eigen gebruik be&iuml;nvloedt het rendement en kan kosten met zich meebrengen.'),
   ('h3', 'Verhuur via Landal'),
   ('p', 'U sluit een verhuurbemiddelingsovereenkomst met Landal, dat het exclusieve verhuurrecht op het park heeft. Landal verzorgt onder meer de verhuurbemiddeling en promotie en ontvangt daarvoor een provisie. Woningen van hetzelfde type worden in een verhuurpool ondergebracht. De opbrengsten worden na aftrek van kosten over de deelnemende woningen verdeeld.'),
   ('h3', 'Wat betekent participatierendement?'),
   ('p', 'Het verwachte rendement uit deelname aan het verhuurconcept, in verhouding tot uw investering en op basis van de toepasselijke opbrengsten en kosten. Een prognose is geen garantie. Zo&rsquo;n prognose gaat over de volledige operationele verhuur over meerdere jaren, niet automatisch over het eerste jaar.'),
   ('p', 'Liever alleen zelf gebruiken? Ook dat kan recreatief, zonder verhuur. Permanente bewoning is niet toegestaan. Willem bespreekt graag uw gewenste periodes, gebruik en financi&euml;le aandachtspunten.'),
  ]),

 dict(nr=3, anchor="werkelijke-kosten", foto=("keuken", "Keuken en eethoek in een villa"), naam="Werkelijke kosten",
  lead="Het hele plaatje telt, niet alleen de aankoopprijs.",
  knop="Ik wil graag meer weten over de kosten",
  blocks=[
   ('p', 'U wilt weten waar u aan begint. Daarom kijken we met u naar de investering &eacute;n de kosten die later terugkomen. Zo kunt u samen beoordelen of de villa past bij uw plannen.'),
   ('h3', 'Wat hoort bij de aankoop?'),
   ('p', 'De koopsommen zijn exclusief btw en vrij op naam. De notaris- en kadasterkosten van de overdracht komen voor rekening van de verkopende partij. Dat betekent niet dat alle mogelijke bijkomende kosten zijn inbegrepen. Tuin, terras en parkeerplaats worden door de ontwikkelaar aangelegd en zijn inbegrepen. Voor verhuur is een compleet inventarispakket nodig dat voldoet aan de eisen van Landal.'),
   ('h3', 'Welke kosten keren terug?'),
   ('ul', ['De parkbijdrage, ook bij uitsluitend recreatief eigen gebruik.',
           'Onderhoud en reserveringen voor groter onderhoud.',
           'Energie, verzekeringen en gemeentelijke en waterschapslasten.',
           'Bij verhuur: onder meer schoonmaak en dienstverlening.']),
   ('h3', 'Kosten en gebruik horen bij elkaar'),
   ('p', 'Uw manier van gebruik be&iuml;nvloedt de kosten en de eventuele verhuuropbrengsten. Een verwacht participatierendement is geen gegarandeerde opbrengst. Willem licht het kostenoverzicht van de villa die u overweegt graag toe. Uw eigen adviseur kan beoordelen hoe de aankoop financieel en fiscaal in uw situatie past.'),
  ]),

 dict(nr=4, anchor="park-omgeving", foto=("betuwe", "De Betuwe aan de Nederrijn vanuit de lucht"), naam="Park &amp; omgeving",
  lead="Een eigen plek in het landschap van de Betuwe.",
  knop="Ik wil graag meer weten over het park en de ontwikkelfasen",
  blocks=[
   ('p', 'Bij Eck en Wiel, achter de dijk van de Nederrijn, komen boomgaarden, water en rivierlandschap samen. Een omgeving om samen op pad te gaan, maar ook om bewust niets te plannen.'),
   ('h3', 'Rust bij de villa, ruimte om eropuit te gaan'),
   ('p', 'In de Betuwe kunt u wandelen en fietsen langs boomgaarden en uiterwaarden. Aan de overkant van de rivier liggen onder meer Amerongen en de Utrechtse Heuvelrug. Bestaande bomen en karakteristieke watergangen blijven op het landgoed zoveel mogelijk behouden, en waterpartijen versterken het groene karakter.'),
   ('h3', 'Eigenaren over hun plek aan het water'),
   ('quote-portret', 'We kijken zo uit over het water. Vanmorgen deden we de gordijnen open en zwom er een meerkoet met kleintjes voorbij. Dat is toch een cadeautje? Zo begin je je dag.'),
   ('p', 'Zo beschrijven de eigenaren van een vierpersoonswoning aan het water hun uitzicht. Het is hun persoonlijke ervaring. Welke ligging bij u past, ontdekt u het beste zelf.'),
   ('h3', 'Een landgoed in ontwikkeling'),
   ('p', 'De Wielsche Dreef wordt in fasen gerealiseerd. Receptie, fietsverhuur en parkshop maken deel uit van de ontwikkeling, net als voorzieningen in latere fasen. Niet alles is automatisch al in gebruik. Tijdens een gesprek of bezoek licht Willem de actuele parksituatie en de ontwikkelfasen toe.'),
  ]),

 dict(nr=5, anchor="aankoopproces", foto=("villa_parasol", "Villa met terras en parasol"), naam="Aankoopproces",
  lead="Van eerste kennismaking tot sleuteloverdracht.",
  knop="Ik wil een kennismaking of parkbezoek plannen",
  blocks=[
   ('p', 'Een vakantievilla kopen doet u stap voor stap. U begint met ontdekken of de plek bij uw wensen past. De precieze planning volgt het aanbod en de gemaakte afspraken.'),
   ('h3', '1. Kennismaken en samen komen kijken'),
   ('p', 'U vertelt wat u zoekt en stelt uw vragen. Tijdens een bezoek bekijkt u het landgoed en, waar mogelijk, een villa. Neem gerust uw partner mee. U hoeft nog geen aankoopbeslissing te nemen.'),
   ('h3', '2. Een voorstel en kostenspecificatie bekijken'),
   ('p', 'U bespreekt de prijs, de inbegrepen onderdelen, keuzemogelijkheden, bijkomende kosten en voorwaarden. Mogelijkheden in uitvoering of inrichting hangen af van de villa en de gemaakte afspraken.'),
   ('h3', '3. Uw financi&euml;le mogelijkheden beoordelen'),
   ('p', 'U bekijkt hoe de aankoop bij uw situatie past en welke financiering eventueel nodig is. Financi&euml;le en fiscale vragen bespreekt u met uw eigen adviseur.'),
   ('h3', '4. De afspraken en overdracht voorbereiden'),
   ('p', 'De koopafspraken worden schriftelijk vastgelegd. Daarna wordt de juridische levering met de notaris voorbereid volgens de gemaakte afspraken.'),
   ('h3', '5. De oplevering en het gebruik voorbereiden'),
   ('p', 'Bij de oplevering worden de villa en eventuele aandachtspunten besproken. Eigen gebruik en eventuele verhuur volgen de afgesproken planning en voorwaarden.'),
   ('p', 'Wilt u eerst iets bespreken, of wilt u een bezoek plannen? Willem helpt u graag verder met de stap die nu bij u past.'),
  ]),

 dict(nr=6, anchor="persoonlijke-match", foto=("woonkamer", "Woonkamer van een villa op het Landgoed"), naam="Persoonlijke match",
  lead="Wat wilt u dat uw villa u beiden brengt?",
  knop="Ik wil graag onze wensen of een vraag bespreken",
  blocks=[
   ('p', 'U hoeft niet met precies dezelfde wensen te beginnen. Misschien kijkt de een vooral naar rust en tijd met familie, en de ander naar kosten, gebruik en beheer. Een passende keuze brengt die vragen bij elkaar.'),
   ('h3', 'Uw wensen als vertrekpunt'),
   ('ul', ['Met wie wilt u er verblijven en hoeveel ruimte zoekt u?',
           'Welke periodes wilt u zelf gebruiken?',
           'Welke ligging en welk comfort spreken u aan?',
           'Wilt u verhuren, en wat verwacht u van de dienstverlening?',
           'Wat wilt u over investering, kosten en voorwaarden weten?']),
   ('h3', 'Zelf gebruiken, verhuren of combineren'),
   ('p', 'Bij eigen gebruik zijn onder meer uw gezelschap, favoriete periodes en gewenste indeling belangrijk. Bij verhuur komen de reserveringsvoorwaarden, de rol van Landal en de invloed op kosten en rendement erbij. U kunt ook kiezen voor uitsluitend recreatief eigen gebruik. Permanent wonen is niet toegestaan.'),
   ('h3', 'Ook twijfel is een goed begin'),
   ('p', 'De eigenaren van een vierpersoonswoning aan het water hadden eerst vragen over hun mogelijkheden. Zij besloten het uit te zoeken. Hun keuze zegt niets over uw eigen situatie, maar laat wel zien dat u niet alle antwoorden hoeft te hebben voordat u contact opneemt.'),
   ('p', 'Willem bespreekt graag uw wensen en openstaande vragen. Een aanvraag is geen aankoopbeslissing. U krijgt informatie om samen verder te kunnen afwegen.'),
  ]),

 dict(nr=7, anchor="privileges", foto=("villa_riet", "Villa aan de waterkant met rietoevers"), naam="Privileges",
  lead="Meer genieten begint bij weten wat er geregeld is.",
  knop="Ik wil graag meer weten over service en beheer",
  blocks=[
   ('p', 'Een eigen villa hoeft niet te betekenen dat u alle praktische werkzaamheden zelf organiseert. Tegelijk wilt u weten wat u uit handen geeft, welke afspraken gelden en wat u zelf blijft regelen.'),
   ('h3', 'Verhuur via Landal'),
   ('p', 'Als u verhuurt, verzorgt Landal de verhuurbemiddeling en promotie volgens de overeengekomen voorwaarden. Dat neemt werkzaamheden uit handen. Daar horen ook afspraken en kosten bij.'),
   ('h3', 'Gezamenlijk beheer en onderhoud'),
   ('p', 'Als eigenaar bent u automatisch lid van de Vereniging van Eigenaars. Die behartigt de gezamenlijke belangen en sluit voor het beheer een overeenkomst met Landal. Ook het onderhoud aan de buitenzijde van de woning, het terras en de tuin wordt via de VvE georganiseerd.'),
   ('h3', 'Wat wilt u vooraf helder hebben?'),
   ('ul', ['Welke taken worden via Landal en de VvE georganiseerd?',
           'Welke bijdragen, kosten en reserveringen horen daarbij?',
           'Welke verantwoordelijkheden en besluiten blijven bij u als eigenaar?']),
   ('p', 'Dienstverlening betekent niet dat alles kosteloos of onbeperkt inbegrepen is. Willem neemt de verdeling en de afspraken graag met u door. Zo wordt duidelijk wat het eigenaarschap praktisch van u vraagt en wat u kunt uitbesteden.'),
  ]),

 dict(nr=8, anchor="duurzaamheid", foto=("slaapkamer", "Slaapkamer in een villa"), naam="Duurzaamheid",
  lead="Comfort, met aandacht voor uitvoering en omgeving.",
  knop="Ik wil graag meer weten over uitvoering en duurzaamheid",
  blocks=[
   ('p', 'De uitstraling van een villa ziet u meteen. Maar een fijne eigen plek moet ook praktisch bij u passen. Daarom loont het om te kijken naar de bouwkundige uitvoering, de installaties en het onderhoud.'),
   ('h3', 'Wat zit er achter het comfort?'),
   ('p', 'De villa&rsquo;s zijn gasloos en worden uitgevoerd met triple glas, een warmtepomp en zonnepanelen. Dat zijn relevante onderdelen bij uw afweging over comfort en energiegebruik. De uiteindelijke energiekosten hangen onder meer af van het woningtype, het gebruik en de tarieven. Lage vaste lasten of een hoger nettorendement zijn daarmee niet gegarandeerd.'),
   ('h3', 'Wat vindt u belangrijk?'),
   ('ul', ['Een prettig binnenklimaat in verschillende seizoenen.',
           'Inzicht in de technische uitvoering en de installaties.',
           'Onderhoud en energiegebruik passend bij uw gebruik.']),
   ('h3', 'De groene omgeving hoort erbij'),
   ('p', 'Bestaande bomen en karakteristieke watergangen blijven waar mogelijk behouden, aangevuld met waterpartijen. Ook het beheer en het onderhoud van het groen maken deel uit van de organisatie van het landgoed.'),
   ('p', 'Wilt u weten wat dit betekent voor de villa die u overweegt? Willem bespreekt graag de uitvoering en de beschikbare specificaties. Zo kunt u uw keuze baseren op concrete kenmerken, niet alleen op de uitstraling.'),
  ]),

 dict(nr=9, anchor="waarde-kwaliteit", foto=("villa_water", "Recreatievilla aan het water op het Landgoed"), naam="Waarde en waardevastheid",
  lead="Begrijpen wat u koopt, verder kijken dan vandaag.",
  knop="Ik wil graag meer weten over eigendom en kwaliteit",
  blocks=[
   ('p', 'Een keuze voor een eigen vakantievilla gaat over de plek &eacute;n over de afspraken die erbij horen. Wat wordt uw priv&eacute;gedeelte? Wat deelt u? En hoe blijft het landgoed verzorgd?'),
   ('h3', 'Uw appartementsrecht'),
   ('p', 'Een appartementsrecht geeft het recht op uitsluitend gebruik van uw priv&eacute;gedeelte: de recreatiewoning met bijbehorende tuin, terras en parkeerplaats(en). Daarnaast zijn er gebruiksrechten en mede-eigendom in de gemeenschappelijke delen volgens de splitsingsstukken.'),
   ('h3', 'Samen verantwoordelijk voor het landgoed'),
   ('p', 'Iedere eigenaar wordt automatisch lid van de VvE. Via die vereniging worden gezamenlijke belangen, bijdragen en onderhoud georganiseerd, zoals voor de wegen, het groen, de waterpartijen en de gemeenschappelijke voorzieningen. Ook reserveringen voor toekomstig onderhoud zijn belangrijk.'),
   ('h3', 'Wat maakt voor u het verschil?'),
   ('p', 'Een echtpaar dat eerst andere parken bekeek, koos hier vanwege de uitstraling van de villa&rsquo;s. Een van hen zei:'),
   ('quote', 'Ik vond het park er eigenlijk heel erg uitspringen.'),
   ('p', 'Dat is hun persoonlijke ervaring, geen uitspraak over toekomstige waarde. Een aantrekkelijke ligging, bouwkwaliteit of verzorgd onderhoud garandeert geen latere verkoopprijs. Willem licht de eigendomsstructuur en de onderhoudsafspraken graag toe, zodat u ook die kant van uw aankoop kunt beoordelen.'),
  ]),

 dict(nr=10, anchor="fase-2", foto=("park_vanuit_lucht", "Het Landgoed vanuit de lucht"), naam="Fase 2",
  lead="Past een volgende fase beter bij uw plannen?",
  knop="Ik wil graag meer weten over fase 2",
  blocks=[
   ('p', 'Misschien zoekt u een andere ligging. Misschien past een later aankoopmoment beter bij u. U kunt De Wielsche Dreef interessant vinden zonder dat de keuze nu al vaststaat.'),
   ('h3', 'Het landgoed groeit in fasen'),
   ('p', 'De Wielsche Dreef is opgezet als een landgoed met circa 245 recreatiewoningen, verdeeld over vijf fasen. Een volgende fase kan aansluiten op een andere voorkeur of een later moment. De mogelijkheden hangen af van de ontwikkeling en de verkoopstatus.'),
   ('h3', 'Vertel wat u zoekt'),
   ('ul', ['Uw voorkeur voor woninggrootte, type en ligging.',
           'Uw plannen voor eigen gebruik en eventuele verhuur.',
           'Het moment waarop u een aankoop wilt overwegen.']),
   ('h3', 'Samen vooruitkijken'),
   ('p', 'Willem bespreekt graag uw wensen en de stand van zaken rond fase 2. Zo kunt u gericht beoordelen of een volgende fase bij uw plannen past, of dat de huidige mogelijkheden toch beter aansluiten.'),
   ('p', 'Een informatieaanvraag is geen reservering en geeft geen voorrang of garantie op beschikbaarheid. Het is een eerste stap om duidelijk te krijgen waar u samen verder naar wilt kijken.'),
  ]),
]


# ------------------------------------------------------------------ rendering

def render(mail):
    body = (HI + mail["body"]
            + cta(mail["link"], mail["anchor"], "wd2-%02da" % mail["n"]))
    if not mail.get("geen_bezoekregel"):
        body += bezoekregel("wd2-%02da" % mail["n"])
    body += SIGN

    html = bm.TEMPLATE
    repl = {
        "TITLE": mail["title"],
        "PREHEADER": mail["preheader"],
        "KICKER": mail["kicker"],
        "H1": mail["h1"],
        "BODY": body,
        "HERO_HTML": bm.hero_html(mail["hero"]),
        "STRIPE_HTML": bm.stripe_html(),
        "KICKER_COLOR": BRAND["kicker_color"],
        "BG_IMG": BRAND["bg_img"],
        "CARD_BG": BRAND["card_bg"],
        "LOGO": BRAND["logo"],
        "BRAND_NAME": BRAND["name"],
        "TAGLINE": BRAND["tagline"],
        "PRIMARY": BRAND["primary"],
        "FOOTER_BG": BRAND["footer_bg"],
        "ACCENT": BRAND["accent"],
        "ACCENT_HOVER": BRAND["accent_hover"],
        "PAGE_BG": BRAND["page_bg"],
        "TEXT": BRAND["text"],
        "PHONE": BRAND["phone"],
        "PHONE_HREF": BRAND["phone_href"],
        "EMAIL": BRAND["email"],
        "EMAIL_HREF": BRAND["email_href"],
        "PARTNER_LINE": BRAND["partner_line"],
        "DISCLAIMER": BRAND["disclaimer"],
        "CREDIT": BRAND["credit"],
        "UNSUBSCRIBE": M["unsubscribe_block"],
    }
    for k, v in repl.items():
        html = html.replace("[[" + k + "]]", v)
    return html


# --------------------------------------------------------- de conversiepagina

PAGE = """<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Landgoed De Wielsche Dreef | Uw vragen, per onderwerp</title>
<meta name="description" content="Tien onderwerpen over Landgoed De Wielsche Dreef: beschikbaarheid, eigen gebruik en verhuur, kosten, park, aankoopproces, service, duurzaamheid, eigendom en fase 2.">
<meta name="robots" content="noindex">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
 :root{
   --green:[[PRIMARY]]; --green-dark:[[FOOTER_BG]]; --accent:[[ACCENT]];
   --accent-hover:[[ACCENT_HOVER]]; --card:[[CARD_BG]]; --text:[[TEXT]];
   --line:#dcd5ca; --quote-bg:#eef4f3;
 }
 *{ box-sizing:border-box; }
 body{ margin:0; background:#ffffff; color:var(--text);
   font-family:'Inter',Arial,sans-serif; font-size:17px; line-height:28px; }
 h1,h2,h3{ font-family:'Playfair Display',Georgia,serif; color:var(--green); font-weight:600; }
 a{ color:var(--green); }
 .wrap{ max-width:760px; margin:0 auto; padding:0 20px; }

 header.hero{ background:var(--green) url('[[BG_IMG]]') center top / cover no-repeat;
   color:#fff; padding:34px 0 46px 0; }
 header.hero h1{ color:#fff; font-size:34px; line-height:44px; margin:22px 0 14px 0; }
 header.hero p{ color:rgba(255,255,255,0.86); margin:0; max-width:620px; }
 .brandbar{ display:flex; align-items:center; gap:16px; }
 .brandbar img{ width:92px; height:auto; display:block; }
 .brandbar span{ font-size:10px; letter-spacing:0.16em; text-transform:uppercase;
   color:rgba(255,255,255,0.62); border-left:1px solid rgba(255,255,255,0.25);
   padding-left:16px; line-height:16px; }
 .stripe{ display:flex; height:10px; }

 nav.themes{ background:#f7f4ef; border-bottom:1px solid var(--line); padding:18px 0; }
 nav.themes ul{ list-style:none; margin:0; padding:0; display:flex; flex-wrap:wrap; gap:8px; }
 nav.themes a{ display:block; text-decoration:none; font-size:14px; line-height:20px;
   padding:7px 14px; border:1px solid var(--line); border-radius:999px;
   background:#fff; color:var(--green); }
 nav.themes a:hover{ border-color:var(--green); }

 section.theme{ border-bottom:1px solid var(--line); padding:44px 0 38px 0; scroll-margin-top:16px; }
 section.theme:last-of-type{ border-bottom:0; }
 .nr{ font-size:11px; letter-spacing:0.2em; text-transform:uppercase;
   color:#8a9a95; font-weight:700; margin-bottom:10px; }
 section.theme h2{ font-size:27px; line-height:36px; margin:0 0 16px 0; }
 section.theme h3{ font-size:18px; line-height:26px; margin:26px 0 6px 0; }
 section.theme p{ margin:0 0 16px 0; }
 .shot{ margin:0 0 24px 0; }
 .shot img{ width:100%; height:auto; display:block; border-radius:6px; }
 .banner img{ width:100%; height:auto; display:block; }
 .met-portret{ display:flex; gap:18px; align-items:flex-start; margin:4px 0 18px 0;
   padding:18px 22px; background:var(--quote-bg); border-left:4px solid var(--green); }
 .met-portret img{ width:108px; height:auto; border-radius:4px; display:block; flex:0 0 auto; }
 .met-portret .tekst{ font-style:italic; color:#1a1a1a; }
 @media (max-width:560px){ .met-portret{ flex-direction:column; } }
 section.theme ul{ margin:0 0 16px 0; padding-left:22px; }
 section.theme li{ margin:0 0 8px 0; }
 blockquote{ margin:4px 0 18px 0; padding:18px 22px; background:var(--quote-bg);
   border-left:4px solid var(--green); font-style:italic; color:#1a1a1a; }

 .toggle{ display:inline-block; margin-top:12px; border:0; cursor:pointer;
   background:var(--accent); color:#fff; font-family:'Inter',Arial,sans-serif;
   font-size:16px; font-weight:700; line-height:24px; padding:15px 28px;
   border-radius:4px; text-align:left; }
 .toggle:hover{ background:var(--accent-hover); }
 .panel{ display:none; margin-top:20px; background:var(--card);
   border-radius:6px; padding:24px; }
 .panel.open{ display:block; }
 .panel p.intro{ margin:0 0 18px 0; font-size:16px; line-height:25px; }
 .row{ display:flex; gap:14px; flex-wrap:wrap; }
 .row > div{ flex:1 1 220px; }
 label{ display:block; font-size:13px; font-weight:600; color:var(--green);
   margin:0 0 5px 0; }
 input,textarea{ width:100%; font-family:'Inter',Arial,sans-serif; font-size:16px;
   padding:11px 13px; border:1px solid var(--line); border-radius:4px;
   background:#fff; color:var(--text); margin-bottom:14px; }
 textarea{ min-height:96px; resize:vertical; }
 input:focus,textarea:focus{ outline:2px solid var(--green); outline-offset:-2px; }
 button.send{ border:0; cursor:pointer; background:var(--green); color:#fff;
   font-family:'Inter',Arial,sans-serif; font-size:16px; font-weight:700;
   padding:14px 30px; border-radius:4px; }
 button.send:hover{ background:var(--green-dark); }
 .small{ font-size:13px; line-height:20px; color:#6d7b78; margin:12px 0 0 0; }
 .done{ display:none; background:#eef4f3; border-left:4px solid var(--green);
   padding:18px 22px; margin-top:16px; }
 .done.open{ display:block; }

 .willem{ background:#f7f4ef; border:1px solid var(--line); border-radius:6px;
   padding:22px 24px; margin:40px 0; display:flex; gap:20px; align-items:center;
   flex-wrap:wrap; }
 .willem div{ flex:1 1 280px; }
 .willem p{ margin:0 0 4px 0; }
 .willem .naam{ font-weight:700; color:var(--green); }

 footer{ background:var(--green-dark); color:rgba(255,255,255,0.6);
   font-size:13px; line-height:21px; padding:32px 0; margin-top:10px; }
 footer a{ color:rgba(255,255,255,0.75); }
 footer .disc{ font-size:11px; line-height:17px; color:rgba(255,255,255,0.45);
   margin-top:14px; }

 @media (max-width:620px){
   body{ font-size:16px; line-height:26px; }
   header.hero h1{ font-size:27px; line-height:36px; }
   section.theme h2{ font-size:23px; line-height:31px; }
   .toggle{ width:100%; }
 }
</style>
</head>
<body>

<header class="hero">
 <div class="wrap">
  <div class="brandbar">
   <img src="[[LOGO]]" alt="[[BRAND_NAME]]">
   <span>[[TAGLINE_PLAIN]]</span>
  </div>
  <h1>Waar wilt u meer over weten?</h1>
  <p>Hieronder staan de onderwerpen die bij een eigen villa op De Wielsche Dreef het vaakst terugkomen. Kies wat voor u nu speelt en laat weten wat u wilt bespreken. U legt daarmee niets vast.</p>
 </div>
</header>
<div class="banner"><img src="[[CDN]]water_villas.jpg" alt="Villa&rsquo;s aan het water op Landgoed De Wielsche Dreef" width="1136" height="496"></div>
<div class="stripe">[[STRIPE_CELLS]]</div>

<nav class="themes">
 <div class="wrap"><ul>[[NAV]]</ul></div>
</nav>

<main class="wrap">
[[SECTIONS]]

 <div class="willem">
  <div>
   <p class="naam">Liever direct contact met Willem?</p>
   <p>Willem van de Griend, uw persoonlijke Landgoed-adviseur</p>
   <p><a href="[[PHONE_HREF]]">[[PHONE]]</a> &middot; <a href="[[EMAIL_HREF]]">[[EMAIL]]</a></p>
  </div>
 </div>
</main>

<footer>
 <div class="wrap">
  <p style="margin:0;">[[BRAND_NAME]] &middot; Kalverlandseweg 3, 4024 BT Eck en Wiel<br>
  [[PARTNER_LINE]]</p>
  <p class="disc">[[DISCLAIMER]]</p>
 </div>
</footer>

<script>
(function(){
  var ENDPOINT = "[[FORM_ENDPOINT]]";

  function qs(){
    var o = {}, s = window.location.search.replace(/^\\?/, "");
    s.split("&").forEach(function(p){
      if(!p) return;
      var i = p.indexOf("="), k = i < 0 ? p : p.slice(0, i);
      var v = i < 0 ? "" : decodeURIComponent(p.slice(i + 1).replace(/\\+/g, " "));
      o[k] = v;
    });
    return o;
  }
  var q = qs();

  // De mails geven naam, e-mail en telefoon mee. Lege of niet-ingevulde
  // merge-tags (%FIRSTNAME% blijft staan als het veld leeg is) negeren we.
  function clean(v){
    if(!v) return "";
    if(v.charAt(0) === "%" || v.indexOf("{{") === 0) return "";
    return v;
  }
  var pre = {
    voornaam: clean(q.first_name),
    achternaam: clean(q.last_name),
    email: clean(q.email),
    telefoon: clean(q.phone)
  };
  Object.keys(pre).forEach(function(k){
    if(!pre[k]) return;
    document.querySelectorAll('[data-field="' + k + '"]').forEach(function(el){
      el.value = pre[k];
    });
  });

  document.querySelectorAll(".toggle").forEach(function(btn){
    btn.addEventListener("click", function(){
      var panel = document.getElementById(btn.getAttribute("aria-controls"));
      var open = panel.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      if(open){
        var f = panel.querySelector("input:not([type=hidden])");
        if(f && !f.value) f.focus({ preventScroll: true });
      }
    });
  });

  document.querySelectorAll("form.aanvraag").forEach(function(form){
    form.addEventListener("submit", function(ev){
      ev.preventDefault();
      var data = {};
      new FormData(form).forEach(function(v, k){ data[k] = v; });
      data.pagina = window.location.href;
      var done = form.parentNode.querySelector(".done");
      if(!ENDPOINT){
        done.innerHTML = "<strong>Voorbeeldversie.</strong> Het formulier is nog niet " +
          "gekoppeld, dus er is niets verstuurd. Zodra de koppeling staat, komt deze " +
          "aanvraag binnen bij Willem.";
        done.classList.add("open");
        return;
      }
      fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      }).then(function(){
        form.style.display = "none";
        done.innerHTML = "<strong>Dank u wel.</strong> Uw bericht staat genoteerd. " +
          "Willem neemt binnen een werkdag contact met u op.";
        done.classList.add("open");
      }).catch(function(){
        done.innerHTML = "Het versturen lukte niet. Belt u gerust naar [[PHONE]] " +
          "of mail naar [[EMAIL]].";
        done.classList.add("open");
      });
    });
  });

  // Komt iemand uit een mail, dan staat het thema al open.
  var doel = q.thema || window.location.hash.replace(/^#/, "");
  if(doel){
    var btn = document.querySelector('.toggle[data-thema="' + doel + '"]');
    if(btn) btn.click();
    var sec = document.getElementById(doel);
    if(sec) setTimeout(function(){ sec.scrollIntoView({ behavior: "smooth", block: "start" }); }, 80);
  }
})();
</script>
</body></html>"""


def form_html(t):
    """Het uitklapformulier onder een thema."""
    pid = "form-" + t["anchor"]
    return (
     '  <button class="toggle" type="button" data-thema="' + t["anchor"] + '" '
     'aria-expanded="false" aria-controls="' + pid + '">' + t["knop"] + '</button>\n'
     '  <div class="panel" id="' + pid + '">\n'
     '   <form class="aanvraag">\n'
     '    <p class="intro">Laat uw gegevens achter, dan neemt Willem contact met u op. '
     'Telefonisch, online of op locatie, op het moment dat u uitkomt.</p>\n'
     '    <input type="hidden" name="onderwerp" value="' + t["naam"].replace("&amp;", "en") + '">\n'
     '    <div class="row">\n'
     '     <div><label for="' + pid + '-vn">Voornaam</label>'
     '<input id="' + pid + '-vn" name="voornaam" data-field="voornaam" type="text" autocomplete="given-name" required></div>\n'
     '     <div><label for="' + pid + '-an">Achternaam</label>'
     '<input id="' + pid + '-an" name="achternaam" data-field="achternaam" type="text" autocomplete="family-name"></div>\n'
     '    </div>\n'
     '    <div class="row">\n'
     '     <div><label for="' + pid + '-em">E-mailadres</label>'
     '<input id="' + pid + '-em" name="email" data-field="email" type="email" autocomplete="email" required></div>\n'
     '     <div><label for="' + pid + '-tel">Telefoonnummer</label>'
     '<input id="' + pid + '-tel" name="telefoon" data-field="telefoon" type="tel" autocomplete="tel"></div>\n'
     '    </div>\n'
     '    <label for="' + pid + '-vr">Uw vraag of opmerking <span style="font-weight:400; color:#6d7b78;">(optioneel)</span></label>\n'
     '    <textarea id="' + pid + '-vr" name="vraag"></textarea>\n'
     '    <button class="send" type="submit">Versturen</button>\n'
     '    <p class="small">Een aanvraag is geen aankoopbeslissing en geen reservering. '
     'U ontvangt informatie en bepaalt daarna zelf of u verder wilt kijken.</p>\n'
     '   </form>\n'
     '   <div class="done"></div>\n'
     '  </div>\n')


def section_html(t):
    out = ['<section class="theme" id="' + t["anchor"] + '">\n',
           '  <div class="nr">Onderwerp ' + str(t["nr"]) + ' &middot; ' + t["naam"] + '</div>\n',
           '  <h2>' + t["lead"] + '</h2>\n']
    if t.get("foto"):
        naam, alt = t["foto"]
        out.append('  <div class="shot"><img src="' + bm._CDN + naam + '.jpg" '
                   'alt="' + alt + '" width="1136" height="496" loading="lazy"></div>\n')
    for kind, val in t["blocks"]:
        if kind == 'p':
            out.append('  <p>' + val + '</p>\n')
        elif kind == 'h3':
            out.append('  <h3>' + val + '</h3>\n')
        elif kind == 'ul':
            out.append('  <ul>' + "".join('<li>' + i + '</li>' for i in val) + '</ul>\n')
        elif kind == 'quote':
            out.append('  <blockquote>&ldquo;' + val + '&rdquo;</blockquote>\n')
        elif kind == 'quote-portret':
            out.append('  <div class="met-portret">'
                       '<img src="' + bm._CDN.replace("hero-", "portret-") + 'eigenaren.jpg" '
                       'alt="Eigenaren op Landgoed De Wielsche Dreef" width="400" height="400" loading="lazy">'
                       '<span class="tekst">&ldquo;' + val + '&rdquo;</span></div>\n')
    out.append(form_html(t))
    out.append('</section>\n')
    return "".join(out)


def build_page():
    nav = "".join('<li><a href="#' + t["anchor"] + '">' + t["naam"] + '</a></li>'
                  for t in THEMES)
    cells = "".join('<i style="flex:%s; background:%s;"></i>' % (pct, col)
                    for col, pct in bm.STRIPE)
    html = PAGE
    repl = {
        "PRIMARY": BRAND["primary"], "FOOTER_BG": BRAND["footer_bg"],
        "ACCENT": BRAND["accent"], "ACCENT_HOVER": BRAND["accent_hover"],
        "CARD_BG": BRAND["card_bg"], "TEXT": BRAND["text"],
        "BG_IMG": BRAND["bg_img"], "LOGO": BRAND["logo"],
        "BRAND_NAME": BRAND["name"],
        "TAGLINE_PLAIN": BRAND["tagline"].replace("<br>", " &middot; "),
        "STRIPE_CELLS": cells, "NAV": nav,
        "SECTIONS": "".join(section_html(t) for t in THEMES),
        "PHONE": BRAND["phone"], "PHONE_HREF": BRAND["phone_href"],
        "EMAIL": BRAND["email"], "EMAIL_HREF": BRAND["email_href"],
        "PARTNER_LINE": BRAND["partner_line"],
        "DISCLAIMER": BRAND["disclaimer"].replace(
            "Deze e-mail is algemene informatie", "Deze informatie is algemeen van aard"),
        "FORM_ENDPOINT": FORM_ENDPOINT,
        "CDN": bm._CDN,
    }
    for k, v in repl.items():
        html = html.replace("[[" + k + "]]", v)
    return html


# ------------------------------------------------------------------- overzicht

INDEX = """<!DOCTYPE html>
<html lang="nl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mailflow v2 | De Wielsche Dreef</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
 body{ margin:0; background:#f7f4ef; color:#374151; font-family:'Inter',Arial,sans-serif;
   font-size:16px; line-height:26px; }
 .wrap{ max-width:900px; margin:0 auto; padding:40px 20px 60px 20px; }
 h1{ font-family:'Playfair Display',Georgia,serif; color:[[PRIMARY]]; font-size:30px;
   margin:0 0 6px 0; }
 p.sub{ margin:0 0 28px 0; color:#6d7b78; }
 table{ width:100%; border-collapse:collapse; background:#fff; border:1px solid #dcd5ca; }
 th,td{ text-align:left; padding:11px 14px; border-bottom:1px solid #eee7dd;
   font-size:15px; line-height:23px; vertical-align:top; }
 th{ background:[[PRIMARY]]; color:#fff; font-size:12px; letter-spacing:0.08em;
   text-transform:uppercase; }
 tr:last-child td{ border-bottom:0; }
 a{ color:[[PRIMARY]]; }
 .kick{ font-size:12px; color:#8a9a95; }
 .cta{ display:inline-block; margin:0 0 28px 0; background:[[ACCENT]]; color:#fff;
   text-decoration:none; font-weight:700; padding:13px 26px; border-radius:4px; }
</style></head><body><div class="wrap">
<h1>Mailflow v2</h1>
<p class="sub">Vijftien mails rond tien onderwerpen, elk met een eigen bestemming op de conversiepagina. Bron: "De Wielsche Dreef - themas en mails final".</p>
<a class="cta" href="conversiepagina.html">Bekijk de conversiepagina &rarr;</a>
<table>
<tr><th>#</th><th>Onderwerp</th><th>Thema</th><th>Mail</th></tr>
[[ROWS]]
</table>
</div></body></html>"""


def build_index():
    naam = {t["anchor"]: t["naam"] for t in THEMES}
    rows = []
    for m in MAILS:
        a = m["anchor"].lstrip("#")
        rows.append(
            '<tr><td>%02d</td><td><strong>%s</strong><br><span class="kick">%s</span></td>'
            '<td><a href="conversiepagina.html#%s">%s</a></td>'
            '<td><a href="mail-%02d.html">openen</a></td></tr>'
            % (m["n"], m["title"], m["preheader"], a, naam[a], m["n"]))
    return (INDEX.replace("[[ROWS]]", "\n".join(rows))
                 .replace("[[PRIMARY]]", BRAND["primary"])
                 .replace("[[ACCENT]]", BRAND["accent"]))


def main():
    OUT_DIR.mkdir(exist_ok=True)
    written = []
    for m in MAILS:
        name = "mail-%02d.html" % m["n"]
        (OUT_DIR / name).write_text(bm.to_ascii(render(m)), encoding="ascii")
        written.append(name)
    (OUT_DIR / "conversiepagina.html").write_text(bm.to_ascii(build_page()), encoding="ascii")
    written.append("conversiepagina.html")
    (OUT_DIR / "index.html").write_text(bm.to_ascii(build_index()), encoding="ascii")
    written.append("index.html")
    print("Geschreven in v2/: %d bestanden" % len(written))
    for n in written:
        print("  v2/" + n)


if __name__ == "__main__":
    main()
