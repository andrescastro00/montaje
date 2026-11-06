#!/usr/bin/env python3
"""
Subtitulos como capa con alfa, en la marca del cliente.

Las dos marcas de MARCAS son EJEMPLOS. Se agrega la del cliente con sus
colores y su tipografia real, y se pasa su nombre en `marca=`.

Se dibujan aqui porque el ffmpeg de este Mac no trae drawtext ni libass
(GOTCHAS 5). Y resulta mejor: asi llevan la tipografia y los colores de
verdad, no los que libass acepte.

REGLA 3.8: el aire de la caja se mide contra el ALTO REAL DEL GLIFO, no
contra el alto de linea. Arriba y abajo dan el mismo numero. Una version
anterior tenia 20 px arriba y 24 abajo, calculados de memoria, y se notaba.
"""
import os
from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------ marca
MARCAS = {
    "regiavia": {
        "fuente": os.environ.get("MONTAJE_FUENTE", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
        "peso": 800,
        "tinta": (250, 246, 241),
        "caja": (26, 19, 16),
        "acento": (255, 106, 43),
    },
    "oscura": {
        "fuente": os.environ.get("MONTAJE_FUENTE", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
        "peso": 800,
        "tinta": (255, 255, 255),
        "caja": (18, 18, 18),
        "acento": (255, 180, 0),
    },
}

AIRE_X = 52          # aire a izquierda y derecha, dentro de la capsula
AIRE_Y = 30          # MISMO numero arriba y abajo. No se toca uno sin el otro.
OPACIDAD_CAJA = 224


def fuente(ruta, px, peso):
    f = ImageFont.truetype(ruta, px)
    try:
        f.set_variation_by_axes([peso])
    except Exception:
        pass
    return f


def partir(d, texto, F, ancho_max, max_filas=2):
    filas, act = [], ""
    for p in texto.split():
        probar = (act + " " + p).strip()
        if d.textlength(probar, font=F) <= ancho_max or not act:
            act = probar
        else:
            filas.append(act)
            act = p
    if act:
        filas.append(act)
    return filas[:max_filas]


def caja(texto, W, H, marca="regiavia", px=60, acentuar=()):
    """Una capsula con el texto centrado. `acentuar` son palabras en el color
    de acento: sirve para que una idea resalte sin cambiar de tamano."""
    m = MARCAS[marca]
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    F = fuente(m["fuente"], px, m["peso"])

    filas = partir(d, texto, F, W - 380)

    # --- el alto REAL de los glifos de estas filas, no el alto de linea ---
    cajas = [d.textbbox((0, 0), f, font=F) for f in filas]
    sobre = min(c[1] for c in cajas)          # cuanto baja el glifo mas alto
    bajo = max(c[3] for c in cajas)           # hasta donde llega el mas bajo
    alto_glifo = bajo - sobre
    salto = int(px * 1.16)                    # separacion entre filas
    alto_texto = alto_glifo + salto * (len(filas) - 1)

    ancho_texto = max(c[2] - c[0] for c in cajas)
    # enteros en todo: con flotantes el borde redondeado se antialiasa
    # distinto arriba que abajo y el aire sale desparejo por 1 o 2 px.
    ancho = int(round(ancho_texto)) + AIRE_X * 2
    alto = int(round(alto_texto)) + AIRE_Y * 2   # <- el mismo arriba y abajo

    x0 = int((W - ancho) // 2)
    y0 = int((H - alto) // 2)
    d.rounded_rectangle([x0, y0, x0 + ancho, y0 + alto],
                        radius=alto / 2, fill=m["caja"] + (OPACIDAD_CAJA,))

    # El texto se ancla restando `sobre`: asi el aire de arriba es AIRE_Y
    # de verdad, medido hasta el pixel mas alto que se pinta.
    y = y0 + AIRE_Y - sobre
    for i, f in enumerate(filas):
        c = cajas[i]
        x = int((W - (c[2] - c[0])) // 2 - c[0])
        if acentuar:
            # palabra por palabra, para pintar las acentuadas distinto
            cx = x
            for w in f.split():
                col = m["acento"] if w.strip(",.:;!?").upper() in acentuar else m["tinta"]
                d.text((cx, y + i * salto), w, font=F, fill=col)
                cx += d.textlength(w + " ", font=F)
        else:
            d.text((x, y + i * salto), f, font=F, fill=m["tinta"])
    return img


def comprobar_aire(marca="regiavia", px=60):
    """Mide el aire real arriba y abajo. REGLA 3.8: se mide, no se confia."""
    img = caja("PRUEBA DE AIRE", 1920, 250, marca, px)
    a = img.split()[3]
    filas = [y for y in range(img.height) if max(a.crop((0, y, img.width, y + 1)).getdata()) > 0]
    if not filas:
        return None
    top_caja, bot_caja = filas[0], filas[-1]
    px_texto = []
    for y in range(top_caja, bot_caja + 1):
        fila = img.crop((0, y, img.width, y + 1)).convert("RGB").getdata()
        if any(p[0] > 200 and p[1] > 200 for p in fila):
            px_texto.append(y)
    arriba = px_texto[0] - top_caja
    abajo = bot_caja - px_texto[-1]
    return arriba, abajo


if __name__ == "__main__":
    a, b = comprobar_aire()
    print(f"aire arriba: {a} px   aire abajo: {b} px   diferencia: {abs(a-b)} px")
    assert abs(a - b) <= 1, "la caja quedo asimetrica (REGLA 3.8)"
    print("simetrica, pasa")
