#!/usr/bin/env python3
"""
Capa 2 y 3: decidir el corte y escribir lo que ffmpeg tiene que ejecutar.

Los cortes caen SIEMPRE dentro de un hueco de silencio medido, nunca en un
tiempo de palabra: los de whisper.cpp son interpolados y cortar ahi se come
silabas (REGLAS 2.1).

De cada pausa se deja un resto: una conversacion sin respiros suena a robot.
"""
import wave, json, numpy as np

SR_OBJ = 16000
UMBRAL = -33.0        # dB, sacado de la distribucion real del material
MIN_HUECO = 0.30      # s
DEJAR = 0.16          # s de respiro que sobrevive a cada pausa

w = wave.open("audio.wav"); n = w.getnframes(); sr = w.getframerate()
x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
DUR = len(x) / sr

V = int(0.02 * sr); m = len(x) // V * V
db = 20 * np.log10(np.sqrt((x[:m].reshape(-1, V) ** 2).mean(axis=1)) + 1e-12)
db = np.convolve(db, np.ones(5) / 5, mode="same")     # 100 ms

# ------------------------------------------------------- huecos de silencio
q = db < UMBRAL
huecos, i = [], 0
while i < len(q):
    if q[i]:
        j = i
        while j < len(q) and q[j]:
            j += 1
        a, b = i * 0.02, j * 0.02
        if b - a >= MIN_HUECO:
            huecos.append((a, b))
        i = j
    else:
        i += 1

# ------------------------------------------------------- que se conserva
# De cada hueco se tira el centro y se dejan DEJAR/2 a cada lado.
conservar, cursor = [], 0.0
for a, b in huecos:
    corte_a = a + DEJAR / 2
    corte_b = b - DEJAR / 2
    if corte_b - corte_a < 0.08:
        continue
    if corte_a > cursor:
        conservar.append((cursor, corte_a))
    cursor = corte_b
if cursor < DUR:
    conservar.append((cursor, DUR))

kept = sum(b - a for a, b in conservar)

# ------------------------------------------------------- remapeo de palabras
d = json.load(open("palabras.json"))

# whisper.cpp con -ml 1 devuelve TOKENS, no palabras: en espanol parte
# "hicimos" en "hic"+"imos". El token que ABRE palabra trae un espacio
# delante; el que continua, no. Se pegan por ahi.
pal = []
for s in d["transcription"]:
    bruto = s["text"]
    txt = bruto.strip()
    if not txt:
        continue
    abre = bruto.startswith((" ", "\u00a0")) or not pal
    if txt in ".,?!;:" and pal:
        pal[-1]["p"] += txt
        pal[-1]["fin"] = s["offsets"]["to"] / 1000
        continue
    if abre:
        pal.append({"t": s["offsets"]["from"] / 1000,
                    "fin": s["offsets"]["to"] / 1000, "p": txt})
    else:
        pal[-1]["p"] += txt
        pal[-1]["fin"] = s["offsets"]["to"] / 1000

def a_salida(ts):
    """Tiempo original -> tiempo en el video ya cortado. None si cayo en un hueco."""
    acc = 0.0
    for a, b in conservar:
        if ts < a:
            return None
        if ts <= b:
            return acc + (ts - a)
        acc += b - a
    return None

# ------------------------------------------------------- subtitulos
# Grupos de 3 a 4 palabras: se leen de un golpe, no obligan a perseguir texto.
grupos, act = [], []
for p in pal:
    act.append(p)
    if len(act) >= 4 or p["p"].endswith((".", "?", "!")):
        grupos.append(act); act = []
if act:
    grupos.append(act)

def esc(s):
    return s.replace("\\", "").replace("{", "").replace("}", "")

def ass_t(s):
    h = int(s // 3600); mnt = int(s % 3600 // 60); sec = s % 60
    return f"{h}:{mnt:02d}:{sec:05.2f}"

lineas = []
for g in grupos:
    ini, fin = a_salida(g[0]["t"]), a_salida(g[-1]["fin"])
    if ini is None or fin is None or fin - ini < 0.25:
        continue
    txt = esc(" ".join(x["p"] for x in g)).replace(" ,", ",").replace(" .", ".")
    lineas.append((ini, fin, txt.strip().upper()))

ASS = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: RV,Archivo,62,&H00F1F6FA,&H000000FF,&H00100A14,&H9E100A14,-1,0,0,0,100,100,0,0,3,0,0,2,180,180,96,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
for ini, fin, txt in lineas:
    ASS += f"Dialogue: 0,{ass_t(ini)},{ass_t(fin)},RV,,0,0,0,,{txt}\n"
open("subs.ass", "w").write(ASS)

# ------------------------------------------------------- filtro de ffmpeg
sel_v = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in conservar)
open("select.txt", "w").write(sel_v)

json.dump({
    "fuente": "material.mov",
    "duracion_original_s": round(DUR, 3),
    "umbral_db": UMBRAL,
    "huecos_detectados": len(huecos),
    "aire_quitado_s": round(DUR - kept, 3),
    "duracion_estimada_s": round(kept, 3),
    "cortes": len(conservar) - 1,
    "subtitulos": len(lineas),
    "conservar": [[round(a, 3), round(b, 3)] for a, b in conservar],
}, open("montaje.json", "w"), ensure_ascii=False, indent=1)

print(f"original      {DUR:7.2f} s")
print(f"huecos        {len(huecos)}")
print(f"aire quitado  {DUR-kept:7.2f} s  ({(DUR-kept)/DUR*100:.1f} %)")
print(f"estimado      {kept:7.2f} s")
print(f"cortes        {len(conservar)-1}")
print(f"subtitulos    {len(lineas)} grupos")
