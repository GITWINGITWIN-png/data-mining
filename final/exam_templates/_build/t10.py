from nbtools import md, code, build

TITLE = r"""
# T10 · Clustering (K-Means · เลือก k · Centroid/Profile · Cohesion/Separation · Hierarchical/Dendrogram)

**ใช้เมื่อโจทย์ถาม:** แบ่งกลุ่ม (ไม่มี label) · เตรียมข้อมูลสำหรับ clustering (ตัด id, normalize) · K-Means + parameters (k, n_init, max_iter) ·
เลือกจำนวน cluster (elbow/WCSS, silhouette, Davies–Bouldin) · ตีความ centroid / ตั้งชื่อกลุ่ม · จุดใหม่อยู่กลุ่มไหน ·
cohesion / separation · วาดบน PCA 2D · hierarchical clustering + dendrogram · เทียบกับ label จริง (ถ้ามี)

| ขั้น | ทำอะไร |
|---|---|
| 1 | แก้ **⚙️ CONFIG** — `ID_COL`, `FEATURES`, `K_FINAL` (k ที่โจทย์กำหนด หรือ None = เลือกอัตโนมัติจาก silhouette) |
| 2 | Run All · ตาราง k §2 · centroid §3 · จุดใหม่ §4 |
"""

CONFIG = r'''# ════════ ⚙️ CONFIG — แก้ cell นี้ให้ตรงโจทย์ ════════
DATA_PATH = "../data/utilities.csv"
ID_COL    = "Company"        # ชื่อ/รหัสแถว (ไม่ใช้คำนวณ ใช้ติดป้าย)
LABEL_COL = None             # ถ้าข้อมูลมี class จริง (ไว้เทียบหลัง cluster เท่านั้น ห้ามใช้ตอน cluster) · None = ไม่มี
DROP_COLS = []               # คอลัมน์ที่ไม่ใช้
FEATURES  = None             # list feature ที่ใช้ cluster · None = ตัวเลขทุกคอลัมน์ที่เหลือ
SCALE     = "standard"       # "standard" (z-score) | "minmax" | None — K-Means ใช้ระยะทาง ควร scale
K_RANGE   = range(2, 9)      # ช่วง k ที่ลอง
K_FINAL   = 4                # k ที่ใช้จริง (None = เลือก k ที่ silhouette สูงสุด)
N_INIT    = 50               # จำนวนรอบสุ่ม centroid เริ่มต้น (เลือกรอบที่ WCSS ต่ำสุด)
MAX_ITER  = 300
NEW_POINT = {"Fixed_charge": 1.10, "RoR": 11.0, "Cost": 160, "Load_factor": 56, "Demand_growth": 3.0,
             "Sales": 14000, "Nuclear": 0, "Fuel_Cost": 0.70}    # None = ข้าม
LINKAGE   = "ward"           # hierarchical: "ward" | "complete" | "average" | "single"
SEED = 42
MISSING_MARKERS, SHEET, CSV_SEP = ["?", "", " ", "NA"], 0, ","
'''

