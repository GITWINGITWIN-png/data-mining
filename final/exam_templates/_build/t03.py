from nbtools import md, code, build

TITLE = r"""
# T03 · PCA (Dimensionality Reduction + 2D Visualization)

**ใช้เมื่อโจทย์ถาม:** ทำ PCA · explained variance / cumulative · ต้องใช้กี่ component (80%/90%/95%, eigenvalue > 1, scree/elbow) ·
loadings (ตัวแปรไหนขับ PC1/PC2) · scatter 2D ระบายสีตาม class/cluster · PCA ก่อนสร้างโมเดล "ดีขึ้นไหม" · แปลงข้อมูลใหม่เป็น PC

| ขั้น | ทำอะไร |
|---|---|
| 1 | แก้ **⚙️ CONFIG** · Run All |
| 2 | อ่านผลตาม § ที่โจทย์ถาม · copy ประโยค `✍️` |

> **ต้อง standardize ก่อน PCA เสมอ** (ยกเว้นโจทย์บอกไม่ต้อง) — ไม่งั้นตัวแปรหน่วยใหญ่ (เช่น proline หลักพัน) จะครอง PC1
"""

CONFIG = r'''# ════════ ⚙️ CONFIG — แก้ cell นี้ให้ตรงโจทย์ ════════
DATA_PATH = "../practice/data/p4_wine.csv"
TARGET    = "cultivar"     # คอลัมน์ class ไว้ "ระบายสี" กราฟ / เทียบโมเดล (ไม่มีใส่ None)
POS_LABEL = None
ID_COL    = None           # ชื่อ/รหัสแถว (ใช้เขียน label บนจุด ถ้ามี)
DROP_COLS = []             # คอลัมน์ที่ไม่ใช้ทำ PCA
FEATURES  = None           # list feature ที่จะใช้ · None = ตัวเลขทุกคอลัมน์ (ยกเว้น TARGET/ID/DROP)
STANDARDIZE = True         # True = z-score ก่อน PCA (ปกติต้อง True)
VAR_TARGET  = 0.80         # เกณฑ์ cumulative variance ที่โจทย์ถาม (0.80 / 0.90 / 0.95)
N_LOADINGS  = 3            # แสดง loadings ของกี่ PC
NEW_POINT = None           # dict ข้อมูลใหม่ที่จะแปลงเป็น PC เช่น {"alcohol": 13.0, ...} · None = ข้าม
SEED, N_FOLDS = 42, 5
MISSING_MARKERS, SHEET, CSV_SEP = ["?", "", " ", "NA"], 0, ","
'''

