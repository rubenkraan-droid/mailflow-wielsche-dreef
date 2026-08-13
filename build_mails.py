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

# Welk mailplatform verstuurt deze flow. Bepaalt de merge-tags in de output.
# "activecampaign" of "ghl".
PLATFORM = "activecampaign"

MERGE_TAGS = {
    "activecampaign": dict(
        first_name="%FIRSTNAME%",
        last_name="%LASTNAME%",
        email="%EMAIL%",
        phone="%PHONE%",
        # AC vult hier de kale uitschrijf-URL in, dus zelf in een <a> wikkelen.
        unsubscribe_block='<a href="%UNSUBSCRIBELINK%" style="color:rgba(255,255,255,0.45); text-decoration:underline;">Uitschrijven</a>',
    ),
    "ghl": dict(
        first_name="{{contact.first_name}}",
        last_name="{{contact.last_name}}",
        email="{{contact.email}}",
        phone="{{contact.phone}}",
        unsubscribe_block='<a href="{{unsubscribe_url}}" style="color:rgba(255,255,255,0.45); text-decoration:underline;">Uitschrijven</a>',
    ),
}

M = MERGE_TAGS[PLATFORM]

BRAND = dict(
    name="Landgoed De Wielsche Dreef",
    short_name="De Wielsche Dreef",
    tagline="Exclusief Vakantievastgoed<br>Betuwe &middot; Nederrijn",
    logo="https://dewielschedreef.nl/wp-content/uploads/2024/09/Logo-wit.svg",
    primary="#004d46",
    footer_bg="#003b36",
    accent="#c45346",
    accent_hover="#a63f34",
    kicker_color="#d3ebe7",
    # Getextureerde groene achtergrond uit het Canva-ontwerp. Wordt gehost op
    # GitHub Pages; #004d46 is de terugvalkleur waar achtergrondafbeeldingen
    # niet werken (onder meer Outlook desktop).
    bg_img="https://rubenkraan-droid.github.io/mailflow-wielsche-dreef/header-bg.jpg",
    # Wit rondom de mail, gebroken wit onder de tekst.
    page_bg="#ffffff",
    card_bg="#f0ebe3",
    text="#374151",
    phone="085 - 303 28 44",
    phone_href="tel:0853032844",
    email="willem@recravas.nl",
    email_href="mailto:willem@recravas.nl",
    contact_party="Recravas",
    cta_url="https://invest.recraparcs.nl/wd-mailflow-lp-page",
    cta_prefill=("email=" + M["email"] + "&first_name=" + M["first_name"]
                 + "&last_name=" + M["last_name"] + "&phone=" + M["phone"]),
    campaign="wielsche-dreef",
    # Eigenarenverhaal als pdf, gehost in ActiveCampaign.
    quote_pdf="https://content.app-us1.com/eYRvv/2026/08/13/8a64e9dc-a480-42dc-a0b0-94e486b652d7.pdf",
    partner_line="Recravas &middot; verhuur verzorgd door Landal",
    disclaimer=("Deze e-mail is algemene informatie en bevat geen aanbod, rendements- of "
                "belastingtoezegging. Aan de inhoud kunnen geen rechten worden ontleend. "
                "Specifieke cijfers, voorwaarden en risico&rsquo;s worden uitsluitend in een "
                "persoonlijk gesprek toegelicht. Deze informatie is geen fiscaal of "
                "beleggingsadvies; laat uw eigen situatie toetsen door een fiscalist of adviseur."),
    credit="Foto&rsquo;s: Landgoed De Wielsche Dreef &middot; Betuwe, aan de Nederrijn.",
)

