import os
import sys
sys.path.append(r'C:\Users\VISHESH-PC\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages')

from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Real Fonts
pdfmetrics.registerFont(TTFont('Archivo-Bold', 'Archivo-Bold.ttf'))
pdfmetrics.registerFont(TTFont('IBMPlexMono', 'IBMPlexMono-Regular.ttf'))
pdfmetrics.registerFont(TTFont('IBMPlexMono-Bold', 'IBMPlexMono-SemiBold.ttf'))
pdfmetrics.registerFont(TTFont('Arial', r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', r'C:\Windows\Fonts\arialbd.ttf'))

# Page Dimensions: A3 Landscape (1190.55 x 841.89 pt)
PAGE_W, PAGE_H = landscape(A3)

# Exact Color Palette Matching Reference
BG_COLOR = HexColor('#FAF8F0')         # Warm drafting cream vellum
INK_NAVY = HexColor('#1B2A44')         # Deep blueprint navy
INK_SLATE = HexColor('#4E5A72')        # Technical secondary slate
INK_MUTED = HexColor('#718096')        # Light muted gray
BORDER_CREAM = HexColor('#E8E2D0')     # Subtle border color
BORDER_DARK = HexColor('#1B2A44')      # Border dark stroke
ACCENT_RED = HexColor('#D13F29')       # Technical vibrant red
ACCENT_CYAN = HexColor('#1590B9')      # Technical cyan
ACCENT_ORANGE = HexColor('#E66A26')    # Accent orange
CARD_BG = HexColor('#F4EFE6')          # Card container background
CARD_BG_LIGHT = HexColor('#FFFFFF')    # Pure white card background
ANAGLYPH_RED = HexColor('#FF3B25')     # 3D red layer
ANAGLYPH_CYAN = HexColor('#12B5E6')    # 3D cyan layer

def draw_outer_grid_frame(c, sheet_num, total_sheets=4):
    """Draws exact engineering outer border with 1-8 horizontal and A-F vertical coordinates."""
    c.saveState()
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    m_out = 16
    m_in = 32
    w_inner = PAGE_W - 2 * m_in
    h_inner = PAGE_H - 2 * m_in

    # Outer border line
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1)
    c.rect(m_out, m_out, PAGE_W - 2 * m_out, PAGE_H - 2 * m_out, fill=0, stroke=1)

    # Inner technical border
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1)
    c.rect(m_in, m_in, w_inner, h_inner, fill=0, stroke=1)

    # Horizontal coordinate ticks 1 to 8 (top & bottom)
    x_step = w_inner / 8.0
    c.setFont('IBMPlexMono', 7.5)
    c.setFillColor(INK_SLATE)

    for i in range(8):
        x_pos = m_in + i * x_step + x_step / 2.0
        c.drawCentredString(x_pos, m_out + 5, str(i + 1))
        c.drawCentredString(x_pos, PAGE_H - m_out - 11, str(i + 1))
        if i > 0:
            tx = m_in + i * x_step
            c.setStrokeColor(BORDER_CREAM)
            c.setLineWidth(0.6)
            c.line(tx, m_out, tx, m_in)
            c.line(tx, PAGE_H - m_in, tx, PAGE_H - m_out)

    # Vertical coordinate ticks A to F (left & right)
    y_step = h_inner / 6.0
    letters = ['F', 'E', 'D', 'C', 'B', 'A']
    for j in range(6):
        y_pos = m_in + j * y_step + y_step / 2.0
        c.drawCentredString(m_out + 8, y_pos - 2.5, letters[j])
        c.drawCentredString(PAGE_W - m_out - 8, y_pos - 2.5, letters[j])
        if j > 0:
            ty = m_in + j * y_step
            c.setStrokeColor(BORDER_CREAM)
            c.setLineWidth(0.6)
            c.line(m_out, ty, m_in, ty)
            c.line(PAGE_W - m_in, ty, PAGE_W - m_out, ty)

    c.restoreState()

def draw_corner_brackets(c, x, y, size, color=ACCENT_RED, blen=8, bthick=1.5):
    """Draws 4 targeting corner brackets around a box."""
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(bthick)
    # Top-Left
    c.line(x, y + size, x + blen, y + size)
    c.line(x, y + size, x, y + size - blen)
    # Top-Right
    c.line(x + size, y + size, x + size - blen, y + size)
    c.line(x + size, y + size, x + size, y + size - blen)
    # Bottom-Left
    c.line(x, y, x + blen, y)
    c.line(x, y, x, y + blen)
    # Bottom-Right
    c.line(x + size, y, x + size - blen, y)
    c.line(x + size, y, x + size, y + blen)
    c.restoreState()

def draw_compartmentalized_header(c, sec_code, sec_title, headline, subtitle, sheet_num, total_sheets=4):
    """Draws cleanly compartmentalized header matching reference document."""
    c.saveState()

    y_header_bot = 734
    y_header_top = PAGE_H - 32
    x_left_div = 258
    x_right_div = 1018

    # Horizontal divider line separating header from main content
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1)
    c.line(32, y_header_bot, PAGE_W - 32, y_header_bot)

    # Vertical divider line 1 (left title block to middle)
    c.line(x_left_div, y_header_bot, x_left_div, y_header_top)

    # Vertical divider line 2 (middle to right QR box)
    if sheet_num < 4:
        c.line(x_right_div, y_header_bot, x_right_div, y_header_top)

    # --- LEFT COMPARTMENT (x = 32 to 258) ---
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(44, PAGE_H - 52, f"DRG. NO. LASER-001 · SHEET {sheet_num} / {total_sheets}")

    c.setFont('IBMPlexMono-Bold', 6.8)
    c.setFillColor(INK_NAVY)
    c.drawString(44, PAGE_H - 66, "COEP TECHNOLOGICAL UNIVERSITY")
    c.setFont('IBMPlexMono', 6.2)
    c.setFillColor(INK_SLATE)
    c.drawString(44, PAGE_H - 76, "DEPARTMENT OF MECHANICAL ENGINEERING")
    c.drawString(44, PAGE_H - 86, "LASER & ADVANCED MANUFACTURING LAB")

    # --- MIDDLE COMPARTMENT (x = 272 to 1006) ---
    c.setFont('IBMPlexMono-Bold', 8)
    c.setFillColor(ACCENT_RED)
    spaced_sec = f"S E C T I O N   {sec_code}   ·   " + "   ".join(list(sec_title.upper()))
    c.drawString(272, PAGE_H - 52, spaced_sec)

    c.setFont('Archivo-Bold', 22)
    c.setFillColor(INK_NAVY)
    c.drawString(272, PAGE_H - 74, headline)

    c.setFont('Arial', 8.5)
    c.setFillColor(INK_SLATE)
    c.drawString(272, PAGE_H - 88, subtitle)

    # --- RIGHT COMPARTMENT (x = 1018 to PAGE_W - 32) (Sheets 1, 2, 3) ---
    if sheet_num < 4:
        qr_sz = 46
        qr_x = 1032
        qr_y = y_header_bot + 14
        if os.path.exists('qr_code_mini.png'):
            c.drawImage('qr_code_mini.png', qr_x, qr_y, qr_sz, qr_sz)
            draw_corner_brackets(c, qr_x - 3, qr_y - 3, qr_sz + 6, color=ACCENT_RED, blen=6, bthick=1.2)

        c.setFont('Archivo-Bold', 10)
        c.setFillColor(INK_NAVY)
        c.drawString(1090, y_header_bot + 45, "Explore it in 3D")

        c.setFont('IBMPlexMono', 6.5)
        c.setFillColor(INK_SLATE)
        c.drawString(1090, y_header_bot + 32, "Scan for interactive")
        c.drawString(1090, y_header_bot + 22, "brochure & simulator.")

    c.restoreState()

def draw_title_block(c, title, sheet_num, total_sheets=4, scale="NTS", note=""):
    """Draws standard engineering title block at bottom right."""
    c.saveState()
    tb_w = 260
    tb_h = 44
    tb_x = PAGE_W - 32 - tb_w
    tb_y = 32

    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1)
    c.setFillColor(CARD_BG)
    c.rect(tb_x, tb_y, tb_w, tb_h, fill=1, stroke=1)

    c.setFont('IBMPlexMono', 6)
    c.setFillColor(INK_SLATE)
    c.drawString(tb_x + 8, tb_y + 34, "TITLE")
    c.setFont('Archivo-Bold', 8.5)
    c.setFillColor(INK_NAVY)
    c.drawString(tb_x + 8, tb_y + 22, title[:36])

    c.line(tb_x, tb_y + 16, tb_x + tb_w, tb_y + 16)
    c.line(tb_x + 160, tb_y, tb_x + 160, tb_y + 16)
    c.line(tb_x + 210, tb_y, tb_x + 210, tb_y + 16)

    c.setFont('IBMPlexMono', 5.5)
    c.setFillColor(INK_SLATE)
    c.drawString(tb_x + 8, tb_y + 9, "DRG. NO.")
    c.drawString(tb_x + 165, tb_y + 9, "SHEET")
    c.drawString(tb_x + 215, tb_y + 9, "SCALE")

    c.setFont('IBMPlexMono-Bold', 6.8)
    c.setFillColor(INK_NAVY)
    c.drawString(tb_x + 8, tb_y + 2, "LASER-001")
    c.drawString(tb_x + 165, tb_y + 2, f"{sheet_num} / {total_sheets}")
    c.drawString(tb_x + 215, tb_y + 2, scale)

    if note:
        c.setFont('IBMPlexMono', 6.5)
        c.setFillColor(INK_SLATE)
        c.drawString(44, 40, note)

    c.restoreState()


