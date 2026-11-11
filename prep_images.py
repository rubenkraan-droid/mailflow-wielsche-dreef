#!/usr/bin/env python3
"""Haalt de hero-foto's van dewielschedreef.nl, cropt ze op headerformaat en
schrijft geoptimaliseerde JPG's naar deze map.

Gebruik:  python3 prep_images.py

De mails hotlinken niet naar de site: de bestanden daar zijn 250 KB tot 1,5 MB
per stuk. Hier worden ze teruggebracht tot ~100 KB op precies de goede
verhouding (1136x496, twee keer de weergavemaat van 568x248).
"""
import io
import pathlib
import urllib.request

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

OUT = pathlib.Path(__file__).parent
BASE = "https://dewielschedreef.nl/wp-content/uploads/"
# 1136x560 = twee keer de weergavemaat 568x280. Deze verhouding (2,03:1) is
# ruimer dan de oorspronkelijke 2,29:1, zodat staande elementen zoals de
# daknok van de avondfoto niet wegvallen.
W, H = 1136, 560

# Videostills: 1136x639 is twee keer de weergavemaat 568x320 (16:9).
VW, VH = 1136, 639
ACCENT_RGB = (196, 83, 70)          # #c45346, dezelfde accentkleur als de knop
LABEL_FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

# naam -> (bron, verticale crop-positie 0..1, label linksonder of "")
VIDEO_STILLS = {
    "eigenaren": (
        "https://assets.cdn.filesafe.space/ogbyRxgEx1wtnWdZeDwe/media/6aeb0cc9dfd4785f0849b0b0.jpg",
        0.5,
        "Bekijk de video, 1 minuut",
    ),
}

# Portretten bij eigenaarsquotes: naam -> (bron, verticale crop-positie 0..1)
PORTRETTEN = {
    "eigenaren": ("bron/eigenaren.jpg", 0.0),
    # Willem staat onder de ondertekening van elke mail in de tweede flow.
    "willem": ("bron/Willem.png", 0.0),
}

# Kleine vierkante beelden naast de bestemmingen in de afspraak-sequence.
# naam -> (bron, verticale crop-positie 0..1)
# De bestemmingen liggen buiten het Landgoed, dus de parkfotografie van
# dewielschedreef.nl volstaat hier niet. Deze vier staan publiek in de GHL-assets.
# De bestandsnamen daar zijn hashes, dus hieronder staat per URL wat erop staat;
# raakt er ooit een kwijt, dan weet je wat je zoekt.
# Alle vier zijn liggend, dus de crop-positie doet hier niets; hij staat er voor
# als er ooit een staand beeld bij komt.
_GHL = "https://assets.cdn.filesafe.space/ogbyRxgEx1wtnWdZeDwe/media/"
THUMBS = {
    # vaartuig op de rivier in de ochtendmist
    "veerpont":    (_GHL + "6a82fef71082d64877671d9a.jpg", 0.50),
    # reuzenpanda tussen bamboe
    "ouwehands":   (_GHL + "6a82ff8cf730bf01a082c7e0.jpeg", 0.50),
    # appelboom vol appels in een boomgaard
    "boomgaarden": (_GHL + "6a82ff8c38315703fb821775.jpg", 0.50),
    # Rhenen vanaf de Nederrijn, met de Cunerakerk en een molen
    "rhenen":      (_GHL + "6a82ff8c255b571c8e1cc68f.jpg", 0.50),
}

