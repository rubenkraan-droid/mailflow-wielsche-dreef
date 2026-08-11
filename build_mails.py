#!/usr/bin/env python3
"""Genereert mail-01.html t/m mail-15.html + index.html uit een template + datastructuur.

Gebruik:  python3 build_mails.py

Alle merk-instellingen staan in BRAND; per-mail content staat in MAILS.
Pas iets aan, draai het script en alle 15 mails zijn weer consistent.
Output is 100% ASCII (accenten als HTML-entities) zodat plakken in GHL geen
tekencorruptie geeft.
"""
import pathlib
import re
import sys

OUT_DIR = pathlib.Path(__file__).parent

BRAND = dict(
    name="Landgoed De Wielsche Dreef",
    short_name="De Wielsche Dreef",
    tagline="Exclusief Vakantievastgoed<br>Betuwe &middot; Nederrijn",
    logo="https://dewielschedreef.nl/wp-content/uploads/2024/09/Logo-wit.svg",
    primary="#1f524d",
    footer_bg="#123330",
    accent="#be5748",
    accent_hover="#9e4438",
    page_bg="#f0ebe3",
    text="#374151",
    phone="085 - 303 28 44",
    phone_href="tel:0853032844",
    email="info@recravas.nl",
    email_href="mailto:info@recravas.nl",
    contact_party="Recravas",
    cta_url="https://rubenkraan-droid.github.io/mailflow-wielsche-dreef/gesprek.html",
    cta_prefill="email={{contact.email}}&first_name={{contact.first_name}}&last_name={{contact.last_name}}&phone={{contact.phone}}",
    campaign="wielsche-dreef",
    partner_line="Recravas &middot; verhuur verzorgd door Landal",
    disclaimer=("Deze e-mail is algemene informatie en bevat geen aanbod, rendements- of "
                "belastingtoezegging. Aan de inhoud kunnen geen rechten worden ontleend. "
                "Specifieke cijfers, voorwaarden en risico&rsquo;s worden uitsluitend in een "
                "persoonlijk gesprek toegelicht. Deze informatie is geen fiscaal of "
                "beleggingsadvies; laat uw eigen situatie toetsen door een fiscalist of adviseur."),
    credit="Foto&rsquo;s: Landgoed De Wielsche Dreef &middot; Betuwe, aan de Nederrijn.",
)

_CDN = "https://dewielschedreef.nl/wp-content/uploads/"
IMG = {
    "ext_8c":     (_CDN + "2024/11/8C_EXT-dwd.jpg", "Recreatievilla type C op Landgoed De Wielsche Dreef"),
    "ext_10elw":  (_CDN + "2024/11/10ELW_EXT-dwd.jpg", "Recreatievilla type ELW met ruime tuin"),
    "ext_12c":    (_CDN + "2024/11/12C_EXT-dwd.jpg", "Ruime recreatievilla type C"),
    "ext_12elf":  (_CDN + "2024/11/12ELF_EXT-dwd.jpg", "Recreatievilla type ELF"),
    "int_2p_elw": (_CDN + "2024/09/De-Wielsche-Dreef-2p-ELW-scaled.jpg", "Interieur van een 2-persoons villa"),
    "int_4p_c":   (_CDN + "2024/09/De-Wielsche-Dreef-4p-C-scaled.jpg", "Woonkamer van een 4-persoons villa"),
    "int_4p_l":   (_CDN + "2024/09/De-Wielsche-Dreef-4p-L-scaled.jpg", "Lichte woonruimte in een 4-persoons villa"),
    "int_4p_elw": (_CDN + "2024/09/De-Wielsche-Dreef-4p-ELW-scaled.jpg", "4-persoons villa met extra lichte woonkamer"),
    "int_6p_c":   (_CDN + "2024/09/De-Wielsche-Dreef-6p-C-scaled.jpg", "Interieur van een 6-persoons villa"),
    "int_6p_l":   (_CDN + "2024/09/De-Wielsche-Dreef-6p-L-scaled.jpg", "6-persoons villa in luxe uitvoering"),
}

# 1 entry = brede hero (600x220), 2 entries = gesplitste hero (2x 300x220)
HERO = {
    1:  [("ext_8c", "center 55%"), ("int_6p_l", "center 50%")],
    2:  [("ext_10elw", "center 58%")],
    3:  [("int_4p_elw", "center 50%"), ("int_6p_c", "center 52%")],
    4:  [("ext_12c", "center 55%")],
    5:  [("ext_12elf", "center 58%"), ("int_4p_l", "center 50%")],
    6:  [("int_6p_l", "center 50%")],
    7:  [("ext_8c", "center 60%"), ("int_2p_elw", "center 50%")],
    8:  [("ext_10elw", "center 55%")],
    9:  [("int_4p_c", "center 50%"), ("ext_12c", "center 58%")],
    10: [("ext_12elf", "center 55%")],
    11: [("int_6p_c", "center 52%"), ("ext_10elw", "center 58%")],
    12: [("ext_12c", "center 60%")],
    13: [("int_4p_elw", "center 50%"), ("ext_8c", "center 55%")],
    14: [("ext_12elf", "center 58%"), ("int_6p_l", "center 50%")],
    15: [("ext_10elw", "center 55%"), ("int_4p_c", "center 50%")],
}

