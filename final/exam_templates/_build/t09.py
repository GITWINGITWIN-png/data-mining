from nbtools import md, code, build

TITLE = r"""
# T09 · Classification Workflow ครบวงจร (Baseline → หลายโมเดล → Optimize → เทียบก่อน/หลัง → เลือกโมเดล → ทำนาย)

**ใช้เมื่อโจทย์ถาม (แบบรวม):** *"สร้าง workflow ตั้งแต่ preprocessing → training → evaluation"* · *"สร้าง baseline แล้วเทียบ"* ·
*"เปรียบเทียบ KNN / Logistic / Decision Tree / Random Forest"* · *"hold-out หรือ cross-validation"* · *"optimize parameters"* ·
*"เปรียบเทียบก่อนและหลัง optimization"* · *"ควรเลือกโมเดลไหน เพราะอะไร"*

นี่คือ **template หลัก** ของโจทย์ classification — ถ้าโจทย์ถามลึกเฉพาะโมเดล ให้เปิด T05 (KNN) / T07 (Logistic) / T08 (Tree/RF) / T04 (imbalanced) ประกอบ

| ขั้น | ทำอะไร |
|---|---|
| 1 | แก้ **⚙️ CONFIG** — `TARGET`, `POS_LABEL`, `ID_COL`, `DROP_COLS`, `EVAL_MODE`, `PRIMARY_METRIC` |
| 2 | Run All → ตาราง §4 (default) · §5 (optimized) · §6 (ก่อน vs หลัง) · §7 (โมเดลสุดท้าย) |
| 3 | ไม่ต้องการโมเดลไหน → ลบออกจาก `MODELS` / `GRIDS` ใน §3 · ต้องการค่าพารามิเตอร์ตามโจทย์ → แก้ใน §3 |
"""

CONFIG = r'''# ════════ ⚙️ CONFIG — แก้ cell นี้ให้ตรงโจทย์ ════════
DATA_PATH = "../mock_lab/mock3_cluster_assoc/data/bank-data.csv"
TARGET    = "pep"
POS_LABEL = "YES"            # คลาสที่สนใจ (= 1)
ID_COL    = "id"
DROP_COLS = []               # คอลัมน์ที่ตัด (leak / ไม่เกี่ยว)
EVAL_MODE = "cv"             # "cv" = k-fold ทั้งชุด · "holdout" = tune ด้วย CV บน train แล้ววัดบน test
PRIMARY_METRIC = "f1"        # "f1" | "accuracy" | "recall" | "precision" (เลือกตามโจทย์/ความไม่สมดุล)
SCALE     = "standard"       # สำหรับ KNN / Logistic (Tree/RF ไม่ scale อัตโนมัติ)
USE_SMOTE = False            # True = ใส่ SMOTE ใน pipeline (เฉพาะ training fold)
NEW_DATA  = None             # dict / list / path .csv ของข้อมูลใหม่ · None = ข้าม
TEST_SIZE, N_FOLDS, SEED = 0.2, 10, 42
MISSING_MARKERS, SHEET, CSV_SEP = ["?", "", " ", "NA"], 0, ","
'''