# naam -> (bron, verticale crop-positie 0..1, alt-tekst)
# De bron is een pad op de site, of "bron/<bestand>" voor een lokaal beeld.
SOURCES = {
    "villa_avond":    ("bron/villa-avond.png", 0.33,
                       "Recreatievilla in de avondzon met gasten op het terras"),
    "water_villas":   ("bron/water-villas.jpg", 0.55,
                       "Villa&rsquo;s aan de waterloop op het Landgoed"),
    "villa_vijver":   ("2025/05/6persoonsL-DeWielscheDreef-79-scaled.jpg", 0.42,
                       "Villa aan de vijver met rietoevers"),
    "fietsers_najaar": ("2025/11/verkoopdag.jpg", 0.40,
                       "Fietsen over de laan in het najaar"),
    "villa_water":    ("2025/05/6persoonsC-DeWielscheDreef-57-scaled.jpg", 0.52,
                       "Recreatievilla aan het water op Landgoed De Wielsche Dreef"),
    "wandelen":       ("2025/07/DWD-Algemeen-Stills-44-Header.jpg", 0.45,
                       "Wandelen door de bloemenweide bij het Landgoed"),
    "woonkamer":      ("2025/05/2persoons-DeWielscheDreef-47-scaled.jpg", 0.50,
                       "Woonkamer van een villa op het Landgoed"),
    "villa_parasol":  ("2025/05/6persoonsL-DeWielscheDreef-81-scaled.jpg", 0.55,
                       "Villa met terras en parasol"),
    "park_vanuit_lucht": ("2026/08/DWD_Testweekend_Review.00_07_02_21.Still067.jpg", 0.50,
                       "Luchtfoto van het Landgoed met de waterloop"),
    "villa_riet":     ("2025/05/6persoonsL-DeWielscheDreef-79-scaled.jpg", 0.52,
                       "Villa aan de waterkant met rietoevers"),
    "fietsen":        ("2025/11/verkoopdag.jpg", 0.45,
                       "Fietsen over de laan bij het Landgoed"),
    "betuwe":         ("2026/03/De-mooiste-plekken-en-bezienswaardigheden-in-de-Betuwe.jpg", 0.50,
                       "Dorp in de Betuwe vanuit de lucht"),
    "terras":         ("2025/05/6persoonsL-DeWielscheDreef-77-scaled.jpg", 0.55,
                       "Terras met ligbedden bij een villa"),
    "keuken":         ("2025/05/2persoons-DeWielscheDreef-48-scaled.jpg", 0.50,
                       "Keuken en eethoek in een villa"),
    "slaapkamer":     ("2025/05/2persoons-DeWielscheDreef-45-scaled.jpg", 0.50,
                       "Slaapkamer en badkamer in een villa"),
    "badkamer":       ("2025/05/2persoons-DeWielscheDreef-42-scaled.jpg", 0.50,
                       "Badkamer met vrijstaand bad"),
}


def main():
    for name, (path, ypos, _alt) in SOURCES.items():
        if path.startswith("bron/"):
            im = Image.open(OUT / path).convert("RGB")
        else:
            # de site geeft 403 op de standaard user-agent van urllib
            req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0"})
            raw = urllib.request.urlopen(req, timeout=60).read()
            im = Image.open(io.BytesIO(raw)).convert("RGB")
        w, h = im.size
        target = W / H
        if w / h > target:
            nw = int(h * target)
            im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else:
            nh = int(w / target)
            top = int((h - nh) * ypos)
            im = im.crop((0, top, w, top + nh))
        im = im.resize((W, H), Image.LANCZOS)
        f = OUT / ("hero-%s.jpg" % name)
        im.save(f, "JPEG", quality=80, optimize=True, progressive=True)
        print("%-24s %6d KB" % (f.name, f.stat().st_size // 1024))


def _laad(path):
    """Bron mag een lokaal pad in bron/ zijn, een pad op dewielschedreef.nl,
    of een volledige URL."""
    if path.startswith("bron/"):
        return Image.open(OUT / path).convert("RGB")
    url = path if path.startswith("http") else BASE + path
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=60).read())).convert("RGB")


