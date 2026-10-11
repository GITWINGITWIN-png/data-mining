"""สร้าง notebook ของ mock lab 3 ชุด: question.ipynb (โจทย์ + cell ว่าง) และ solution.ipynb (เฉลย)

ทำไมสร้างด้วยสคริปต์: โจทย์และเฉลยมาจากรายการ cell ชุดเดียวกัน → ข้อในโจทย์กับข้อในเฉลยตรงกันเสมอ
เฉลยถูกรันจริงด้วย kernel dm-exam หลังสร้าง (ตัวเลขในข้อความเฉลยมาจากผลที่รันได้)

รัน:  final/.venv/bin/python final/mock_lab/build_mocks.py
     (แล้ว execute เฉลย:  jupyter nbconvert --to notebook --execute --inplace <mock>/solution.ipynb)
"""
from pathlib import Path
import nbformat as nbf

HERE = Path(__file__).resolve().parent
KERNEL = {"name": "dm-exam", "display_name": "Python (dm-exam)", "language": "python"}


def build(folder, cells):
    """cells: list ของ (kind, text) — kind = 'md' (ทั้งสองไฟล์) · 'q' (โจทย์) · 'code' (เฉลย) · 'ans' (คำอธิบายเฉลย)"""
    q, s = nbf.v4.new_notebook(), nbf.v4.new_notebook()
    for kind, text in cells:
        text = text.strip("\n")
        if kind == "md":
            q.cells.append(nbf.v4.new_markdown_cell(text))
            s.cells.append(nbf.v4.new_markdown_cell(text))
        elif kind == "q":
            q.cells.append(nbf.v4.new_markdown_cell(text))
            q.cells.append(nbf.v4.new_code_cell("# เขียนโค้ดตรงนี้\n"))
            q.cells.append(nbf.v4.new_markdown_cell("**คำตอบ / การตีความ:** …"))
            s.cells.append(nbf.v4.new_markdown_cell(text))
        elif kind == "code":
            s.cells.append(nbf.v4.new_code_cell(text))
        elif kind == "ans":
            s.cells.append(nbf.v4.new_markdown_cell("> **✅ เฉลย / การตีความ**\n>\n" + "\n".join(
                "> " + line for line in text.splitlines())))
    for nb in (q, s):
        nb.metadata["kernelspec"] = KERNEL
    nbf.write(q, HERE / folder / "question.ipynb")
    nbf.write(s, HERE / folder / "solution.ipynb")
    print(f"  ✓ {folder}: question.ipynb + solution.ipynb")


SETUP = '''
import warnings; warnings.filterwarnings("ignore", category=UserWarning)   # ซ่อน warning precision=0 ของ baseline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import (train_test_split, StratifiedKFold, KFold, cross_validate,
                                     cross_val_predict, GridSearchCV)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import (precision_score, recall_score, f1_score, confusion_matrix,
                             mean_absolute_error, mean_squared_error, root_mean_squared_error, r2_score,
                             silhouette_score, davies_bouldin_score)
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from mlxtend.frequent_patterns import apriori, association_rules
SEED = 1992
'''

