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

from PIL import Image

OUT = pathlib.Path(__file__).parent
BASE = "https://dewielschedreef.nl/wp-content/uploads/"
# 1136x560 = twee keer de weergavemaat 568x280. Deze verhouding (2,03:1) is
# ruimer dan de oorspronkelijke 2,29:1, zodat staande elementen zoals de
# daknok van de avondfoto niet wegvallen.
W, H = 1136, 560

# naam -> (bron, verticale crop-positie 0..1, alt-tekst)
# De bron is een pad op de site, of "bron/<bestand>" voor een lokaal beeld.
SOURCES = {
    "villa_avond":    ("bron/villa-avond.png", 0.33,
                       "Recreatievilla in de avondzon met gasten op het terras"),
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


if __name__ == "__main__":
    main()