# Echte parkfotografie, vooraf gecropt op headerformaat door prep_images.py
# en gehost naast de mails. Draai prep_images.py opnieuw na een wijziging daar.
_CDN = "https://rubenkraan-droid.github.io/mailflow-wielsche-dreef/hero-"
IMG = {
    "villa_avond":       (_CDN + "villa_avond.jpg", "Recreatievilla in de avondzon met gasten op het terras"),
    "water_villas":      (_CDN + "water_villas.jpg", "Villa&rsquo;s aan de waterloop op het Landgoed"),
    "villa_vijver":      (_CDN + "villa_vijver.jpg", "Villa aan de vijver met rietoevers"),
    "fietsers_najaar":   (_CDN + "fietsers_najaar.jpg", "Fietsen over de laan in het najaar"),
    "villa_water":       (_CDN + "villa_water.jpg", "Recreatievilla aan het water op Landgoed De Wielsche Dreef"),
    "wandelen":          (_CDN + "wandelen.jpg", "Wandelen door de bloemenweide bij het Landgoed"),
    "woonkamer":         (_CDN + "woonkamer.jpg", "Woonkamer van een villa op het Landgoed"),
    "villa_parasol":     (_CDN + "villa_parasol.jpg", "Villa met terras en parasol"),
    "park_vanuit_lucht": (_CDN + "park_vanuit_lucht.jpg", "Luchtfoto van het Landgoed met de waterloop"),
    "villa_riet":        (_CDN + "villa_riet.jpg", "Villa aan de waterkant met rietoevers"),
    "fietsen":           (_CDN + "fietsen.jpg", "Fietsen over de laan bij het Landgoed"),
    "betuwe":            (_CDN + "betuwe.jpg", "Dorp in de Betuwe vanuit de lucht"),
    "terras":            (_CDN + "terras.jpg", "Terras met ligbedden bij een villa"),
    "keuken":            (_CDN + "keuken.jpg", "Keuken en eethoek in een villa"),
    "slaapkamer":        (_CDN + "slaapkamer.jpg", "Slaapkamer en badkamer in een villa"),
    "badkamer":          (_CDN + "badkamer.jpg", "Badkamer met vrijstaand bad"),
}

# Een foto per mail, in het formaat van de Canva-header (brede liggende crop).
# Elke mail een andere foto; met 10 beelden en 15 mails rouleert een deel.
HERO = {
    1:  "villa_avond",        # signatuurbeeld uit het Canva-ontwerp
    2:  "wandelen",           # mensen in de bloemenweide, warm openingsbeeld
    3:  "slaapkamer",         # comfort en afwerking
    4:  "villa_parasol",      # uitnodigend, kom langs
    5:  "villa_vijver",       # rustig beeld bij het aankooptraject
    6:  "villa_riet",         # verzorgd park
    7:  "fietsen",            # eigen gebruik
    8:  "betuwe",             # de streek
    9:  "terras",             # verhaal van een eigenaar
    10: "keuken",             # inrichting en kwaliteit
    11: "woonkamer",          # een dag op het Landgoed
    12: "fietsers_najaar",    # vakantiegangers op het Landgoed
    13: "badkamer",           # afwerking en kwaliteit
    14: "villa_water",        # wat vakantiegangers zoeken
    15: "villa_parasol",
}

# Merkbalk onder de foto: de zeven kleuren uit het Canva-ontwerp,
# met de breedteverhouding van het origineel.
STRIPE = [
    ("#f1dbb6", 14.6),
    ("#d6a057", 15.7),
    ("#c45346", 15.7),
    ("#44afb7", 14.6),
    ("#00534d", 15.7),
    ("#232b6b", 14.7),
    ("#d3ebe7", 9.0),
]

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
   .hpx{ padding-left:10px!important; padding-right:10px!important; }
   .pcol{ display:block!important; width:100%!important; }
   .pimg{ padding:18px 18px 0 18px!important; }
 }