# ════════════════════════════════════════════════════════════════════════════════════════════
# MOCK 1 — Classification + Imbalanced (adult)
# ════════════════════════════════════════════════════════════════════════════════════════════
M1 = [
("md", """
# Mock Lab 1 — Premium Card Targeting (Classification + Imbalanced)
**เวลา:** 90 นาที (Python) + 60 นาที (สร้างซ้ำส่วน C ใน RapidMiner) · **seed = 1992** · **5-fold stratified CV** ทุกข้อที่ประเมินโมเดล

ธนาคารต้องการเสนอ **บัตรเครดิตพรีเมียม** ให้คนที่มีรายได้ **> 50K** และอยากหา "คนรายได้สูง" ให้ได้มากที่สุด
ข้อมูลถูกส่งมา 3 ไฟล์ใน `data/`:
- `people.csv` — ข้อมูลส่วนตัว (key = `person_id`)
- `work_2025H1.csv`, `work_2025H2.csv` — ข้อมูลการทำงาน + `income` (target) แบ่งเป็นสองช่วงเวลา คอลัมน์เหมือนกัน
- `new_person.csv` — ลูกค้าใหม่ 1 คน (ไม่มี income)

> ทุกข้อให้ตอบครบ: **process/โค้ด → ตั้งค่าที่ใช้ → ผล (ตาราง/กราฟ) → การตีความ**
"""),
("md", "## ตั้งต้น"),
("code", SETUP),
# ── Part A ──
("md", "## Part A · Data Handling (20 คะแนน)"),
("q", "**A1.** อ่านไฟล์ทั้ง 3 ไฟล์ ต่อ `work_2025H1` กับ `work_2025H2` เป็นตารางเดียว แล้ว **join** กับ `people` ด้วย `person_id` · รายงานจำนวนแถว/คอลัมน์ก่อนและหลัง join และอธิบายว่าเลือก join แบบไหนเพราะอะไร"),
("code", '''
people = pd.read_csv("data/people.csv")
h1 = pd.read_csv("data/work_2025H1.csv")
h2 = pd.read_csv("data/work_2025H2.csv")
print(set(h1.columns) ^ set(h2.columns))                 # set() = คอลัมน์ตรงกัน ต่อแถวได้
work = pd.concat([h1, h2], ignore_index=True)
print("people", people.shape, "| work", work.shape)
print("key ซ้ำ:", people["person_id"].duplicated().sum(), work["person_id"].duplicated().sum())
df = pd.merge(people, work, on="person_id", how="inner", validate="one_to_one")
print("joined", df.shape)
'''),
("ans", """
work = 3,500 + 2,499 = **5,999 แถว** (คอลัมน์ตรงกันทั้งสองไฟล์) · people = 5,999 แถว · key ไม่ซ้ำทั้งสองฝั่ง
หลัง join ได้ **5,999 × 16** (9 + 8 − key ที่ซ้ำ 1)
เลือก **inner join** เพราะต้องการเฉพาะคนที่มีทั้งข้อมูลส่วนตัวและข้อมูลการทำงาน + target · ผลเท่ากับ left join ในกรณีนี้ (ทุก id มีคู่) · ใส่ `validate="one_to_one"` เพื่อยืนยันว่าไม่มี key ซ้ำทำให้แถวงอก
"""),
("q", "**A2.** ข้อมูลใช้ `\"?\"` แทนค่าว่าง จงแปลงเป็น missing, นับค่าว่างต่อคอลัมน์ และหาสัดส่วนคนรายได้ > 50K · ข้อมูลสมดุลหรือไม่"),
("code", '''
df = df.replace("?", np.nan)
print(df.isna().sum().loc[lambda s: s > 0])
df["rich"] = (df["income"] == ">50K").astype(int)
print(df["rich"].value_counts(normalize=True).round(4))
'''),
("ans", """
ค่าว่าง: workclass **368**, occupation **369**, native-country **118** (≈ 6% / 6% / 2%)
รายได้ > 50K = **23.9%** → **ไม่สมดุล** (IR ≈ 76.1/23.9 = 3.2 : 1) → ห้ามดู accuracy อย่างเดียว · baseline ทาย "≤ 50K" ทุกคนก็ได้ accuracy ~76%
"""),
("q", "**A3.** ทำ **pivot table** สัดส่วนคนรายได้ > 50K โดยแถว = `education` คอลัมน์ = `gender` (เรียงตาม Male มากไปน้อย แสดง 5 แถวแรก) และตีความ 1–2 ประโยค"),
("code", '''
pv = pd.pivot_table(df, index="education", columns="gender", values="rich", aggfunc="mean").round(3)
pv.sort_values("Male", ascending=False).head(5)
'''),
("ans", """
Prof-school (Male 81.6%), Doctorate (76.2%), Masters (64.9%) มีสัดส่วนรายได้สูงมากที่สุด → **การศึกษาสูงสัมพันธ์กับรายได้สูง**
และในทุกระดับการศึกษา **ชายมีสัดส่วนรายได้สูงกว่าหญิง** (เช่น Prof-school 81.6% vs 28.6%) · ⚠️ เป็นความสัมพันธ์ ไม่ใช่เหตุ-ผล และบางกลุ่ม (หญิง Prof-school) มีจำนวนน้อย ค่าจึงแกว่งได้
"""),
("q", "**A4.** วาดกราฟ 2 รูปที่เหมาะสม: (1) การกระจายของ `age` แยกตามกลุ่มรายได้ (2) สัดส่วนรายได้ > 50K ตาม `occupation` · ตีความแต่ละรูป"),
("code", '''
fig, ax = plt.subplots(1, 2, figsize=(13, 4))
sns.histplot(df, x="age", hue="income", stat="density", common_norm=False, bins=30, ax=ax[0])
ax[0].set_title("Age by income (normalized)")
occ = df.groupby("occupation")["rich"].mean().sort_values()
occ.plot.barh(ax=ax[1]); ax[1].set_title("Share >50K by occupation"); ax[1].set_xlabel("share")
plt.tight_layout(); plt.show()
print(occ.tail(3).round(3))
'''),
("ans", """
(1) histogram แบบ normalize (เพราะสองกลุ่มขนาดต่างกัน): กลุ่ม > 50K กระจุกช่วง **~35–55 ปี** ส่วนกลุ่ม ≤ 50K มีคนอายุน้อย (< 30) จำนวนมาก → อายุ/ประสบการณ์สัมพันธ์กับรายได้
(2) bar แนวนอนเรียงค่า: Exec-managerial และ Prof-specialty มีสัดส่วนรายได้สูงที่สุด ส่วนงานบริการ/แรงงานต่ำสุด → occupation เป็น feature ที่น่าจะช่วยทำนาย
"""),
# ── Part B ──
("md", "## Part B · Preprocessing (20 คะแนน)"),
("q", "**B1.** ควรตัดคอลัมน์ใดออกก่อนสร้างโมเดล เพราะอะไร (พิจารณา `person_id`, `fnlwgt`, `educational-num`, `income`)"),
("code", '''
# educational-num ซ้ำกับ education หรือไม่?
print(df.groupby("education")["educational-num"].nunique().max())     # 1 → education แต่ละค่ามี educational-num ค่าเดียว
X = df.drop(columns=["person_id", "fnlwgt", "educational-num", "income", "rich"])
y = df["rich"]
print(X.shape)
'''),
("ans", """
- **person_id** — ตัวระบุ ไม่มีความหมาย (RapidMiner: ตั้ง role = id)
- **fnlwgt** — น้ำหนักการสุ่มของสำมะโน ไม่ใช่คุณสมบัติของบุคคล
- **educational-num** — **redundant** กับ education (หนึ่งค่า education ↔ หนึ่งค่าตัวเลข)
- **income / rich** — คือ target (ถ้าใส่ = leakage)
เหลือ **12 feature** (4 ตัวเลข + 8 categorical)
"""),
("q", "**B2.** สร้าง preprocessing ที่ **ไม่ทำให้เกิด data leakage** สำหรับ: เติมค่าว่าง, scale ตัวเลข, one-hot categorical · อธิบายว่าทำไมไม่ leak"),
("code", '''
num_cols = X.select_dtypes(include="number").columns.tolist()
cat_cols = X.select_dtypes(exclude="number").columns.tolist()
prep = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), num_cols),
    ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                      ("oh", OneHotEncoder(handle_unknown="ignore"))]), cat_cols)])
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
print(num_cols, cat_cols, sep="\\n")
'''),
("ans", """
- ตัวเลข: **median** (capital-gain/loss เบ้มาก) + StandardScaler · categorical: **mode** + one-hot (`handle_unknown="ignore"` กัน fold ที่เจอหมวดใหม่)
- **ไม่ leak** เพราะทุกขั้นอยู่ใน `ColumnTransformer` ที่จะถูกใส่ใน Pipeline → ตอน `cross_validate` แต่ละ fold จะ **fit imputer/scaler/encoder จาก training fold เท่านั้น** แล้วแค่ transform validation fold
- ⚠️ ถ้า `df.fillna(df.median())` หรือ scale ทั้งตารางก่อน CV = ใช้ค่าที่รวม validation fold ไปแล้ว = leakage
"""),
("q", "**B3.** แบ่ง `age` เป็น 4 กลุ่มแบบ **equal frequency** แล้วหาสัดส่วนรายได้ > 50K ในแต่ละกลุ่ม · ทำไมเลือก equal frequency แทน equal width"),
("code", '''
df["age_group"] = pd.qcut(df["age"], q=4)
df.groupby("age_group", observed=True)["rich"].agg(share="mean", n="size").round(3)
'''),
("ans", """
| age_group | ≤ 28 | 29–38 | 39–48 | 49–90 |
|---|---|---|---|---|
| share > 50K | 4.0% | 24.5% | **37.4%** | 31.9% |
สัดส่วนรายได้สูงเพิ่มตามอายุจนสูงสุดช่วง 39–48 แล้วลดลงเล็กน้อย (ใกล้เกษียณ) → ความสัมพันธ์ **ไม่เป็นเชิงเส้น**
**equal frequency** ให้ทุกกลุ่มมีราว 1,400–1,600 คน (เทียบสัดส่วนได้น่าเชื่อถือ) · age เบ้ขวา ถ้าใช้ equal width ช่วงอายุมาก (70–90) จะมีคนน้อยมาก
"""),
# ── Part C ──
("md", "## Part C · Baseline & Models (30 คะแนน)"),
("q", "**C1.** ประเมินด้วย 5-fold stratified CV (seed 1992): **majority baseline**, KNN (k=5), Logistic Regression, Decision Tree (max_depth=5), Random Forest (100 ต้น) · รายงาน accuracy / precision / recall / F1 ในตารางเดียว"),
("code", '''
def evaluate(name, clf, smote=False):
    steps = [("prep", prep)] + ([("smote", SMOTE(random_state=SEED))] if smote else []) + [("clf", clf)]
    r = cross_validate(ImbPipeline(steps), X, y, cv=cv, scoring=["accuracy", "precision", "recall", "f1"])
    return {"model": name, **{m: round(r[f"test_{m}"].mean(), 4) for m in ["accuracy", "precision", "recall", "f1"]}}

results = pd.DataFrame([
    evaluate("Majority baseline", DummyClassifier(strategy="most_frequent")),
    evaluate("KNN k=5", KNeighborsClassifier(n_neighbors=5)),
    evaluate("Logistic Regression", LogisticRegression(max_iter=2000)),
    evaluate("Decision Tree d=5", DecisionTreeClassifier(max_depth=5, random_state=SEED)),
    evaluate("Random Forest 100", RandomForestClassifier(n_estimators=100, random_state=SEED, n_jobs=-1)),
])
results
'''),
("ans", """
| model | accuracy | precision | recall | F1 |
|---|---|---|---|---|
| Majority baseline | 0.761 | 0 | 0 | 0 |
| KNN k=5 | 0.816 | 0.628 | 0.569 | 0.597 |
| Logistic Regression | **0.848** | 0.736 | 0.571 | 0.642 |
| Decision Tree d=5 | 0.835 | **0.777** | 0.442 | 0.559 |
| Random Forest 100 | 0.841 | 0.691 | **0.609** | **0.647** |
- ทุกโมเดลดีกว่า baseline · baseline ได้ accuracy **76.1%** ทั้งที่หาคนรวยไม่เจอเลย → ยืนยันว่า **accuracy หลอกได้** เมื่อข้อมูลไม่สมดุล
- **RF ได้ F1 และ recall สูงสุด** · LogReg accuracy สูงสุด · Tree d=5 precision สูงแต่ recall ต่ำ (ทายว่ารวยเฉพาะคนที่มั่นใจมาก)
"""),
# ── Part D ──
("md", "## Part D · Optimization & Imbalance (20 คะแนน)"),
("q", "**D1.** Optimize: (a) KNN — k = 1, 3, …, 31 (b) Random Forest — max_depth ∈ {None, 10, 15} × min_samples_leaf ∈ {1, 3, 5} · ใช้ CV folds เดิม เลือกด้วย **F1** · ดีขึ้นจาก C1 แค่ไหน"),
("code", '''
g_knn = GridSearchCV(ImbPipeline([("prep", prep), ("clf", KNeighborsClassifier())]),
                     {"clf__n_neighbors": list(range(1, 32, 2))}, cv=cv, scoring="f1").fit(X, y)
g_rf = GridSearchCV(ImbPipeline([("prep", prep), ("clf", RandomForestClassifier(random_state=SEED, n_jobs=-1))]),
                    {"clf__max_depth": [None, 10, 15], "clf__min_samples_leaf": [1, 3, 5]},
                    cv=cv, scoring="f1").fit(X, y)
print("KNN:", g_knn.best_params_, round(g_knn.best_score_, 4))
print("RF :", g_rf.best_params_, round(g_rf.best_score_, 4))
'''),
("ans", """
- KNN: best **k = 25** F1 **0.613** (จาก 0.597 ที่ k=5, +0.016) · k ใหญ่ช่วยเพราะข้อมูลมี noise และมีมิติมาก (one-hot)
- RF: best **max_depth = None, min_samples_leaf = 3** F1 **0.650** (จาก 0.647, +0.003 — แทบไม่ต่าง) → ค่า default ของ RF ดีอยู่แล้ว
- สรุป: optimization ช่วยได้เล็กน้อย · F1 ยังติดที่ ~0.65 เพราะ **recall ต่ำ** (ข้อมูลไม่สมดุล) → ไปแก้ด้วย D2/D3
"""),
("q", "**D2.** ใส่ **SMOTE** ให้ Logistic Regression และ RF (ค่าที่ดีที่สุดจาก D1) โดย SMOTE ต้องทำ **เฉพาะ training fold** · เทียบกับไม่ใช้ SMOTE"),
("code", '''
best_rf = {k.split("__")[1]: v for k, v in g_rf.best_params_.items()}
smote_results = pd.DataFrame([
    evaluate("LogReg + SMOTE", LogisticRegression(max_iter=2000), smote=True),
    evaluate("RF tuned + SMOTE", RandomForestClassifier(random_state=SEED, n_jobs=-1, **best_rf), smote=True),
])
smote_results
'''),
("ans", """
| model | accuracy | precision | recall | F1 |
|---|---|---|---|---|
| LogReg (C1) | 0.848 | 0.736 | 0.571 | 0.642 |
| **LogReg + SMOTE** | 0.806 | 0.564 | **0.832** | 0.672 |
| RF tuned + SMOTE | 0.823 | 0.602 | 0.765 | **0.674** |
SMOTE ทำให้ **recall เพิ่มมาก** (LogReg 0.571 → 0.832) และ F1 เพิ่ม · แลกกับ precision และ accuracy ที่ลดลง (ทายว่า "รวย" บ่อยขึ้น → FP มากขึ้น)
SMOTE อยู่ใน `imblearn.Pipeline` ต่อจาก preprocessing → ในแต่ละ fold สร้างจุดสังเคราะห์จาก **training fold เท่านั้น** · validation fold เป็นข้อมูลจริงสัดส่วนจริง
"""),
("q", "**D3.** ไม่ใช้ SMOTE แต่ปรับ **threshold** ของ Logistic Regression จาก 0.5 เป็น 0.3 (ใช้ `cross_val_predict` แบบ predict_proba) · รายงาน confusion matrix, precision, recall, F1 ของทั้งสอง threshold"),
("code", '''
logreg = ImbPipeline([("prep", prep), ("clf", LogisticRegression(max_iter=2000))])
proba = cross_val_predict(logreg, X, y, cv=cv, method="predict_proba")[:, 1]
rows = []
for t in (0.5, 0.3):
    pred = (proba >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, pred).ravel()
    rows.append({"threshold": t, "TN": tn, "FP": fp, "FN": fn, "TP": tp,
                 "precision": precision_score(y, pred), "recall": recall_score(y, pred), "F1": f1_score(y, pred)})
pd.DataFrame(rows).round(3)
'''),
("ans", """
| threshold | TN | FP | FN | TP | precision | recall | F1 |
|---|---|---|---|---|---|---|---|
| 0.5 | 4,267 | 296 | 616 | 820 | 0.735 | 0.571 | 0.643 |
| **0.3** | 3,828 | 735 | 317 | 1,119 | 0.604 | **0.779** | **0.680** |
ลด threshold → หาคนรวยเจอเพิ่ม **299 คน** (FN 616 → 317) แลกกับ FP เพิ่ม 439 คน · F1 ดีขึ้น · ได้ผลใกล้เคียง SMOTE โดยไม่ต้องสร้างข้อมูลสังเคราะห์ (ง่ายกว่า)
"""),
# ── Part E ──
("md", "## Part E · Decision (10 คะแนน)"),
("q", "**E1.** ธนาคารต้องการ \"หาคนรายได้ > 50K ให้ได้มากที่สุด\" ควรใช้ metric ใดและเลือกโมเดลใด เพราะอะไร · **E2.** ทำนายลูกค้าใน `new_person.csv` ด้วยโมเดลที่เลือก (ความน่าจะเป็น + คำตัดสิน)"),
("code", '''
new = pd.read_csv("data/new_person.csv").replace("?", np.nan)
final = ImbPipeline([("prep", prep), ("clf", LogisticRegression(max_iter=2000))]).fit(X, y)
p_new = final.predict_proba(new[X.columns])[0, 1]
print(new[["age", "education", "occupation", "hours-per-week", "gender"]].to_string(index=False))
print("P(>50K) =", round(p_new, 3), "→", "เสนอบัตร" if p_new >= 0.3 else "ไม่เสนอ")
'''),
("ans", """
**E1.** metric หลัก = **recall** (พลาดคนรวย = เสียลูกค้า) โดยดู **F1** ประกอบไม่ให้ precision ต่ำเกินไป (ค่าส่งเอกสารให้คนไม่เข้าเกณฑ์)
เลือก **Logistic Regression + threshold 0.3**: recall **0.779**, F1 **0.680** ใกล้เคียง RF + SMOTE (0.765 / 0.674) แต่ **ง่าย เร็ว ตีความได้** (coefficient/odds) และไม่ต้องใช้ข้อมูลสังเคราะห์ · ถ้าต้องการ recall สูงสุดเลือก LogReg + SMOTE (0.832)
**E2.** ลูกค้าอายุ 47 เรียน 5th-6th งาน Sales ทำงาน 32 ชม./สัปดาห์ → **P(> 50K) ≈ 0.002** → **ไม่เสนอบัตร** (ต่ำกว่า threshold 0.3 มาก — การศึกษาต่ำและชั่วโมงทำงานน้อยเป็นปัจจัยหลัก)
"""),
("md", """
## Part C ใน RapidMiner (ทำซ้ำ — 60 นาที)
สร้าง process เดียวกับ C1 ใน RapidMiner แล้วเทียบผล — เฉลย: `solution_partC.rmp`
`Read CSV ×3` → `Append` (H1, H2) → `Join` (inner, key = person_id) → `Declare Missing Value` ("?") → `Select Attributes` (ตัด fnlwgt, educational-num) → `Set Role` (income = label, person_id = id) → `Nominal to Numerical` (dummy) → `Multiply` → `Cross Validation` ×3 (5 folds, stratified, seed 1992):
**Default Model** · **Normalize → k-NN → Group Models** · **Random Forest** → แต่ละตัว Testing: `Apply Model` → `Performance (Binominal Classification)` (ติ๊ก **manually set positive class** → positive class = `>50K` · ไม่งั้น RapidMiner อาจคิด precision/recall ให้ `<=50K`)
"""),
]

