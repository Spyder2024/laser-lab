import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

BG_COLOR = '#FAF8F0'
INK_DARK = '#1B2A44'
INK_SLATE = '#4E5A72'
ACCENT_RED = '#D23F29'
ACCENT_CYAN = '#1590BA'
ACCENT_ORANGE = '#E66A26'
PANEL_BG = '#F3EFE6'

def draw_callout(ax, num, px, py, cx, cy):
    ax.plot([px, cx], [py, cy], color=INK_DARK, lw=1.1, zorder=15)
    circle = plt.Circle((cx, cy), 2.2, facecolor=BG_COLOR, edgecolor=INK_DARK, lw=1.5, zorder=20)
    ax.add_patch(circle)
    ax.text(cx, cy, str(num), color=INK_DARK, fontsize=8, fontweight='bold', ha='center', va='center', zorder=25)

# --- 1A: Nd:YAG Resonator Cavity ---
def draw_fig1a():
    fig, ax = plt.subplots(figsize=(8.5, 5.2), dpi=300)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis('off')

    # Aluminum resonator rail / optical bench
    bench = patches.Polygon([[10, 12], [88, 12], [92, 18], [14, 18]], closed=True,
                            facecolor='#CBD5E1', edgecolor=INK_DARK, lw=1.8)
    bench_front = patches.Rectangle((10, 6), 78, 6, facecolor='#94A3B8', edgecolor=INK_DARK, lw=1.8)
    ax.add_patch(bench_front)
    ax.add_patch(bench)

    # 4: Rear Total Reflector Mirror Mount (100% HR @ 1064 nm)
    m1_base = patches.Rectangle((14, 16), 6, 12, facecolor='#475569', edgecolor=INK_DARK, lw=1.4)
    m1_mirror = patches.Rectangle((18, 22), 2.5, 16, facecolor='#0284C7', edgecolor=INK_DARK, lw=1.4)
    ax.add_patch(m1_base)
    ax.add_patch(m1_mirror)

    # 5: EO Q-Switch Crystal Assembly (Pockels Cell)
    qs_base = patches.Rectangle((26, 16), 8, 10, facecolor='#475569', edgecolor=INK_DARK, lw=1.4)
    qs_box = patches.Rectangle((27, 24), 10, 14, facecolor='#F59E0B', edgecolor=INK_DARK, lw=1.4)
    ax.add_patch(qs_base)
    ax.add_patch(qs_box)
    ax.text(32, 31, "Q-SWITCH", color=INK_DARK, fontsize=5.5, fontweight='bold', ha='center')

    # 6: Intra-Cavity Aperture / Polarizer
    ap_base = patches.Rectangle((41, 16), 5, 8, facecolor='#475569', edgecolor=INK_DARK, lw=1.4)
    ap_plate = patches.Rectangle((42.5, 23), 2, 14, facecolor='#1E293B', edgecolor=INK_DARK, lw=1.2)
    ax.add_patch(ap_base)
    ax.add_patch(ap_plate)

    # 2: Gold-Plated Elliptical Pump Chamber & 1: Nd:YAG Rod
    pump_chamber = patches.Rectangle((48, 20), 24, 20, facecolor='#E2E8F0', edgecolor=INK_DARK, lw=1.8)
    ax.add_patch(pump_chamber)
    # Coolant tubes
    ax.plot([52, 52], [40, 48], color=ACCENT_CYAN, lw=2)
    ax.plot([68, 68], [40, 48], color=ACCENT_CYAN, lw=2)
    ax.text(60, 36, "PUMP CHAMBER", color=INK_DARK, fontsize=6, fontweight='bold', ha='center')
    # Nd:YAG Crystal Rod (1)
    ax.plot([46, 74], [29, 29], color=ACCENT_RED, lw=4.5)
    ax.plot([46, 74], [29, 29], color='#FECACA', lw=1.8)
    # Flashlamp (2)
    ax.plot([50, 70], [24, 24], color='#FDE047', lw=3)

    # 3: Output Coupler (OC) Mirror Mount (T = 40%)
    m2_base = patches.Rectangle((76, 16), 6, 12, facecolor='#475569', edgecolor=INK_DARK, lw=1.4)
    m2_mirror = patches.Rectangle((78, 22), 2.5, 16, facecolor='#38BDF8', edgecolor=INK_DARK, lw=1.4)
    ax.add_patch(m2_base)
    ax.add_patch(m2_mirror)

    # Laser Beam exiting resonator
    ax.plot([19, 96], [29, 29], color=ACCENT_RED, lw=2, linestyle=':')
    ax.plot([80, 98], [29, 29], color=ACCENT_RED, lw=2.5)

    # Callouts (1 to 6)
    draw_callout(ax, 1, 60, 29, 60, 52)   # 1 Nd:YAG Rod
    draw_callout(ax, 2, 60, 24, 60, 10)   # 2 Flashlamp Pump Chamber
    draw_callout(ax, 3, 79, 30, 85, 48)   # 3 Output Coupler Mirror
    draw_callout(ax, 4, 19, 30, 14, 48)   # 4 Rear Total Reflector
    draw_callout(ax, 5, 32, 35, 32, 52)   # 5 EO Q-Switch
    draw_callout(ax, 6, 43, 33, 44, 10)   # 6 Polarizer & Aperture

    ax.text(50, 2, "FIG. 1A · Nd:YAG LASER RESONATOR CAVITY & PUMP CHAMBER",
            color=INK_DARK, fontsize=7.5, fontweight='bold', ha='center')

    plt.tight_layout()
    plt.savefig('fig_1a_resonator.png', dpi=300, facecolor=BG_COLOR)
    plt.close()

