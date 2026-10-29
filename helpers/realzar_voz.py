#!/usr/bin/env python3
# OJO: correr con /usr/bin/python3 (el de brew no trae numpy) · GOTCHAS 12
"""
realzar_voz.py · lo que faltaba: masterizar una voz, no solo limpiarla.

    /usr/bin/python3 realzar_voz.py cruda.wav lista.wav [--fuerza 1.0] [--informe]

`sonido_limpio.py` quita RUIDO. Esto arregla las otras dos cosas que hacen
que una grabacion de celular suene "sin calidad", y que ningun quita-ruido
toca:

  1. ECO del cuarto. La propia voz rebotando. Se quita con WPE (Nakatani
     2010), el mismo algoritmo de Kaldi y ESPnet: predice la cola tardia a
     partir de lo que ya sono y se la RESTA. No inventa audio.

  2. TONO. Una voz grabada con el celular lejos y abajo queda retumbada en
     los 200 Hz y sin presencia en los 2-5 kHz, que es exactamente la banda
     donde se entienden las consonantes. Eso no es ruido: es ecualizacion,
     y se corrige MIDIENDO el espectro real y comparandolo con una curva de
     locucion. No se ecualiza de oido ni por receta.

El limite es el mismo de siempre: si se OYE procesado, se paso. Por eso la
correccion va con techo (+-10 dB) y por eso `--informe` imprime las dos
curvas para poder auditar la decision.

NO es Adobe Enhance. Adobe usa un modelo generativo que RESINTETIZA la voz:
queda impecable y a veces deja de ser la voz de la persona. Esto solo resta
y ecualiza, asi que no puede inventar lo que el microfono no capto, pero
tampoco puede cambiar a quien habla.
"""
import os, subprocess, sys, tempfile, wave
import numpy as np
from scipy.signal import firwin2, fftconvolve

# Curva de locucion de referencia (tercios de octava, dB relativos).
# Voz masculina cerca del microfono: cuerpo en 200-300, presencia sostenida
# hasta 5 kHz, caida suave arriba. Es la forma, no el volumen.
OBJETIVO = [(50,-30),(63,-24),(80,-16),(100,-10),(125,-5),(160,-2),(200,-1),
            (250,0),(315,-1),(400,-3),(500,-5),(630,-7),(800,-9),(1000,-10),
            (1250,-11),(1600,-12),(2000,-12),(2500,-12),(3150,-13),(4000,-15),
            (5000,-17),(6300,-20),(8000,-24),(10000,-28),(12500,-33),(16000,-40)]
TECHO = 10.0          # dB: ni un corte ni un realce mayor que este
CORTE = 85            # Hz del filtro de graves: debajo no se corrige nada
SR = 48000


# ----------------------------------------------------------------- utilidades
def _ff(ent, sal, af):
    subprocess.run(["ffmpeg","-y","-v","error","-i",ent,"-af",af,
                    "-ar",str(SR),"-ac","1","-c:a","pcm_s16le",sal], check=True)

def leer(p):
    w=wave.open(p); n=w.getnframes(); sr=w.getframerate(); ch=w.getnchannels()
    x=np.frombuffer(w.readframes(n),dtype=np.int16).astype(np.float64)/32768
    if ch>1: x=x.reshape(-1,ch).mean(axis=1)
    return x,sr