TEMPLATE = """<!DOCTYPE html>
<html lang="nl" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light">
<title>[[TITLE]]</title>
<!--[if mso]><noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript><![endif]-->
<!--[if !mso]><!--><link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@400;600;700&display=swap" rel="stylesheet"><!--<![endif]-->
<style>
 body,table,td,a{ -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%; }
 table,td{ mso-table-lspace:0pt; mso-table-rspace:0pt; }
 img{ -ms-interpolation-mode:bicubic; border:0; height:auto; line-height:100%; outline:none; text-decoration:none; display:block; }
 body{ margin:0; padding:0; width:100%!important; background-color:[[PAGE_BG]]; }
 a{ color:[[PRIMARY]]; }
 .btn:hover{ background-color:[[ACCENT_HOVER]]!important; }
 @media only screen and (max-width:620px){
   .container{ width:100%!important; }
   .px{ padding-left:24px!important; padding-right:24px!important; }
   .h1{ font-size:23px!important; line-height:31px!important; }
   .hero{ height:190px!important; }
 }
</style>
</head>
<body style="margin:0; padding:0; background-color:[[PAGE_BG]];">
<!-- Onderwerp: [[TITLE]] -->
<div style="display:none; max-height:0; overflow:hidden; mso-hide:all; font-size:1px; line-height:1px; color:[[PAGE_BG]];">[[PREHEADER]] &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:[[PAGE_BG]];"><tr>
<td align="center" style="padding:24px 12px;">
<table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" style="width:600px; max-width:600px; background-color:#ffffff; border-radius:6px; overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,0.06);">
 <tr><td style="background-color:[[PRIMARY]]; padding:14px 32px; text-align:center;" class="px">
   <table role="presentation" cellpadding="0" cellspacing="0" align="center" style="margin:0 auto;"><tr>
     <td style="vertical-align:middle; padding-right:16px;">
       <img src="[[LOGO]]" alt="[[BRAND_NAME]]" width="88" style="max-width:88px; height:auto; display:block;">
     </td>
     <td style="vertical-align:middle; padding-left:16px; border-left:1px solid rgba(255,255,255,0.25);">
       <p style="margin:0; font-family:'Inter',Arial,sans-serif; font-size:10px; color:rgba(255,255,255,0.62); letter-spacing:0.16em; text-transform:uppercase; text-align:left; line-height:16px;">[[TAGLINE]]</p>
     </td>
   </tr></table>
 </td></tr>
 <tr><td style="padding:0; line-height:0; font-size:0;">
[[HERO_HTML]]
 </td></tr>
 <tr><td style="padding:34px 32px 6px 32px;" class="px">
   <div style="font-family:'Inter',Arial,sans-serif; font-size:11px; letter-spacing:0.18em; text-transform:uppercase; color:[[ACCENT]]; font-weight:bold; margin-bottom:12px;">[[KICKER]]</div>
   <h1 class="h1" style="margin:0; font-family:'Playfair Display',Georgia,serif; font-size:27px; line-height:35px; color:[[PRIMARY]]; font-weight:600;">[[H1]]</h1>
 </td></tr>
 <tr><td style="padding:18px 32px 4px 32px; font-family:'Inter',Arial,sans-serif; font-size:16px; line-height:26px; color:[[TEXT]];" class="px">
[[BODY]]
 </td></tr>
 <tr><td style="background-color:[[FOOTER_BG]]; padding:28px 32px; text-align:center;" class="px">
   <img src="[[LOGO]]" alt="[[BRAND_NAME]]" width="100" style="max-width:100px; height:auto; display:inline-block; opacity:0.7; margin-bottom:14px;">
   <p style="margin:0 0 4px 0; font-family:'Inter',Arial,sans-serif; font-size:12px; color:rgba(255,255,255,0.55);">[[PARTNER_LINE]]</p>
   <p style="margin:0 0 16px 0; font-family:'Inter',Arial,sans-serif; font-size:13px;"><a href="[[PHONE_HREF]]" style="color:rgba(255,255,255,0.7); text-decoration:none;">[[PHONE]]</a> &nbsp;&middot;&nbsp; <a href="[[EMAIL_HREF]]" style="color:rgba(255,255,255,0.7); text-decoration:none;">[[EMAIL]]</a></p>
   <p style="margin:0 0 12px 0; font-family:'Inter',Arial,sans-serif; font-size:11px; line-height:17px; color:rgba(255,255,255,0.45); max-width:460px; margin-left:auto; margin-right:auto;">[[DISCLAIMER]]</p>
   <p style="margin:0; font-family:'Inter',Arial,sans-serif; font-size:11px; color:rgba(255,255,255,0.45);">[[BRAND_NAME]] &nbsp;&middot;&nbsp; <a href="{{unsubscribe_url}}" style="color:rgba(255,255,255,0.45); text-decoration:underline;">Uitschrijven</a></p>
 </td></tr>
</table>
<div style="font-family:'Inter',Arial,sans-serif; font-size:11px; color:#a89f92; padding:14px 8px 0 8px;">[[CREDIT]]</div>
</td></tr></table>
</body></html>"""


