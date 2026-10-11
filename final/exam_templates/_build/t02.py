from nbtools import md, code, build

TITLE = r"""
# T02 · Data Preprocessing (Missing · Outlier · Encoding · Scaling · Discretization · Sampling · Split ไม่ leak · Feature selection)

**ใช้เมื่อโจทย์ถาม:** จัดการค่าว่าง · ค่าแฝง (`?`, 0 ที่เป็นไปไม่ได้) · outlier · one-hot / ordinal / label encoding ·
z-score / min-max · แบ่งช่วง (equal width / equal frequency / กำหนดเอง) · สุ่มตัวอย่าง / stratified ·
แบ่ง train/test **โดยไม่ leak** · เลือก feature · "เปรียบเทียบก่อน/หลัง preprocessing"

> SMOTE / undersampling แบบเต็ม → **T04** · PCA → **T03**

| ขั้น | ทำอะไร |
|---|---|
| 1 | แก้ **⚙️ CONFIG** · Run All |
| 2 | ไป § ที่โจทย์ถาม → แก้บรรทัด `# ✏️` → รันใหม่ |
| 3 | §1–§7 = **สำรวจ/สาธิต** (ทำกับทั้งตาราง เพื่อดูผล) · §8 = วิธีที่ **ถูกต้องตอนสร้างโมเดล** (fit บน train เท่านั้น) |
"""

CONFIG = r'''# ════════ ⚙️ CONFIG — แก้ cell นี้ให้ตรงโจทย์ ════════
DATA_PATH = "../practice/data/p2_penguins.csv"
TARGET    = "species"        # label (ไม่มีใส่ None)
POS_LABEL = None             # ถ้า target มี 2 คลาส: คลาสที่สนใจ (เช่น "Yes", 1, ">50K") · None = เลือกตัวท้ายตามตัวอักษร
ID_COL    = None             # คอลัมน์ id
DROP_COLS = []               # คอลัมน์ที่ตัดทิ้งแน่นอน (leak / ไม่เกี่ยว)
MISSING_MARKERS = ["?", "", " ", "NA", "N/A", "null", "-"]
ZERO_AS_MISSING = []         # คอลัมน์ที่ค่า 0 เป็นไปไม่ได้ = ค่าว่าง (เช่น pima: ["glucose", "bmi", "blood_pressure"])
SCALE     = "standard"       # "standard" (z-score) | "minmax" (0–1) | None
TEST_SIZE = 0.2
SEED      = 42
N_FOLDS   = 5
SHEET, CSV_SEP = 0, ","
'''

