import os
import sys
sys.path.append(r'C:\Users\VISHESH-PC\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages')

from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Real Google Fonts
pdfmetrics.registerFont(TTFont('Archivo-Bold', 'Archivo-Bold.ttf'))
pdfmetrics.registerFont(TTFont('IBMPlexMono', 'IBMPlexMono-Regular.ttf'))
pdfmetrics.registerFont(TTFont('IBMPlexMono-Bold', 'IBMPlexMono-SemiBold.ttf'))
pdfmetrics.registerFont(TTFont('Arial', r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', r'C:\Windows\Fonts\arialbd.ttf'))

# Page Dimensions: A3 Landscape (1190.55 x 841.89 pt)
PAGE_W, PAGE_H = landscape(A3)

# Exact Color Palette from Reference
BG_COLOR = HexColor('#FAF8F0')         # Warm drafting cream vellum
INK_NAVY = HexColor('#1B2A44')         # Deep blueprint navy
INK_SLATE = HexColor('#4E5A72')        # Technical secondary slate
INK_MUTED = HexColor('#718096')        # Light muted gray
ACCENT_RED = HexColor('#D13F29')       # Technical vibrant red
ACCENT_CYAN = HexColor('#1590B9')      # Technical cyan
ACCENT_ORANGE = HexColor('#E66A26')    # Accent orange
BORDER_CREAM = HexColor('#E8E2D0')     # Subtle border color
CARD_BG = HexColor('#F4EFE6')          # Card container background
CARD_BG_LIGHT = HexColor('#FFFFFF')    # Pure white card background
ANAGLYPH_RED = HexColor('#FF3B25')     # 3D red layer
ANAGLYPH_CYAN = HexColor('#12B5E6')    # 3D cyan layer

def draw_grid_border(c, sheet_num, total_sheets=4):
    """Draws exact engineering border with 1-8 horizontal and A-F vertical coordinates."""
    c.saveState()
    # Background fill
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Coordinates from ref: outer (margin 16pt) and inner (margin 32pt)
    m_out = 16
    m_in = 32
    w_inner = PAGE_W - 2 * m_in
    h_inner = PAGE_H - 2 * m_in

    # Outer thin border line
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1)
    c.rect(m_out, m_out, PAGE_W - 2 * m_out, PAGE_H - 2 * m_out, fill=0, stroke=1)

    # Inner technical border
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1)
    c.rect(m_in, m_in, w_inner, h_inner, fill=0, stroke=1)

    # Horizontal coordinate ticks 1 to 8 (top & bottom)
    x_step = w_inner / 8.0
    c.setFont('IBMPlexMono', 7)
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

def draw_header(c, sec_code, sec_title, headline, subtitle, sheet_num, total_sheets=4):
    """Draws top header section matching reference PDF."""
    c.saveState()
    
    # Left Header: Drawing Number & Lab Title
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(44, PAGE_H - 46, f"DRG. NO. LASER-001  ·  SHEET {sheet_num} / {total_sheets}")
    
    # Wide-tracked institution title
    c.setFont('IBMPlexMono-Bold', 7)
    c.setFillColor(INK_NAVY)
    spaced_lab = "L A S E R   P R O C E S S I N G   &   A D V A N C E D   M A N U F A C T U R I N G   L A B   ·   C O E P   T E C H"
    c.drawString(44, PAGE_H - 58, spaced_lab)

    # Section Indicator & Headline (starting at x=340)
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(ACCENT_RED)
    spaced_sec = f"S E C T I O N   {sec_code}   ·   " + "   ".join(list(sec_title.upper()))
    c.drawString(340, PAGE_H - 46, spaced_sec)

    c.setFont('Archivo-Bold', 26)
    c.setFillColor(INK_NAVY)
    c.drawString(340, PAGE_H - 74, headline)

    c.setFont('Arial', 8.5)
    c.setFillColor(INK_SLATE)
    c.drawString(340, PAGE_H - 88, subtitle)

    # Top Right Mini QR Box (Sheets 1, 2, 3)
    if sheet_num < 4:
        bx = PAGE_W - 200
        by = PAGE_H - 96
        bw = 156
        bh = 48
        
        c.setStrokeColor(BORDER_CREAM)
        c.setLineWidth(0.8)
        c.setFillColor(CARD_BG)
        c.roundRect(bx, by, bw, bh, 3, fill=1, stroke=1)

        if os.path.exists('qr_code_mini.png'):
            c.drawImage('qr_code_mini.png', bx + 6, by + 4, 40, 40)

        c.setFont('Archivo-Bold', 9.5)
        c.setFillColor(INK_NAVY)
        c.drawString(bx + 52, by + 32, "Explore it in 3D")

        c.setFont('IBMPlexMono', 6.5)
        c.setFillColor(INK_SLATE)
        c.drawString(bx + 52, by + 21, "Scan for the interactive")
        c.drawString(bx + 52, by + 12, "web brochure & simulator.")

        # Pill badge
        c.setFillColor(ACCENT_RED)
        c.roundRect(bx + bw - 32, by + 30, 24, 10, 2, fill=1, stroke=0)
        c.setFont('IBMPlexMono-Bold', 5.5)
        c.setFillColor(HexColor('#FFFFFF'))
        c.drawCentredString(bx + bw - 20, by + 32.5, "WEB")

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

    # TITLE
    c.setFont('IBMPlexMono', 6)
    c.setFillColor(INK_SLATE)
    c.drawString(tb_x + 6, tb_y + 34, "TITLE")
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_NAVY)
    c.drawString(tb_x + 6, tb_y + 25, title.upper())

    # DRG NO
    c.setFont('IBMPlexMono', 6)
    c.setFillColor(INK_SLATE)
    c.drawString(tb_x + 6, tb_y + 13, "DRG. NO.")
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_NAVY)
    c.drawString(tb_x + 6, tb_y + 4, "LASER-001")

    # SHEET
    c.setFont('IBMPlexMono', 6)
    c.setFillColor(INK_SLATE)
    c.drawString(tb_x + 146, tb_y + 13, "SHEET")
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_NAVY)
    c.drawString(tb_x + 146, tb_y + 4, f"{sheet_num} / {total_sheets}")

    # SCALE
    c.setFont('IBMPlexMono', 6)
    c.setFillColor(INK_SLATE)
    c.drawString(tb_x + 206, tb_y + 13, "SCALE")
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_NAVY)
    c.drawString(tb_x + 206, tb_y + 4, scale)

    # Left footnote
    if note:
        c.setFont('Arial', 6.8)
        c.setFillColor(INK_SLATE)
        c.drawString(44, tb_y + 8, note)

    c.restoreState()

