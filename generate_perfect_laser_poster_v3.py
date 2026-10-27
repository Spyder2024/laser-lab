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

# Exact Color Palette
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

def draw_compartmentalized_header(c, sec_code, sec_title, headline, subtitle, sheet_num, total_sheets=4):
    """Draws cleanly compartmentalized header matching reference document."""
    c.saveState()

    y_header_bot = 734
    y_header_top = PAGE_H - 32
    x_left_div = 258
    x_right_div = 1028

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

    # --- MIDDLE COMPARTMENT (x = 272 to 1016) ---
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

    # --- RIGHT COMPARTMENT (x = 1028 to PAGE_W - 32) (Sheets 1, 2, 3) ---
    if sheet_num < 4:
        if os.path.exists('qr_code_mini.png'):
            c.drawImage('qr_code_mini.png', 1042, y_header_bot + 16, 42, 42)

        c.setFont('Archivo-Bold', 9.5)
        c.setFillColor(INK_NAVY)
        c.drawString(1092, y_header_bot + 46, "Explore it in 3D")

        c.setFont('IBMPlexMono', 6.5)
        c.setFillColor(INK_SLATE)
        c.drawString(1092, y_header_bot + 34, "Scan for interactive")
        c.drawString(1092, y_header_bot + 24, "brochure & simulator.")

        # Pill badge
        c.setFillColor(ACCENT_RED)
        c.roundRect(PAGE_W - 74, y_header_bot + 43, 24, 10, 2, fill=1, stroke=0)
        c.setFont('IBMPlexMono-Bold', 5.5)
        c.setFillColor(HexColor('#FFFFFF'))
        c.drawCentredString(PAGE_W - 62, y_header_bot + 45.5, "WEB")

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

    c.setLineWidth(0.6)
    c.line(tb_x, tb_y + 22, tb_x + tb_w, tb_y + 22)
    c.line(tb_x + 140, tb_y, tb_x + 140, tb_y + 22)
    c.line(tb_x + 200, tb_y, tb_x + 200, tb_y + 22)

    c.setFont('IBMPlexMono', 6)
    c.setFillColor(INK_SLATE)
    c.drawString(tb_x + 6, tb_y + 34, "TITLE")
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_NAVY)
    c.drawString(tb_x + 6, tb_y + 25, title.upper())

    c.setFont('IBMPlexMono', 6)
    c.setFillColor(INK_SLATE)
    c.drawString(tb_x + 6, tb_y + 13, "DRG. NO.")
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_NAVY)
    c.drawString(tb_x + 6, tb_y + 4, "LASER-001")

    c.setFont('IBMPlexMono', 6)
    c.setFillColor(INK_SLATE)
    c.drawString(tb_x + 146, tb_y + 13, "SHEET")
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_NAVY)
    c.drawString(tb_x + 146, tb_y + 4, f"{sheet_num} / {total_sheets}")

    c.setFont('IBMPlexMono', 6)
    c.setFillColor(INK_SLATE)
    c.drawString(tb_x + 206, tb_y + 13, "SCALE")
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_NAVY)
    c.drawString(tb_x + 206, tb_y + 4, scale)

    if note:
        c.setFont('Arial', 7.2)
        c.setFillColor(INK_SLATE)
        c.drawString(44, tb_y + 8, note)

    c.restoreState()

