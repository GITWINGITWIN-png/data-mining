"""บทที่ 4 — Smoothing by Binning ทั้ง 3 วิธี บนตัวอย่างมาตรฐาน

ใช้ชุดข้อมูลคลาสสิกของ Han & Kamber (ที่สไลด์อ้างอิง):
    4, 8, 15, 21, 21, 24, 25, 28, 34   → equal-frequency 3 bins (bin ละ 3 ค่า)
แล้วเทียบ smoothing by bin means / medians / boundaries
"""
from _style import apply, save, C
import matplotlib.pyplot as plt
import numpy as np

apply()

data = np.array([4, 8, 15, 21, 21, 24, 25, 28, 34])
bins = data.reshape(3, 3)                 # equal-frequency: bin ละ 3 ค่า

by_mean = np.repeat(bins.mean(axis=1), 3)
by_median = np.repeat(np.median(bins, axis=1), 3)
# boundaries: แทนแต่ละค่าด้วย "ขอบที่ใกล้กว่า" (min หรือ max ของ bin ตัวเอง)
by_bound = np.array([b[0] if abs(v - b[0]) <= abs(v - b[-1]) else b[-1]
                     for b in bins for v in b])

print("original  :", data.tolist())
print("bins      :", bins.tolist())
print("bin means :", bins.mean(axis=1).tolist())
print("by mean   :", by_mean.tolist())
print("by median :", by_median.tolist())
print("by bound  :", by_bound.tolist())

series = [
    ("Original (sorted)", data,      C["grey"],   "ข้อมูลดิบเรียงแล้ว"),
    ("Smooth by bin MEANS", by_mean, C["blue"],   "ทุกค่าใน bin → ค่าเฉลี่ยของ bin"),
    ("Smooth by bin MEDIANS", by_median, C["green"], "ทุกค่าใน bin → มัธยฐานของ bin"),
    ("Smooth by bin BOUNDARIES", by_bound, C["orange"],
     "ทุกค่า → ขอบ (min/max) ที่ใกล้กว่า"),
]

idx = np.arange(1, 10)
fig, axes = plt.subplots(1, 4, figsize=(14.6, 5.0), sharey=True)

for ax, (title, y, col, note) in zip(axes, series):
    # แถบสีอ่อนแบ่ง bin ให้เห็นขอบเขต
    for b in range(3):
        ax.axvspan(b * 3 + 0.5, b * 3 + 3.5, color=C["grey"],
                   alpha=0.06 + 0.05 * (b % 2), zorder=0)
        ax.text(b * 3 + 2, 37.5, f"bin {b+1}", ha="center", fontsize=9.5,
                color=C["grey"], fontweight="bold")
    ax.plot(idx, data, "o--", color=C["grey"], ms=6, lw=1.2, alpha=0.5,
            zorder=2, label="เดิม")
    ax.plot(idx, y, "o-", color=col, ms=9, lw=2.6, zorder=3, label="หลัง smooth")
    for i, v in zip(idx, y):
        ax.annotate(f"{v:g}", (i, v), textcoords="offset points",
                    xytext=(0, 11), ha="center", fontsize=9,
                    color=col, fontweight="bold")
    ax.set_title(title, fontsize=11.5)
    ax.set_xlabel(note, fontsize=9.5, color=col)
    ax.set_xticks(idx)
    ax.set_ylim(0, 41)
    ax.grid(axis="x", alpha=0)

axes[0].set_ylabel("ค่าของข้อมูล")
fig.suptitle("Smoothing by Binning — ลด noise โดยแทนค่าในแต่ละ bin ด้วยค่าสรุป",
             fontsize=14.5, fontweight="bold", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.94])
save(fig, "prep_binning.png")
