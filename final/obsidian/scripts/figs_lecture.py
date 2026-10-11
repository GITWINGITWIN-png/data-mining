"""ภาพประกอบโน้ต Lecture (LEC 03–10) — ทุกภาพคำนวณจากข้อมูลจริง/ตัวเลขในสไลด์

รัน:  cd final/obsidian/scripts && ../../.venv/bin/python figs_lecture.py
ภาพไปอยู่ที่ final/obsidian/assets/
"""
from math import log2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from _style import apply, save, C, DATA, ROOT

apply()


# ── 1 · leakage: ลำดับที่ถูก vs ผิด ─────────────────────────────────────────────────────
def box(ax, x, y, w, h, text, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02", fc=color, ec=C["ink"], lw=1.2, alpha=0.9))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9.5, linespacing=1.5)


fig, axes = plt.subplots(2, 1, figsize=(13, 7.4))
for ax, title, steps, col in [
    (axes[0], "✗ ผิด — preprocess ทั้งชุดก่อน split (leak)",
     ["ข้อมูลทั้งหมด", "fillna / scale / SMOTE\nเรียนค่าจากทุกแถว\n(รวม test ไปด้วย)", "split\ntrain / test", "train → test\nผลดีเกินจริง"], C["red"]),
    (axes[1], "✓ ถูก — split ก่อน · เรียนค่าจาก train เท่านั้น",
     ["ข้อมูลทั้งหมด", "split train / test\n(ล็อก test ไว้)", "fit preprocess\nบน train เท่านั้น\ntransform test", "train → test\nผลเชื่อถือได้"], C["green"])]:
    ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis("off"); ax.set_title(title, color=col)
    for i, s in enumerate(steps):
        box(ax, 0.2 + i * 2.45, 1.3, 2.1, 1.5, s, "#FFFFFF" if i else "#EEF3F8")
        if i:
            ax.annotate("", (0.2 + i * 2.45, 2.05), (0.2 + i * 2.45 - 0.33, 2.05),
                        arrowprops=dict(arrowstyle="->", color=C["ink"], lw=1.5))
    ax.text(5, 0.6, "สไลด์ KNN p.60: \"Always split the dataset into training and test sets first,\nthen apply preprocessing separately.\"" if col == C["green"] else
            "ตัวอย่างในสไลด์เอง: KNN p.56 (impute ทั้งชุด) · Imbalanced p.21 (SMOTE ก่อน split)",
            ha="center", fontsize=9.5, color=C["grey"])
save(fig, "lec_leakage.png")

# ── 2 · 5-fold CV ──────────────────────────────────────────────────────────────────
acc = [80, 88, 85, 78, 84]
fig, ax = plt.subplots(figsize=(11, 3.8))
for r in range(5):
    for f in range(5):
        ax.add_patch(plt.Rectangle((f, 4 - r), 0.95, 0.8, fc=C["orange"] if f == r else C["sky"], ec="white"))
        ax.text(f + 0.475, 4.4 - r, "test" if f == r else "train", ha="center", va="center", fontsize=9)
    ax.text(5.2, 4.4 - r, f"รอบ {r+1}: accuracy = {acc[r]}%", va="center", fontsize=10.5)
ax.text(5.2, -0.3, f"เฉลี่ย = {np.mean(acc):.0f}%  ± {np.std(acc, ddof=1):.1f}% (sd)", fontsize=12, fontweight="bold", color=C["green"])
ax.set_xlim(0, 8.3); ax.set_ylim(-0.7, 5); ax.axis("off")
ax.set_title("5-fold Cross-Validation — ทุกแถวได้เป็น test 1 ครั้ง (ตัวเลขจากสไลด์ Tree p.74–76)")
save(fig, "lec_kfold.png")

# ── 3 · threshold trade-off (Riding Mowers p.70–72) ─────────────────────────────────
pr = pd.read_csv(DATA / "riding_mowers_probs.csv")
ts = np.linspace(0.01, 0.99, 99)
P, R, A = [], [], []
for t in ts:
    pred = pr.Prob_Owner >= t
    tp = (pred & (pr.Actual == "Owner")).sum(); fp = (pred & (pr.Actual == "Nonowner")).sum()
    fn = (~pred & (pr.Actual == "Owner")).sum(); tn = 24 - tp - fp - fn
    P.append(tp / (tp + fp) if tp + fp else np.nan); R.append(tp / (tp + fn)); A.append((tp + tn) / 24)
fig, ax = plt.subplots(1, 2, figsize=(14, 4.8), gridspec_kw={"width_ratios": [1.4, 1]})
ax[0].plot(ts, P, color=C["blue"], lw=2.2, label="precision")
ax[0].plot(ts, R, color=C["red"], lw=2.2, label="recall")
ax[0].plot(ts, A, color=C["grey"], lw=1.6, ls="--", label="accuracy")
for t in (0.25, 0.5, 0.75):
    ax[0].axvline(t, color=C["ink"], lw=0.8, alpha=0.4)
ax[0].set_xlabel("cutoff (threshold)"); ax[0].set_ylim(0, 1.05); ax[0].legend(loc="lower left")
ax[0].set_title("ขยับ threshold: recall ↔ precision แลกกัน")
ax[1].axis("off")
rows = [["cutoff", "TP", "FN", "FP", "TN", "acc", "P", "R"],
        ["0.25", 11, 1, 4, 8, "0.792", "0.733", "0.917"],
        ["0.50", 11, 1, 2, 10, "0.875", "0.846", "0.917"],
        ["0.75", 7, 5, 1, 11, "0.750", "0.875", "0.583"]]
tb = ax[1].table(cellText=rows[1:], colLabels=rows[0], loc="center", cellLoc="center")
tb.scale(1, 2); tb.set_fontsize(11)
ax[1].set_title("Riding Mowers 24 ราย (KNN p.72)")
save(fig, "lec_threshold.png")

# ── 4 · KNN: เลือก k (p.42–43) ─────────────────────────────────────────────────────
k = np.arange(1, 19)
tr = [0, 16.67, 11.11, 22.22, 11.11, 27.78, 22.22, 22.22, 22.22, 22.22, 16.67, 16.67, 11.11, 11.11, 5.56, 16.67, 11.11, 50]
va = [33.33] * 7 + [16.67, 16.67, 16.67, 33.33, 16.67, 33.33, 16.67, 33.33, 33.33, 33.33, 50]
fig, ax = plt.subplots(1, 2, figsize=(14, 4.8))
ax[0].plot(k, tr, "o-", color=C["blue"], label="% error training")
ax[0].plot(k, va, "s-", color=C["red"], label="% error validation")
ax[0].scatter([8], [16.67], s=260, facecolor="none", edgecolor=C["green"], lw=2.5, zorder=5)
ax[0].annotate("k = 8 (ต่ำสุดตัวแรก)", (8, 16.67), (9.5, 4), arrowprops=dict(arrowstyle="->"), fontsize=10)
ax[0].annotate("k = n = 18 → naïve rule", (18, 50), (11, 44), arrowprops=dict(arrowstyle="->"), fontsize=10)
ax[0].set_xlabel("k"); ax[0].set_ylabel("% error"); ax[0].legend(); ax[0].set_xticks(k)
ax[0].set_title("เลือก k จาก validation error (สไลด์ KNN p.43)")
rm = pd.read_csv(DATA / "riding_mowers.csv")
for own, col, mk in [("Owner", C["blue"], "o"), ("Nonowner", C["orange"], "s")]:
    s = rm[rm.Ownership == own]
    ax[1].scatter(s.Income, s.Lot_Size, color=col, marker=mk, s=60, label=own, edgecolor="white")
ax[1].scatter([60], [20], marker="*", s=380, color=C["red"], label="ครัวเรือนใหม่ (60, 20)", zorder=5)
d = np.sqrt((rm.Income - 60) ** 2 + (rm.Lot_Size - 20) ** 2)
near = rm.loc[np.argsort(d.values)[:3]]
ax[1].scatter(near.Income, near.Lot_Size, s=260, facecolor="none", edgecolor=C["red"], lw=2, label="เพื่อนบ้าน 3 ตัวที่ใกล้สุด")
ax[1].set_xlabel("Income ($000s)"); ax[1].set_ylabel("Lot_Size (000 sqft)"); ax[1].legend(fontsize=9, loc="lower right")
ax[1].set_title("k = 3: เพื่อนบ้าน Owner, Owner, Nonowner → Owner")
save(fig, "lec_knn_k.png")

# ── 5 · sigmoid (KNN p.16–17) ───────────────────────────────────────────────────────
b1 = (np.log(0.81 / 0.19) - np.log(0.42 / 0.58)) / 10
b0 = np.log(0.42 / 0.58) - 35 * b1
age = np.linspace(15, 65, 300)
fig, ax = plt.subplots(1, 2, figsize=(14, 4.6))
p = 1 / (1 + np.exp(-(b0 + b1 * age)))
ax[0].plot(age, p, color=C["blue"], lw=2.6)
ax[0].axhline(0.5, color=C["grey"], ls="--"); ax[0].text(16, 0.53, "threshold 0.5", color=C["grey"])
for a, pp, lab in [(35, 0.42, "35 ปี → 42% → NO"), (45, 0.81, "45 ปี → 81% → YES")]:
    ax[0].scatter([a], [pp], color=C["red"], s=80, zorder=5); ax[0].annotate(lab, (a, pp), (a + 2, pp - 0.15), fontsize=10)
ax[0].set_xlabel("Age"); ax[0].set_ylabel("P(รับประกัน = yes)")
ax[0].set_title(f"p = 1/(1+e^-(b0+b1·Age))  ฟิตจาก 2 จุดในสไลด์: b0 = {b0:.2f}, b1 = {b1:.3f}")
z = np.linspace(-6, 6, 300)
ax[1].plot(z, 1 / (1 + np.exp(-z)), color=C["ink"], lw=2.4)
ax[1].set_xlabel("z = b0 + b1·x1 + …  (log-odds)"); ax[1].set_ylabel("p")
for zz in (-2, 0, 2):
    ax[1].scatter([zz], [1 / (1 + np.exp(-zz))], color=C["orange"], s=60, zorder=5)
    ax[1].annotate(f"z={zz} → p={1/(1+np.exp(-zz)):.2f}", (zz, 1 / (1 + np.exp(-zz))), (zz + 0.4, 1 / (1 + np.exp(-zz)) - 0.12), fontsize=9.5)
ax[1].set_title("sigmoid: z ใดก็ได้ → p ในช่วง (0, 1)")
save(fig, "lec_sigmoid.png")

# ── 6 · impurity + Weather gains ─────────────────────────────────────────────────────
pp = np.linspace(0.001, 0.999, 300)
ent = -(pp * np.log2(pp) + (1 - pp) * np.log2(1 - pp))
gin = 1 - pp ** 2 - (1 - pp) ** 2
mis = 1 - np.maximum(pp, 1 - pp)
fig, ax = plt.subplots(1, 2, figsize=(14, 4.6))
ax[0].plot(pp, ent, color=C["blue"], lw=2.4, label="Entropy (max 1)")
ax[0].plot(pp, gin, color=C["orange"], lw=2.4, label="Gini (max 0.5)")
ax[0].plot(pp, mis, color=C["grey"], lw=2, ls="--", label="Misclassification error")
ax[0].set_xlabel("p = สัดส่วนคลาส 1 ใน node"); ax[0].legend(); ax[0].set_title("impurity สูงสุดที่ 50:50 · ต่ำสุด (0) เมื่อ pure (Tree p.28)")
w = pd.read_csv(DATA / "weather.csv")
def H(s): q = s.value_counts(normalize=True); return -(q * np.log2(q)).sum()
gains = {a: H(w.Class) - sum(len(g) / 14 * H(g.Class) for _, g in w.groupby(a)) for a in ["Outlook", "Humidity", "Windy", "Temperature"]}
bars = ax[1].bar(gains.keys(), gains.values(), color=[C["green"], C["sky"], C["sky"], C["sky"]])
for b_, v in zip(bars, gains.values()):
    ax[1].text(b_.get_x() + b_.get_width() / 2, v + 0.005, f"{v:.3f}", ha="center")
ax[1].set_ylabel("Information Gain"); ax[1].set_title("Weather 14 records: Outlook ได้ IG สูงสุด → root (Tree p.10, 39)")
save(fig, "lec_impurity_gain.png")

# ── 7 · overfitting tree vs RF (Social Network Ads) ────────────────────────────────
ads = pd.read_csv(ROOT / "W12" / "Social_Network_Ads_2.csv"); ads["Gender"] = (ads.Gender == "Male").astype(int)
X, y = ads[["Gender", "Age", "EstimatedSalary"]], ads.Purchased
cv = StratifiedKFold(10, shuffle=True, random_state=42)
depths = list(range(1, 16))
trn, tst = [], []
for d_ in depths:
    r = cross_validate(DecisionTreeClassifier(max_depth=d_, random_state=42), X, y, cv=cv, return_train_score=True)
    trn.append(r["train_score"].mean()); tst.append(r["test_score"].mean())
rf = cross_validate(RandomForestClassifier(min_samples_leaf=5, random_state=42), X, y, cv=cv)["test_score"].mean()
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.plot(depths, trn, "o-", color=C["blue"], label="training accuracy")
ax.plot(depths, tst, "s-", color=C["red"], label="CV accuracy")
ax.axhline(rf, color=C["green"], ls="--", lw=2, label=f"Random Forest (CV) = {rf:.3f}")
best = depths[int(np.argmax(tst))]
ax.axvline(best, color=C["grey"], lw=1); ax.text(best + 0.2, 0.985, f"CV ดีที่สุดที่ depth = {best}", color=C["grey"])
ax.fill_between(depths, tst, trn, color=C["orange"], alpha=0.15)
ax.text(10, (trn[9] + tst[9]) / 2, "ช่องว่าง = overfitting", color=C["orange"], fontweight="bold")
ax.set_xlabel("max_depth (ความซับซ้อนของ tree)"); ax.set_ylabel("accuracy"); ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5))
ax.set_title("Decision Tree: train ↑ เรื่อย ๆ แต่ CV ขึ้นแล้วลง (Social Network Ads, 10-fold)")
save(fig, "lec_tree_overfit.png")