S = [
md(r"""## §1 โหลด + เลือก feature ตัวเลข"""),
code(r'''df = load_data(DATA_PATH)
skip = [c for c in [TARGET, ID_COL] + list(DROP_COLS) if c]
feats = FEATURES or [c for c in num_cols(df) if c not in skip]
data = df.dropna(subset=feats).reset_index(drop=True)
print(f"ใช้ {len(feats)} feature: {feats}")
print(f"แถว {len(df)} → ตัดแถวที่มีค่าว่าง {len(df) - len(data)} → {len(data)}")
display(data[feats].describe().T[["mean", "std", "min", "max"]])
print("✍️ ช่วงของตัวแปรต่างกันมาก (std ตั้งแต่ %.3f ถึง %.3f) → ต้อง standardize ก่อน PCA" % (data[feats].std().min(), data[feats].std().max()))'''),

md(r"""
## §2 Standardize → PCA (ทุก component) → ตาราง explained variance
- **eigenvalue** = ความแปรปรวนของ PC (ข้อมูล z-score: ผลรวม eigenvalue = จำนวน feature)
- **explained variance ratio** = eigenvalue / ผลรวม · **cumulative** = สะสม
"""),
code(r'''scaler = StandardScaler() if STANDARDIZE else None
Z = scaler.fit_transform(data[feats]) if STANDARDIZE else data[feats].values
pca_full = PCA(random_state=SEED).fit(Z)
ev = pd.DataFrame({"PC": [f"PC{i+1}" for i in range(len(feats))],
                   "eigenvalue": pca_full.explained_variance_,
                   "explained_%": pca_full.explained_variance_ratio_ * 100,
                   "cumulative_%": pca_full.explained_variance_ratio_.cumsum() * 100})
display(ev.round(3))
n_target = int(np.argmax(ev["cumulative_%"].values >= VAR_TARGET * 100) + 1)
n_kaiser = int((ev["eigenvalue"] > 1).sum())
print(f"✍️ ต้องใช้ {n_target} component จึงอธิบายความแปรปรวนได้ ≥ {VAR_TARGET:.0%} (ได้ {ev['cumulative_%'][n_target-1]:.2f}%)")
print(f"✍️ เกณฑ์ Kaiser (eigenvalue > 1) เก็บ {n_kaiser} component")
print(f"✍️ PC1 อธิบายได้ {ev['explained_%'][0]:.2f}% · PC1+PC2 = {ev['cumulative_%'][1]:.2f}% (ภาพ 2D แสดงข้อมูลได้ประมาณนี้)")'''),
code(r'''# Scree plot + cumulative
fig, ax = plt.subplots(1, 2, figsize=(12, 3.8))
ax[0].plot(range(1, len(ev) + 1), ev["eigenvalue"], "o-"); ax[0].axhline(1, color="r", ls="--", label="eigenvalue = 1 (Kaiser)")
ax[0].set(title="Scree plot", xlabel="component", ylabel="eigenvalue"); ax[0].legend()
ax[1].bar(range(1, len(ev) + 1), ev["explained_%"], alpha=.6, label="each PC")
ax[1].plot(range(1, len(ev) + 1), ev["cumulative_%"], "o-", color="C1", label="cumulative")
ax[1].axhline(VAR_TARGET * 100, color="r", ls="--", label=f"{VAR_TARGET:.0%}"); ax[1].axvline(n_target, color="gray", ls=":")
ax[1].set(title="Explained variance (%)", xlabel="component", ylabel="%"); ax[1].legend()
plt.tight_layout(); plt.show()'''),
md(r"""**✍️ คำตอบ §2:** PC1 อธิบาย …% PC2 …% รวม …% · ต้องใช้ … component ถึง …% · Kaiser เลือก … · scree plot หักศอกที่ PC … → เลือก … component"""),

md(r"""
## §3 Loadings — ตัวแปรไหนขับเคลื่อน PC แต่ละตัว
loading = น้ำหนักของตัวแปรใน PC (`components_`) · |ค่า| ใหญ่ = มีอิทธิพลมาก · เครื่องหมายบอกทิศ (ตัวแปรเครื่องหมายเดียวกันไปทางเดียวกัน)
⚠️ เครื่องหมายของทั้ง PC อาจกลับด้านได้ระหว่างโปรแกรม (ไม่ผิด)
"""),
code(r'''k = min(N_LOADINGS, len(feats))
loadings = pd.DataFrame(pca_full.components_[:k].T, index=feats, columns=[f"PC{i+1}" for i in range(k)])
display(loadings.round(4).style.background_gradient(cmap="coolwarm", vmin=-1, vmax=1))
for pc in loadings.columns:
    top = loadings[pc].abs().sort_values(ascending=False).head(4).index
    print(f"✍️ {pc}: loading สูงสุด " + ", ".join(f"{t} ({loadings.loc[t, pc]:+.3f})" for t in top))
plt.figure(figsize=(1.2 * k + 3, 0.35 * len(feats) + 1.5))
sns.heatmap(loadings, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1); plt.title("Loadings"); plt.show()'''),
md(r"""**✍️ คำตอบ §3:** PC1 ขับเคลื่อนโดย … (บวก) และ … (ลบ) → แทน "…" · PC2 ขับเคลื่อนโดย … → แทน "…" """),

md(r"""## §4 PCA 2D visualization (scatter PC1 × PC2 ระบายสีตาม class) + biplot"""),
code(r'''pca2 = PCA(n_components=2, random_state=SEED).fit(Z)
P = pca2.transform(Z)
scores = pd.DataFrame(P, columns=["PC1", "PC2"])
if TARGET and TARGET in data:
    scores[TARGET] = data[TARGET].astype(str).values
display(scores.head())

fig, ax = plt.subplots(1, 2, figsize=(13, 5))
sns.scatterplot(data=scores, x="PC1", y="PC2", hue=TARGET if TARGET in scores else None, palette="tab10", s=40, ax=ax[0])
ax[0].set(title=f"PCA 2D ({pca2.explained_variance_ratio_.sum():.1%} of variance)",
          xlabel=f"PC1 ({pca2.explained_variance_ratio_[0]:.1%})", ylabel=f"PC2 ({pca2.explained_variance_ratio_[1]:.1%})")
if ID_COL and ID_COL in data and len(data) <= 60:
    for i, name in enumerate(data[ID_COL]):
        ax[0].annotate(str(name), P[i], fontsize=7, alpha=.8)
# biplot: ลูกศร = loading ของแต่ละตัวแปร
ax[1].scatter(P[:, 0], P[:, 1], s=8, alpha=.25, color="gray")
sc = np.abs(P).max() / np.abs(pca2.components_).max() * 0.8
for j, f in enumerate(feats):
    ax[1].arrow(0, 0, pca2.components_[0, j] * sc, pca2.components_[1, j] * sc, color="C3", head_width=0.05 * sc / 3)
    ax[1].text(pca2.components_[0, j] * sc * 1.1, pca2.components_[1, j] * sc * 1.1, f, fontsize=8)
ax[1].set(title="Biplot (arrows = loadings)", xlabel="PC1", ylabel="PC2")
plt.tight_layout(); plt.show()
if TARGET and TARGET in scores:
    display(scores.groupby(TARGET)[["PC1", "PC2"]].mean().round(3))'''),
md(r"""**✍️ คำตอบ §4:** ภาพ 2D อธิบายได้ …% · คลาส … แยกออกชัดทาง PC1 (ค่าบวก/ลบ) · คลาส … กับ … ซ้อนกันบางส่วน · ลูกศร … ชี้ไปทางคลาส … แปลว่าคลาสนั้นมี … สูง"""),

md(r"""
## §5 PCA ก่อนสร้างโมเดล — เทียบก่อน/หลัง (ไม่ leak: scaler + PCA อยู่ใน Pipeline)
"""),
code(r'''if TARGET and TARGET in data:
    X, y = data[feats], data[TARGET]
    if y.nunique() == 2:
        _, y = make_xy(data[feats + [TARGET]])
    MODEL = KNeighborsClassifier(n_neighbors=5)          # ✏️ เปลี่ยนโมเดลได้ (เช่น LogisticRegression(max_iter=1000))
    rows = [evaluate("Majority baseline", DummyClassifier(), X, y),
            evaluate("Model ทุก feature (z-score)", Pipeline([("sc", StandardScaler()), ("m", MODEL)]), X, y, settings=f"{len(feats)} features")]
    for n in sorted({2, n_target, n_kaiser}):
        rows.append(evaluate(f"Model + PCA({n})", Pipeline([("sc", StandardScaler()), ("pca", PCA(n_components=n)), ("m", MODEL)]), X, y,
                             settings=f"{n} PCs"))
    rows.append(evaluate(f"Model + PCA({VAR_TARGET:.0%} var)", Pipeline([("sc", StandardScaler()), ("pca", PCA(n_components=VAR_TARGET)), ("m", MODEL)]), X, y,
                         settings=f"keep {VAR_TARGET:.0%}"))
    t = results_table(rows)
    say_compare(t, "f1", "Majority baseline")
else:
    print("ไม่มี TARGET → ข้าม §5")'''),
md(r"""**✍️ คำตอบ §5:** ใช้ PCA … component ได้ F1 … เทียบกับใช้ทุก feature … → ลดมิติจาก … เหลือ … โดยเสียความแม่นยำเล็กน้อย/ไม่เสีย (หรือดีขึ้นเพราะตัด noise)"""),

md(r"""## §6 แปลงข้อมูลใหม่เป็นคะแนน PC (ใช้ scaler + PCA ตัวเดิม)"""),
code(r'''if NEW_POINT is not None:
    new = new_data(NEW_POINT)[feats]
    z_new = scaler.transform(new) if STANDARDIZE else new.values
    print("z-score:", np.round(z_new, 3)); print("PC1, PC2 =", np.round(pca2.transform(z_new), 4))
else:
    # ตัวอย่าง: แถวแรกของข้อมูล — PC = z · loading (ผลคูณจุด)
    z0 = Z[0]; print("แถวแรก z-score:", np.round(z0, 3))
    print("PC1 = Σ z·loading =", round(float(z0 @ pca2.components_[0]), 4), "| PC2 =", round(float(z0 @ pca2.components_[1]), 4))
    print("(ตรงกับ scores.iloc[0]:", np.round(P[0], 4), ")")'''),
md(r"""## §7 Save คะแนน PC (ถ้าต้องส่ง)"""),
code(r'''scores.to_csv("t03_pca_scores.csv", index=False); print("saved t03_pca_scores.csv")'''),
]

if __name__ == "__main__":
    build("../T03_pca.ipynb", TITLE, CONFIG, S)
