---
title: LAB 09 · Cheat Sheet
exam: Lab — จ. 12 ต.ค. 2569 09:00–12:00
tags: [final, lab, cheatsheet]
---

# LAB 09 · Cheat Sheet
### หน้าเดียวสำหรับห้องสอบ — template · helper · skeleton · operator chain · กับดัก

**ลิงก์:** [[LAB 00 START HERE|หน้าหลัก Lab]] · รายละเอียดแต่ละเรื่อง: [[LAB 02 Data Handling & Visualization|02 Data]] · [[LAB 03 Preprocessing Recipes|03 Prep]] · [[LAB 04 Workflow, Baseline & Evaluation|04 Eval]] · [[LAB 05 Supervised Models|05 Models]] · [[LAB 06 Clustering & Association|06 Unsup]] · [[LAB 07 Reading & Explaining Results|07 Read]]

> [!tip] ถ้าสอบ closed-book: ท่อง 3 อย่างนี้ให้ได้
> 1. ลำดับ **split → fit บน train → transform test** (หรือ Pipeline)
> 2. **Cross Validation:** Training = preprocess + learner (+ Group Models) · Testing = Apply Model + Performance
> 3. ทุกข้อ: **process → settings → results → interpretation** + เทียบ baseline

---

## 1. Template cell แรกของ notebook

```python
# ===== 6710503739 — Final Lab =====
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import (train_test_split, StratifiedKFold, KFold,
                                     cross_validate, cross_val_predict, GridSearchCV)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder, KBinsDiscretizer
from sklearn.decomposition import PCA
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
                             confusion_matrix, ConfusionMatrixDisplay, classification_report,
                             mean_absolute_error, mean_squared_error, root_mean_squared_error, r2_score,
                             silhouette_score, davies_bouldin_score)
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder

SEED = 42                                  # ใช้ค่าเดียวทุกที่ → ผลซ้ำได้ · ถ้าโจทย์กำหนด (เช่น 1992) ใช้ตามโจทย์
pd.set_option("display.max_columns", 50)
```

## 2. Helper functions (copy ทั้งบล็อก)

```python
def check(df, target=None):
    """ตรวจข้อมูลเบื้องต้นใน 1 คำสั่ง: ขนาด · ชนิด · ค่าว่าง · ค่าแฝง · สัดส่วน target"""
    print("shape:", df.shape, "| duplicated rows:", df.duplicated().sum())
    info = pd.DataFrame({"dtype": df.dtypes.astype(str), "missing": df.isna().sum(),
                         "unique": df.nunique()})
    sentinels = {c: int(df[c].isin(["?", " ", ""]).sum()) for c in df.select_dtypes(exclude="number")}
    info["'?'/blank"] = pd.Series(sentinels)
    print(info.fillna(0).to_string())
    if target is not None:
        print(df[target].value_counts(normalize=True).round(4))


def evaluate(name, model, X, y, cv, settings=""):
    """classification: CV → 1 แถว (mean) ใช้ต่อเป็นตารางเปรียบเทียบ"""
    r = cross_validate(model, X, y, cv=cv, scoring=["accuracy", "precision", "recall", "f1"])
    row = {"model": name, "settings": settings}
    row.update({m: round(r[f"test_{m}"].mean(), 4) for m in ["accuracy", "precision", "recall", "f1"]})
    return row


def evaluate_reg(name, model, X, y, cv, settings=""):
    """regression: CV → MAE / RMSE / R²"""
    r = cross_validate(model, X, y, cv=cv,
                       scoring=["neg_mean_absolute_error", "neg_root_mean_squared_error", "r2"])
    return {"model": name, "settings": settings,
            "MAE": round(-r["test_neg_mean_absolute_error"].mean(), 4),
            "RMSE": round(-r["test_neg_root_mean_squared_error"].mean(), 4),
            "R2": round(r["test_r2"].mean(), 4)}


def cm_report(model, X, y, cv, labels=(0, 1)):
    """confusion matrix จาก CV (แต่ละแถวถูกทำนายตอนอยู่ใน test fold)"""
    pred = cross_val_predict(model, X, y, cv=cv)
    cm = confusion_matrix(y, pred, labels=list(labels))
    print(pd.DataFrame(cm, index=[f"actual {l}" for l in labels], columns=[f"pred {l}" for l in labels]))
    print(classification_report(y, pred, digits=3))
    return cm


def top_k(grid, n=5):
    """ตาราง n อันดับแรกของ GridSearchCV (คอลัมน์ param_* + mean_test_*)"""
    res = pd.DataFrame(grid.cv_results_)
    cols = [c for c in res if c.startswith("param_")] + [c for c in res if c.startswith("mean_test_")]
    key = f"mean_test_{grid.refit}" if isinstance(grid.refit, str) else "mean_test_score"
    return res[cols].sort_values(key, ascending=False).head(n).round(4)
```