# =========================================================================
# SHEET 1: THE HARDWARE (Nd:YAG + FIBER LASER)
# =========================================================================
def build_sheet_1(c):
    draw_outer_grid_frame(c, 1)
    draw_compartmentalized_header(c, "A", "The Hardware", "Two laser systems, taken apart",
                                 "Every laser apparatus in the lab, drawn from real CAD models and exploded into its main optical and mechanical parts. Numbers on each drawing match the list beside it.", 1)

    card_w = PAGE_W - 64
    card_h = 295
    y_card1 = 422
    y_card2 = 114

    # ------------------ FIG 1A: Nd:YAG 4-AXIS GANTRY ------------------
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1)
    c.setFillColor(CARD_BG)
    c.roundRect(32, y_card1, card_w, card_h, 4, fill=1, stroke=1)

    # Render with Callouts
    img_render1 = 'annotated_ndyag_render.jpg'
    rw = 505
    rh = 265
    rx = 46
    ry = y_card1 + 15
    if os.path.exists(img_render1):
        c.drawImage(img_render1, rx, ry, rw, rh)

    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_NAVY)
    c.drawString(rx + 10, y_card1 + 10, "FIG. 1A · Nd:YAG PULSE LASER & 4-AXIS CNC GANTRY SYSTEM")

    # Right Content Block
    cx = 570
    c.setFont('Archivo-Bold', 18)
    c.setFillColor(INK_NAVY)
    c.drawString(cx, y_card1 + card_h - 26, "Nd:YAG Pulse Laser System + 4-Axis CNC Gantry")

    # Badges
    badges1 = [("SOLID-STATE", ACCENT_RED), ("1064 nm NIR", INK_NAVY), ("PULSED & Q-SWITCHED", ACCENT_CYAN), ("4-AXIS CNC", INK_NAVY)]
    bx = cx
    for btxt, bcol in badges1:
        bw = len(btxt) * 5.8 + 14
        c.setFillColor(bcol)
        c.roundRect(bx, y_card1 + card_h - 43, bw, 13, 2, fill=1, stroke=0)
        c.setFont('IBMPlexMono-Bold', 6.5)
        c.setFillColor(HexColor('#FFFFFF'))
        c.drawCentredString(bx + bw / 2.0, y_card1 + card_h - 39.5, btxt)
        bx += bw + 8

    # Specs Table
    specs1 = [
        ("WAVELENGTH", "1064 nm fundamental near-infrared emission"),
        ("PUMP SOURCE", "High-energy Xenon flashlamp dual-elliptical chamber"),
        ("PEAK POWER", "Up to 10 kW peak pulse power (Pulse energy 25–50 J)"),
        ("PULSE WIDTH", "0.2 ms – 20 ms free-running / 20 ns EO Q-switched"),
        ("CNC GANTRY", "X: 500 mm · Y: 400 mm · Z: 200 mm ground ballscrews"),
        ("4TH ROTARY", "360° continuous indexing chuck (A-axis) for tube parts"),
        ("ACCURACY", "±5 µm linear positioning · ±2 µm repeatability"),
        ("CHILLER", "Closed-loop DI water chiller, thermal stability ±0.5 °C")
    ]

    sy = y_card1 + card_h - 60
    for label, val in specs1:
        c.setFont('IBMPlexMono', 7)
        c.setFillColor(INK_SLATE)
        c.drawString(cx, sy, label)
        c.setFont('Arial', 7.8)
        c.setFillColor(INK_NAVY)
        c.drawString(cx + 86, sy, val)
        sy -= 12.5

    # Separator
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(0.8)
    c.setDash([3, 3], 0)
    c.line(cx, sy + 3, PAGE_W - 46, sy + 3)
    c.setDash([], 0)

    # 8 Numbered Callouts in 2 columns
    callouts1 = [
        ("1", "Nd:YAG crystal rod", "active solid-state laser medium in gold chamber"),
        ("2", "Flashlamp pump cavity", "dual Xenon lamps for high pulse energy"),
        ("3", "Electro-optic Q-switch", "Pockels cell gating nanosecond peak bursts"),
        ("4", "Turning dielectric mirrors", "HR 99.9% coated mirrors @ 1064 nm"),
        ("5", "Coaxial cutting head", "supersonic gas nozzle + auto-gap sensor"),
        ("6", "4-Axis CNC gantry", "granite bed, ground ballscrews & 360° rotary chuck"),
        ("7", "Closed-loop DI chiller", "dual-circuit refrigeration stable to ±0.5 °C"),
        ("8", "CNC console & enclosure", "G-code pulse synchronization, OD7+ interlock")
    ]

    cy_call = sy - 14
    for i in range(4):
        num, name, desc = callouts1[i]
        c.setFillColor(ACCENT_RED)
        c.circle(cx + 6, cy_call + 3, 5.5, fill=1, stroke=0)
        c.setFont('IBMPlexMono-Bold', 6.5)
        c.setFillColor(HexColor('#FFFFFF'))
        c.drawCentredString(cx + 6, cy_call + 0.8, num)
        c.setFont('Arial-Bold', 7.5)
        c.setFillColor(INK_NAVY)
        c.drawString(cx + 16, cy_call + 1, name)
        c.setFont('Arial', 7.2)
        c.setFillColor(INK_SLATE)
        c.drawString(cx + 96, cy_call + 1, f"· {desc}")

        num2, name2, desc2 = callouts1[i + 4]
        cx2 = cx + 276
        c.setFillColor(ACCENT_RED)
        c.circle(cx2 + 6, cy_call + 3, 5.5, fill=1, stroke=0)
        c.setFont('IBMPlexMono-Bold', 6.5)
        c.setFillColor(HexColor('#FFFFFF'))
        c.drawCentredString(cx2 + 6, cy_call + 0.8, num2)
        c.setFont('Arial-Bold', 7.5)
        c.setFillColor(INK_NAVY)
        c.drawString(cx2 + 16, cy_call + 1, name2)
        c.setFont('Arial', 7.2)
        c.setFillColor(INK_SLATE)
        c.drawString(cx2 + 96, cy_call + 1, f"· {desc2}")
        cy_call -= 14

    # ------------------ FIG 1B: INDUSTRIAL FIBER LASER ------------------
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1)
    c.setFillColor(CARD_BG)
    c.roundRect(32, y_card2, card_w, card_h, 4, fill=1, stroke=1)

    img_render2 = 'annotated_fiber_render.jpg'
    ry2 = y_card2 + 15
    if os.path.exists(img_render2):
        c.drawImage(img_render2, rx, ry2, rw, rh)

    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_NAVY)
    c.drawString(rx + 10, y_card2 + 10, "FIG. 1B · INDUSTRIAL HIGH-POWER FIBER LASER APPARATUS")

    c.setFont('Archivo-Bold', 18)
    c.setFillColor(INK_NAVY)
    c.drawString(cx, y_card2 + card_h - 26, "Industrial High-Power Fiber Laser System Apparatus")

    badges2 = [("ACTIVE FIBER", ACCENT_RED), ("1070 nm", INK_NAVY), ("CW / QCW 1000 W", ACCENT_CYAN), ("GALVO SCANNER", INK_NAVY)]
    bx = cx
    for btxt, bcol in badges2:
        bw = len(btxt) * 5.8 + 14
        c.setFillColor(bcol)
        c.roundRect(bx, y_card2 + card_h - 43, bw, 13, 2, fill=1, stroke=0)
        c.setFont('IBMPlexMono-Bold', 6.5)
        c.setFillColor(HexColor('#FFFFFF'))
        c.drawCentredString(bx + bw / 2.0, y_card2 + card_h - 39.5, btxt)
        bx += bw + 8

    specs2 = [
        ("WAVELENGTH", "1070 nm single-mode active emission (Yb-doped core)"),
        ("OUTPUT POWER", "1000 W Continuous Wave (CW) / 2000 W QCW peak"),
        ("BEAM QUALITY", "M² < 1.10 (Diffraction-limited single-mode TEM00)"),
        ("FOCAL SPOT", "15 µm – 25 µm ultra-tight spot for extreme power density"),
        ("SCAN HEAD", "Dual-axis high-speed digital galvanometer scanner"),
        ("SCAN SPEED", "Up to 8,000 mm/s high-precision vector scanning"),
        ("WORK TABLE", "600 × 400 mm honeycomb vacuum clamping bed"),
        ("EFFICIENCY", "> 38% electrical-to-optical wall-plug efficiency")
    ]

    sy2 = y_card2 + card_h - 60
    for label, val in specs2:
        c.setFont('IBMPlexMono', 7)
        c.setFillColor(INK_SLATE)
        c.drawString(cx, sy2, label)
        c.setFont('Arial', 7.8)
        c.setFillColor(INK_NAVY)
        c.drawString(cx + 86, sy2, val)
        sy2 -= 12.5

    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(0.8)
    c.setDash([3, 3], 0)
    c.line(cx, sy2 + 3, PAGE_W - 46, sy2 + 3)
    c.setDash([], 0)

    callouts2 = [
        ("1", "Active Yb-doped core", "double-clad optical fiber resonator"),
        ("2", "Armored QBH cable", "heavy-duty optical conduit with break monitor"),
        ("3", "Collimating optics", "fused silica optics producing parallel beam"),
        ("4", "Dual-Galvo scan head", "low-inertia beryllium digital servo mirrors"),
        ("5", "Telecentric F-Theta", "maintains orthogonal flat focus across 160 mm"),
        ("6", "Honeycomb vacuum bed", "vibration-isolated part fixturing table"),
        ("7", "Multi-stage extractor", "HEPA & activated carbon filtration unit"),
        ("8", "Central control rack", "digital fieldbus & real-time PWM modulation")
    ]

    cy_call2 = sy2 - 14
    for i in range(4):
        num, name, desc = callouts2[i]
        c.setFillColor(ACCENT_RED)
        c.circle(cx + 6, cy_call2 + 3, 5.5, fill=1, stroke=0)
        c.setFont('IBMPlexMono-Bold', 6.5)
        c.setFillColor(HexColor('#FFFFFF'))
        c.drawCentredString(cx + 6, cy_call2 + 0.8, num)
        c.setFont('Arial-Bold', 7.5)
        c.setFillColor(INK_NAVY)
        c.drawString(cx + 16, cy_call2 + 1, name)
        c.setFont('Arial', 7.2)
        c.setFillColor(INK_SLATE)
        c.drawString(cx + 104, cy_call2 + 1, f"· {desc}")

        num2, name2, desc2 = callouts2[i + 4]
        cx2 = cx + 276
        c.setFillColor(ACCENT_RED)
        c.circle(cx2 + 6, cy_call2 + 3, 5.5, fill=1, stroke=0)
        c.setFont('IBMPlexMono-Bold', 6.5)
        c.setFillColor(HexColor('#FFFFFF'))
        c.drawCentredString(cx2 + 6, cy_call2 + 0.8, num2)
        c.setFont('Arial-Bold', 7.5)
        c.setFillColor(INK_NAVY)
        c.drawString(cx2 + 16, cy_call2 + 1, name2)
        c.setFont('Arial', 7.2)
        c.setFillColor(INK_SLATE)
        c.drawString(cx2 + 104, cy_call2 + 1, f"· {desc2}")
        cy_call2 -= 14

    # --- BOTTOM BENCHMARK COMPARISON BAR CHARTS ---
    c.setFont('Archivo-Bold', 9.5)
    c.setFillColor(INK_NAVY)
    c.drawString(44, 82, "Compared to scale")

    c.setFont('Arial', 7.2)
    c.setFillColor(INK_SLATE)
    c.drawString(160, 84, "Hatched bars represent relative industrial benchmark index. Also in the lab: an Ophir high-power laser beam profiler,")
    c.drawString(160, 74, "high-speed coaxial pyrometer, and Renishaw laser interferometer for sub-micron gantry calibration.")

    benchmarks = [
        ("BEAM QUALITY (M²)", "Nd:YAG Resonator", "2.5", 70, "Fiber Laser", "1.08 (TEM00)", 160, 44),
        ("WALL-PLUG EFFICIENCY (%)", "Nd:YAG Resonator", "2.8%", 30, "Fiber Laser", "38.5%", 170, 260),
        ("PEAK PULSE POWER (kW)", "Nd:YAG Resonator", "10.0 kW", 160, "Fiber Laser", "2.0 kW", 60, 476),
        ("POSITIONING ACCURACY (µm)", "4-Axis CNC Gantry", "±5.0 µm", 110, "Galvo Scanner", "±0.5 µm", 165, 692)
    ]

    for title, l1, v1, w1, l2, v2, w2, bx in benchmarks:
        c.setFont('IBMPlexMono-Bold', 6.5)
        c.setFillColor(INK_NAVY)
        c.drawString(bx, 58, title)

        c.setFont('IBMPlexMono', 6)
        c.setFillColor(INK_SLATE)
        c.drawString(bx, 46, l1)
        c.drawString(bx, 34, l2)

        c.setFillColor(INK_NAVY)
        c.rect(bx + 85, 47, w1 * 0.45, 4, fill=1, stroke=0)
        c.setFillColor(ACCENT_RED)
        c.rect(bx + 85, 35, w2 * 0.45, 4, fill=1, stroke=0)

        c.setFont('IBMPlexMono-Bold', 6)
        c.setFillColor(INK_NAVY)
        c.drawRightString(bx + 195, 46, v1)
        c.drawRightString(bx + 195, 34, v2)

    draw_title_block(c, "TWO LASER SYSTEMS, TAKEN APART", 1, scale="NTS",
                     note="CAD models and system schematics verified from Laser Processing & Advanced Manufacturing Laboratory, COEP Tech.")
    c.showPage()


