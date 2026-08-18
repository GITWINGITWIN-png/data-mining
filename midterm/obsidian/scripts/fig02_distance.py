"""บทที่ 2 — ระยะทาง Euclidean / Manhattan + ตรวจสอบตัวอย่างในสไลด์

สคริปต์นี้ทำ 2 อย่าง:
1. คำนวณ dissimilarity matrix ของตัวอย่าง 4 จุดในสไลด์ซ้ำ เพื่อ "ตรวจการบ้านสไลด์"
2. วาดภาพให้เห็นว่า Euclidean (เส้นตรง) กับ Manhattan (เดินตามตาราง) ต่างกันยังไง
"""
from _style import apply, save, C
import matplotlib.pyplot as plt
import numpy as np

apply()

# ── ส่วนที่ 1: ตรวจตัวเลขในสไลด์ ───────────────────────────────────────────
pts = {"x1": (1, 2), "x2": (3, 5), "x3": (2, 0), "x4": (4, 5)}
names = list(pts)
print("Euclidean dissimilarity matrix (คำนวณเอง):")
print("      " + "".join(f"{n:>8}" for n in names))
for a in names:
    row = f"{a:>4}  "
    for b in names:
        d = np.hypot(pts[a][0] - pts[b][0], pts[a][1] - pts[b][1])
        row += f"{d:8.2f}"
    print(row)

slide = {("x1", "x2"): 3.61, ("x1", "x3"): 5.1, ("x1", "x4"): 4.24,
         ("x2", "x3"): 5.1, ("x2", "x4"): 1.0, ("x3", "x4"): 5.39}
print("\nเทียบกับตัวเลขที่พิมพ์ในสไลด์:")
for (a, b), v in slide.items():
    d = np.hypot(pts[a][0] - pts[b][0], pts[a][1] - pts[b][1])
    flag = "OK" if abs(d - v) < 0.02 else f"<-- ไม่ตรง! ที่ถูกคือ {d:.2f}"
    print(f"  d({a},{b}): สไลด์={v:<5} คำนวณ={d:5.2f}  {flag}")

# ── ส่วนที่ 2: ภาพเปรียบเทียบระยะทาง ────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.0))

# ซ้าย: จุดทั้ง 4 จากสไลด์ พร้อมระยะจริง
ax = axes[0]
for n, (x, y) in pts.items():
    ax.scatter(x, y, s=170, color=C["blue"], zorder=3, edgecolor="white", linewidth=1.6)
    ax.annotate(f"{n} ({x},{y})", (x, y), textcoords="offset points",
                xytext=(10, 8), fontsize=10, fontweight="bold")
# ลากเส้นคู่ที่สไลด์พิมพ์ผิด ให้เห็นว่ามันสั้น ไม่ใช่ 5.1
ax.plot([1, 2], [2, 0], color=C["red"], lw=2.2, ls="--", zorder=2)
ax.annotate("d(x1,x3) = 2.24\nสไลด์พิมพ์ 5.1", (1.5, 1.0),
            textcoords="offset points", xytext=(18, -6),
            fontsize=9.5, color=C["red"], fontweight="bold")
ax.plot([2, 3], [0, 5], color=C["grey"], lw=1.6, ls=":", zorder=1)
ax.annotate("d(x2,x3) = 5.10", (2.5, 2.5), textcoords="offset points",
            xytext=(6, 4), fontsize=9, color=C["grey"])
ax.set_xlim(0, 5.4); ax.set_ylim(-0.8, 6.2)
ax.set_xlabel("attribute 1"); ax.set_ylabel("attribute 2")
ax.set_title("ตัวอย่าง 4 จุดจากสไลด์ (Euclidean)")

# ขวา: Euclidean vs Manhattan
ax = axes[1]
p, q = np.array([1, 1]), np.array([5, 4])
ax.plot(*zip(p, q), color=C["blue"], lw=2.8, zorder=3,
        label="Euclidean (h=2) = 5.00")
ax.plot([p[0], q[0], q[0]], [p[1], p[1], q[1]], color=C["orange"], lw=2.8,
        zorder=2, label="Manhattan (h=1) = 7")
ax.plot([p[0], p[0], q[0]], [p[1], q[1], q[1]], color=C["orange"], lw=2.0,
        ls="--", alpha=0.6, zorder=2)
for pt, lab in [(p, "i (1,1)"), (q, "j (5,4)")]:
    ax.scatter(*pt, s=170, color=C["ink"], zorder=4, edgecolor="white", linewidth=1.6)
    ax.annotate(lab, pt, textcoords="offset points", xytext=(10, -16),
                fontsize=10, fontweight="bold")
ax.annotate("|5-1| + |4-1| = 4 + 3 = 7", (3, 0.72), fontsize=9.5,
            color=C["orange"], fontweight="bold", ha="center")
ax.annotate(r"$\sqrt{4^2+3^2}=5$", (2.5, 3.1), fontsize=11,
            color=C["blue"], fontweight="bold")
ax.set_xlim(0, 6.3); ax.set_ylim(0, 5.3)
ax.set_xlabel("attribute 1"); ax.set_ylabel("attribute 2")
ax.set_title("Minkowski: h=1 vs h=2")
ax.legend(loc="upper left", fontsize=9.5)

fig.suptitle("Distance measures — เส้นตรง vs เดินตามถนน",
             fontsize=14, fontweight="bold", y=1.00)
fig.tight_layout()
save(fig, "distance_measures.png")
