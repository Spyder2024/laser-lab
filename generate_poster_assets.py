import os
import sys
sys.path.append(r'C:\Users\VISHESH-PC\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages')
import qrcode
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np
from PIL import Image

# Global color palette matching AR-VR sample document
BG_COLOR = '#FAF8F0'
INK_DARK = '#1B2A44'
INK_SLATE = '#4E5A72'
ACCENT_RED = '#D23F29'
ACCENT_CYAN = '#1590BA'
ACCENT_ORANGE = '#E66A26'
ACCENT_GREEN = '#2E7D32'
GRID_COLOR = '#E9E2D0'
PANEL_BG = '#F3EFE6'

# --- 1. QR CODES ---
def generate_qr_codes():
    print("Generating QR codes...")
    # QR Code for AR Explorer
    qr_ar = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=2)
    qr_ar.add_data('https://coep-laser-lab.github.io/ar')
    qr_ar.make(fit=True)
    img_ar = qr_ar.make_image(fill_color=ACCENT_RED, back_color=BG_COLOR).convert('RGBA')
    img_ar.save('qr_code_ar.png')

    # QR Code for Web Brochure & Simulator
    qr_web = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=2)
    qr_web.add_data('https://coep-laser-lab.github.io')
    qr_web.make(fit=True)
    img_web = qr_web.make_image(fill_color=INK_DARK, back_color=BG_COLOR).convert('RGBA')
    img_web.save('qr_code_web.png')

    # Mini QR code for headers
    qr_mini = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=1)
    qr_mini.add_data('https://coep-laser-lab.github.io')
    qr_mini.make(fit=True)
    img_mini = qr_mini.make_image(fill_color=INK_DARK, back_color=BG_COLOR).convert('RGBA')
    img_mini.save('qr_code_mini.png')
    print("QR codes saved successfully.")