```python
# ทดสอบ helper กับข้อมูลจริง (ใช้ตรวจว่า copy มาครบ)
ads = pd.read_csv("W12/Social_Network_Ads_2.csv")
check(ads, target="Purchased")
ads["Gender"] = (ads["Gender"] == "Male").astype(int)
X, y = ads[["Gender", "Age", "EstimatedSalary"]], ads["Purchased"]
cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=SEED)
knn = Pipeline([("scale", StandardScaler()), ("knn", KNeighborsClassifier())])
rows = [evaluate("Majority", DummyClassifier(strategy="most_frequent"), X, y, cv),
        evaluate("KNN k=5", knn, X, y, cv, "k=5")]
grid = GridSearchCV(knn, {"knn__n_neighbors": range(1, 21)}, cv=cv, scoring=["f1", "recall"], refit="f1").fit(X, y)
rows.append(evaluate("KNN tuned", grid.best_estimator_, X, y, cv, str(grid.best_params_)))
print(pd.DataFrame(rows).to_string(index=False))
print(top_k(grid, 3))
_ = cm_report(grid.best_estimator_, X, y, cv)
```

## 3. Skeleton ที่ใช้บ่อย

```python
# skip-test  (แม่แบบ — แทน df / "target" / รายชื่อคอลัมน์ ด้วยของจริง)
# ── preprocessing ไม่ leak ──
num_cols = X.select_dtypes(include="number").columns.tolist()
cat_cols = X.select_dtypes(exclude="number").columns.tolist()
prep = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), num_cols),
    ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                      ("oh", OneHotEncoder(handle_unknown="ignore"))]), cat_cols)])

# ── classification + SMOTE ใน CV ──
model = ImbPipeline([("prep", prep), ("smote", SMOTE(random_state=SEED)),
                     ("clf", RandomForestClassifier(random_state=SEED))])

# ── grid search ──
grid = GridSearchCV(model, {"clf__n_estimators": [100, 300], "clf__max_depth": [None, 5, 10]},
                    cv=StratifiedKFold(5, shuffle=True, random_state=SEED), scoring="f1").fit(X, y)

# ── logistic threshold ──
proba = fitted_logreg.predict_proba(X_test)[:, 1]
pred = (proba >= 0.3).astype(int)

# ── PCA 2D ──
Z = StandardScaler().fit_transform(X_num)
pca = PCA(n_components=2).fit(Z); P = pca.transform(Z)
print(pca.explained_variance_ratio_, pca.explained_variance_ratio_.cumsum())
loadings = pd.DataFrame(pca.components_.T, index=X_num.columns, columns=["PC1", "PC2"])

# ── K-Means k loop ──
for k in range(2, 11):
    km = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit(Z)
    print(k, km.inertia_, silhouette_score(Z, km.labels_))

# ── association rules ──
items = df_onehot.astype(bool)
rules = association_rules(fpgrowth(items, min_support=0.2, use_colnames=True),
                          metric="confidence", min_threshold=0.7).sort_values("lift", ascending=False)
```

## 4. RapidMiner — operator chain บรรทัดเดียวต่อ task

| Task | Chain |
|---|---|
| เตรียม label 0/1 | `Read CSV` → `Numerical to Binominal` (label, min 0 max 0) → `Set Role` (label; + id) · ใน Performance ติ๊ก **manually set positive class** |
| ตัด/เลือกคอลัมน์ · แถว | `Select Attributes` (subset, invert) · `Filter Examples` (custom filters, match all/any) |
| รวมตาราง | `Join` (left/right, join type, key attributes) · `Append` (example set 1, 2…) |
| สรุปกลุ่ม | `Aggregate` (group by + function) · `Pivot` (group by, column grouping, aggregation) · `Generate Attributes` (`if(Churn=="Yes",1,0)`) |
| ค่าว่าง | `Replace Missing Values` (average/zero/value; columns list) |
| encode | `Nominal to Numerical` (dummy coding / unique integers) · `Nominal to Binominal` |
| scale | `Normalize` (Z-transformation / range transformation) → `pre` ไป `Apply Model` |
| discretize | `Discretize by Binning` (width) · `by Frequency` · `by User Specification` |
| hold-out | `Split Data` (0.8/0.2, stratified, seed) → train: learner · test: `Apply Model` → `Performance` |
| CV | `Cross Validation` [Training: `Normalize` → learner → `Group Models` · Testing: `Apply Model` → `Performance (Binominal Classification)`] |
| baseline | learner = `Default Model` (mode / average) |
| tune | `Optimize Parameters (Grid)` ครอบ CV · Edit Parameter Settings (k-NN.k 1–10) · main criterion ใน Performance · `Log` + `Log to Data` |
| threshold | `Apply Model` → `Apply Threshold` ← `Create Threshold` (threshold, first = negative, second = positive) |
| imbalance | Training pane: `SMOTE Upsampling` (Operator Toolbox) หรือ `Sample` (balance data) |
| PCA | `Normalize` → `Principal Component Analysis` (fixed number = 2 / keep variance 0.95) → Scatter pc_1 × pc_2 color = label |
| models | `k-NN` · `Linear Regression` (**feature selection = none**) · `Logistic Regression` · `Decision Tree` (criterion!) · `Random Forest` (number of trees) |
| clustering | `Set Role` (id) → `Normalize` → `k-Means` (k, max runs, good start values) → `Cluster Distance Performance` |
| association | `Set Role` (id) → `Numerical to Binominal` / `Nominal to Binominal` → `FP-Growth` (min support, positive value true) → `Create Association Rules` (min confidence) |