# ── 8 · PCA scree raw vs standardized (cereals, PCA p.16/18) ──────────────────────────
raw = np.array([55.53, 37.25, 3.84, 2.75, 0.56, 0.03]); raw_cum = [55.53, 92.78, 96.62, 99.38, 99.93, 99.97]
std = np.array([27.66, 24.34, 14.35, 8.40, 7.46, 5.56]); std_cum = [27.66, 51.99, 66.35, 74.75, 82.20, 87.77]   # ค่าสะสมตามสไลด์
fig, ax = plt.subplots(1, 2, figsize=(14, 4.6))
for a_, vals, cum, title in [(ax[0], raw, raw_cum, "ไม่ normalize: PC1 = sodium, PC2 = potassium (p.16)"),
                             (ax[1], std, std_cum, "standardize แล้ว: กระจายหลาย PC (p.18)")]:
    idx = np.arange(1, 7)
    a_.bar(idx, vals, color=C["sky"], label="% variance")
    a_.plot(idx, cum, "o-", color=C["red"], label="cumulative %")
    for i, v in zip(idx, cum):
        a_.text(i, v + 2, f"{v:.1f}", ha="center", fontsize=9)
    a_.axhline(80, color=C["grey"], ls="--", lw=1); a_.text(0.55, 82, "80%", color=C["grey"])
    a_.set_ylim(0, 108); a_.set_xticks(idx, [f"PC{i}" for i in idx]); a_.set_title(title); a_.legend(loc="center right")
