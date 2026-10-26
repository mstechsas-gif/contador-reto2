"""Genera site/contador.png: cuenta regresiva del Reto 2 (Calculo Diferencial 100410).
Hora de referencia: America/Bogota. Se ejecuta cada pocos minutos con GitHub Actions."""
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

TZ = ZoneInfo("America/Bogota")
EVENTOS = [
    ("CIERRE DEL FORO", "Jueves 19 de noviembre de 2026", datetime(2026, 11, 19, 23, 55, tzinfo=TZ)),
    ("ENTREGA DEL RETO 2", "Lunes 23 de noviembre de 2026 · 11:55 p. m.", datetime(2026, 11, 23, 23, 55, tzinfo=TZ)),
]
AZUL, AZUL_OSC, CLARO, GRIS, ROJO = (21, 71, 148), (12, 44, 100), (232, 240, 252), (90, 100, 120), (192, 38, 38)
F = Path("/usr/share/fonts/opentype/inter")
def fuente(n, t): return ImageFont.truetype(str(F / f"Inter-{n}.otf"), t)

def restante(destino, ahora):
    s = int((destino - ahora).total_seconds())
    if s <= 0: return None
    return s // 86400, s % 86400 // 3600, s % 3600 // 60

# Semaforo: (encabezado, fondo de casillas, numeros)
VERDE = ((22, 128, 61), (226, 246, 233), (14, 84, 40))
NARANJA = ((217, 119, 6), (254, 240, 217), (146, 74, 4))
ROJO_S = ((192, 38, 38), (253, 228, 228), (127, 29, 29))

def semaforo(r):
    if r is None or r[0] < 3: return ROJO_S      # menos de 3 dias
    if r[0] <= 10: return NARANJA                # de 3 a 10 dias
    return VERDE                                 # mas de 10 dias

def tarjeta(d, x, y, w, h, titulo, sub, destino, ahora):
    d.rounded_rectangle((x, y, x + w, y + h), 22, fill="white", outline=(200, 213, 235), width=2)
    r = restante(destino, ahora)
    enc, fondo, num = semaforo(r)
    d.rounded_rectangle((x, y, x + w, y + 56), 22, fill=enc)
    d.rectangle((x, y + 30, x + w, y + 56), fill=enc)
    d.text((x + w / 2, y + 28), titulo, font=fuente("Bold", 22), fill="white", anchor="mm")
    if r is None:
        d.text((x + w / 2, y + 120), "Plazo finalizado", font=fuente("Bold", 34), fill=ROJO, anchor="mm")
    else:
        celda = (w - 60) / 3
        for i, (v, et) in enumerate(zip(r, ("DÍAS", "HORAS", "MINUTOS"))):
            cx = x + 30 + celda * i + celda / 2
            d.rounded_rectangle((cx - celda / 2 + 7, y + 74, cx + celda / 2 - 7, y + 166), 16, fill=fondo)
            d.text((cx, y + 114), f"{v:02d}", font=fuente("Bold", 54), fill=num, anchor="mm")
            d.text((cx, y + 150), et, font=fuente("SemiBold", 13), fill=GRIS, anchor="mm")
    d.text((x + w / 2, y + h - 26), sub, font=fuente("Regular", 16), fill=GRIS, anchor="mm")

def main():
    ahora = datetime.now(TZ)
    W, H = 1000, 330
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    d.text((W / 2, 28), "CUENTA REGRESIVA · RETO 2 · CÁLCULO DIFERENCIAL 100410", font=fuente("Bold", 20), fill=AZUL, anchor="mm")
    for i, (t, s, dest) in enumerate(EVENTOS):
        tarjeta(d, 30 + i * 485, 60, 455, 220, t, s, dest, ahora)
    d.text((W / 2, 308), f"Actualizado: {ahora:%d/%m/%Y %H:%M} (hora de Colombia)", font=fuente("Regular", 14), fill=GRIS, anchor="mm")
    out = Path(__file__).parent / "site"; out.mkdir(exist_ok=True)
    img.save(out / "contador.png", optimize=True)
    (out / "index.html").write_text('<!doctype html><meta charset="utf-8"><title>Contador Reto 2</title><img src="contador.png" style="max-width:100%">', encoding="utf-8")

if __name__ == "__main__":
    main()