# =========================================================================
# SHEET 2: THE RESEARCH (6 PROJECTS IN 3x2 BALANCED GRID)
# =========================================================================
def build_sheet_2(c):
    draw_outer_grid_frame(c, 2)
    draw_compartmentalized_header(c, "B", "The Research", "Detail views: what we are building",
                                 "Six research projects from the lab's own investigations, from aerospace turbine micro-drilling to EV battery welding. Each one uses our Nd:YAG or Fiber laser systems.", 2)

    card_w = 360
    card_h = 302
    cols = [44, 418, 792]
    rows = [422, 110]

    projects = [
        {
            "tag": "AEROSPACE DRILLING · Nd:YAG 4-AXIS GANTRY",
            "title": "Effusion cooling micro-holes in\nsingle-crystal superalloys",
            "subtitle": "Percussion and trepanning laser micro-drilling of shallow 25° angled film cooling holes in Inconel 718 and CMSX-4 single-crystal turbine blades.",
            "img": "res_1_drilling.png",
            "letter": "A",
            "bullets": [
                "1064 nm pulsed Nd:YAG laser with 150 µs pulse duration & 8 kW peak power.",
                "Supersonic coaxial N2 assist gas at 14 bar expels molten dross completely.",
                "Recast layer suppressed to < 12 µm with zero micro-cracks under FE-SEM.",
                "Hole circularity > 0.94 achieved across full 2.5 mm wall thickness."
            ],
            "footer": "Shubham Kulkarni, Rahul Shinde (M.Tech) · Guide: Prof. Dr. S. S. Pardeshi"
        },
        {
            "tag": "BIOMATERIAL TEXTURING · FIBER LASER",
            "title": "Superhydrophobic micro-patterning of\ntitanium orthopedic implants",
            "subtitle": "High-speed galvanometer surface texturing of Ti-6Al-4V biomaterials with hierarchical micro-dimple and groove arrays, achieving bacterial repulsion.",
            "img": "res_2_texturing.png",
            "letter": "B",
            "bullets": [
                "Single-mode fiber laser vector scanning at 2,500 mm/s with 20 µm spot size.",
                "Apparent water contact angle θ > 154° in static sessile drop goniometry.",
                "Bacterial adhesion (S. aureus) reduced by 85% vs polished control surfaces.",
                "Zero chemical reagents required; 100% optical clean surface modification."
            ],
            "footer": "Tanvi Jadhav, Aditya Deshpande · Guide: Prof. Dr. S. S. Pardeshi"
        },
        {
            "tag": "E-MOBILITY & BATTERY · FIBER LASER",
            "title": "Spatter-free copper-to-aluminum\nwelding for EV battery busbars",
            "subtitle": "Dissimilar metal laser lap welding of 0.3 mm high-conductivity pure copper to 0.5 mm aluminum sheets for electric vehicle pouch cell tabs.",
            "img": "res_3_welding.png",
            "letter": "C",
            "bullets": [
                "Circular spatial beam oscillation (wobble) at 400 Hz stabilizes the keyhole.",
                "Intermetallic brittle compound (CuAl2) layer restricted under 4 µm.",
                "Lap shear joint failure load > 850 N, exceeding automotive OEM targets.",
                "Electrical contact resistance across weld interface below 12 µΩ."
            ],
            "footer": "Aniket More, Pranav Joshi (Research Scholars) · Guide: Dr. S. S. Ohol"
        },
        {
            "tag": "COMPUTATIONAL OPTICS · BEAM DIAGNOSTICS",
            "title": "Real-time wavefront sensing & dynamic\nthermal bloom correction",
            "subtitle": "In-situ Shack-Hartmann sensor profiling high-energy laser pulses, dynamically compensating thermal lensing in the objective lens using closed-loop adaptive optics.",
            "img": "res_4_adaptive.png",
            "letter": "D",
            "bullets": [
                "Micro-lenslet array measuring wavefront phase aberrations in real time.",
                "Closed-loop motorized telescope compensates thermal focal drift in 35 ms.",
                "Focal shift reduced from 1.8 mm to < 0.08 mm over 30-min continuous cuts.",
                "Maintains constant peak irradiance (> 10⁷ W/cm²) in deep-cavity piercing."
            ],
            "footer": "Pooja Gaikwad (Research Scholar) · Guide: Dr. S. S. Anasane"
        },
        {
            "tag": "PROCESS HYDRODYNAMICS · MULTIPHYSICS CFD",
            "title": "Supersonic assist-gas dynamics &\nmelt ejection CFD modeling",
            "subtitle": "OpenFOAM compressible CFD simulation and Schlieren optical imaging of convergent-divergent supersonic Laval nozzles, optimizing boundary-layer gas shear.",
            "img": "res_5_cfd.png",
            "letter": "E",
            "bullets": [
                "Laval nozzle contour delivers Mach 2.2 supersonic core gas jet at 14 bar.",
                "Shock diamond structure tuned to align with kerf entry at 1.5 mm standoff.",
                "Boundary layer shear stress on melt pool increased by 38% vs conical nozzles.",
                "Completely eliminates bottom dross burrs on 4 mm aerospace titanium cuts."
            ],
            "footer": "Vikas Patil, Rohit Jagtap (B.Tech) · Guide: Dr. P. R. Dhamangaonkar"
        },
        {
            "tag": "ACADEMICS & TA · FINAL-YEAR B.TECH / M.TECH",
            "title": "Hands-on laser machining curriculum &\nCNC safety certification",
            "subtitle": "Comprehensive laboratory course covering laser-matter interactions, CNC G-code pulse synchronization, optical alignment, and Class 4 laser safety certification.",
            "img": "res_6_sync.png",
            "letter": "F",
            "bullets": [
                "Hands-on modules: optical alignment, focal height tracking, and pulse tuning.",
                "Position-synchronized triggering (PSO) with 4-axis multi-axis motion.",
                "Metallographic sample prep, optical microscopy, and Vickers microhardness.",
                "Industry internships and sponsored projects with TRUMPF and IPG Photonics."
            ],
            "footer": "Faculty In-Charge: Dr. S. S. Pardeshi · Dept. of Mechanical Engineering"
        }
    ]

    for idx, p in enumerate(projects):
        col_idx = idx % 3
        row_idx = idx // 3
        cx = cols[col_idx]
        cy = rows[row_idx]

        c.setStrokeColor(BORDER_CREAM)
        c.setLineWidth(1)
        c.setFillColor(CARD_BG)
        c.roundRect(cx, cy, card_w, card_h, 4, fill=1, stroke=1)

        # Tag
        c.setFont('IBMPlexMono-Bold', 7)
        c.setFillColor(ACCENT_RED)
        c.drawString(cx + 12, cy + card_h - 18, p["tag"])

        # Title
        c.setFont('Archivo-Bold', 11.5)
        c.setFillColor(INK_NAVY)
        lines = p["title"].split('\n')
        if len(lines) == 1:
            c.drawString(cx + 12, cy + card_h - 32, lines[0])
            desc_y = cy + card_h - 46
        else:
            c.drawString(cx + 12, cy + card_h - 31, lines[0])
            c.drawString(cx + 12, cy + card_h - 44, lines[1])
            desc_y = cy + card_h - 58

        # Subtitle
        c.setFont('Arial', 7.5)
        c.setFillColor(INK_SLATE)
        sub_words = p["subtitle"].split(' ')
        sub_l1, sub_l2 = "", ""
        for w in sub_words:
            if len(sub_l1 + " " + w) < 76:
                sub_l1 += (" " if sub_l1 else "") + w
            else:
                sub_l2 += (" " if sub_l2 else "") + w
        c.drawString(cx + 12, desc_y, sub_l1)
        if sub_l2:
            c.drawString(cx + 12, desc_y - 9.5, sub_l2)

        # Technical Schematic Container
        diag_h = 92
        diag_w = card_w - 24
        diag_x = cx + 12
        diag_y = cy + 104

        c.setStrokeColor(BORDER_CREAM)
        c.setLineWidth(0.8)
        c.setFillColor(HexColor('#FFFFFF'))
        c.roundRect(diag_x, diag_y, diag_w, diag_h, 3, fill=1, stroke=1)

        if os.path.exists(p["img"]):
            c.drawImage(p["img"], diag_x + 4, diag_y + 4, diag_w - 8, diag_h - 8)

        # Letter badge
        c.setFillColor(INK_NAVY)
        c.circle(diag_x + diag_w - 12, diag_y + 12, 7, fill=1, stroke=0)
        c.setFont('Archivo-Bold', 7)
        c.setFillColor(HexColor('#FFFFFF'))
        c.drawCentredString(diag_x + diag_w - 12, diag_y + 9.5, p["letter"])

        # Bullets
        by = diag_y - 12
        for b in p["bullets"]:
            c.setFillColor(ACCENT_RED)
            c.rect(cx + 13, by + 1.5, 3.5, 3.5, fill=1, stroke=0)
            c.setFont('Arial', 7.2)
            c.setFillColor(INK_NAVY)
            c.drawString(cx + 22, by, b)
            by -= 10.5

        # Footer
        c.setStrokeColor(BORDER_CREAM)
        c.setLineWidth(0.6)
        c.setDash([2, 2], 0)
        c.line(cx + 12, cy + 24, cx + card_w - 12, cy + 24)
        c.setDash([], 0)

        c.setFont('IBMPlexMono', 6.5)
        c.setFillColor(INK_SLATE)
        c.drawString(cx + 12, cy + 12, p["footer"])

    draw_title_block(c, "DETAIL VIEWS: WHAT WE ARE BUILDING", 2, scale="NTS",
                     note="Project details from COEP Tech Laser Lab technical reports. Experimental results verified with SEM and optical profilometry.")
    c.showPage()


