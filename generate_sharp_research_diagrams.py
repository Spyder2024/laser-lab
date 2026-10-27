import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Exact palette matching the poster vellum and white card
BG_WHITE = '#FFFFFF'
INK_NAVY = '#1B2A44'
INK_SLATE = '#4E5A72'
ACCENT_RED = '#D13F29'
ACCENT_CYAN = '#1590B9'
ACCENT_ORANGE = '#E66A26'
ACCENT_GREEN = '#1F8A4C'
BORDER_COLOR = '#C8BFA8'

FIG_SIZE = (8.0, 2.05)
DPI = 300

def create_base_fig():
    fig, ax = plt.subplots(figsize=FIG_SIZE, dpi=DPI)
    fig.patch.set_facecolor(BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 25)
    ax.axis('off')
    return fig, ax

# ==============================================================================
# 1. res_1_drilling.png: Effusion Cooling Hole Cross-Section Profile
# ==============================================================================
def draw_res_1():
    fig, ax = create_base_fig()
    
    # Substrate Metal Plate (Inconel 718)
    sub_left = patches.Polygon([[8, 4], [38, 4], [34, 21], [8, 21]], closed=True, 
                               facecolor='#94A3B8', edgecolor=INK_NAVY, lw=1.5)
    sub_right = patches.Polygon([[44, 4], [74, 4], [74, 21], [48, 21]], closed=True,
                                facecolor='#94A3B8', edgecolor=INK_NAVY, lw=1.5)
    ax.add_patch(sub_left)
    ax.add_patch(sub_right)
    
    # Hatching lines inside metal
    for y in np.linspace(6, 19, 6):
        ax.plot([10, 31], [y, y], color='#64748B', lw=0.75, linestyle=':')
        ax.plot([51, 72], [y, y], color='#64748B', lw=0.75, linestyle=':')

    # Angled 25° hole profile walls (Recast layer in red)
    ax.plot([34, 38], [21, 4], color=ACCENT_RED, lw=3.0, solid_capstyle='round')
    ax.plot([48, 44], [21, 4], color=ACCENT_RED, lw=3.0, solid_capstyle='round')

    # Laser Beam Cone
    beam = patches.Polygon([[39, 25], [43, 25], [41.5, 4], [40.5, 4]], closed=True,
                           facecolor=ACCENT_RED, alpha=0.35, edgecolor=ACCENT_RED, lw=1.2)
    ax.add_patch(beam)
    ax.plot([41, 41], [25, 4], color='#FF2A15', lw=2.0)

    # Assist Gas Vectors (Coaxial N2)
    for gx in [36, 46]:
        ax.annotate('', xy=(gx + 1, 14), xytext=(gx, 23),
                    arrowprops=dict(arrowstyle="->", color=ACCENT_CYAN, lw=1.5))

    # Focal plasma spark
    ax.scatter([41], [4], color='#F59E0B', s=70, zorder=5)
    ax.scatter([41], [4], color='#FFFFFF', s=25, zorder=6)

    # Right Side: Technical Metrology Box
    m_box = patches.FancyBboxPatch((78, 3), 19, 19, boxstyle="round,pad=0.5",
                                   facecolor='#F8FAFC', edgecolor=BORDER_COLOR, lw=1.2)
    ax.add_patch(m_box)
    ax.text(87.5, 18.5, "METROLOGY DATA", color=INK_NAVY, fontsize=7.5, fontweight='bold', ha='center', family='sans-serif')
    ax.plot([80, 95], [16.5, 16.5], color=BORDER_COLOR, lw=0.8)
    ax.text(80, 13.5, "• Recast Layer: < 12 µm", color=ACCENT_RED, fontsize=6.8, fontweight='bold', family='monospace')
    ax.text(80, 10.0, "• Aspect Ratio: > 20 : 1", color=INK_NAVY, fontsize=6.8, family='monospace')
    ax.text(80, 6.5,  "• Hole Taper:  0.8°", color=INK_NAVY, fontsize=6.8, family='monospace')

    # Left Annotations
    ax.text(41, 23.5, "1064 nm Laser Beam + 14 bar Coaxial N₂", color=ACCENT_RED, fontsize=7.2, fontweight='bold', ha='center', family='sans-serif')
    ax.text(21, 2.0, "Inconel 718 Substrate (2.5 mm)", color=INK_SLATE, fontsize=6.5, ha='center', family='sans-serif')
    ax.text(41, 1.8, "Effusion Hole Profile", color=INK_NAVY, fontsize=7.2, fontweight='bold', ha='center', family='sans-serif')

    plt.tight_layout()
    plt.savefig('res_1_drilling.png', dpi=DPI, facecolor=BG_WHITE)
    plt.close()
    print("res_1_drilling.png generated.")

