"""บทที่ 3 — กายวิภาคของ Boxplot + กฎ IQR สำหรับหา outlier

ทำไมต้องมีภาพนี้: guideline ระบุ "Boxplot" ตรง ๆ และกฎ 1.5×IQR เป็นสูตรที่คำนวณ
ในข้อสอบได้จริง ภาพนี้จึงใช้ "ชุดข้อมูลจริง" ที่คำนวณตัวเลขให้เห็น ไม่ใช่ภาพลอย ๆ
"""
from _style import apply, save, C
import matplotlib.pyplot as plt
import numpy as np

apply()

# ชุดข้อมูลเล็ก ๆ ที่คำนวณมือตามได้ — เงินเดือน (พันบาท) ของพนักงาน 15 คน
data = np.array([18, 20, 22, 23, 25, 26, 28, 30, 32, 34, 36, 38, 42, 45, 95])

q1, q2, q3 = np.percentile(data, [25, 50, 75])
iqr = q3 - q1
lo_fence, hi_fence = q1 - 1.5 * iqr, q3 + 1.5 * iqr
inliers = data[(data >= lo_fence) & (data <= hi_fence)]
outliers = data[(data < lo_fence) | (data > hi_fence)]
whisk_lo, whisk_hi = inliers.min(), inliers.max()   # หนวด = ค่าสุดขั้วที่ "ยังไม่ใช่" outlier

print(f"Q1={q1}  Q2(median)={q2}  Q3={q3}  IQR={iqr}")
print(f"รั้วล่าง = Q1 - 1.5*IQR = {q1} - {1.5*iqr} = {lo_fence}")
print(f"รั้วบน  = Q3 + 1.5*IQR = {q3} + {1.5*iqr} = {hi_fence}")
print(f"หนวด: {whisk_lo} ถึง {whisk_hi}   outliers: {outliers}")

fig, ax = plt.subplots(figsize=(11.5, 5.4))

# วาด boxplot เอง เพื่อคุมตำแหน่ง label ได้เต็มที่
Y = 0.0
ax.add_patch(plt.Rectangle((q1, Y - 0.22), iqr, 0.44,
                           facecolor=C["sky"], edgecolor=C["blue"],
                           linewidth=2, alpha=0.55, zorder=2))
ax.plot([q2, q2], [Y - 0.22, Y + 0.22], color=C["blue"], lw=3.4, zorder=3)
for w in (whisk_lo, whisk_hi):                       # หนวด
    ax.plot([w, w], [Y - 0.13, Y + 0.13], color=C["blue"], lw=2.2, zorder=3)
ax.plot([whisk_lo, q1], [Y, Y], color=C["blue"], lw=1.8, zorder=1)
ax.plot([q3, whisk_hi], [Y, Y], color=C["blue"], lw=1.8, zorder=1)
ax.scatter(outliers, [Y] * len(outliers), s=120, color=C["red"],
           zorder=5, edgecolor="white", linewidth=1.4)

# จุดข้อมูลดิบทั้งหมด กระจายไว้ด้านล่าง ให้เห็นว่ากล่องมาจากข้อมูลจริง
rng = np.random.default_rng(7)
ax.scatter(data, Y - 0.70 + rng.normal(0, 0.035, len(data)),
           s=42, color=C["grey"], alpha=0.75, zorder=4)
ax.text(56, Y - 0.70, "← ข้อมูลดิบ 15 ค่า", fontsize=9.5, va="center", color=C["grey"])

# ป้ายกำกับส่วนต่าง ๆ
labels = [
    (whisk_lo, '"min"\n(หนวดล่าง)', 0.40, C["blue"]),
    (q1,       f"Q1 = {q1:g}\n(25%)", 0.62, C["blue"]),
    (q2,       f"Median Q2 = {q2:g}\n(50%)", 0.40, C["blue"]),
    (q3,       f"Q3 = {q3:g}\n(75%)", 0.62, C["blue"]),
    (whisk_hi, '"max"\n(หนวดบน)', 0.40, C["blue"]),
    (outliers[0], f"Outlier = {outliers[0]:g}", 0.40, C["red"]),
]
for x, txt, dy, col in labels:
    ax.annotate(txt, (x, Y + 0.24), xytext=(x, Y + dy), ha="center",
                fontsize=9.6, color=col, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=col, lw=1.2))

# แถบ IQR
ax.annotate("", (q1, Y - 0.34), (q3, Y - 0.34),
            arrowprops=dict(arrowstyle="<->", color=C["orange"], lw=2.2))
ax.text((q1 + q3) / 2, Y - 0.41, f"IQR = Q3 − Q1 = {q3:g} − {q1:g} = {iqr:g}",
        ha="center", va="top", fontsize=10.5, color=C["orange"], fontweight="bold")

# รั้ว (fences)
for fx, name in [(lo_fence, "รั้วล่าง"), (hi_fence, "รั้วบน")]:
    ax.axvline(fx, color=C["red"], ls="--", lw=1.5, alpha=0.8, zorder=0)
    ax.text(fx, Y + 0.86, f"{name}\n{fx:g}", ha="center", fontsize=9,
            color=C["red"], fontweight="bold")

ax.text(48, Y + 0.86,
        "กฎ 1.5×IQR:  x < Q1 − 1.5·IQR  หรือ  x > Q3 + 1.5·IQR  →  Outlier",
        fontsize=11, color=C["ink"], fontweight="bold", ha="left", va="center",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="#FFF4E5",
                  edgecolor=C["orange"], linewidth=1.3))

ax.set_xlim(-2, 108)
ax.set_ylim(-0.95, 1.15)
ax.set_yticks([])
ax.set_xlabel("เงินเดือน (พันบาท)")
ax.set_title("Boxplot — อ่านส่วนประกอบและกฎหา Outlier ด้วย IQR", pad=14)
ax.grid(axis="y", alpha=0)
save(fig, "eda_boxplot_anatomy.png")