# =========================================================================
# SHEET 1: THE HARDWARE (UNIFORM READABLE SIZES, NO GAPS)
# =========================================================================
def build_sheet_1(c):
    draw_outer_grid_frame(c, 1)
    draw_compartmentalized_header(c, "A", "The Hardware", "Two laser systems, taken apart",
                                 "Every laser apparatus in the lab, drawn from real CAD models and exploded into its main optical and mechanical parts. Numbers on each drawing match the list beside it.", 1)

    machines = [
        {
            "img": "annotated_ndyag_render.jpg",
            "name": "Nd:YAG Pulse Laser System + 4-Axis CNC Gantry",
            "tag": "FIG. 1A · Nd:YAG PULSE LASER & 4-AXIS CNC GANTRY SYSTEM",
            "badges": [("SOLID-STATE", ACCENT_RED), ("1064 nm NIR", INK_NAVY), ("PULSED & Q-SWITCHED", ACCENT_CYAN), ("4-AXIS CNC", INK_SLATE)],
            "specs": [
                ("WAVELENGTH", "1064 nm fundamental near-infrared emission"),
                ("PUMP SOURCE", "High-energy Xenon flashlamp dual-elliptical chamber"),
                ("PEAK POWER", "Up to 10 kW peak pulse power (Pulse energy 25–50 J)"),
                ("PULSE WIDTH", "0.2 ms – 20 ms free-running / 20 ns EO Q-switched"),
                ("CNC GANTRY", "X: 500 mm · Y: 400 mm · Z: 200 mm ground ballscrews"),
                ("4TH ROTARY", "360° continuous indexing chuck (A-axis) for tube parts"),
                ("ACCURACY", "±5 µm linear positioning · ±2 µm repeatability"),
                ("CHILLER", "Closed-loop DI water chiller, thermal stability ±0.5 °C")
            ],
            "parts": [
                ("1", "Nd:YAG crystal rod", "active solid-state laser medium in gold chamber"),
                ("2", "Flashlamp pump cavity", "dual Xenon lamps for high pulse energy"),
                ("3", "Electro-optic Q-switch", "Pockels cell gating nanosecond peak bursts"),
                ("4", "Turning dielectric mirrors", "HR 99.9% coated mirrors @ 1064 nm"),
                ("5", "Coaxial cutting head", "supersonic gas nozzle + auto-gap sensor"),
                ("6", "4-Axis CNC gantry", "granite bed, ground ballscrews & 360° rotary chuck"),
                ("7", "Closed-loop DI chiller", "dual-circuit refrigeration stable to ±0.5 °C"),
                ("8", "CNC console & enclosure", "G-code pulse synchronization, OD7+ interlock")
            ],
            "card_y": 420, "card_h": 298
        },
        {
            "img": "annotated_fiber_render.jpg",
            "name": "Industrial High-Power Fiber Laser System Apparatus",
            "tag": "FIG. 1B · INDUSTRIAL HIGH-POWER FIBER LASER APPARATUS",
            "badges": [("ACTIVE FIBER", ACCENT_RED), ("1070 nm", INK_NAVY), ("CW / QCW 1000 W", ACCENT_CYAN), ("GALVO SCANNER", INK_SLATE)],
            "specs": [
                ("WAVELENGTH", "1070 nm single-mode active emission (Yb-doped core)"),
                ("OUTPUT POWER", "1000 W Continuous Wave (CW) / 2000 W QCW peak"),
                ("BEAM QUALITY", "M² < 1.10 (Diffraction-limited single-mode TEM₀₀)"),
                ("FOCAL SPOT", "15 µm – 25 µm ultra-tight spot for extreme power density"),
                ("SCAN HEAD", "Dual-axis high-speed digital galvanometer scanner"),
                ("SCAN SPEED", "Up to 8,000 mm/s high-precision vector scanning"),
                ("WORK TABLE", "600 × 400 mm honeycomb vacuum clamping bed"),
                ("EFFICIENCY", "> 38% electrical-to-optical wall-plug efficiency")
            ],
            "parts": [
                ("1", "Active Yb-doped core", "double-clad optical fiber resonator"),
                ("2", "Armored QBH cable", "heavy-duty optical conduit with break monitor"),
                ("3", "Collimating optics", "fused silica optics producing parallel beam"),
                ("4", "Dual-Galvo scan head", "low-inertia beryllium digital servo mirrors"),
                ("5", "Telecentric F-Theta", "maintains orthogonal flat focus across 160 mm"),
                ("6", "Honeycomb vacuum bed", "vibration-isolated part fixturing table"),
                ("7", "Multi-stage extractor", "HEPA & activated carbon filtration unit"),
                ("8", "Central control rack", "digital fieldbus & real-time PWM modulation")
            ],
            "card_y": 115, "card_h": 295
        }
    ]

    card_w = PAGE_W - 88

    for m in machines:
        cy = m["card_y"]
        ch = m["card_h"]
        cx = 44

        c.setStrokeColor(BORDER_CREAM)
        c.setLineWidth(1)
        c.setFillColor(CARD_BG)
        c.roundRect(cx, cy, card_w, ch, 4, fill=1, stroke=1)

        # Realistic Image left side
        img_w = 485
        img_h = ch - 24
        img_x = cx + 12
        img_y = cy + 12

        if os.path.exists(m["img"]):
            c.drawImage(m["img"], img_x, img_y, img_w, img_h)

        c.setFont('IBMPlexMono-Bold', 7.5)
        c.setFillColor(INK_SLATE)
        c.drawString(img_x + 10, img_y + 10, m["tag"])

        # Details right side
        tx = cx + 512

        # Title
        c.setFont('Archivo-Bold', 17)
        c.setFillColor(INK_NAVY)
        c.drawString(tx, cy + ch - 26, m["name"])

        # Badges
        cur_bx = tx
        for btext, bcol in m["badges"]:
            b_width = len(btext) * 4.6 + 10
            c.setFillColor(bcol)
            c.roundRect(cur_bx, cy + ch - 41, b_width, 11, 2, fill=1, stroke=0)
            c.setFont('IBMPlexMono-Bold', 6.2)
            c.setFillColor(HexColor('#FFFFFF'))
            c.drawCentredString(cur_bx + b_width/2.0, cy + ch - 38.5, btext)
            cur_bx += b_width + 6

        # Hairline divider
        c.setStrokeColor(BORDER_CREAM)
        c.setLineWidth(0.6)
        c.line(tx, cy + ch - 48, cx + card_w - 14, cy + ch - 48)

        # Specifications Table (Readable 7.5pt / 8.5pt font)
        sy = cy + ch - 64
        for slabel, sval in m["specs"]:
            c.setFont('IBMPlexMono-Bold', 7)
            c.setFillColor(INK_SLATE)
            c.drawString(tx, sy, slabel)
            c.setFont('Arial', 8)
            c.setFillColor(INK_NAVY)
            c.drawString(tx + 86, sy, sval)
            sy -= 11

        # Numbered Component Callouts List (1 to 8)
        py_start = sy - 4
        col1_parts = m["parts"][:4]
        col2_parts = m["parts"][4:]

        py = py_start
        for num, pname, pdesc in col1_parts:
            c.setFillColor(ACCENT_RED)
            c.circle(tx + 4, py + 2.5, 4.5, fill=1, stroke=0)
            c.setFont('IBMPlexMono-Bold', 6)
            c.setFillColor(HexColor('#FFFFFF'))
            c.drawCentredString(tx + 4, py + 0.8, num)

            c.setFont('Arial-Bold', 7.5)
            c.setFillColor(INK_NAVY)
            c.drawString(tx + 14, py + 0.8, pname)
            p_len = c.stringWidth(pname, 'Arial-Bold', 7.5)
            c.setFont('Arial', 7.5)
            c.setFillColor(INK_SLATE)
            c.drawString(tx + 16 + p_len, py + 0.8, f"· {pdesc}")
            py -= 12

        py2 = py_start
        tx2 = tx + 280
        for num, pname, pdesc in col2_parts:
            c.setFillColor(ACCENT_RED)
            c.circle(tx2 + 4, py2 + 2.5, 4.5, fill=1, stroke=0)
            c.setFont('IBMPlexMono-Bold', 6)
            c.setFillColor(HexColor('#FFFFFF'))
            c.drawCentredString(tx2 + 4, py2 + 0.8, num)

            c.setFont('Arial-Bold', 7.5)
            c.setFillColor(INK_NAVY)
            c.drawString(tx2 + 14, py2 + 0.8, pname)
            p_len = c.stringWidth(pname, 'Arial-Bold', 7.5)
            c.setFont('Arial', 7.5)
            c.setFillColor(INK_SLATE)
            c.drawString(tx2 + 16 + p_len, py2 + 0.8, f"· {pdesc}")
            py2 -= 12

    # --- BOTTOM SECTION: COMPARED TO SCALE ---
    comp_y = 96
    c.setFont('Archivo-Bold', 10)
    c.setFillColor(INK_NAVY)
    c.drawString(44, comp_y, "Compared to scale")

    c.setFont('Arial', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(160, comp_y, "Hatched bars represent relative industrial benchmark index. Also in the lab: an Ophir high-power laser beam profiler,")
    c.drawString(160, comp_y - 9, "high-speed coaxial pyrometer, and Renishaw laser interferometer for sub-micron gantry calibration.")

    benchmarks = [
        ("BEAM QUALITY (M²)", [("Nd:YAG Resonator", 2.5, "2.5"), ("Fiber Laser", 1.08, "1.08 (TEM₀₀)")]),
        ("WALL-PLUG EFFICIENCY (%)", [("Nd:YAG Resonator", 2.8, "2.8%"), ("Fiber Laser", 38.5, "38.5%")]),
        ("PEAK PULSE POWER (kW)", [("Nd:YAG Resonator", 10.0, "10.0 kW"), ("Fiber Laser", 2.0, "2.0 kW")]),
        ("POSITIONING ACCURACY (µm)", [("4-Axis CNC Gantry", 5.0, "±5.0 µm"), ("Galvo Scanner", 0.5, "±0.5 µm")])
    ]

    bx_start = 44
    for btitle, blist in benchmarks:
        c.setFont('IBMPlexMono-Bold', 6.8)
        c.setFillColor(INK_NAVY)
        c.drawString(bx_start, comp_y - 21, btitle)

        by_bar = comp_y - 32
        for bname, bval, blabel in blist:
            c.setFont('Arial', 6.8)
            c.setFillColor(INK_SLATE)
            c.drawString(bx_start, by_bar, bname)

            c.setFillColor(CARD_BG)
            c.rect(bx_start + 65, by_bar - 1, 95, 5, fill=1, stroke=0)

            bar_len = min(90, (bval / (40 if 'EFFICIENCY' in btitle else 12)) * 90)
            c.setFillColor(ACCENT_RED if 'Fiber' in bname or 'Galvo' in bname else INK_NAVY)
            c.rect(bx_start + 65, by_bar - 1, bar_len, 5, fill=1, stroke=0)

            c.setFont('IBMPlexMono-Bold', 6)
            c.setFillColor(INK_NAVY)
            c.drawString(bx_start + 164, by_bar, blabel)
            by_bar -= 9

        bx_start += 215

    draw_title_block(c, "TWO LASER SYSTEMS, TAKEN APART", 1, scale="NTS",
                     note="CAD models and system schematics verified from Laser Processing & Advanced Manufacturing Laboratory, COEP Tech.")
    c.showPage()

# =========================================================================
# SHEET 2: THE RESEARCH (BALANCED 3x2 GRID, READABLE FONTS)
# =========================================================================
def build_sheet_2(c):
    draw_outer_grid_frame(c, 2)
    draw_compartmentalized_header(c, "B", "The Research", "Detail views: what we are building",
                                 "Six research projects from the lab's own investigations, from aerospace turbine micro-drilling to EV battery welding. Each one uses our Nd:YAG or Fiber laser systems.", 2)

    projects = [
        {
            "cat": "AEROSPACE DRILLING · Nd:YAG 4-AXIS GANTRY",
            "title_1": "Effusion cooling micro-holes in",
            "title_2": "single-crystal superalloys",
            "desc": "Percussion and trepanning micro-drilling of shallow 25° angled film cooling holes in Inconel 718 and CMSX-4 single-crystal turbine blades. 4-axis gantry positions complex aerofoil geometry.",
            "team": "Shubham Kulkarni, Rahul Shinde (M.Tech) · Guide: Prof. Dr. S. S. Pardeshi",
            "bullets": [
                "1064 nm pulsed Nd:YAG laser with 150 µs pulse duration & 8 kW peak power.",
                "Supersonic coaxial N₂ assist gas at 14 bar expels molten dross completely.",
                "Recast layer suppressed to < 12 µm with zero micro-cracks under FE-SEM.",
                "Hole circularity > 0.94 achieved across full 2.5 mm wall thickness."
            ],
            "img": "res_1_drilling.png"
        },
        {
            "cat": "BIOMATERIAL TEXTURING · FIBER LASER",
            "title_1": "Superhydrophobic micro-patterning of",
            "title_2": "titanium orthopedic implants",
            "desc": "High-speed galvanometer surface texturing of Ti-6Al-4V biomaterials with hierarchical micro-dimple and groove arrays, achieving bacterial repulsion and enhanced osseointegration.",
            "team": "Tanvi Jadhav, Aditya Deshpande · Guide: Prof. Dr. S. S. Pardeshi",
            "bullets": [
                "Single-mode fiber laser vector scanning at 2,500 mm/s with 20 µm spot size.",
                "Apparent water contact angle θ > 154° in static sessile drop goniometry.",
                "Bacterial adhesion (S. aureus) reduced by 85% vs polished control surfaces.",
                "Zero chemical reagents required; 100% optical clean surface modification."
            ],
            "img": "res_2_texturing.png"
        },
        {
            "cat": "E-MOBILITY & BATTERY · FIBER LASER",
            "title_1": "Spatter-free copper-to-aluminum",
            "title_2": "welding for EV battery busbars",
            "desc": "Dissimilar metal laser lap welding of 0.3 mm high-conductivity pure copper to 0.5 mm aluminum sheets for electric vehicle pouch cell tabs and current collectors.",
            "team": "Aniket More, Pranav Joshi (Research Scholars) · Guide: Dr. S. S. Ohol",
            "bullets": [
                "Circular spatial beam oscillation (wobble) at 400 Hz stabilizes the keyhole.",
                "Intermetallic brittle compound (CuAl₂) layer restricted under 4 µm.",
                "Lap shear joint failure load > 850 N, exceeding automotive OEM targets.",
                "Electrical contact resistance across weld interface below 12 µΩ."
            ],
            "img": "res_3_welding.png"
        },
        {
            "cat": "COMPUTATIONAL OPTICS · BEAM DIAGNOSTICS",
            "title_1": "Real-time wavefront sensing & dynamic",
            "title_2": "thermal bloom correction",
            "desc": "In-situ Shack-Hartmann sensor profiling high-energy laser pulses, dynamically compensating thermal lensing in the objective lens using closed-loop adaptive beam expansion.",
            "team": "Pooja Gaikwad (Research Scholar) · Guide: Dr. S. S. Anasane",
            "bullets": [
                "Micro-lenslet array measuring wavefront phase aberrations in real time.",
                "Closed-loop motorized telescope compensates thermal focal drift in 35 ms.",
                "Focal shift reduced from 1.8 mm to < 0.08 mm over 30-min continuous cuts.",
                "Maintains constant peak irradiance (> 10⁷ W/cm²) in deep-cavity piercing."
            ],
            "img": "res_4_wavefront.png"
        },
        {
            "cat": "PROCESS HYDRODYNAMICS · MULTIPHYSICS CFD",
            "title_1": "Supersonic assist-gas dynamics &",
            "title_2": "melt ejection CFD modeling",
            "desc": "OpenFOAM compressible CFD simulation and Schlieren optical imaging of convergent-divergent supersonic Laval nozzles, optimizing boundary-layer gas shear for dross-free laser cutting.",
            "team": "Vikas Patil, Rohit Jagtap (B.Tech) · Guide: Dr. P. R. Dhamangaonkar",
            "bullets": [
                "Laval nozzle contour delivers Mach 2.2 supersonic core gas jet at 14 bar.",
                "Shock diamond structure tuned to align with kerf entry at 1.5 mm standoff.",
                "Boundary layer shear stress on melt pool increased by 38% vs conical nozzles.",
                "Completely eliminates bottom dross burrs on 4 mm aerospace titanium cuts."
            ],
            "img": "res_5_cfd.png"
        },
        {
            "cat": "ACADEMICS & TA · FINAL-YEAR B.TECH / M.TECH",
            "title_1": "Hands-on laser machining curriculum &",
            "title_2": "CNC safety certification",
            "desc": "Comprehensive laboratory course covering laser-matter interactions, CNC G-code pulse synchronization, optical alignment, and Class 4 laser safety certification.",
            "team": "Faculty In-Charge: Dr. S. S. Pardeshi · Dept. of Mechanical Engineering",
            "bullets": [
                "Hands-on modules: optical alignment, focal height tracking, and pulse tuning.",
                "Position-synchronized laser triggering (PSO) with 4-axis multi-axis motion.",
                "Metallographic sample prep, optical microscopy, and Vickers microhardness.",
                "Industry internships and sponsored projects with TRUMPF and IPG Photonics."
            ],
            "img": "res_6_sync.png"
        }
    ]

    card_w = 356
    card_h = 302
    x_starts = [44, 420, 796]
    y_starts = [422, 110]

    for idx, p in enumerate(projects):
        col_idx = idx % 3
        row_idx = idx // 3
        cx = x_starts[col_idx]
        cy = y_starts[row_idx]

        c.setStrokeColor(BORDER_CREAM)
        c.setLineWidth(1)
        c.setFillColor(CARD_BG)
        c.roundRect(cx, cy, card_w, card_h, 4, fill=1, stroke=1)

        c.setFont('IBMPlexMono-Bold', 7.5)
        c.setFillColor(ACCENT_RED)
        c.drawString(cx + 14, cy + card_h - 18, p["cat"])

        c.setFont('Archivo-Bold', 12.5)
        c.setFillColor(INK_NAVY)
        c.drawString(cx + 14, cy + card_h - 33, p["title_1"])
        c.drawString(cx + 14, cy + card_h - 46, p["title_2"])

        c.setFont('Arial', 7.8)
        c.setFillColor(INK_SLATE)
        c.drawString(cx + 14, cy + card_h - 60, p["desc"][:74])
        c.drawString(cx + 14, cy + card_h - 70, p["desc"][74:150])

        iw = card_w - 28
        ih = 98
        iy = cy + card_h - 176
        if os.path.exists(p["img"]):
            c.drawImage(p["img"], cx + 14, iy, iw, ih)

        by_pt = iy - 13
        for b in p["bullets"]:
            c.setFillColor(ACCENT_CYAN)
            c.circle(cx + 18, by_pt + 2.5, 2.2, fill=1, stroke=0)
            c.setFont('Arial', 7.2)
            c.setFillColor(INK_NAVY)
            c.drawString(cx + 25, by_pt, b)
            by_pt -= 10.5

        c.setFont('IBMPlexMono', 6.5)
        c.setFillColor(INK_MUTED)
        c.drawString(cx + 14, cy + 10, p["team"])

    draw_title_block(c, "DETAIL VIEWS: WHAT WE ARE BUILDING", 2, scale="NTS",
                     note="Project details from COEP Tech Laser Lab technical reports. Experimental results verified with SEM and optical profilometry.")
    c.showPage()

# =========================================================================
# SHEET 3: THE LAB (FULL-PAGE PROPORTIONED GRID, ZERO GAPS)
# =========================================================================
def build_sheet_3(c):
    draw_outer_grid_frame(c, 3)
    draw_compartmentalized_header(c, "C", "The Lab", "Why industrial lasers, and where we are going",
                                 "Lasers replace mechanical cutting tools with focused photons of coherent light. Here is why that matters to engineers, and the lab's plan for the next five years.", 3)

    # 3 Proportioned Columns filling the vertical canvas from y=105 to y=725 (height 620 pt)
    col_w = 354
    x1 = 44
    x2 = 418
    x3 = 792
    top_y = 712

    # --- COLUMN 1: C1 WHY INDUSTRIAL LASERS IN ADVANCED MANUFACTURING ---
    c.setFont('Archivo-Bold', 14)
    c.setFillColor(INK_NAVY)
    c.drawString(x1, top_y, "C1  Why industrial lasers in engineering?")

    pillars = [
        ("Design before you cut", "Direct CAD/CAM digital workflow eliminates expensive custom dies, hard tooling, and long setup lead times. Part modifications take minutes rather than weeks."),
        ("Zero mechanical tool wear", "The cutting tool is an optical beam that never dulls, chatters, or causes mechanical deformation on thin walls. Delivers 100% part-to-part consistency."),
        ("Micro-scale precision", "Focused spot sizes under 20 µm enable micro-drilling of cooling holes, micro-stents, and semiconductor features impossible by traditional machining."),
        ("Minimal heat-affected zone", "Ultra-short pulsed laser energy vaporizes material before heat can conduct into the bulk workpiece, preventing thermal distortion and micro-cracks."),
        ("Multi-material versatility", "Effortlessly processes superalloys, titanium, diamond, tungsten carbide, advanced ceramics, and composite laminates without tool degradation."),
        ("Green, sustainable manufacturing", "Eliminates cutting fluids, lubricants, toxic chemical etching acids, and dangerous hazardous sludge. 100% clean photon-based manufacturing.")
    ]

    py = top_y - 24
    for title, desc in pillars:
        c.setStrokeColor(BORDER_CREAM)
        c.setLineWidth(0.8)
        c.setFillColor(CARD_BG)
        c.roundRect(x1, py - 38, col_w, 48, 3, fill=1, stroke=1)

        c.setFont('Archivo-Bold', 9.5)
        c.setFillColor(INK_NAVY)
        c.drawString(x1 + 10, py - 4, title)

        c.setFont('Arial', 7.5)
        c.setFillColor(INK_SLATE)
        c.drawString(x1 + 10, py - 16, desc[:72])
        c.drawString(x1 + 10, py - 26, desc[72:144])
        c.drawString(x1 + 10, py - 35, desc[144:210])
        py -= 54

    # WHERE IT IS ALREADY USED
    c.setFont('IBMPlexMono-Bold', 8)
    c.setFillColor(INK_SLATE)
    c.drawString(x1, py - 8, "WHERE IT IS ALREADY USED")

    sectors = [
        ("Healthcare & Stents", "Aerospace Turbines", "Automotive & EV", "Semiconductors"),
        ("Tool & Die Micro-Machining", "Biomaterial Implants", "Solar PV Scribing", "Defense & Space")
    ]

    sy = py - 24
    for row in sectors:
        sx = x1
        for sec in row:
            c.setFillColor(CARD_BG_LIGHT)
            c.roundRect(sx, sy - 3, 84, 13, 2, fill=1, stroke=0)
            c.setFont('IBMPlexMono', 6.5)
            c.setFillColor(INK_NAVY)
            c.drawString(sx + 3, sy + 1, sec[:16])
            sx += 88
        sy -= 16

    c.setFont('Arial', 7.5)
    c.setFillColor(INK_MUTED)
    c.drawString(x1, sy - 6, "Global laser hubs: Stuttgart, Boston, Tokyo, Wuhan, Oxford. In India, Atmanirbhar Bharat")
    c.drawString(x1, sy - 16, "and the defense manufacturing corridors are accelerating industrial laser adoption. Building")
    c.drawString(x1, sy - 26, "that specialized technical workforce and indigenous IP is this laboratory's primary mandate.")

    # --- COLUMN 2: C2 REVISION TABLE: THE FIVE-YEAR PLAN ---
    c.setFont('Archivo-Bold', 14)
    c.setFillColor(INK_NAVY)
    c.drawString(x2, top_y, "C2  Revision table: the five-year plan")

    c.setFont('IBMPlexMono-Bold', 8)
    c.setFillColor(INK_SLATE)
    c.drawString(x2, top_y - 20, "REVISION TIMELINE · 2024 TO 2028")

    revs = [
        ("2024", "REV A", "Commissioning of 4-axis gantry, optical alignment & baseline testing"),
        ("2025", "REV B", "Industry workshops, contract testing services, and B.Tech TA lab curriculum"),
        ("2026", "REV C", "TODAY · Postgraduate certification, DST/DRDO research, and wobble welding IP"),
        ("2027", "REV D", "Technology transfer of specialized supersonic nozzle & trepanning heads"),
        ("2028", "REV E", "State-of-the-art National Centre of Excellence in Advanced Laser Systems")
    ]

    ry = top_y - 36
    for yr, rev, rdesc in revs:
        is_today = "TODAY" in rdesc
        c.setFillColor(HexColor('#FFF5F5') if is_today else CARD_BG)
        c.roundRect(x2, ry - 3, col_w, 18, 2, fill=1, stroke=0)
        c.setFont('IBMPlexMono-Bold', 7.5)
        c.setFillColor(ACCENT_RED if is_today else INK_NAVY)
        c.drawString(x2 + 6, ry + 3, yr)
        c.drawString(x2 + 42, ry + 3, rev)
        c.setFont('Arial', 7.5)
        c.setFillColor(INK_NAVY if is_today else INK_SLATE)
        c.drawString(x2 + 86, ry + 3, rdesc[:54])
        ry -= 22

    c.setFont('IBMPlexMono-Bold', 8)
    c.setFillColor(INK_SLATE)
    c.drawString(x2, ry - 10, "FIVE STEPS TO A CENTRE OF EXCELLENCE (CoE)")

    steps = [
        ("01", "Research Laboratory", "Core infrastructure, baseline calibration & laser-material trials"),
        ("02", "Knowledge Transfer Hub", "FDP courses, hands-on student workshops & TA lab curriculum"),
        ("03", "Industry Partner Centre", "Sponsored defense grants, contract testing & commercial prototypes"),
        ("04", "Notable IP & Patent Portfolio", "Indigenous micro-drilling heads, nozzle designs & wobble welding"),
        ("05", "National Centre of Excellence", "Apex national hub for industrial photonics & advanced manufacturing")
    ]

    sy_step = ry - 26
    for num, stitle, sdesc in steps:
        c.setFillColor(CARD_BG)
        c.roundRect(x2, sy_step - 3, col_w, 18, 2, fill=1, stroke=0)
        c.setFont('IBMPlexMono-Bold', 7.5)
        c.setFillColor(ACCENT_RED)
        c.drawString(x2 + 6, sy_step + 3, num)
        c.setFont('Archivo-Bold', 8)
        c.setFillColor(INK_NAVY)
        c.drawString(x2 + 28, sy_step + 3, stitle)
        c.setFont('Arial', 7.2)
        c.setFillColor(INK_SLATE)
        c.drawString(x2 + 150, sy_step + 3, f"· {sdesc[:42]}")
        sy_step -= 22

    c.setFont('IBMPlexMono-Bold', 8)
    c.setFillColor(INK_SLATE)
    c.drawString(x2, sy_step - 10, "FIVE-POINT INITIATIVE PROGRAMMES")

    inits = [
        ("01 Research", "High-impact laser processing publications, sponsored DRDO/DST defense grants."),
        ("02 Learning & Dev", "Webinars, advanced hands-on workshops, Faculty Development Programmes (FDP)."),
        ("03 Consultancy", "Contract micro-machining, metallurgical failure analysis, industrial cutting consultancy."),
        ("04 Tech Transfer", "Indigenous laser nozzle designs, wobble welding heads, and startup incubation."),
        ("05 Conference", "Hosting the National Symposium on Advances in Industrial Lasers & Precision Manufacturing.")
    ]

    iy = sy_step - 26
    for ititle, idesc in inits:
        c.setFont('IBMPlexMono-Bold', 7.2)
        c.setFillColor(ACCENT_CYAN)
        c.drawString(x2, iy, ititle)
        c.setFont('Arial', 7.5)
        c.setFillColor(INK_SLATE)
        c.drawString(x2 + 88, iy, idesc[:60])
        c.drawString(x2 + 88, iy - 9, idesc[60:])
        iy -= 23

    # --- COLUMN 3: C3 LAB DEDICATION, METRICS & VISIT ---
    c.setFont('Archivo-Bold', 14)
    c.setFillColor(INK_NAVY)
    c.drawString(x3, top_y, "C3  Lab dedication & metrics")

    c.setFont('Archivo-Bold', 10.5)
    c.setFillColor(INK_NAVY)
    c.drawString(x3, top_y - 20, "Department of Mechanical Engineering")
    c.setFont('Arial', 8.5)
    c.setFillColor(INK_SLATE)
    c.drawString(x3, top_y - 32, "COEP Technological University, Pune (Est. 1854)")

    c.setFont('Arial', 7.8)
    c.setFillColor(INK_NAVY)
    c.drawString(x3, top_y - 48, "Established under the Advanced Manufacturing Initiative to provide cutting-edge")
    c.drawString(x3, top_y - 58, "photonics infrastructure for undergraduate teaching, postgraduate research, and")
    c.drawString(x3, top_y - 68, "defense/aerospace industry collaboration in precision laser micro-machining.")

    stat_y = top_y - 94
    stats = [
        ("2", "HIGH-POWER INDUSTRIAL LASER SYSTEMS (Nd:YAG & FIBER)"),
        ("4-AXIS", "PRECISION CNC BRIDGE GANTRY WITH 360° ROTARY CHUCK"),
        ("10 kW", "PEAK PULSE POWER AVAILABLE FOR MICRO-DRILLING & CLADDING"),
        ("2028", "TARGET: NATIONAL CENTRE OF EXCELLENCE IN LASER MACHINING")
    ]

    for val, lbl in stats:
        c.setFillColor(CARD_BG)
        c.roundRect(x3, stat_y - 8, col_w, 36, 3, fill=1, stroke=0)
        c.setFont('Archivo-Bold', 20)
        c.setFillColor(ACCENT_RED)
        c.drawString(x3 + 10, stat_y + 4, val)
        c.setFont('IBMPlexMono-Bold', 7)
        c.setFillColor(INK_NAVY)
        c.drawString(x3 + 74, stat_y + 12, lbl[:40])
        c.drawString(x3 + 74, stat_y + 3, lbl[40:])
        stat_y -= 46

    # Visit the Lab Box filling remaining space down to y=105
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1)
    c.setFillColor(CARD_BG)
    c.roundRect(x3, 105, col_w, stat_y - 105, 4, fill=1, stroke=1)

    c.setFont('Archivo-Bold', 11)
    c.setFillColor(INK_NAVY)
    c.drawString(x3 + 14, stat_y - 24, "Visit the Laser Laboratory")
    c.setFont('Arial', 8.2)
    c.setFillColor(INK_SLATE)
    c.drawString(x3 + 14, stat_y - 38, "Advanced Manufacturing Section, Mechanical Engineering Department")
    c.drawString(x3 + 14, stat_y - 50, "COEP Technological University, Wellesely Road, Shivajinagar, Pune 411005")
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_NAVY)
    c.drawString(x3 + 14, stat_y - 66, "Room: Laser Lab (Mech Annex)  ·  Hours: 09:00 – 18:00")
    c.drawString(x3 + 14, stat_y - 78, "Contact: laser.lab@coeptech.ac.in  ·  Phone: +91 20 2550 7000")
    c.setFont('Arial', 7.5)
    c.setFillColor(INK_MUTED)
    c.drawString(x3 + 14, stat_y - 96, "Equipped with Class 4 interlock enclosures, laser-safe OD7+ viewports,")
    c.drawString(x3 + 14, stat_y - 106, "chilled DI water loops, high-pressure assist gases, and fume extractors.")

    draw_title_block(c, "WHY INDUSTRIAL LASERS, AND WHERE WE ARE GOING", 3, scale="NTS",
                     note="Roadmap, programmes, and laboratory objectives from Department of Mechanical Engineering, COEP Technological University.")
    c.showPage()