</style>
</head>
<body style="margin:0; padding:0; background-color:[[PAGE_BG]];">
<!-- Onderwerp: [[TITLE]] -->
<div style="display:none; max-height:0; overflow:hidden; mso-hide:all; font-size:1px; line-height:1px; color:[[PAGE_BG]];">[[PREHEADER]] &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:[[PAGE_BG]];"><tr>
<td align="center" style="padding:24px 12px;">
<table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" style="width:600px; max-width:600px; background-color:[[CARD_BG]]; border-radius:6px; overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,0.06);">
 <tr><td background="[[BG_IMG]]" bgcolor="[[PRIMARY]]" valign="top" style="background-color:[[PRIMARY]]; background-image:url('[[BG_IMG]]'); background-position:center top; background-size:cover; background-repeat:no-repeat; padding:0;">
   <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
     <tr><td style="padding:18px 32px 16px 32px; text-align:center;" class="px">
       <table role="presentation" cellpadding="0" cellspacing="0" align="center" style="margin:0 auto;"><tr>
         <td style="vertical-align:middle; padding-right:16px;">
           <img src="[[LOGO]]" alt="[[BRAND_NAME]]" width="88" style="max-width:88px; height:auto; display:block;">
         </td>
         <td style="vertical-align:middle; padding-left:16px; border-left:1px solid rgba(255,255,255,0.25);">
           <p style="margin:0; font-family:'Inter',Arial,sans-serif; font-size:10px; color:rgba(255,255,255,0.62); letter-spacing:0.16em; text-transform:uppercase; text-align:left; line-height:16px;">[[TAGLINE]]</p>
         </td>
       </tr></table>
     </td></tr>
     <tr><td style="padding:0 16px; line-height:0; font-size:0;" class="hpx">
[[HERO_HTML]]
     </td></tr>
     <tr><td style="padding:0 16px; line-height:0; font-size:0;" class="hpx">
[[STRIPE_HTML]]
     </td></tr>
     <tr><td style="padding:30px 40px 36px 40px;" class="px">
       <div style="font-family:'Inter',Arial,sans-serif; font-size:11px; letter-spacing:0.2em; text-transform:uppercase; color:[[KICKER_COLOR]]; font-weight:bold; margin-bottom:14px;">[[KICKER]]</div>
       <h1 class="h1" style="margin:0; font-family:'Playfair Display',Georgia,serif; font-size:28px; line-height:37px; color:#ffffff; font-weight:600;">[[H1]]</h1>
     </td></tr>
   </table>
 </td></tr>
 <tr><td style="padding:32px 32px 4px 32px; font-family:'Inter',Arial,sans-serif; font-size:16px; line-height:26px; color:[[TEXT]];" class="px">
[[BODY]]
 </td></tr>
 <tr><td style="background-color:[[FOOTER_BG]]; padding:28px 32px; text-align:center;" class="px">
   <img src="[[LOGO]]" alt="[[BRAND_NAME]]" width="100" style="max-width:100px; height:auto; display:inline-block; opacity:0.7; margin-bottom:14px;">
   <p style="margin:0 0 4px 0; font-family:'Inter',Arial,sans-serif; font-size:12px; color:rgba(255,255,255,0.55);">[[PARTNER_LINE]]</p>
   <p style="margin:0 0 16px 0; font-family:'Inter',Arial,sans-serif; font-size:13px;"><a href="[[PHONE_HREF]]" style="color:rgba(255,255,255,0.7); text-decoration:none;">[[PHONE]]</a> &nbsp;&middot;&nbsp; <a href="[[EMAIL_HREF]]" style="color:rgba(255,255,255,0.7); text-decoration:none;">[[EMAIL]]</a></p>
   <p style="margin:0 0 12px 0; font-family:'Inter',Arial,sans-serif; font-size:11px; line-height:17px; color:rgba(255,255,255,0.45); max-width:460px; margin-left:auto; margin-right:auto;">[[DISCLAIMER]]</p>
   <p style="margin:0; font-family:'Inter',Arial,sans-serif; font-size:11px; color:rgba(255,255,255,0.45);">[[BRAND_NAME]] &nbsp;&middot;&nbsp; [[UNSUBSCRIBE]]</p>
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