# ════════════════════════════════════════════════════════════════════════════════════════════
# MOCK 2 — Regression + PCA (Boston)
# ════════════════════════════════════════════════════════════════════════════════════════════
M2 = [
("md", """
# Mock Lab 2 — House Price (Regression + KNN Regressor + PCA)
**เวลา:** 75 นาที · **seed = 1992** · hold-out 80/20 (`random_state=1992`) · CV = KFold 5 folds (shuffle, seed 1992) บน training set
ข้อมูล `data/housing.csv` (503 หลัง, target = `medv` ราคาบ้านเป็นพันดอลลาร์) · `data/new_houses.csv` = บ้านใหม่ 3 หลังให้ทำนาย
"""),
("md", "## ตั้งต้น"),
("code", SETUP),
("md", "## Part A · EDA (20 คะแนน)"),
("q", "**A1.** สรุปสถิติของ `medv` + histogram · การกระจายเป็นอย่างไร มีอะไรผิดปกติ"),
("code", '''
h = pd.read_csv("data/housing.csv")
print(h.shape)
print(h["medv"].describe().round(2))
print("skew =", round(h["medv"].skew(), 3), "| จำนวนบ้าน medv = 50:", (h["medv"] == 50).sum())
h["medv"].plot.hist(bins=30, title="medv"); plt.show()
'''),
("ans", """
mean 22.55 > median 21.2 · **skew = 1.10 (เบ้ขวา)** · มีบ้าน **medv = 50.0 ถึง 16 หลัง** กองที่ค่าสูงสุดพอดี → น่าจะถูก **ตัดเพดาน (censored at 50)** ไม่ใช่ราคาจริง → ควรเขียนกำกับว่าโมเดลจะทายบ้านแพงต่ำกว่าจริง
"""),
("q", "**A2.** heatmap correlation · ตัวแปรใด 3 ตัวที่สัมพันธ์กับ `medv` มากที่สุด (|r|) · คู่ predictor ใดสัมพันธ์กันเองสูงสุด และเป็นปัญหาอย่างไร"),
("code", '''
corr = h.corr()
sns.heatmap(corr, cmap="coolwarm", center=0, annot=True, fmt=".1f", annot_kws={"size": 7}); plt.show()
r = corr["medv"].drop("medv")
print(r.reindex(r.abs().sort_values(ascending=False).index).head(3).round(3))
pred_corr = h.drop(columns="medv").corr().abs()
pairs = pred_corr.where(np.triu(np.ones(pred_corr.shape, bool), k=1)).stack().sort_values(ascending=False)
print(pairs.head(3).round(3))
'''),
("ans", """
top 3: **lstat (r = −0.738)**, **rm (+0.696)**, **ptratio (−0.508)** → ชุมชนรายได้ต่ำมาก ราคาต่ำ · ห้องมาก ราคาสูง · ครูน้อยต่อนักเรียน ราคาต่ำ
คู่ predictor: **rad–tax r = 0.91**, nox–dis 0.77, indus–nox 0.77 → **multicollinearity**: coefficient ของ rad/tax ใน linear regression จะไม่เสถียร ตีความยาก (เครื่องหมายอาจกลับ) · แนวทาง: เก็บตัวเดียว / รวม / ใช้ regularization
"""),
("md", "## Part B · Linear Regression (30 คะแนน)"),
("q", "**B1.** split 80/20 · เทียบ **mean baseline**, Linear Regression ทุกตัวแปร, Linear Regression 2 ตัว (lstat, rm) ด้วย MAE / MSE / RMSE / R² บน test"),
("code", '''
X, y = h.drop(columns="medv"), h["medv"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)

def test_row(name, model, cols=None):
    cols = cols or list(X.columns)
    p = model.fit(X_train[cols], y_train).predict(X_test[cols])
    return {"model": name, "MAE": mean_absolute_error(y_test, p), "MSE": mean_squared_error(y_test, p),
            "RMSE": root_mean_squared_error(y_test, p), "R2": r2_score(y_test, p)}

pd.DataFrame([test_row("Mean baseline", DummyRegressor(strategy="mean")),
              test_row("LinReg (13 features)", LinearRegression()),
              test_row("LinReg (lstat, rm)", LinearRegression(), ["lstat", "rm"])]).round(3)
'''),
("ans", """
| model | MAE | MSE | RMSE | R² |
|---|---|---|---|---|
| Mean baseline | 7.019 | 106.17 | 10.304 | −0.029 |
| LinReg 13 ตัว | **3.889** | **36.15** | **6.013** | **0.649** |
| LinReg 2 ตัว | 4.562 | 44.06 | 6.638 | 0.573 |
ทั้งสองดีกว่า baseline มาก (RMSE ลด ~40%) · 13 ตัวดีกว่า 2 ตัว (R² +0.076) แต่ 2 ตัวง่ายกว่ามาก → เลือกตามเป้าหมาย (ทำนาย vs อธิบาย)
"""),
("q", "**B2.** เขียนสมการของโมเดล 2 ตัวแปร และตีความ coefficient · ในโมเดล 13 ตัว coefficient ของ `nox` = −16.4 แปลว่าอะไร และทำไมไม่ควรสรุปว่า nox สำคัญที่สุด"),
("code", '''
lin2 = LinearRegression().fit(X_train[["lstat", "rm"]], y_train)
print(f"medv = {lin2.intercept_:.3f} + ({lin2.coef_[0]:.4f})·lstat + ({lin2.coef_[1]:.4f})·rm")
lin13 = LinearRegression().fit(X_train, y_train)
print(pd.Series(lin13.coef_, index=X.columns).round(4))
print(X[["nox", "rm", "tax"]].std().round(3))
'''),
("ans", """
**medv = −1.616 − 0.610·lstat + 5.050·rm** → lstat เพิ่ม 1 จุด % ราคาลด 0.61 พันดอลลาร์ (rm คงที่) · ห้องเพิ่ม 1 ห้อง ราคาเพิ่ม 5.05 พันดอลลาร์ (lstat คงที่)
nox = −16.4 → nox เพิ่ม **1 หน่วย** ราคาลด 16.4 พันดอลลาร์ (ตัวอื่นคงที่) — แต่ nox มี SD แค่ **0.116** (1 หน่วยกว้างกว่าช่วงข้อมูลทั้งหมด) → coefficient ใหญ่เพราะ **หน่วยเล็ก** · เทียบความสำคัญต้องใช้ **standardized coefficient** (หรือ coef × SD) · และ nox สัมพันธ์สูงกับ dis/indus (multicollinearity)
"""),
("md", "## Part C · KNN Regressor (25 คะแนน)"),
("q", "**C1.** เทียบ KNN regressor (k = 5) **ไม่ scale vs StandardScaler** และ Linear Regression ด้วย 5-fold CV บน training set (RMSE, R²) · **C2.** Optimize k = 1–20 × weights ∈ {uniform, distance} แล้วประเมินตัวที่ดีที่สุดบน test"),
("code", '''
kcv = KFold(n_splits=5, shuffle=True, random_state=SEED)
cands = {"KNN raw k=5": KNeighborsRegressor(n_neighbors=5),
         "KNN scaled k=5": Pipeline([("sc", StandardScaler()), ("knn", KNeighborsRegressor(n_neighbors=5))]),
         "LinReg": LinearRegression()}
rows = []
for name, m in cands.items():
    r = cross_validate(m, X_train, y_train, cv=kcv, scoring=["neg_root_mean_squared_error", "r2"])
    rows.append({"model": name, "CV RMSE": -r["test_neg_root_mean_squared_error"].mean(), "CV R2": r["test_r2"].mean()})
print(pd.DataFrame(rows).round(3).to_string(index=False))

grid = GridSearchCV(Pipeline([("sc", StandardScaler()), ("knn", KNeighborsRegressor())]),
                    {"knn__n_neighbors": range(1, 21), "knn__weights": ["uniform", "distance"]},
                    cv=kcv, scoring="neg_root_mean_squared_error").fit(X_train, y_train)
print(grid.best_params_, "CV RMSE =", round(-grid.best_score_, 3))
pd.DataFrame([test_row("KNN tuned (test)", grid.best_estimator_)]).round(3)
'''),
("ans", """
| model | CV RMSE | CV R² |
|---|---|---|
| KNN raw k=5 | 6.318 | 0.483 |
| **KNN scaled k=5** | **4.436** | **0.749** |
| LinReg | 4.678 | 0.715 |
**scaling ลด RMSE 30%** (6.32 → 4.44) เพราะ tax/black (หลักร้อย) ครองระยะทาง · KNN scaled ชนะ LinReg เล็กน้อย → ความสัมพันธ์มีส่วนที่ไม่เป็นเชิงเส้น
best: **k = 6, weights = distance** (CV RMSE 4.219) → test **RMSE 5.008, R² 0.757** ดีกว่า LinReg บน test (6.013 / 0.649)
"""),
("md", "## Part D · PCA (25 คะแนน)"),
("q", "**D1.** standardize 13 feature แล้วทำ PCA: ตาราง explained variance + cumulative · ต้องใช้กี่ component ถึง 80% · ถ้าใช้เกณฑ์ eigenvalue > 1 ได้กี่ตัว · **D2.** loading สูงสุดของ PC1 (4 ตัว) และ PC2 (3 ตัว) ตีความ · **D3.** scatter PC1 × PC2 ระบายสีตาม medv 3 ช่วง (equal frequency: Low/Mid/High)"),
("code", '''
Z = StandardScaler().fit_transform(X)        # PCA เพื่ออธิบาย/visualize ทำกับข้อมูลทั้งชุดได้ (ไม่ได้ใช้วัดผลโมเดล)
pca = PCA().fit(Z)
evr = pd.DataFrame({"explained": pca.explained_variance_ratio_, "cumulative": pca.explained_variance_ratio_.cumsum(),
                    "eigenvalue": pca.explained_variance_}, index=[f"PC{i+1}" for i in range(13)]).round(4)
print(evr.head(6))
print("PC for 80%:", int((evr["cumulative"] < 0.8).sum() + 1), "| eigenvalue > 1:", int((evr["eigenvalue"] > 1).sum()))
load = pd.DataFrame(pca.components_[:2].T, index=X.columns, columns=["PC1", "PC2"]).round(3)
print(load.reindex(load["PC1"].abs().sort_values(ascending=False).index).head(4))
print(load.reindex(load["PC2"].abs().sort_values(ascending=False).index).head(3))
band = pd.qcut(y, 3, labels=["Low", "Mid", "High"])
P = pca.transform(Z)[:, :2]
for b, c in zip(["Low", "Mid", "High"], ["#D55E00", "#999999", "#0072B2"]):
    m = (band == b).to_numpy()
    plt.scatter(P[m, 0], P[m, 1], s=12, alpha=0.6, color=c, label=b)
plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})"); plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
plt.legend(title="medv"); plt.show()
print(pd.DataFrame(P, columns=["PC1", "PC2"]).groupby(band.values, observed=True).mean().round(2))
'''),
("ans", """
PC1 **47.2%**, PC2 11.0%, PC3 9.5% → สะสม 47.2 → 58.2 → 67.8 → 74.4 → **80.8%** → ต้องใช้ **5 components** ถึง 80% · eigenvalue > 1 (Kaiser) ได้ **3 ตัว**
PC1 loading: indus +0.35, nox +0.34, tax +0.34, dis −0.32 → **"ความเป็นเขตอุตสาหกรรม/เมืองชั้นใน"** (โรงงาน มลพิษ ภาษีสูง ใกล้ศูนย์กลาง) · PC2: chas +0.46, dis −0.35, zn −0.33 → ติดแม่น้ำ/ใกล้เมือง
scatter: ค่าเฉลี่ย PC1 ของบ้าน Low = **+2.24**, Mid −0.44, High **−1.84** → **บ้านราคาต่ำอยู่ฝั่ง PC1 สูง** (เขตอุตสาหกรรม) แยกตามแกน PC1 ได้ชัด ส่วน PC2 แยกไม่ค่อยได้ · ⚠️ 2 PC เก็บได้แค่ 58% ของความแปรปรวน
"""),
("q", "**E.** ทำนายราคา `new_houses.csv` ด้วย Linear Regression (13 ตัว) และ KNN ที่ดีที่สุด · แล้วเปิด `new_houses_answer.csv` เทียบ"),
("code", '''
new = pd.read_csv("data/new_houses.csv")
truth = pd.read_csv("data/new_houses_answer.csv")["medv"]
pd.DataFrame({"LinReg": lin13.predict(new).round(2),
              "KNN tuned": grid.best_estimator_.predict(new).round(2), "actual": truth})
'''),
("ans", """
| | LinReg | KNN tuned | actual |
|---|---|---|---|
| บ้าน 1 | 20.33 | 20.91 | 21.8 |
| บ้าน 2 | 20.43 | 19.70 | 19.3 |
| บ้าน 3 | 19.03 | 20.06 | 19.9 |
KNN ใกล้ค่าจริงกว่าใน 3 หลังนี้ (|error| เฉลี่ย **0.48** vs **1.16**) สอดคล้องกับผล test · **เลือก KNN (k = 6, distance, scaled)** เพื่อทำนาย · ถ้าต้องอธิบายปัจจัยราคา ใช้ LinReg ประกอบ
"""),
]

