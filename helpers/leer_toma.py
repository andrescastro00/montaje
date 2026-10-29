#!/usr/bin/env python3
"""
Leer una toma de locucion. Paso 1 de dos: este MIDE y TRANSCRIBE por bloques.
Decidir que sobra es del humano (o del modelo), nunca de este script.

    /usr/bin/python3 leer_toma.py toma.m4a [--modelo <ruta ggml>]

Imprime, en orden:
  1. nivel, pico y SEPARACION voz-ruido de la toma cruda
  2. que cadena de limpieza conviene (medida, no supuesta)
  3. los bloques de voz con sus fronteras reales y que dice cada uno

Con esa tabla se arma el EDL a mano: pegar los bloques que se quedan, con la
pausa que uno quiera DESPUES de cada uno, y pasarselo a montar_voz.py.

OJO: /usr/bin/python3, no el de Homebrew (GOTCHAS 12).
"""
import os, subprocess, sys, tempfile, wave
import numpy as np

MODELO = os.path.expanduser("~/Proyectos/_modelos/whisper/ggml-small.bin")
QUITA = {
    "suave":  "highpass=f=75,afftdn=nf=-28:tn=1",
    "normal": "highpass=f=80,afftdn=nf=-20:tn=1,anlmdn=s=0.0004,deesser=i=0.4",
}


def _wav(entrada, salida, af=None, sr=48000, mono=False):
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", entrada]
    if af:
        cmd += ["-af", af]
    cmd += ["-ar", str(sr)] + (["-ac", "1"] if mono else []) + ["-c:a", "pcm_s16le", salida]
    subprocess.run(cmd, check=True)


def medir(ruta):
    w = wave.open(ruta); sr = w.getframerate(); ch = w.getnchannels()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    V = int(0.02 * sr); m = len(x) // V * V
    db = 20 * np.log10(np.sqrt((x[:m].reshape(-1, V) ** 2).mean(axis=1)) + 1e-12)
    p5, p95 = np.percentile(db, 5), np.percentile(db, 95)
    return dict(sep=p95 - p5, piso=p5, pico=20 * np.log10(np.abs(x).max() + 1e-12))


def bloques(ruta, umbral=-45, minimo=0.20):
    """Fronteras REALES de voz, por energia. Nunca los tiempos de whisper."""
    s = subprocess.run(["ffmpeg", "-hide_banner", "-i", ruta, "-af",
                        f"silencedetect=noise={umbral}dB:d={minimo}", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    silencios = []
    ini = None
    for ln in s.splitlines():
        if "silence_start:" in ln:
            ini = float(ln.split("silence_start:")[1].split()[0])
        elif "silence_end:" in ln and ini is not None:
            silencios.append((ini, float(ln.split("silence_end:")[1].split()[0]))); ini = None
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", ruta], capture_output=True, text=True).stdout)
    hab, t = [], 0.0
    for a, b in silencios:
        if a - t > 0.04:
            hab.append((t, a))
        t = b
    if dur - t > 0.04:
        hab.append((t, dur))
    return hab


def main():
    src = sys.argv[1]
    modelo = sys.argv[sys.argv.index("--modelo") + 1] if "--modelo" in sys.argv else MODELO
    tmp = tempfile.mkdtemp(prefix="toma-")
    crudo = os.path.join(tmp, "crudo.wav")
    _wav(src, crudo)

    m = medir(crudo)
    print(f"toma          {m['sep']:5.1f} dB de separacion · piso {m['piso']:.1f} · pico {m['pico']:.2f} dBFS")

    mejor, limpio = None, None
    for nombre, cadena in QUITA.items():
        r = os.path.join(tmp, f"{nombre}.wav")
        _wav(crudo, r, cadena)
        mm = medir(r)
        aviso = "  <- SE PASO: piso en silencio digital, va a sonar a lata" if mm["piso"] < -100 else ""
        print(f"  {nombre:7s}     {mm['sep']:5.1f} dB   piso {mm['piso']:7.1f}{aviso}")
        if mm["piso"] > -100 and (mejor is None or mm["sep"] > mejor):
            mejor, limpio = mm["sep"], r
    print(f"\nse sigue con: {os.path.basename(limpio)}  ({limpio})\n")

    hab = bloques(limpio)
    print(f"{len(hab)} bloques de voz\n")
    print(f"{'ini':>8} {'fin':>8} {'dura':>6}   texto")
    for a, b in hab:
        chico = os.path.join(tmp, f"b{a:.3f}.wav")
        _wav(limpio, chico, f"atrim={a}:{b},asetpts=N/SR/TB", sr=16000, mono=True)
        t = subprocess.run(["whisper-cli", "-m", modelo, "-l", "es", "-f", chico, "-nt"],
                           capture_output=True, text=True).stdout.replace("\n", " ").strip()
        print(f"{a:8.3f} {b:8.3f} {b-a:6.2f}   {t}")
    print(f"\nlo limpio quedo en {limpio}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    main()
