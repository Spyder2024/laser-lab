import os
from PIL import Image, ImageDraw, ImageFont

def annotate_ndyag():
    im = Image.open('render_ndyag_real.jpg').convert('RGBA')
    w, h = im.size
    overlay = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    # Try loading Arial or default font
    try:
        font = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', 20)
    except:
        font = ImageFont.load_default()

    # Callouts for Nd:YAG (points on 1376 x 768 image)
    # 1: Resonator/Top Head, 2: Flashlamp chamber, 3: Turning mirror, 4: Cutting head nozzle, 5: Workpiece/Rotary chuck, 6: Granite base, 7: Chiller, 8: CNC console
    pts = [
        (1, int(w*0.50), int(h*0.28), int(w*0.50), int(h*0.12)), # 1 Resonator
        (2, int(w*0.44), int(h*0.35), int(w*0.35), int(h*0.18)), # 2 Laser cavity
        (3, int(w*0.56), int(h*0.32), int(w*0.68), int(h*0.18)), # 3 Turning mirror
        (4, int(w*0.52), int(h*0.56), int(w*0.36), int(h*0.56)), # 4 Cutting head
        (5, int(w*0.54), int(h*0.68), int(w*0.68), int(h*0.68)), # 5 Rotary chuck / Part
        (6, int(w*0.50), int(h*0.82), int(w*0.32), int(h*0.82)), # 6 Granite base
        (7, int(w*0.18), int(h*0.62), int(w*0.18), int(h*0.42)), # 7 Chiller
        (8, int(w*0.84), int(h*0.54), int(w*0.84), int(h*0.38))  # 8 CNC Console
    ]

    for num, px, py, cx, cy in pts:
        # Leader line
        draw.line([(px, py), (cx, cy)], fill=(27, 42, 68, 230), width=3)
        # Dot at target
        draw.ellipse([(px-5, py-5), (px+5, py+5)], fill=(209, 63, 41, 255), outline=(27, 42, 68, 255), width=2)
        # Number badge
        r = 16
        draw.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=(250, 248, 240, 255), outline=(27, 42, 68, 255), width=3)
        # Text
        bbox = font.getbbox(str(num))
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((cx - tw/2, cy - th/2 - 2), str(num), fill=(27, 42, 68, 255), font=font)

    result = Image.alpha_composite(im, overlay)
    result.convert('RGB').save('annotated_ndyag_render.jpg', quality=95)
    print("Saved annotated_ndyag_render.jpg")

def annotate_fiber():
    im = Image.open('render_fiber_real.jpg').convert('RGBA')
    w, h = im.size
    overlay = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    try:
        font = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', 20)
    except:
        font = ImageFont.load_default()

    # Callouts for Fiber Laser
    # 1: Yb fiber rack engine, 2: Armored QBH cable, 3: Collimator, 4: Galvo scan head, 5: F-Theta lens, 6: Honeycomb bed, 7: Fume extractor, 8: Operator PC
    pts = [
        (1, int(w*0.28), int(h*0.48), int(w*0.28), int(h*0.22)), # 1 Fiber Rack
        (2, int(w*0.45), int(h*0.38), int(w*0.45), int(h*0.18)), # 2 QBH Cable
        (3, int(w*0.56), int(h*0.38), int(w*0.62), int(h*0.20)), # 3 Collimator
        (4, int(w*0.58), int(h*0.46), int(w*0.72), int(h*0.34)), # 4 Galvo Head
        (5, int(w*0.58), int(h*0.58), int(w*0.72), int(h*0.58)), # 5 F-Theta Lens
        (6, int(w*0.55), int(h*0.75), int(w*0.40), int(h*0.82)), # 6 Honeycomb Bed
        (7, int(w*0.42), int(h*0.58), int(w*0.25), int(h*0.68)), # 7 Fume Extractor
        (8, int(w*0.84), int(h*0.52), int(w*0.84), int(h*0.32))  # 8 PC Console
    ]

    for num, px, py, cx, cy in pts:
        draw.line([(px, py), (cx, cy)], fill=(27, 42, 68, 230), width=3)
        draw.ellipse([(px-5, py-5), (px+5, py+5)], fill=(209, 63, 41, 255), outline=(27, 42, 68, 255), width=2)
        r = 16
        draw.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=(250, 248, 240, 255), outline=(27, 42, 68, 255), width=3)
        bbox = font.getbbox(str(num))
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((cx - tw/2, cy - th/2 - 2), str(num), fill=(27, 42, 68, 255), font=font)

    result = Image.alpha_composite(im, overlay)
    result.convert('RGB').save('annotated_fiber_render.jpg', quality=95)
    print("Saved annotated_fiber_render.jpg")

if __name__ == '__main__':
    annotate_ndyag()
    annotate_fiber()