# ==============================================================================
# 2. res_2_texturing.png: Superhydrophobic Sessile Water Droplet (Cassie-Baxter)
# ==============================================================================
def draw_res_2():
    fig, ax = create_base_fig()

    # Titanium Substrate
    sub = patches.Rectangle((8, 3), 64, 4, facecolor='#94A3B8', edgecolor=INK_NAVY, lw=1.5)
    ax.add_patch(sub)

    # Periodic Laser-Etched Micro-Dimples along top of substrate
    for x in np.linspace(14, 66, 18):
        arc = patches.Arc((x, 7), 1.6, 1.2, angle=0, theta1=180, theta2=360, color=ACCENT_CYAN, lw=1.8)
        ax.add_patch(arc)
        # Air pockets underneath in cyan
        ax.plot([x - 0.7, x + 0.7], [7, 7], color=ACCENT_CYAN, lw=1.0, linestyle='--')

    # Sessile Water Droplet (Spherical Cap with Contact Angle > 154°)
    theta = np.linspace(0, 2*np.pi, 200)
    drop_x = 40 + 7.5 * np.cos(theta)
    drop_y = 14 + 7.5 * np.sin(theta)
    # Clip bottom slightly
    ax.fill(drop_x, np.maximum(drop_y, 7), facecolor='#38BDF8', alpha=0.85, edgecolor=ACCENT_CYAN, lw=2.0)

    # Tangent contact angle line at baseline contact point
    ax.plot([33, 27], [7, 18], color=ACCENT_RED, lw=2.0, linestyle='-')
    ax.plot([33, 20], [7, 7], color=INK_NAVY, lw=1.2, linestyle=':')
    
    # Contact angle arc
    arc_ca = patches.Arc((33, 7), 7, 7, angle=0, theta1=0, theta2=154, color=ACCENT_RED, lw=1.8)
    ax.add_patch(arc_ca)
    ax.text(28, 12, "θ = 154°", color=ACCENT_RED, fontsize=8.0, fontweight='bold', family='sans-serif')

    # Right Side: Metrology Box
    m_box = patches.FancyBboxPatch((78, 3), 19, 19, boxstyle="round,pad=0.5",
                                   facecolor='#F8FAFC', edgecolor=BORDER_COLOR, lw=1.2)
    ax.add_patch(m_box)
    ax.text(87.5, 18.5, "SURFACE WETTABILITY", color=INK_NAVY, fontsize=7.2, fontweight='bold', ha='center', family='sans-serif')
    ax.plot([80, 95], [16.5, 16.5], color=BORDER_COLOR, lw=0.8)
    ax.text(80, 13.5, "• State: Cassie-Baxter", color=ACCENT_CYAN, fontsize=6.6, fontweight='bold', family='monospace')
    ax.text(80, 10.0, "• Dimple Pitch: 35 µm", color=INK_NAVY, fontsize=6.6, family='monospace')
    ax.text(80, 6.5,  "• Bacteria Repel: 85%", color=ACCENT_GREEN, fontsize=6.6, fontweight='bold', family='monospace')

    # Center Labels
    ax.text(40, 22.5, "Cassie-Baxter Superhydrophobic State on Ti-6Al-4V", color=INK_NAVY, fontsize=7.5, fontweight='bold', ha='center', family='sans-serif')
    ax.text(40, 14.5, "Water Droplet (θ = 154°)", color='#0F172A', fontsize=7.0, fontweight='bold', ha='center', family='sans-serif')
    ax.text(40, 1.5, "Galvanometer Vector Scanning at 2,500 mm/s", color=INK_SLATE, fontsize=6.5, ha='center', family='sans-serif')

    plt.tight_layout()
    plt.savefig('res_2_texturing.png', dpi=DPI, facecolor=BG_WHITE)
    plt.close()
    print("res_2_texturing.png generated.")