def cta(label, variant):
    url = (BRAND["cta_url"] + "?utm_source=email&utm_medium=mailflow"
           + "&utm_campaign=" + BRAND["campaign"]
           + "&utm_content=" + variant + "&" + BRAND["cta_prefill"])
    return ('   <table role="presentation" cellpadding="0" cellspacing="0" style="margin:6px 0 20px 0;">'
            '<tr><td align="center" style="border-radius:4px; background-color:' + BRAND["accent"] + ';">'
            '<a class="btn" href="' + url + '" target="_blank" '
            'style="display:inline-block; padding:15px 32px; font-family:\'Inter\',Arial,sans-serif; '
            'font-size:16px; font-weight:bold; color:#ffffff; text-decoration:none; border-radius:4px;">'
            + label + ' &rarr;</a></td></tr></table>\n')


def quote(text):
    return ('   <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:4px 0 20px 0;">'
            '<tr><td style="background-color:#eef4f3; border-left:4px solid ' + BRAND["primary"] + '; '
            'padding:18px 22px; font-family:\'Inter\',Arial,sans-serif; font-style:italic; font-size:16px; '
            'line-height:26px; color:#1a1a1a;">&ldquo;' + text + '&rdquo;</td></tr></table>\n')


def bullets(items):
    lis = "".join('<li style="margin:0 0 8px 0;">' + i + '</li>' for i in items)
    return ('   <ul style="margin:0 0 20px 0; padding-left:22px; font-family:\'Inter\',Arial,sans-serif; '
            'font-size:16px; line-height:26px; color:#374151;">' + lis + '</ul>\n')


P = '   <p style="margin:0 0 18px 0;">'
SIGN = '   <p style="margin:0;">Met vriendelijke groet,<br><strong>' + BRAND["short_name"] + '</strong></p>\n'
HI = P + 'Beste {{contact.first_name}},</p>\n'

