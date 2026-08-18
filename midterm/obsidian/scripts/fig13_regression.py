"""บทที่ 9 — Least Squares, R² และ Overfitting

แผง A: ข้อมูล 5 จุดที่ตัวเลขลงตัวพอดี → คำนวณ b0, b1 มือตามได้ในห้องสอบ
แผง B: แยก SST ออกเป็น "ส่วนที่โมเดลอธิบายได้ (SSR)" กับ "ส่วนที่เหลือ (SSE)"
        เพื่อให้เห็นว่า R² = 1 - SSE/SST มาจากไหน
แผง C: กราฟ train vs test error — หน้าตาของ overfitting
"""
from _style import apply, save, C
import matplotlib.pyplot as plt
import numpy as np

apply()

# ── ข้อมูลตัวอย่าง: ประสบการณ์ (ปี) vs เงินเดือน (พันบาท) ──────────────────
x = np.array([1.0, 2, 3, 4, 5])
y = np.array([30.0, 35, 45, 55, 60])
n = len(x)

Sx, Sy, Sxy, Sxx = x.sum(), y.sum(), (x * y).sum(), (x ** 2).sum()
b1 = (Sxy - Sx * Sy / n) / (Sxx - Sx ** 2 / n)     # สูตรในสไลด์
b0 = y.mean() - b1 * x.mean()
yhat = b0 + b1 * x
resid = y - yhat
SSE = (resid ** 2).sum()
SST = ((y - y.mean()) ** 2).sum()
SSR = ((yhat - y.mean()) ** 2).sum()
R2 = 1 - SSE / SST

print(f"Σx={Sx:g} Σy={Sy:g} Σxy={Sxy:g} Σx²={Sxx:g}  n={n}")
print(f"b1 = ({Sxy:g} - {Sx:g}*{Sy:g}/{n}) / ({Sxx:g} - {Sx:g}²/{n}) = {b1:g}")
print(f"b0 = {y.mean():g} - {b1:g}*{x.mean():g} = {b0:g}")
print(f"ŷ = {b0:g} + {b1:g}x     residuals = {resid.tolist()}")
print(f"SSE={SSE:g}  SSR={SSR:g}  SST={SST:g}  (SSR+SSE={SSR+SSE:g})  R²={R2:.4f}")

fig, axes = plt.subplots(1, 3, figsize=(16.0, 5.6))

# ══════════ A: OLS + residuals ══════════
ax = axes[0]
xs = np.linspace(0.4, 5.6, 100)
ax.plot(xs, b0 + b1 * xs, color=C["blue"], lw=2.6, zorder=2,
        label=f"ŷ = {b0:g} + {b1:g}x")
for xi, yi, yh in zip(x, y, yhat):
    ax.plot([xi, xi], [yi, yh], color=C["red"], lw=2.2, ls="-", zorder=3)
    ax.annotate(f"{yi-yh:+.0f}", (xi, (yi + yh) / 2), xytext=(9, 0),
                textcoords="offset points", fontsize=9.5, color=C["red"],
                fontweight="bold", va="center")
ax.scatter(x, y, s=140, color=C["ink"], zorder=5, edgecolor="white", linewidth=1.6,
           label="ค่าจริง $y_i$")
ax.scatter(x, yhat, s=90, color=C["blue"], zorder=4, marker="s",
           edgecolor="white", linewidth=1.4, label="ค่าทำนาย $\\hat{y}_i$")
ax.set_xlabel("ประสบการณ์ (ปี)  —  $x$")
ax.set_ylabel("เงินเดือน (พันบาท)  —  $y$")
ax.set_title("Least Squares — ลากเส้นที่ทำให้ผลรวมกำลังสองของ residual น้อยที่สุด")
ax.legend(loc="upper left", fontsize=9.5)
ax.text(0.97, 0.05, f"เส้นแดง = residual $(y_i-\\hat{{y}}_i)$\nSSE = {SSE:g}",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=10,
        color=C["red"], fontweight="bold", linespacing=1.6)