# ==============================================================================
# 3. res_3_welding.png: Cu-Al Dissimilar Welding with 400 Hz Beam Wobble
# ==============================================================================
def draw_res_3():
    fig, ax = create_base_fig()

    # Top Sheet: Pure Copper (0.3 mm) in rich polished orange/copper
    cu_sheet = patches.Rectangle((8, 12), 64, 5, facecolor='#ED8936', edgecolor='#C05621', lw=1.5)
    ax.add_patch(cu_sheet)
    ax.text(12, 14.2, "Cu (0.3 mm) Pure Copper", color='#FFFFFF', fontsize=7.0, fontweight='bold', family='sans-serif')

    # Bottom Sheet: Aluminum (0.5 mm) in silver/gray
    al_sheet = patches.Rectangle((8, 6), 64, 5, facecolor='#CBD5E1', edgecolor='#64748B', lw=1.5)
    ax.add_patch(al_sheet)
    ax.text(12, 8.2, "Al (0.5 mm) Aluminum Sheet", color=INK_NAVY, fontsize=7.0, fontweight='bold', family='sans-serif')

    # Weld Interface Seam
    ax.plot([8, 72], [11.5, 11.5], color=BORDER_COLOR, lw=1.0, linestyle='--')

    # 400 Hz Spatial Circular Beam Wobble Trajectory
    theta = np.linspace(0, 10 * np.pi, 400)
    wobble_x = 32 + 1.2 * theta
    wobble_y = 11.5 + 3.8 * np.sin(theta)
    ax.plot(wobble_x, wobble_y, color=ACCENT_RED, lw=2.2, zorder=5)

    # Keyhole laser melt pool center
    ax.scatter([wobble_x[-1]], [wobble_y[-1]], color='#FF1E00', s=60, zorder=6)
    ax.scatter([wobble_x[-1]], [wobble_y[-1]], color='#FFFFFF', s=20, zorder=7)

    # Right Side: Metrology Box
    m_box = patches.FancyBboxPatch((78, 3), 19, 19, boxstyle="round,pad=0.5",
                                   facecolor='#F8FAFC', edgecolor=BORDER_COLOR, lw=1.2)
    ax.add_patch(m_box)
    ax.text(87.5, 18.5, "WELD INTEGRITY", color=INK_NAVY, fontsize=7.5, fontweight='bold', ha='center', family='sans-serif')
    ax.plot([80, 95], [16.5, 16.5], color=BORDER_COLOR, lw=0.8)
    ax.text(80, 13.5, "• Shear Load: > 850 N", color=ACCENT_GREEN, fontsize=6.8, fontweight='bold', family='monospace')
    ax.text(80, 10.0, "• CuAl₂ Layer: < 4 µm", color=ACCENT_RED, fontsize=6.8, family='monospace')
    ax.text(80, 6.5,  "• Resistance: < 12 µΩ", color=INK_NAVY, fontsize=6.8, family='monospace')

    # Center Labels
    ax.text(40, 22.5, "Spatial 400 Hz Beam Wobbling (Keyhole Stabilization)", color=ACCENT_RED, fontsize=7.5, fontweight='bold', ha='center', family='sans-serif')
    ax.text(40, 1.8, "Suppression of Brittle Intermetallic Phases in EV Busbars", color=INK_SLATE, fontsize=6.5, ha='center', family='sans-serif')

    plt.tight_layout()
    plt.savefig('res_3_welding.png', dpi=DPI, facecolor=BG_WHITE)
    plt.close()
    print("res_3_welding.png generated.")