save(fig, "lec_pca_scree.png")

# ── 9 · SMOTE + accuracy paradox ─────────────────────────────────────────────────────
rng = np.random.default_rng(1992)
maj = rng.normal([0, 0], [1.2, 1.0], (120, 2)); mino = rng.normal([2.6, 2.2], [0.5, 0.5], (12, 2))
fig, ax = plt.subplots(1, 2, figsize=(14, 4.8))
ax[0].scatter(*maj.T, s=14, color=C["grey"], alpha=0.5, label="majority")
ax[0].scatter(*mino.T, s=45, color=C["red"], label="minority (จริง)")
xi = mino[np.argmin(np.linalg.norm(mino - mino.mean(0), axis=1))]; dd = np.linalg.norm(mino - xi, axis=1); nb = mino[np.argsort(dd)[1:6]]
for n_ in nb:
    ax[0].plot([xi[0], n_[0]], [xi[1], n_[1]], color=C["red"], lw=0.8, ls=":")
new = [xi + lam * (n_ - xi) for n_, lam in zip(nb, rng.uniform(0, 1, 5))]
ax[0].scatter(*np.array(new).T, s=70, marker="^", color=C["orange"], edgecolor=C["ink"], label="จุดสังเคราะห์ SMOTE", zorder=5)
ax[0].scatter(*xi, s=140, facecolor="none", edgecolor=C["ink"], lw=2)
ax[0].set_title("SMOTE: x_new = x_i + λ(x_nn − x_i), λ ~ U(0,1) (Imbalanced p.17)"); ax[0].legend(fontsize=9)
models = ["ทาย Legit ทุกแถว\n(majority)", "โมเดลในสไลด์\n(p.11)"]
accs, recs, f1s = [0.98, 0.955], [0.0, 0.25], [0.0, 0.182]
xx = np.arange(2); wdt = 0.26
for off, vals, lab, col in [(-wdt, accs, "accuracy", C["grey"]), (0, recs, "recall (fraud)", C["red"]), (wdt, f1s, "F1 (fraud)", C["orange"])]:
    bb = ax[1].bar(xx + off, vals, wdt, label=lab, color=col)
    for b_, v in zip(bb, vals):
        ax[1].text(b_.get_x() + b_.get_width() / 2, v + 0.02, f"{v:.3f}", ha="center", fontsize=9)
