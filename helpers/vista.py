#!/usr/bin/env python3
"""
Arma vista/vista.html: la pagina que deja MIRAR un video a un agente que no ve.

Solo biblioteca estandar, a proposito: tiene que correr aunque no exista .venv.
Se abre con el navegador, con computer use, o se leen los .jpg uno por uno.

    python3 helpers/vista.py trabajos/2026-11-06-reel --cada 0.25
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

ZONAS = {  # medido sobre 1080x1920 (docs: skill/video-de-marca/referencias/diagnostico.md)
    "arriba": 270 / 1920,
    "abajo": 1480 / 1920,
    "derecha": 960 / 1080,
}


def ffprobe(base, sel, campos):
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", sel,
             "-show_entries", f"stream={campos}", "-of", "csv=p=0", str(base)],
            capture_output=True, text=True, timeout=30).stdout.strip().splitlines()
        return out[0].split(",") if out else []
    except Exception:
        return []


def palabras(carpeta):
    """Pega los TOKENS de whisper.cpp en palabras. GOTCHAS 1 bis: el token que
    ABRE palabra trae un espacio al principio, y NO se hace strip() antes de
    decidir. En espanol los tokens parten palabras por la mitad."""
    j = carpeta / "datos" / "palabras.json"
    if not j.exists():
        return []
    try:
        datos = json.loads(j.read_text())
    except Exception:
        return []
    out = []
    for t in datos.get("transcription", []):
        txt = t.get("text", "")
        if not txt.strip():
            continue
        ini = t.get("offsets", {}).get("from", 0) / 1000.0
        fin = t.get("offsets", {}).get("to", 0) / 1000.0
        if txt.startswith(" ") or not out or re.match(r"^[¿¡\"(\[]", txt.strip()):
            out.append({"t": ini, "f": fin, "p": txt.strip()})
        else:
            out[-1]["p"] += txt.strip()
            out[-1]["f"] = fin
    (carpeta / "datos" / "palabras.txt").write_text(
        "\n".join(f'{w["t"]:8.2f}  {w["p"]}' for w in out) or "", encoding="utf-8")
    return out


def main():
    carpeta = Path(sys.argv[1]).expanduser().resolve()
    cada = 1.0
    hasta = None
    for i, a in enumerate(sys.argv):
        if a == "--cada":
            cada = float(sys.argv[i + 1].replace(",", "."))
        if a == "--hasta":
            hasta = float(sys.argv[i + 1])

    brutos = [p for p in sorted((carpeta / "bruto").glob("base.*"))
              if p.suffix.lower() not in (".json", ".jpg", ".png", ".webp", ".txt")]
    if not brutos:
        print("No hay bruto/base.*", file=sys.stderr)
        return 1
    base = brutos[0]

    v = ffprobe(base, "v:0", "width,height,r_frame_rate,duration")
    ancho, alto = (int(v[0]), int(v[1])) if len(v) >= 2 and v[0].isdigit() else (0, 0)
    fps = "?"
    if len(v) >= 3 and "/" in v[2]:
        a, b = v[2].split("/")
        fps = f"{float(a) / float(b):.2f}".rstrip("0").rstrip(".") if float(b) else "?"
    dur = 0.0
    try:
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                    "format=duration", "-of", "csv=p=0", str(base)],
                                   capture_output=True, text=True).stdout.strip())
    except Exception:
        pass
    if hasta:
        dur = min(dur, hasta)
    audio = ffprobe(base, "a:0", "codec_name,sample_rate,channels")
    aud = f"{audio[0]} {audio[1]} Hz" if audio else "sin pista de audio"

    cortes = []
    f = carpeta / "datos" / "cortes.txt"
    if f.exists():
        cortes = [float(x) for x in re.findall(r"^\s*([0-9]+\.[0-9]+)\s*$", f.read_text(), re.M)]
    cpm = round(len(cortes) * 60 / dur) if dur else 0

    fotos = sorted((carpeta / "vista" / "fotogramas").glob("*.jpg"))
    pal = palabras(carpeta)
    vertical = alto > ancho

    def seg(nombre):
        m = re.search(r"s([0-9]+),([0-9]+)", nombre)
        return float(f"{m.group(1)}.{m.group(2)}") if m else 0.0

    rejilla = "\n".join(
        f'<figure data-t="{seg(p.name):.2f}" tabindex="0">'
        f'<img src="fotogramas/{html.escape(p.name)}" alt="segundo {seg(p.name):.2f}" loading="lazy">'
        f'<figcaption>{seg(p.name):.2f} s</figcaption></figure>'
        for p in fotos)

    chips = "\n".join(f'<button data-t="{c:.2f}">{c:.2f} s</button>' for c in cortes) \
        or '<span class="gris">ninguno detectado</span>'

    texto = "\n".join(
        f'<span data-t="{w["t"]:.2f}">{html.escape(w["p"])}</span>' for w in pal) \
        or '<span class="gris">sin transcripcion. Corre ./instalar.sh y vuelve a mirar</span>'

    onda = ""
    if (carpeta / "vista" / "onda.png").exists():
        onda = ('<section><h2>Onda</h2><div id="onda"><img src="onda.png" alt="forma de onda">'
                '<div id="aguja"></div></div>'
                '<p class="gris">Donde esta alto hay voz o un golpe. Lo plano es silencio.</p></section>')

    zonas = ""
    if vertical:
        zonas = (f'<div id="zonas" hidden>'
                 f'<div class="z" style="top:0;height:{ZONAS["arriba"]*100:.1f}%">interfaz de arriba</div>'
                 f'<div class="z" style="top:{ZONAS["abajo"]*100:.1f}%;bottom:0">descripcion</div>'
                 f'<div class="z" style="top:0;bottom:0;left:{ZONAS["derecha"]*100:.1f}%;right:0">botones</div>'
                 f'</div>')

    doc = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(carpeta.name)} · vista</title>
<style>
 :root {{ --tinta:#f4f1ee; --fondo:#121010; --caja:#1c1918; --gris:#8c8683; --acento:#ff6a2b; }}
 * {{ box-sizing:border-box }}
 body {{ margin:0; padding:24px; background:var(--fondo); color:var(--tinta);
        font:15px/1.5 ui-sans-serif,system-ui,-apple-system,"Helvetica Neue",sans-serif }}
 h1 {{ font-size:20px; margin:0 0 4px }} h2 {{ font-size:14px; text-transform:uppercase;
        letter-spacing:.08em; color:var(--gris); margin:28px 0 10px }}
 .gris {{ color:var(--gris) }} a {{ color:var(--acento) }}
 .datos {{ display:flex; flex-wrap:wrap; gap:8px; margin:12px 0 0 }}
 .datos b {{ background:var(--caja); padding:6px 10px; border-radius:6px; font-weight:600;
        font-variant-numeric:tabular-nums }} .datos b i {{ color:var(--gris); font-style:normal; font-weight:400 }}
 .pliego > div:first-child {{ position:sticky; top:16px }}
 @media (max-width:860px) {{ .pliego > div:first-child {{ position:static }} }}
 .pliego {{ display:grid; grid-template-columns:minmax(260px,{'32%' if vertical else '52%'}) 1fr; gap:24px; align-items:start }}
 @media (max-width:860px) {{ .pliego {{ grid-template-columns:1fr }} }}
 #caja {{ position:relative; background:#000; border-radius:10px; overflow:hidden }}
 video {{ width:100%; display:block }}
 #zonas {{ position:absolute; inset:0; pointer-events:none }}
 #zonas .z {{ position:absolute; left:0; right:0; background:rgba(255,106,43,.22);
        border:1px dashed rgba(255,106,43,.75); font-size:11px; color:#fff; padding:2px 5px }}
 .mandos {{ display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin:10px 0 }}
 button {{ background:var(--caja); color:var(--tinta); border:1px solid #2c2725; border-radius:6px;
        padding:5px 9px; font:inherit; font-size:13px; cursor:pointer; font-variant-numeric:tabular-nums }}
 button:hover {{ border-color:var(--acento) }}
 label {{ font-size:13px; color:var(--gris); display:flex; gap:6px; align-items:center; cursor:pointer }}
 #rejilla {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); gap:8px }}
 figure {{ margin:0; cursor:pointer; border-radius:6px; overflow:hidden; background:var(--caja);
        outline:2px solid transparent }}
 figure:hover, figure:focus {{ outline-color:var(--acento) }}
 figure.ahora {{ outline-color:var(--acento) }}
 figure img {{ width:100%; display:block }}
 figcaption {{ font-size:11px; color:var(--gris); padding:3px 6px; font-variant-numeric:tabular-nums }}
 #onda {{ position:relative }} #onda img {{ width:100%; display:block; border-radius:6px }}
 #aguja {{ position:absolute; top:0; bottom:0; width:2px; background:var(--acento); left:0 }}
 #texto span {{ cursor:pointer; padding:1px 2px; border-radius:3px }}
 #texto span:hover {{ background:#2c2725 }} #texto span.ahora {{ background:var(--acento); color:#111 }}
 .hoja img {{ width:100%; max-width:720px; border-radius:8px; display:block }}
 footer {{ margin-top:36px; color:var(--gris); font-size:13px; border-top:1px solid #241f1e; padding-top:14px }}
</style></head><body>

<h1>{html.escape(carpeta.name)}</h1>
<p class="gris">Esta pagina existe para una sola cosa: que quien edita <b>mire</b> el material
antes de decidir. Los numeros son medidos, no estimados.</p>
<div class="datos">
  <b><i>formato</i> {ancho}x{alto} {'vertical' if vertical else 'horizontal'}</b>
  <b><i>duracion</i> {dur:.2f} s</b>
  <b><i>fps</i> {fps}</b>
  <b><i>cortes</i> {len(cortes)} (~{cpm}/min)</b>
  <b><i>audio</i> {html.escape(aud)}</b>
  <b><i>fotogramas</i> {len(fotos)} cada {cada} s</b>
</div>

<div class="pliego">
 <div>
  <h2>El video</h2>
  <div id="caja">
    <video id="v" src="../bruto/{html.escape(base.name)}" controls preload="metadata" playsinline></video>
    {zonas}
  </div>
  <div class="mandos">
    <button id="atras">− 0,5 s</button><button id="play">play</button><button id="alante">+ 0,5 s</button>
    <span class="gris" id="reloj" style="font-variant-numeric:tabular-nums">0,00 s</span>
  </div>
  {'<div class="mandos"><label><input type="checkbox" id="zcheck"> ver las zonas que tapa la interfaz (Reel y TikTok)</label></div>' if vertical else ''}
  <h2>Cortes</h2>
  <div class="mandos">{chips}</div>
  {onda}
 </div>
 <div>
  <h2>Fotogramas · clic para ir a ese segundo</h2>
  <div id="rejilla">{rejilla}</div>
  <h2>Lo que se dice</h2>
  <p id="texto">{texto}</p>
  <h2>Todo en una imagen</h2>
  <div class="hoja"><img src="hoja-de-contacto.jpg" alt="hoja de contacto"></div>
 </div>
</div>

<footer>
 Para un agente sin navegador: <code>vista/hoja-de-contacto.jpg</code> es el video entero en una
 imagen, y <code>vista/fotogramas/sSSSS,CC.jpg</code> es el segundo exacto. Las palabras con su
 milisegundo estan en <code>datos/palabras.txt</code>, los cortes en <code>datos/cortes.txt</code>.
 Como mirar segun lo que sepas hacer: <code>docs/VER-VIDEO.md</code>.
</footer>

<script>
const v = document.getElementById('v'), dur = {dur:.3f};
const ir = t => {{ v.currentTime = Math.max(0, Math.min(t, v.duration || dur)); }};
document.querySelectorAll('[data-t]').forEach(el =>
  el.addEventListener('click', () => ir(parseFloat(el.dataset.t))));
document.querySelectorAll('figure[data-t]').forEach(el =>
  el.addEventListener('keydown', e => {{ if (e.key === 'Enter') ir(parseFloat(el.dataset.t)); }}));
document.getElementById('atras').onclick  = () => ir(v.currentTime - 0.5);
document.getElementById('alante').onclick = () => ir(v.currentTime + 0.5);
document.getElementById('play').onclick   = () => v.paused ? v.play() : v.pause();
const z = document.getElementById('zcheck');
if (z) z.onchange = () => document.getElementById('zonas').hidden = !z.checked;
const aguja = document.getElementById('aguja');
v.addEventListener('timeupdate', () => {{
  const t = v.currentTime;
  document.getElementById('reloj').textContent = t.toFixed(2).replace('.', ',') + ' s';
  if (aguja) aguja.style.left = (100 * t / (v.duration || dur)) + '%';
  let cerca = null, d = 9e9;
  document.querySelectorAll('#rejilla figure').forEach(f => {{
    const dt = Math.abs(parseFloat(f.dataset.t) - t);
    if (dt < d) {{ d = dt; cerca = f; }}
    f.classList.remove('ahora');
  }});
  if (cerca) cerca.classList.add('ahora');
  document.querySelectorAll('#texto span[data-t]').forEach(s => s.classList.remove('ahora'));
  const ws = [...document.querySelectorAll('#texto span[data-t]')]
    .filter(s => parseFloat(s.dataset.t) <= t);
  if (ws.length) ws[ws.length - 1].classList.add('ahora');
}});
</script>
</body></html>
"""
    salida = carpeta / "vista" / "vista.html"
    salida.write_text(doc, encoding="utf-8")
    print(f"  vista/vista.html · {len(fotos)} fotogramas · {len(cortes)} cortes · {len(pal)} palabras")
    return 0


if __name__ == "__main__":
    sys.exit(main())
