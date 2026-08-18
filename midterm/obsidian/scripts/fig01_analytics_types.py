"""บทที่ 1 — แผนภาพ 4 ระดับของ Analytics

แนวคิดของภาพ: วางทั้ง 4 ระดับบนแกน "ความยาก" (แนวนอน) กับ "มูลค่าทางธุรกิจ"
(แนวตั้ง) เพราะสไลด์บอกว่า "Each level provides greater business value" —
ภาพแบบนี้ทำให้เห็นว่าทำไมถึงไต่ระดับขึ้นไป และแต่ละระดับตอบคำถามอะไร
"""
from _style import apply, save, C
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

apply()

levels = [
    ("Descriptive",  "What happened?",      "เชิงพรรณนา",  C["blue"],
     "Reports · Dashboard\nDescriptive Statistics · DW"),
    ("Diagnostic",   "Why did it happen?",  "หาสาเหตุ",     C["sky"],
     "Drill-down · Segmentation\nCorrelation analysis"),
    ("Predictive",   "What will happen?",   "เชิงพยากรณ์",  C["orange"],
     "Linear Regression\nTime series · Data Mining"),
    ("Prescriptive", "What should we do?",  "เชิงแนะนำ",    C["green"],
     "Recommendation\nCollaborative filtering · Clustering"),
]

fig, ax = plt.subplots(figsize=(11, 6.2))

for i, (name, question, _th, color, tech) in enumerate(levels):
    x, y = i * 2.55, i * 1.30          # ไต่ขึ้นทางขวา = ยากขึ้น + มูลค่าสูงขึ้น
    box = FancyBboxPatch((x, y), 2.35, 1.15,
                         boxstyle="round,pad=0.06,rounding_size=0.12",
                         facecolor=color, edgecolor="none", alpha=0.92)
    ax.add_patch(box)
    ax.text(x + 1.175, y + 0.78, name, ha="center", va="center",
            fontsize=13, fontweight="bold", color="white")
    ax.text(x + 1.175, y + 0.34, question, ha="center", va="center",
            fontsize=10.5, color="white", style="italic")
    # เทคนิคที่ใช้ วางไว้ใต้กล่อง เพื่อไม่ให้กล่องรก
    ax.text(x + 1.175, y - 0.30, tech, ha="center", va="top",
            fontsize=8.4, color=C["grey"], linespacing=1.45)
    if i < 3:                           # ลูกศรเชื่อมระดับ
        ax.add_patch(FancyArrowPatch((x + 2.42, y + 0.58), (x + 2.48, y + 1.30),
                                     arrowstyle="-|>", mutation_scale=16,
                                     color=C["grey"], lw=1.6,
                                     connectionstyle="arc3,rad=0.0"))

# แกนบอกทิศทาง — ไม่ใช้แกนจริง เพราะเป็นแผนภาพเชิงแนวคิด ไม่มีหน่วยวัด
ax.add_patch(FancyArrowPatch((-0.85, -0.55), (-0.85, 5.15), arrowstyle="-|>",
                             mutation_scale=17, color=C["ink"], lw=1.8))
ax.text(-1.25, 2.3, "Business Value  →  สูงขึ้น", rotation=90,
        ha="center", va="center", fontsize=11, fontweight="bold")
ax.add_patch(FancyArrowPatch((-0.55, -1.45), (10.2, -1.45), arrowstyle="-|>",
                             mutation_scale=17, color=C["ink"], lw=1.8))
ax.text(4.7, -1.85, "Complexity / Difficulty  →  ยากขึ้น",
        ha="center", va="center", fontsize=11, fontweight="bold")

ax.text(4.7, 6.05, "Types of Analytics — ไต่ระดับตามคำถามที่ตอบได้",
        ha="center", fontsize=15, fontweight="bold")
ax.text(4.7, 5.62,
        'guideline ระบุ 3 ตัว (Descriptive / Predictive / Prescriptive) '
        '— Diagnostic อยู่ในสไลด์แต่ไม่อยู่ใน guideline',
        ha="center", fontsize=9.5, color=C["grey"], style="italic")

ax.set_xlim(-1.9, 11.4)
ax.set_ylim(-2.35, 6.4)
ax.axis("off")
ax.grid(False)
save(fig, "analytics_types.png")