def quote_person(text, portret, alt, caption):
    """Quote met een vierkant portret ernaast. Stapelt onder 620px."""
    src = _CDN.replace("hero-", "portret-") + portret + ".jpg"
    return ('   <table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            'style="margin:4px 0 20px 0; background-color:#eef4f3; border-left:4px solid '
            + BRAND["primary"] + ';"><tr>'
            '<td class="pcol pimg" width="120" valign="top" style="padding:18px 0 18px 18px; width:120px;">'
            '<img src="' + src + '" alt="' + alt + '" width="120" '
            'style="width:120px; max-width:120px; height:auto; display:block; border-radius:4px;">'
            '</td>'
            '<td class="pcol" valign="top" style="padding:18px 22px; font-family:\'Inter\',Arial,sans-serif;">'
            '<div style="font-style:italic; font-size:16px; line-height:26px; color:#1a1a1a;">'
            '&ldquo;' + text + '&rdquo;</div>'
            '<div style="font-size:13px; line-height:20px; color:#5f7a75; padding-top:10px;">'
            + caption + '</div>'
            '</td></tr></table>\n')


def pdf_link(label):
    """Tekstlink naar het eigenarenverhaal als pdf, met pdf-icoon in tekstvorm."""
    return ('   <p style="margin:0 0 20px 0;"><a href="' + BRAND["quote_pdf"] + '" target="_blank" '
            'style="color:' + BRAND["primary"] + '; font-weight:bold; text-decoration:underline;">'
            + label + '</a> <span style="color:#8a9a95; font-size:14px;">(pdf)</span></p>\n')


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
HI = P + 'Beste ' + M["first_name"] + ',</p>\n'

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
   + P + 'Eigenaren die hier vorig jaar voor kozen, verwoordden hun eerste indruk zo:</p>\n'
   + quote_person(
       'Prachtig gebied. Echt heel natuurvriendelijk en vogelrijk. We zijn allebei gek op vogels, '
       'maar ook op het landschap en de manier waarop het park zich daarin ontwikkelt. Vanaf het '
       'eerste moment heeft het ons niet meer losgelaten.',
       'eigenaren', 'Eigenaren op Landgoed De Wielsche Dreef',
       'Eigenaren van een vierpersoonswoning aan het water')
   + P + 'Wat dat dagelijks oplevert, vatten ze zelf het mooist samen:</p>\n'
   + quote('We kijken zo uit over het water. Vanmorgen deden we de gordijnen open en zwom er een meerkoet met kleintjes voorbij. Dat is toch een cadeautje? Zo begin je je dag.')
   + pdf_link('Lees hun volledige verhaal')
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
  title='Hoe verloopt zo&rsquo;n traject eigenlijk?',
  title_b='Van eerste gesprek tot de sleutel',
  preheader='Wat u kunt verwachten, stap voor stap',
  preheader_b='Geen verrassingen, wel duidelijkheid vooraf',
  kicker='Bezwaar: de onbekendheid',
  h1='Weten waar u aan begint',
  body=HI
   + P + 'Veel mensen orienteren zich maandenlang op een vakantiewoning zonder ooit te vragen hoe zo&rsquo;n aankoop nu eigenlijk verloopt. Begrijpelijk, want niemand wil ergens instappen zonder het overzicht te hebben.</p>\n'
   + P + 'Daarom zetten we het hier gewoon op een rij:</p>\n'
   + bullets([
       'een kennismaking waarin we uw wensen en situatie doornemen,',
       'een rondleiding op het Landgoed, zodat u de ligging zelf ervaart,',
       'een keuze voor een type villa en een plek die daarbij past,',
       'de vastlegging bij de notaris, met heldere voorwaarden,',
       'de oplevering, waarna verhuur en beheer worden overgenomen.',
   ])
   + P + 'Tussen die stappen zit geen druk. U bepaalt zelf het tempo, en bij elke stap weet u wat de volgende inhoudt.</p>\n'
   + P + 'De eerste stap kost u niet meer dan een gesprek. Daarin hoort u wat er mogelijk is, en wij horen of dit uberhaupt bij u past.</p>\n'
   + cta('Plan een kennismaking', 'wd-mail-05a')
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
   + P + 'Op Landgoed De Wielsche Dreef is dat volledig geregeld. Het groenonderhoud, de gemeenschappelijke voorzieningen en de infrastructuur worden door de Vereniging van Eigenaren beheerd. De verhuur van uw villa loopt via Landal.</p>\n'
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
   + P + 'U bepaalt zelf welke periodes u voor eigen gebruik reserveert, tot 90 dagen per jaar. De resterende weken worden professioneel verhuurd aan vakantiegangers. Zo blijft de villa een plek waar u naartoe gaat, en niet alleen een bezit op papier.</p>\n'
   + P + 'Negentig dagen is in de praktijk ruim. Eigenaren gebruiken hun villa vaak op momenten die voor hen tellen: een week met familie in de zomer, een lang weekend in het najaar, de feestdagen met vrienden. Wat past bij uw ritme, stemmen we samen af.</p>\n'
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
   + P + 'Een echtpaar dat hier nu een woning heeft, dacht aanvankelijk dat het er voor hen niet in zat. Ze besloten de mogelijkheden toch te onderzoeken.</p>\n'
   + quote('We vonden dit park er echt uitspringen. We hebben ook andere parken bekeken, in Nederland en Belgie, maar die spraken ons niet aan. Hier hebben de woningen met hun schuine daken echt een mooie, warme uitstraling. Het voelt gezellig en bijzonder.')
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
   + P + 'De ochtend begint met mist boven de uiterwaarden en vogels die u wakker maken. Koffie op het terras, de dijk op met de fiets, langs de Nederrijn richting het dorp. Middags terug, de tuin in, de zon schuift langzaam over het terras.</p>\n'
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
   + P + 'De villa&rsquo;s op het Landgoed worden verhuurd via Landal. Dat is een bewuste keuze.</p>\n'
   + P + 'Landal brengt bereik, een boekingsplatform en een verhuurorganisatie mee die al decennia draait. Voor u als eigenaar betekent dat: geen advertenties plaatsen, geen sleutels overdragen, geen schoonmaak inplannen.</p>\n'
   + P + 'De praktijk is eenvoudig. U geeft aan welke weken u zelf gebruikt, tot 90 dagen per jaar. De rest van het jaar is uw villa beschikbaar voor verhuur, en die wordt aangeboden, geboekt, schoongemaakt en onderhouden zonder dat u er iets voor hoeft te doen.</p>\n'
   + P + 'Er is een punt dat veel mensen niet verwachten. De verhuur loopt via een pool: alle villa&rsquo;s van hetzelfde type vormen samen een groep, en de inkomsten uit de verhuur worden binnen die groep verdeeld.</p>\n'
   + P + 'Dat heeft een prettig gevolg. Of nu juist uw villa geboekt wordt of een woning van hetzelfde type verderop, maakt voor u geen verschil. U bent niet afhankelijk van de boekingen van een enkele woning, maar deelt mee in het resultaat van de hele groep.</p>\n'
   + P + 'Hoe dat precies is vastgelegd en wat het voor uw situatie betekent, nemen we in een gesprek met u door.</p>\n'
   + cta('Vraag het verhuurconcept op', 'wd-mail-12a')
   + SIGN),

 dict(n=13, day=28, phase=3,
  title='Niet elke plek op het Landgoed is hetzelfde',
  title_b='Waarom de ene kavel anders ligt dan de andere',
  preheader='Ligging, zonorientatie en privacy',
  preheader_b='Wat het verschil maakt tussen twee kavels',
  kicker='Inzicht',
  h1='Waarom de plek op het Landgoed uitmaakt',
  body=HI
   + P + 'Twee villa&rsquo;s van hetzelfde type kunnen heel verschillend aanvoelen. Dat zit hem zelden in de woning zelf, en bijna altijd in waar die staat.</p>\n'
   + P + 'Op het Landgoed verschillen de posities op een paar punten die u pas merkt als u er staat:</p>\n'
   + bullets([
       'de orientatie op de zon, en dus waar u &rsquo;s avonds zit,',
       'de mate van privacy en het zicht vanaf uw terras,',
       'of een kavel direct aan het groen of aan het water grenst,',
       'de afstand tot de voorzieningen en de entree van het park.',
   ])
   + P + 'Die verschillen bepalen vooral hoe u de plek zelf beleeft. Voor de verhuur wegen ze minder zwaar dan u zou verwachten, want de inkomsten worden verdeeld binnen een pool van villa&rsquo;s van hetzelfde type. U kiest een plek dus in de eerste plaats voor uzelf.</p>\n'
   + P + 'Dat maakt de keuze eenvoudiger. U hoeft niet te gokken welke kavel het beste verhuurt, maar kunt kijken waar u zelf het liefst zit. Welke posities bij uw voorkeuren passen, nemen we graag persoonlijk met u door.</p>\n'
   + cta('Bespreek de mogelijkheden', 'wd-mail-13a')
   + SIGN),

 dict(n=14, day=31, phase=3,
  title='Wat vakantiegangers zoeken in een villa',
  title_b='Waarom het type villa uitmaakt',
  preheader='Wat de bezettingsgraad bepaalt',
  preheader_b='De keuzes die vakantiegangers maken',
  kicker='Inzicht',
  h1='Waarom het type villa uitmaakt',
  body=HI
   + P + 'Niet elk type villa spreekt dezelfde vakantieganger aan. Dat is relevant, ook voor u.</p>\n'
   + P + 'Vakantiegangers kijken naar het aantal slaapkamers, de aanwezigheid van een tuin of terras, de nabijheid van water en de mate van privacy. Dat bepaalt welke typen het hele jaar door in trek zijn en welke vooral in het hoogseizoen.</p>\n'
   + P + 'Voor u telt dat mee, omdat de verhuurinkomsten worden verdeeld binnen een pool van villa&rsquo;s van hetzelfde type. De keuze voor een type is daarmee meer dan een smaakkwestie: u kiest ook in welke groep u meedeelt.</p>\n'
   + P + 'Op het Landgoed zijn verschillende typen beschikbaar, van compact tot ruim, met verschillende indelingen. Welk type het beste aansluit bij zowel uw eigen gebruik als de verhuurpraktijk, verschilt per situatie. Dat is een van de dingen waar we in een gesprek concreet naar kijken.</p>\n'
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
   + P + 'In dat gesprek kijken we naar uw wensen, de beschikbare posities op het Landgoed en wat realistisch en passend is. Vrijblijvend. Als het niets voor u is, weet u dat ook snel.</p>\n'
   + P + 'Liever even bellen of mailen? Dat kan bij Recravas op <strong>' + BRAND["phone"] + '</strong> of via <strong>' + BRAND["email"] + '</strong>.</p>\n'
   + cta('Plan uw gesprek', 'wd-mail-15a')
   + SIGN),
]


def hero_html(n):
    """Een brede foto met groene marge eromheen, zoals in het Canva-ontwerp."""
    url, alt = IMG[HERO[n]]
    # De foto is al op 1136x496 gecropt, dus schalen volstaat: geen object-fit
    # nodig (dat werkt toch niet in Outlook).
    return ('  <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>'
            '<td class="hero" style="background-color:#dfe7e5; line-height:0; font-size:0;">'
            '<img src="' + url + '" alt="' + alt + '" width="568" '
            'style="width:100%; max-width:568px; height:auto; display:block;">'
            '</td></tr></table>')


def stripe_html():
    """De zevenkleurige merkbalk direct onder de foto."""
    cells = "".join(
        '<td width="%s%%" style="width:%s%%; background-color:%s; height:20px; '
        'line-height:20px; font-size:0;">&nbsp;</td>' % (pct, pct, col)
        for col, pct in STRIPE)
    return ('  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
            'style="border-collapse:collapse;"><tr>' + cells + '</tr></table>')


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
        "STRIPE_HTML": stripe_html(),
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
            + '<div class="links"><a href="mail-%02d.html">Preview mail</a></div>' % m["n"]
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