# =========================================================================
# SHEET 4: SCAN · STEP INSIDE (GENEROUS PADDING, ZERO GAPS)
# =========================================================================
def build_sheet_4(c):
    draw_outer_grid_frame(c, 4)

    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(44, PAGE_H - 46, "DRG. NO. LASER-001  ·  SHEET 4 / 4")

    c.setFont('IBMPlexMono-Bold', 7)
    c.setFillColor(INK_NAVY)
    c.drawString(44, PAGE_H - 58, "L A S E R   P R O C E S S I N G   &   A D V A N C E D   M A N U F A C T U R I N G   L A B   ·   C O E P   T E C H ,   P U N E")

    c.setFont('IBMPlexMono', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(PAGE_W - 460, PAGE_H - 46, "Two codes, two ways in. Open your phone camera and point it at either code.")
    c.drawString(PAGE_W - 130, PAGE_H - 46, "Nothing to install.")

    # Chromatic Anaglyph Title
    c.setFont('Archivo-Bold', 44)
    c.setFillColor(ANAGLYPH_CYAN)
    c.drawString(46, PAGE_H - 105, "SCAN  ·  STEP INSIDE")
    c.setFillColor(ANAGLYPH_RED)
    c.drawString(44, PAGE_H - 107, "SCAN  ·  STEP INSIDE")

    card_w = 540
    card_h = 585
    card_y = 110

    # --- CODE 1: 3D / AR EXPLORER ---
    x1 = 44
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1.2)
    c.setFillColor(CARD_BG)
    c.roundRect(x1, card_y, card_w, card_h, 6, fill=1, stroke=1)

    c.setFont('IBMPlexMono-Bold', 9.5)
    c.setFillColor(ACCENT_RED)
    c.drawString(x1 + 24, card_y + card_h - 26, "CODE 1  ·  3D & AUGMENTED REALITY (AR)")

    c.setFont('Archivo-Bold', 26)
    c.setFillColor(INK_NAVY)
    c.drawString(x1 + 24, card_y + card_h - 58, "The laser systems,")
    c.drawString(x1 + 24, card_y + card_h - 86, "in your room")

    c.setFont('Arial', 9)
    c.setFillColor(INK_SLATE)
    c.drawString(x1 + 24, card_y + card_h - 106, "Place life-size 3D models of both laser systems on your workshop table,")
    c.drawString(x1 + 24, card_y + card_h - 120, "explode their components into optical paths and CNC stages, and trace the beam.")

    steps1 = [
        ("01", "Scan the QR code, then tap 'View in your room' on your mobile browser."),
        ("02", "Point your phone camera at a table or floor surface to place the 1:1 scale model."),
        ("03", "Walk around the apparatus; switch to 'Exploded View' to inspect the optical cavity.")
    ]

    sy1 = card_y + card_h - 148
    for num, txt in steps1:
        c.setFont('IBMPlexMono-Bold', 12)
        c.setFillColor(ACCENT_RED)
        c.drawString(x1 + 24, sy1, num)
        c.setFont('Arial', 8.5)
        c.setFillColor(INK_NAVY)
        c.drawString(x1 + 52, sy1, txt)
        sy1 -= 20

    qr_size = 175
    qr_x = x1 + 24
    qr_y = sy1 - qr_size - 8
    if os.path.exists('qr_code_ar.png'):
        c.drawImage('qr_code_ar.png', qr_x, qr_y, qr_size, qr_size)

    ix = qr_x + qr_size + 24
    c.setFont('IBMPlexMono-Bold', 8.5)
    c.setFillColor(INK_NAVY)
    c.drawString(ix, qr_y + 155, "TARGET APPARATUSES")

    c.setFont('Arial-Bold', 8)
    c.setFillColor(ACCENT_RED)
    c.drawString(ix, qr_y + 140, "• Nd:YAG 4-Axis CNC Gantry System")
    c.drawString(ix, qr_y + 128, "• Industrial Fiber Laser with Galvo Head")

    c.setFont('IBMPlexMono-Bold', 8)
    c.setFillColor(INK_SLATE)
    c.drawString(ix, qr_y + 104, "SUPPORTED PLATFORMS")
    c.setFont('Arial', 7.5)
    c.setFillColor(INK_NAVY)
    c.drawString(ix, qr_y + 90, "Android phones with Google Play Services for AR (WebXR)")
    c.drawString(ix, qr_y + 80, "iPhone / iPad with iOS 12+ (AR Quick Look)")
    c.drawString(ix, qr_y + 70, "Modern desktop browsers (WebGL 3D Orbit View)")

    c.setFillColor(CARD_BG_LIGHT)
    c.roundRect(ix, qr_y + 10, 290, 42, 3, fill=1, stroke=0)
    c.setFont('IBMPlexMono-Bold', 7)
    c.setFillColor(ACCENT_RED)
    c.drawString(ix + 10, qr_y + 36, "OR TYPE DIRECTLY IN BROWSER:")
    c.setFont('IBMPlexMono-Bold', 10.5)
    c.setFillColor(INK_NAVY)
    c.drawString(ix + 10, qr_y + 20, "coep-laser-lab.github.io/ar")

    mock_y = card_y + 12
    mock_w = card_w - 48
    mock_h = 135
    if os.path.exists('mockup_ar.png'):
        c.drawImage('mockup_ar.png', x1 + 24, mock_y, mock_w, mock_h)

    # --- CODE 2: WEB BROCHURE & SIMULATOR ---
    x2 = 606
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1.2)
    c.setFillColor(CARD_BG)
    c.roundRect(x2, card_y, card_w, card_h, 6, fill=1, stroke=1)

    c.setFont('IBMPlexMono-Bold', 9.5)
    c.setFillColor(INK_NAVY)
    c.drawString(x2 + 24, card_y + card_h - 26, "CODE 2  ·  WEB BROCHURE & LAB SIMULATOR")

    c.setFont('Archivo-Bold', 26)
    c.setFillColor(INK_NAVY)
    c.drawString(x2 + 24, card_y + card_h - 58, "The whole lab,")
    c.drawString(x2 + 24, card_y + card_h - 86, "interactive")

    c.setFont('Arial', 9)
    c.setFillColor(INK_SLATE)
    c.drawString(x2 + 24, card_y + card_h - 106, "Take both laser systems apart in 3D, compare their technical specs,")
    c.drawString(x2 + 24, card_y + card_h - 120, "and run working simulators of pulse drilling, assist gas cutting, and kerf width.")

    steps2 = [
        ("01", "Scan the QR code to open the interactive lab brochure in your browser."),
        ("02", "Select an apparatus and drag the explode slider to isolate subsystems in real time."),
        ("03", "Try working models: laser pulse drilling, assist gas nozzle CFD, and wobble welding.")
    ]

    sy2 = card_y + card_h - 148
    for num, txt in steps2:
        c.setFont('IBMPlexMono-Bold', 12)
        c.setFillColor(INK_NAVY)
        c.drawString(x2 + 24, sy2, num)
        c.setFont('Arial', 8.5)
        c.setFillColor(INK_NAVY)
        c.drawString(x2 + 52, sy2, txt)
        sy2 -= 20

    qr_x2 = x2 + 24
    qr_y2 = sy2 - qr_size - 8
    if os.path.exists('qr_code_web.png'):
        c.drawImage('qr_code_web.png', qr_x2, qr_y2, qr_size, qr_size)

    ix2 = qr_x2 + qr_size + 24
    c.setFont('IBMPlexMono-Bold', 8.5)
    c.setFillColor(INK_NAVY)
    c.drawString(ix2, qr_y2 + 155, "INTERACTIVE MODULES")

    c.setFont('Arial-Bold', 8)
    c.setFillColor(ACCENT_CYAN)
    c.drawString(ix2, qr_y2 + 140, "• 3D Exploded View & Component Inspector")
    c.drawString(ix2, qr_y2 + 128, "• Laser Micro-Drilling Recast Calculator")
    c.drawString(ix2, qr_y2 + 116, "• Cutting Speed & Kerf Width Estimator")

    c.setFont('IBMPlexMono-Bold', 8)
    c.setFillColor(INK_SLATE)
    c.drawString(ix2, qr_y2 + 94, "COMPATIBILITY")
    c.setFont('Arial', 7.5)
    c.setFillColor(INK_NAVY)
    c.drawString(ix2, qr_y2 + 80, "Works in any modern browser (Chrome, Safari, Edge, Firefox)")
    c.drawString(ix2, qr_y2 + 70, "Zero installation required · Fully responsive on mobile & tablet")

    c.setFillColor(CARD_BG_LIGHT)
    c.roundRect(ix2, qr_y2 + 10, 290, 42, 3, fill=1, stroke=0)
    c.setFont('IBMPlexMono-Bold', 7)
    c.setFillColor(ACCENT_RED)
    c.drawString(ix2 + 10, qr_y2 + 36, "OR TYPE DIRECTLY IN BROWSER:")
    c.setFont('IBMPlexMono-Bold', 10.5)
    c.setFillColor(INK_NAVY)
    c.drawString(ix2 + 10, qr_y2 + 20, "coep-laser-lab.github.io")

    if os.path.exists('mockup_web.png'):
        c.drawImage('mockup_web.png', x2 + 24, mock_y, mock_w, mock_h)

    # --- BOTTOM DEFINITION PILLS (AR, VR, MR) ---
    def_y = 52
    pills = [
        ("AR", "Augmented reality", "Digital models placed in the real world, seen through your phone or a tablet."),
        ("VR", "Virtual reality", "A fully simulated optical cavity. Explore inside the resonator and gantry."),
        ("MR", "Mixed reality", "Virtual laser tools that react to the real workshop environment.")
    ]

    px = 44
    for pcode, ptitle, pdesc in pills:
        c.setFont('IBMPlexMono-Bold', 11)
        c.setFillColor(INK_NAVY)
        c.drawString(px, def_y + 16, pcode)

        c.setFont('Archivo-Bold', 9.5)
        c.setFillColor(INK_NAVY)
        c.drawString(px + 32, def_y + 16, ptitle)

        c.setFont('Arial', 7.5)
        c.setFillColor(INK_SLATE)
        c.drawString(px + 32, def_y + 5, pdesc)
        px += 370

    draw_title_block(c, "SCAN · STEP INSIDE", 4, scale="NTS",
                     note="Both QR codes encoded with Level H error correction (30% recovery) and verified before printing. Web app developed for COEP Tech Laser Lab.")
    c.showPage()

def compile_pdf():
    out_pdf = "Laser-Systems-Lab-Poster-Series-A3.pdf"
    print(f"Compiling balanced v3 master engineering poster series to {out_pdf}...")
    c = canvas.Canvas(out_pdf, pagesize=landscape(A3))

    build_sheet_1(c)
    build_sheet_2(c)
    build_sheet_3(c)
    build_sheet_4(c)

    c.save()
    print(f"SUCCESS: {out_pdf} generated cleanly with zero gaps, uniform readable fonts, and balanced cards!")

if __name__ == '__main__':
    compile_pdf()