S = [
md(r"""## §1 โหลด + สำรวจค่าว่าง (รันเสมอ)"""),
code(r'''df = load_data(DATA_PATH)
for c in ZERO_AS_MISSING:
    n0 = int((df[c] == 0).sum()); df[c] = df[c].replace(0, np.nan)
    print(f"{c}: 0 → NaN จำนวน {n0} ค่า (ค่า 0 เป็นไปไม่ได้ทางความหมาย)")
check(df, TARGET)
miss = df.isna().sum()
miss = miss[miss > 0].sort_values(ascending=False)
if len(miss):
    (miss / len(df) * 100).plot(kind="bar", figsize=(6, 3), title="% missing per column"); plt.ylabel("%"); plt.show()
print(f"แถวที่มีค่าว่างอย่างน้อย 1 ช่อง: {int(df.isna().any(axis=1).sum())} / {len(df)}")'''),
md(r"""**✍️ คำตอบ §1:** มีค่าว่างใน … (… ค่า, …%) · ค่าแฝง `?`/0 ที่เป็นไปไม่ได้ใน … ถูกแปลงเป็น missing ก่อน"""),

md(r"""
## §2 Missing-value handling — เลือกวิธี
| วิธี | ใช้เมื่อ | ข้อเสีย |
|---|---|---|
| ลบแถว (`dropna`) | ค่าว่างน้อยมาก (< ~5%) | เสียข้อมูล · bias ถ้าว่างไม่สุ่ม |
| ลบคอลัมน์ | คอลัมน์ว่าง > ~40–50% | เสียตัวแปร |
| mean | ตัวเลข สมมาตร ไม่มี outlier | โดน outlier ดึง |
| **median** | ตัวเลข เบ้ / มี outlier | — |
| mode (ค่าที่พบบ่อย) | หมวดหมู่ | คลาสนั้นพองขึ้น |
| ค่าคงที่ / "Unknown" | ความว่างมีความหมาย | — |
| ตามกลุ่ม (group median) | ค่าต่างกันตามกลุ่มชัดเจน | ต้องรู้กลุ่ม |
"""),
code(r'''MISS_METHOD = "median"     # ✏️ "drop_rows" | "drop_cols" | "mean" | "median" | "mode" | "constant" | "group"
DROP_COL_THRESHOLD = 0.5   # ✏️ ใช้กับ drop_cols: ตัดคอลัมน์ที่ว่างเกินสัดส่วนนี้
CONSTANT = "Unknown"       # ✏️ ใช้กับ constant (หมวดหมู่) — ตัวเลขจะเติม 0
GROUP_COL = TARGET         # ✏️ ใช้กับ group: เติม median/mode ตามกลุ่มนี้

clean = df.copy()
before = int(clean.isna().sum().sum())
if MISS_METHOD == "drop_rows":
    clean = clean.dropna()
elif MISS_METHOD == "drop_cols":
    clean = clean.loc[:, clean.isna().mean() <= DROP_COL_THRESHOLD]
else:
    for c in clean.columns[clean.isna().any()]:
        is_num = c in num_cols(clean)
        if MISS_METHOD == "group" and GROUP_COL and c != GROUP_COL:
            fill = clean.groupby(GROUP_COL)[c].transform(lambda s: s.median() if is_num else (s.mode().iloc[0] if s.notna().any() else np.nan))
            clean[c] = clean[c].fillna(fill)
        elif MISS_METHOD == "constant":
            clean[c] = clean[c].fillna(0 if is_num else CONSTANT)
        elif is_num and MISS_METHOD in ("mean", "median"):
            v = clean[c].mean() if MISS_METHOD == "mean" else clean[c].median()
            print(f"{c}: เติม {MISS_METHOD} = {v:.4f}"); clean[c] = clean[c].fillna(v)
        else:                                  # หมวดหมู่ หรือ mode
            v = clean[c].mode().iloc[0]; print(f"{c}: เติม mode = {v!r}"); clean[c] = clean[c].fillna(v)
print(f"วิธี {MISS_METHOD}: missing ทั้งหมด {before} → {int(clean.isna().sum().sum())} | shape {df.shape} → {clean.shape}")
display(clean.describe().T)'''),
md(r"""**✍️ คำตอบ §2:** เลือก … เพราะ … (เช่น `…` เบ้ขวา/มี outlier → median ทนกว่า mean · หมวดหมู่ใช้ mode) · ค่าว่างลดจาก … เป็น 0 · ⚠️ ตอนสร้างโมเดลต้องคำนวณค่าที่เติมจาก **train เท่านั้น** (§8)"""),

md(r"""## §3 Outliers (IQR rule: < Q1 − 1.5·IQR หรือ > Q3 + 1.5·IQR)"""),
code(r'''OUT_METHOD = None     # ✏️ None = แค่นับ · "clip" = ตัดให้อยู่ในขอบ (winsorize) · "remove" = ลบแถว

cols = [c for c in num_cols(clean) if c not in (TARGET, ID_COL)]
rows = []
for c in cols:
    q1, q3 = clean[c].quantile([.25, .75]); iqr = q3 - q1; lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    n = int(((clean[c] < lo) | (clean[c] > hi)).sum())
    rows.append({"column": c, "Q1": q1, "Q3": q3, "IQR": iqr, "lower": lo, "upper": hi, "n_outliers": n})
    if OUT_METHOD == "clip":
        clean[c] = clean[c].clip(lo, hi)
    elif OUT_METHOD == "remove":
        clean = clean[(clean[c] >= lo) & (clean[c] <= hi)]
display(pd.DataFrame(rows))
zs = (clean[cols] - clean[cols].mean()) / clean[cols].std()
fig, ax = plt.subplots(figsize=(min(14, 1.6 * len(cols) + 2), 3.5))
sns.boxplot(data=zs, ax=ax); ax.set_title("Boxplot (z-scored so all fit one axis)"); plt.xticks(rotation=30); plt.show()'''),

md(r"""
## §4 Encoding categorical attributes
| วิธี | ใช้กับ | ตัวอย่าง |
|---|---|---|
| **One-hot (dummy)** | nominal ไม่มีลำดับ | island → island_Biscoe, island_Dream, … |
| **Ordinal / mapping** | มีลำดับ | low < mid < high → 0,1,2 |
| **Binary map** | 2 ค่า | Yes/No → 1/0 |
| **Label encoding** | **target** เท่านั้น | species → 0,1,2 |
"""),
code(r'''ORDINAL_MAP = {}                       # ✏️ เช่น {"education": ["low", "mid", "high"]} (เรียงจากน้อยไปมาก)
BINARY_MAP  = {}                       # ✏️ เช่น {"smoker": {"yes": 1, "no": 0}}
DROP_FIRST  = False                    # ✏️ True = ตัด dummy ตัวแรก (กัน multicollinearity ใน linear/logistic regression)

enc = clean.copy()
for c, order in ORDINAL_MAP.items():
    enc[c] = enc[c].map({v: i for i, v in enumerate(order)}); print(f"ordinal {c}: {order} → 0..{len(order)-1}")
for c, m in BINARY_MAP.items():
    enc[c] = enc[c].map(m); print(f"binary {c}: {m}")
onehot_cols = [c for c in cat_cols(enc) if c not in (TARGET, ID_COL)]
enc = pd.get_dummies(enc, columns=onehot_cols, drop_first=DROP_FIRST, dtype=int)
print("one-hot:", onehot_cols, f"→ คอลัมน์ {clean.shape[1]} → {enc.shape[1]}")
if TARGET and TARGET in enc and not pd.api.types.is_numeric_dtype(enc[TARGET]):
    le = LabelEncoder().fit(enc[TARGET])
    print("label encoding ของ target:", {k: int(v) for k, v in zip(le.classes_, le.transform(le.classes_))})
display(enc.head())'''),
md(r"""**✍️ คำตอบ §4:** `…` เป็น nominal (ไม่มีลำดับ) → one-hot เพื่อไม่ให้โมเดลคิดว่า A < B · `…` มีลำดับ → ordinal · ได้ … คอลัมน์"""),

md(r"""
## §5 Standardization vs Normalization
- **z-score (standardization)** $z = (x-\bar x)/s$ → mean 0, std 1 · ทนกับ outlier มากกว่า · ใช้กับ KNN, K-Means, PCA, logistic
- **min-max (normalization)** $x' = (x-\min)/(\max-\min)$ → อยู่ใน [0, 1] · ถูก outlier บีบ
- โมเดลที่ใช้ **ระยะทาง** (KNN, K-Means) และ PCA **ต้อง** scale · Tree/RF **ไม่ต้อง**
- sklearn หาร $n$ · RapidMiner หาร $n-1$ (ตัวเลขต่างเล็กน้อย — ไม่ผิด)
"""),
code(r'''cols = [c for c in num_cols(clean) if c not in (TARGET, ID_COL)]
Z = pd.DataFrame(StandardScaler().fit_transform(clean[cols]), columns=cols, index=clean.index)
M = pd.DataFrame(MinMaxScaler().fit_transform(clean[cols]), columns=cols, index=clean.index)
Z_rm = (clean[cols] - clean[cols].mean()) / clean[cols].std(ddof=1)        # แบบ RapidMiner (n−1)
summary = pd.concat({"original": clean[cols].agg(["mean", "std", "min", "max"]),
                     "z-score": Z.agg(["mean", "std", "min", "max"]),
                     "min-max": M.agg(["mean", "std", "min", "max"])})
display(summary.round(4))
print("ตัวอย่าง 3 แถวแรก (z-score):"); display(Z.head(3))
fig, ax = plt.subplots(1, 3, figsize=(14, 3.5))
for a, (name, d) in zip(ax, [("original", clean[cols]), ("z-score", Z), ("min-max", M)]):
    sns.boxplot(data=d, ax=a); a.set_title(name); a.tick_params(axis="x", rotation=40)
plt.tight_layout(); plt.show()'''),
md(r"""**✍️ คำตอบ §5:** ก่อน scale `…` มีช่วง … ถึง … ใหญ่กว่า `…` มาก → ครอบงำระยะทาง · หลัง z-score ทุกตัว mean 0 std 1 · min-max อยู่ใน [0,1]"""),

md(r"""
## §6 Discretization (แบ่งช่วง / binning)
| วิธี | pandas | RapidMiner | ข้อดี/ข้อเสีย |
|---|---|---|---|
| equal **width** | `pd.cut(x, bins=k)` | Discretize by Binning | ช่วงกว้างเท่ากัน · บาง bin แทบว่างถ้าเบ้ |
| equal **frequency** | `pd.qcut(x, q=k)` | Discretize by Frequency | จำนวนต่อ bin เท่ากัน · ทนข้อมูลเบ้ |
| **กำหนดเอง** | `pd.cut(x, bins=[...], labels=[...])` | Discretize by User Specification | ตามความหมายทางธุรกิจ |
"""),
code(r'''DISC_COL = "body_mass_g"             # ✏️ คอลัมน์ที่จะแบ่ง
N_BINS   = 3                         # ✏️ จำนวนช่วง
LABELS   = ["Low", "Mid", "High"]    # ✏️ ชื่อช่วง (ต้องยาว = N_BINS) · None = แสดงช่วงตัวเลข
USER_BINS = [0, 3500, 4500, np.inf]  # ✏️ ขอบเขตกำหนดเอง (ขวาปิด: (a, b])

x = clean[DISC_COL]
d = pd.DataFrame({DISC_COL: x,
                  "equal_width": pd.cut(x, bins=N_BINS, labels=LABELS),
                  "equal_freq": pd.qcut(x, q=N_BINS, labels=LABELS, duplicates="drop"),
                  "user": pd.cut(x, bins=USER_BINS, labels=LABELS if LABELS and len(LABELS) == len(USER_BINS) - 1 else None)})
print("ขอบเขต equal width :", np.round(pd.cut(x, bins=N_BINS, retbins=True)[1], 3))
print("ขอบเขต equal freq  :", np.round(pd.qcut(x, q=N_BINS, retbins=True, duplicates="drop")[1], 3))
display(pd.concat({m: d[m].value_counts().sort_index() for m in ["equal_width", "equal_freq", "user"]}, axis=1))
if TARGET and TARGET in clean and clean[TARGET].nunique() <= 10:
    print(f"สัดส่วน {TARGET} ในแต่ละช่วง (equal freq):")
    display(pd.crosstab(d["equal_freq"], clean[TARGET], normalize="index").round(3))
# แบบ sklearn (ใช้ใน Pipeline ได้): KBinsDiscretizer(n_bins=3, encode="ordinal", strategy="uniform" | "quantile")'''),
md(r"""**✍️ คำตอบ §6:** equal width ได้จำนวนต่อช่วง … (ไม่เท่ากันเพราะข้อมูลเบ้) · equal frequency ได้ประมาณ … ต่อช่วง · เลือก … เพราะ …"""),

md(r"""
## §7 Sampling (สุ่มตัวอย่าง)
- **simple random** = สุ่มเฉย ๆ · **stratified** = รักษาสัดส่วนคลาสเหมือนเดิม (ใช้กับ label ไม่สมดุล)
- **balance** (undersample/oversample/SMOTE) → ทำ **เฉพาะ train** — ดู T04
"""),
code(r'''SAMPLE_FRAC = 0.3        # ✏️ สัดส่วนที่สุ่ม (หรือใช้ n=… แทน)

simple = clean.sample(frac=SAMPLE_FRAC, random_state=SEED)
strat = clean.groupby(TARGET, group_keys=False).sample(frac=SAMPLE_FRAC, random_state=SEED) if TARGET else simple
comp = pd.concat({"ทั้งหมด": clean[TARGET].value_counts(normalize=True),
                  "simple random": simple[TARGET].value_counts(normalize=True),
                  "stratified": strat[TARGET].value_counts(normalize=True)}, axis=1).round(4)
print(f"ขนาด: ทั้งหมด {len(clean)} | simple {len(simple)} | stratified {len(strat)}"); display(comp)
# balance แบบง่าย (downsample ทุกคลาสให้เท่าคลาสเล็กสุด) — ทำเฉพาะ train จริง ๆ:
n_min = clean[TARGET].value_counts().min()
balanced = clean.groupby(TARGET, group_keys=False).sample(n=n_min, random_state=SEED)
print("หลัง downsample ให้เท่ากัน:", balanced[TARGET].value_counts().to_dict())'''),

md(r"""
## §8 แบ่งข้อมูลโดย **ไม่เกิด data leakage** ⭐ (วิธีที่ถูกต้องตอนสร้างโมเดล)
**กฎ:** split ก่อน → `fit` ตัว imputer/scaler/encoder/SMOTE **บน train เท่านั้น** → `transform` test ด้วยค่าจาก train
ใช้ `Pipeline` = ทำให้อัตโนมัติ (ใน CV ก็ fit ใหม่ทุก fold)
❌ ผิด: `StandardScaler().fit_transform(X)` ทั้งตารางก่อน split · เติม mean ของทั้งตาราง · SMOTE ก่อน CV · เลือก feature ด้วยทั้งตาราง
"""),
code(r'''X, y = make_xy(df)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=SEED, stratify=y)
print(f"train {X_train.shape} | test {X_test.shape}")
print("สัดส่วน y: train", y_train.value_counts(normalize=True).round(3).to_dict(), "| test", y_test.value_counts(normalize=True).round(3).to_dict())

prep = build_prep(X_train, scale=SCALE)          # median/mode imputer + scaler + one-hot
Xtr = prep.fit_transform(X_train)                # ✅ fit บน train เท่านั้น
Xte = prep.transform(X_test)                     # ✅ test ใช้ค่าจาก train
names = prep.get_feature_names_out()
print("feature หลัง preprocess:", len(names)); print(list(names))
display(pd.DataFrame(Xtr, columns=names).describe().T[["mean", "std", "min", "max"]].round(3))
print("ค่าเฉลี่ยที่ scaler เรียนจาก train (5 ตัวแรก):", np.round(prep.named_transformers_["num"].named_steps["scale"].mean_[:5], 3)
      if SCALE == "standard" else "-")'''),
code(r'''# เปรียบเทียบ "ก่อน vs หลัง preprocessing" ด้วยโมเดลเดียวกัน (KNN ไวต่อ scale ที่สุด) — ใช้ CV + Pipeline (ไม่ leak)
MODEL_FOR_COMPARE = KNeighborsClassifier(n_neighbors=5)    # ✏️ เปลี่ยนโมเดลได้
rows = [evaluate("Majority baseline", DummyClassifier(strategy="most_frequent"), X, y),
        evaluate("KNN ไม่ scale", make_pipe(MODEL_FOR_COMPARE, X, scale=None), X, y, settings="impute + one-hot"),
        evaluate("KNN + z-score", make_pipe(MODEL_FOR_COMPARE, X, scale="standard"), X, y, settings="impute + one-hot + z"),
        evaluate("KNN + min-max", make_pipe(MODEL_FOR_COMPARE, X, scale="minmax"), X, y, settings="impute + one-hot + minmax")]
t = results_table(rows)
say_compare(t, "f1", "Majority baseline")'''),
md(r"""**✍️ คำตอบ §8:** แบ่ง train/test (…/…) แบบ stratified ก่อน แล้ว fit imputer/scaler บน train เท่านั้น จึงไม่ leak เพราะค่าทางสถิติของ test ไม่ถูกใช้ตอนเรียนรู้ · หลัง scale F1 เปลี่ยนจาก … เป็น … เพราะ KNN ใช้ระยะทาง"""),

md(r"""
## §9 Feature selection
1. ตัดก่อนเลย: id · ค่าคงที่ · ค่าว่างเยอะ · **leak** (ข้อมูลที่รู้หลังผลเกิด) · ซ้ำ (|r| > 0.9 กับตัวอื่น)
2. Filter: correlation / ANOVA F / mutual information กับ target
3. Embedded: feature importance ของ Random Forest
4. ตรวจผล: CV ทุก feature vs feature ที่เลือก (เลือกบน train/ใน pipeline เพื่อไม่ leak)
"""),
code(r'''from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
K_BEST = 3                                     # ✏️ จำนวน feature ที่จะเลือก

Xp = pd.DataFrame(Xtr, columns=names)
const = [c for c in Xp if Xp[c].nunique() <= 1]
print("feature ค่าคงที่:", const or "-")
cm_ = Xp.corr().abs(); upper = cm_.where(np.triu(np.ones(cm_.shape, dtype=bool), 1))
print("คู่ที่ |r| > 0.9:", [(a, b, round(float(upper.loc[a, b]), 3)) for a in upper.index for b in upper.columns if upper.loc[a, b] > 0.9] or "-")

ytr_num = y_train if pd.api.types.is_numeric_dtype(y_train) else LabelEncoder().fit_transform(y_train)
fs = pd.DataFrame({"ANOVA_F": f_classif(Xp, ytr_num)[0],
                   "mutual_info": mutual_info_classif(Xp, ytr_num, random_state=SEED),
                   "RF_importance": RandomForestClassifier(random_state=SEED).fit(Xp, y_train).feature_importances_},
                  index=names).sort_values("RF_importance", ascending=False)
display(fs.round(4))
fs["RF_importance"].plot(kind="barh", figsize=(6, 0.35 * len(fs) + 1), title="RF feature importance"); plt.gca().invert_yaxis(); plt.show()

# CV: ทุก feature vs SelectKBest ใน pipeline (เลือกใหม่ทุก fold → ไม่ leak)
sel_pipe = Pipeline([("prep", build_prep(X)), ("select", SelectKBest(f_classif, k=K_BEST)), ("model", KNeighborsClassifier())])
t = results_table([evaluate("KNN ทุก feature", make_pipe(KNeighborsClassifier(), X), X, y),
                   evaluate(f"KNN top-{K_BEST} (ANOVA)", sel_pipe, X, y)])
print("✍️ feature สำคัญสุด 3 อันดับ (RF):", list(fs.index[:3]))'''),
md(r"""**✍️ คำตอบ §9:** ตัด … เพราะ … · feature สำคัญสุดคือ … · ใช้ top-… แล้ว F1 … (ดีขึ้น/ใกล้เดิมแต่โมเดลง่ายขึ้น)"""),

md(r"""## §10 Save ข้อมูลที่ preprocess แล้ว (ถ้าโจทย์ให้ส่งไฟล์)"""),
code(r'''pd.DataFrame(Xtr, columns=names).assign(**{TARGET: y_train.values}).to_csv("t02_train_preprocessed.csv", index=False)
pd.DataFrame(Xte, columns=names).assign(**{TARGET: y_test.values}).to_csv("t02_test_preprocessed.csv", index=False)
print("saved t02_train_preprocessed.csv, t02_test_preprocessed.csv")'''),
]

if __name__ == "__main__":
    build("../T02_preprocessing.ipynb", TITLE, CONFIG, S)
