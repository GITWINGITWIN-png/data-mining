"""บทที่ 3 — Scatter Plot + Correlation Heatmap (2 ใน 4 กราฟที่ guideline ระบุชื่อ)

ภาพนี้แบ่งเป็น 2 ส่วน:
A) แถวของ scatter ที่มี r ต่าง ๆ กัน → ฝึกตา "เดา r จากภาพ" ซึ่งเป็นแนวข้อสอบ
B) กับดักคลาสสิก: ความสัมพันธ์แบบโค้ง (non-linear) ที่ r ≈ 0 ทั้งที่สัมพันธ์กันชัดเจน
   → พิสูจน์ว่า "r วัดได้เฉพาะความสัมพันธ์เชิงเส้น" เท่านั้น
C) Correlation heatmap ของชุดข้อมูลรถมือสอง (ล้อจากตัวอย่าง Toyota Corolla ในสไลด์)
"""
from _style import apply, save, C
import matplotlib.pyplot as plt
import numpy as np

apply()
rng = np.random.default_rng(11)
n = 220


def corr_pair(target_r, n=n):
    """สร้างคู่ (x, y) ที่มี Pearson r ประมาณตามที่ต้องการ"""
    x = rng.normal(0, 1, n)
    e = rng.normal(0, 1, n)
    y = target_r * x + np.sqrt(max(1 - target_r ** 2, 1e-9)) * e
    return x, y


fig = plt.figure(figsize=(13.6, 8.6))
gs = fig.add_gridspec(2, 5, height_ratios=[1, 1.25], hspace=0.42, wspace=0.30,
                      top=0.87, bottom=0.06, left=0.06, right=0.96)

# ── แถวบน: scatter ที่ r ต่าง ๆ ────────────────────────────────────────────
targets = [(-0.95, "Strong negative"), (-0.5, "Moderate negative"),
           (0.0, "No correlation"), (0.5, "Moderate positive"),
           (0.9, "Strong positive")]

for i, (tr, lab) in enumerate(targets):
    ax = fig.add_subplot(gs[0, i])
    x, y = corr_pair(tr)
    r = np.corrcoef(x, y)[0, 1]          # วัด r จริงจากข้อมูลที่สร้าง
    col = C["red"] if r < -0.3 else (C["green"] if r > 0.3 else C["grey"])
    ax.scatter(x, y, s=13, color=col, alpha=0.6, edgecolor="none")
    if abs(r) > 0.25:                     # ลากเส้นแนวโน้มเฉพาะเมื่อมีความสัมพันธ์
        xs = np.linspace(x.min(), x.max(), 2)
        b1, b0 = np.polyfit(x, y, 1)
        ax.plot(xs, b1 * xs + b0, color=C["ink"], lw=1.6, ls="--")
    ax.set_title(f"r = {r:+.2f}\n{lab}", fontsize=10.5)
    ax.set_xticks([]); ax.set_yticks([])
    ax.grid(False)

# ── แถวล่างซ้าย: กับดัก non-linear ────────────────────────────────────────
ax = fig.add_subplot(gs[1, 0:2])
x = np.linspace(-3, 3, n)
y = x ** 2 + rng.normal(0, 0.7, n)
r = np.corrcoef(x, y)[0, 1]
ax.scatter(x, y, s=18, color=C["purple"], alpha=0.75, edgecolor="none")
b1, b0 = np.polyfit(x, y, 1)
ax.plot(x, b1 * x + b0, color=C["red"], lw=2.0, ls="--",
        label=f"เส้นตรงที่ fit ได้  (r = {r:+.2f})")
ax.set_title("⚠️ กับดัก: r ≈ 0 ไม่ได้แปลว่า 'ไม่มีความสัมพันธ์'", fontsize=12)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.legend(loc="upper right", fontsize=9.5)
ax.text(0.03, 0.97, "ความสัมพันธ์ชัดเจนมาก (y = x²)\nแต่ไม่ใช่ 'เชิงเส้น' → r จับไม่ได้",
        transform=ax.transAxes, ha="left", va="top", fontsize=10,
        color=C["purple"], fontweight="bold", linespacing=1.5,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                  edgecolor=C["purple"], alpha=0.93, linewidth=1.0))

# ── แถวล่างขวา: correlation heatmap ───────────────────────────────────────
ax = fig.add_subplot(gs[1, 2:5])
# จำลองข้อมูลรถมือสองให้มีความสัมพันธ์เหมือนตัวอย่าง Toyota Corolla ในสไลด์:
# ยิ่งเก่า/วิ่งเยอะ ราคายิ่งถูก
m = 600
age = rng.uniform(1, 80, m)                                   # อายุ (เดือน)
km = age * 900 + rng.normal(0, 12_000, m) + 5_000              # ระยะทางสะสม
hp = rng.normal(105, 14, m)                                    # แรงม้า
price = 22_000 - 130 * age - 0.045 * km + 55 * hp + rng.normal(0, 900, m)
M = np.vstack([price, age, km, hp])
labels = ["Price", "Age", "KM", "HP"]
R = np.corrcoef(M)

im = ax.imshow(R, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(labels)), labels)
ax.set_yticks(range(len(labels)), labels)
for i in range(len(labels)):
    for j in range(len(labels)):
        # ตัวอักษรขาวบนพื้นเข้ม ดำบนพื้นอ่อน เพื่อให้อ่านออกทุกช่อง
        ax.text(j, i, f"{R[i, j]:+.2f}", ha="center", va="center",
                fontsize=11, fontweight="bold",
                color="white" if abs(R[i, j]) > 0.55 else C["ink"])
ax.set_title("Correlation Heatmap — ยิ่งเข้มยิ่งสัมพันธ์แรง\n"
             "แดง = ลบ · น้ำเงิน = บวก", fontsize=12)
ax.grid(False)
fig.colorbar(im, ax=ax, shrink=0.78, label="Pearson r")

fig.suptitle("Scatter Plot & Correlation Heatmap — อ่านค่า r ให้เป็น",
             fontsize=15, fontweight="bold", y=0.975)
save(fig, "eda_correlation.png")

print("ตัวอย่างค่า r ใน heatmap:")
for i, a in enumerate(labels):
    for b, v in zip(labels[i+1:], R[i, i+1:]):
        print(f"  r({a:5s}, {b:5s}) = {v:+.2f}")
