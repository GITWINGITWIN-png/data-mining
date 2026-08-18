"""บทที่ 4 — Feature Scaling: ทำไมต้องทำ และ Standardization vs Min-Max ต่างกันยังไง

โจทย์: หา "เพื่อนบ้านที่ใกล้ที่สุด" ของคน A (แบบที่ k-NN ทำ)
  A = อายุ 30 เงินเดือน 50,000
  B = อายุ 32 เงินเดือน 62,000   ← ต่างกันนิดเดียวทั้งสองด้าน
  C = อายุ 55 เงินเดือน 51,000   ← อายุต่างกัน 25 ปี แต่เงินเดือนใกล้กัน

ก่อน scaling ระยะทางถูกครอบงำโดยเงินเดือน (สเกลใหญ่กว่าอายุพันเท่า) → ตอบ C
หลัง scaling อายุได้มีสิทธิ์มีเสียง → ตอบ B
นี่คือ "ผลพลิก" ที่พิสูจน์ว่าทำไม k-NN / k-Means / Neural Network ต้อง scale ก่อน
"""
from _style import apply, save, C
import matplotlib.pyplot as plt
import numpy as np

apply()
rng = np.random.default_rng(21)

# ประชากรพื้นหลัง — ใช้คำนวณ mean/std/min/max ให้สมจริง (ไม่ได้คิดจากแค่ 3 จุด)
pop_age = rng.uniform(22, 60, 60)
pop_sal = rng.uniform(20_000, 200_000, 60)

names = ["A", "B", "C"]
age = np.array([30.0, 32.0, 55.0])
sal = np.array([50_000.0, 62_000.0, 51_000.0])

all_age = np.concatenate([pop_age, age])
all_sal = np.concatenate([pop_sal, sal])


def zscore(v, ref):
    return (v - ref.mean()) / ref.std(ddof=0)


def minmax(v, ref):
    return (v - ref.min()) / (ref.max() - ref.min())


views = [
    ("① ก่อน scaling (ค่าดิบ)",
     np.column_stack([age, sal]),
     np.column_stack([pop_age, pop_sal]),
     ("อายุ (ปี)", "เงินเดือน (บาท)"), C["red"]),
    ("② Standardization (z-score)",
     np.column_stack([zscore(age, all_age), zscore(sal, all_sal)]),
     np.column_stack([zscore(pop_age, all_age), zscore(pop_sal, all_sal)]),
     ("อายุ (z)", "เงินเดือน (z)"), C["blue"]),
    ("③ Normalization (Min-Max)",
     np.column_stack([minmax(age, all_age), minmax(sal, all_sal)]),
     np.column_stack([minmax(pop_age, all_age), minmax(pop_sal, all_sal)]),
     ("อายุ (0–1)", "เงินเดือน (0–1)"), C["green"]),
]

fig, axes = plt.subplots(1, 3, figsize=(14.2, 5.4))

for ax, (title, M, P, (xl, yl), col) in zip(axes, views):
    ax.scatter(P[:, 0], P[:, 1], s=16, color=C["grey"], alpha=0.28, zorder=1)
    ax.scatter(M[:, 0], M[:, 1], s=190, color=col, zorder=4,
               edgecolor="white", linewidth=2.0)
    for i, nm in enumerate(names):
        ax.annotate(nm, M[i], ha="center", va="center", fontsize=12,
                    fontweight="bold", color="white", zorder=5)

    dAB = np.linalg.norm(M[0] - M[1])
    dAC = np.linalg.norm(M[0] - M[2])
    nearer = "B" if dAB < dAC else "C"
    for j, lab in enumerate(["B", "C"]):
        win = lab == nearer
        ax.plot([M[0, 0], M[j + 1, 0]], [M[0, 1], M[j + 1, 1]],
                color=C["ink"] if win else C["grey"],
                lw=2.6 if win else 1.3, ls="-" if win else ":",
                zorder=3, alpha=0.9)

    ax.set_title(title, fontsize=12.5)
    ax.set_xlabel(xl); ax.set_ylabel(yl)
    # วางกล่องผลลัพธ์ไว้ในแกน เพื่อไม่ให้กินพื้นที่ใต้ภาพ
    ax.text(0.03, 0.97,
            f"d(A,B) = {dAB:,.3f}\nd(A,C) = {dAC:,.3f}\n"
            f"→ ใกล้สุด = {nearer}",
            transform=ax.transAxes, ha="left", va="top", fontsize=10,
            linespacing=1.7, color=C["ink"] if nearer == "B" else C["red"],
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.45", facecolor="white",
                      edgecolor=C["ink"] if nearer == "B" else C["red"],
                      alpha=0.94, linewidth=1.2))
    print(f"{title:32s} d(A,B)={dAB:12,.3f}  d(A,C)={dAC:12,.3f} -> {nearer}")

fig.suptitle("ทำไมต้อง Feature Scaling — สเกลที่ต่างกันเปลี่ยนคำตอบของ k-NN ได้เลย",
             fontsize=14.5, fontweight="bold", y=0.99)
fig.text(0.5, 0.02,
         "A = อายุ 30 / เงินเดือน 50,000   ·   B = อายุ 32 / 62,000   ·   C = อายุ 55 / 51,000\n"
         "ค่าดิบ: เงินเดือนสเกลใหญ่กว่าอายุ ~1,000 เท่า → ระยะทางเป็นเรื่องของเงินเดือนล้วน ๆ ตอบ C  "
         "|  หลัง scale: อายุมีน้ำหนักเท่าเทียม ตอบ B",
         ha="center", fontsize=10.5, linespacing=1.8,
         bbox=dict(boxstyle="round,pad=0.55", facecolor="#FFF4E5",
                   edgecolor=C["orange"], linewidth=1.2))
fig.tight_layout(rect=[0, 0.17, 1, 0.93])
save(fig, "prep_scaling.png")
