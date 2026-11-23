# -*- coding: utf-8 -*-
"""Buat preview PNG sederhana untuk mod Al-Muhit (versi Mesir merdeka)."""
import os
from PIL import Image, ImageDraw

MOD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 640, 320

im = Image.new("RGB", (W, H), (16, 96, 56))
d = ImageDraw.Draw(im)

# Border emas
d.rectangle([0, 0, W - 1, H - 1], outline=(224, 184, 72), width=6)

# Crescent + bintang sederhana
d.ellipse([70, 70, 230, 230], fill=(236, 196, 76))
d.ellipse([115, 50, 250, 185], fill=(16, 96, 56))
d.polygon([(300, 80), (310, 105), (338, 107), (317, 125),
           (323, 152), (300, 137), (277, 152), (283, 125),
           (262, 107), (290, 105)], fill=(236, 196, 76))

d.text((330, 155), "GRAND SULTANATE", fill=(236, 196, 76))
d.text((330, 185), "OF AL-MUHIT", fill=(236, 196, 76))
d.text((330, 225), "Egypt independent - all states megalopolis",
       fill=(220, 235, 225))

path = os.path.join(MOD, "preview.png")
im.save(path)
print("PREVIEW:", path)
