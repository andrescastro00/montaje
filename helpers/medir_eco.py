#!/usr/bin/env python3
# OJO: /usr/bin/python3 · GOTCHAS 12
"""
medir_eco.py · cuanta reverberacion hay DENTRO del habla.

    /usr/bin/python3 medir_eco.py a.wav b.wav c.wav

Por que hacia falta otra medida: el RT60 se mide en las pausas, y en una
grabacion de celular las pausas ya estan en el piso de ruido, asi que un
desreverberador puede no mover el RT60 y aun asi limpiar muchisimo. El eco
que se OYE no esta en los silencios: esta pegado a las silabas siguientes.

SRMR (Falk, Zheng y Chan, 2010) mide justo eso y sin necesitar una version
limpia de referencia:

  1. banco auditivo de 23 bandas (ERB, 125 Hz a 8 kHz)
  2. la envolvente de cada banda  (lo que modula la voz)
  3. banco de 8 bandas de MODULACION (4 a 128 Hz)
  4. SRMR = energia de modulacion lenta (4-18 Hz, que es el habla: silabas y
     fonemas) dividida por la rapida (29-128 Hz, que es lo que agrega el
     cuarto al embarrar la envolvente)

  SRMR alto  = seco      SRMR bajo = reverberado

Esta es una implementacion propia, fiel al metodo pero no al codigo original
(el banco es Butterworth y no gammatone). Sirve para COMPARAR versiones del
mismo archivo, que es para lo que se usa aqui; no para publicar un numero.
"""
import sys
import numpy as np
from scipy.signal import butter, sosfiltfilt, hilbert, resample_poly

MOD = [4.0, 6.5, 10.7, 17.6, 28.9, 47.5, 78.1, 128.0]   # Hz, los 8 del metodo
LENTAS, RAPIDAS = slice(0, 4), slice(4, 8)
SR_ENV = 1000


def _erb(f):   return 21.4 * np.log10(4.37e-3 * f + 1)
def _ierb(e):  return (10 ** (e / 21.4) - 1) / 4.37e-3

def bandas_auditivas(n=23, f0=125.0, f1=8000.0):
    e = np.linspace(_erb(f0), _erb(f1), n)
    return _ierb(e)

def srmr(x, sr):
    cf = bandas_auditivas()
    # cuadros con voz: el silencio no cuenta, si no el numero mide el cuarto vacio
    V = int(0.020 * sr); m = len(x) // V * V
    pot = (x[:m].reshape(-1, V) ** 2).mean(axis=1)
    db = 10 * np.log10(pot + 1e-20)
    voz = db > (np.percentile(db, 95) - 20)

    lento = rapido = 0.0
    for fc in cf:
        lo, hi = fc / 2 ** (1 / 6), min(fc * 2 ** (1 / 6), sr / 2 * 0.98)
        if lo >= hi: continue
        sos = butter(4, [lo / (sr / 2), hi / (sr / 2)], btype="band", output="sos")
        y = sosfiltfilt(sos, x)
        env = np.abs(hilbert(y))
        env = resample_poly(env, SR_ENV, sr)
        # la mascara de voz, en la rejilla de la envolvente
        k = np.repeat(voz, max(1, int(0.020 * SR_ENV)))[:len(env)]
        if len(k) < len(env): k = np.pad(k, (0, len(env) - len(k)))
        env = env - env.mean()
        for i, mf in enumerate(MOD):
            blo, bhi = mf / 2 ** 0.5, min(mf * 2 ** 0.5, SR_ENV / 2 * 0.95)
            s2 = butter(2, [blo / (SR_ENV / 2), bhi / (SR_ENV / 2)],
                        btype="band", output="sos")
            e = sosfiltfilt(s2, env)
            pe = float((e[k] ** 2).sum())
            if i < 4: lento += pe
            else:     rapido += pe
    return 10 * np.log10(lento / (rapido + 1e-20) + 1e-20)


def leer(p):
    import wave
    w = wave.open(p); n = w.getnframes(); sr = w.getframerate(); ch = w.getnchannels()
    x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64) / 32768
    if ch > 1: x = x.reshape(-1, ch).mean(axis=1)
    return x, sr


if __name__ == "__main__":
    print("REFERENCIA (relativa, para comparar versiones del mismo archivo):")
    print("  mas alto = mas seco · +3 dB ya se oye · +6 dB es otra grabacion\n")
    print(f"{'archivo':44s} {'SRMR':>8s}")
    base = None
    for p in sys.argv[1:]:
        x, sr = leer(p)
        v = srmr(x, sr)
        if base is None: base = v
        print(f"{p[-44:]:44s} {v:7.2f} dB   {v-base:+5.2f}")