# ==============================================================================
# 4. res_4_wavefront.png: Shack-Hartmann Wavefront Sensing & Thermal Bloom Correction
# ==============================================================================
def draw_res_4():
    fig, ax = create_base_fig()

    # Left Side: Micro-Lenslet Array Grid (Cyan Reference vs Red Distorted Spots)
    box_sh = patches.Rectangle((8, 4), 32, 17, facecolor='#F8FAFC', edgecolor=BORDER_COLOR, lw=1.2)
    ax.add_patch(box_sh)
    ax.text(24, 18.8, "SHACK-HARTMANN LENSLET ARRAY", color=INK_NAVY, fontsize=6.2, fontweight='bold', ha='center', family='sans-serif')

    for gx in np.linspace(12, 36, 6):
        for gy in np.linspace(6, 16, 4):
            # Unaberrated reference grid spot (cyan)
            ax.scatter([gx], [gy], color='#94A3B8', s=16)
            # Aberrated spot (red displaced by thermal lensing)
            dx = (gx - 24) * 0.12
            dy = (gy - 11) * 0.14
            ax.scatter([gx + dx], [gy + dy], color=ACCENT_RED, s=24)
            ax.plot([gx, gx + dx], [gy, gy + dy], color=ACCENT_RED, lw=0.9)

    # Middle Arrow: Real-time Closed Loop Feedback
    ax.annotate('', xy=(48, 12.5), xytext=(41, 12.5),
                arrowprops=dict(arrowstyle="->", color=ACCENT_CYAN, lw=2.5))
    ax.text(44.5, 14.5, "35 ms Closed-Loop", color=ACCENT_CYAN, fontsize=6.5, fontweight='bold', ha='center', family='monospace')

    # Middle Right: Focal Drift Compensation Curve
    t = np.linspace(50, 74, 100)
    # Uncompensated drift (dotted red line rising to 1.8mm)
    drift_uncomp = 8 + 8 * (1 - np.exp(-(t - 50) / 6))
    ax.plot(t, drift_uncomp, color=ACCENT_RED, lw=1.8, linestyle='--', label="Uncompensated")
    # Compensated drift (solid green line flat < 0.08mm)
    drift_comp = 8 + 0.5 * np.sin((t - 50) * 1.5)
    ax.plot(t, drift_comp, color=ACCENT_GREEN, lw=2.2, label="Adaptive AO")
    ax.text(62, 18.5, "Focal Drift: 1.8 mm → 0.08 mm", color=ACCENT_GREEN, fontsize=6.8, fontweight='bold', ha='center', family='monospace')
    ax.text(62, 6.0, "Time (min) →", color=INK_SLATE, fontsize=6.0, ha='center', family='sans-serif')

    # Right Side: Metrology Box
    m_box = patches.FancyBboxPatch((78, 3), 19, 19, boxstyle="round,pad=0.5",
                                   facecolor='#F8FAFC', edgecolor=BORDER_COLOR, lw=1.2)
    ax.add_patch(m_box)
    ax.text(87.5, 18.5, "ADAPTIVE OPTICS", color=INK_NAVY, fontsize=7.2, fontweight='bold', ha='center', family='sans-serif')
    ax.plot([80, 95], [16.5, 16.5], color=BORDER_COLOR, lw=0.8)
    ax.text(80, 13.5, "• Response: 35 ms", color=ACCENT_CYAN, fontsize=6.8, fontweight='bold', family='monospace')
    ax.text(80, 10.0, "• Drift: < 0.08 mm", color=ACCENT_GREEN, fontsize=6.8, fontweight='bold', family='monospace')
    ax.text(80, 6.5,  "• Strehl Ratio: > 0.92", color=INK_NAVY, fontsize=6.8, family='monospace')

    # Bottom Title
    ax.text(42, 22.5, "In-Situ Wavefront Sensing & Thermal Bloom Dynamic Correction", color=INK_NAVY, fontsize=7.5, fontweight='bold', ha='center', family='sans-serif')
    ax.text(42, 1.8, "Motorized Beam Expander Compensates Thermal Lensing in Real Time", color=INK_SLATE, fontsize=6.5, ha='center', family='sans-serif')

    plt.tight_layout()
    plt.savefig('res_4_wavefront.png', dpi=DPI, facecolor=BG_WHITE)
    plt.close()
    print("res_4_wavefront.png generated.")