# --- 2. FIG 1A: Nd:YAG PULSED LASER & 4-AXIS CNC GANTRY ---
def draw_fig1a_ndyag():
    print("Drawing FIG. 1A: Nd:YAG Gantry...")
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 65)
    ax.axis('off')

    # Isometric/Orthographic technical drawing of 4-axis gantry
    # Granite machine base
    granite = patches.Polygon([[15, 8], [75, 8], [85, 18], [25, 18]], closed=True, 
                              facecolor='#D9D2C5', edgecolor=INK_DARK, lw=1.8)
    granite_front = patches.Polygon([[15, 3], [75, 3], [75, 8], [15, 8]], closed=True,
                                    facecolor='#C2B9A7', edgecolor=INK_DARK, lw=1.8)
    granite_side = patches.Polygon([[75, 3], [85, 13], [85, 18], [75, 8]], closed=True,
                                   facecolor='#AFA591', edgecolor=INK_DARK, lw=1.8)
    ax.add_patch(granite_front)
    ax.add_patch(granite_side)
    ax.add_patch(granite)

    # Base guide rails (X-axis longitudinal)
    ax.plot([20, 30], [9, 17], color=INK_DARK, lw=2.5)
    ax.plot([68, 78], [9, 17], color=INK_DARK, lw=2.5)

    # 4th Axis Rotary Chuck & Workpiece (Part 6)
    chuck_base = patches.Rectangle((38, 12), 10, 5, facecolor='#637081', edgecolor=INK_DARK, lw=1.4)
    ax.add_patch(chuck_base)
    # Cylindrical workpiece in rotary chuck
    ax.plot([48, 62], [14.5, 14.5], color=ACCENT_ORANGE, lw=4.5)
    ax.plot([48, 62], [14.5, 14.5], color='#FFE0B2', lw=2)

    # Gantry upright columns & Y-axis cross beam (Part 5)
    left_col = patches.Polygon([[23, 14], [28, 14], [28, 42], [23, 42]], closed=True,
                               facecolor='#4A5568', edgecolor=INK_DARK, lw=1.8)
    right_col = patches.Polygon([[71, 14], [76, 14], [76, 42], [71, 42]], closed=True,
                                facecolor='#4A5568', edgecolor=INK_DARK, lw=1.8)
    cross_beam = patches.Polygon([[21, 40], [78, 40], [78, 47], [21, 47]], closed=True,
                                 facecolor='#718096', edgecolor=INK_DARK, lw=1.8)
    ax.add_patch(left_col)
    ax.add_patch(right_col)
    ax.add_patch(cross_beam)

    # Y-axis motion guide linear rail
    ax.plot([23, 76], [43.5, 43.5], color=ACCENT_CYAN, lw=2, linestyle='--')

    # Z-axis vertical carriage & ram (Part 5 / 6)
    z_carriage = patches.Rectangle((44, 34), 10, 14, facecolor='#2D3748', edgecolor=INK_DARK, lw=1.6)
    ax.add_patch(z_carriage)

    # Nd:YAG Laser Resonator Head on Top Bridge (Part 1, 2, 3)
    resonator_box = patches.Rectangle((28, 49), 42, 10, facecolor='#2B6CB0', edgecolor=INK_DARK, lw=2)
    ax.add_patch(resonator_box)
    ax.text(49, 54, "Nd:YAG RESONATOR CAVITY (1064 nm)", color='white', fontsize=7, fontweight='bold', ha='center')

    # Internal resonator components: Flashlamp chamber & Nd:YAG rod (1)
    ax.plot([30, 44], [52, 52], color='#E2E8F0', lw=3)
    ax.plot([32, 42], [52, 52], color=ACCENT_RED, lw=1.5)
    # Q-Switch EO crystal (2)
    qswitch = patches.Rectangle((46, 50.5), 5, 3, facecolor='#F6E05E', edgecolor=INK_DARK, lw=1.2)
    ax.add_patch(qswitch)
    ax.text(48.5, 52, "Q", color=INK_DARK, fontsize=6, fontweight='bold', ha='center', va='center')
    # Beam Expanding Telescope (3)
    bet = patches.Polygon([[53, 50.5], [59, 49.5], [59, 54.5], [53, 53.5]], closed=True,
                          facecolor='#90CDF4', edgecolor=INK_DARK, lw=1.2)
    ax.add_patch(bet)
    # Turning mirror block (4)
    ax.plot([62, 66], [49.5, 53.5], color=ACCENT_CYAN, lw=3)

    # Cutting & Focusing Head Assembly (Part 5 / Coaxial Nozzle)
    laser_head = patches.Polygon([[47, 24], [51, 24], [50, 34], [48, 34]], closed=True,
                                 facecolor='#E2E8F0', edgecolor=INK_DARK, lw=1.5)
    nozzle = patches.Polygon([[48.2, 19], [49.8, 19], [51, 24], [47, 24]], closed=True,
                             facecolor='#CBD5E0', edgecolor=INK_DARK, lw=1.5)
    ax.add_patch(laser_head)
    ax.add_patch(nozzle)

    # Laser Beam Path (Coherent 1064 nm in International Red)
    ax.plot([64, 49], [51.5, 51.5], color=ACCENT_RED, lw=2, linestyle=':')
    ax.plot([49, 49], [51.5, 23], color=ACCENT_RED, lw=2)
    # Focused beam cone striking workpiece
    ax.plot([49, 49], [19, 14.5], color=ACCENT_RED, lw=2.5)
    # Spark at impingement point
    ax.scatter([49], [14.5], color='#FFD700', s=90, zorder=10)

    # Assist gas line & Solenoid feed
    ax.plot([51, 55], [26, 26], color='#4A5568', lw=1.8)
    ax.plot([55, 55], [26, 38], color='#4A5568', lw=1.8)

    # Closed-Loop Chiller Unit (Part 7) beside machine
    chiller = patches.Rectangle((3, 6), 9, 18, facecolor='#4A5568', edgecolor=INK_DARK, lw=1.6)
    ax.add_patch(chiller)
    ax.text(7.5, 20, "DI WATER", color='white', fontsize=5.5, fontweight='bold', ha='center')
    ax.text(7.5, 17, "CHILLER", color='white', fontsize=5.5, fontweight='bold', ha='center')
    # Chiller hoses to resonator
    ax.plot([12, 18, 18, 28], [15, 15, 48, 48], color=ACCENT_CYAN, lw=1.5, linestyle='--')
    ax.plot([12, 16, 16, 28], [13, 13, 46, 46], color='#3182CE', lw=1.5, linestyle='--')

    # CNC Control Console (Part 8)
    cnc_stand = patches.Rectangle((83, 6), 12, 22, facecolor='#2D3748', edgecolor=INK_DARK, lw=1.6)
    ax.add_patch(cnc_stand)
    screen = patches.Rectangle((85, 18), 8, 8, facecolor='#1A202C', edgecolor=ACCENT_CYAN, lw=1.2)
    ax.add_patch(screen)
    ax.text(89, 22, "CNC 4-AXIS", color=ACCENT_CYAN, fontsize=4.8, fontweight='bold', ha='center')
    ax.text(89, 20, "G-CODE SYNC", color='#68D391', fontsize=4.2, ha='center')

    # Numbered Callout Badges (1 to 8)
    callouts = [
        (1, 35, 56, 35, 61),   # 1 Resonator & Nd:YAG rod
        (2, 48.5, 54, 48.5, 61),# 2 Q-Switch
        (3, 56, 55, 58, 61),   # 3 Beam Expanding Telescope
        (4, 65, 52, 70, 57),   # 4 Dielectric Turning Mirrors
        (5, 47, 21, 36, 23),   # 5 Assist Gas Cutting Head & Nozzle
        (6, 60, 14.5, 65, 10), # 6 4-Axis CNC Gantry & Rotary Chuck
        (7, 7.5, 14, 7.5, 27), # 7 DI Water Chiller
        (8, 89, 14, 89, 31)    # 8 CNC Controller Console
    ]

    for num, px, py, cx, cy in callouts:
        ax.plot([px, cx], [py, cy], color=INK_DARK, lw=1, linestyle='-', zorder=12)
        circle = plt.Circle((cx, cy), 1.8, facecolor=BG_COLOR, edgecolor=INK_DARK, lw=1.4, zorder=15)
        ax.add_patch(circle)
        ax.text(cx, cy, str(num), color=INK_DARK, fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=16)

    # Caption Box
    ax.text(50, 1.5, "FIG. 1A · Nd:YAG PULSE LASER & 4-AXIS CNC GANTRY SYSTEM", 
            color=INK_DARK, fontsize=8, fontweight='bold', ha='center')

    plt.tight_layout()
    plt.savefig('fig_1a_ndyag_gantry.png', dpi=300, facecolor=BG_COLOR)
    plt.close()
    print("FIG. 1A saved successfully.")