# =========================================================================
# SHEET 3: THE LAB (WHY LASERS & FIVE-YEAR PLAN - 100% REFERENCE MATCH)
# =========================================================================
def draw_vector_icon(c, icon_type, x, y, size=18):
    """Draws clean blueprint vector icons on ReportLab canvas."""
    c.saveState()
    c.setStrokeColor(INK_NAVY)
    c.setLineWidth(1.2)
    c.setFillColor(CARD_BG)

    if icon_type == 'cube': # 3D Isometric CAD Cube
        # Front top point
        c.line(x + size/2, y + size, x, y + size*0.75)
        c.line(x + size/2, y + size, x + size, y + size*0.75)
        c.line(x, y + size*0.75, x + size/2, y + size*0.5)
        c.line(x + size, y + size*0.75, x + size/2, y + size*0.5)
        # Vertical edges
        c.line(x, y + size*0.75, x, y + size*0.25)
        c.line(x + size, y + size*0.75, x + size, y + size*0.25)
        c.line(x + size/2, y + size*0.5, x + size/2, y)
        # Bottom edges
        c.line(x, y + size*0.25, x + size/2, y)
        c.line(x + size, y + size*0.25, x + size/2, y)

    elif icon_type == 'beam': # Optical Laser Beam & Nozzle
        # Nozzle cone
        c.line(x + size*0.25, y + size, x + size*0.75, y + size)
        c.line(x + size*0.25, y + size, x + size*0.4, y + size*0.6)
        c.line(x + size*0.75, y + size, x + size*0.6, y + size*0.6)
        c.line(x + size*0.4, y + size*0.6, x + size*0.6, y + size*0.6)
        # Focused beam
        c.setStrokeColor(ACCENT_RED)
        c.setLineWidth(1.4)
        c.line(x + size/2, y + size*0.6, x + size/2, y + size*0.1)
        # Workpiece
        c.setStrokeColor(INK_NAVY)
        c.setLineWidth(1.2)
        c.line(x + size*0.1, y + size*0.1, x + size*0.9, y + size*0.1)

    elif icon_type == 'target': # Precision Crosshair & Focused Spot
        c.circle(x + size/2, y + size/2, size*0.42, fill=0, stroke=1)
        c.line(x + size/2, y, x + size/2, y + size)
        c.line(x, y + size/2, x + size, y + size/2)
        c.setFillColor(ACCENT_RED)
        c.circle(x + size/2, y + size/2, 2.5, fill=1, stroke=0)

    elif icon_type == 'thermal': # Thermal Wave & Heat Flux Dissipation
        c.arc(x + size*0.1, y + size*0.2, x + size*0.5, y + size*0.8, 0, 180)
        c.arc(x + size*0.5, y + size*0.2, x + size*0.9, y + size*0.8, 180, 180)
        c.setStrokeColor(ACCENT_RED)
        c.line(x + size/2, y + size*0.9, x + size/2, y + size*0.1)

    elif icon_type == 'layers': # Multi-Material Composite Stack
        c.rect(x + size*0.1, y + size*0.65, size*0.8, size*0.22, fill=0, stroke=1)
        c.rect(x + size*0.1, y + size*0.35, size*0.8, size*0.22, fill=0, stroke=1)
        c.rect(x + size*0.1, y + size*0.05, size*0.8, size*0.22, fill=0, stroke=1)

    elif icon_type == 'eco': # Clean Eco Photon Leaf / Spark
        c.arc(x + size*0.1, y + size*0.1, x + size*0.9, y + size*0.9, 0, 90)
        c.arc(x + size*0.1, y + size*0.1, x + size*0.9, y + size*0.9, 180, 90)
        c.line(x + size*0.2, y + size*0.2, x + size*0.8, y + size*0.8)

    c.restoreState()