# ==============================================================================
# 5. res_5_cfd.png: Supersonic Laval Nozzle & Shock Diamond Ejection Dynamics
# ==============================================================================
def draw_res_5():
    fig, ax = create_base_fig()

    # Laval Nozzle Contour (Convergent-Divergent Profile)
    # Upper lip
    ax.plot([8, 18, 24, 34], [21, 16, 16, 20], color=INK_NAVY, lw=2.5)
    # Lower lip
    ax.plot([8, 18, 24, 34], [5, 10, 10, 6], color=INK_NAVY, lw=2.5)
    
    # Gas Inlet Hatch
    ax.fill_between([8, 18, 24, 34], [21, 16, 16, 20], [24, 24, 24, 24], color='#CBD5E1', alpha=0.5)
    ax.fill_between([8, 18, 24, 34], [2, 2, 2, 2], [5, 10, 10, 6], color='#CBD5E1', alpha=0.5)

    # Supersonic Gas Core Stream (Mach 2.2)
    ax.fill_between([24, 68], [16, 19], [10, 7], color='#E0F2FE', alpha=0.7)

    # Shock Diamonds (Train of 4 Supersonic Diamonds)
    diamonds_x = [30, 38, 46, 54]
    for dx in diamonds_x:
        poly_d = patches.Polygon([[dx - 2.5, 13], [dx, 15.5], [dx + 2.5, 13], [dx, 10.5]], closed=True,
                                 facecolor='#F59E0B', edgecolor='#D97706', lw=1.2)
        ax.add_patch(poly_d)

    # Kerf Standoff & Workpiece at x = 68
    wp = patches.Rectangle((68, 4), 6, 18, facecolor='#94A3B8', edgecolor=INK_NAVY, lw=1.5)
    ax.add_patch(wp)
    # Kerf slot
    ax.plot([68, 74], [13, 13], color=ACCENT_RED, lw=2.5)
    ax.annotate('', xy=(72, 8), xytext=(66, 13),
                arrowprops=dict(arrowstyle="->", color=ACCENT_CYAN, lw=2.0))
    ax.text(70, 2.0, "Kerf Standoff: 1.5 mm", color=INK_SLATE, fontsize=6.2, ha='center', family='monospace')

    # Right Side: Metrology Box
    m_box = patches.FancyBboxPatch((78, 3), 19, 19, boxstyle="round,pad=0.5",
                                   facecolor='#F8FAFC', edgecolor=BORDER_COLOR, lw=1.2)
    ax.add_patch(m_box)
    ax.text(87.5, 18.5, "SUPERSONIC CFD", color=INK_NAVY, fontsize=7.2, fontweight='bold', ha='center', family='sans-serif')
    ax.plot([80, 95], [16.5, 16.5], color=BORDER_COLOR, lw=0.8)
    ax.text(80, 13.5, "• Core Velocity: Mach 2.2", color=ACCENT_RED, fontsize=6.6, fontweight='bold', family='monospace')
    ax.text(80, 10.0, "• Melt Speed: > 320 m/s", color=INK_NAVY, fontsize=6.6, family='monospace')
    ax.text(80, 6.5,  "• Melt Dross: ZERO", color=ACCENT_GREEN, fontsize=6.6, fontweight='bold', family='monospace')

    # Center Labels
    ax.text(42, 22.5, "Mach 2.2 Shock Diamond Train Aligned to Kerf Entry", color=ACCENT_RED, fontsize=7.5, fontweight='bold', ha='center', family='sans-serif')
    ax.text(42, 1.8, "Boundary-Layer Gas Shear (+38%) Completely Eliminates Dross Burrs", color=INK_SLATE, fontsize=6.5, ha='center', family='sans-serif')

    plt.tight_layout()
    plt.savefig('res_5_cfd.png', dpi=DPI, facecolor=BG_WHITE)
    plt.close()
    print("res_5_cfd.png generated.")

