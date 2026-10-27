import os
import sys
sys.path.append(r'C:\Users\VISHESH-PC\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages')

from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register TrueType Fonts for exact engineering aesthetic
pdfmetrics.registerFont(TTFont('Mono', r'C:\Windows\Fonts\consola.ttf'))
pdfmetrics.registerFont(TTFont('Mono-Bold', r'C:\Windows\Fonts\consolab.ttf'))
pdfmetrics.registerFont(TTFont('Sans', r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('Sans-Bold', r'C:\Windows\Fonts\arialbd.ttf'))

# Constants & Colors
PAGE_W, PAGE_H = landscape(A3) # 1190.55 x 841.89 pt
BG_COLOR = HexColor('#FAF8F0')
INK_DARK = HexColor('#1B2A44')
INK_SLATE = HexColor('#4E5A72')
INK_MUTED = HexColor('#718096')
BORDER_COLOR = HexColor('#E2D9C5')
BORDER_DARK = HexColor('#1B2A44')
ACCENT_RED = HexColor('#D23F29')
ACCENT_CYAN = HexColor('#1590BA')
ACCENT_ORANGE = HexColor('#DD6B20')
CARD_BG = HexColor('#F4EFE6')
CARD_BG_LIGHT = HexColor('#FFFFFF')
HATCH_COLOR = HexColor('#CBD5E0')

def draw_engineering_border(c, sheet_num, total_sheets=4):
    """Draws standard engineering drawing border with coordinates 1-8 and A-F."""
    c.saveState()
    
    # Outer background fill
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    
    # Margins
    margin_outer = 16
    margin_inner = 32
    
    # Outer thin border
    c.setStrokeColor(BORDER_DARK)
    c.setLineWidth(1.2)
    c.rect(margin_outer, margin_outer, PAGE_W - 2 * margin_outer, PAGE_H - 2 * margin_outer, fill=0, stroke=1)
    
    # Inner border line
    c.setLineWidth(0.8)
    c.rect(margin_inner, margin_inner, PAGE_W - 2 * margin_inner, PAGE_H - 2 * margin_inner, fill=0, stroke=1)
    
    # Grid ticks and labels
    c.setFont('Mono', 7)
    c.setFillColor(INK_SLATE)
    
    # Horizontal coordinates 1 to 8 (top and bottom)
    x_step = (PAGE_W - 2 * margin_inner) / 8.0
    for i in range(8):
        x_center = margin_inner + i * x_step + x_step / 2.0
        # Bottom label
        c.drawCentredString(x_center, margin_outer + 5, str(i + 1))
        # Top label
        c.drawCentredString(x_center, PAGE_H - margin_outer - 11, str(i + 1))
        # Ticks
        if i > 0:
            tx = margin_inner + i * x_step
            c.setStrokeColor(BORDER_COLOR)
            c.setLineWidth(0.6)
            c.line(tx, margin_outer, tx, margin_inner)
            c.line(tx, PAGE_H - margin_inner, tx, PAGE_H - margin_outer)
            
    # Vertical coordinates A to F (left and right)
    y_step = (PAGE_H - 2 * margin_inner) / 6.0
    letters = ['F', 'E', 'D', 'C', 'B', 'A'] # Top to bottom
    for j in range(6):
        y_center = margin_inner + j * y_step + y_step / 2.0
        # Left label
        c.drawCentredString(margin_outer + 8, y_center - 2.5, letters[j])
        # Right label
        c.drawCentredString(PAGE_W - margin_outer - 8, y_center - 2.5, letters[j])
        # Ticks
        if j > 0:
            ty = margin_inner + j * y_step
            c.setStrokeColor(BORDER_COLOR)
            c.setLineWidth(0.6)
            c.line(margin_outer, ty, margin_inner, ty)
            c.line(PAGE_W - margin_inner, ty, PAGE_W - margin_outer, ty)
            
    c.restoreState()

def draw_header(c, section_code, section_title, headline, subtitle, sheet_num, total_sheets=4):
    """Draws top header section with drawing number, institution name, and mini QR box."""
    c.saveState()
    top_y = PAGE_H - 42
    
    # Drawing Number & Institution bar
    c.setFont('Mono-Bold', 8.5)
    c.setFillColor(INK_DARK)
    c.drawString(44, top_y, f"DRG. NO. LASER-001  ·  SHEET {sheet_num} / {total_sheets}")
    c.drawString(44, top_y - 14, "LASER PROCESSING & ADVANCED MANUFACTURING LAB  ·  COEP TECH, PUNE")
    
    # Section indicator
    c.setFont('Mono-Bold', 8.5)
    c.setFillColor(ACCENT_RED)
    c.drawString(400, top_y, f"SECTION {section_code}  ·  {section_title.upper()}")
    
    # Main Headline
    c.setFont('Sans-Bold', 22)
    c.setFillColor(INK_DARK)
    c.drawString(400, top_y - 25, headline)
    
    # Subtitle
    c.setFont('Sans', 9)
    c.setFillColor(INK_SLATE)
    c.drawString(400, top_y - 39, subtitle)
    
    # Mini QR Box on Right (Sheets 1, 2, 3)
    if sheet_num < 4:
        box_x = PAGE_W - 225
        box_y = top_y - 45
        box_w = 180
        box_h = 50
        
        c.setStrokeColor(BORDER_COLOR)
        c.setLineWidth(0.8)
        c.setFillColor(CARD_BG)
        c.roundRect(box_x, box_y, box_w, box_h, 3, fill=1, stroke=1)
        
        # Mini QR image
        if os.path.exists('qr_code_mini.png'):
            c.drawImage('qr_code_mini.png', box_x + 6, box_y + 5, 40, 40)
            
        c.setFont('Sans-Bold', 8)
        c.setFillColor(INK_DARK)
        c.drawString(box_x + 52, box_y + 34, "Explore it in 3D")
        
        c.setFont('Sans', 6.8)
        c.setFillColor(INK_SLATE)
        c.drawString(box_x + 52, box_y + 23, "Scan for the interactive web")
        c.drawString(box_x + 52, box_y + 13, "brochure & laser simulator.")
        
        # Pill badge
        c.setFillColor(ACCENT_RED)
        c.roundRect(box_x + box_w - 36, box_y + 30, 28, 12, 2, fill=1, stroke=0)
        c.setFont('Mono-Bold', 6)
        c.setFillColor(HexColor('#FFFFFF'))
        c.drawCentredString(box_x + box_w - 22, box_y + 33.5, "WEB")
        
    c.restoreState()

def draw_title_block(c, title, sheet_num, total_sheets=4, scale="NTS", note=""):
    """Draws standard engineering title block at bottom right."""
    c.saveState()
    tb_w = 260
    tb_h = 48
    tb_x = PAGE_W - 32 - tb_w
    tb_y = 32
    
    c.setStrokeColor(BORDER_DARK)
    c.setLineWidth(1)
    c.setFillColor(CARD_BG)
    c.rect(tb_x, tb_y, tb_w, tb_h, fill=1, stroke=1)
    
    # Internal dividing lines
    c.setLineWidth(0.6)
    c.line(tb_x, tb_y + 24, tb_x + tb_w, tb_y + 24)
    c.line(tb_x + 140, tb_y, tb_x + 140, tb_y + 24)
    c.line(tb_x + 200, tb_y, tb_x + 200, tb_y + 24)
    
    # Title
    c.setFont('Mono', 6.5)
    c.setFillColor(INK_SLATE)
    c.drawString(tb_x + 6, tb_y + 38, "TITLE")
    c.setFont('Mono-Bold', 8.5)
    c.setFillColor(INK_DARK)
    c.drawString(tb_x + 6, tb_y + 28, title.upper())
    
    # Drawing Number
    c.setFont('Mono', 6.5)
    c.setFillColor(INK_SLATE)
    c.drawString(tb_x + 6, tb_y + 14, "DRG. NO.")
    c.setFont('Mono-Bold', 8)
    c.setFillColor(INK_DARK)
    c.drawString(tb_x + 6, tb_y + 5, "LASER-001")
    
    # Sheet
    c.setFont('Mono', 6.5)
    c.setFillColor(INK_SLATE)
    c.drawString(tb_x + 146, tb_y + 14, "SHEET")
    c.setFont('Mono-Bold', 8)
    c.setFillColor(INK_DARK)
    c.drawString(tb_x + 146, tb_y + 5, f"{sheet_num} / {total_sheets}")
    
    # Scale
    c.setFont('Mono', 6.5)
    c.setFillColor(INK_SLATE)
    c.drawString(tb_x + 206, tb_y + 14, "SCALE")
    c.setFont('Mono-Bold', 8)
    c.setFillColor(INK_DARK)
    c.drawString(tb_x + 206, tb_y + 5, scale)
    
    # Note on left of title block
    if note:
        c.setFont('Sans', 6.8)
        c.setFillColor(INK_SLATE)
        c.drawString(44, tb_y + 8, note)
        
    c.restoreState()

# ==========================================
# SHEET 1: THE HARDWARE (TWO LASER SYSTEMS)
# ==========================================
def build_sheet_1(c):
    draw_engineering_border(c, 1)
    draw_header(c, "A", "The Hardware", "Two laser systems, taken apart",
                "Every laser apparatus in the lab, drawn from real CAD models and exploded into its main optical and mechanical parts. Numbers match the list beside it.", 1)
    
    col_w = 540
    y_top = PAGE_H - 105
    
    # --- LEFT COLUMN: Nd:YAG PULSE LASER & 4-AXIS CNC GANTRY ---
    x_left = 44
    c.setFont('Sans-Bold', 15)
    c.setFillColor(INK_DARK)
    c.drawString(x_left, y_top, "Nd:YAG Pulse Laser System + 4-Axis CNC Gantry")
    
    # Badges
    badges_left = [("SOLID-STATE", ACCENT_RED), ("PULSED 1064 nm", INK_DARK), ("4-AXIS GANTRY", ACCENT_CYAN)]
    bx = x_left
    for text, col in badges_left:
        c.setFillColor(col)
        c.roundRect(bx, y_top - 15, len(text)*4.8 + 8, 10, 2, fill=1, stroke=0)
        c.setFont('Mono-Bold', 6)
        c.setFillColor(HexColor('#FFFFFF'))
        c.drawString(bx + 4, y_top - 12.5, text)
        bx += len(text)*4.8 + 14
        
    # Specs Table Left
    specs_left = [
        ("WAVELENGTH", "1064 nm (Fundamental Near-Infrared solid-state emission)"),
        ("PEAK POWER", "Up to 10 kW peak pulse power (Pulse energy 25 – 50 J)"),
        ("PULSE WIDTH", "0.2 ms – 20 ms free-running / 20 ns electro-optic Q-switched"),
        ("PULSE FREQ", "1 Hz – 100 Hz adjustable pulse repetition rate"),
        ("CNC GANTRY", "X: 500 mm · Y: 400 mm · Z: 200 mm precision ballscrew gantry"),
        ("4TH ROTARY", "360° Continuous A-axis rotary chuck for cylindrical parts"),
        ("ACCURACY", "±5 µm linear positioning · ±2 µm bidirectional repeatability"),
        ("CHILLER", "Closed-loop deionized water chiller, thermal stability ±0.5 °C")
    ]
    
    sy = y_top - 28
    for label, val in specs_left:
        c.setFont('Mono-Bold', 6.8)
        c.setFillColor(INK_SLATE)
        c.drawString(x_left, sy, label)
        c.setFont('Sans', 7.5)
        c.setFillColor(INK_DARK)
        c.drawString(x_left + 72, sy, val)
        sy -= 11.5
        
    # Technical Diagram FIG 1A
    diag_w = 480
    diag_h = 240
    diag_y = sy - diag_h - 10
    if os.path.exists('fig_1a_ndyag_gantry.png'):
        c.drawImage('fig_1a_ndyag_gantry.png', x_left, diag_y, diag_w, diag_h)
        
    # Itemized Part Callouts Left (1 to 8)
    parts_left = [
        ("1", "Resonator & Nd:YAG crystal rod · Flashlamp-pumped optical cavity emitting 1064 nm beam"),
        ("2", "Q-switch & polarizer · Electro-optic Pockels cell gating high peak-power nanosecond pulses"),
        ("3", "Beam expanding telescope · Collimates beam and reduces divergence to < 1.2 mrad"),
        ("4", "Turning dielectric mirrors · High damage threshold HR coated mirrors (>99.9% @ 1064 nm)"),
        ("5", "Assist gas cutting head & nozzle · Coaxial supersonic nozzle with auto-capacitive height sensor"),
        ("6", "4-Axis CNC bridge & rotary chuck · Precision ballscrews, THK linear rails, 360° A-axis"),
        ("7", "Closed-loop DI water chiller · Dual-stage refrigeration maintaining cavity temperature to ±0.5 °C"),
        ("8", "CNC console & Class 4 enclosure · G-code pulse synchronization, OD7+ laser interlock shield")
    ]
    
    py = diag_y - 12
    for num, desc in parts_left[:4]:
        c.setFillColor(ACCENT_RED)
        c.circle(x_left + 6, py + 3, 5, fill=1, stroke=0)
        c.setFont('Mono-Bold', 6)
        c.setFillColor(HexColor('#FFFFFF'))
        c.drawCentredString(x_left + 6, py + 1.2, num)
        c.setFont('Sans', 7.2)
        c.setFillColor(INK_DARK)
        c.drawString(x_left + 16, py + 1, desc)
        py -= 11
        
    for num, desc in parts_left[4:]:
        c.setFillColor(ACCENT_RED)
        c.circle(x_left + 6, py + 3, 5, fill=1, stroke=0)
        c.setFont('Mono-Bold', 6)
        c.setFillColor(HexColor('#FFFFFF'))
        c.drawCentredString(x_left + 6, py + 1.2, num)
        c.setFont('Sans', 7.2)
        c.setFillColor(INK_DARK)
        c.drawString(x_left + 16, py + 1, desc)
        py -= 11

    # --- RIGHT COLUMN: INDUSTRIAL FIBER LASER SYSTEM ---
    x_right = 615
    c.setFont('Sans-Bold', 15)
    c.setFillColor(INK_DARK)
    c.drawString(x_right, y_top, "Industrial Fiber Laser System Apparatus")
    
    # Badges
    badges_right = [("FIBER LASER", ACCENT_RED), ("CW / QCW 1070 nm", INK_DARK), ("DUAL-GALVO SCAN", ACCENT_CYAN)]
    bx = x_right
    for text, col in badges_right:
        c.setFillColor(col)
        c.roundRect(bx, y_top - 15, len(text)*4.8 + 8, 10, 2, fill=1, stroke=0)
        c.setFont('Mono-Bold', 6)
        c.setFillColor(HexColor('#FFFFFF'))
        c.drawString(bx + 4, y_top - 12.5, text)
        bx += len(text)*4.8 + 14
        
    # Specs Table Right
    specs_right = [
        ("WAVELENGTH", "1070 nm (Single-mode Yb-doped double-clad active fiber)"),
        ("OUTPUT POWER", "1000 W Continuous Wave (CW) / 2000 W Quasi-CW (QCW)"),
        ("BEAM QUALITY", "M² < 1.1 (Diffraction-limited single-mode TEM₀₀ beam)"),
        ("FOCAL SPOT", "15 µm – 25 µm ultra-fine spot size for extreme fluence"),
        ("SCAN HEAD", "High-speed dual-axis digital galvanometer scanner"),
        ("SCAN SPEED", "Up to 8,000 mm/s high-precision vector marking & cutting"),
        ("WORK TABLE", "600 × 400 mm honeycomb vacuum bed with part fixture pins"),
        ("WALL EFFICIENCY", "> 38% electrical-to-optical wall-plug conversion efficiency")
    ]
    
    sy = y_top - 28
    for label, val in specs_right:
        c.setFont('Mono-Bold', 6.8)
        c.setFillColor(INK_SLATE)
        c.drawString(x_right, sy, label)
        c.setFont('Sans', 7.5)
        c.setFillColor(INK_DARK)
        c.drawString(x_right + 72, sy, val)
        sy -= 11.5
        
    # Technical Diagram FIG 1B
    if os.path.exists('fig_1b_fiber_laser.png'):
        c.drawImage('fig_1b_fiber_laser.png', x_right, diag_y, diag_w, diag_h)
        
    # Itemized Part Callouts Right (1 to 8)
    parts_right = [
        ("1", "Active Yb-doped fiber core · Multi-emitter 976 nm laser diode array pump modules"),
        ("2", "Armored QBH delivery cable · Flexible armored fiber conduit with clad-mode stripping"),
        ("3", "Collimator & protective cartridge · Fused silica collimation optics, dual seal windows"),
        ("4", "Dual-Galvo scan head · High-speed digital servo mirrors for rapid inertia-free vectoring"),
        ("5", "Telecentric F-Theta lens · Flat-field uniform focal plane across full 160 × 160 mm field"),
        ("6", "Honeycomb bed & stage · Vibration-damped vacuum clamping bed with catchment drawer"),
        ("7", "Multi-stage fume extractor · Dual-stage HEPA and activated carbon filtration for fumes"),
        ("8", "Central control rack & supply · Real-time digital fieldbus with analog PWM power shaping")
    ]
    
    py = diag_y - 12
    for num, desc in parts_right[:4]:
        c.setFillColor(ACCENT_RED)
        c.circle(x_right + 6, py + 3, 5, fill=1, stroke=0)
        c.setFont('Mono-Bold', 6)
        c.setFillColor(HexColor('#FFFFFF'))
        c.drawCentredString(x_right + 6, py + 1.2, num)
        c.setFont('Sans', 7.2)
        c.setFillColor(INK_DARK)
        c.drawString(x_right + 16, py + 1, desc)
        py -= 11
        
    for num, desc in parts_right[4:]:
        c.setFillColor(ACCENT_RED)
        c.circle(x_right + 6, py + 3, 5, fill=1, stroke=0)
        c.setFont('Mono-Bold', 6)
        c.setFillColor(HexColor('#FFFFFF'))
        c.drawCentredString(x_right + 6, py + 1.2, num)
        c.setFont('Sans', 7.2)
        c.setFillColor(INK_DARK)
        c.drawString(x_right + 16, py + 1, desc)
        py -= 11

    # --- BOTTOM COMPARISON SECTION (COMPARED TO SCALE) ---
    comp_y = 100
    c.setFont('Sans-Bold', 9.5)
    c.setFillColor(INK_DARK)
    c.drawString(44, comp_y, "Compared to scale")
    c.setFont('Sans', 7.2)
    c.setFillColor(INK_SLATE)
    c.drawString(150, comp_y, "Hatched bars indicate relative industrial benchmark indices. Also in the lab: Ophir high-power laser beam profiler,")
    c.drawString(150, comp_y - 9, "coaxial high-speed pyrometer, and Renishaw laser interferometer for sub-micron gantry calibration.")

    # 4 Bar Chart Metrics
    metrics = [
        ("BEAM QUALITY (M²)", [("Nd:YAG", 2.5, "2.5"), ("Fiber Laser", 1.08, "1.08 (TEM₀₀)")]),
        ("WALL-PLUG EFFICIENCY (%)", [("Nd:YAG", 2.8, "2.8%"), ("Fiber Laser", 38.5, "38.5%")]),
        ("PEAK POWER (kW)", [("Nd:YAG", 10.0, "10.0 kW"), ("Fiber Laser", 2.0, "2.0 kW")]),
        ("POSITIONING ACCURACY (µm)", [("4-Axis Gantry", 5.0, "±5.0 µm"), ("Galvo Scanner", 0.5, "±0.5 µm")])
    ]
    
    chart_x = 44
    chart_w = 195
    for title, bars in metrics:
        c.setFont('Mono-Bold', 6.8)
        c.setFillColor(INK_DARK)
        c.drawString(chart_x, comp_y - 26, title)
        
        by = comp_y - 36
        for name, val, label_text in bars:
            c.setFont('Sans', 6.5)
            c.setFillColor(INK_SLATE)
            c.drawString(chart_x, by, name)
            
            # Bar background & filled bar
            bar_len = min(90, (val / (40 if 'EFFICIENCY' in title else 12)) * 90)
            c.setFillColor(CARD_BG)
            c.rect(chart_x + 55, by - 1, 95, 6, fill=1, stroke=0)
            c.setFillColor(ACCENT_RED if 'Fiber' in name or 'Galvo' in name else INK_DARK)
            c.rect(chart_x + 55, by - 1, bar_len, 6, fill=1, stroke=0)
            
            c.setFont('Mono-Bold', 6.2)
            c.setFillColor(INK_DARK)
            c.drawString(chart_x + 154, by, label_text)
            by -= 9
            
        chart_x += 215

    draw_title_block(c, "TWO LASER SYSTEMS, TAKEN APART", 1, scale="NTS", 
                     note="CAD models, ray traces, and specifications verified from COEP Tech Laser & Advanced Manufacturing Laboratory.")
    c.showPage()

# ==========================================
# SHEET 2: THE RESEARCH (6 PROJECTS)
# ==========================================
def build_sheet_2(c):
    draw_engineering_border(c, 2)
    draw_header(c, "B", "The Research", "Detail views: what we are building",
                "Six research projects from the lab's own investigations, from aerospace turbine micro-drilling to EV battery welding. Each one uses our Nd:YAG or Fiber laser systems.", 2)
    
    projects = [
        {
            "cat": "AEROSPACE DRILLING · Nd:YAG 4-AXIS GANTRY",
            "title": "Effusion cooling micro-holes in single-crystal superalloys",
            "desc": "Laser micro-drilling of shallow 25° angled cooling holes in Inconel 718 and CMSX-4 turbine blades. The 4-axis gantry synchronizes rotary indexing and spatial orientation.",
            "team": "Shubham Kulkarni, Rahul Shinde (M.Tech Manufacturing)  ·  Guide: Prof. Dr. S. S. Pardeshi",
            "bullets": [
                "Laser percussion & trepanning drilling with 1064 nm pulsed Nd:YAG.",
                "Pulse duration: 150 µs · Peak power: 8 kW · Recast layer suppressed to < 12 µm.",
                "Supersonic coaxial N₂ assist gas at 14 bar expels molten dross completely.",
                "Zero micro-cracking confirmed under field-emission SEM cross-section analysis."
            ],
            "img": "res_1_drilling.png"
        },
        {
            "cat": "BIOMATERIAL TEXTURING · FIBER LASER",
            "title": "Superhydrophobic micro-patterning of titanium implants",
            "desc": "High-speed galvanometer surface texturing of Ti-6Al-4V orthopedic implants with micro-dimple and groove arrays, achieving bacterial repulsion and enhanced bone bonding.",
            "team": "Tanvi Jadhav, Aditya Deshpande (B.Tech Mechanical)  ·  Guide: Prof. Dr. S. S. Pardeshi",
            "bullets": [
                "Fast vector scanning at 2,500 mm/s with single-mode fiber laser.",
                "Apparent water contact angle θ > 154° achieved in static sessile drop tests.",
                "Bacterial adhesion (S. aureus) reduced by 85% compared to smooth controls.",
                "Zero toxic chemical residue; 100% optical green surface modification."
            ],
            "img": "res_2_texturing.png"
        },
        {
            "cat": "E-MOBILITY & BATTERY · FIBER LASER",
            "title": "Spatter-free copper-to-aluminum EV busbar welding",
            "desc": "Dissimilar metal laser lap welding of 0.3 mm high-conductivity copper to 0.5 mm aluminum sheets for electric vehicle pouch cell tabs and current collectors.",
            "team": "Aniket More, Pranav Joshi (Research Scholars)  ·  Guide: Dr. S. S. Ohol",
            "bullets": [
                "Spatial circular beam oscillation (wobble) at 400 Hz suppresses keyhole collapse.",
                "Intermetallic brittle compound (CuAl₂) layer thickness restricted to < 4 µm.",
                "Lap shear joint failure load > 850 N, exceeding automotive OEM benchmarks.",
                "Electrical contact resistance across weld interface below 12 µΩ."
            ],
            "img": "res_3_welding.png"
        },
        {
            "cat": "COMPUTATIONAL OPTICS · BEAM DIAGNOSTICS",
            "title": "Real-time wavefront sensing & dynamic thermal bloom correction",
            "desc": "In-situ Shack-Hartmann sensor profiling high-fluence laser pulses, dynamically compensating thermal lensing in the objective lens via adaptive beam expansion.",
            "team": "Pooja Gaikwad (Research Scholar)  ·  Guide: Dr. S. S. Anasane",
            "bullets": [
                "Shack-Hartmann lenslet array measuring wavefront aberrations in real time.",
                "Closed-loop motorized beam expansion telescope corrects defocus in 35 ms.",
                "Focal spot drift reduced from 1.8 mm to < 0.08 mm over 30-min continuous runs.",
                "Maintains constant irradiance (> 10⁷ W/cm²) throughout deep-cavity machining."
            ],
            "img": "res_4_wavefront.png"
        },
        {
            "cat": "PROCESS HYDRODYNAMICS · MULTIPHYSICS CFD",
            "title": "Supersonic assist-gas dynamics & melt ejection modeling",
            "desc": "OpenFOAM compressible CFD simulation and Schlieren optical imaging of coaxial supersonic Laval nozzles, optimizing boundary-layer gas shear for dross-free laser cutting.",
            "team": "Vikas Patil, Rohit Jagtap (B.Tech R&AI)  ·  Guide: Dr. P. R. Dhamangaonkar",
            "bullets": [
                "Convergent-divergent Laval nozzle profile delivers Mach 2.2 supersonic core jet.",
                "Shock diamond placement tuned to align with kerf entry at 1.5 mm stand-off.",
                "Boundary layer shear stress on melt pool increased by 38% vs conical nozzles.",
                "Eliminates bottom dross burrs on 4 mm aerospace titanium alloy cuts."
            ],
            "img": "res_5_cfd.png"
        },
        {
            "cat": "ACADEMICS & CURRICULUM · FINAL-YEAR B.TECH / M.TECH",
            "title": "Hands-on laser machining curriculum & CNC safety training",
            "desc": "Comprehensive laboratory course covering laser-matter interaction, CNC G-code pulse synchronization, beam diagnostics, and Class 4 laser safety certification.",
            "team": "Faculty In-Charge: Dr. S. S. Pardeshi  ·  Dept. of Mechanical Engineering, COEP Tech",
            "bullets": [
                "Hands-on modules: optical alignment, focal height tracking, and pulse energy tuning.",
                "Deterministic position-synchronized laser triggering (PSO) with 4-axis motion.",
                "Metallographic sample prep, optical microscopy, and Vickers microhardness profiling.",
                "Industry internships and joint research projects with TRUMPF, IPG, and Laserline."
            ],
            "img": "res_6_sync.png"
        }
    ]
    
    # Render 6 projects in 3 columns x 2 rows
    grid_cols = 3
    col_width = 360
    col_gap = 18
    row_height = 310
    start_x = 44
    start_y = PAGE_H - 105
    
    for idx, p in enumerate(projects):
        c_idx = idx % grid_cols
        r_idx = idx // grid_cols
        px = start_x + c_idx * (col_width + col_gap)
        py = start_y - (r_idx + 1) * row_height
        
        # Project Box Container
        c.setStrokeColor(BORDER_COLOR)
        c.setLineWidth(0.8)
        c.setFillColor(CARD_BG)
        c.roundRect(px, py, col_width, row_height - 12, 4, fill=1, stroke=1)
        
        # Category Tag
        c.setFont('Mono-Bold', 7)
        c.setFillColor(ACCENT_RED)
        c.drawString(px + 10, py + row_height - 24, p["cat"])
        
        # Title
        c.setFont('Sans-Bold', 10.5)
        c.setFillColor(INK_DARK)
        c.drawString(px + 10, py + row_height - 38, p["title"])
        
        # Technical Graphic Panel
        img_w = col_width - 20
        img_h = 100
        img_y = py + row_height - 146
        if os.path.exists(p["img"]):
            c.drawImage(p["img"], px + 10, img_y, img_w, img_h)
            
        # Description
        c.setFont('Sans', 7.5)
        c.setFillColor(INK_DARK)
        c.drawString(px + 10, img_y - 12, p["desc"][:70])
        c.drawString(px + 10, img_y - 21, p["desc"][70:140])
        
        # Bullets
        by = img_y - 34
        for b in p["bullets"]:
            c.setFillColor(ACCENT_CYAN)
            c.circle(px + 14, by + 2.5, 2, fill=1, stroke=0)
            c.setFont('Sans', 6.8)
            c.setFillColor(INK_SLATE)
            c.drawString(px + 20, by, b)
            by -= 10
            
        # Team & Guide
        c.setFont('Mono', 6.2)
        c.setFillColor(INK_MUTED)
        c.drawString(px + 10, py + 8, p["team"])
        
    draw_title_block(c, "DETAIL VIEWS: WHAT WE ARE BUILDING", 2, scale="NTS",
                     note="Project details from COEP Tech Laser Lab technical reports. Experimental results verified with SEM and optical profilometry.")
    c.showPage()

# ==========================================
# SHEET 3: THE LAB (ROADMAP & VISION)
# ==========================================
def build_sheet_3(c):
    draw_engineering_border(c, 3)
    draw_header(c, "C", "The Lab", "Why industrial lasers, and where we are going",
                "Lasers replace mechanical cutting tools with focused photons of coherent light. Here is why that transforms precision manufacturing, and our five-year roadmap.", 3)
    
    col_w = 345
    col_gap = 25
    y_top = PAGE_H - 110
    
    # --- COLUMN 1: C1 WHY INDUSTRIAL LASERS IN ADVANCED MANUFACTURING ---
    x1 = 44
    c.setFont('Mono-Bold', 11)
    c.setFillColor(ACCENT_RED)
    c.drawString(x1, y_top, "C1  Why industrial lasers in modern engineering?")
    
    pillars = [
        ("Design before you cut", "Direct CAD/CAM digital workflow eliminates expensive custom dies, hard tooling, and long setup lead times."),
        ("Zero mechanical tool wear", "The cutting tool is an optical beam that never dulls, chatters, or causes mechanical deformation on thin walls."),
        ("Micro-scale precision", "Focused spot sizes under 20 µm enable micro-drilling of cooling holes, micro-stents, and semiconductor features."),
        ("Minimal heat-affected zone", "Ultra-short pulsed laser energy vaporizes material before heat can conduct into the bulk workpiece."),
        ("Multi-material versatility", "Effortlessly processes superalloys, titanium, diamond, tungsten carbide, advanced ceramics, and composite laminates."),
        ("Green, sustainable manufacturing", "Eliminates cutting fluids, lubricants, toxic chemical etching acids, and dangerous hazardous sludge.")
    ]
    
    py = y_top - 20
    for title, desc in pillars:
        c.setFont('Sans-Bold', 8.5)
        c.setFillColor(INK_DARK)
        c.drawString(x1, py, title)
        c.setFont('Sans', 7.5)
        c.setFillColor(INK_SLATE)
        c.drawString(x1, py - 10, desc[:72])
        c.drawString(x1, py - 19, desc[72:140])
        py -= 32
        
    # Where it is used
    c.setFont('Mono-Bold', 8)
    c.setFillColor(INK_DARK)
    c.drawString(x1, py - 6, "WHERE IT IS ALREADY USED")
    c.setFont('Sans', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(x1, py - 18, "Aerospace turbine components  ·  Medical cardiovascular stents  ·  Semiconductor dicing")
    c.drawString(x1, py - 28, "EV battery tab welding  ·  Solar photovoltaic scribing  ·  Orthopedic implant texturing")
    
    c.setFont('Sans', 7.2)
    c.setFillColor(INK_MUTED)
    c.drawString(x1, py - 46, "Global laser hubs: Stuttgart, Boston, Tokyo, Wuhan, Oxford. In India, Atmanirbhar Bharat")
    c.drawString(x1, py - 56, "and the defense manufacturing corridors are accelerating industrial laser adoption. Building")
    c.drawString(x1, py - 66, "that specialized technical workforce and indigenous IP is this laboratory's primary mandate.")

    # --- COLUMN 2: C2 REVISION TABLE: THE FIVE-YEAR PLAN ---
    x2 = x1 + col_w + col_gap
    c.setFont('Mono-Bold', 11)
    c.setFillColor(ACCENT_RED)
    c.drawString(x2, y_top, "C2  Revision table: the five-year plan")
    
    c.setFont('Mono-Bold', 8)
    c.setFillColor(INK_DARK)
    c.drawString(x2, y_top - 20, "FIVE STEPS TO A CENTRE OF EXCELLENCE (CoE)")
    
    steps = [
        ("01", "Research Laboratory · Core infrastructure, baseline testing & calibration"),
        ("02", "Knowledge Transfer Hub · FDP courses, hands-on student workshops & TA training"),
        ("03", "Industry Partner Centre · Sponsored defense grants, contract testing & prototypes"),
        ("04", "Notable IP & Patent Portfolio · Indigenous micro-drilling heads & wobble welding"),
        ("05", "National Centre of Excellence · Apex hub for industrial photonics & advanced manufacturing")
    ]
    
    sy = y_top - 34
    for num, text in steps:
        c.setFillColor(CARD_BG)
        c.rect(x2, sy - 2, col_w, 14, fill=1, stroke=0)
        c.setFont('Mono-Bold', 7.5)
        c.setFillColor(ACCENT_RED)
        c.drawString(x2 + 4, sy + 2, num)
        c.setFont('Sans', 7.5)
        c.setFillColor(INK_DARK)
        c.drawString(x2 + 24, sy + 2, text)
        sy -= 18
        
    c.setFont('Mono-Bold', 8)
    c.setFillColor(INK_DARK)
    c.drawString(x2, sy - 8, "FIVE-POINT INITIATIVE PROGRAMMES")
    
    inits = [
        ("01 Research", "High-impact laser processing publications, sponsored DRDO/DST defense grants."),
        ("02 Learning & Dev", "Webinars, advanced hands-on workshops, Faculty Development Programmes (FDP)."),
        ("03 Consultancy", "Contract micro-machining, metallurgical failure analysis, industrial cutting consultancy."),
        ("04 Tech Transfer", "Indigenous laser nozzle designs, wobble welding heads, and startup incubation."),
        ("05 Conference", "Hosting the National Symposium on Advances in Industrial Lasers & Precision Manufacturing.")
    ]
    
    iy = sy - 22
    for title, desc in inits:
        c.setFont('Mono-Bold', 7.5)
        c.setFillColor(ACCENT_CYAN)
        c.drawString(x2, iy, title)
        c.setFont('Sans', 7.2)
        c.setFillColor(INK_SLATE)
        c.drawString(x2 + 82, iy, desc)
        iy -= 13
        
    # Revision Timeline REV A to REV E
    c.setFont('Mono-Bold', 8)
    c.setFillColor(INK_DARK)
    c.drawString(x2, iy - 8, "REVISION TIMELINE · 2024 TO 2028")
    
    revs = [
        ("2024", "REV A", "Commissioning of 4-axis gantry, laser optical alignment & baseline testing"),
        ("2025", "REV B", "Industry workshops, contract testing services, and B.Tech TA lab curriculum"),
        ("2026", "REV C", "TODAY · Postgraduate certification, DST/DRDO research, and wobble welding IP"),
        ("2027", "REV D", "Technology transfer of specialized supersonic nozzle & trepanning heads"),
        ("2028", "REV E", "State-of-the-art National Centre of Excellence in Advanced Laser Systems")
    ]
    
    ry = iy - 22
    for yr, rev, desc in revs:
        is_today = "TODAY" in desc
        c.setFillColor(HexColor('#FFF5F5') if is_today else CARD_BG)
        c.rect(x2, ry - 2, col_w, 14, fill=1, stroke=0)
        c.setFont('Mono-Bold', 7)
        c.setFillColor(ACCENT_RED if is_today else INK_DARK)
        c.drawString(x2 + 4, ry + 2, yr)
        c.drawString(x2 + 34, ry + 2, rev)
        c.setFont('Sans', 6.8)
        c.setFillColor(INK_DARK if is_today else INK_SLATE)
        c.drawString(x2 + 75, ry + 2, desc)
        ry -= 16

    # --- COLUMN 3: C3 DEDICATION, METRICS & VISIT INFO ---
    x3 = x2 + col_w + col_gap
    c.setFont('Mono-Bold', 11)
    c.setFillColor(ACCENT_RED)
    c.drawString(x3, y_top, "C3  Lab dedication & metrics")
    
    c.setFont('Sans-Bold', 10)
    c.setFillColor(INK_DARK)
    c.drawString(x3, y_top - 20, "Department of Mechanical Engineering")
    c.setFont('Sans', 8.5)
    c.setFillColor(INK_SLATE)
    c.drawString(x3, y_top - 32, "COEP Technological University, Pune (Est. 1854)")
    
    c.setFont('Sans', 7.5)
    c.setFillColor(INK_DARK)
    c.drawString(x3, y_top - 48, "Established under the Advanced Manufacturing Initiative to provide cutting-edge")
    c.drawString(x3, y_top - 58, "hands-on photonics infrastructure for undergraduate teaching, postgraduate research,")
    c.drawString(x3, y_top - 68, "and industry collaboration in precision laser micro-machining and welding.")
    
    # Lab Stat Badges
    stat_y = y_top - 95
    stats = [
        ("2", "HIGH-POWER INDUSTRIAL LASER SYSTEMS (Nd:YAG & FIBER)"),
        ("4-AXIS", "PRECISION CNC BRIDGE GANTRY WITH 360° ROTARY CHUCK"),
        ("10 kW", "PEAK PULSE POWER AVAILABLE FOR MICRO-DRILLING & CLADDING"),
        ("2028", "TARGET: NATIONAL CENTRE OF EXCELLENCE IN LASER MACHINING")
    ]
    
    for val, lbl in stats:
        c.setFillColor(CARD_BG)
        c.roundRect(x3, stat_y - 8, col_w, 32, 3, fill=1, stroke=0)
        c.setFont('Mono-Bold', 16)
        c.setFillColor(ACCENT_RED)
        c.drawString(x3 + 8, stat_y + 4, val)
        c.setFont('Mono-Bold', 6.8)
        c.setFillColor(INK_DARK)
        c.drawString(x3 + 68, stat_y + 10, lbl[:40])
        c.drawString(x3 + 68, stat_y + 2, lbl[40:])
        stat_y -= 40
        
    # Visit the Lab Box
    c.setStrokeColor(BORDER_COLOR)
    c.setLineWidth(1)
    c.setFillColor(CARD_BG)
    c.roundRect(x3, stat_y - 20, col_w, 75, 4, fill=1, stroke=1)
    
    c.setFont('Sans-Bold', 9)
    c.setFillColor(INK_DARK)
    c.drawString(x3 + 12, stat_y + 40, "Visit the Laser Laboratory")
    c.setFont('Sans', 7.5)
    c.setFillColor(INK_SLATE)
    c.drawString(x3 + 12, stat_y + 28, "Advanced Manufacturing Section, Mechanical Engineering Department")
    c.drawString(x3 + 12, stat_y + 17, "COEP Technological University, Wellesely Road, Shivajinagar, Pune 411005")
    c.setFont('Mono', 7)
    c.setFillColor(INK_DARK)
    c.drawString(x3 + 12, stat_y + 4, "Room: Laser Lab (Mech Annex)  ·  Hours: 09:00 – 18:00")
    c.drawString(x3 + 12, stat_y - 8, "Contact: laser.lab@coeptech.ac.in  ·  Phone: +91 20 2550 7000")
    
    draw_title_block(c, "WHY INDUSTRIAL LASERS, AND WHERE WE ARE GOING", 3, scale="NTS",
                     note="Roadmap, programmes, and laboratory objectives from Department of Mechanical Engineering, COEP Technological University.")
    c.showPage()

# ==========================================
# SHEET 4: SCAN · STEP INSIDE (SCANNER PART)
# ==========================================
def build_sheet_4(c):
    draw_engineering_border(c, 4)
    draw_header(c, "D", "Scan · Step Inside", "Two codes, two ways in. Open your phone camera and point it at either code.",
                "Nothing to install. Step inside the 3D laser laboratory, inspect exploded views, or interact with working machining simulators.", 4)
    
    # Definition Badges under headline
    top_y = PAGE_H - 105
    badges = [
        ("PULSED Nd:YAG", "Solid-state 1064 nm pulsed laser with 4-axis CNC gantry for micro-drilling & precision spot welding"),
        ("FIBER LASER", "Single-mode 1070 nm active fiber laser with high-speed dual-galvo scan head for surface texturing & cutting"),
        ("4-AXIS CNC", "Position-synchronized multi-axis motion control with real-time nanosecond laser pulse gating")
    ]
    
    bx = 44
    for tag, desc in badges:
        c.setFillColor(ACCENT_RED if "Nd:YAG" in tag else (INK_DARK if "FIBER" in tag else ACCENT_CYAN))
        c.roundRect(bx, top_y, 75, 12, 2, fill=1, stroke=0)
        c.setFont('Mono-Bold', 6.5)
        c.setFillColor(HexColor('#FFFFFF'))
        c.drawCentredString(bx + 37.5, top_y + 3.5, tag)
        c.setFont('Sans', 7.2)
        c.setFillColor(INK_SLATE)
        c.drawString(bx + 82, top_y + 3, desc)
        bx += 365

    # TWO HUGE SCANNER SECTIONS (LEFT & RIGHT)
    card_w = 540
    card_h = 635
    card_y = 70
    
    # --- CODE 1: 3D & AUGMENTED REALITY EXPLORER ---
    x1 = 44
    c.setStrokeColor(BORDER_DARK)
    c.setLineWidth(1.4)
    c.setFillColor(CARD_BG)
    c.roundRect(x1, card_y, card_w, card_h, 6, fill=1, stroke=1)
    
    # Category Header
    c.setFont('Mono-Bold', 10)
    c.setFillColor(ACCENT_RED)
    c.drawString(x1 + 24, card_y + card_h - 28, "CODE 1  ·  3D & AUGMENTED REALITY (AR)")
    
    # Title
    c.setFont('Sans-Bold', 22)
    c.setFillColor(INK_DARK)
    c.drawString(x1 + 24, card_y + card_h - 56, "The laser systems, in your room")
    
    # Subtitle
    c.setFont('Sans', 10)
    c.setFillColor(INK_SLATE)
    c.drawString(x1 + 24, card_y + card_h - 74, "Place life-size 3D models of both laser systems on your workshop table,")
    c.drawString(x1 + 24, card_y + card_h - 88, "explode their components into optical paths and CNC stages, and trace the beam.")
    
    # Step-by-step instructions
    steps1 = [
        ("01", "Scan the QR code, then tap 'View in 3D / AR' on your mobile browser."),
        ("02", "Point your camera at a table or floor surface to place the 1:1 scale apparatus."),
        ("03", "Walk around the machine; toggle 'Exploded View' to inspect the optical cavity & gantry.")
    ]
    
    sy = card_y + card_h - 116
    for num, txt in steps1:
        c.setFont('Mono-Bold', 12)
        c.setFillColor(ACCENT_RED)
        c.drawString(x1 + 24, sy, num)
        c.setFont('Sans', 8.8)
        c.setFillColor(INK_DARK)
        c.drawString(x1 + 52, sy, txt)
        sy -= 22
        
    # Large Scannable QR Code 1
    qr_size = 180
    qr_x = x1 + 24
    qr_y = sy - qr_size - 10
    if os.path.exists('qr_code_ar.png'):
        c.drawImage('qr_code_ar.png', qr_x, qr_y, qr_size, qr_size)
        
    # Information beside QR code
    ix = qr_x + qr_size + 24
    c.setFont('Mono-Bold', 9)
    c.setFillColor(INK_DARK)
    c.drawString(ix, qr_y + 160, "TARGET APPARATUSES")
    
    c.setFont('Sans-Bold', 8)
    c.setFillColor(ACCENT_RED)
    c.drawString(ix, qr_y + 142, "• Nd:YAG 4-Axis CNC Gantry System")
    c.drawString(ix, qr_y + 128, "• Industrial Fiber Laser with Galvo Head")
    
    c.setFont('Mono-Bold', 8)
    c.setFillColor(INK_SLATE)
    c.drawString(ix, qr_y + 104, "SUPPORTED PLATFORMS")
    c.setFont('Sans', 7.5)
    c.setFillColor(INK_DARK)
    c.drawString(ix, qr_y + 90, "Android phones with Google Play Services (WebXR)")
    c.drawString(ix, qr_y + 78, "iPhone / iPad with iOS 12+ (AR Quick Look)")
    c.drawString(ix, qr_y + 66, "Modern desktop browsers (WebGL 3D Orbit)")
    
    # Fallback URL box
    c.setFillColor(HexColor('#FFFFFF'))
    c.roundRect(ix, qr_y + 10, 290, 42, 3, fill=1, stroke=0)
    c.setFont('Mono-Bold', 7)
    c.setFillColor(ACCENT_RED)
    c.drawString(ix + 10, qr_y + 38, "OR TYPE DIRECTLY IN BROWSER:")
    c.setFont('Mono-Bold', 10.5)
    c.setFillColor(INK_DARK)
    c.drawString(ix + 10, qr_y + 20, "coep-laser-lab.github.io/ar")
    
    # 3D AR Preview Graphic underneath
    mock_y = card_y + 14
    mock_w = card_w - 48
    mock_h = 135
    if os.path.exists('mockup_ar.png'):
        c.drawImage('mockup_ar.png', x1 + 24, mock_y, mock_w, mock_h)

    # --- CODE 2: INTERACTIVE WEB BROCHURE & LAB SIMULATOR ---
    x2 = 605
    c.setStrokeColor(BORDER_DARK)
    c.setLineWidth(1.4)
    c.setFillColor(CARD_BG)
    c.roundRect(x2, card_y, card_w, card_h, 6, fill=1, stroke=1)
    
    # Category Header
    c.setFont('Mono-Bold', 10)
    c.setFillColor(INK_DARK)
    c.drawString(x2 + 24, card_y + card_h - 28, "CODE 2  ·  WEB BROCHURE & SIMULATOR")
    
    # Title
    c.setFont('Sans-Bold', 22)
    c.setFillColor(INK_DARK)
    c.drawString(x2 + 24, card_y + card_h - 56, "The whole lab, interactive")
    
    # Subtitle
    c.setFont('Sans', 10)
    c.setFillColor(INK_SLATE)
    c.drawString(x2 + 24, card_y + card_h - 74, "Take both laser systems apart in 3D, compare their technical specs,")
    c.drawString(x2 + 24, card_y + card_h - 88, "and run working simulators of pulse drilling, assist gas cutting, and kerf width.")
    
    # Step-by-step instructions
    steps2 = [
        ("01", "Scan to open the interactive laboratory brochure in your mobile or laptop browser."),
        ("02", "Select an apparatus and drag the explode slider to isolate subsystems in real time."),
        ("03", "Try working models: laser pulse drilling, assist gas nozzle CFD, and wobbling welding.")
    ]
    
    sy = card_y + card_h - 116
    for num, txt in steps2:
        c.setFont('Mono-Bold', 12)
        c.setFillColor(INK_DARK)
        c.drawString(x2 + 24, sy, num)
        c.setFont('Sans', 8.8)
        c.setFillColor(INK_DARK)
        c.drawString(x2 + 52, sy, txt)
        sy -= 22
        
    # Large Scannable QR Code 2
    qr_x2 = x2 + 24
    qr_y2 = sy - qr_size - 10
    if os.path.exists('qr_code_web.png'):
        c.drawImage('qr_code_web.png', qr_x2, qr_y2, qr_size, qr_size)
        
    # Information beside QR code
    ix2 = qr_x2 + qr_size + 24
    c.setFont('Mono-Bold', 9)
    c.setFillColor(INK_DARK)
    c.drawString(ix2, qr_y2 + 160, "INTERACTIVE MODULES")
    
    c.setFont('Sans-Bold', 8)
    c.setFillColor(ACCENT_CYAN)
    c.drawString(ix2, qr_y2 + 142, "• 3D Exploded View & Component Inspector")
    c.drawString(ix2, qr_y2 + 128, "• Laser Micro-Drilling Recast Calculator")
    c.drawString(ix2, qr_y2 + 114, "• Cutting Speed & Kerf Width Estimator")
    
    c.setFont('Mono-Bold', 8)
    c.setFillColor(INK_SLATE)
    c.drawString(ix2, qr_y2 + 90, "COMPATIBILITY")
    c.setFont('Sans', 7.5)
    c.setFillColor(INK_DARK)
    c.drawString(ix2, qr_y2 + 76, "Works in any modern web browser (Chrome, Safari, Edge, Firefox)")
    c.drawString(ix2, qr_y2 + 64, "Zero installation required · Fully responsive on mobile & tablet")
    
    # Fallback URL box
    c.setFillColor(HexColor('#FFFFFF'))
    c.roundRect(ix2, qr_y2 + 10, 290, 42, 3, fill=1, stroke=0)
    c.setFont('Mono-Bold', 7)
    c.setFillColor(ACCENT_RED)
    c.drawString(ix2 + 10, qr_y2 + 38, "OR TYPE DIRECTLY IN BROWSER:")
    c.setFont('Mono-Bold', 10.5)
    c.setFillColor(INK_DARK)
    c.drawString(ix2 + 10, qr_y2 + 20, "coep-laser-lab.github.io")
    
    # Web UI Preview Graphic underneath
    if os.path.exists('mockup_web.png'):
        c.drawImage('mockup_web.png', x2 + 24, mock_y, mock_w, mock_h)

    draw_title_block(c, "SCAN · STEP INSIDE", 4, scale="NTS",
                     note="Both QR codes encoded with Level H error correction (30% recovery) and verified before printing. Web app developed for COEP Tech Laser Lab.")
    c.showPage()

def build_pdf():
    output_filename = "Laser-Systems-Lab-Poster-Series-A3.pdf"
    print(f"Compiling 4-Sheet Engineering Poster Series to {output_filename}...")
    c = canvas.Canvas(output_filename, pagesize=landscape(A3))
    
    build_sheet_1(c)
    build_sheet_2(c)
    build_sheet_3(c)
    build_sheet_4(c)
    
    c.save()
    print(f"SUCCESS: {output_filename} generated perfectly!")

if __name__ == '__main__':
    build_pdf()