# =========================================================================
# SHEET 1: THE HARDWARE (4-QUADRANT ENGINEERING CAD BREAKDOWN)
# =========================================================================
def build_sheet_1(c):
    draw_grid_border(c, 1)
    draw_header(c, "A", "The Hardware", "Two laser systems, taken apart",
                "Every laser apparatus in the lab, drawn from real CAD models and exploded into its main optical and mechanical parts. Numbers on each drawing match the list beside it.", 1)

    quad_data = [
        # Quad 1: Top Left
        {
            "img": "fig_1a_resonator.png",
            "name": "Nd:YAG Pulse Laser Resonator",
            "badges": [("SOLID-STATE", ACCENT_RED), ("1064 nm NIR", INK_NAVY), ("PULSED & Q-SWITCHED", ACCENT_CYAN)],
            "specs": [
                ("WAVELENGTH", "1064 nm fundamental emission"),
                ("PUMP SOURCE", "High-energy Xenon flashlamp array"),
                ("PEAK POWER", "Up to 10 kW (Pulse energy 25–50 J)"),
                ("PULSE WIDTH", "0.2–20 ms / 20 ns EO Q-switched"),
                ("REP RATE", "1 Hz – 100 Hz adjustable")
            ],
            "parts": [
                ("1", "Nd:YAG crystal rod", "active solid-state laser medium"),
                ("2", "Flashlamp pump cavity", "gold-plated elliptical reflector chamber"),
                ("3", "Output coupler mirror", "partial dielectric reflector (T = 40%)"),
                ("4", "Rear total reflector", "99.9% dielectric HR mirror @ 1064 nm"),
                ("5", "EO Q-switch & polarizer", "nanosecond pulse modulation crystal"),
                ("6", "Aperture & shutter", "safety intra-cavity beam dump interlock")
            ],
            "x_box": 44, "y_box": 440, "w_box": 540, "h_box": 285
        },
        # Quad 2: Top Right
        {
            "img": "fig_1b_gantry.png",
            "name": "4-Axis CNC Precision Workstation",
            "badges": [("4-AXIS CNC", ACCENT_RED), ("GRANITE BASE", INK_NAVY), ("360° ROTARY A-AXIS", ACCENT_CYAN)],
            "specs": [
                ("X/Y TRAVEL", "X: 500 mm · Y: 400 mm bridge gantry"),
                ("Z-AXIS", "200 mm vertical ram slide (servo driven)"),
                ("4TH ROTARY", "360° continuous indexing chuck (A-axis)"),
                ("ACCURACY", "±5 µm positioning · ±2 µm repeatability"),
                ("CHILLER", "Closed-loop deionized water chiller ±0.5 °C")
            ],
            "parts": [
                ("1", "Synthetic granite base", "vibration-damped high-mass bed"),
                ("2", "Precision ground ballscrews", "zero-backlash C3 class drive axes"),
                ("3", "Linear motion guide rails", "THK cage-guided linear bearings"),
                ("4", "Coaxial cutting head", "supersonic nozzle + auto-gap sensor"),
                ("5", "Rotary indexing chuck", "harmonic-drive 4th axis for tube parts"),
                ("6", "DI water chiller unit", "refrigeration unit stable to ±0.5 °C")
            ],
            "x_box": 606, "y_box": 440, "w_box": 540, "h_box": 285
        },
        # Quad 3: Bottom Left
        {
            "img": "fig_1c_fiber_engine.png",
            "name": "Single-Mode Yb Fiber Laser Engine",
            "badges": [("ACTIVE FIBER", ACCENT_RED), ("1070 nm", INK_NAVY), ("CW / QCW 1000 W", ACCENT_CYAN)],
            "specs": [
                ("WAVELENGTH", "1070 nm single-mode active emission"),
                ("CW POWER", "1000 W continuous / 2000 W QCW peak"),
                ("BEAM QUALITY", "M² < 1.10 (diffraction-limited TEM₀₀)"),
                ("PUMP SOURCE", "976 nm multi-emitter laser diode arrays"),
                ("WALL EFFICIENCY", "> 38% electrical wall-plug efficiency")
            ],
            "parts": [
                ("1", "Active Yb-doped core", "double-clad optical fiber resonator"),
                ("2", "Fiber Bragg gratings", "all-fiber distributed cavity mirrors"),
                ("3", "976 nm pump diodes", "multi-emitter high-brightness stacks"),
                ("4", "Fused fiber combiner", "high-efficiency pump combiner"),
                ("5", "Clad mode stripper", "removes residual unabsorbed pump light"),
                ("6", "Armored QBH cable", "armored conduit with break detection")
            ],
            "x_box": 44, "y_box": 140, "w_box": 540, "h_box": 285
        },
        # Quad 4: Bottom Right
        {
            "img": "fig_1d_galvo_head.png",
            "name": "Galvo Scan Head & Optical Endstation",
            "badges": [("GALVO HEAD", ACCENT_RED), ("F-THETA LENS", INK_NAVY), ("VACUUM BED", ACCENT_CYAN)],
            "specs": [
                ("SCAN SPEED", "Up to 8,000 mm/s high-speed vectoring"),
                ("SCAN FIELD", "160 × 160 mm telecentric flat field"),
                ("FOCAL SPOT", "15 µm – 25 µm ultra-tight focal spot"),
                ("WORK TABLE", "600 × 400 mm honeycomb vacuum clamping"),
                ("RESOLUTION", "±0.5 µm optical angular resolution")
            ],
            "parts": [
                ("1", "QBH fiber receiver", "water-cooled receptacle & optical seal"),
                ("2", "Collimator doublet", "fused silica optics producing parallel beam"),
                ("3", "X-axis Galvo mirror", "low-inertia beryllium scan mirror"),
                ("4", "Y-axis Galvo mirror", "high-speed digital encoder servo drive"),
                ("5", "Telecentric F-Theta", "maintains orthogonal focal spot across bed"),
                ("6", "Fume extractor", "multi-stage HEPA & carbon filtration unit")
            ],
            "x_box": 606, "y_box": 140, "w_box": 540, "h_box": 285
        }
    ]

    for q in quad_data:
        bx = q["x_box"]
        by = q["y_box"]

        # Diagram on Left of quadrant
        dw = 240
        dh = 150
        dy = by + 90
        if os.path.exists(q["img"]):
            c.drawImage(q["img"], bx, dy, dw, dh)

        # Content on Right of quadrant
        tx = bx + 252
        
        # Name
        c.setFont('Archivo-Bold', 14)
        c.setFillColor(INK_NAVY)
        c.drawString(tx, by + 232, q["name"])

        # Badges
        cur_bx = tx
        for btext, bcol in q["badges"]:
            b_width = len(btext) * 4.2 + 8
            c.setFillColor(bcol)
            c.roundRect(cur_bx, by + 218, b_width, 9, 2, fill=1, stroke=0)
            c.setFont('IBMPlexMono-Bold', 5.5)
            c.setFillColor(HexColor('#FFFFFF'))
            c.drawCentredString(cur_bx + b_width/2.0, by + 220.5, btext)
            cur_bx += b_width + 5

        # Specs Table
        sy = by + 204
        for slabel, sval in q["specs"]:
            c.setFont('IBMPlexMono-Bold', 6)
            c.setFillColor(INK_SLATE)
            c.drawString(tx, sy, slabel)
            c.setFont('Arial', 6.8)
            c.setFillColor(INK_NAVY)
            c.drawString(tx + 72, sy, sval)
            sy -= 9.5

        # Numbered Callouts List (1 to 6)
        py = sy - 4
        for num, pname, pdesc in q["parts"]:
            # Callout number badge
            c.setFillColor(ACCENT_RED)
            c.circle(tx + 4, py + 2.5, 4, fill=1, stroke=0)
            c.setFont('IBMPlexMono-Bold', 5.5)
            c.setFillColor(HexColor('#FFFFFF'))
            c.drawCentredString(tx + 4, py + 0.8, num)

            # Part name (bold) & description
            c.setFont('Arial-Bold', 6.8)
            c.setFillColor(INK_NAVY)
            c.drawString(tx + 12, py + 0.8, pname)
            
            pname_w = c.stringWidth(pname, 'Arial-Bold', 6.8)
            c.setFont('Arial', 6.8)
            c.setFillColor(INK_SLATE)
            c.drawString(tx + 14 + pname_w, py + 0.8, f"· {pdesc}")
            py -= 10

    # --- BOTTOM SECTION: COMPARED TO SCALE ---
    comp_y = 100
    c.setFont('Archivo-Bold', 10)
    c.setFillColor(INK_NAVY)
    c.drawString(44, comp_y, "Compared to scale")
    
    c.setFont('Arial', 7)
    c.setFillColor(INK_SLATE)
    c.drawString(160, comp_y, "Hatched bars represent relative industrial benchmark index. Also in the lab: an Ophir high-power laser beam profiler,")
    c.drawString(160, comp_y - 8.5, "high-speed coaxial pyrometer, and Renishaw laser interferometer for sub-micron gantry calibration.")

    # 4 Bar Chart metric groups
    benchmarks = [
        ("BEAM QUALITY (M²)", [("Nd:YAG Resonator", 2.5, "2.5"), ("Fiber Laser", 1.08, "1.08 (TEM₀₀)")]),
        ("WALL-PLUG EFFICIENCY (%)", [("Nd:YAG Resonator", 2.8, "2.8%"), ("Fiber Laser", 38.5, "38.5%")]),
        ("PEAK PULSE POWER (kW)", [("Nd:YAG Resonator", 10.0, "10.0 kW"), ("Fiber Laser", 2.0, "2.0 kW")]),
        ("POSITIONING ACCURACY (µm)", [("4-Axis CNC Gantry", 5.0, "±5.0 µm"), ("Galvo Scanner", 0.5, "±0.5 µm")])
    ]

    bx_start = 44
    for btitle, blist in benchmarks:
        c.setFont('IBMPlexMono-Bold', 6.5)
        c.setFillColor(INK_NAVY)
        c.drawString(bx_start, comp_y - 22, btitle)

        by_bar = comp_y - 32
        for bname, bval, blabel in blist:
            c.setFont('Arial', 6.2)
            c.setFillColor(INK_SLATE)
            c.drawString(bx_start, by_bar, bname)

            # Gray track & fill bar
            c.setFillColor(CARD_BG)
            c.rect(bx_start + 65, by_bar - 1, 95, 5, fill=1, stroke=0)
            
            bar_len = min(90, (bval / (40 if 'EFFICIENCY' in btitle else 12)) * 90)
            c.setFillColor(ACCENT_RED if 'Fiber' in bname or 'Galvo' in bname else INK_NAVY)
            c.rect(bx_start + 65, by_bar - 1, bar_len, 5, fill=1, stroke=0)

            c.setFont('IBMPlexMono-Bold', 5.8)
            c.setFillColor(INK_NAVY)
            c.drawString(bx_start + 164, by_bar, blabel)
            by_bar -= 8

        bx_start += 215

    draw_title_block(c, "TWO LASER SYSTEMS, TAKEN APART", 1, scale="NTS",
                     note="CAD models and system schematics verified from Laser Processing & Advanced Manufacturing Laboratory, COEP Tech.")
    c.showPage()