ax[1].set_xticks(xx, models); ax[1].set_ylim(0, 1.12); ax[1].legend()
ax[1].set_title("Accuracy paradox: fraud 20 / 1,000 แถว")
save(fig, "lec_smote_paradox.png")

# ── 10 · K-Means 9 จุด (HW9) ─────────────────────────────────────────────────────────
P9 = {"A1": (3, 8), "A2": (9, 4), "A3": (4, 9), "A4": (2, 2), "A5": (10, 5), "A6": (2, 4), "A7": (6, 8), "A8": (4, 3), "A9": (4, 7)}
names = list(P9); Xk = np.array(list(P9.values()), float); cen = Xk[[0, 3, 6]].copy()
cols = [C["red"], C["green"], C["blue"]]
fig, axs = plt.subplots(1, 3, figsize=(15, 4.6), sharey=True)
for it, ax_ in enumerate(axs, start=1):
    lab = ((Xk[:, None] - cen[None]) ** 2).sum(2).argmin(1)
    for kk in range(3):
        m = lab == kk
        ax_.scatter(*Xk[m].T, s=90, color=cols[kk], edgecolor="white")
        ax_.scatter(*cen[kk], marker="X", s=200, color=cols[kk], edgecolor=C["ink"])
    for n_, (a, b) in zip(names, Xk):
        ax_.annotate(n_, (a, b), (4, 4), textcoords="offset points", fontsize=9)
    new = np.array([Xk[lab == kk].mean(0) for kk in range(3)])
    sse = sum(((Xk[lab == kk] - new[kk]) ** 2).sum() for kk in range(3))
    ax_.set_title(f"รอบ {it} · SSE = {sse:.2f}")
    ax_.set_xlim(0, 11.5); ax_.set_ylim(0, 10.5)
    cen = new