## 5. Default ที่ต่างกันระหว่างสองเครื่องมือ (สาเหตุ "ผลไม่ตรงกัน")

| เรื่อง | sklearn | RapidMiner |
|---|---|---|
| z-score | หาร $n$ | หาร $n-1$ |
| Decision Tree criterion | gini | **gain_ratio** · มี pruning + prepruning เปิดอยู่ |
| Linear Regression | ใช้ทุกตัวแปร | **M5 prime** ตัดตัวแปรเอง |
| Logistic Regression | มี regularization (C = 1) | ไม่มี regularization · standardize ให้เอง · มี p-value |
| confusion matrix | แถว = actual | แถว = **pred.**, คอลัมน์ = true |
| positive class | `pos_label=1` | ค่าที่ 2 ของ binominal mapping → ติ๊ก **manually set positive class** ใน Performance |
| K-Means | `n_init="auto"` | max runs 10 |
| Cluster metrics | Davies–Bouldin บวก | **avg within centroid distance / Davies Bouldin แสดงติดลบ** |
| PCA sign | — | เครื่องหมาย loading อาจกลับด้าน (ไม่ผิด) |
| logistic threshold | `predict()` ตัดที่ 0.5 | **H2O ใช้ threshold ที่ F1 สูงสุด** (ไม่ใช่ 0.5) → ใช้ Create/Apply Threshold เอง |

## 6. ประโยคตีความสำเร็จรูป

| ผล | ประโยค |
|---|---|
| เทียบ baseline | *"โมเดลได้ F1 [x] สูงกว่า majority baseline (accuracy [a], F1 0) → เรียนรู้รูปแบบได้จริง"* |
| ก่อน/หลัง | *"[ขั้นตอน] ทำให้ [metric] เปลี่ยนจาก [a] เป็น [b] ([+/−d]) เพราะ [เหตุผล]"* |
| เลือก metric | *"เลือก recall เพราะการพลาด [positive] (FN) เสียหายมากกว่าการเตือนผิด"* |
| threshold | *"ลด threshold 0.5 → 0.3 recall เพิ่ม [a→b] precision ลด [c→d]"* |
| coefficient (LinReg) | *"[x] เพิ่ม 1 หน่วย [y] เปลี่ยน [b] หน่วย โดยตัวแปรอื่นคงที่"* |
| coefficient (LogReg) | *"[x] เพิ่ม 1 หน่วย odds ของ [คลาส] คูณด้วย e^b = [OR]"* |
| tree | *"IF [เงื่อนไข] THEN [คลาส] · feature สำคัญสุดคือ [root]"* |
| overfit | *"train [a] แต่ CV [b] ช่องว่าง [a−b] → overfitting → จำกัด depth / เพิ่ม min leaf"* |
| PCA | *"PC1+PC2 อธิบายได้ [x]% · PC1 ขับเคลื่อนโดย [ตัวแปร loading สูง]"* |
| cluster | *"กลุ่ม [n] มี [ตัวแปร] สูง/ต่ำกว่าค่าเฉลี่ย → [ชื่อกลุ่ม/ความหมาย]"* |
| rule | *"[X] → [Y]: [s]% ของทุก transaction มีทั้งคู่ · คนซื้อ X [c]% ซื้อ Y · lift [l] → สัมพันธ์จริง"* |

---

**กลับหน้าหลัก →** [[LAB 00 START HERE]]