# --- 3. FIG 1B: INDUSTRIAL FIBER LASER SYSTEM ---
def draw_fig1b_fiber():
    print("Drawing FIG. 1B: Fiber Laser System...")
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 65)
    ax.axis('off')

    # Central 19" Rack: Yb Fiber Laser Engine & DC Power Supply (Part 1 & 8)
    rack = patches.Rectangle((12, 10), 22, 42, facecolor='#2D3748', edgecolor=INK_DARK, lw=2)
    ax.add_patch(rack)
    # Louvers / vents
    for vy in range(14, 26, 3):
        ax.plot([15, 31], [vy, vy], color='#718096', lw=1.2)
    # Laser source module display
    rack_disp = patches.Rectangle((15, 38), 16, 10, facecolor='#1A202C', edgecolor=ACCENT_CYAN, lw=1.4)
    ax.add_patch(rack_disp)
    ax.text(23, 44, "Yb FIBER LASER", color=ACCENT_CYAN, fontsize=7, fontweight='bold', ha='center')
    ax.text(23, 41, "1070 nm · 1000 W CW", color='#68D391', fontsize=6, ha='center')
    ax.text(23, 30, "PUMP DIODES (976 nm)", color='#E2E8F0', fontsize=5.5, ha='center')

    # Armored QBH Optical Fiber Delivery Cable (Part 2)
    # Curving yellow/black armored conduit
    t = np.linspace(0, 1, 50)
    cable_x = 34 + 20 * t + 8 * np.sin(np.pi * t)
    cable_y = 45 + 5 * np.cos(np.pi * t) - 8 * t
    ax.plot(cable_x, cable_y, color='#ECC94B', lw=4)
    ax.plot(cable_x, cable_y, color=INK_DARK, lw=1.5, linestyle='--')

    # Collimator & High-Speed Dual-Galvo Scan Head (Part 3 & 4)
    collimator = patches.Rectangle((58, 41), 8, 6, facecolor='#718096', edgecolor=INK_DARK, lw=1.4)
    galvo_housing = patches.Rectangle((66, 37), 16, 14, facecolor='#4A5568', edgecolor=INK_DARK, lw=1.8)
    ax.add_patch(collimator)
    ax.add_patch(galvo_housing)
    ax.text(74, 46, "GALVO SCAN HEAD", color='white', fontsize=6.5, fontweight='bold', ha='center')
    # Galvo mirrors inside housing
    ax.plot([69, 72], [42, 45], color=ACCENT_CYAN, lw=2.5) # X mirror
    ax.plot([75, 78], [44, 41], color=ACCENT_CYAN, lw=2.5) # Y mirror

    # Telecentric F-Theta Objective Lens (Part 5)
    ftheta = patches.Polygon([[68, 37], [80, 37], [78, 31], [70, 31]], closed=True,
                             facecolor='#63B3ED', edgecolor=INK_DARK, lw=1.6)
    ax.add_patch(ftheta)
    ax.text(74, 34, "F-THETA LENS", color=INK_DARK, fontsize=5.5, fontweight='bold', ha='center')

    # Focused Laser Beam Cone onto workpiece
    beam_cone = patches.Polygon([[71, 31], [77, 31], [74, 18]], closed=True,
                                facecolor=ACCENT_RED, alpha=0.35, edgecolor=ACCENT_RED, lw=1)
    ax.add_patch(beam_cone)
    ax.plot([74, 74], [31, 18], color=ACCENT_RED, lw=2)
    # Focal spot spark on bed
    ax.scatter([74], [18], color='#FFD700', s=80, zorder=10)

    # Precision Honeycomb Worktable & X-Y Translation Stage (Part 6)
    table_top = patches.Polygon([[50, 14], [94, 14], [98, 20], [54, 20]], closed=True,
                                facecolor='#E2E8F0', edgecolor=INK_DARK, lw=1.8)
    table_base = patches.Rectangle((54, 5), 38, 9, facecolor='#CBD5E0', edgecolor=INK_DARK, lw=1.8)
    ax.add_patch(table_base)
    ax.add_patch(table_top)
    # Honeycomb grid pattern
    for hx in range(58, 92, 5):
        ax.plot([hx, hx + 3], [15, 19], color='#A0AEC0', lw=1, linestyle=':')

    # Multi-Stage Fume Extractor Unit (Part 7)
    fume_unit = patches.Rectangle((40, 5), 11, 18, facecolor='#4A5568', edgecolor=INK_DARK, lw=1.6)
    ax.add_patch(fume_unit)
    ax.text(45.5, 16, "HEPA / CARBON", color='white', fontsize=4.8, fontweight='bold', ha='center')
    ax.text(45.5, 13, "FUME FILTER", color='white', fontsize=4.8, fontweight='bold', ha='center')
    # Exhaust flex hose to workpiece
    ax.plot([48, 56, 68], [21, 25, 19], color='#718096', lw=3, linestyle=':')

    # Numbered Callout Badges (1 to 8)
    callouts_b = [
        (1, 23, 46, 23, 56),    # 1 Active Yb-Doped Fiber Resonator
        (2, 45, 43, 45, 54),    # 2 Armored QBH Cable
        (3, 62, 44, 62, 56),    # 3 Collimator Module
        (4, 74, 48, 74, 57),    # 4 Dual-Galvo Scan Head
        (5, 76, 33, 85, 36),    # 5 Telecentric F-Theta Lens
        (6, 82, 17, 88, 11),    # 6 Honeycomb Table & Stage
        (7, 45.5, 10, 45.5, 2), # 7 Fume Extractor
        (8, 23, 16, 23, 4)      # 8 Central Control Rack & Supply
    ]

    for num, px, py, cx, cy in callouts_b:
        ax.plot([px, cx], [py, cy], color=INK_DARK, lw=1, linestyle='-', zorder=12)
        circle = plt.Circle((cx, cy), 1.8, facecolor=BG_COLOR, edgecolor=INK_DARK, lw=1.4, zorder=15)
        ax.add_patch(circle)
        ax.text(cx, cy, str(num), color=INK_DARK, fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=16)

    # Caption Box
    ax.text(50, 1.5, "FIG. 1B · HIGH-POWER FIBER LASER APPARATUS & GALVO SCAN HEAD", 
            color=INK_DARK, fontsize=8, fontweight='bold', ha='center')

    plt.tight_layout()
    plt.savefig('fig_1b_fiber_laser.png', dpi=300, facecolor=BG_COLOR)
    plt.close()
    print("FIG. 1B saved successfully.")

