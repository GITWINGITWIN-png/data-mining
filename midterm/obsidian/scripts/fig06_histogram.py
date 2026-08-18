"""บทที่ 3 — Histogram: ผลของจำนวน bin + histogram ซ้อน target (churn overlay)

ซ้ายบน/ขวาบน: bin น้อยไป vs พอดี vs เยอะไป — เพราะข้อสอบชอบถามว่า
"จำนวน bin มีผลต่อการตีความอย่างไร"
แถวล่าง: จำลองตัวอย่าง "customer service calls with churn overlay" จากสไลด์ EDA
ทั้งแบบนับดิบและแบบ normalized เพื่อแสดงว่าทำไมต้อง normalize
"""
from _style import apply, save, C
import matplotlib.pyplot as plt
import numpy as np

apply()
rng = np.random.default_rng(3)

# ── ข้อมูล: การแจกแจงสองยอด (bimodal) ที่จะ "หายไป" ถ้า bin น้อยเกิน ──────
x = np.concatenate([rng.normal(25, 4, 1200), rng.normal(48, 5, 900)])

fig, axes = plt.subplots(2, 3, figsize=(13.6, 8.0))

for ax, bins, note in zip(axes[0], [4, 30, 200],
                          ["น้อยเกินไป — ยอดสองยอดถูกกลบหายไป",
                           "พอดี — เห็นว่าข้อมูลมี 2 กลุ่มชัดเจน",
                           "มากเกินไป — เห็นแต่ noise หยึกหยัก"]):
    ax.hist(x, bins=bins, color=C["blue"], alpha=0.8, edgecolor="white", linewidth=0.4)
    ax.set_title(f"bins = {bins}", fontsize=12)
    ax.set_xlabel("ค่าของตัวแปร"); ax.set_ylabel("count")
    ax.text(0.5, -0.34, note, transform=ax.transAxes, ha="center", va="top",
            fontsize=9.8, color=C["grey"], wrap=True)

# ── ตัวอย่าง churn overlay ─────────────────────────────────────────────────
# จำลองให้ตรงกับข้อสรุปในสไลด์: โทรหา customer service ≥ 4 ครั้ง → churn สูงขึ้นชัดเจน
calls = np.arange(0, 10)
n_total = np.array([210, 1180, 760, 430, 165, 66, 22, 9, 4, 2])
churn_rate = np.array([.19, .10, .11, .10, .46, .61, .66, .78, .75, 1.0])
n_churn = np.round(n_total * churn_rate).astype(int)
n_stay = n_total - n_churn

# ล่างซ้าย: นับดิบ (stacked)
ax = axes[1, 0]
ax.bar(calls, n_stay, color=C["blue"], label="ไม่ churn", edgecolor="white")
ax.bar(calls, n_churn, bottom=n_stay, color=C["red"], label="churn", edgecolor="white")
ax.set_title("Histogram ดิบ + churn overlay", fontsize=12)
ax.set_xlabel("จำนวนครั้งที่โทรหา customer service"); ax.set_ylabel("count")
ax.set_xticks(calls)
ax.legend(fontsize=9.5)
ax.text(0.98, 0.72, "ปัญหา: แท่งขวามือเตี้ยมาก\nจนดูไม่ออกว่าสัดส่วน churn สูง",
        transform=ax.transAxes, ha="right", va="top", fontsize=9.5,
        color=C["grey"], linespacing=1.5)

# ล่างกลาง: normalized (สัดส่วน)
ax = axes[1, 1]
ax.bar(calls, 1 - churn_rate, color=C["blue"], label="ไม่ churn", edgecolor="white")
ax.bar(calls, churn_rate, bottom=1 - churn_rate, color=C["red"],
       label="churn", edgecolor="white")
ax.axvline(3.5, color=C["ink"], ls="--", lw=2.0)
ax.set_title("Histogram แบบ Normalized (สัดส่วน)", fontsize=12)
ax.set_xlabel("จำนวนครั้งที่โทรหา customer service"); ax.set_ylabel("สัดส่วน")
ax.set_xticks(calls); ax.set_ylim(0, 1)
ax.legend(fontsize=9, loc="lower left", framealpha=0.9, frameon=True)
ax.text(3.62, 0.50, "≥ 4 ครั้ง\nchurn พุ่ง", fontsize=10, color=C["ink"],
        fontweight="bold", linespacing=1.4)

# ล่างขวา: อัตรา churn เป็นเส้น ให้เห็นจุดหักชัด ๆ
ax = axes[1, 2]
ax.plot(calls, churn_rate * 100, "o-", color=C["red"], lw=2.4, ms=8)
ax.axvline(3.5, color=C["ink"], ls="--", lw=2.0)
ax.fill_between([-0.5, 3.5], 0, 118, color=C["green"], alpha=0.10)
ax.fill_between([3.5, 9.5], 0, 118, color=C["red"], alpha=0.10)
ax.set_title("อัตรา churn ต่อจำนวนครั้งที่โทร", fontsize=12)
ax.set_xlabel("จำนวนครั้งที่โทรหา customer service"); ax.set_ylabel("churn rate (%)")
ax.set_xticks(calls); ax.set_xlim(-0.5, 9.5); ax.set_ylim(0, 118)
ax.text(1.5, 68, "โทร ≤ 3 ครั้ง\nchurn ต่ำ", ha="center", fontsize=10,
        color=C["green"], fontweight="bold", linespacing=1.4)
ax.text(6.5, 30, "โทร ≥ 4 ครั้ง\nchurn สูงมาก", ha="center", fontsize=10,
        color=C["red"], fontweight="bold", linespacing=1.4)

fig.suptitle("Histogram — จำนวน bin สำคัญ และการซ้อน target ทำให้เห็น insight",
             fontsize=15, fontweight="bold", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.96], h_pad=4.2)
save(fig, "eda_histogram.png")