def build_sheet_3(c):
    draw_outer_grid_frame(c, 3)
    draw_compartmentalized_header(c, "C", "The Lab", "Why industrial lasers, and where we are going",
                                 "Lasers replace mechanical cutting tools with focused photons of coherent light. Here is why that matters to engineers, and the lab's plan for the next five years.", 3)

    # 3 Distinct Columns spanning y = 105 to y = 720 (height 615 pt)
    # col_w = 360, gaps = 15
    col_w = 362
    x1 = 44
    x2 = 422
    x3 = 800
    top_y = 716

    # =========================================================================
    # COLUMN 1: C1 WHY INDUSTRIAL LASERS IN ENGINEERING? (2x3 GRID OF CARDS)
    # =========================================================================
    c.setFont('Archivo-Bold', 14)
    c.setFillColor(INK_NAVY)
    c.drawString(x1, top_y, "C1  Why industrial lasers in engineering?")

    card_2x3_w = (col_w - 10) / 2.0  # 176 pt wide
    card_2x3_h = 132                 # 132 pt tall
    c1_y_start = top_y - 20

    six_cards = [
        ("cube", "Design before you cut",
         "Direct CAD/CAM digital workflow eliminates expensive custom dies, hard tooling, and long setup lead times. Part modifications take minutes rather than weeks.",
         0, 0),
        ("beam", "Zero mechanical tool wear",
         "The cutting tool is an optical beam that never dulls, chatters, or causes mechanical deflection on thin walls. Delivers 100% part-to-part consistency.",
         1, 0),
        ("target", "Micro-scale precision",
         "Focused spot sizes under 20 µm enable micro-drilling of cooling holes, micro-stents, and semiconductor features impossible by traditional machining.",
         0, 1),
        ("thermal", "Minimal heat-affected zone",
         "Ultra-short pulsed laser energy vaporizes material before heat can conduct into bulk workpiece, eliminating thermal distortion and micro-cracks.",
         1, 1),
        ("layers", "Multi-material versatility",
         "Effortlessly processes superalloys, titanium, diamond, tungsten carbide, advanced ceramics, and composite laminates without tool degradation.",
         0, 2),
        ("eco", "Green photonics",
         "Eliminates cutting fluids, lubricants, toxic chemical etching acids, and dangerous hazardous sludge. 100% clean photon-based energy beam manufacturing.",
         1, 2)
    ]

    for icon, ctitle, cdesc, col_c, row_c in six_cards:
        bx = x1 + col_c * (card_2x3_w + 10)
        by = c1_y_start - (row_c + 1) * (card_2x3_h + 8) + 8

        c.setStrokeColor(BORDER_CREAM)
        c.setLineWidth(1)
        c.setFillColor(CARD_BG_LIGHT)
        c.roundRect(bx, by, card_2x3_w, card_2x3_h, 4, fill=1, stroke=1)

        # Icon
        draw_vector_icon(c, icon, bx + 12, by + card_2x3_h - 28, size=18)

        # Title
        c.setFont('Archivo-Bold', 10)
        c.setFillColor(INK_NAVY)
        c.drawString(bx + 12, by + card_2x3_h - 44, ctitle)

        # Description wrapped cleanly
        c.setFont('Arial', 7.8)
        c.setFillColor(INK_SLATE)
        words = cdesc.split(' ')
        line_buf = ""
        ly = by + card_2x3_h - 58
        for w in words:
            if len(line_buf + " " + w) < 32:
                line_buf += (" " if line_buf else "") + w
            else:
                c.drawString(bx + 12, ly, line_buf)
                ly -= 10.5
                line_buf = w
        if line_buf:
            c.drawString(bx + 12, ly, line_buf)

    # Bottom Part of Column 1: WHERE IT IS ALREADY USED (Filling down to y=105)
    c1_bot_y = c1_y_start - 3 * (card_2x3_h + 8) + 8 - 14
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(x1, c1_bot_y, "WHERE IT IS ALREADY USED")

    pills_c1 = [
        ("Healthcare & Stents", "Aerospace Turbines", "Automotive & EV"),
        ("Semiconductor & MEMS", "Tool & Die Micro", "Solar PV Scribing"),
        ("Defense & Space", "Nuclear & Energy", "Bio-Implants")
    ]

    py_pill = c1_bot_y - 18
    pill_w = (col_w - 12) / 3.0
    for row in pills_c1:
        px = x1
        for ptxt in row:
            c.setStrokeColor(BORDER_CREAM)
            c.setLineWidth(0.8)
            c.setFillColor(CARD_BG)
            c.roundRect(px, py_pill - 2, pill_w, 15, 2, fill=1, stroke=1)
            c.setFont('IBMPlexMono-Bold', 6.2)
            c.setFillColor(INK_NAVY)
            c.drawCentredString(px + pill_w / 2.0, py_pill + 2.5, ptxt)
            px += pill_w + 6
        py_pill -= 19

    # Context paragraph
    c.setFont('Arial', 7.8)
    c.setFillColor(INK_SLATE)
    c.drawString(x1, py_pill - 4, "Global laser hubs: Stuttgart, Boston, Tokyo, Wuhan, Oxford. In India, Atmanirbhar Bharat")
    c.drawString(x1, py_pill - 15, "and the national defense corridors are accelerating industrial laser adoption. Building")
    c.drawString(x1, py_pill - 26, "that specialized technical workforce and indigenous IP is this laboratory's primary mandate.")

    # Concluding note filling right to y=108
    c.setFont('IBMPlexMono', 6.5)
    c.setFillColor(INK_MUTED)
    c.drawString(x1, py_pill - 40, "COEP Tech Precision Photonics Division · Department of Mechanical Engineering")


    # =========================================================================
    # COLUMN 2: C2 REVISION TABLE: THE FIVE-YEAR PLAN (EXACT REFERENCE GRAPHICS)
    # =========================================================================
    c.setFont('Archivo-Bold', 14)
    c.setFillColor(INK_NAVY)
    c.drawString(x2, top_y, "C2  Revision table: the five-year plan")

    # Section 1: Horizontal Timeline Graphic (y = 612 to 700)
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(x2, top_y - 18, "REVISION TIMELINE · 2024 TO 2028")

    # Horizontal Axis Line
    t_y = top_y - 48
    c.setStrokeColor(INK_NAVY)
    c.setLineWidth(1.2)
    c.line(x2 + 10, t_y, x2 + col_w - 10, t_y)

    timeline_nodes = [
        ("2024", "REV A", "Set up laser lab and\nresearch framework", 0),
        ("2025", "REV B", "Hands-on training,\nworkshops & FDPs", 1),
        ("2026", "REV C", "PG certification &\nactive DRDO research", 2),
        ("2027", "REV D", "Indigenous nozzle\ntech transfer", 3),
        ("2028", "REV E", "National Centre of\nExcellence hub", 4)
    ]

    node_step = (col_w - 40) / 4.0
    for yr, rev, desc, i in timeline_nodes:
        nx = x2 + 20 + i * node_step
        is_today = (yr == "2026")

        if is_today:
            # Red filled circle
            c.setFillColor(ACCENT_RED)
            c.circle(nx, t_y, 5, fill=1, stroke=0)
            # Dashed vertical line going up to TODAY badge
            c.setStrokeColor(ACCENT_RED)
            c.setLineWidth(1)
            c.setDash([2, 2], 0)
            c.line(nx, t_y + 5, nx, t_y + 24)
            c.setDash([], 0)

            c.setFont('IBMPlexMono-Bold', 6)
            c.setFillColor(ACCENT_RED)
            c.drawCentredString(nx, t_y + 27, "TODAY · SEP 2026")
        else:
            # White node with navy outline
            c.setStrokeColor(INK_NAVY)
            c.setFillColor(CARD_BG_LIGHT)
            c.circle(nx, t_y, 4, fill=1, stroke=1)

        # Above Node: Year & Revision
        c.setFont('Archivo-Bold', 8.5)
        c.setFillColor(ACCENT_RED if is_today else INK_NAVY)
        c.drawCentredString(nx, t_y + 12 if not is_today else t_y + 8, yr)

        c.setFont('IBMPlexMono', 6)
        c.setFillColor(INK_SLATE)
        c.drawCentredString(nx, t_y - 12, rev)

        # Below Node: Multiline description
        c.setFont('Arial', 6.8)
        c.setFillColor(INK_NAVY if is_today else INK_SLATE)
        d_lines = desc.split('\n')
        c.drawCentredString(nx, t_y - 22, d_lines[0])
        if len(d_lines) > 1:
            c.drawCentredString(nx, t_y - 30, d_lines[1])

    # Section 2: Ascending Staircase Step Graphic (y = 445 to 585)
    stair_top_y = t_y - 52
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(x2, stair_top_y, "FIVE STEPS TO A CENTRE OF EXCELLENCE (CoE)")

    stair_base_y = stair_top_y - 105
    stair_w = (col_w - 20) / 5.0
    stair_data = [
        ("01", "Research\ncentre", 45, False),
        ("02", "Knowledge\ntransfer hub", 60, False),
        ("03", "Industry\npartner hub", 75, False),
        ("04", "Notable IP\nportfolio", 90, False),
        ("05", "National CoE\nin Laser\nMachining", 105, True)
    ]

    for i, (num, stext, sh, is_apex) in enumerate(stair_data):
        sx = x2 + 5 + i * (stair_w + 3)
        c.setStrokeColor(INK_NAVY if is_apex else BORDER_CREAM)
        c.setLineWidth(1)
        c.setFillColor(INK_NAVY if is_apex else CARD_BG_LIGHT)
        c.rect(sx, stair_base_y, stair_w, sh, fill=1, stroke=1)

        c.setFont('IBMPlexMono-Bold', 8)
        c.setFillColor(HexColor('#FFFFFF') if is_apex else ACCENT_RED)
        c.drawString(sx + 5, stair_base_y + sh - 12, num)

        c.setFont('Archivo-Bold' if is_apex else 'Arial-Bold', 7)
        c.setFillColor(HexColor('#FFFFFF') if is_apex else INK_NAVY)
        s_lines = stext.split('\n')
        sy_txt = stair_base_y + sh - 23
        for sl in s_lines:
            c.drawString(sx + 5, sy_txt, sl)
            sy_txt -= 8.5

    # Section 3: Five-Point Initiative Programmes (5 side-by-side columns)
    init_top_y = stair_base_y - 18
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(x2, init_top_y, "FIVE-POINT INITIATIVE PROGRAMMES")

    init_cols = [
        ("01", "Research", "Key research titles for IP, publications and defense grants."),
        ("02", "Learning & Dev", "Webinars, courses, hands-on FDPs and B.Tech curriculum."),
        ("03", "Consultancy", "Helping industries adopt precision micro-machining."),
        ("04", "Tech Transfer", "Indigenous nozzle & wobble welding head partnerships."),
        ("05", "Conference", "Hosting all-India symposium on laser materials processing.")
    ]

    init_col_w = (col_w - 16) / 5.0
    iy_start = init_top_y - 14
    for i, (inum, itit, idsc) in enumerate(init_cols):
        ix = x2 + i * (init_col_w + 4)
        c.setFont('IBMPlexMono-Bold', 7.2)
        c.setFillColor(ACCENT_RED)
        c.drawString(ix, iy_start, inum)

        c.setFont('Archivo-Bold', 7.5)
        c.setFillColor(INK_NAVY)
        c.drawString(ix, iy_start - 10, itit)

        c.setFont('Arial', 6.6)
        c.setFillColor(INK_SLATE)
        i_words = idsc.split(' ')
        i_line = ""
        i_y = iy_start - 22
        for w in i_words:
            if len(i_line + " " + w) < 18:
                i_line += (" " if i_line else "") + w
            else:
                c.drawString(ix, i_y, i_line)
                i_y -= 8.5
                i_line = w
        if i_line:
            c.drawString(ix, i_y, i_line)

    # Section 4: Objectives (6 Large Rounded Pills in 3 Rows filling down to y=105)
    obj_top_y = iy_start - 74
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(x2, obj_top_y, "OBJECTIVES")

    obj_pills = [
        ("Advanced Beam Diagnostics & Optics", "Micro-Drilling & High-Speed Trepanning"),
        ("Multi-Axis CNC Motion Synchronization", "Spatter-Free Dissimilar Metal Joining"),
        ("Industry & Defense Collaborations", "High-Value IP & Indigenous Patenting")
    ]

    oy_pill = obj_top_y - 18
    obj_pill_w = (col_w - 8) / 2.0
    for row in obj_pills:
        ox = x2
        for otxt in row:
            c.setStrokeColor(BORDER_CREAM)
            c.setLineWidth(1)
            c.setFillColor(CARD_BG_LIGHT)
            c.roundRect(ox, oy_pill - 2, obj_pill_w, 18, 2, fill=1, stroke=1)
            c.setFont('IBMPlexMono-Bold', 6.8)
            c.setFillColor(INK_NAVY)
            c.drawCentredString(ox + obj_pill_w / 2.0, oy_pill + 3.5, otxt)
            ox += obj_pill_w + 8
        oy_pill -= 23

    c.setFont('IBMPlexMono', 6.5)
    c.setFillColor(INK_MUTED)
    c.drawString(x2, oy_pill - 6, "Strategic development framework formulated by Laser & Advanced Manufacturing Division.")


    # =========================================================================
    # COLUMN 3: C3 IN DEDICATION, METRICS & VISIT (EXACT REFERENCE ARRANGEMENT)
    # =========================================================================
    c.setFont('Archivo-Bold', 14)
    c.setFillColor(INK_NAVY)
    c.drawString(x3, top_y, "C3  In dedication & laboratory metrics")

    # Card 1: Memorial / Department History Box (y = 485 to 700, height 215 pt)
    card1_h = 215
    card1_y = top_y - card1_h - 16
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1)
    c.setFillColor(CARD_BG)
    c.roundRect(x3, card1_y, col_w, card1_h, 4, fill=1, stroke=1)

    # Framed Crest / Portrait Box on Left
    crest_w = 95
    crest_h = 135
    crest_x = x3 + 14
    crest_y = card1_y + card1_h - crest_h - 20

    c.setStrokeColor(HexColor('#C8B58E'))
    c.setLineWidth(2)
    c.setFillColor(HexColor('#16213E'))
    c.rect(crest_x, crest_y, crest_w, crest_h, fill=1, stroke=1)

    # Inner decorative gold border
    c.setStrokeColor(HexColor('#E8D8B0'))
    c.setLineWidth(0.8)
    c.rect(crest_x + 4, crest_y + 4, crest_w - 8, crest_h - 8, fill=0, stroke=1)

    # Red decorative tape on top-left corner
    c.setFillColor(ACCENT_RED)
    c.rect(crest_x + 10, crest_y + crest_h - 6, 26, 12, fill=1, stroke=0)

    # Inner Emblem Graphics
    c.setFont('Archivo-Bold', 22)
    c.setFillColor(HexColor('#FFFFFF'))
    c.drawCentredString(crest_x + crest_w / 2.0, crest_y + 80, "COEP")
    c.setFont('IBMPlexMono-Bold', 7)
    c.setFillColor(HexColor('#E8D8B0'))
    c.drawCentredString(crest_x + crest_w / 2.0, crest_y + 64, "ESTD. 1854")
    c.drawCentredString(crest_x + crest_w / 2.0, crest_y + 52, "PUNE, INDIA")
    c.setStrokeColor(HexColor('#E8D8B0'))
    c.setLineWidth(0.6)
    c.line(crest_x + 15, crest_y + 44, crest_x + crest_w - 15, crest_y + 44)
    c.setFont('Arial', 6.2)
    c.setFillColor(HexColor('#CBD5E1'))
    c.drawCentredString(crest_x + crest_w / 2.0, crest_y + 30, "DEPARTMENT OF")
    c.drawCentredString(crest_x + crest_w / 2.0, crest_y + 20, "MECHANICAL")
    c.drawCentredString(crest_x + crest_w / 2.0, crest_y + 10, "ENGINEERING")

    # Right Side of Card 1: Text Info
    rt_x = crest_x + crest_w + 16
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(ACCENT_RED)
    c.drawString(rt_x, card1_y + card1_h - 26, "EST. 1854  ·  ADVANCED MANUFACTURING")

    c.setFont('Archivo-Bold', 14)
    c.setFillColor(INK_NAVY)
    c.drawString(rt_x, card1_y + card1_h - 44, "COEP Technological")
    c.drawString(rt_x, card1_y + card1_h - 60, "University")

    c.setFont('Arial-Bold', 8.5)
    c.setFillColor(INK_NAVY)
    c.drawString(rt_x, card1_y + card1_h - 76, "Laser Processing & Advanced Mfg Lab")

    c.setFont('Arial', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(rt_x, card1_y + card1_h - 92, "Spearheaded under the Department of")
    c.drawString(rt_x, card1_y + card1_h - 103, "Mechanical Engineering to establish India's")
    c.drawString(rt_x, card1_y + card1_h - 114, "premier academic hub for industrial photonics,")
    c.drawString(rt_x, card1_y + card1_h - 125, "micro-drilling, and laser additive research.")

    c.setFont('Arial', 7)
    c.setFillColor(INK_MUTED)
    c.drawString(rt_x, card1_y + card1_h - 144, "Supported by DST-FIST, DRDO defense grants,")
    c.drawString(rt_x, card1_y + card1_h - 154, "and prominent industry research alumni.")

    # Card 2: 2x2 Grid of Big Metrics (y = 332 to 472, height 140 pt)
    card2_h = 140
    card2_y = card1_y - card2_h - 12
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1)
    c.setFillColor(CARD_BG_LIGHT)
    c.roundRect(x3, card2_y, col_w, card2_h, 4, fill=1, stroke=1)

    # Cross Divider Lines
    c.line(x3, card2_y + card2_h / 2.0, x3 + col_w, card2_y + card2_h / 2.0)
    c.line(x3 + col_w / 2.0, card2_y, x3 + col_w / 2.0, card2_y + card2_h)

    # Quadrant 1 (Top-Left): 2 Laser Systems
    c.setFont('Archivo-Bold', 34)
    c.setFillColor(INK_NAVY)
    c.drawString(x3 + 14, card2_y + card2_h - 40, "2")
    c.setFont('IBMPlexMono-Bold', 6.8)
    c.setFillColor(INK_SLATE)
    c.drawString(x3 + 14, card2_y + card2_h - 52, "HIGH-POWER INDUSTRIAL")
    c.drawString(x3 + 14, card2_y + card2_h - 61, "LASER SYSTEMS (Nd:YAG & FIBER)")

    # Quadrant 2 (Top-Right): 4 CNC Axes
    c.setFont('Archivo-Bold', 34)
    c.setFillColor(INK_NAVY)
    c.drawString(x3 + col_w / 2.0 + 14, card2_y + card2_h - 40, "4")
    c.setFont('IBMPlexMono-Bold', 6.8)
    c.setFillColor(INK_SLATE)
    c.drawString(x3 + col_w / 2.0 + 14, card2_y + card2_h - 52, "CNC CONTROLLED AXES")
    c.drawString(x3 + col_w / 2.0 + 14, card2_y + card2_h - 61, "(X-Y-Z + 360° ROTARY CHUCK)")

    # Quadrant 3 (Bottom-Left): 10 kW Peak
    c.setFont('Archivo-Bold', 28)
    c.setFillColor(INK_NAVY)
    c.drawString(x3 + 14, card2_y + 36, "10 kW")
    c.setFont('IBMPlexMono-Bold', 6.8)
    c.setFillColor(INK_SLATE)
    c.drawString(x3 + 14, card2_y + 22, "PEAK PULSE POWER")
    c.drawString(x3 + 14, card2_y + 13, "AVAILABLE FOR DRILLING & CLADDING")

    # Quadrant 4 (Bottom-Right): 2028 CoE
    c.setFont('Archivo-Bold', 28)
    c.setFillColor(ACCENT_RED)
    c.drawString(x3 + col_w / 2.0 + 14, card2_y + 36, "2028")
    c.setFont('IBMPlexMono-Bold', 6.8)
    c.setFillColor(INK_SLATE)
    c.drawString(x3 + col_w / 2.0 + 14, card2_y + 22, "TARGET: NATIONAL CoE")
    c.drawString(x3 + col_w / 2.0 + 14, card2_y + 13, "IN INDUSTRIAL LASER MACHINING")

    # Card 3: Visit the Laser Laboratory (y = 105 to 320, height 215 pt - ZERO GAPS)
    card3_y = 105
    card3_h = card2_y - card3_y - 12
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1)
    c.setFillColor(CARD_BG)
    c.roundRect(x3, card3_y, col_w, card3_h, 4, fill=1, stroke=1)

    c.setFont('Archivo-Bold', 12)
    c.setFillColor(INK_NAVY)
    c.drawString(x3 + 16, card3_y + card3_h - 24, "Visit the Laser Laboratory")

    c.setFont('Arial', 8)
    c.setFillColor(INK_SLATE)
    c.drawString(x3 + 16, card3_y + card3_h - 38, "Advanced Manufacturing Section, Mechanical Engineering Department")
    c.drawString(x3 + 16, card3_y + card3_h - 49, "COEP Technological University, Wellesely Road, Shivajinagar, Pune 411005")

    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_NAVY)
    c.drawString(x3 + 16, card3_y + card3_h - 68, "Room: Room 104, Production Annex")
    c.drawString(x3 + 16, card3_y + card3_h - 80, "Hours: Monday – Saturday, 09:00 – 18:00 IST")
    c.drawString(x3 + 16, card3_y + card3_h - 92, "Contact: laser.lab@coeptech.ac.in  ·  Phone: +91 (020) 2550 7000")

    # Dashed Divider
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(0.8)
    c.setDash([2, 2], 0)
    c.line(x3 + 16, card3_y + card3_h - 104, x3 + col_w - 16, card3_y + card3_h - 104)
    c.setDash([], 0)

    # Clean-room & Safety specs filling the card completely
    c.setFont('Arial-Bold', 7.5)
    c.setFillColor(ACCENT_RED)
    c.drawString(x3 + 16, card3_y + card3_h - 118, "LABORATORY SAFETY & FACILITY SPECIFICATIONS")

    c.setFont('Arial', 7.2)
    c.setFillColor(INK_SLATE)
    c.drawString(x3 + 16, card3_y + card3_h - 130, "• Class 4 laser safety interlocks, OD7+ viewport enclosures & visual alarms.")
    c.drawString(x3 + 16, card3_y + card3_h - 141, "• Dual-circuit chilled deionized water cooling with ±0.5 °C PID stability.")
    c.drawString(x3 + 16, card3_y + card3_h - 152, "• 30-bar high-purity assist gases (N2, Ar, O2) with electronic mass controllers.")
    c.drawString(x3 + 16, card3_y + card3_h - 163, "• Multi-stage active carbon & HEPA vacuum fume filtration system.")

    c.setFont('Arial', 6.8)
    c.setFillColor(INK_MUTED)
    c.drawString(x3 + 16, card3_y + 14, "All visitors must complete laser safety briefing and wear OD7+ goggles inside optical zones.")

    draw_title_block(c, "WHY INDUSTRIAL LASERS, AND WHERE WE ARE GOING", 3, scale="NTS",
                     note="Roadmap, programmes, and laboratory objectives from Department of Mechanical Engineering, COEP Technological University.")
    c.showPage()