# ══════════ B: SST = SSR + SSE ══════════
ax = axes[1]
ax.axhline(y.mean(), color=C["grey"], ls="--", lw=2.0, zorder=1)
ax.text(5.12, y.mean(), f"  $\\bar{{y}}$ = {y.mean():g}", fontsize=10.5,
        color=C["grey"], va="center", fontweight="bold")
ax.plot(xs, b0 + b1 * xs, color=C["blue"], lw=2.4, zorder=2)
off = 0.075
for xi, yi, yh in zip(x, y, yhat):
    # ซ้าย: ระยะจากค่าเฉลี่ย (SST)   ขวา: ระยะจากเส้น (SSE)
    ax.plot([xi - off, xi - off], [y.mean(), yi], color=C["purple"], lw=3.2, zorder=3)
    ax.plot([xi + off, xi + off], [yh, yi], color=C["red"], lw=3.2, zorder=3)
ax.scatter(x, y, s=110, color=C["ink"], zorder=5, edgecolor="white", linewidth=1.5)
ax.set_xlim(0.3, 8.6)          # เผื่อที่ว่างขวามือไว้วางกล่องสรุป
ax.set_xticks([1, 2, 3, 4, 5])
ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
ax.set_title("R² มาจากไหน — แยกความแปรผันออกเป็นสองส่วน")
ax.text(0.97, 0.04,
        f"SST (ม่วง: $y_i-\\bar{{y}}$)   = {SST:g}\n"
        f"SSE (แดง: $y_i-\\hat{{y}}_i$) = {SSE:g}\n"
        f"SSR (ที่อธิบายได้)      = {SSR:g}\n"
        f"────────────────────\n"
        f"R² = 1 − SSE/SST = {R2:.4f}",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=9.6,
        linespacing=1.75, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white",
                  edgecolor=C["ink"], alpha=0.95, linewidth=1.2))

# ══════════ C: Overfitting ══════════
ax = axes[2]
k = np.arange(1, 13)
train_err = 1400 * np.exp(-0.16 * k) + 620          # เทรนดีขึ้นเรื่อย ๆ เสมอ
test_err = 1400 * np.exp(-0.30 * k) + 620 + 26 * (k - 3.2) ** 2 * (k > 3.2)
best = k[test_err.argmin()]
ax.plot(k, train_err, "o-", color=C["green"], lw=2.6, ms=7, label="Training error")
ax.plot(k, test_err, "s-", color=C["red"], lw=2.6, ms=7, label="Test / Validation error")
ax.axvline(best, color=C["ink"], ls="--", lw=2.0)
ax.axvspan(best, 12.6, color=C["red"], alpha=0.08)
ax.axvspan(0.4, best, color=C["green"], alpha=0.07)
ax.text(best - 0.25, ax.get_ylim()[1] * 0.97, "จุดที่ดีที่สุด", ha="right",
        va="top", fontsize=10, fontweight="bold", color=C["ink"])
ax.text(best + 0.35, 2560, "OVERFITTING\nโมเดลจำ noise\nของ training data",
        ha="left", va="top", fontsize=10.5, color=C["red"], fontweight="bold",
        linespacing=1.6)
ax.set_xlabel("จำนวน predictors / ความซับซ้อนของโมเดล")
ax.set_ylabel("Error (เช่น RMSE)")
ax.set_title("Overfitting — เทรนดีขึ้นเรื่อย ๆ แต่ทดสอบแย่ลง")
ax.legend(loc="lower left", fontsize=9.8)
ax.set_xticks(k)

fig.suptitle("Regression Analysis — จากเส้นตรงที่ดีที่สุด สู่ R² และกับดัก Overfitting",
             fontsize=15, fontweight="bold", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.93])
save(fig, "reg_ols_r2_overfit.png")