MAILS = [
 dict(n=1, day=1, phase=1,
  title='Welkom bij Landgoed De Wielsche Dreef',
  title_b='Uw kennismaking met Landgoed De Wielsche Dreef',
  preheader='Ontdek de plek waar rust, luxe en natuur samenkomen',
  preheader_b='Aan de Nederrijn, midden in het groen van de Betuwe',
  kicker='Welkom',
  h1='Waar rust, luxe en natuur samenkomen',
  body=HI
   + P + 'Hartelijk dank voor uw interesse in Landgoed De Wielsche Dreef.</p>\n'
   + P + 'Aan de Nederrijn, midden in het groen van de Betuwe, ontstaat een plek voor mensen die waarde hechten aan rust en ruimte, maar dat gekoppeld willen zien aan kwaliteit, luxe en comfort. Geen standaard parkbeleving, maar een omgeving waar eigenaarschap, luxe en aandacht op een vanzelfsprekende manier samenkomen.</p>\n'
   + P + 'Landgoed De Wielsche Dreef is meer dan een park met recreatievilla&rsquo;s. Het is een eigen plek waar u naartoe gaat om te verblijven, te delen en tot rust te komen in alle comfort.</p>\n'
   + P + 'In de komende periode nemen wij u stap voor stap mee in de sfeer van het Landgoed, de ligging, het aanbod en de manier waarop eigenaarschap hier voelt. Niet alles tegelijk, maar precies genoeg om te ontdekken of dit bij u past.</p>\n'
   + cta('Plan een kennismaking', 'wd-mail-01a')
   + P + 'Wilt u liever direct kennismaken of uw vragen persoonlijk bespreken? Dat kan telefonisch, online of op locatie.</p>\n'
   + SIGN),

 dict(n=2, day=2, phase=1,
  title='Waarom Landgoed De Wielsche Dreef direct aanspreekt',
  title_b='Niet alleen een villa, maar een plek die iets met u doet',
  preheader='Niet alleen een villa, maar een plek die iets met u doet',
  preheader_b='Wat eigenaren als eerste opvalt',
  kicker='Herkenning',
  h1='Sommige plekken voelen direct anders',
  body=HI
   + P + 'Wat mensen in De Wielsche Dreef vaak meteen herkennen, is de combinatie van rust, uitstraling, ruimte, kwaliteit en luxe. Niet als losse elementen, maar als een geheel. Juist dat maakt dat deze plek niet voelt als een standaardaanbod, maar als een omgeving die past bij een bepaalde manier van leven.</p>\n'
   + P + 'Wat veel geinteresseerden aanspreekt:</p>\n'
   + bullets([
       'de natuurrijke ligging aan de Nederrijn,',
       'de hoogwaardige uitstraling van villa en omgeving,',
       'de zorgvuldige begeleiding,',
       'de combinatie van eigen gebruik en slim eigenaarschap,',
       'unieke services passend bij het nastreven van comfort.',
   ])
   + quote('De Betuwe: een prachtig, natuurvriendelijk en vogelrijk gebied. Vanaf het eerste moment dat we het zagen, heeft het ons niet meer losgelaten. Ik vond het park eruit springen. We hebben zeker drie andere parken vergeleken, maar die spraken ons niet aan.')
   + P + 'Wie hier interesse in heeft, zoekt doorgaans geen villa, maar een plek die past bij wie u bent.</p>\n'
   + cta('Plan uw afspraak', 'wd-mail-02a')
   + SIGN),

 dict(n=3, day=3, phase=1,
  title='Comfort, eigen gebruik en professioneel beheer',
  title_b='Een sterk concept begint met rust en duidelijkheid',
  preheader='Een sterk concept begint met rust, kwaliteit en duidelijkheid',
  preheader_b='De privileges die alleen eigenaren krijgen',
  kicker='Vertrouwen',
  h1='Gevoel en overzicht gaan hier samen',
  body=HI
   + P + 'Bij interesse in recreatief vastgoed gaan gevoel en overzicht vrijwel altijd samen.</p>\n'
   + P + 'Aan de ene kant is er de aantrekkingskracht van een plek: rust, natuur, comfort en de gedachte aan een eigen vakantievilla waar u graag verblijft. Aan de andere kant wilt u weten of het geheel goed georganiseerd is. Juist daarin onderscheidt Landgoed De Wielsche Dreef zich.</p>\n'
   + P + 'Binnen het concept wordt veel aandacht besteed aan privileges die alleen gelden voor u als eigenaar:</p>\n'
   + bullets([
       'een persoonlijke Landgoed-adviseur en ontzorgservice,',
       'kwaliteit en luxe op maat,',
       'tijd voor uzelf, familie, vrienden en relaties,',
       'comfort in persoonlijk gebruik,',
       'een professioneel georganiseerd verhuurconcept.',
   ])
   + P + 'Daarmee is het Landgoed niet alleen interessant voor later, maar juist ook voor het leven van nu.</p>\n'
   + cta('Plan een persoonlijke kennismaking', 'wd-mail-03a')
   + SIGN),

 dict(n=4, day=5, phase=2,
  title='Zullen we kennismaken op het Landgoed?',
  title_b='Ervaar zelf de sfeer, ligging en mogelijkheden',
  preheader='Ervaar zelf de sfeer, ligging en mogelijkheden',
  preheader_b='Wat we tijdens uw bezoek doornemen',
  kicker='Uitnodiging',
  h1='Het Landgoed komt pas echt tot leven als u er bent',
  body=HI
   + P + 'De rust, de ruimte, de ligging aan de Nederrijn en de opzet van het Landgoed laten zich in een persoonlijk gesprek beter voelen dan in woorden of beelden alleen. Daarom nodigen wij u graag uit voor een kennismaking op locatie.</p>\n'
   + P + 'Tijdens deze afspraak nemen we rustig met u door:</p>\n'
   + bullets([
       'wat Landgoed De Wielsche Dreef bijzonder maakt,',
       'welke mogelijkheden voor u relevant zijn,',
       'welke vorm van gebruik of eigenaarschap het beste past,',
       'hoe het verhuurconcept in de praktijk werkt.',
   ])
   + P + 'Geen standaardverkoop, maar een persoonlijk gesprek met ruimte voor sfeer, vragen en een heldere eerste indruk.</p>\n'
   + quote('Ik heb gekozen voor de rust, de omgeving, de ontspanning en het park. Alles is mooi aangelegd: de sfeer, het interieur, de afwerking. Het gevoel van luxe overheerst: heerlijk, een rijk gevoel.')
   + cta('Maak een afspraak', 'wd-mail-04a')
   + SIGN),

 dict(n=5, day=7, phase=2,
  title='Een eerste selectie van beschikbare mogelijkheden',
  title_b='Een aantal kavels binnen fase 2 is nu in beeld',
  preheader='Een aantal kavels binnen fase 2 is nu in beeld',
  preheader_b='Fase 1 is uitverkocht, fase 2 komt in beeld',
  kicker='Beschikbaarheid',
  h1='Fase 2 komt nu in beeld',
  body=HI
   + P + 'Zoals aangekondigd werken wij met een gefaseerde benadering van het beschikbare aanbod.</p>\n'
   + P + 'Alle vakantiewoningen uit fase 1 zijn verkocht en gaan vanaf juli 2026 in de verhuur via Landal. Op dit moment hebben wij een eerste selectie van mogelijkheden in beeld voor fase 2, voor geinteresseerden die zich tijdig orienteren.</p>\n'
   + P + 'Juist in deze fase merken we dat het waardevol is om vroeg inzicht te krijgen in:</p>\n'
   + bullets([
       'welk type het beste aansluit,',
       'welke ligging het meest aanspreekt,',
       'welke keuzes op termijn relevant kunnen worden.',
   ])
   + P + 'Fase 2 biedt nieuwe kansen doordat er andere kavels beschikbaar komen: een gunstigere ligging, meer privacy of een betere zonorientatie. Daarmee ontstaan keuzemogelijkheden die beter aansluiten op uw persoonlijke wensen.</p>\n'
   + cta('Bespreek beschikbaarheid', 'wd-mail-05a')
   + SIGN),

 dict(n=6, day=9, phase=2,
  title='Wat kost het onderhoud eigenlijk?',
  title_b='Wie regelt het beheer als u er niet bent?',
  preheader='Wie regelt wat, en wat betekent dat voor u',
  preheader_b='Onderhoud, VvE en verhuur op een rij',
  kicker='Bezwaar: het onderhoud',
  h1='U hoeft geen tweede baan als beheerder',
  body=HI
   + P + 'Een terechte vraag bij recreatief vastgoed: wie doet het werk als u er niet bent?</p>\n'
   + P + 'Op Landgoed De Wielsche Dreef is dat volledig geregeld. Het groenonderhoud, de gemeenschappelijke voorzieningen en de infrastructuur worden door de Vereniging van Eigenaren beheerd. De verhuur en het onderhoud van uw villa lopen via Landal.</p>\n'
   + P + 'Concreet betekent dat: u ontvangt een overzicht van hoe het jaar is verlopen en u bepaalt zelf wanneer u er zelf verblijft. Verder hoeft u er niet naar om te kijken.</p>\n'
   + P + 'Dat is precies wat eigenaren van dit concept verwachten. Geen zorgen op afstand, wel de vrijheid van een eigen plek.</p>\n'
   + cta('Vraag naar het beheerconcept', 'wd-mail-06a')
   + SIGN),

 dict(n=7, day=11, phase=2,
  title='Kan ik er zelf ook gewoon verblijven?',
  title_b='Hoeveel weken houdt u zelf beschikbaar?',
  preheader='Eigen gebruik en verhuur naast elkaar',
  preheader_b='U bepaalt zelf wanneer u er bent',
  kicker='Bezwaar: eigen gebruik',
  h1='Uw eigen plek, wanneer u wilt',
  body=HI
   + P + 'Veel mensen denken dat verhuur en eigen gebruik elkaar uitsluiten. Dat is hier niet zo.</p>\n'
   + P + 'U bepaalt zelf welke periodes u voor eigen gebruik reserveert. De resterende weken worden professioneel verhuurd aan vakantiegangers. Zo blijft de villa een plek waar u naartoe gaat, en niet alleen een bezit op papier.</p>\n'
   + P + 'Eigenaren gebruiken hun villa vaak op momenten die voor hen tellen: een week met familie in de zomer, een lang weekend in het najaar, de feestdagen met vrienden. Wat past bij uw ritme, stemmen we samen af.</p>\n'
   + cta('Bespreek uw gebruikswensen', 'wd-mail-07a')
   + SIGN),

 dict(n=8, day=13, phase=2,
  title='Waarom de Betuwe, en niet de kust?',
  title_b='Wat maakt deze ligging bijzonder?',
  preheader='Over de ligging aan de Nederrijn',
  preheader_b='Rust, natuur en bereikbaarheid in een',
  kicker='Bezwaar: de ligging',
  h1='Rust en bereikbaarheid tegelijk',
  body=HI
   + P + 'De kust is populair, maar ook druk, duur en seizoensgebonden. De Betuwe biedt iets anders.</p>\n'
   + P + 'Landgoed De Wielsche Dreef ligt aan de Nederrijn, in een van de rustigste en groenste delen van Nederland. Een gebied dat vogelrijk is, met uiterwaarden, dijken en fietsroutes die het hele jaar door aantrekkelijk zijn.</p>\n'
   + P + 'Tegelijk bent u vanuit de Randstad, Brabant en Gelderland binnen een uur ter plaatse. Dat maakt het verschil tussen een villa waar u twee keer per jaar komt, en een plek waar u ook een doordeweeks moment naartoe rijdt.</p>\n'
   + quote('We fietsen regelmatig, lekker de omgeving verkennen. Het voelt als een stukje thuiskomen met familie en vrienden.')
   + cta('Ontdek de omgeving', 'wd-mail-08a')
   + SIGN),

 dict(n=9, day=14, phase=3,
  title='Het verhaal van een eigenaar van het eerste uur',
  title_b='Waarom zij drie parken vergeleken en hier bleven',
  preheader='Hoe eigenaren tot hun keuze kwamen',
  preheader_b='Van twijfel naar zekerheid, in hun eigen woorden',
  kicker='Verhaal',
  h1='Wat eigenaren over het Landgoed vertellen',
  body=HI
   + P + 'De meest eerlijke beoordeling van een plek komt niet van de verkoper, maar van de mensen die er zijn.</p>\n'
   + quote('We dachten eerst: niet haalbaar, maar later bleek het toch wel haalbaar. Ik vond het park eruit springen. We hebben zeker drie andere parken vergeleken, maar die spraken ons niet aan. Dit park heeft een hele mooie uitstraling.')
   + P + 'Wat in vrijwel elk gesprek terugkomt, is dat de keuze niet in een keer viel. Mensen orienteren zich, vergelijken, bezoeken meerdere parken en komen dan terug. Niet vanwege een aanbieding, maar omdat de sfeer bleef hangen.</p>\n'
   + P + 'Dat is ook precies waarom wij geen haast maken. Een goede keuze heeft tijd nodig.</p>\n'
   + cta('Plan een bezoek', 'wd-mail-09a')
   + SIGN),

 dict(n=10, day=17, phase=3,
  title='Wat een VvE-constructie voor u betekent',
  title_b='Hoe het beheer op het Landgoed is geregeld',
  preheader='Het verschil tussen beheerd en zelf regelen',
  preheader_b='Waarom de VvE-structuur uitmaakt',
  kicker='Inzicht',
  h1='Waarom de beheerstructuur uitmaakt',
  body=HI
   + P + 'Bij recreatievastgoed wordt vaak gekeken naar de villa zelf. De structuur eromheen bepaalt echter minstens zoveel over hoe prettig het eigenaarschap is.</p>\n'
   + P + 'Op Landgoed De Wielsche Dreef is het beheer ondergebracht bij een Vereniging van Eigenaren. Dat betekent dat het onderhoud van het groen, de wegen en de gemeenschappelijke voorzieningen collectief is geregeld, met een vaste bijdrage en een transparante begroting.</p>\n'
   + P + 'Het voordeel: de kwaliteit van het park blijft op peil, ook over tien of twintig jaar. Dat is precies wat de uitstraling en de aantrekkelijkheid voor vakantiegangers op de lange termijn beschermt.</p>\n'
   + cta('Vraag naar de VvE-structuur', 'wd-mail-10a')
   + SIGN),

 dict(n=11, day=21, phase=3,
  title='Een dag op het Landgoed',
  title_b='Hoe een weekend hier eruitziet',
  preheader='Van ochtendmist boven de uiterwaarden tot de avond op het terras',
  preheader_b='Het ritme van een dag aan de Nederrijn',
  kicker='Verhaal',
  h1='Van ochtendmist tot avondzon',
  body=HI
   + P + 'Een villa kopen is geen abstracte beslissing. Het gaat om hoe een dag hier voelt.</p>\n'
   + P + 'De ochtend begint met mist boven de uiterwaarden en vogels die u wakker maken. Koffie op het terras, de dijk op met de fiets, langs de Nederrijn richting het dorp. Middags terug, de tuin in, iemand zet de barbecue aan.</p>\n'
   + P + '&rsquo;s Avonds is het stil. Geen doorgaand verkeer, geen straatverlichting die het donker wegneemt. Alleen het geluid van het water en het park dat tot rust komt.</p>\n'
   + quote('Vogels die ons wakker maken: dit is een cadeautje.')
   + P + 'Dat is wat eigenaren bedoelen als ze zeggen dat het meer is dan een investering.</p>\n'
   + cta('Ervaar het zelf', 'wd-mail-11a')
   + SIGN),

 dict(n=12, day=24, phase=3,
  title='Hoe de verhuur via Landal werkt',
  title_b='Wie zorgt er voor de vakantiegangers?',
  preheader='Boekingen, schoonmaak en onderhoud, geregeld',
  preheader_b='Het verhuurconcept in de praktijk',
  kicker='Inzicht',
  h1='Verhuur zonder dat u iets hoeft te doen',
  body=HI
   + P + 'Vanaf juli 2026 worden de villa&rsquo;s uit fase 1 verhuurd via Landal. Dat is een bewuste keuze.</p>\n'
   + P + 'Landal brengt bereik, een boekingsplatform en een verhuurorganisatie mee die al decennia draait. Voor u als eigenaar betekent dat: geen advertenties plaatsen, geen sleutels overdragen, geen schoonmaak inplannen.</p>\n'
   + P + 'De praktijk is eenvoudig. U geeft aan welke weken u zelf gebruikt. De rest wordt aangeboden, geboekt, schoongemaakt en onderhouden. U ontvangt periodiek een overzicht.</p>\n'
   + P + 'Wat dit voor uw specifieke situatie betekent, hangt af van het type villa, de ligging en het aantal weken eigen gebruik. Dat rekenen we in een gesprek met u door.</p>\n'
   + cta('Vraag het verhuurconcept op', 'wd-mail-12a')
   + SIGN),

 dict(n=13, day=28, phase=3,
  title='Waarom fase 2 andere kansen biedt',
  title_b='De kavels die nu vrijkomen',
  preheader='Ligging, privacy en zonorientatie',
  preheader_b='Wat er in fase 2 anders is dan in fase 1',
  kicker='Inzicht',
  h1='Fase 2: nieuwe posities op het Landgoed',
  body=HI
   + P + 'Fase 1 is volledig verkocht. Dat betekent niet dat de beste plekken weg zijn.</p>\n'
   + P + 'De kavels in fase 2 liggen op andere posities binnen het Landgoed. Een deel grenst direct aan het groen, een deel ligt gunstiger ten opzichte van de zon, en een deel biedt meer privacy dan wat in fase 1 beschikbaar was.</p>\n'
   + P + 'Voor wie zich nu orienteert, is dat een voordeel. U kunt kiezen op basis van uw eigen voorkeuren in plaats van wat er toevallig nog over is.</p>\n'
   + P + 'Welke posities op dit moment in beeld zijn en welke bij u passen, nemen we graag persoonlijk met u door.</p>\n'
   + cta('Bekijk de posities in fase 2', 'wd-mail-13a')
   + SIGN),

 dict(n=14, day=31, phase=3,
  title='Wat vakantiegangers zoeken in een villa',
  title_b='Waarom het type villa uitmaakt',
  preheader='Wat de bezettingsgraad bepaalt',
  preheader_b='De keuzes die vakantiegangers maken',
  kicker='Inzicht',
  h1='Waarom het type villa uitmaakt',
  body=HI
   + P + 'Niet elke villa spreekt dezelfde vakantieganger aan. Dat is relevant, ook voor u.</p>\n'
   + P + 'Vakantiegangers kijken naar het aantal slaapkamers, de aanwezigheid van een tuin of terras, de nabijheid van water en de mate van privacy. Villa&rsquo;s die op meerdere van die punten scoren, worden vaker en langer geboekt.</p>\n'
   + P + 'Op het Landgoed zijn verschillende typen beschikbaar, van compact tot ruim, met verschillende indelingen en liggingen. Welke combinatie het meest aansluit bij zowel uw eigen gebruik als de verhuurpraktijk, verschilt per situatie.</p>\n'
   + P + 'Dat is een van de dingen waar we in een gesprek concreet naar kijken.</p>\n'
   + cta('Bespreek de villatypen', 'wd-mail-14a')
   + SIGN),

 dict(n=15, day=35, phase=3,
  title='Een laatste uitnodiging',
  title_b='Zullen we het gesprek plannen?',
  preheader='Vrijblijvend, op locatie of online',
  preheader_b='Als het niets voor u is, weet u dat ook snel',
  kicker='Uitnodiging',
  h1='Zullen we het gesprek plannen?',
  body=HI
   + P + 'De afgelopen weken hebben we u meegenomen in wat Landgoed De Wielsche Dreef is: de ligging, het concept, het beheer en de manier waarop eigenaarschap hier werkt.</p>\n'
   + P + 'Als het u aanspreekt, is de logische volgende stap een gesprek. Telefonisch, online of op locatie. Wat u prettig vindt.</p>\n'
   + P + 'In dat gesprek kijken we naar uw wensen, de beschikbare posities in fase 2 en wat realistisch en passend is. Vrijblijvend. Als het niets voor u is, weet u dat ook snel.</p>\n'
   + P + 'Liever even bellen of mailen? Dat kan bij Recravas op <strong>' + BRAND["phone"] + '</strong> of via <strong>' + BRAND["email"] + '</strong>.</p>\n'
   + cta('Plan uw gesprek', 'wd-mail-15a')
   + SIGN),
]


