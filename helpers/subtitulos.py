#!/usr/bin/env python3
"""
Capa de subtitulos como overlay con alfa, en la marca de RegiaVia.
Este ffmpeg no trae drawtext ni libass, asi que la banda se dibuja aqui.
"""
import json, re, os
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 250
ESPRESSO = (26, 19, 16)
CREMA = (250, 246, 241)
NARANJA = (255, 106, 43)
FUENTE = "/Users/santiagocastro/Library/Fonts/Archivo-var.ttf"

os.makedirs("subs", exist_ok=True)

def fuente(px, peso=800):
    f = ImageFont.truetype(FUENTE, px)
    try:
        f.set_variation_by_axes([peso])
    except Exception:
        pass
    return f

F = fuente(60, 800)

# Lee los tiempos ya remapeados que escribio montar.py
lineas = []
for ln in open("subs.ass", encoding="utf-8"):
    if not ln.startswith("Dialogue:"):
        continue
    partes = ln.split(",", 9)
    def seg(s):
        h, m, rest = s.split(":")
        return int(h) * 3600 + int(m) * 60 + float(rest)
    lineas.append((seg(partes[1]), seg(partes[2]), partes[9].strip()))

def caja(texto):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # parte el texto si no cabe
    maxw = W - 380
    palabras, filas, act = texto.split(), [], ""
    for p in palabras:
        probar = (act + " " + p).strip()
        if d.textlength(probar, font=F) <= maxw:
            act = probar
        else:
            if act:
                filas.append(act)
            act = p
    if act:
        filas.append(act)
    filas = filas[:2]

    alto_f = 74
    alto = alto_f * len(filas) + 44
    ancho = max(d.textlength(f, font=F) for f in filas) + 96
    x0 = (W - ancho) / 2
    y0 = (H - alto) / 2
    # capsula completa, nunca esquina suave
    d.rounded_rectangle([x0, y0, x0 + ancho, y0 + alto],
                        radius=alto / 2, fill=ESPRESSO + (222,))
    for i, f in enumerate(filas):
        tw = d.textlength(f, font=F)
        d.text(((W - tw) / 2, y0 + 20 + i * alto_f), f, font=F, fill=CREMA)
    return img

vacio = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vacio.save("subs/vacio.png")

concat, cursor, n = [], 0.0, 0
for ini, fin, txt in lineas:
    if ini > cursor + 0.04:
        concat.append(("subs/vacio.png", ini - cursor))
    p = f"subs/s{n:04d}.png"
    caja(txt).save(p)
    concat.append((p, max(0.12, fin - ini)))
    cursor = fin
    n += 1

with open("subs/lista.txt", "w") as fh:
    for p, dur in concat:
        fh.write(f"file '{os.path.abspath(p)}'\nduration {dur:.3f}\n")
    fh.write(f"file '{os.path.abspath(concat[-1][0])}'\n")

print(f"cajas dibujadas : {n}")
print(f"tramos en pista : {len(concat)}")
print(f"largo de pista  : {sum(d for _, d in concat):.2f} s")