def escribir(p,x,sr):
    pcm=(np.clip(x,-1,1)*32767).astype(np.int16)
    with wave.open(p,"wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(pcm.tobytes())


# ------------------------------------------------------------------ medir
def ltas(x, sr, centros):
    """Espectro promedio SOLO de los cuadros con voz, en tercios de octava."""
    N=2048; H=512
    if len(x) < N: return np.zeros(len(centros))
    tr=np.stack([x[i:i+N]*np.hanning(N) for i in range(0,len(x)-N,H)])
    P=np.abs(np.fft.rfft(tr,axis=1))**2
    en=10*np.log10(P.sum(axis=1)+1e-20)
    voz=P[en > np.percentile(en,65)]          # fuera los silencios
    if not len(voz): voz=P
    pot=voz.mean(axis=0)
    f=np.fft.rfftfreq(N,1/sr)
    out=[]
    for fc in centros:
        lo,hi=fc/2**(1/6), fc*2**(1/6)
        m=(f>=lo)&(f<hi)
        out.append(10*np.log10(pot[m].mean()+1e-20) if m.any() else -200.0)
    return np.array(out)

def rt60(x, sr):
    """RT60 de la sala, medido en la curva de caida PROMEDIO de las pausas.

    OJO, aqui me equivoque dos veces y vale dejarlo escrito: ajustar una
    recta a la envolvente despues de una palabra da numeros absurdos (medi
    1,5 s en un cuarto normal) porque a los ~180 ms la curva ya toco el piso
    de ruido y se APLANA, y la recta promedia esa parte plana. Un piso plano
    extrapola a un RT60 enorme.

    Lo que si funciona: promediar la caida de todas las pausas, y medir el
    tiempo que tarda en bajar de -10 a -30 dB respecto a la palabra, usando
    solo la parte que todavia esta 8 dB por encima del piso. Eso es T20, y
    se extrapola a RT60 por tres.

    Devuelve (rt60, confianza). Confianza False = el piso de ruido esta
    demasiado cerca de la voz y el dato no se puede sostener.
    """
    V=0.010; n=int(V*sr); m=len(x)//n*n
    db=20*np.log10(np.sqrt((x[:m].reshape(-1,n)**2).mean(axis=1))+1e-12)
    alto=np.percentile(db,95); piso=np.percentile(db,5)
    hay=db>(alto-18.0)
    K=int(0.45/V)
    fin=[i for i in np.where(hay[:-1]&~hay[1:])[0]
         if i+K<len(hay) and not hay[i+1:i+K].any()]
    if len(fin)<3: return 0.0, False
    L=int(0.30/V)
    curvas=[]
    for i in fin:
        pre=db[max(0,i-15):i+1].max()
        if pre-piso<32: continue            # sin rango dinamico no hay medida
        curvas.append(db[i:i+L]-pre)
    if len(curvas)<3: return 0.0, False
    c=np.mean(curvas,axis=0)
    rel_piso=piso-np.mean([db[max(0,i-15):i+1].max() for i in fin])
    util=c > rel_piso+8.0                   # fuera la parte plana
    t=np.arange(len(c))*V
    sel=util & (c<=-10.0) & (c>=-30.0)
    if sel.sum()<4: return 0.0, False
    s_,_=np.polyfit(t[sel], c[sel], 1)
    if s_>=-20: return 0.0, False
    return float(60.0/(-s_)), True


def separacion(x, sr):
    V=0.020; n=int(V*sr); m=len(x)//n*n
    db=20*np.log10(np.sqrt((x[:m].reshape(-1,n)**2).mean(axis=1))+1e-12)
    return float(np.percentile(db,95)-np.percentile(db,5))


# -------------------------------------------------------------- 1 · el eco
def desreverberar(x, sr, taps):
    from nara_wpe.wpe import wpe
    from nara_wpe.utils import stft, istft
    o=dict(size=1024, shift=256, window_length=None, fading=True, pad=True,
           symmetric_window=False)
    Y=stft(x[None,:],**o).transpose(2,0,1)              # (F, D=1, T)
    Z=wpe(Y, taps=taps, delay=2, iterations=8, statistics_mode="full")
    z=istft(Z.transpose(1,2,0), size=1024, shift=256)[0][:len(x)]
    p=np.max(np.abs(x))/(np.max(np.abs(z))+1e-12)       # WPE cambia el nivel
    return z*p


# -------------------------------------------------------------- 2 · el tono
def correccion(x, sr, fuerza=1.0):
    centros=np.array([c for c,_ in OBJETIVO], dtype=float)
    obj=np.array([g for _,g in OBJETIVO], dtype=float)
    hay=ltas(x, sr, centros)
    hay=hay-hay.max(); obj=obj-obj.max()
    d=obj-hay
    # sin regalar volumen: se reparte en cortar lo que sobra y realzar lo que falta
    w=10**(obj/20); d=d-np.sum(d*w)/np.sum(w)
    d=np.clip(d*fuerza, -TECHO, TECHO)
    # Debajo del filtro de graves la banda esta vacia A PROPOSITO: "corregirla"
    # seria devolver el retumbe que se acaba de quitar.
    d[centros < CORTE*1.3] = 0.0
    # Arriba de 12,5 kHz un AAC de 64 kbps ya no guardo nada. Realzar ahi
    # solo sube el ruido del propio codec.
    d[centros > 12500] = np.minimum(d[centros > 12500], 0.0)
    return centros, hay, obj, d

def ecualizar(x, sr, centros, d):
    f=np.concatenate(([0.0, 30.0], centros, [min(20000.0, sr/2*0.97), sr/2]))
    g=np.concatenate(([0.0, 0.0], d, [d[-1], 0.0]))
    f,idx=np.unique(f, return_index=True); g=g[idx]
    h=firwin2(2049, f/(sr/2), 10**(g/20))
    y=fftconvolve(x, h, mode="same")
    return y


# ----------------------------------------------------------------- el pase
def realzar(entrada, salida, fuerza=1.0, lufs=-16.0, informe=False):
    tmp=tempfile.mkdtemp(prefix="realzar_")
    a=os.path.join(tmp,"a.wav")
    # 85 Hz: debajo de ahi no hay voz, solo cuarto y manos en el telefono
    _ff(entrada, a, "highpass=f=85")
    x,sr=leer(a)

    rt0,fiable=rt60(x,sr); sep0=separacion(x,sr)
    # El eco manda los taps: cuarto mas vivo, ventana de prediccion mas larga.
    if not fiable:
        # Sin una medida que se sostenga no se desreverbera a ciegas: WPE mal
        # ajustado vacia las consonantes.
        z, rt1, taps = x, 0.0, 0
    else:
        taps=20 if rt0<0.45 else (30 if rt0<0.75 else 40)
        z=desreverberar(x,sr,taps)
        rt1,_=rt60(z,sr)
        if rt1<=0 or rt1>rt0*0.98:   # no empeorar ni gastar por nada
            z, rt1, taps = x, rt0, 0

    centros,cur,obj,d = correccion(z,sr,fuerza)
    y=ecualizar(z,sr,centros,d)
    y=y/(np.max(np.abs(y))+1e-9)*0.89

    sep1=separacion(y,sr)
    b=os.path.join(tmp,"b.wav"); escribir(b,y,sr)
    # Realzar presencia sube tambien el siseo: el de-esser va DESPUES del EQ.
    c=os.path.join(tmp,"c.wav")
    _ff(b, c, "afftdn=nf=-30:tn=1,deesser=i=0.45:f=0.25,"
              "acompressor=threshold=-19dB:ratio=3:attack=10:release=200")
    # loudnorm en pasada aparte · GOTCHAS 6
    _ff(c, salida, f"loudnorm=I={lufs}:TP=-1.5:LRA=9")

    fin,_=leer(salida)
    if not fiable:
        print("eco  (RT60)        no medible (el piso de ruido tapa la cola);"
              " no se desreverbera")
    else:
        print(f"eco  (RT60)        {rt0:5.2f} s  ->  {rt1:5.2f} s"
              + (f"   (WPE taps={taps})" if taps else "   (WPE no ayudo, no se uso)"))
    print(f"separacion         {sep0:5.1f} dB ->  {sep1:5.1f} dB  (antes de comprimir)")
    print(f"inclinacion a presencia  {d[(centros>=2000)&(centros<=4000)].mean()-d[(centros>=160)&(centros<=315)].mean():+5.1f} dB")
    print(f"destino            {lufs} LUFS")
    if informe:
        print("\ntercio de octava   grabado  objetivo  correccion")
        for fc,h_,o_,dd in zip(centros,cur,obj,d):
            marca=" <<" if abs(dd)>=TECHO-0.01 else ""
            print(f"  {fc:8.0f} Hz      {h_:6.1f}   {o_:6.1f}   {dd:+7.1f} dB{marca}")
        print("  << = llego al techo: el microfono no capto mas, no se fuerza")
    # A/B para oir: 7 s antes + 7 s despues
    ab=os.path.splitext(salida)[0]+" (antes y despues).wav"
    subprocess.run(["ffmpeg","-y","-v","error","-i",entrada,"-i",salida,
        "-filter_complex",
        "[0:a]atrim=0:7,asetpts=N/SR/TB,aformat=channel_layouts=mono[a];"
        "[1:a]atrim=0:7,asetpts=N/SR/TB,aformat=channel_layouts=mono[b];"
        "[a][b]concat=n=2:v=0:a=1","-ar",str(SR),"-c:a","pcm_s16le",ab], check=True)
    print(f"\nA/B: {ab}")
    return salida


if __name__=="__main__":
    if len(sys.argv)<3: print(__doc__); sys.exit(1)
    fz=1.0
    if "--fuerza" in sys.argv: fz=float(sys.argv[sys.argv.index("--fuerza")+1])
    realzar(sys.argv[1], sys.argv[2], fuerza=fz, informe="--informe" in sys.argv)