# --- 4. SHEET 2 RESEARCH PROJECT SCHEMATICS ---
def draw_research_projects():
    print("Drawing Sheet 2 Research Project Panels...")
    # Project 1: Micro-drilling hole cross section
    fig, ax = plt.subplots(figsize=(4.5, 3.2), dpi=250)
    fig.patch.set_facecolor(PANEL_BG)
    ax.set_facecolor(PANEL_BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    # Metal substrate
    sub = patches.Polygon([[1, 1], [9, 1], [9, 7], [6.5, 7], [5.8, 2], [4.2, 2], [3.5, 7], [1, 7]],
                          closed=True, facecolor='#A0AEC0', edgecolor=INK_DARK, lw=1.5)
    ax.add_patch(sub)
    # Recast layer along hole walls
    ax.plot([3.5, 4.2], [7, 2], color=ACCENT_RED, lw=2.5)
    ax.plot([6.5, 5.8], [7, 2], color=ACCENT_RED, lw=2.5)
    # Laser beam and assist gas
    ax.plot([5, 5], [9.5, 2], color=ACCENT_RED, lw=2, linestyle='-')
    ax.scatter([5], [2], color='#FFD700', s=60)
    ax.text(5, 0.5, "Inconel 718 Hole Profile (Recast < 12 µm)", color=INK_DARK, fontsize=7, ha='center', fontweight='bold')
    plt.tight_layout()
    plt.savefig('res_1_drilling.png', dpi=250, facecolor=PANEL_BG)
    plt.close()

    # Project 2: Surface texturing dimples & contact angle
    fig, ax = plt.subplots(figsize=(4.5, 3.2), dpi=250)
    fig.patch.set_facecolor(PANEL_BG)
    ax.set_facecolor(PANEL_BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    # Titanium substrate with dimples
    ax.plot([1, 9], [3, 3], color=INK_DARK, lw=2)
    for x in np.linspace(2, 8, 9):
        arc = patches.Arc((x, 3), 0.5, 0.4, angle=0, theta1=180, theta2=360, color=ACCENT_CYAN, lw=1.8)
        ax.add_patch(arc)
    # Water droplet (Superhydrophobic sphere)
    droplet = patches.Circle((5, 5.2), 2.1, facecolor='#63B3ED', alpha=0.8, edgecolor='#2B6CB0', lw=1.5)
    ax.add_patch(droplet)
    ax.text(5, 8.2, "Contact Angle θ = 154°", color=INK_DARK, fontsize=7, ha='center', fontweight='bold')
    ax.text(5, 0.5, "Superhydrophobic Ti-6Al-4V Surface", color=INK_DARK, fontsize=7, ha='center')
    plt.tight_layout()
    plt.savefig('res_2_texturing.png', dpi=250, facecolor=PANEL_BG)
    plt.close()

    # Project 3: Cu-Al Dissimilar Welding & Wobble
    fig, ax = plt.subplots(figsize=(4.5, 3.2), dpi=250)
    fig.patch.set_facecolor(PANEL_BG)
    ax.set_facecolor(PANEL_BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    # Copper sheet (top) & Aluminum sheet (bottom)
    cu = patches.Rectangle((1.5, 4.5), 7, 1.5, facecolor='#ED8936', edgecolor=INK_DARK, lw=1.2)
    al = patches.Rectangle((1.5, 2.5), 7, 1.5, facecolor='#CBD5E0', edgecolor=INK_DARK, lw=1.2)
    ax.add_patch(cu)
    ax.add_patch(al)
    ax.text(2.2, 5.2, "Cu (0.3 mm)", color='white', fontsize=6, fontweight='bold')
    ax.text(2.2, 3.2, "Al (0.5 mm)", color=INK_DARK, fontsize=6, fontweight='bold')
    # Weld nugget with circular wobble pattern
    theta = np.linspace(0, 8*np.pi, 200)
    wx = 5 + 1.2 * np.cos(theta) + 0.1 * theta
    wy = 4 + 0.6 * np.sin(theta)
    ax.plot(wx, wy, color=ACCENT_RED, lw=1.5)
    ax.text(5, 8.2, "Circular Wobble Trajectory (400 Hz)", color=ACCENT_RED, fontsize=7, ha='center', fontweight='bold')
    ax.text(5, 0.5, "Lap Shear Strength > 850 N", color=INK_DARK, fontsize=7, ha='center')
    plt.tight_layout()
    plt.savefig('res_3_welding.png', dpi=250, facecolor=PANEL_BG)
    plt.close()

    # Project 4: Shack-Hartmann Wavefront Sensing
    fig, ax = plt.subplots(figsize=(4.5, 3.2), dpi=250)
    fig.patch.set_facecolor(PANEL_BG)
    ax.set_facecolor(PANEL_BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    # Wavefront contour grid
    for gx in range(2, 9):
        for gy in range(2, 9):
            ax.scatter([gx], [gy], color='#CBD5E0', s=15)
            # distorted vs corrected spots
            dx = (gx - 5) * 0.12
            dy = (gy - 5) * 0.12
            ax.scatter([gx + dx], [gy + dy], color=ACCENT_RED, s=20)
    ax.text(5, 9.2, "Wavefront Aberration Map", color=INK_DARK, fontsize=7, ha='center', fontweight='bold')
    ax.text(5, 0.5, "In-Situ Thermal Lensing Correction", color=INK_DARK, fontsize=7, ha='center')
    plt.tight_layout()
    plt.savefig('res_4_wavefront.png', dpi=250, facecolor=PANEL_BG)
    plt.close()

    # Project 5: Supersonic Laval Nozzle Gas Flow
    fig, ax = plt.subplots(figsize=(4.5, 3.2), dpi=250)
    fig.patch.set_facecolor(PANEL_BG)
    ax.set_facecolor(PANEL_BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    # Nozzle contour (convergent-divergent)
    ax.plot([2, 4, 6, 8], [8, 6, 6, 8], color=INK_DARK, lw=2)
    ax.plot([2, 4, 6, 8], [2, 4, 4, 2], color=INK_DARK, lw=2)
    # Shock diamonds
    diamonds = [[4.5, 5], [5.5, 5], [6.5, 5]]
    for cx, cy in diamonds:
        d = patches.Polygon([[cx-0.4, cy], [cx, cy+0.6], [cx+0.4, cy], [cx, cy-0.6]], 
                            closed=True, facecolor='#ECC94B', edgecolor=ACCENT_ORANGE, lw=1)
        ax.add_patch(d)
    ax.text(5, 8.8, "Mach 2.2 Supersonic Core", color=ACCENT_RED, fontsize=7, ha='center', fontweight='bold')
    ax.text(5, 0.5, "CFD Melt Ejection Velocity > 320 m/s", color=INK_DARK, fontsize=7, ha='center')
    plt.tight_layout()
    plt.savefig('res_5_cfd.png', dpi=250, facecolor=PANEL_BG)
    plt.close()

    # Project 6: CNC G-Code & Pulse Sync
    fig, ax = plt.subplots(figsize=(4.5, 3.2), dpi=250)
    fig.patch.set_facecolor(PANEL_BG)
    ax.set_facecolor(PANEL_BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    # Motion clock waveform & laser pulse gating
    time = np.linspace(1, 9, 300)
    gantry_pos = 2 + 0.6 * time
    ax.plot(time, gantry_pos, color=ACCENT_CYAN, lw=2, label="CNC Position")
    # Gated pulse train
    pulse_y = [7 if int(t*4) % 2 == 0 else 5.5 for t in time]
    ax.step(time, pulse_y, color=ACCENT_RED, lw=1.5, label="Laser Gate")
    ax.text(5, 8.8, "G-Code Position-Synchronized Output (PSO)", color=INK_DARK, fontsize=6.8, ha='center', fontweight='bold')
    ax.text(5, 0.5, "Deterministic Pulse Pitch at 200 mm/s", color=INK_DARK, fontsize=7, ha='center')
    plt.tight_layout()
    plt.savefig('res_6_sync.png', dpi=250, facecolor=PANEL_BG)
    plt.close()
    print("Research project graphics saved.")

# --- 5. SHEET 4 3D / AR & WEB MOCKUPS ---
def draw_sheet4_mockups():
    print("Drawing Sheet 4 Mockups...")
    # AR Model View Mockup
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=250)
    fig.patch.set_facecolor(PANEL_BG)
    ax.set_facecolor(PANEL_BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    # Table plane
    ax.plot([1, 9], [1.5, 1.5], color='#CBD5E0', lw=2)
    # Phone frame
    phone = patches.FancyBboxPatch((2.5, 0.8), 5, 4.8, boxstyle="round,pad=0.2", 
                                   facecolor='#1A202C', edgecolor=INK_DARK, lw=2)
    ax.add_patch(phone)
    screen = patches.Rectangle((2.7, 1.1), 4.6, 4.2, facecolor='#2D3748', edgecolor='none')
    ax.add_patch(screen)
    # AR 3D model representation on screen
    ax.plot([3.5, 6.5], [2.2, 2.2], color='#4A5568', lw=3)
    ax.plot([4, 6], [3.2, 3.2], color=ACCENT_CYAN, lw=4)
    ax.plot([5, 5], [3.2, 2.2], color=ACCENT_RED, lw=2)
    ax.text(5, 4.7, "AR VIEWPORT · 1:1 SCALE", color='white', fontsize=6, fontweight='bold', ha='center')
    ax.text(5, 1.4, "[ EXPLODED VIEW ]", color=ACCENT_ORANGE, fontsize=5.5, ha='center')
    plt.tight_layout()
    plt.savefig('mockup_ar.png', dpi=250, facecolor=PANEL_BG)
    plt.close()

    # Web Brochure Mockup
    fig, ax = plt.subplots(figsize=(6, 3.5), dpi=250)
    fig.patch.set_facecolor(PANEL_BG)
    ax.set_facecolor(PANEL_BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    # Browser window
    browser = patches.FancyBboxPatch((1, 0.8), 8, 4.8, boxstyle="round,pad=0.1",
                                    facecolor='#FFFFFF', edgecolor=INK_DARK, lw=1.8)
    ax.add_patch(browser)
    # Browser top bar
    bar = patches.Rectangle((1, 5.0), 8, 0.6, facecolor='#EDF2F7', edgecolor=INK_DARK, lw=1)
    ax.add_patch(bar)
    for bx in [1.4, 1.8, 2.2]:
        ax.scatter([bx], [5.3], color='#A0AEC0', s=15)
    ax.text(5, 5.3, "coep-laser-lab.github.io", color='#4A5568', fontsize=5.5, ha='center', va='center')
    # Interactive UI elements
    slider_bar = patches.Rectangle((2, 1.5), 6, 0.3, facecolor='#E2E8F0', edgecolor='none')
    ax.add_patch(slider_bar)
    slider_knob = patches.Circle((4.5, 1.65), 0.35, facecolor=ACCENT_RED, edgecolor=INK_DARK, lw=1)
    ax.add_patch(slider_knob)
    ax.text(5, 2.2, "Explode Slider: 45%", color=INK_DARK, fontsize=5.5, fontweight='bold', ha='center')
    ax.text(5, 3.5, "Interactive 3D Resonator & Galvo Model", color='#2B6CB0', fontsize=6, fontweight='bold', ha='center')
    plt.tight_layout()
    plt.savefig('mockup_web.png', dpi=250, facecolor=PANEL_BG)
    plt.close()
    print("Mockups saved successfully.")

if __name__ == '__main__':
    generate_qr_codes()
    draw_fig1a_ndyag()
    draw_fig1b_fiber()
    draw_research_projects()
    draw_sheet4_mockups()
    print("All graphic assets successfully created!")