def hero_html(n):
    entries = HERO[n]
    if len(entries) == 1:
        key, pos = entries[0]
        url, alt = IMG[key]
        return ('  <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>'
                '<td class="hero" style="height:220px; background-color:#dfe7e5; line-height:0;">'
                '<img src="' + url + '" alt="' + alt + '" width="600" '
                'style="width:100%; height:220px; object-fit:cover; object-position:' + pos + '; display:block;">'
                '</td></tr></table>')
    cells = []
    for key, pos in entries:
        url, alt = IMG[key]
        cells.append('<td class="hero" width="50%" style="height:220px; background-color:#dfe7e5; line-height:0;">'
                     '<img src="' + url + '" alt="' + alt + '" width="300" '
                     'style="width:100%; height:220px; object-fit:cover; object-position:' + pos + '; display:block;">'
                     '</td>')
    return ('  <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>'
            + "".join(cells) + '</tr></table>')


def render(mail, variant):
    is_b = variant == "b"
    html = TEMPLATE
    repl = {
        "TITLE": mail["title_b"] if is_b else mail["title"],
        "PREHEADER": mail["preheader_b"] if is_b else mail["preheader"],
        "KICKER": mail["kicker"],
        "H1": mail["h1"],
        "BODY": mail["body"],
        "HERO_HTML": hero_html(mail["n"]),
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
    }
    for k, v in repl.items():
        html = html.replace("[[" + k + "]]", v)
    if is_b:
        html = html.replace("utm_content=wd-mail-%02da" % mail["n"],
                            "utm_content=wd-mail-%02db" % mail["n"])
    return html