fig.suptitle("K-Means 9 จุด (HW9) · ✕ = centroid ที่ใช้ assign รอบนั้น · seed = A1, A4, A7 · รอบ 3 ไม่มีจุดย้าย → converge", y=1.03)
save(fig, "lec_kmeans_iter.png")

# ── 11 · elbow + silhouette (Utilities) ──────────────────────────────────────────────
u = pd.read_csv(DATA / "utilities.csv").set_index("Company")
Z = StandardScaler().fit_transform(u)
ks = range(2, 11); wcss, sil = [], []
for kk in ks:
    km = KMeans(kk, n_init=50, random_state=42).fit(Z); wcss.append(km.inertia_); sil.append(silhouette_score(Z, km.labels_))
fig, ax = plt.subplots(1, 2, figsize=(14, 4.4))
ax[0].plot(list(ks), wcss, "o-", color=C["blue"]); ax[0].set_title("Elbow: WCSS ลดเสมอเมื่อ k เพิ่ม — หาจุดที่เริ่มแบน")
ax[1].plot(list(ks), sil, "o-", color=C["red"]); ax[1].set_title("Silhouette: สูง = กลุ่มแน่น + แยกกันดี")
ax[1].scatter([ks[int(np.argmax(sil))]], [max(sil)], s=200, facecolor="none", edgecolor=C["green"], lw=2.5)
for a_ in ax: a_.set_xlabel("k")
fig.suptitle("22 Public Utilities (สไลด์ clustering p.10) · standardized · n_init = 50", y=1.02)
save(fig, "lec_elbow_silhouette.png")