# --- 1B: 4-Axis CNC Gantry ---
def draw_fig1b():
    fig, ax = plt.subplots(figsize=(8.5, 5.2), dpi=300)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis('off')

    # 1: Synthetic Granite Machine Base
    base_top = patches.Polygon([[18, 14], [82, 14], [90, 23], [26, 23]], closed=True,
                               facecolor='#94A3B8', edgecolor=INK_DARK, lw=1.8)
    base_front = patches.Rectangle((18, 6), 64, 8, facecolor='#64748B', edgecolor=INK_DARK, lw=1.8)
    base_side = patches.Polygon([[82, 6], [90, 15], [90, 23], [82, 14]], closed=True,
                                facecolor='#475569', edgecolor=INK_DARK, lw=1.8)
    ax.add_patch(base_front)
    ax.add_patch(base_side)
    ax.add_patch(base_top)

    # 3: X-Axis Linear Motion Guide Rails
    ax.plot([23, 31], [15, 22], color=INK_DARK, lw=2.5)
    ax.plot([75, 83], [15, 22], color=INK_DARK, lw=2.5)

    # 5: Rotary Indexing Chuck (A-Axis) & Workpiece
    chuck = patches.Rectangle((42, 17), 10, 6, facecolor='#D97706', edgecolor=INK_DARK, lw=1.4)
    ax.add_patch(chuck)
    # Cylindrical workpiece
    ax.plot([52, 68], [20, 20], color='#FBBF24', lw=4.5)

    # Gantry Uprights & Crossbeam
    col_l = patches.Polygon([[25, 20], [29, 20], [29, 48], [25, 48]], closed=True,
                            facecolor='#334155', edgecolor=INK_DARK, lw=1.8)
    col_r = patches.Polygon([[77, 20], [81, 20], [81, 48], [77, 48]], closed=True,
                            facecolor='#334155', edgecolor=INK_DARK, lw=1.8)
    beam = patches.Polygon([[23, 45], [83, 45], [83, 52], [23, 52]], closed=True,
                           facecolor='#475569', edgecolor=INK_DARK, lw=1.8)
    ax.add_patch(col_l)
    ax.add_patch(col_r)
    ax.add_patch(beam)

    # 2: Y-Axis Precision Ballscrew & Z-Carriage
    ax.plot([26, 80], [48.5, 48.5], color=ACCENT_CYAN, lw=2, linestyle='--')
    z_slide = patches.Rectangle((48, 36), 12, 15, facecolor='#1E293B', edgecolor=INK_DARK, lw=1.5)
    ax.add_patch(z_slide)

    # 4: Coaxial Cutting Head & Supersonic Nozzle
    head = patches.Polygon([[52, 26], [56, 26], [55, 36], [53, 36]], closed=True,
                           facecolor='#E2E8F0', edgecolor=INK_DARK, lw=1.4)
    nozzle = patches.Polygon([[53, 21], [55, 21], [56, 26], [52, 26]], closed=True,
                             facecolor='#CBD5E1', edgecolor=INK_DARK, lw=1.4)
    ax.add_patch(head)
    ax.add_patch(nozzle)
    # Laser focus cone
    ax.plot([54, 54], [21, 20], color=ACCENT_RED, lw=2.5)
    ax.scatter([54], [20], color='#FFD700', s=70, zorder=12)

    # 6: Closed-Loop DI Water Chiller Unit beside gantry
    chiller = patches.Rectangle((6, 8), 9, 20, facecolor='#334155', edgecolor=INK_DARK, lw=1.6)
    ax.add_patch(chiller)
    ax.text(10.5, 24, "DI CHILLER", color='white', fontsize=4.8, fontweight='bold', ha='center')
    ax.plot([15, 23], [18, 18], color=ACCENT_CYAN, lw=1.5, linestyle=':')

    # Callouts (1 to 6)
    draw_callout(ax, 1, 50, 10, 50, 3)    # 1 Granite Base
    draw_callout(ax, 2, 65, 48.5, 68, 56) # 2 Ballscrews
    draw_callout(ax, 3, 27, 18, 20, 26)   # 3 Linear Guide Rails
    draw_callout(ax, 4, 54, 25, 42, 32)   # 4 Cutting Head & Nozzle
    draw_callout(ax, 5, 60, 20, 72, 26)   # 5 Rotary A-Axis Chuck
    draw_callout(ax, 6, 10.5, 14, 10.5, 33) # 6 DI Water Chiller

    ax.text(50, 0.8, "FIG. 1B · 4-AXIS CNC BRIDGE GANTRY & ROTARY AXIS",
            color=INK_DARK, fontsize=7.5, fontweight='bold', ha='center')

    plt.tight_layout()
    plt.savefig('fig_1b_gantry.png', dpi=300, facecolor=BG_COLOR)
    plt.close()