def videostills():
    """Stills met een afspeelknop erop, voor een klikbare videoafbeelding in
    de mail. 1136x639 is twee keer de weergavemaat 568x320 (16:9).

    E-mailclients spelen geen video af, dus dit is een gewone afbeelding met
    een link eronder. De knop moet er daarom uitzien als een afspeelknop
    zonder er een te zijn.
    """
    for name, (bron, ypos, label) in VIDEO_STILLS.items():
        im = _laad(bron)
        w, h = im.size
        doel = VW / VH
        if w / h > doel:
            nw = int(h * doel)
            im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else:
            nh = int(w / doel)
            top = int((h - nh) * ypos)
            im = im.crop((0, top, w, top + nh))
        im = im.resize((VW, VH), Image.LANCZOS)
        # Iets temperen zodat het wit van de knop en het label blijft staan.
        im = ImageEnhance.Brightness(im).enhance(0.88)

        # Donkere verloop onderaan, alleen voor de leesbaarheid van het label.
        if label:
            verloop = Image.new("L", (1, VH), 0)
            for y in range(VH):
                start = int(VH * 0.55)
                verloop.putpixel((0, y), 0 if y < start
                                 else int(165 * (y - start) / (VH - start)))
            im.paste(Image.new("RGB", (VW, VH), (0, 0, 0)),
                     (0, 0), verloop.resize((VW, VH)))

        # De knop op vier keer de maat tekenen en terugschalen, anders zijn de
        # randen van de cirkel en de driehoek getrapt.
        s = 4
        laag = Image.new("RGBA", (VW * s, VH * s), (0, 0, 0, 0))
        d = ImageDraw.Draw(laag)
        cx, cy, r = VW * s // 2, VH * s // 2, 64 * s
        d.ellipse((cx - r - 5 * s, cy - r - 5 * s, cx + r + 5 * s, cy + r + 5 * s),
                  fill=(255, 255, 255, 60))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ACCENT_RGB + (255,))
        d.polygon([(cx - int(0.26 * r), cy - int(0.42 * r)),
                   (cx - int(0.26 * r), cy + int(0.42 * r)),
                   (cx + int(0.48 * r), cy)], fill=(255, 255, 255, 255))
        laag = laag.resize((VW, VH), Image.LANCZOS)
        im = Image.alpha_composite(im.convert("RGBA"), laag).convert("RGB")

        if label:
            d2 = ImageDraw.Draw(im)
            try:
                font = ImageFont.truetype(LABEL_FONT, 30)
            except OSError:
                font = ImageFont.load_default()
            d2.text((40, VH - 62), label, font=font, fill=(255, 255, 255))

        f = OUT / ("video-%s.jpg" % name)
        im.save(f, "JPEG", quality=82, optimize=True, progressive=True)
        print("%-24s %6d KB" % (f.name, f.stat().st_size // 1024))


def _vierkant(path, ypos, side_out):
    """Middencrop op vierkant, geschaald naar side_out. Bron mag een lokaal pad
    in bron/ zijn, een pad op dewielschedreef.nl, of een volledige URL."""
    if path.startswith("bron/"):
        im = Image.open(OUT / path).convert("RGB")
    else:
        url = path if path.startswith("http") else BASE + path
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=60).read())).convert("RGB")
    w, h = im.size
    side = min(w, h)
    left = (w - side) // 2
    top = int((h - side) * ypos)
    return im.crop((left, top, left + side, top + side)).resize((side_out, side_out), Image.LANCZOS)


# Portretten waarop de persoon klein in beeld staat: een strakkere uitsnede op
# hoofd en schouders, als deel van de breedte en met het midden van het gezicht.
# naam -> (breedte van de uitsnede 0..1, midden horizontaal, midden verticaal)
PORTRET_UITSNEDE = {
    "willem": (0.58, 0.50, 0.46),
}