S = [
md(r"""
## §1 เตรียมข้อมูล: ตัด id/label · เลือก feature ตัวเลข · จัดการค่าว่าง · **scale**
K-Means ใช้ระยะ Euclidean → ตัวแปรหน่วยใหญ่ (เช่น Sales หลักหมื่น) จะครอบงำถ้าไม่ scale
"""),
code(r'''df = load_data(DATA_PATH)
check(df)
skip = [c for c in [ID_COL, LABEL_COL] + list(DROP_COLS) if c]
feats = FEATURES or [c for c in num_cols(df) if c not in skip]
cat_in = [c for c in df.columns if c not in skip + feats]
if cat_in:
    print("⚠️ คอลัมน์หมวดหมู่ที่ไม่ได้ใช้:", cat_in, "(ถ้าต้องใช้ → one-hot ก่อน: df = pd.get_dummies(df, columns=[...], dtype=int) แล้วใส่ใน FEATURES)")
data = df.dropna(subset=feats).reset_index(drop=True)
names = data[ID_COL].astype(str) if ID_COL and ID_COL in data else pd.Series(data.index.astype(str))
Xc = data[feats]
scaler = {"standard": StandardScaler(), "minmax": MinMaxScaler()}.get(SCALE)
Z = scaler.fit_transform(Xc) if scaler else Xc.values
print(f"ใช้ {len(feats)} feature: {feats} · {len(data)} แถว · scale = {SCALE}")
display(pd.concat({"original": Xc.agg(["mean", "std", "min", "max"]),
                   "scaled": pd.DataFrame(Z, columns=feats).agg(["mean", "std", "min", "max"])}).round(3))'''),
md(r"""**✍️ คำตอบ §1:** ตัด `…` (id / label) · ใช้ … feature ตัวเลข · normalize (z-score) เพราะหน่วยต่างกันมาก (std ของ … = … vs … = …) ไม่งั้น … จะครอบงำระยะทาง"""),

md(r"""
## §2 เลือกจำนวน cluster k
| เกณฑ์ | ดูอะไร | ดี = |
|---|---|---|
| **WCSS / SSE (inertia)** — cohesion | ผลรวมระยะ² ถึง centroid | หา "ข้อศอก" (elbow) ที่ลดลงช้าลง |
| **Silhouette** (−1..1) | cohesion + separation ต่อจุด | สูงสุด |
| **Davies–Bouldin** | ความกระจายในกลุ่ม / ระยะระหว่างกลุ่ม | ต่ำสุด |
"""),
code(r'''rows = []
for k in K_RANGE:
    km = KMeans(n_clusters=k, n_init=N_INIT, max_iter=MAX_ITER, random_state=SEED).fit(Z)
    rows.append({"k": k, "WCSS (inertia)": km.inertia_, "avg within-centroid dist²": km.inertia_ / len(Z),
                 "silhouette": silhouette_score(Z, km.labels_), "davies_bouldin": davies_bouldin_score(Z, km.labels_),
                 "sizes": sorted(np.bincount(km.labels_).tolist(), reverse=True)})
kt = pd.DataFrame(rows)
kt["WCSS drop"] = -kt["WCSS (inertia)"].diff()
display(kt.round(4))
fig, ax = plt.subplots(1, 3, figsize=(15, 3.6))
ax[0].plot(kt.k, kt["WCSS (inertia)"], "o-"); ax[0].set(title="Elbow (WCSS)", xlabel="k")
ax[1].plot(kt.k, kt.silhouette, "o-", color="C2"); ax[1].set(title="Silhouette (higher = better)", xlabel="k")
ax[2].plot(kt.k, kt.davies_bouldin, "o-", color="C3"); ax[2].set(title="Davies-Bouldin (lower = better)", xlabel="k")
plt.tight_layout(); plt.show()
k_sil = int(kt.loc[kt.silhouette.idxmax(), "k"]); k_db = int(kt.loc[kt.davies_bouldin.idxmin(), "k"])
K = K_FINAL or k_sil
print(f"✍️ silhouette สูงสุดที่ k = {k_sil} ({kt.silhouette.max():.4f}) · Davies–Bouldin ต่ำสุดที่ k = {k_db} ({kt.davies_bouldin.min():.4f}) · ใช้ k = {K}")'''),
md(r"""**✍️ คำตอบ §2:** WCSS ลดลงเร็วจนถึง k = … แล้วลดช้าลง (elbow) · silhouette สูงสุดที่ k = … · DB ต่ำสุดที่ k = … · เลือก k = … เพราะ … (ตัวเลข + ตีความได้ทางธุรกิจ)"""),

md(r"""## §3 K-Means ด้วย k ที่เลือก → สมาชิก · centroid (หน่วยเดิม + z-score) · profile · ตั้งชื่อกลุ่ม"""),
code(r'''km = KMeans(n_clusters=K, n_init=N_INIT, max_iter=MAX_ITER, random_state=SEED).fit(Z)
data["cluster"] = km.labels_
print(f"k = {K} · WCSS = {km.inertia_:.4f} · silhouette = {silhouette_score(Z, km.labels_):.4f} · iterations = {km.n_iter_}")
for c in range(K):
    mem = names[data.cluster == c].tolist()
    print(f"Cluster {c} ({len(mem)}): {', '.join(mem[:30])}{' …' if len(mem) > 30 else ''}")
cent_orig = data.groupby("cluster")[feats].mean()                       # centroid หน่วยเดิม
cent_z = pd.DataFrame(km.cluster_centers_, columns=feats)               # centroid หลัง scale
print("\ncentroid (หน่วยเดิม) + ค่าเฉลี่ยรวม:"); display(pd.concat([cent_orig, Xc.mean().to_frame("ALL").T]).round(3))
print("centroid (scaled; + = สูงกว่าค่าเฉลี่ย, − = ต่ำกว่า):"); display(cent_z.round(3))
plt.figure(figsize=(1 + 0.9 * len(feats), 0.6 * K + 1.5))
sns.heatmap(cent_z, annot=True, fmt=".2f", cmap="coolwarm", center=0); plt.title("Cluster profile (scaled centroids)"); plt.ylabel("cluster"); plt.show()
# คำอธิบายอัตโนมัติ: ตัวแปรที่ |z| ≥ 0.5
for c in range(K):
    hi = [f for f in feats if cent_z.loc[c, f] >= 0.5]; lo = [f for f in feats if cent_z.loc[c, f] <= -0.5]
    print(f"✍️ Cluster {c} (n={int((data.cluster == c).sum())}): สูง → {', '.join(hi) or '-'} | ต่ำ → {', '.join(lo) or '-'}")'''),
md(r"""**✍️ คำตอบ §3:** Cluster 0 = … (… สูง, … ต่ำ) → ตั้งชื่อ "…" · Cluster 1 = … · …"""),

md(r"""## §4 จุดใหม่อยู่ cluster ไหน (scale ด้วย scaler ตัวเดิม → หา centroid ที่ใกล้สุด)"""),
code(r'''if NEW_POINT is not None:
    newp = new_data(NEW_POINT)[feats]
    zn = scaler.transform(newp) if scaler else newp.values
    d = np.sqrt(((km.cluster_centers_ - zn) ** 2).sum(axis=1))
    display(pd.DataFrame({"distance to centroid": d}, index=[f"cluster {c}" for c in range(K)]).round(4))
    print("จุดใหม่หลัง scale:", np.round(zn[0], 3))
    print(f"✍️ จุดใหม่อยู่ cluster {int(km.predict(zn)[0])} (ระยะถึง centroid ใกล้สุด = {d.min():.4f})")'''),

md(r"""
## §5 Cohesion & Separation + silhouette ต่อกลุ่ม
- **Cohesion** = ความแน่นในกลุ่ม (WCSS ต่อกลุ่ม, ระยะเฉลี่ยถึง centroid) — ยิ่งต่ำยิ่งดี
- **Separation** = ระยะห่างระหว่าง centroid — ยิ่งมากยิ่งดี
"""),
code(r'''sil = silhouette_samples(Z, km.labels_)
coh = []
for c in range(K):
    Zc = Z[km.labels_ == c]; d = np.sqrt(((Zc - km.cluster_centers_[c]) ** 2).sum(axis=1))
    coh.append({"cluster": c, "n": len(Zc), "WCSS": (d ** 2).sum(), "avg dist to centroid": d.mean(), "avg silhouette": sil[km.labels_ == c].mean()})
display(pd.DataFrame(coh).round(4))
sep = pd.DataFrame(np.sqrt(((km.cluster_centers_[:, None, :] - km.cluster_centers_[None, :, :]) ** 2).sum(-1)),
                   index=[f"C{c}" for c in range(K)], columns=[f"C{c}" for c in range(K)])
print("ระยะระหว่าง centroid (separation):"); display(sep.round(3))
neg = names[sil < 0].tolist()
print(f"✍️ silhouette เฉลี่ย {sil.mean():.4f} · จุดที่ silhouette < 0 (อาจอยู่ผิดกลุ่ม): {neg or '-'}")'''),

md(r"""## §6 ภาพ cluster บน PCA 2D (ใส่ชื่อจุด)"""),
code(r'''pca = PCA(n_components=2, random_state=SEED).fit(Z)
P = pca.transform(Z); C = pca.transform(km.cluster_centers_)
plt.figure(figsize=(8, 6))
sns.scatterplot(x=P[:, 0], y=P[:, 1], hue=data.cluster.astype(str), palette="tab10", s=70)
plt.scatter(C[:, 0], C[:, 1], marker="X", s=250, c="k", label="centroid")
if len(data) <= 80:
    for i, n in enumerate(names):
        plt.annotate(n, P[i], fontsize=7, alpha=.8, xytext=(3, 3), textcoords="offset points")
if NEW_POINT is not None:
    pn = pca.transform(zn); plt.scatter(pn[:, 0], pn[:, 1], marker="*", s=400, c="gold", edgecolor="k", label="new point")
plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})"); plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
plt.title(f"K-Means k={K} on PCA 2D ({pca.explained_variance_ratio_.sum():.1%} variance)"); plt.legend(bbox_to_anchor=(1, 1)); plt.tight_layout(); plt.show()
# scatter 2 feature เดิม (✏️ เลือกคู่)
FX, FY = feats[0], feats[1]
sns.scatterplot(data=data, x=FX, y=FY, hue=data.cluster.astype(str), palette="tab10", s=60); plt.title(f"{FY} vs {FX}"); plt.show()'''),
md(r"""**✍️ คำตอบ §6:** บนภาพ PCA (…% ของความแปรปรวน) cluster … แยกชัด (separation ดี) · cluster … กับ … อยู่ใกล้กัน/ซ้อนบางส่วน · จุด … อยู่ขอบกลุ่ม"""),

md(r"""
## §7 Hierarchical clustering + Dendrogram
- agglomerative: เริ่มทุกจุดเป็นกลุ่มเดี่ยว → รวมคู่ที่ใกล้สุดทีละขั้น
- linkage: **single** (ระยะคู่ที่ใกล้สุด) · **complete** (ไกลสุด) · **average** · **ward** (เพิ่ม WCSS น้อยสุด)
- ตัด dendrogram ที่ความสูงที่ทำให้ได้ k กลุ่ม
"""),
code(r'''from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
Lk = linkage(Z, method=LINKAGE)
plt.figure(figsize=(max(8, 0.35 * len(data)), 4.5))
dendrogram(Lk, labels=names.tolist() if len(data) <= 80 else None, leaf_rotation=90, color_threshold=Lk[-(K - 1), 2])
plt.axhline(Lk[-(K - 1), 2], color="r", ls="--", label=f"cut → {K} clusters"); plt.title(f"Dendrogram ({LINKAGE} linkage)"); plt.legend(); plt.show()
data["hier"] = fcluster(Lk, t=K, criterion="maxclust") - 1
print(f"hierarchical ({LINKAGE}) silhouette = {silhouette_score(Z, data.hier):.4f} vs K-Means {silhouette_score(Z, km.labels_):.4f}")
print("เทียบ K-Means (แถว) กับ Hierarchical (คอลัมน์):"); display(pd.crosstab(data.cluster, data.hier))
for c in sorted(data.hier.unique()):
    print(f"H{c}: {', '.join(names[data.hier == c].tolist()[:30])}")'''),

md(r"""## §8 เทียบกับ label จริง (ถ้ามี — ใช้ประเมินภายนอกเท่านั้น)"""),
code(r'''if LABEL_COL and LABEL_COL in data:
    from sklearn.metrics import adjusted_rand_score
    display(pd.crosstab(data[LABEL_COL], data.cluster, margins=True))
    print(f"✍️ Adjusted Rand Index = {adjusted_rand_score(data[LABEL_COL], data.cluster):.4f} (1 = ตรงกันสมบูรณ์, 0 = สุ่ม)")
else:
    print("ไม่มี LABEL_COL → ข้าม")
data.to_csv("t10_clusters.csv", index=False); print("saved t10_clusters.csv")'''),
]

if __name__ == "__main__":
    build("../T10_clustering.ipynb", TITLE, CONFIG, S)
