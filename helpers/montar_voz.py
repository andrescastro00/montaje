#!/usr/bin/env python3
"""
Paso 2 de dos: pega los bloques elegidos con el aire que uno decide.

El EDL es una lista de (ini, fin, pausa_despues, que_dice). Los dos primeros
salen de leer_toma.py; la pausa la pone quien monta, segun el sentido, no segun
donde cayo al grabar. Eso es lo que convierte una lectura en una locucion.

    from montar_voz import montar
    montar("limpio.wav", EDL, "voz.wav", cabeza=0.60, cola=1.24)

Lo que hace y por que:
  · 0,03 s de margen a cada lado del bloque, para no comerse el ataque
  · 0,01 s de fundido en cada corte, para que no suene el chasquido
  · tono de sala en los huecos: el silencio digital delata el montaje

OJO: /usr/bin/python3, no el de Homebrew (GOTCHAS 12).
"""
import wave
import numpy as np

PAD_IN, PAD_OUT, FADE = 0.030, 0.035, 0.010


def montar(origen, edl, salida, cabeza=0.60, cola=1.20, sala=None, verboso=True):
    """sala = (ini, fin) de un tramo sin voz del MISMO archivo. Sin eso, los
    huecos quedan en cero y la voz suena pegada con cinta."""
    w = wave.open(origen); sr = w.getframerate(); ch = w.getnchannels()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)

    total = cabeza + sum((b - a) + p for a, b, p, *_ in edl) + cola
    y = np.zeros(int(round(total * sr)), dtype=np.float32)

    t = cabeza
    huecos = [(0.0, cabeza)]
    for fila in edl:
        a, b, p = fila[0], fila[1], fila[2]
        i0 = max(0, int((a - PAD_IN) * sr)); i1 = min(len(x), int((b + PAD_OUT) * sr))
        s = x[i0:i1].copy()
        nf = int(FADE * sr)
        v = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, nf))
        s[:nf] *= v; s[-nf:] *= v[::-1]
        j = int(round(t * sr))
        y[j:j + len(s)] += s
        if verboso:
            dice = fila[3] if len(fila) > 3 else ""
            print(f"{t:7.2f}  dura {b-a:5.2f}  pausa {p:5.2f}   {dice}")
        t += (b - a)
        if p > 0:
            huecos.append((t, t + p))
        t += p
    huecos.append((t, total))

    if sala:
        base = x[int(sala[0] * sr):int(sala[1] * sr)]
        for h0, h1 in huecos:
            i0 = max(0, int((h0 - 0.03) * sr)); i1 = min(len(y), int((h1 + 0.03) * sr))
            n = i1 - i0
            if n <= 0:
                continue
            r = np.resize(base, n).copy()
            nf = min(int(0.03 * sr), n // 2)
            if nf > 0:
                v = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, nf))
                r[:nf] *= v; r[-nf:] *= v[::-1]
            y[i0:i1] += r
    elif verboso:
        print("\n  AVISO: sin tono de sala. Los huecos quedan en cero digital y")
        print("  la voz va a sonar pegada encima. Pasa sala=(ini, fin).")

    pcm = (np.clip(np.stack([y, y], 1), -1, 1) * 32767).astype(np.int16)
    with wave.open(salida, "wb") as o:
        o.setnchannels(2); o.setsampwidth(2); o.setframerate(sr)
        o.writeframes(pcm.tobytes())
    if verboso:
        print(f"\nultima palabra en {t - edl[-1][2]:.2f} s · pista {total:.2f} s -> {salida}")
    return total