# --- 1C: Fiber Laser Engine ---
def draw_fig1c():
    fig, ax = plt.subplots(figsize=(8.5, 5.2), dpi=300)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis('off')

    # Main 19" Industrial Cabinet
    cab = patches.Rectangle((18, 8), 64, 44, facecolor='#1E293B', edgecolor=INK_DARK, lw=2)
    ax.add_patch(cab)

    # Rack module 1: DC Power & Diode Driver
    psu = patches.Rectangle((22, 38), 56, 10, facecolor='#334155', edgecolor=INK_DARK, lw=1.2)
    ax.add_patch(psu)
    ax.text(50, 43, "DC DIODE DRIVER & INTERLOCKS", color='#94A3B8', fontsize=6, fontweight='bold', ha='center')

    # Rack module 2: 3: 976 nm Pump Laser Diode Modules
    pumps = patches.Rectangle((22, 24), 26, 12, facecolor='#0F172A', edgecolor=INK_DARK, lw=1.2)
    ax.add_patch(pumps)
    for dy in [27, 30, 33]:
        ax.plot([25, 45], [dy, dy], color='#F59E0B', lw=1.5)
    ax.text(35, 25, "976 nm DIODES", color='#FBBF24', fontsize=5.5, ha='center')

    # 4: Fused Fiber Combiner
    comb = patches.Polygon([[49, 27], [55, 28], [55, 32], [49, 33]], closed=True,
                           facecolor='#0284C7', edgecolor=INK_DARK, lw=1)
    ax.add_patch(comb)

    # 1: Active Yb-Doped Double-Clad Fiber Spool & 2: FBGs
    spool = patches.Circle((66, 30), 6, facecolor='none', edgecolor=ACCENT_RED, lw=2.5)
    ax.add_patch(spool)
    # FBG marks
    ax.plot([58, 60], [30, 30], color='#A855F7', lw=3) # HR FBG
    ax.plot([72, 74], [30, 30], color='#A855F7', lw=3) # OC FBG

    # 5: Clad Mode Stripper (CMS)
    cms = patches.Rectangle((75, 28), 5, 4, facecolor='#64748B', edgecolor=INK_DARK, lw=1)
    ax.add_patch(cms)

    # 6: Armored QBH Cable Emerging from Cabinet
    t = np.linspace(0, 1, 40)
    cx = 82 + 12 * t
    cy = 30 + 10 * np.sin(np.pi * t)
    ax.plot(cx, cy, color='#EAB308', lw=4)
    ax.plot(cx, cy, color=INK_DARK, lw=1.5, linestyle='--')

    # Lower Rack: Control Interface & Display
    disp = patches.Rectangle((22, 12), 56, 10, facecolor='#0F172A', edgecolor=ACCENT_CYAN, lw=1.2)
    ax.add_patch(disp)
    ax.text(50, 17, "1070 nm Yb FIBER LASER · 1000 W CW", color=ACCENT_CYAN, fontsize=7, fontweight='bold', ha='center')

    # Callouts (1 to 6)
    draw_callout(ax, 1, 66, 36, 66, 48)   # 1 Yb Active Fiber
    draw_callout(ax, 2, 59, 30, 56, 18)   # 2 FBGs
    draw_callout(ax, 3, 35, 30, 35, 48)   # 3 976 nm Diodes
    draw_callout(ax, 4, 52, 30, 48, 48)   # 4 Combiner
    draw_callout(ax, 5, 77.5, 30, 80, 48) # 5 Clad Mode Stripper
    draw_callout(ax, 6, 88, 38, 92, 48)   # 6 QBH Cable

    ax.text(50, 2, "FIG. 1C · SINGLE-MODE Yb FIBER LASER ENGINE & PUMP MODULES",
            color=INK_DARK, fontsize=7.5, fontweight='bold', ha='center')

    plt.tight_layout()
    plt.savefig('fig_1c_fiber_engine.png', dpi=300, facecolor=BG_COLOR)
    plt.close()

