#!/usr/bin/env python3
# OJO: este se corre con /usr/bin/python3; el modelo vive en otro entorno.
"""
quitar_eco.py · quita la reverberacion de un cuarto chico con Resemble Enhance.

    /usr/bin/python3 quitar_eco.py cruda.wav seca.wav

POR QUE ESTE Y NO OTRO. Se probaron siete modelos de de-reverb de UVR
(DeEcho-DeReverb, De-Echo-Normal, De-Echo-Aggressive, aufr33-jarredou, y tres
MelBand Roformer, uno de ellos con SDR 19,17). **Ninguno quito nada**: la
energia de lo que se llevaron quedo 28 a 59 dB por debajo de la voz y el SRMR
no se movio ni 0,1 dB. Estan entrenados con voces de MUSICA y reverb
artificial de plancha o sala; no se activan con una voz real grabada con
celular en un cuarto de verdad.

Resemble Enhance si, porque no RESTA: resintetiza la voz con un modelo
generativo (flow matching). Medido en la toma de Santiago:
RT60 1,27 s -> 0,14 s.

EL PELIGRO, Y COMO SE DESARMA. Con los valores por omision el modelo
INVENTA. Medido:

    tau=0,5 nfe=64    "calcomania"            -> "pescomania"
                      "Escribanos por WhatsApp" -> "Estriba nuestro WhatsApp"
    tau=0,0 nfe=128   identico a la toma cruda, palabra por palabra

`tau` es la temperatura. **Va en 0 y no se negocia**: ademas de no inventar,
en 0 es determinista, o sea que la misma entrada da el mismo archivo y el
montaje se puede repetir (REGLAS 1.2).

Y aun asi se COMPRUEBA: esta funcion transcribe la entrada y la salida y
compara. Si el modelo cambio una palabra, avisa y no deja pasar el archivo
en silencio. Con un modelo generativo, la transcripcion no es un lujo.

Instalacion (una vez, en su propio entorno; nunca en el python del sistema,
GOTCHAS 15):
    brew install python@3.11
    python3.11 -m venv ~/Proyectos/_modelos/resemble
    ~/Proyectos/_modelos/resemble/bin/pip install resemble-enhance
    # los pesos se bajan a mano porque el descargador pide git-lfs:
    #   huggingface.co/ResembleAI/resemble-enhance -> enhancer_stage2/
    #   dentro de .../site-packages/resemble_enhance/model_repo/
"""
import os, re, subprocess, sys, tempfile
from pathlib import Path

VENV = Path.home() / "Proyectos/_modelos/resemble"
PESOS = (VENV / "lib/python3.11/site-packages/resemble_enhance/model_repo/"
                "enhancer_stage2")
WHISPER = "whisper-cli"
MODELO_W = Path.home() / "Proyectos/_modelos/whisper/ggml-large-v3-turbo.bin"


def disponible():
    return (VENV / "bin/python").exists() and PESOS.exists()


def transcribir(wav):
    t = tempfile.mktemp(suffix=".wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", wav, "-ac", "1",
                    "-ar", "16000", "-c:a", "pcm_s16le", t], check=True)
    r = subprocess.run([WHISPER, "-m", str(MODELO_W), "-l", "es", "-nt",
                        "-f", t], capture_output=True, text=True)
    os.remove(t)
    return r.stdout.strip()


def palabras(s):
    s = s.lower()
    for a, b in (("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ñ","n")):
        s = s.replace(a, b)
    return [w for w in re.findall(r"[a-z]+", s)]


def quitar(entrada, salida, nfe=128, lambd=0.5, verificar=True):
    if not disponible():
        raise RuntimeError(
            "Resemble Enhance no esta instalado. Ver la cabecera de este archivo.\n"
            f"  esperaba  {VENV}\n  y los pesos en  {PESOS}")
    py = str(VENV / "bin/python")
    crudo = tempfile.mktemp(suffix=".wav")
    guion = tempfile.mktemp(suffix=".py")
    Path(guion).write_text(
        "import torch, torchaudio, sys\n"
        "from pathlib import Path\n"
        "from resemble_enhance.enhancer.inference import enhance\n"
        "x, sr = torchaudio.load(sys.argv[1]); x = x.mean(0)\n"
        # tau=0: ni invencion ni azar. cpu: varias operaciones no existen en MPS.
        f"w, s = enhance(x, sr, 'cpu', nfe={nfe}, solver='midpoint',\n"
        f"               lambd={lambd}, tau=0.0, run_dir=Path(sys.argv[3]))\n"
        "torchaudio.save(sys.argv[2], w.unsqueeze(0).cpu(), s)\n")
    print(f"quitando el eco con Resemble Enhance (nfe={nfe}, tau=0)...")
    subprocess.run([py, guion, entrada, crudo, str(PESOS)], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # el modelo entrega 44,1 kHz; el resto de la cadena trabaja a 48
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", crudo, "-ac", "1",
                    "-ar", "48000", "-c:a", "pcm_s16le", salida], check=True)
    os.remove(crudo); os.remove(guion)

    if verificar:
        a, b = palabras(transcribir(entrada)), palabras(transcribir(salida))
        # SequenceMatcher y no zip: si el modelo (o whisper) mete UNA palabra,
        # comparar por posicion desalinea todo lo que viene despues y da 8 %
        # cuando en realidad cambio una sola cosa. Me paso.
        from difflib import SequenceMatcher
        sm = SequenceMatcher(None, a, b)
        iguales = sum(bl.size for bl in sm.get_matching_blocks())
        tot = max(len(a), len(b), 1)
        print(f"palabras iguales a la toma cruda: {iguales}/{tot}"
              f"  ({100*iguales/tot:.0f} %)")
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op != "equal":
                print(f"  {op:8s} cruda[{' '.join(a[i1:i2]) or '-'}]"
                      f" -> salida[{' '.join(b[j1:j2]) or '-'}]")
        if iguales / tot < 0.95:
            print("\n  AVISO: el modelo cambio palabras. NO se entrega asi.")
            print("  Lo que dice la toma cruda:"); print("   ", " ".join(a))
            print("  Lo que dice la salida:");     print("   ", " ".join(b))
            print("  Baja nfe, o quedate con la toma cruda y arregla solo el tono.")
        else:
            print("dice lo mismo: el modelo no invento nada")
    return salida


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    quitar(sys.argv[1], sys.argv[2])