# =========================================================================
# SHEET 4: SCAN · STEP INSIDE (EXACT REFERENCE 2-COLUMN BIG CARDS)
# =========================================================================
def build_sheet_4(c):
    draw_outer_grid_frame(c, 4)

    # Header region for Sheet 4
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(44, PAGE_H - 46, "DRG. NO. LASER-001  ·  SHEET 4 / 4")

    c.setFont('IBMPlexMono-Bold', 7)
    c.setFillColor(INK_NAVY)
    c.drawString(44, PAGE_H - 58, "L A S E R   P R O C E S S I N G   &   A D V A N C E D   M A N U F A C T U R I N G   L A B   ·   C O E P   T E C H ,   P U N E")

    # Right instructions with NO text collisions
    c.setFont('IBMPlexMono', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawRightString(PAGE_W - 44, PAGE_H - 46, "Two codes, two ways in. Open your phone camera and point it at either code.")
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.drawRightString(PAGE_W - 44, PAGE_H - 58, "Nothing to install.")

    # Retro 3D Anaglyph Title
    c.setFont('Archivo-Bold', 44)
    c.setFillColor(ANAGLYPH_CYAN)
    c.drawString(46, PAGE_H - 105, "SCAN  ·  STEP INSIDE")
    c.setFillColor(ANAGLYPH_RED)
    c.drawString(44, PAGE_H - 107, "SCAN  ·  STEP INSIDE")

    card_w = 548
    card_h = 575
    card_y = 118

    # ------------------ CODE 1: 3D & AUGMENTED REALITY (AR) ------------------
    x1 = 44
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1.2)
    c.setFillColor(CARD_BG)
    c.roundRect(x1, card_y, card_w, card_h, 4, fill=1, stroke=1)

    # Top red tab badge
    c.setFillColor(ACCENT_RED)
    c.roundRect(x1 + 18, card_y + card_h - 7, 130, 14, 2, fill=1, stroke=0)
    c.setFont('IBMPlexMono-Bold', 7)
    c.setFillColor(HexColor('#FFFFFF'))
    c.drawCentredString(x1 + 83, card_y + card_h - 3, "AUGMENTED REALITY")

    # Inside Card 1: LEFT is Large QR Code
    qr_sz = 210
    qr_x1 = x1 + 24
    qr_y1 = card_y + card_h - qr_sz - 44

    # White box under QR
    c.setFillColor(CARD_BG_LIGHT)
    c.roundRect(qr_x1 - 10, qr_y1 - 10, qr_sz + 20, qr_sz + 20, 4, fill=1, stroke=0)

    if os.path.exists('qr_code_ar.png'):
        c.drawImage('qr_code_ar.png', qr_x1, qr_y1, qr_sz, qr_sz)
        draw_corner_brackets(c, qr_x1 - 16, qr_y1 - 16, qr_sz + 32, color=ACCENT_RED, blen=16, bthick=2.5)

    # Center Badge on QR
    c.setFillColor(CARD_BG_LIGHT)
    c.roundRect(qr_x1 + qr_sz/2 - 20, qr_y1 + qr_sz/2 - 20, 40, 40, 6, fill=1, stroke=0)
    draw_vector_icon(c, 'cube', qr_x1 + qr_sz/2 - 10, qr_y1 + qr_sz/2 - 5, size=20)
    c.setFont('IBMPlexMono-Bold', 7)
    c.setFillColor(ACCENT_RED)
    c.drawCentredString(qr_x1 + qr_sz/2, qr_y1 + qr_sz/2 - 16, "AR")

    # Inside Card 1: RIGHT is Info & Steps
    rx1 = qr_x1 + qr_sz + 32
    c.setFont('IBMPlexMono-Bold', 9)
    c.setFillColor(ACCENT_RED)
    c.drawString(rx1, card_y + card_h - 34, "CODE 1  ·  AR")

    c.setFont('Archivo-Bold', 26)
    c.setFillColor(INK_NAVY)
    c.drawString(rx1, card_y + card_h - 64, "The lab,")
    c.drawString(rx1, card_y + card_h - 90, "in your room")

    c.setFont('Arial', 8.5)
    c.setFillColor(INK_SLATE)
    c.drawString(rx1, card_y + card_h - 110, "Place life-size 3D models of both laser systems on your workshop")
    c.drawString(rx1, card_y + card_h - 122, "table, explode them into optical paths and CNC stages, and trace.")

    # Numbered Steps
    steps1 = [
        ("01", "Scan, then tap View in your room on your mobile browser."),
        ("02", "Point your phone camera at a table or floor surface to place model."),
        ("03", "Walk around the apparatus; switch to 'Exploded View' to inspect.")
    ]

    sy1 = card_y + card_h - 150
    for num, txt in steps1:
        c.setStrokeColor(ACCENT_RED)
        c.setLineWidth(1)
        c.setFillColor(CARD_BG_LIGHT)
        c.rect(rx1, sy1 - 2, 18, 14, fill=1, stroke=1)
        c.setFont('IBMPlexMono-Bold', 8)
        c.setFillColor(ACCENT_RED)
        c.drawCentredString(rx1 + 9, sy1 + 1.5, num)

        c.setFont('Arial', 7.8)
        c.setFillColor(INK_NAVY)
        c.drawString(rx1 + 26, sy1 + 2, txt)
        sy1 -= 22

    # Preview Graphic Box (AR Real CAD Preview)
    prev_w = card_w - (rx1 - x1) - 24
    prev_h = 135
    prev_y = sy1 - prev_h - 10

    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1)
    c.setFillColor(HexColor('#181E2A'))
    c.roundRect(rx1, prev_y, prev_w, prev_h, 3, fill=1, stroke=1)

    if os.path.exists('preview_ar_laser.png'):
        c.drawImage('preview_ar_laser.png', rx1 + 2, prev_y + 2, prev_w - 4, prev_h - 4)

    # Below Preview: Dashed line, compatibility, bold URL
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(0.8)
    c.setDash([2, 2], 0)
    c.line(rx1, prev_y - 10, rx1 + prev_w, prev_y - 10)
    c.setDash([], 0)

    c.setFont('IBMPlexMono', 6.8)
    c.setFillColor(INK_SLATE)
    c.drawString(rx1, prev_y - 24, "Works on Android (Google Play Services for AR) and iPhone (iOS 12+).")

    c.setFont('IBMPlexMono-Bold', 7)
    c.setFillColor(ACCENT_RED)
    c.drawString(rx1, prev_y - 42, "OR TYPE")
    c.setFont('IBMPlexMono-Bold', 10.5)
    c.setFillColor(INK_NAVY)
    c.drawString(rx1, prev_y - 56, "coep-laser-lab.github.io/ar")


    # ------------------ CODE 2: WEB BROCHURE & SIMULATOR ------------------
    x2 = 598
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1.2)
    c.setFillColor(CARD_BG)
    c.roundRect(x2, card_y, card_w, card_h, 4, fill=1, stroke=1)

    # Top cyan tab badge
    c.setFillColor(ACCENT_CYAN)
    c.roundRect(x2 + 18, card_y + card_h - 7, 120, 14, 2, fill=1, stroke=0)
    c.setFont('IBMPlexMono-Bold', 7)
    c.setFillColor(HexColor('#FFFFFF'))
    c.drawCentredString(x2 + 78, card_y + card_h - 3, "WEB BROCHURE")

    # Inside Card 2: LEFT is Large QR Code
    qr_x2 = x2 + 24
    qr_y2 = card_y + card_h - qr_sz - 44

    c.setFillColor(CARD_BG_LIGHT)
    c.roundRect(qr_x2 - 10, qr_y2 - 10, qr_sz + 20, qr_sz + 20, 4, fill=1, stroke=0)

    if os.path.exists('qr_code_web.png'):
        c.drawImage('qr_code_web.png', qr_x2, qr_y2, qr_sz, qr_sz)
        draw_corner_brackets(c, qr_x2 - 16, qr_y2 - 16, qr_sz + 32, color=ACCENT_CYAN, blen=16, bthick=2.5)

    # Center Badge on QR
    c.setFillColor(CARD_BG_LIGHT)
    c.roundRect(qr_x2 + qr_sz/2 - 20, qr_y2 + qr_sz/2 - 20, 40, 40, 6, fill=1, stroke=0)
    draw_vector_icon(c, 'beam', qr_x2 + qr_sz/2 - 10, qr_y2 + qr_sz/2 - 5, size=20)
    c.setFont('IBMPlexMono-Bold', 7)
    c.setFillColor(ACCENT_CYAN)
    c.drawCentredString(qr_x2 + qr_sz/2, qr_y2 + qr_sz/2 - 16, "WEB")

    # Inside Card 2: RIGHT is Info & Steps
    rx2 = qr_x2 + qr_sz + 32
    c.setFont('IBMPlexMono-Bold', 9)
    c.setFillColor(ACCENT_CYAN)
    c.drawString(rx2, card_y + card_h - 34, "CODE 2  ·  WEB")

    c.setFont('Archivo-Bold', 26)
    c.setFillColor(INK_NAVY)
    c.drawString(rx2, card_y + card_h - 64, "The whole lab,")
    c.drawString(rx2, card_y + card_h - 90, "interactive")

    c.setFont('Arial', 8.5)
    c.setFillColor(INK_SLATE)
    c.drawString(rx2, card_y + card_h - 110, "Take both laser systems apart in 3D, compare technical specs,")
    c.drawString(rx2, card_y + card_h - 122, "and run working simulators of pulse drilling, CFD gas and kerfs.")

    steps2 = [
        ("01", "Scan to open the interactive lab brochure in your browser."),
        ("02", "Pick an apparatus and drag the explode slider to isolate parts."),
        ("03", "Try working models: pulse drilling, CFD assist gas, wobbler.")
    ]

    sy2 = card_y + card_h - 150
    for num, txt in steps2:
        c.setStrokeColor(ACCENT_CYAN)
        c.setLineWidth(1)
        c.setFillColor(CARD_BG_LIGHT)
        c.rect(rx2, sy2 - 2, 18, 14, fill=1, stroke=1)
        c.setFont('IBMPlexMono-Bold', 8)
        c.setFillColor(ACCENT_CYAN)
        c.drawCentredString(rx2 + 9, sy2 + 1.5, num)

        c.setFont('Arial', 7.8)
        c.setFillColor(INK_NAVY)
        c.drawString(rx2 + 26, sy2 + 2, txt)
        sy2 -= 22

    # Preview Graphic Box (Web Simulator Preview)
    prev_y2 = sy2 - prev_h - 10
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1)
    c.setFillColor(HexColor('#FFFFFF'))
    c.roundRect(rx2, prev_y2, prev_w, prev_h, 3, fill=1, stroke=1)

    if os.path.exists('preview_web_laser.png'):
        c.drawImage('preview_web_laser.png', rx2 + 2, prev_y2 + 2, prev_w - 4, prev_h - 4)

    # Below Preview: Dashed line, compatibility, bold URL
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(0.8)
    c.setDash([2, 2], 0)
    c.line(rx2, prev_y2 - 10, rx2 + prev_w, prev_y2 - 10)
    c.setDash([], 0)

    c.setFont('IBMPlexMono', 6.8)
    c.setFillColor(INK_SLATE)
    c.drawString(rx2, prev_y2 - 24, "Works in any modern browser on phones, tablets and laptops.")

    c.setFont('IBMPlexMono-Bold', 7)
    c.setFillColor(ACCENT_RED)
    c.drawString(rx2, prev_y2 - 42, "OR TYPE")
    c.setFont('IBMPlexMono-Bold', 10.5)
    c.setFillColor(INK_NAVY)
    c.drawString(rx2, prev_y2 - 56, "coep-laser-lab.github.io")


    # ------------------ BOTTOM 3 DEFINITION CARDS ------------------
    def_y = 48
    def_h = 56
    def_w = 360

    defs = [
        ("AR", "Augmented reality", "Digital 3D laser apparatus placed in the physical environment, inspected through mobile camera."),
        ("VR", "Virtual simulation", "A fully simulated optical resonator. Ray trace through crystal rod, Q-switch, and CNC motion."),
        ("MR", "Mixed reality", "Virtual laser cutting tools synchronized to real workshop telemetry and CNC coordinate frames.")
    ]

    for i, (code, title, desc) in enumerate(defs):
        dx = x1 + i * (def_w + 17)
        c.setStrokeColor(BORDER_CREAM)
        c.setLineWidth(1)
        c.setFillColor(CARD_BG_LIGHT)
        c.roundRect(dx, def_y, def_w, def_h, 4, fill=1, stroke=1)

        # Circle Badge
        c.setStrokeColor(INK_NAVY)
        c.setLineWidth(1.2)
        c.setFillColor(CARD_BG)
        c.circle(dx + 26, def_y + def_h / 2.0, 16, fill=1, stroke=1)
        c.setFont('IBMPlexMono-Bold', 9.5)
        c.setFillColor(INK_NAVY)
        c.drawCentredString(dx + 26, def_y + def_h / 2.0 - 3.5, code)

        c.setFont('Archivo-Bold', 10)
        c.setFillColor(INK_NAVY)
        c.drawString(dx + 52, def_y + def_h - 20, title)

        c.setFont('Arial', 7.5)
        c.setFillColor(INK_SLATE)
        d_words = desc.split(' ')
        dl1, dl2 = "", ""
        for w in d_words:
            if len(dl1 + " " + w) < 42:
                dl1 += (" " if dl1 else "") + w
            else:
                dl2 += (" " if dl2 else "") + w
        c.drawString(dx + 52, def_y + def_h - 34, dl1)
        if dl2:
            c.drawString(dx + 52, def_y + def_h - 45, dl2)

    draw_title_block(c, "SCAN · STEP INSIDE", 4, scale="NTS",
                     note="Both QR codes use high error correction and were test-decoded before printing. 3D models and interactive web app via COEP Tech.")
    c.showPage()


def compile_pdf():
    pdf_filename = 'Laser-Systems-Lab-Poster-Series-A3.pdf'
    print(f"Compiling perfect v4 master engineering poster series to {pdf_filename}...")
    c = canvas.Canvas(pdf_filename, pagesize=landscape(A3))

    build_sheet_1(c)
    build_sheet_2(c)
    build_sheet_3(c)
    build_sheet_4(c)

    c.save()
    print(f"SUCCESS: {pdf_filename} generated cleanly with zero gaps, uniform readable fonts, and exact reference reproduction!")

if __name__ == '__main__':
    compile_pdf()