# ════════════════════════════════════════════════════════════════════════════════════════════
# MOCK 3 — Clustering + Association
# ════════════════════════════════════════════════════════════════════════════════════════════
M3 = [
("md", """
# Mock Lab 3 — Utility Segmentation & Bank Cross-selling (Clustering + Association Rules)
**เวลา:** 75 นาที · **seed = 1992**
Part A: `data/utilities.csv` — 22 บริษัทไฟฟ้า × 8 ตัวแปร (ข้อมูลเดียวกับสไลด์ clustering p.10)
Part B: `data/bank-data.csv` — ลูกค้า 600 คน · `pep` = ซื้อ Personal Equity Plan หรือไม่
"""),
("md", "## ตั้งต้น"),
("code", SETUP),
("md", "## Part A · Clustering (50 คะแนน)"),
("q", "**A1.** เตรียมข้อมูลสำหรับ K-Means (อะไรต้องตัด/ตั้ง role · ต้อง normalize ไหม เพราะอะไร) · **A2.** K-Means k = 2…8 (`n_init=50`) รายงาน WCSS, silhouette, Davies–Bouldin + กราฟ แล้วเลือก k พร้อมเหตุผล"),
("code", '''
u = pd.read_csv("data/utilities.csv").set_index("Company")      # Company = id → ไม่ใช้คำนวณระยะทาง
print(u.agg(["min", "max", "std"]).round(2))                     # Sales หลักหมื่น vs Fixed_charge ~1
scaler = StandardScaler().fit(u)
Z = pd.DataFrame(scaler.transform(u), index=u.index, columns=u.columns)
rows = []
for k in range(2, 9):
    km = KMeans(n_clusters=k, n_init=50, random_state=SEED).fit(Z)
    rows.append({"k": k, "WCSS": km.inertia_, "silhouette": silhouette_score(Z, km.labels_),
                 "DB": davies_bouldin_score(Z, km.labels_), "sizes": sorted(np.bincount(km.labels_), reverse=True)})
ks = pd.DataFrame(rows).round(3)
fig, ax = plt.subplots(1, 2, figsize=(10, 3.5))
ax[0].plot(ks["k"], ks["WCSS"], "o-"); ax[0].set_title("Elbow")
ax[1].plot(ks["k"], ks["silhouette"], "o-", color="#D55E00"); ax[1].set_title("Silhouette"); plt.show()
ks
'''),
("ans", """
- ตั้ง `Company` เป็น index/id (ไม่ใช้คำนวณ) · ทุกตัวแปรเป็นตัวเลขแล้ว
- **ต้อง normalize** — Sales อยู่ช่วง 3,300–17,441 ขณะที่ Fixed_charge 0.75–1.49 → ถ้าไม่ scale ระยะทาง Euclidean ≈ ผลต่าง Sales อย่างเดียว
- WCSS ลดลงเรื่อย ๆ (137 → 46) ไม่มีข้อศอกชัด · silhouette สูงสุดที่ **k = 5 (0.248)** รองลงมา **k = 4 (0.234)** และ k = 3 (0.230) · DB ลดตาม k (k มากขึ้นดูดีขึ้นเสมอ — อย่าใช้ DB ตัวเดียว)
- k = 5 มีกลุ่มสมาชิกเพียง 1 บริษัท (sizes 7/6/5/3/1) · **เลือก k = 4** (silhouette 0.234 ใกล้ k = 5 แต่ทุกกลุ่มมี ≥ 3 บริษัท ตีความได้) — ถ้าเลือก k = 5 ก็รับได้หากให้เหตุผลด้วย silhouette
"""),
("q", "**A3.** ด้วย k ที่เลือก: แสดงสมาชิก + centroid (หน่วยเดิม และ z-score) แล้วตั้งชื่อ/อธิบายแต่ละกลุ่ม · **A4.** บริษัทใหม่ Fixed_charge 1.10, RoR 11.0, Cost 160, Load 56, Demand 3.0, Sales 14,000, Nuclear 0, Fuel 0.70 อยู่กลุ่มไหน"),
("code", '''
km4 = KMeans(n_clusters=4, n_init=50, random_state=SEED).fit(Z)
lab = pd.Series(km4.labels_, index=u.index, name="cluster")
print(lab.groupby(lab).apply(lambda s: ", ".join(s.index)).to_string())
print(u.groupby(lab).mean().round(2).to_string())
print(pd.DataFrame(km4.cluster_centers_, columns=u.columns).round(2).to_string())
new = pd.DataFrame([[1.10, 11.0, 160, 56.0, 3.0, 14000, 0.0, 0.70]], columns=u.columns)
print("บริษัทใหม่ → cluster", km4.predict(pd.DataFrame(scaler.transform(new), columns=u.columns))[0])
'''),
("ans", """
(เลข cluster อาจสลับได้ — ดูที่สมาชิก)
| กลุ่ม | สมาชิก | ลักษณะ (z ของ centroid) | ชื่อ |
|---|---|---|---|
| A | Idaho, Nevada, Puget | Sales +1.90 · Cost +1.37 · Demand +1.02 · Fuel −0.99 | ขายมาก โตเร็ว เชื้อเพลิงถูก |
| B | Boston, NY, Hawaiian, New England, Pacific, San Diego, United | Fuel_Cost +1.28 · Load +0.82 · Sales −0.88 | เชื้อเพลิงแพง ขายน้อย |
| C | Commonwealth, Madison, Northern, Wisconsin, Virginia | Nuclear +1.60 | พึ่งพานิวเคลียร์ |
| D | Arizona, Central, Florida, Kentucky, Oklahoma, Southern, Texas | Cost −1.01 · RoR +0.80 | ต้นทุนต่ำ ผลตอบแทนดี |
**A4.** บริษัทใหม่ (Sales 14,000 ค่อนข้างสูง, Cost/Fuel ต่ำ, ไม่มี nuclear) → ตกกลุ่ม **D "ต้นทุนต่ำ ผลตอบแทนดี"** (ต้อง transform ด้วย scaler ตัวเดิมก่อน predict)
"""),
("q", "**A5.** วาดกลุ่มบน PCA 2 มิติ (ใส่ชื่อบริษัท) และประเมิน cohesion / separation จากภาพ"),
("code", '''
pca = PCA(n_components=2).fit(Z); P = pca.transform(Z)
plt.figure(figsize=(7, 5))
plt.scatter(P[:, 0], P[:, 1], c=km4.labels_, cmap="tab10", s=60)
for name, (a, b) in zip(u.index, P):
    plt.annotate(name, (a, b), fontsize=7, xytext=(3, 3), textcoords="offset points")
plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.0%})"); plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.0%})")
plt.show()
print("PC1+PC2 =", pca.explained_variance_ratio_[:2].sum().round(3))
'''),
("ans", """
2 PC เก็บความแปรปรวนได้เพียง **50.9%** (8 มิติ → 2) จึงเห็นภาพบางส่วนเท่านั้น · กลุ่ม Idaho/Nevada/Puget แยกออกจากกลุ่มอื่นชัด (**separation ดี**) · กลุ่มเชื้อเพลิงแพงกระจายกว้าง (**cohesion ต่ำ** — San Diego, NY อยู่ขอบ) · ภาพสอดคล้องกับ silhouette ~0.23 (กลุ่มซ้อนกันบางส่วน)
"""),
("md", "## Part B · Association Rules (50 คะแนน)"),
("q", "**B1.** เลือก attribute ที่เหมาะกับการหากฎ (อธิบายว่าตัดอะไรเพราะอะไร) · discretize `age`, `income` เป็น 3 ช่วง equal frequency, `children` เป็น 0 / 1-2 / 3+ · แปลงเป็นตาราง item (True/False)"),
("code", '''
b = pd.read_csv("data/bank-data.csv")
print(b["sex"].value_counts(normalize=True).round(3).to_dict(), b["current_act"].value_counts(normalize=True).round(3).to_dict())
basket = pd.DataFrame({
    "age": pd.qcut(b["age"], 3, labels=["YOUNG", "MIDDLE", "SENIOR"]),
    "income": pd.qcut(b["income"], 3, labels=["LOW", "MID", "HIGH"]),
    "children": pd.cut(b["children"], [-1, 0, 2, 10], labels=["0", "1-2", "3+"]),
})
for c in ["married", "car", "save_act", "mortgage", "pep"]:
    basket[c] = b[c]
items = pd.get_dummies(basket, prefix_sep="=").astype(bool)
print(items.shape)
items.head(3)
'''),
("ans", """
ตัด **id** (ไม่ซ้ำทุกแถว = ไม่มีวันเป็น frequent item) · **region** (4 ค่า ทำให้ support กระจายจนกฎน้อย) · **sex** (50/50 พอดี ไม่ให้ข้อมูล) · **current_act** (YES 75.8% เกือบคงที่ → ไปโผล่ในกฎเกือบทุกข้อโดยไม่มีความหมาย)
discretize: equal frequency เพราะ income **เบ้ขวา** (equal width ช่วง HIGH จะแทบว่าง) · children ใช้ช่วงตามความหมาย
ได้ **600 transaction × 19 item** (แต่ละ item = attribute=value)
"""),
("q", "**B2.** Apriori min_support = 0.10 · rules min_confidence = 0.70 · แสดง 5 กฎที่ทำนาย `pep=YES` เรียงตาม lift · ตีความกฎอันดับ 1 ครบ support/confidence/lift + ข้อเสนอธุรกิจ · **B3.** ถ้าเพิ่ม min_support เป็น 0.20 เกิดอะไรขึ้น"),
("code", '''
def pep_rules(min_support):
    freq = apriori(items, min_support=min_support, use_colnames=True)
    rules = association_rules(freq, metric="confidence", min_threshold=0.70)
    pep = rules[rules["consequents"] == frozenset({"pep=YES"})].sort_values("lift", ascending=False)
    print(f"min_support={min_support}: itemsets={len(freq)} rules={len(rules)} rules→pep=YES: {len(pep)}")
    return pep[["antecedents", "support", "confidence", "lift"]].round(3)

print("P(pep=YES) =", round(items["pep=YES"].mean(), 3))
display(pep_rules(0.10).head(5))
pep_rules(0.20)
'''),
("ans", """
P(pep=YES) = **0.457** · min_support 0.10 → 413 itemsets · 215 rules · ทำนาย pep=YES **8 กฎ** · 4 อันดับแรก:
| antecedents | support | confidence | lift |
|---|---|---|---|
| age=SENIOR, income=HIGH, children=1-2 | 0.105 | 0.940 | **2.059** |
| income=HIGH, children=1-2, mortgage=NO | 0.103 | 0.939 | 2.057 |
| save_act=YES, income=HIGH, children=1-2 | 0.125 | 0.926 | 2.028 |
| income=HIGH, children=1-2 | 0.145 | 0.926 | 2.027 |
**กฎอันดับ 1:** 10.5% ของลูกค้าทั้งหมดเป็นผู้สูงวัย รายได้สูง มีลูก 1–2 คน **และ** ซื้อ PEP · ในกลุ่มนี้ **94.0%** ซื้อ PEP · สูงกว่าอัตราซื้อทั่วไป (45.7%) **2.06 เท่า**
**ข้อเสนอ:** เจาะกลุ่ม "รายได้สูง + มีลูก 1–2 คน" (ปรากฏในทุกกฎอันดับต้น) ด้วยแคมเปญ PEP เพื่อการศึกษาลูก/เกษียณ
**B3.** min_support 0.20 → **ไม่มีกฎที่ทำนาย pep=YES เลย** — กลุ่มที่สัมพันธ์กับ PEP สูงเป็น **กลุ่มเฉพาะ (~10–15% ของลูกค้า)** ตั้ง support สูงเกินจึงตัดกฎที่มีประโยชน์ทิ้ง · ตั้งต่ำเกินได้กฎมากเกินและไม่น่าเชื่อถือ → เลือก support ตามขนาดกลุ่มเป้าหมายที่ธุรกิจยอมรับได้
"""),
("md", """
## ทำซ้ำใน RapidMiner — เฉลย `solution_rapidminer.rmp`
- **Part A:** `Read CSV` → `Set Role` (Company = id) → `Normalize` (Z) → `k-Means` (k = 4, max runs 50, good start values) → `Cluster Distance Performance` (Davies Bouldin) · elbow: ครอบด้วย `Optimize Parameters (Grid)` + `Log`
- **Part B:** `Read CSV` → `Select Attributes` (ตัด id, region, sex, current_act) → `Discretize by Frequency` (age, income: 3 bins) → `Discretize by User Specification` (children) → `Nominal to Binominal` → `FP-Growth` (min support 0.1) → `Create Association Rules` (min confidence 0.7)
"""),
]

if __name__ == "__main__":
    build("mock1_classification", M1)
    build("mock2_regression_pca", M2)
    build("mock3_cluster_assoc", M3)