S = [
md(r"""## §1 โหลด + ตรวจข้อมูล"""),
code(r'''df = load_data(DATA_PATH)
check(df, TARGET)
X, y = make_xy(df)
print("ตัวเลข:", num_cols(X)); print("หมวดหมู่ (จะ one-hot):", cat_cols(X))'''),

md(r"""
## §2 แบ่งข้อมูล + กำหนดวิธีประเมิน
- **hold-out**: train (ใช้ CV เลือก/tune) → test (วัดครั้งเดียวตอนจบ) · เร็ว ใช้เมื่อข้อมูลเยอะ
- **k-fold CV**: ทุกแถวได้เป็น validation 1 ครั้ง → ค่าเสถียรกว่า · ใช้เมื่อข้อมูลน้อย
- ทั้งสองแบบ preprocessing อยู่ใน Pipeline → fit เฉพาะ train/training fold (ไม่ leak)
"""),
code(r'''cv = get_cv()
if EVAL_MODE == "holdout":
    X_dev, X_test, y_dev, y_test = train_test_split(X, y, test_size=TEST_SIZE, stratify=y, random_state=SEED)
    print(f"hold-out: train {X_dev.shape} / test {X_test.shape} · tune ด้วย {N_FOLDS}-fold CV บน train")
else:
    X_dev, y_dev = X, y
    print(f"{N_FOLDS}-fold stratified CV บนข้อมูลทั้งหมด {X.shape}")

def score(name, model, settings=""):
    """ประเมิน 1 โมเดลตาม EVAL_MODE → 1 แถว"""
    if EVAL_MODE == "holdout":
        return evaluate_holdout(name, model, X_dev, y_dev, X_test, y_test, settings)
    return evaluate(name, model, X_dev, y_dev, cv, settings, train=True)

def pipe(model, scale="config"):
    if USE_SMOTE:
        from imblearn.pipeline import Pipeline as ImbPipeline
        from imblearn.over_sampling import SMOTE
        return ImbPipeline([("prep", build_prep(X, scale=scale)), ("smote", SMOTE(random_state=SEED)), ("model", model)])
    return make_pipe(model, X, scale=scale)'''),

md(r"""
## §3 Baseline + โมเดล default + grid สำหรับ optimize (✏️ แก้ค่าตามโจทย์ได้ที่นี่)
**baseline** = จุดอ้างอิงขั้นต่ำ: majority (ทายคลาสที่พบบ่อยสุดเสมอ) · stratified (สุ่มตามสัดส่วน) → โมเดลจริงต้องชนะ baseline
"""),
code(r'''BASELINES = {"Majority baseline": DummyClassifier(strategy="most_frequent"),
             "Stratified random baseline": DummyClassifier(strategy="stratified", random_state=SEED)}

MODELS = {   # ✏️ ชื่อ: (pipeline, ข้อความ settings)
    "KNN":                 (pipe(KNeighborsClassifier(n_neighbors=5)), "k=5"),
    "Logistic Regression": (pipe(LogisticRegression(max_iter=5000)), "C=1, t=0.5"),
    "Decision Tree":       (pipe(DecisionTreeClassifier(random_state=SEED), scale=None), "gini, no depth limit"),
    "Random Forest":       (pipe(RandomForestClassifier(n_estimators=100, random_state=SEED), scale=None), "100 trees"),
}
GRIDS = {    # ✏️ ช่วงค่าที่จะลอง (ชื่อ model__<parameter>)
    "KNN": {"model__n_neighbors": list(range(1, 32, 2)), "model__weights": ["uniform", "distance"]},
    "Logistic Regression": {"model__C": [0.01, 0.1, 1, 10, 100], "model__class_weight": [None, "balanced"]},
    "Decision Tree": {"model__max_depth": [2, 3, 4, 5, 6, 8, 10, None], "model__min_samples_leaf": [1, 2, 5, 10],
                      "model__criterion": ["gini", "entropy"]},
    "Random Forest": {"model__n_estimators": [100, 300], "model__max_depth": [None, 5, 10],
                      "model__min_samples_leaf": [1, 3, 5]},
}
print("models:", list(MODELS), "| primary metric:", PRIMARY_METRIC)'''),

md(r"""## §4 Baseline vs โมเดล default ⭐"""),
code(r'''rows = [score(n, m) for n, m in BASELINES.items()]
rows += [score(n, m, s) for n, (m, s) in MODELS.items()]
default_tab = results_table(rows)
say_compare(default_tab, PRIMARY_METRIC, "Majority baseline")
if "train_accuracy" in default_tab:
    gap = (default_tab["train_accuracy"] - default_tab["accuracy"]).round(4)
    for n, g in zip(default_tab["model"], gap):
        if g > 0.1:
            print(f"⚠️ {n}: train accuracy สูงกว่า validation {g:.3f} → overfit")
default_tab.set_index("model")[["accuracy", "precision", "recall", "f1"]].plot(kind="barh", figsize=(8, 4.5), title=f"Default models ({EVAL_MODE})")
plt.gca().invert_yaxis(); plt.legend(loc="lower right"); plt.tight_layout(); plt.show()'''),
md(r"""**✍️ คำตอบ §4:** baseline (majority) ได้ accuracy … F1 … · โมเดล default ที่ดีที่สุดคือ … (… = …) ชนะ baseline … → โมเดลเรียนรู้รูปแบบได้จริง · … overfit (train … vs validation …)"""),

md(r"""## §5 Optimize parameters (GridSearchCV บน train/CV — เลือกด้วย PRIMARY_METRIC)"""),
code(r'''grids, best_rows = {}, []
for n, grid_params in GRIDS.items():
    if n not in MODELS:
        continue
    g = GridSearchCV(MODELS[n][0], grid_params, cv=cv, scoring=cls_scoring(y), refit=PRIMARY_METRIC, n_jobs=-1).fit(X_dev, y_dev)
    grids[n] = g
    print(f"── {n}: best {g.best_params_} · CV {PRIMARY_METRIC} = {g.best_score_:.4f}")
    display(top_k(g, 3))
    best_rows.append(score(f"{n} (optimized)", g.best_estimator_, str({k.replace('model__', ''): v for k, v in g.best_params_.items()})))
opt_tab = results_table(best_rows)'''),

md(r"""## §6 เปรียบเทียบก่อน vs หลัง optimize ⭐"""),
code(r'''ba = []
for n in grids:
    before = default_tab.set_index("model").loc[n]; after = opt_tab.set_index("model").loc[f"{n} (optimized)"]
    ba.append({"model": n, "settings ก่อน": MODELS[n][1], "settings หลัง": after["settings"],
               f"{PRIMARY_METRIC} ก่อน": before[PRIMARY_METRIC], f"{PRIMARY_METRIC} หลัง": after[PRIMARY_METRIC],
               "เปลี่ยน": after[PRIMARY_METRIC] - before[PRIMARY_METRIC],
               "accuracy ก่อน": before["accuracy"], "accuracy หลัง": after["accuracy"]})
ba = results_table(ba)
for _, r in ba.iterrows():
    print(f"✍️ {r['model']}: {PRIMARY_METRIC} {r[f'{PRIMARY_METRIC} ก่อน']:.4f} → {r[f'{PRIMARY_METRIC} หลัง']:.4f} ({r['เปลี่ยน']:+.4f}) ด้วย {r['settings หลัง']}")
all_tab = pd.concat([default_tab, opt_tab], ignore_index=True)
all_tab.set_index("model")[PRIMARY_METRIC].sort_values().plot(kind="barh", figsize=(7, 4.5), title=f"{PRIMARY_METRIC}: all models"); plt.tight_layout(); plt.show()'''),

md(r"""## §7 เลือกโมเดลสุดท้าย → confusion matrix"""),
code(r'''cand = all_tab[~all_tab["model"].str.contains("baseline")]
final_name = cand.loc[cand[PRIMARY_METRIC].idxmax(), "model"]
lookup = {n: m for n, (m, _) in MODELS.items()} | {f"{n} (optimized)": g.best_estimator_ for n, g in grids.items()}
final_model = lookup[final_name]
print(f"✍️ โมเดลสุดท้าย = {final_name} ({PRIMARY_METRIC} = {cand[PRIMARY_METRIC].max():.4f})")
if EVAL_MODE == "holdout":
    final_model.fit(X_dev, y_dev); show_cm(y_test, final_model.predict(X_test), f"{final_name} — test")
else:
    show_cm(y, cross_val_predict(final_model, X, y, cv=cv), f"{final_name} — CV predictions")
final_model.fit(X, y)       # fit ด้วยข้อมูลทั้งหมดก่อนใช้งานจริง'''),
md(r"""
**✍️ คำตอบ §7 (โครงคำตอบ 4 ขั้น):**
1. **Process:** อ่านข้อมูล → ตัด `…` → Pipeline (median/mode imputer + z-score + one-hot) → {EVAL_MODE} → baseline + 4 โมเดล → GridSearch
2. **Settings:** seed …, … folds, metric หลัก … เพราะ …
3. **Results:** ตาราง §4–§6 · โมเดลที่ดีที่สุด … ได้ … = …
4. **Interpretation:** ดีกว่า baseline … · optimize แล้วดีขึ้น … · confusion matrix: FN … FP … → …
"""),

md(r"""## §8 ทำนายข้อมูลใหม่"""),
code(r'''if NEW_DATA is not None:
    nd = align_new(new_data(NEW_DATA), X)
    out = nd.copy(); out["pred (1 = POS_LABEL)"] = final_model.predict(nd)
    if hasattr(final_model, "predict_proba"):
        out["P(1)"] = final_model.predict_proba(nd)[:, -1]
    display(out)
else:
    print("NEW_DATA = None → ข้าม (ตัวอย่างทำนาย 3 แถวแรก):")
    display(X.head(3).assign(pred=final_model.predict(X.head(3)), actual=y.head(3).values))'''),
]

if __name__ == "__main__":
    build("../T09_classification_workflow.ipynb", TITLE, CONFIG, S)