# --- 1D: Galvo Scan Head & Optical Endstation ---
def draw_fig1d():
    fig, ax = plt.subplots(figsize=(8.5, 5.2), dpi=300)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis('off')

    # 1: QBH Fiber Receiver Socket & 2: Collimator Lens
    qbh = patches.Rectangle((18, 40), 10, 8, facecolor='#475569', edgecolor=INK_DARK, lw=1.4)
    collimator = patches.Rectangle((28, 39), 12, 10, facecolor='#64748B', edgecolor=INK_DARK, lw=1.4)
    ax.add_patch(qbh)
    ax.add_patch(collimator)
    # Yellow fiber entering
    ax.plot([8, 18], [44, 44], color='#EAB308', lw=4)

    # Collimated beam path
    ax.plot([40, 52], [44, 44], color=ACCENT_RED, lw=2, linestyle=':')

    # 3: X-Axis Galvo Mirror & 4: Y-Axis Galvo Mirror Housing
    galvo_housing = patches.Rectangle((46, 32), 22, 20, facecolor='#1E293B', edgecolor=INK_DARK, lw=1.8)
    ax.add_patch(galvo_housing)
    ax.text(57, 48, "GALVO HEAD", color='white', fontsize=6, fontweight='bold', ha='center')
    # Mirrors
    ax.plot([50, 54], [42, 46], color=ACCENT_CYAN, lw=3) # X mirror
    ax.plot([58, 62], [40, 36], color=ACCENT_CYAN, lw=3) # Y mirror

    # 5: Telecentric F-Theta Objective Lens
    ftheta = patches.Polygon([[50, 32], [66, 32], [64, 25], [52, 25]], closed=True,
                             facecolor='#0284C7', edgecolor=INK_DARK, lw=1.6)
    ax.add_patch(ftheta)

    # Focused Laser Beam Envelope
    cone = patches.Polygon([[54, 25], [62, 25], [58, 14]], closed=True,
                           facecolor=ACCENT_RED, alpha=0.35, edgecolor=ACCENT_RED, lw=1)
    ax.add_patch(cone)
    ax.scatter([58], [14], color='#FFD700', s=80, zorder=12)

    # Worktable surface & Honeycomb vacuum bed
    table = patches.Rectangle((30, 8), 56, 6, facecolor='#CBD5E1', edgecolor=INK_DARK, lw=1.6)
    ax.add_patch(table)

    # 6: Multi-Stage Fume Extractor Nozzle
    fume = patches.Rectangle((74, 16), 14, 8, facecolor='#475569', edgecolor=INK_DARK, lw=1.2)
    ax.add_patch(fume)
    ax.plot([74, 62], [20, 16], color='#94A3B8', lw=2, linestyle=':')

    # Callouts (1 to 6)
    draw_callout(ax, 1, 23, 44, 23, 54)   # 1 QBH Receiver
    draw_callout(ax, 2, 34, 44, 34, 54)   # 2 Collimator Lens
    draw_callout(ax, 3, 52, 44, 48, 55)   # 3 X-Galvo Mirror
    draw_callout(ax, 4, 60, 38, 68, 55)   # 4 Y-Galvo Mirror
    draw_callout(ax, 5, 58, 27, 44, 25)   # 5 F-Theta Lens
    draw_callout(ax, 6, 81, 20, 85, 28)   # 6 Fume Extractor

    ax.text(50, 1, "FIG. 1D · HIGH-SPEED GALVO SCAN HEAD & F-THETA OPTICS",
            color=INK_DARK, fontsize=7.5, fontweight='bold', ha='center')

    plt.tight_layout()
    plt.savefig('fig_1d_galvo_head.png', dpi=300, facecolor=BG_COLOR)
    plt.close()

if __name__ == '__main__':
    print("Generating 4 quadrant diagrams...")
    draw_fig1a()
    draw_fig1b()
    draw_fig1c()
    draw_fig1d()
    print("All 4 quadrant diagrams generated successfully!")
