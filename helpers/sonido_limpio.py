#!/usr/bin/env python3
"""
Limpieza de voz. Cajon 1: se hace siempre, no se pregunta (REGLAS 0.6).

    python3 sonido_limpio.py entrada.wav salida.wav [--destino redes|calma] [--suave]

Mide la SEPARACION voz-ruido, no el piso a secas: `loudnorm` sube todo y
un piso mas alto despues de normalizar no quiere decir nada. Lo que importa
es cuanto se despega la voz del fondo.

Valores medidos sobre material real (grabacion de pantalla con ruido de
sistema, 116 s):

    sin tocar                                   19,7 dB
    highpass + afftdn nf=-25                    26,3 dB
    highpass + afftdn nf=-20 + tn + anlmdn      30,7 dB   <- esta

Contraintuitivo y vale saberlo: en `afftdn`, un `nf` MENOS negativo asume mas
ruido y limpia mas. Bajarlo a -40 o -60 limpia MENOS (21,3 dB), al reves de
lo que uno esperaria.

EL LIMITE: si se OYE que el audio fue procesado, se paso. Mas vale algo de
ruido que una voz de lata. Para eso esta --suave, y por eso siempre se deja
el A/B para escuchar.
"""
import subprocess, sys, wave
import numpy as np

DESTINOS = {"redes": (-14, -1.5), "calma": (-17, -2.0)}

# Lo que QUITA ruido. Aqui se mide la mejora.
QUITA = {
    "normal": "highpass=f=80,afftdn=nf=-20:tn=1,anlmdn=s=0.0004,deesser=i=0.4",
    "suave":  "highpass=f=75,afftdn=nf=-28:tn=1",
}
# Lo que EMPAREJA. Comprime a proposito, asi que baja la separacion medida:
# no se mide aqui.
EMPAREJA = ("acompressor=threshold=-20dB:ratio=3:attack=12:release=220,"
            "speechnorm=e=6.25:r=0.0003:l=1")


def separacion(ruta):
    """Cuanto se despega la voz del fondo, en dB. Percentil 95 menos el 5."""
    w = wave.open(ruta); n = w.getnframes(); sr = w.getframerate(); ch = w.getnchannels()
    x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    V = int(0.02 * sr); m = len(x) // V * V
    db = 20 * np.log10(np.sqrt((x[:m].reshape(-1, V) ** 2).mean(axis=1)) + 1e-12)
    return float(np.percentile(db, 95) - np.percentile(db, 5))


def _ff(entrada, salida, filtro):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", entrada, "-af", filtro,
                    "-ar", "48000", "-c:a", "pcm_s16le", salida], check=True)


def limpiar(entrada, salida, destino="redes", suave=False, ab=True):
    I, TP = DESTINOS[destino]
    modo = "suave" if suave else "normal"

    antes = separacion(entrada)
    # 1 · solo quitar, para poder medir que tanto quito
    tmp = salida + ".quitado.wav"
    _ff(entrada, tmp, QUITA[modo])
    despues = separacion(tmp)
    # 2 · emparejar y llevar al destino
    _ff(tmp, salida, f"{EMPAREJA},loudnorm=I={I}:TP={TP}:LRA=11")

    gana = despues - antes
    print(f"separacion voz-ruido   {antes:5.1f} dB  ->  {despues:5.1f} dB   ({gana:+.1f} dB)")
    print(f"destino                {I} LUFS / {TP} dBTP")

    if gana < 2:
        print("\n  AVISO: gano menos de 2 dB. O no tenia ruido, o el ruido no es")
        print("  estacionario (voces de fondo, musica, calle): afftdn no lo quita.")
    if gana > 14:
        print("\n  AVISO: gano mas de 14 dB. Riesgo real de voz de lata.")
        print("  Escucha el A/B; si suena procesada, corre con --suave.")

    if ab:
        comp = salida + ".ab.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", entrada, "-i", salida,
                        "-filter_complex",
                        "[0:a]atrim=0:6,asetpts=N/SR/TB[a];[1:a]atrim=0:6,asetpts=N/SR/TB[b];[a][b]concat=n=2:v=0:a=1",
                        "-c:a", "pcm_s16le", comp], check=True)
        print(f"\nA/B (6 s antes + 6 s despues): {comp}")
        print("Escuchalo antes de dar la limpieza por buena.")

    import os
    os.remove(tmp)
    return {"antes": antes, "despues": despues, "gana_db": gana}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    destino = "redes"
    if "--destino" in sys.argv:
        destino = sys.argv[sys.argv.index("--destino") + 1]
    limpiar(sys.argv[1], sys.argv[2], destino, suave="--suave" in sys.argv)