# ── 12 · Apriori lattice ACD (p.15 / p.24) ──────────────────────────────────────────
T = [set("ACD"), set("BCE"), set("ABCE"), set("BE"), set("ABCE")]
sup = lambda s: sum(set(s) <= t for t in T)
from itertools import combinations
levels = [["".join(c) for c in combinations("ABCDE", r)] for r in (1, 2, 3)]
fig, ax = plt.subplots(figsize=(15, 5.4))
pos = {}
for r, lev in enumerate(levels):
    for i, s in enumerate(lev):
        x = (i + 0.5) / len(lev) * 15; yv = 4 - r * 1.6; pos[s] = (x, yv)
for r in (1, 2):
    for s in levels[r]:
        for sub in combinations(s, r):
            a = "".join(sub)
            ax.plot([pos[a][0], pos[s][0]], [pos[a][1], pos[s][1]], color="#DDDDDD", lw=0.6, zorder=1)
for s, (x, yv) in pos.items():
    cnt = sup(s); freq = cnt >= 3
    pruned = len(s) > 1 and any(sup("".join(sub)) < 3 for sub in combinations(s, len(s) - 1))
    col = C["green"] if freq else ("#EEEEEE" if pruned else C["orange"])
    ax.add_patch(FancyBboxPatch((x - 0.32, yv - 0.25), 0.64, 0.5, boxstyle="round,pad=0.02", fc=col, ec=C["ink"], lw=0.8, zorder=2))
    ax.text(x, yv + 0.02, f"{s}\n{'—' if pruned else cnt}", ha="center", va="center", fontsize=8.5, zorder=3)
ax.set_xlim(0, 15); ax.set_ylim(-0.4, 4.6); ax.axis("off")
ax.text(0.1, -0.15, "■ เขียว = frequent (count ≥ 3 = 60%)   ■ ส้ม = นับแล้วไม่ถึง minsup   ■ เทา = ถูก prune (มี subset ไม่ frequent → ไม่ต้องนับ)", fontsize=10)
ax.set_title("Apriori บนฐานข้อมูล 5 transactions (สไลด์ Apriori p.15): L1 = {A,B,C,E} → L2 = {AC,BC,BE,CE} → L3 = {BCE}")
save(fig, "lec_apriori_lattice.png")