PHASE_LABEL = {1: "Fase 1 &middot; Beste bewijs", 2: "Fase 2 &middot; Bezwaar wegnemen",
                3: "Fase 3 &middot; Verhaal en inzicht"}


def build_index():
    rows = []
    for m in MAILS:
        rows.append(
            '<div class="card" data-phase="%d">' % m["phase"]
            + '<div class="card-top"><span class="badge b%d">Dag %d</span>' % (m["phase"], m["day"])
            + '<span class="num">Mail %02d</span></div>' % m["n"]
            + '<div class="subj"><span class="lbl">A</span>%s</div>' % m["title"]
            + '<div class="subj"><span class="lbl b">B</span>%s</div>' % m["title_b"]
            + '<div class="pre">%s</div>' % m["preheader"]
            + '<div class="links"><a href="mail-%02d.html">Variant A</a>' % m["n"]
            + '<a href="mail-%02db.html">Variant B</a></div>' % m["n"]
            + '</div>'
        )
    phases = "".join(
        '<div class="phase"><h2>%s</h2><div class="grid">%s</div></div>' % (
            PHASE_LABEL[p],
            "".join(r for m, r in zip(MAILS, rows) if m["phase"] == p))
        for p in (1, 2, 3))
    return """<!DOCTYPE html>
<html lang="nl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mailflow Landgoed De Wielsche Dreef</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',sans-serif;background:#f0ebe3;color:#374151;padding:48px 24px 80px}
.wrap{max-width:1100px;margin:0 auto}
header{border-bottom:2px solid #1f524d;padding-bottom:24px;margin-bottom:40px}
.eyebrow{font-size:11px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#be5748;margin-bottom:8px}
h1{font-family:'Playfair Display',serif;font-size:34px;color:#1f524d;font-weight:600;line-height:1.15}
.sub{font-size:14px;color:#7a8c88;margin-top:10px;max-width:640px;line-height:1.6}
.meta{display:flex;gap:32px;margin-top:20px;flex-wrap:wrap}
.mi{font-size:12px}.mi b{display:block;font-size:19px;color:#1f524d;font-family:'Playfair Display',serif}
.mi span{color:#9aaba8;letter-spacing:.1em;text-transform:uppercase;font-size:10px;font-weight:600}
.phase{margin-bottom:44px}
.phase h2{font-family:'Playfair Display',serif;font-size:19px;color:#1f524d;font-weight:600;margin-bottom:18px;padding-bottom:8px;border-bottom:1px solid #ddd5c9}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}
.card{background:#fff;border-radius:6px;padding:18px 20px 16px;border:1px solid #e5ded3}
.card-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
.badge{font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#fff;padding:4px 10px;border-radius:11px}
.b1{background:#1f524d}.b2{background:#be5748}.b3{background:#8a9b6e}
.num{font-size:10px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#b4aa9c}
.subj{font-size:14px;line-height:1.5;color:#1f524d;margin-bottom:7px;display:flex;gap:8px;align-items:flex-start}
.lbl{font-size:9px;font-weight:700;background:#e8efed;color:#1f524d;padding:2px 6px;border-radius:3px;flex-shrink:0;margin-top:3px}
.lbl.b{background:#f7e6e2;color:#be5748}
.pre{font-size:12px;color:#9aaba8;font-style:italic;margin:10px 0 14px;line-height:1.5}
.links{display:flex;gap:8px}
.links a{flex:1;text-align:center;font-size:12px;font-weight:600;padding:8px;border-radius:4px;text-decoration:none;background:#f2f5f4;color:#1f524d;border:1px solid #dde5e3}
.links a:hover{background:#1f524d;color:#fff}
</style></head><body><div class="wrap">
<header>
<div class="eyebrow">Mozi Flow &middot; 3-7-30-methode</div>
<h1>Mailflow Landgoed De Wielsche Dreef</h1>
<p class="sub">15 mails over 35 dagen. Fase 1 dagelijks (beste bewijs), fase 2 om de dag (een bezwaar per mail), fase 3 twee keer per week (verhaal en inzicht). Elke mail heeft een A- en B-variant; de splittest zit uitsluitend in de onderwerpregel.</p>
<div class="meta">
<div class="mi"><b>15</b><span>Mails</span></div>
<div class="mi"><b>35</b><span>Dagen</span></div>
<div class="mi"><b>30</b><span>Varianten</span></div>
<div class="mi"><b>19:00</b><span>Verzendtijd</span></div>
</div>
</header>
""" + phases + """
</div></body></html>"""


def to_ascii(s):
    out = []
    for ch in s:
        if ord(ch) < 128:
            out.append(ch)
        else:
            out.append("&#%d;" % ord(ch))
    return "".join(out)


def main():
    written = []
    for m in MAILS:
        for variant in ("a", "b"):
            name = "mail-%02d%s.html" % (m["n"], "" if variant == "a" else "b")
            (OUT_DIR / name).write_text(to_ascii(render(m, variant)), encoding="ascii")
            written.append(name)
    (OUT_DIR / "index.html").write_text(to_ascii(build_index()), encoding="ascii")
    written.append("index.html")
    print("Geschreven: %d bestanden" % len(written))
    for n in written:
        print("  " + n)


if __name__ == "__main__":
    main()