# =========================================================================
# SHEET 2: THE RESEARCH (6 PROJECTS IN 3x2 GRID)
# =========================================================================
def build_sheet_2(c):
    draw_grid_border(c, 2)
    draw_header(c, "B", "The Research", "Detail views: what we are building",
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
    card_h = 300
    x_starts = [44, 420, 796]
    y_starts = [435, 125]

    for idx, p in enumerate(projects):
        col_idx = idx % 3
        row_idx = idx // 3
        cx = x_starts[col_idx]
        cy = y_starts[row_idx]

        # Project Box Container
        c.setStrokeColor(BORDER_CREAM)
        c.setLineWidth(0.8)
        c.setFillColor(CARD_BG)
        c.roundRect(cx, cy, card_w, card_h, 4, fill=1, stroke=1)

        # Top Red Category Tag
        c.setFont('IBMPlexMono-Bold', 7)
        c.setFillColor(ACCENT_RED)
        c.drawString(cx + 12, cy + card_h - 18, p["cat"])

        # 2-Line Bold Headline
        c.setFont('Archivo-Bold', 12)
        c.setFillColor(INK_NAVY)
        c.drawString(cx + 12, cy + card_h - 32, p["title_1"])
        c.drawString(cx + 12, cy + card_h - 45, p["title_2"])

        # Summary Paragraph
        c.setFont('Arial', 7.2)
        c.setFillColor(INK_SLATE)
        # 2 lines of description
        c.drawString(cx + 12, cy + card_h - 58, p["desc"][:74])
        c.drawString(cx + 12, cy + card_h - 67, p["desc"][74:150])

        # Technical Graphic Image
        iw = card_w - 24
        ih = 95
        iy = cy + card_h - 170
        if os.path.exists(p["img"]):
            c.drawImage(p["img"], cx + 12, iy, iw, ih)

        # Technical Bullet Points
        by_pt = iy - 12
        for b in p["bullets"]:
            c.setFillColor(ACCENT_CYAN)
            c.circle(cx + 16, by_pt + 2.5, 2, fill=1, stroke=0)
            c.setFont('Arial', 6.6)
            c.setFillColor(INK_NAVY)
            c.drawString(cx + 22, by_pt, b)
            by_pt -= 10

        # Author & Guide in Mono
        c.setFont('IBMPlexMono', 6)
        c.setFillColor(INK_MUTED)
        c.drawString(cx + 12, cy + 10, p["team"])

    draw_title_block(c, "DETAIL VIEWS: WHAT WE ARE BUILDING", 2, scale="NTS",
                     note="Project details from COEP Tech Laser Lab technical reports. Experimental results verified with SEM and optical profilometry.")
    c.showPage()

# =========================================================================
# SHEET 3: THE LAB (WHY LASERS, 5-YEAR PLAN, STATS)
# =========================================================================
def build_sheet_3(c):
    draw_grid_border(c, 3)
    draw_header(c, "C", "The Lab", "Why industrial lasers, and where we are going",
                "Lasers replace mechanical cutting tools with focused photons of coherent light. Here is why that matters to engineers, and the lab's plan for the next five years.", 3)

    # 3 Structured Vertical Columns
    col_w = 345
    x1 = 44
    x2 = 416
    x3 = 788
    top_y = PAGE_H - 110

    # --- COLUMN 1: C1 WHY INDUSTRIAL LASERS IN ADVANCED MANUFACTURING ---
    c.setFont('Archivo-Bold', 12)
    c.setFillColor(INK_NAVY)
    c.drawString(x1, top_y, "C1  Why industrial lasers in engineering?")

    pillars = [
        ("Design before you cut", "Direct CAD/CAM digital workflow eliminates expensive custom dies, hard tooling, and long setup lead times."),
        ("Zero mechanical tool wear", "The cutting tool is an optical beam that never dulls, chatters, or causes mechanical deformation on thin walls."),
        ("Micro-scale precision", "Focused spot sizes under 20 µm enable micro-drilling of cooling holes, micro-stents, and semiconductor features."),
        ("Minimal heat-affected zone", "Ultra-short pulsed laser energy vaporizes material before heat can conduct into the bulk workpiece."),
        ("Multi-material versatility", "Effortlessly processes superalloys, titanium, diamond, tungsten carbide, advanced ceramics, and composite laminates."),
        ("Green, sustainable manufacturing", "Eliminates cutting fluids, lubricants, toxic chemical etching acids, and dangerous hazardous sludge.")
    ]

    py = top_y - 20
    for title, desc in pillars:
        c.setFont('Archivo-Bold', 9)
        c.setFillColor(INK_NAVY)
        c.drawString(x1, py, title)
        c.setFont('Arial', 7.2)
        c.setFillColor(INK_SLATE)
        c.drawString(x1, py - 10, desc[:75])
        c.drawString(x1, py - 19, desc[75:145])
        py -= 34

    # WHERE IT IS ALREADY USED
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(x1, py - 6, "WHERE IT IS ALREADY USED")

    sectors = [
        ("Healthcare & Stents", "Aerospace Turbines", "Automotive & EV", "Semiconductors"),
        ("Tool & Die Micro-Machining", "Biomaterial Implants", "Solar PV Scribing", "Defense & Space")
    ]
    
    sy = py - 18
    for row in sectors:
        sx = x1
        for sec in row:
            c.setFont('IBMPlexMono', 6.8)
            c.setFillColor(INK_NAVY)
            c.drawString(sx, sy, sec)
            sx += 86
        sy -= 11

    c.setFont('Arial', 7)
    c.setFillColor(INK_MUTED)
    c.drawString(x1, sy - 10, "Global laser hubs: Stuttgart, Boston, Tokyo, Wuhan, Oxford. In India, Atmanirbhar Bharat")
    c.drawString(x1, sy - 19, "and the defense manufacturing corridors are accelerating industrial laser adoption. Building")
    c.drawString(x1, sy - 28, "that specialized technical workforce and indigenous IP is this laboratory's primary mandate.")

    # --- COLUMN 2: C2 REVISION TABLE: THE FIVE-YEAR PLAN ---
    c.setFont('Archivo-Bold', 12)
    c.setFillColor(INK_NAVY)
    c.drawString(x2, top_y, "C2  Revision table: the five-year plan")

    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(x2, top_y - 18, "FIVE STEPS TO A CENTRE OF EXCELLENCE (CoE)")

    steps = [
        ("01", "Research Laboratory", "Core infrastructure, baseline testing & calibration"),
        ("02", "Knowledge Transfer Hub", "FDP courses, hands-on student workshops & TA training"),
        ("03", "Industry Partner Centre", "Sponsored defense grants, contract testing & prototypes"),
        ("04", "Notable IP & Patent Portfolio", "Indigenous micro-drilling heads & wobble welding"),
        ("05", "National Centre of Excellence", "Apex hub for industrial photonics & advanced manufacturing")
    ]

    sy_step = top_y - 32
    for num, stitle, sdesc in steps:
        c.setFillColor(CARD_BG)
        c.rect(x2, sy_step - 2, col_w, 14, fill=1, stroke=0)
        c.setFont('IBMPlexMono-Bold', 7)
        c.setFillColor(ACCENT_RED)
        c.drawString(x2 + 4, sy_step + 2, num)
        c.setFont('Archivo-Bold', 7.5)
        c.setFillColor(INK_NAVY)
        c.drawString(x2 + 22, sy_step + 2, stitle)
        c.setFont('Arial', 6.8)
        c.setFillColor(INK_SLATE)
        c.drawString(x2 + 130, sy_step + 2, f"· {sdesc}")
        sy_step -= 17

    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(x2, sy_step - 6, "FIVE-POINT INITIATIVE PROGRAMMES")

    inits = [
        ("01 Research", "High-impact laser processing publications, sponsored DRDO/DST defense grants."),
        ("02 Learning & Dev", "Webinars, advanced hands-on workshops, Faculty Development Programmes (FDP)."),
        ("03 Consultancy", "Contract micro-machining, metallurgical failure analysis, industrial cutting consultancy."),
        ("04 Tech Transfer", "Indigenous laser nozzle designs, wobble welding heads, and startup incubation."),
        ("05 Conference", "Hosting the National Symposium on Advances in Industrial Lasers & Precision Manufacturing.")
    ]

    iy = sy_step - 18
    for ititle, idesc in inits:
        c.setFont('IBMPlexMono-Bold', 6.8)
        c.setFillColor(ACCENT_CYAN)
        c.drawString(x2, iy, ititle)
        c.setFont('Arial', 6.8)
        c.setFillColor(INK_SLATE)
        c.drawString(x2 + 78, iy, idesc)
        iy -= 13

    # REVISION TIMELINE 2024 TO 2028
    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(x2, iy - 6, "REVISION TIMELINE · 2024 TO 2028")

    revs = [
        ("2024", "REV A", "Commissioning of 4-axis gantry, optical alignment & baseline testing"),
        ("2025", "REV B", "Industry workshops, contract testing services, and B.Tech TA lab curriculum"),
        ("2026", "REV C", "TODAY · Postgraduate certification, DST/DRDO research, and wobble welding IP"),
        ("2027", "REV D", "Technology transfer of specialized supersonic nozzle & trepanning heads"),
        ("2028", "REV E", "State-of-the-art National Centre of Excellence in Advanced Laser Systems")
    ]

    ry = iy - 20
    for yr, rev, rdesc in revs:
        is_today = "TODAY" in rdesc
        c.setFillColor(HexColor('#FFF5F5') if is_today else CARD_BG)
        c.rect(x2, ry - 2, col_w, 14, fill=1, stroke=0)
        c.setFont('IBMPlexMono-Bold', 7)
        c.setFillColor(ACCENT_RED if is_today else INK_NAVY)
        c.drawString(x2 + 4, ry + 2, yr)
        c.drawString(x2 + 36, ry + 2, rev)
        c.setFont('Arial', 6.8)
        c.setFillColor(INK_NAVY if is_today else INK_SLATE)
        c.drawString(x2 + 76, ry + 2, rdesc)
        ry -= 16

    # --- COLUMN 3: C3 LAB DEDICATION, METRICS & VISIT ---
    c.setFont('Archivo-Bold', 12)
    c.setFillColor(INK_NAVY)
    c.drawString(x3, top_y, "C3  Lab dedication & metrics")

    c.setFont('Archivo-Bold', 9.5)
    c.setFillColor(INK_NAVY)
    c.drawString(x3, top_y - 18, "Department of Mechanical Engineering")
    c.setFont('Arial', 8)
    c.setFillColor(INK_SLATE)
    c.drawString(x3, top_y - 29, "COEP Technological University, Pune (Est. 1854)")

    c.setFont('Arial', 7.2)
    c.setFillColor(INK_NAVY)
    c.drawString(x3, top_y - 44, "Established under the Advanced Manufacturing Initiative to provide cutting-edge")
    c.drawString(x3, top_y - 53, "photonics infrastructure for undergraduate teaching, postgraduate research, and")
    c.drawString(x3, top_y - 62, "defense/aerospace industry collaboration in precision laser micro-machining.")

    # 4 Large Metric Badges
    stat_y = top_y - 85
    stats = [
        ("2", "HIGH-POWER INDUSTRIAL LASER SYSTEMS (Nd:YAG & FIBER)"),
        ("4-AXIS", "PRECISION CNC BRIDGE GANTRY WITH 360° ROTARY CHUCK"),
        ("10 kW", "PEAK PULSE POWER AVAILABLE FOR MICRO-DRILLING & CLADDING"),
        ("2028", "TARGET: NATIONAL CENTRE OF EXCELLENCE IN LASER MACHINING")
    ]

    for val, lbl in stats:
        c.setFillColor(CARD_BG)
        c.roundRect(x3, stat_y - 8, col_w, 32, 3, fill=1, stroke=0)
        c.setFont('Archivo-Bold', 18)
        c.setFillColor(ACCENT_RED)
        c.drawString(x3 + 8, stat_y + 3, val)
        c.setFont('IBMPlexMono-Bold', 6.5)
        c.setFillColor(INK_NAVY)
        c.drawString(x3 + 68, stat_y + 10, lbl[:40])
        c.drawString(x3 + 68, stat_y + 2, lbl[40:])
        stat_y -= 40

    # Visit the Lab Box
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1)
    c.setFillColor(CARD_BG)
    c.roundRect(x3, stat_y - 20, col_w, 75, 4, fill=1, stroke=1)

    c.setFont('Archivo-Bold', 9.5)
    c.setFillColor(INK_NAVY)
    c.drawString(x3 + 12, stat_y + 38, "Visit the Laser Laboratory")
    c.setFont('Arial', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(x3 + 12, stat_y + 26, "Advanced Manufacturing Section, Mechanical Engineering Department")
    c.drawString(x3 + 12, stat_y + 15, "COEP Technological University, Wellesely Road, Shivajinagar, Pune 411005")
    c.setFont('IBMPlexMono', 6.8)
    c.setFillColor(INK_NAVY)
    c.drawString(x3 + 12, stat_y + 2, "Room: Laser Lab (Mech Annex)  ·  Hours: 09:00 – 18:00")
    c.drawString(x3 + 12, stat_y - 9, "Contact: laser.lab@coeptech.ac.in  ·  Phone: +91 20 2550 7000")

    draw_title_block(c, "WHY INDUSTRIAL LASERS, AND WHERE WE ARE GOING", 3, scale="NTS",
                     note="Roadmap, programmes, and laboratory objectives from Department of Mechanical Engineering, COEP Technological University.")
    c.showPage()

# =========================================================================
# SHEET 4: SCAN · STEP INSIDE (THE SCANNER PART WITH ANAGLYPH 3D TITLE)
# =========================================================================
def build_sheet_4(c):
    draw_grid_border(c, 4)

    # Top Bar: Drawing Number & Lab Title
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

    # Chromatic Anaglyph 3D Double Print Title: "SCAN · STEP INSIDE"
    # Cyan offset layer
    c.setFont('Archivo-Bold', 44)
    c.setFillColor(ANAGLYPH_CYAN)
    c.drawString(46, PAGE_H - 105, "SCAN  ·  STEP INSIDE")
    # Red primary layer
    c.setFillColor(ANAGLYPH_RED)
    c.drawString(44, PAGE_H - 107, "SCAN  ·  STEP INSIDE")

    # TWO HUGE SCANNER BLOCKS (LEFT & RIGHT)
    card_w = 540
    card_h = 580
    card_y = 110

    # --- CODE 1: 3D / AR EXPLORER ---
    x1 = 44
    c.setStrokeColor(BORDER_CREAM)
    c.setLineWidth(1.2)
    c.setFillColor(CARD_BG)
    c.roundRect(x1, card_y, card_w, card_h, 6, fill=1, stroke=1)

    # Header Tag
    c.setFont('IBMPlexMono-Bold', 9)
    c.setFillColor(ACCENT_RED)
    c.drawString(x1 + 24, card_y + card_h - 26, "CODE 1  ·  3D & AUGMENTED REALITY (AR)")

    # Big 3-Line Headline
    c.setFont('Archivo-Bold', 26)
    c.setFillColor(INK_NAVY)
    c.drawString(x1 + 24, card_y + card_h - 58, "The laser systems,")
    c.drawString(x1 + 24, card_y + card_h - 86, "in your room")

    # Subtitle
    c.setFont('Arial', 8.5)
    c.setFillColor(INK_SLATE)
    c.drawString(x1 + 24, card_y + card_h - 106, "Place life-size 3D models of both laser systems on your workshop table,")
    c.drawString(x1 + 24, card_y + card_h - 118, "explode their components into optical paths and CNC stages, and trace the beam.")

    # Instructions 01, 02, 03
    steps1 = [
        ("01", "Scan the QR code, then tap 'View in your room' on your mobile browser."),
        ("02", "Point your phone camera at a table or floor surface to place the 1:1 scale model."),
        ("03", "Walk around the apparatus; switch to 'Exploded View' to inspect the optical cavity.")
    ]
    
    sy1 = card_y + card_h - 146
    for num, txt in steps1:
        c.setFont('IBMPlexMono-Bold', 11)
        c.setFillColor(ACCENT_RED)
        c.drawString(x1 + 24, sy1, num)
        c.setFont('Arial', 8)
        c.setFillColor(INK_NAVY)
        c.drawString(x1 + 50, sy1, txt)
        sy1 -= 18

    # Large Scannable QR Code 1 (AR)
    qr_size = 175
    qr_x = x1 + 24
    qr_y = sy1 - qr_size - 8
    if os.path.exists('qr_code_ar.png'):
        c.drawImage('qr_code_ar.png', qr_x, qr_y, qr_size, qr_size)

    # Info beside QR code
    ix = qr_x + qr_size + 24
    c.setFont('IBMPlexMono-Bold', 8)
    c.setFillColor(INK_NAVY)
    c.drawString(ix, qr_y + 155, "TARGET APPARATUSES")

    c.setFont('Arial-Bold', 7.5)
    c.setFillColor(ACCENT_RED)
    c.drawString(ix, qr_y + 140, "• Nd:YAG 4-Axis CNC Gantry System")
    c.drawString(ix, qr_y + 128, "• Industrial Fiber Laser with Galvo Head")

    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(ix, qr_y + 104, "SUPPORTED PLATFORMS")
    c.setFont('Arial', 7)
    c.setFillColor(INK_NAVY)
    c.drawString(ix, qr_y + 90, "Android phones with Google Play Services for AR (WebXR)")
    c.drawString(ix, qr_y + 80, "iPhone / iPad with iOS 12+ (AR Quick Look)")
    c.drawString(ix, qr_y + 70, "Modern desktop browsers (WebGL 3D Orbit View)")

    # Fallback URL box
    c.setFillColor(CARD_BG_LIGHT)
    c.roundRect(ix, qr_y + 10, 290, 42, 3, fill=1, stroke=0)
    c.setFont('IBMPlexMono-Bold', 6.5)
    c.setFillColor(ACCENT_RED)
    c.drawString(ix + 10, qr_y + 36, "OR TYPE DIRECTLY IN BROWSER:")
    c.setFont('IBMPlexMono-Bold', 10)
    c.setFillColor(INK_NAVY)
    c.drawString(ix + 10, qr_y + 20, "coep-laser-lab.github.io/ar")

    # 3D Preview Mockup Graphic underneath
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

    # Header Tag
    c.setFont('IBMPlexMono-Bold', 9)
    c.setFillColor(INK_NAVY)
    c.drawString(x2 + 24, card_y + card_h - 26, "CODE 2  ·  WEB BROCHURE & LAB SIMULATOR")

    # Big 3-Line Headline
    c.setFont('Archivo-Bold', 26)
    c.setFillColor(INK_NAVY)
    c.drawString(x2 + 24, card_y + card_h - 58, "The whole lab,")
    c.drawString(x2 + 24, card_y + card_h - 86, "interactive")

    # Subtitle
    c.setFont('Arial', 8.5)
    c.setFillColor(INK_SLATE)
    c.drawString(x2 + 24, card_y + card_h - 106, "Take both laser systems apart in 3D, compare their technical specs,")
    c.drawString(x2 + 24, card_y + card_h - 118, "and run working simulators of pulse drilling, assist gas cutting, and kerf width.")

    # Instructions 01, 02, 03
    steps2 = [
        ("01", "Scan the QR code to open the interactive lab brochure in your browser."),
        ("02", "Select an apparatus and drag the explode slider to isolate subsystems in real time."),
        ("03", "Try working models: laser pulse drilling, assist gas nozzle CFD, and wobble welding.")
    ]

    sy2 = card_y + card_h - 146
    for num, txt in steps2:
        c.setFont('IBMPlexMono-Bold', 11)
        c.setFillColor(INK_NAVY)
        c.drawString(x2 + 24, sy2, num)
        c.setFont('Arial', 8)
        c.setFillColor(INK_NAVY)
        c.drawString(x2 + 50, sy2, txt)
        sy2 -= 18

    # Large Scannable QR Code 2 (WEB)
    qr_x2 = x2 + 24
    qr_y2 = sy2 - qr_size - 8
    if os.path.exists('qr_code_web.png'):
        c.drawImage('qr_code_web.png', qr_x2, qr_y2, qr_size, qr_size)

    # Info beside QR code
    ix2 = qr_x2 + qr_size + 24
    c.setFont('IBMPlexMono-Bold', 8)
    c.setFillColor(INK_NAVY)
    c.drawString(ix2, qr_y2 + 155, "INTERACTIVE MODULES")

    c.setFont('Arial-Bold', 7.5)
    c.setFillColor(ACCENT_CYAN)
    c.drawString(ix2, qr_y2 + 140, "• 3D Exploded View & Component Inspector")
    c.drawString(ix2, qr_y2 + 128, "• Laser Micro-Drilling Recast Calculator")
    c.drawString(ix2, qr_y2 + 116, "• Cutting Speed & Kerf Width Estimator")

    c.setFont('IBMPlexMono-Bold', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(ix2, qr_y2 + 94, "COMPATIBILITY")
    c.setFont('Arial', 7)
    c.setFillColor(INK_NAVY)
    c.drawString(ix2, qr_y2 + 80, "Works in any modern browser (Chrome, Safari, Edge, Firefox)")
    c.drawString(ix2, qr_y2 + 70, "Zero installation required · Fully responsive on mobile & tablet")

    # Fallback URL box
    c.setFillColor(CARD_BG_LIGHT)
    c.roundRect(ix2, qr_y2 + 10, 290, 42, 3, fill=1, stroke=0)
    c.setFont('IBMPlexMono-Bold', 6.5)
    c.setFillColor(ACCENT_RED)
    c.drawString(ix2 + 10, qr_y2 + 36, "OR TYPE DIRECTLY IN BROWSER:")
    c.setFont('IBMPlexMono-Bold', 10)
    c.setFillColor(INK_NAVY)
    c.drawString(ix2 + 10, qr_y2 + 20, "coep-laser-lab.github.io")

    # Web UI Mockup Graphic underneath
    if os.path.exists('mockup_web.png'):
        c.drawImage('mockup_web.png', x2 + 24, mock_y, mock_w, mock_h)

    # --- BOTTOM DEFINITION PILLS (AR, VR, MR) ---
    def_y = 65
    pills = [
        ("AR", "Augmented reality", "Digital models placed in the real world, seen through your phone or a tablet."),
        ("VR", "Virtual reality", "A fully simulated optical cavity. Explore inside the resonator and gantry."),
        ("MR", "Mixed reality", "Virtual laser tools that react to the real workshop environment.")
    ]
    
    px = 44
    for pcode, ptitle, pdesc in pills:
        c.setFont('IBMPlexMono-Bold', 10)
        c.setFillColor(INK_NAVY)
        c.drawString(px, def_y + 14, pcode)

        c.setFont('Archivo-Bold', 9)
        c.setFillColor(INK_NAVY)
        c.drawString(px + 28, def_y + 14, ptitle)

        c.setFont('Arial', 7)
        c.setFillColor(INK_SLATE)
        c.drawString(px + 28, def_y + 4, pdesc)
        px += 370

    draw_title_block(c, "SCAN · STEP INSIDE", 4, scale="NTS",
                     note="Both QR codes encoded with Level H error correction (30% recovery) and verified before printing. Web app developed for COEP Tech Laser Lab.")
    c.showPage()

def compile_pdf():
    out_pdf = "Laser-Systems-Lab-Poster-Series-A3.pdf"
    print(f"Compiling perfect engineering poster series to {out_pdf}...")
    c = canvas.Canvas(out_pdf, pagesize=landscape(A3))

    build_sheet_1(c)
    build_sheet_2(c)
    build_sheet_3(c)
    build_sheet_4(c)

    c.save()
    print(f"SUCCESS: {out_pdf} generated cleanly with Archivo and IBM Plex Mono fonts!")

if __name__ == '__main__':
    compile_pdf()