# ==============================================================================
# 6. res_6_sync.png: CNC G-Code & Position-Synchronized Triggering (PSO)
# ==============================================================================
def draw_res_6():
    fig, ax = create_base_fig()

    # Waveform Axis Frame
    w_frame = patches.Rectangle((8, 4), 66, 17, facecolor='#F8FAFC', edgecolor=BORDER_COLOR, lw=1.2)
    ax.add_patch(w_frame)

    t = np.linspace(10, 72, 350)
    
    # 1. CNC Motion Encoder Velocity Ramp (Cyan)
    cnc_v = 15.5 + 2.5 * np.sin((t - 10) * 0.1)
    ax.plot(t, cnc_v, color=ACCENT_CYAN, lw=2.0)
    ax.text(12, 18.5, "CH 1: CNC Position Clock (200 mm/s Encoder Output)", color=ACCENT_CYAN, fontsize=6.5, fontweight='bold', family='sans-serif')

    # 2. Synchronized PSO Laser Gate Pulses (Red Square Waves)
    ax.text(12, 11.5, "CH 2: Deterministic Laser Fire Pulse Train (PSO Gated)", color=ACCENT_RED, fontsize=6.5, fontweight='bold', family='sans-serif')
    p_wave = []
    for x in t:
        cycle = int((x - 10) * 0.6)
        p_wave.append(9.5 if (cycle % 2 == 0) else 7.5)
    ax.step(t, p_wave, color=ACCENT_RED, lw=1.8, where='mid')

    # 3. Micro-Spot Track on Workpiece
    ax.plot([10, 72], [5.5, 5.5], color=BORDER_COLOR, lw=1.0, linestyle=':')
    for sx in np.linspace(12, 70, 24):
        ax.scatter([sx], [5.5], color='#F59E0B', s=20)
    ax.text(12, 4.2, "RESULT: Exact Equidistant Spot Pitch (Zero Distortion During Accel/Decel)", color=INK_NAVY, fontsize=6.0, fontweight='bold', family='sans-serif')

    # Right Side: Metrology Box
    m_box = patches.FancyBboxPatch((78, 3), 19, 19, boxstyle="round,pad=0.5",
                                   facecolor='#F8FAFC', edgecolor=BORDER_COLOR, lw=1.2)
    ax.add_patch(m_box)
    ax.text(87.5, 18.5, "MOTION & PSO SYNC", color=INK_NAVY, fontsize=7.2, fontweight='bold', ha='center', family='sans-serif')
    ax.plot([80, 95], [16.5, 16.5], color=BORDER_COLOR, lw=0.8)
    ax.text(80, 13.5, "• Jitter: < 50 ns", color=ACCENT_GREEN, fontsize=6.8, fontweight='bold', family='monospace')
    ax.text(80, 10.0, "• 4-Axis Multi-Sync", color=INK_NAVY, fontsize=6.8, family='monospace')
    ax.text(80, 6.5,  "• Class 4 Interlocked", color=ACCENT_RED, fontsize=6.8, fontweight='bold', family='monospace')

    # Top & Bottom Titles
    ax.text(42, 22.5, "Position-Synchronized Output (PSO) Pulse Gating Architecture", color=INK_NAVY, fontsize=7.5, fontweight='bold', ha='center', family='sans-serif')

    plt.tight_layout()
    plt.savefig('res_6_sync.png', dpi=DPI, facecolor=BG_WHITE)
    plt.close()
    print("res_6_sync.png generated.")

if __name__ == '__main__':
    print("Generating ultra-sharp, panoramic research diagrams...")
    draw_res_1()
    draw_res_2()
    draw_res_3()
    draw_res_4()
    draw_res_5()
    draw_res_6()
    print("All 6 research diagrams successfully regenerated at 300 DPI!")
