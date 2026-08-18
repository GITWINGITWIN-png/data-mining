"""บทที่ 3 — รูปทรงการแจกแจง 3 แบบ และตำแหน่ง Mean/Median/Mode

จุดสำคัญที่ภาพนี้ต้องสอนให้ได้: "ทำไม skewed distribution ต้องเติมค่าว่างด้วย Median
ไม่ใช่ Mean" — เพราะหางที่ยาวลาก Mean ตามไป แต่ Median แทบไม่ขยับ
(guideline ข้อ 3 ระบุ: Median — numerical data, especially skewed distributions)
"""
from _style import apply, save, C
import matplotlib.pyplot as plt
import numpy as np

apply()
rng = np.random.default_rng(42)
N = 200_000

panels = [
    ("Skewed Right (บวก)", rng.gamma(2.0, 1.0, N),          C["orange"],
     "หางยาวไปทางขวา\nMean > Median > Mode"),
    ("Normal / Symmetric", rng.normal(0, 1, N),              C["blue"],
     "สมมาตร\nMean ≈ Median ≈ Mode"),
    ("Skewed Left (ลบ)",   -rng.gamma(2.0, 1.0, N),          C["green"],
     "หางยาวไปทางซ้าย\nMean < Median < Mode"),
]

fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.6))

for ax, (title, x, col, note) in zip(axes, panels):
    counts, edges = np.histogram(x, bins=140, density=True)
    centres = (edges[:-1] + edges[1:]) / 2
    ax.fill_between(centres, counts, color=col, alpha=0.30)
    ax.plot(centres, counts, color=col, lw=2.0)

    mean, median = x.mean(), np.median(x)
    mode = centres[counts.argmax()]          # ยอดของ histogram = ประมาณค่า mode
    top = counts.max()
    # skewness (โมเมนต์ที่ 3) — คำนวณจริงเพื่อให้ตัวเลขบนภาพเชื่อถือได้
    sk = ((x - mean) ** 3).mean() / x.std() ** 3

    # วาดเส้น 3 เส้น แล้วบอกค่าในกล่องแทนการติดป้ายบนเส้น
    # (เส้นสามเส้นอยู่ชิดกันมากในกรณี Normal ป้ายบนเส้นจะทับกันจนอ่านไม่ออก)
    for val, c, ls in [(mode, C["grey"], ":"), (median, C["ink"], "--"),
                       (mean, C["red"], "-")]:
        ax.axvline(val, color=c, ls=ls, lw=2.0, ymax=0.88)
    # เผื่อที่ว่างเหนือกราฟ เพื่อให้กล่องค่าสถิติไม่ทับเส้นโค้ง
    ax.set_ylim(0, top * 1.62)
    bx = 0.97 if sk >= -0.2 else 0.03   # เบ้ซ้ายเท่านั้นที่ต้องย้ายกล่องไปซ้าย
    ax.text(bx, 0.97,
            f"Mean   = {mean:6.2f}\nMedian = {median:6.2f}\nMode   = {mode:6.2f}",
            transform=ax.transAxes, ha=("right" if sk >= -0.2 else "left"),
            va="top", fontsize=9.2,
            family="DejaVu Sans Mono", linespacing=1.5,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                      edgecolor=C["grey"], alpha=0.92, linewidth=0.9))

    ax.set_title(f"{title}\nSkewness = {sk:+.2f}", fontsize=12)
    ax.text(0.5, -0.20, note, transform=ax.transAxes, ha="center", va="top",
            fontsize=10.5, color=col, fontweight="bold", linespacing=1.6)
    ax.set_yticks([])

fig.suptitle("Distribution shape — หางลาก Mean ไป แต่ Median อยู่กับที่",
             fontsize=14.5, fontweight="bold", y=1.03)
# legend รวมของทั้งภาพ — อธิบายว่าเส้นแต่ละแบบคืออะไร
from matplotlib.lines import Line2D
fig.legend(handles=[Line2D([], [], color=C["red"], ls="-", lw=2, label="Mean"),
                    Line2D([], [], color=C["ink"], ls="--", lw=2, label="Median"),
                    Line2D([], [], color=C["grey"], ls=":", lw=2, label="Mode")],
           loc="upper center", bbox_to_anchor=(0.5, 0.965), ncol=3, fontsize=10.5)

fig.text(0.5, 0.005,
         "เกณฑ์ในสไลด์:  |Skew| < 0.5 เบ้เล็กน้อย  ·  0.5 ≤ |Skew| < 1 เบ้ปานกลาง  ·  |Skew| ≥ 1 เบ้มาก",
         ha="center", fontsize=10.5, color=C["ink"], fontweight="bold",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#F3F5F8",
                   edgecolor=C["grey"], linewidth=1.0))
fig.tight_layout(rect=[0, 0.20, 1, 0.87])
save(fig, "eda_skewness.png")
