"""บทที่ 4 — Unsupervised Discretization 3 วิธี บนข้อมูลชุดเดียวกัน

จำลองข้อมูลตามที่สไลด์บรรยาย: "Data consists of four groups of points and two outliers"
แล้วตัดเป็น 4 ช่วงด้วย Equal Width / Equal Frequency / K-means
เพื่อให้เห็นว่า "ข้อมูลเดียวกัน วิธีต่างกัน ได้ขอบเขตคนละแบบ"
"""
from _style import apply, save, C
import matplotlib.pyplot as plt
import numpy as np

apply()
rng = np.random.default_rng(5)

# 4 กลุ่ม + 2 outliers ตามที่สไลด์บรรยาย
groups = np.concatenate([
    rng.normal(10, 1.2, 60), rng.normal(22, 1.2, 60),
    rng.normal(34, 1.2, 60), rng.normal(46, 1.2, 60),
])
x = np.concatenate([groups, np.array([78.0, 92.0])])   # 2 outliers ลากช่วงขวาให้ยาว
K = 4


def equal_width(x, k):
    """แบ่งช่วงให้ 'กว้างเท่ากัน' — ไม่สนว่าแต่ละช่วงมีข้อมูลกี่จุด"""
    return np.linspace(x.min(), x.max(), k + 1)


def equal_frequency(x, k):
    """แบ่งให้แต่ละช่วงมี 'จำนวนจุดเท่ากัน' — ใช้ percentile เป็นขอบ"""
    return np.percentile(x, np.linspace(0, 100, k + 1))


def kmeans_1d(x, k, iters=100):
    """K-means 1 มิติแบบเขียนเอง (ไม่มี sklearn ในเครื่อง)
    เริ่มจากศูนย์กลางที่ percentile กระจายทั่ว แล้ววนจนนิ่ง"""
    cent = np.percentile(x, np.linspace(10, 90, k))
    for _ in range(iters):
        lab = np.abs(x[:, None] - cent[None, :]).argmin(axis=1)
        new = np.array([x[lab == j].mean() if (lab == j).any() else cent[j]
                        for j in range(k)])
        if np.allclose(new, cent):
            break
        cent = np.sort(new)
    # ขอบเขต = จุดกึ่งกลางระหว่างศูนย์กลางที่ติดกัน
    edges = [x.min()] + list((cent[:-1] + cent[1:]) / 2) + [x.max()]
    return np.array(edges), cent


methods = [
    ("Equal Width", equal_width(x, K), C["blue"],
     "ช่วงกว้างเท่ากันทุกช่วง\n→ outlier ทำให้ 3 ช่วงขวาแทบว่างเปล่า"),
    ("Equal Frequency", equal_frequency(x, K), C["orange"],
     "แต่ละช่วงมีจำนวนจุดเท่ากัน\n→ ช่วงขวากว้างมากเพื่อกลืน outlier"),
    ("K-means", kmeans_1d(x, K)[0], C["green"],
     "ตัดตามการเกาะกลุ่มจริงของข้อมูล\n→ ตรงกับ 4 กลุ่มธรรมชาติมากที่สุด"),
]

fig, axes = plt.subplots(3, 1, figsize=(12.5, 8.2), sharex=True)

for ax, (name, edges, col, note) in zip(axes, methods):
    counts, _ = np.histogram(x, bins=edges)
    for i in range(len(edges) - 1):
        ax.axvspan(edges[i], edges[i + 1], color=col,
                   alpha=0.10 + 0.07 * (i % 2), zorder=0)
        mid = (edges[i] + edges[i + 1]) / 2
        ax.text(mid, 0.72, f"bin {i+1}\nn = {counts[i]}", ha="center",
                va="center", fontsize=9.5, fontweight="bold", color=col)
    for e in edges:
        ax.axvline(e, color=col, lw=1.8, ls="--", zorder=2)
    ax.scatter(x, rng.normal(0.22, 0.045, len(x)), s=26, color=C["ink"],
               alpha=0.55, zorder=3)
    ax.set_ylim(0, 1.0)
    ax.set_yticks([])
    ax.set_title(f"{name}  —  {note}", fontsize=11.5, loc="left", pad=6)
    ax.grid(False)

axes[-1].set_xlabel("ค่าของตัวแปรต่อเนื่อง  (ข้อมูล 4 กลุ่ม + outlier 2 จุดที่ 78 และ 92)")
fig.suptitle("Discretization — ข้อมูลชุดเดียวกัน ตัด 4 ช่วง ด้วย 3 วิธี ได้ผลต่างกัน",
             fontsize=14.5, fontweight="bold", y=0.98)
fig.tight_layout(rect=[0, 0, 1, 0.95])
save(fig, "prep_discretization.png")

for name, edges, _, _ in methods:
    print(f"{name:17s} ขอบเขต: " + " | ".join(f"{e:.1f}" for e in edges))