def portretten():
    """Vierkante portretten, 360x360 (2x de weergavemaat van 180, ruim genoeg
    voor de 92px-avatar bij de ondertekening en het 120px-quoteblok)."""
    for name, (path, ypos) in PORTRETTEN.items():
        if name in PORTRET_UITSNEDE:
            deel, cx, cy = PORTRET_UITSNEDE[name]
            im = _laad(path)
            w, h = im.size
            zij = int(min(w, h) * deel)
            left = max(0, min(w - zij, int(w * cx - zij / 2)))
            top = max(0, min(h - zij, int(h * cy - zij / 2)))
            im = im.crop((left, top, left + zij, top + zij)).resize((360, 360), Image.LANCZOS)
        else:
            im = _vierkant(path, ypos, 360)
        f = OUT / ("portret-%s.jpg" % name)
        im.save(f, "JPEG", quality=82, optimize=True, progressive=True)
        print("%-24s %6d KB" % (f.name, f.stat().st_size // 1024))


def thumbs():
    """Kleine vierkanten bij de bestemmingen, 192x192 (2x weergavemaat 96px)."""
    for name, (path, ypos) in THUMBS.items():
        im = _vierkant(path, ypos, 192)
        f = OUT / ("thumb-%s.jpg" % name)
        im.save(f, "JPEG", quality=82, optimize=True, progressive=True)
        print("%-24s %6d KB" % (f.name, f.stat().st_size // 1024))


# --- beelden voor de conversiepagina ------------------------------------
#
# De hero's hierboven zijn gemaakt voor de mail: 1136 breed is twee keer de
# weergavemaat van 568. Op een webpagina is dat te weinig. De pagina toont de
# themafoto's op ongeveer 720 pixels en het openingsbeeld over de volle breedte
# van het scherm, dus daar horen grotere bestanden bij.
WEB_W, WEB_H = 1600, 788          # themafoto's, ruim 2x de weergavemaat
BANNER_W, BANNER_H = 2400, 1000   # openingsbeeld, over de volle schermbreedte

# Welke beelden de conversiepagina gebruikt, en in welke maat.
WEB_BEELDEN = ["villa_avond", "terras", "keuken", "betuwe", "villa_parasol",
               "woonkamer", "villa_riet", "slaapkamer", "villa_water",
               "park_vanuit_lucht"]
BANNER_BEELDEN = ["water_villas"]


def _crop(im, bw, bh, ypos):
    """Middencrop op de gevraagde verhouding, daarna schalen."""
    w, h = im.size
    doel = bw / bh
    if w / h > doel:
        nw = int(h * doel)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / doel)
        top = int((h - nh) * ypos)
        im = im.crop((0, top, w, top + nh))
    return im.resize((bw, bh), Image.LANCZOS)


def webbeelden():
    """Grotere versies voor de conversiepagina: web-<naam>.jpg en
    banner-<naam>.jpg. De mails blijven de kleinere hero-bestanden gebruiken,
    want daar telt het gewicht zwaarder dan de scherpte."""
    for naam in WEB_BEELDEN:
        pad, ypos, _alt = SOURCES[naam]
        f = OUT / ("web-%s.jpg" % naam)
        _crop(_laad(pad), WEB_W, WEB_H, ypos).save(
            f, "JPEG", quality=78, optimize=True, progressive=True)
        print("%-24s %6d KB" % (f.name, f.stat().st_size // 1024))
    for naam in BANNER_BEELDEN:
        pad, ypos, _alt = SOURCES[naam]
        f = OUT / ("banner-%s.jpg" % naam)
        _crop(_laad(pad), BANNER_W, BANNER_H, ypos).save(
            f, "JPEG", quality=76, optimize=True, progressive=True)
        print("%-24s %6d KB" % (f.name, f.stat().st_size // 1024))


# --- teamportretten ----------------------------------------------------
#
# De vijf portretten op de merkgroene achtergrond, zoals aangeleverd: vierkant
# en zonder uitsnede. De originelen in bron/ zijn 4000x4000 PNG van 7 tot 11 MB,
# veel te zwaar voor een pagina of een mail. Hier gaan ze naar 1000x1000 JPEG.
TEAM = ["Andr\u00e9", "Ruben", "Sem", "Walter", "Willem"]
TEAM_ZIJ = 1000


def teamportretten():
    for naam in TEAM:
        im = Image.open(OUT / "bron" / (naam + ".png")).convert("RGB")
        im = im.resize((TEAM_ZIJ, TEAM_ZIJ), Image.LANCZOS)
        # Bestandsnaam zonder accenten, zodat de URL overal werkt.
        kaal = naam.replace("\u00e9", "e").lower()
        f = OUT / ("team-%s.jpg" % kaal)
        im.save(f, "JPEG", quality=86, optimize=True, progressive=True)
        print("%-24s %6d KB" % (f.name, f.stat().st_size // 1024))


if __name__ == "__main__":
    main()
    portretten()
    thumbs()
    videostills()
    webbeelden()
    teamportretten()
