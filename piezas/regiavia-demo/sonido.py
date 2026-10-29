#!/usr/bin/env python3
"""
Sonido · RegiaVia · demo del sistema (41,00 s)

Una sola familia tonal, centrada en Fa. Nada de efectos de catalogo.
El cierre repite LAS MISMAS DOS NOTAS del "Cierre de marca" (F3 -> C4):
una marca tambien suena igual siempre.

  0,25   F3     el gancho. Antes de eso, silencio.
  4,45   -      textura de datos, muy baja, mientras se dibuja la onda
 10,35   Eb3    cae un tono: el obstaculo
 14,90   -      seis pulsos, uno por linea de palabra, subiendo
 20,30   C4     abre: la vista compuesta
 26,80   -      pulsos de corte
 30,00   F3+C4  la quinta junta: "lo que sirve se junta"
 32,30   Ab3    calma, se abre el aire
 36,75   F3     el motivo
 38,90   C4     resuelve. Igual que la pieza de 6 s.
"""

import numpy as np
import wave

SR = 48000
DUR = 41.0
N = int(SR * DUR)
t = np.arange(N) / SR

# Notas, en Hz
F2, F3, Ab3, Bb3, C4, Eb3 = 87.31, 174.61, 207.65, 233.08, 261.63, 155.56


def env(inicio, ataque, caida):
    e = np.zeros(N)
    i0 = int(inicio * SR)
    if i0 >= N:
        return e
    rel = t[i0:] - inicio
    e[i0:] = (np.clip(rel / ataque, 0, 1) ** 2) * np.exp(-rel / caida)
    return e


def nota(inicio, f0, gain, caida=2.6, brillo=1.0):
    """Fundamental + octava + quinta. Parciales cada vez mas cortas,
    como suena un cuerpo real. Dos copias desafinadas para dar calor."""
    out = np.zeros(N)
    for mult, amp, dec in ((1, 1.0, 1.0), (2, 0.30 * brillo, 0.72),
                           (3, 0.12 * brillo, 0.52), (4, 0.05 * brillo, 0.38)):
        e = env(inicio, 0.045, caida * dec)
        for cents in (-0.12, 0.12):
            out += amp * np.sin(2 * np.pi * f0 * mult * (2 ** (cents / 1200)) * t) * e
    return out * gain


def pulso(inicio, f0, gain, caida=0.16):
    """Blip corto y suave. Marca un evento sin percutir."""
    e = env(inicio, 0.006, caida)
    return gain * (np.sin(2 * np.pi * f0 * t) + 0.25 * np.sin(4 * np.pi * f0 * t)) * e


def paso_bajo(x, corte_hz):
    """Pasabajos de un polo, vectorizado (convolucion con exponencial)."""
    tau = SR / (2 * np.pi * corte_hz)
    L = int(min(8 * tau, SR))
    k = np.exp(-np.arange(L) / tau)
    k /= k.sum()
    return np.convolve(x, k)[:N]


def textura(inicio, dur, gain, corte=900):
    """Ruido filtrado muy bajo: 'hay datos moviendose'. No es un whoosh."""
    rng = np.random.default_rng(23)          # semilla fija -> render identico
    x = paso_bajo(rng.standard_normal(N), corte)
    x /= np.max(np.abs(x)) + 1e-9
    e = np.clip((t - inicio) / 0.8, 0, 1) * np.clip((inicio + dur - t) / 0.9, 0, 1)
    return gain * x * np.clip(e, 0, 1)


def bed(gain):
    """Zumbido grave que respira. Casi no se oye; se siente si falta."""
    lento = 0.5 + 0.5 * np.sin(2 * np.pi * t / 19.0)
    b = np.zeros(N)
    for f, a in ((F2, 1.0), (F2 * 1.5, 0.22), (F2 * 2, 0.12)):
        for c in (-1.5, 1.5):
            b += a * np.sin(2 * np.pi * f * (2 ** (c / 1200)) * t)
    entra = np.clip(t / 2.2, 0, 1) * np.clip((DUR - t) / 2.0, 0, 1)
    return gain * b * (0.55 + 0.45 * lento) * entra


def reverb(x, cola=1.6, mezcla=0.26):
    rng = np.random.default_rng(11)
    L = int(cola * SR)
    ir = rng.standard_normal(L) * np.exp(-np.arange(L) / (0.30 * SR))
    ir[0] = 1.0
    ir /= np.sqrt(np.sum(ir ** 2))
    return (1 - mezcla) * x + mezcla * np.convolve(x, ir)[:N]


# ------------------------------------------------------------------ la pieza
voz = np.zeros(N)

# 1 · el gancho
voz += nota(0.25, F3, 0.40, caida=3.2)

# 2 · se dibuja la onda: textura, no efecto
voz += textura(4.3, 5.4, 0.045)
voz += pulso(6.05, Bb3 * 2, 0.07)          # silencio
voz += pulso(6.75, Bb3 * 2, 0.07)          # repeticion
voz += pulso(7.45, Bb3 * 2, 0.07)          # muletilla

# 3 · cae un tono. El obstaculo.
voz += nota(10.35, Eb3, 0.38, caida=3.4, brillo=0.7)

# 4 · un pulso por linea, subiendo
for i, f in enumerate((F3 * 2, Ab3 * 2, Bb3 * 2, C4 * 2, C4 * 2 * 1.122, F3 * 4)):
    voz += pulso(14.90 + i * 0.30, f, 0.085)

# 5 · abre
voz += nota(20.30, C4, 0.34, caida=3.0)
voz += textura(20.6, 5.4, 0.035)
voz += pulso(23.60, F3 * 4, 0.10)          # el cuadro que se mira

# 6 · los cortes, y despues la union
for i, ts in enumerate((28.50, 28.95, 29.40)):
    voz += pulso(ts, Eb3 * 2, 0.10)
voz += nota(30.00, F3, 0.34, caida=3.2)    # la quinta junta:
voz += nota(30.00, C4, 0.28, caida=3.2)    # F + C sonando a la vez

# 7 · calma. Se abre el aire.
voz += nota(32.30, Ab3, 0.30, caida=4.0, brillo=0.8)

# 8 · el motivo del cierre de marca, igual que en la pieza de 6 s
voz += nota(36.75, F3, 0.42, caida=3.0)
voz += nota(38.90, C4, 0.46, caida=3.4)
voz += nota(38.90, F3, 0.16, caida=3.4)
voz += 0.20 * np.sin(2 * np.pi * 65.41 * t) * env(38.90, 0.07, 2.0)   # C2, cuerpo

voz = reverb(voz)
voz += bed(0.016)

# ------------------------------------------------------------------ salida
voz /= np.max(np.abs(voz)) + 1e-9
voz *= 0.70
voz *= np.clip((DUR - t) / 0.8, 0, 1)

pcm = (np.clip(np.stack([voz, voz], axis=1), -1, 1) * 32767).astype(np.int16)
with wave.open("audio/pista.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())

print(f"pista -> audio/pista.wav  ({DUR:.2f} s)")
