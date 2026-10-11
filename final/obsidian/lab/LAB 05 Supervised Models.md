---
title: LAB 05 · Supervised Models (KNN · LinReg · LogReg · Tree · RF)
exam: Lab — จ. 12 ต.ค. 2569 09:00–12:00
guideline: "Lab › Model Construction and Evaluation ข้อ 5 (K-NN, Linear Regression, Logistic Regression, Decision Tree)"
tags: [final, lab, knn, linear-regression, logistic-regression, decision-tree, random-forest, rapidminer]
---

# LAB 05 · Supervised Models
### KNN · Linear Regression · Logistic Regression · Decision Tree · Random Forest

> [!abstract] guideline Lab: *"สร้างโมเดลสำหรับ K-NN, Linear Regression, Logistic Regression, Decision Tree, Clustering และ Association Rules"*
> บทนี้ = 4 ตัวแรก + **Random Forest** (อยู่ใน Lecture guideline ข้อ 4 และอยู่ในสไลด์ Tree p.72) · Clustering และ Association → [[LAB 06 Clustering & Association]]
> ทุก recipe ใช้ **folds / split เดียวกัน** และ helper `evaluate()` จาก [[LAB 04 Workflow, Baseline & Evaluation#4.6 ตารางเทียบก่อน–หลัง ⭐⭐⭐]]

**ลิงก์:** [[LAB 00 START HERE|หน้าหลัก Lab]] · ก่อนหน้า [[LAB 04 Workflow, Baseline & Evaluation]] · ถัดไป [[LAB 06 Clustering & Association]] · ทฤษฎี: [[LEC 06 KNN]] · [[LEC 07 Linear & Logistic Regression]] · [[LEC 08 Decision Trees & Random Forest]]

> [!warning] 🕳️ Gap ของคุณในบทนี้ (ตัวหนา = ไม่เคยทำเลย)
> - **Random Forest** — ไม่เคยใช้ทั้ง Python และ RapidMiner
> - **Logistic Regression + `predict_proba` + threshold เอง + ตีความ coefficient/odds** — เคยแค่ `predict()` (HW7) · RapidMiner ไม่เคย
> - **`KNeighborsRegressor`** · RapidMiner: Linear Regression, Logistic Regression, Decision Tree, Random Forest **ไม่เคยสร้าง**

## สรุป 5 โมเดลในหน้าเดียว

| | **KNN** | **Linear Reg.** | **Logistic Reg.** | **Decision Tree** | **Random Forest** |
|---|---|---|---|---|---|
| งาน | class + **reg** | **reg** | **class** (binary) | class + reg | class + reg |
| ต้อง scale? | **✅ ต้อง** | ไม่จำเป็น (ช่วยตีความ coef เทียบกัน) | ✅ ควร (regularization) | ❌ | ❌ |
| hyperparameter หลัก | `n_neighbors` (k), `weights`, `metric` | — | `C`, threshold | `criterion`, `max_depth`, `min_samples_leaf` | `n_estimators`, `max_features`, `max_depth`, `min_samples_leaf` |
| ตีความ | เพื่อนบ้าน k ตัว | **coefficient** | **coefficient → odds** | **กฎ IF-THEN** | **feature importance** |
| sklearn | `KNeighborsClassifier/Regressor` | `LinearRegression` | `LogisticRegression` | `DecisionTreeClassifier` | `RandomForestClassifier` |
| RapidMiner | `k-NN` | `Linear Regression` | `Logistic Regression` | `Decision Tree` | `Random Forest` |

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, KFold, cross_validate, cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (confusion_matrix, accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, root_mean_squared_error, r2_score, mean_absolute_error)

ads = pd.read_csv("W12/Social_Network_Ads_2.csv")
ads["Gender"] = (ads["Gender"] == "Male").astype(int)
X = ads[["Gender", "Age", "EstimatedSalary"]]
y = ads["Purchased"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

new_customer = pd.read_csv("W12/new_customer.csv")                     # Female, 40, 100000
new_customer["Gender"] = (new_customer["Gender"] == "Male").astype(int)
new_X = new_customer[X.columns]                                         # คอลัมน์ต้องเรียงเหมือนตอน train
```

---

## 5.1 K-Nearest Neighbors ⭐⭐⭐

**แนวคิด (สไลด์ KNN p.26):** (1) กำหนด k (2) คำนวณระยะทางจากจุดใหม่ไปทุกจุดใน training (3) เลือก k ตัวที่ใกล้สุด (4) **classification = เสียงข้างมาก · regression = ค่าเฉลี่ย** ของเพื่อนบ้าน → ไม่มีการ "เรียน" โมเดลจริง (**lazy learner**) · ทฤษฎี + คำนวณมือ: [[LEC 06 KNN]]

### 🐍 Classification + ดูว่าเพื่อนบ้านเป็นใคร

```python
from sklearn.neighbors import KNeighborsClassifier

knn = Pipeline([("scale", StandardScaler()),
                ("knn", KNeighborsClassifier(n_neighbors=5, metric="minkowski", p=2))])  # p=2 → Euclidean
knn.fit(X_train, y_train)
print("test accuracy:", round(knn.score(X_test, y_test), 4))
print("new customer →", knn.predict(new_X), knn.predict_proba(new_X).round(2))  # proba = สัดส่วนโหวตใน 5 ตัว

# เพื่อนบ้าน 5 ตัวของลูกค้าใหม่ (ระยะทางคิดใน space ที่ scale แล้ว)
dist, idx = knn["knn"].kneighbors(knn["scale"].transform(new_X))
neighbours = X_train.iloc[idx[0]].assign(Purchased=y_train.iloc[idx[0]].values, distance=dist[0].round(3))
print(neighbours)
```

### 🐍 Regression (KNN ทำนายตัวเลข) + ผลของ scaling

```python
from sklearn.neighbors import KNeighborsRegressor

boston = pd.read_csv("W8/boston_r.csv")
Xb, yb = boston.drop(columns="medv"), boston["medv"]
kcv = KFold(n_splits=5, shuffle=True, random_state=42)               # regression → KFold (ไม่มี stratify)

for k in [3, 5, 7, 10]:
    raw = -cross_val_score(KNeighborsRegressor(n_neighbors=k), Xb, yb, cv=kcv,
                           scoring="neg_root_mean_squared_error").mean()
    scaled = -cross_val_score(Pipeline([("s", StandardScaler()), ("k", KNeighborsRegressor(n_neighbors=k))]),
                              Xb, yb, cv=kcv, scoring="neg_root_mean_squared_error").mean()
    print(f"k={k:>2}  RMSE raw={raw:.3f}  scaled={scaled:.3f}")
```

> [!example] ผลจริง: k = 3 → RMSE **6.103 (ไม่ scale) → 4.348 (scale)** ลดลง 29% · ทุก k ให้ผลแบบเดียวกัน
> sklearn ให้ "neg_…" (ค่าติดลบ) เพราะ `cross_val_score` ถือว่า "ยิ่งมากยิ่งดี" → ใส่ลบหน้าเพื่อกลับเป็น RMSE

### ⚙️ RapidMiner — `k-NN`
| พารามิเตอร์ | ค่า |
|---|---|
| **k** | 5 (หรือ optimize) |
| **weighted vote** | ❌ = โหวตเท่ากัน · ✅ = เพื่อนบ้านใกล้มีน้ำหนักมากกว่า (= `weights="distance"`) |
| **measure types** | `NumericalMeasures` → numerical measure = `EuclideanDistance` · ข้อมูลผสม → `MixedMeasures` |
- label เป็น nominal → classification · label เป็นตัวเลข → **regression อัตโนมัติ** (operator เดียวกัน)
- ต้องมี **`Normalize` ใน Training pane** (ดู [[LAB 03 Preprocessing Recipes#3.7 Split โดยไม่เกิด Data Leakage ⭐⭐⭐⭐]])

---

## 5.2 Linear Regression ⭐⭐⭐

ทฤษฎีเต็ม (OLS, R², assumptions, multicollinearity): [[09 Regression Analysis]] (มิดเทอม) · [[LEC 07 Linear & Logistic Regression]]

```python
from sklearn.linear_model import LinearRegression

Xb_tr, Xb_te, yb_tr, yb_te = train_test_split(Xb, yb, test_size=0.2, random_state=42)

two = ["lstat", "rm"]                                   # 2 ตัวที่ |r| กับ medv สูงสุด (W8)
lin = LinearRegression().fit(Xb_tr[two], yb_tr)
b0, (b1, b2) = lin.intercept_, lin.coef_
print(f"medv = {b0:.4f} + ({b1:.4f})·lstat + ({b2:.4f})·rm")

pred = lin.predict(Xb_te[two])
print("test MAE :", round(mean_absolute_error(yb_te, pred), 4))
print("test RMSE:", round(root_mean_squared_error(yb_te, pred), 4))        # 5.5896 — ตรงกับงาน W8 ของคุณ
print("test R²  :", round(r2_score(yb_te, pred), 4))                       # 0.574

coef_table = pd.Series(lin.coef_, index=two).round(4)
print(coef_table)

# ทำนายบ้านใหม่: lstat = 10%, rm = 6 ห้อง
print(lin.predict(pd.DataFrame({"lstat": [10], "rm": [6]})).round(2))
```

> [!important] ⭐ ประโยคตีความ coefficient (ต้องมีวรรค "ตัวอื่นคงที่")
> *"สมการ **medv = −3.841 − 0.633·lstat + 5.465·rm** · เมื่อสัดส่วนประชากรรายได้ต่ำ (lstat) เพิ่ม 1 จุด % ราคาบ้านเฉลี่ย**ลดลง 0.633 พันดอลลาร์** โดยที่จำนวนห้องคงที่ · ห้องเพิ่ม 1 ห้อง ราคา**เพิ่ม 5.465 พันดอลลาร์** โดยที่ lstat คงที่ · โมเดลอธิบายความแปรปรวนของราคาบน test ได้ **57.4%** (R²) และทายพลาดเฉลี่ย RMSE 5.59 พันดอลลาร์"*
> ⚠️ ถ้า fit บนข้อมูลที่ standardize แล้ว (แบบ W8) coefficient = "เปลี่ยนกี่หน่วยของ y ต่อ **1 SD** ของ x" — ใช้เทียบความสำคัญระหว่างตัวแปรได้ แต่ตีความเป็นหน่วยจริงไม่ได้

### ⚙️ RapidMiner — `Linear Regression`
| พารามิเตอร์ | ค่า | ⚠️ |
|---|---|---|
| **feature selection** | **`none`** | **ค่า default คือ `M5 prime` — RapidMiner จะตัด attribute ทิ้งเองบางตัว** → ผลไม่ตรงกับ sklearn และอาจไม่ตรงกับโจทย์ที่ให้ใช้ตัวแปรครบ |
| eliminate colinear features | ✅ (default) | ตัวแปรที่ collinear จะถูกตัด |
| use bias | ✅ | = มี intercept |
- ผล **LinearRegression model** → ตาราง: Attribute · **Coefficient** · Std. Error · Std. Coefficient · Tolerance · t-Stat · **p-Value** · Code (`****` = มีนัยสำคัญมาก)
- ประเมิน: `Performance (Regression)` → root mean squared error, absolute error, squared correlation

---

## 5.3 Logistic Regression ⭐⭐⭐⭐ (gap ใหญ่)

**แนวคิด:** ทำนาย **ความน่าจะเป็น** ของคลาส positive ด้วย sigmoid ของสมการเชิงเส้น · ทฤษฎี (logit, MLE, odds): [[LEC 07 Linear & Logistic Regression]]
$$p = P(y=1\mid x)=\frac{1}{1+e^{-(b_0+b_1x_1+\dots)}}\qquad \ln\frac{p}{1-p}=b_0+b_1x_1+\dots$$

```python
from sklearn.linear_model import LogisticRegression

logreg = Pipeline([("scale", StandardScaler()),
                   ("lr", LogisticRegression(C=1.0, max_iter=1000))])   # sklearn 1.9: อย่าใส่ penalty= (deprecated)
logreg.fit(X_train, y_train)

coefs = pd.DataFrame({"coef (ต่อ 1 SD)": logreg["lr"].coef_[0],
                      "odds ratio = e^coef": np.exp(logreg["lr"].coef_[0])},
                     index=X.columns).round(3)
print("intercept:", logreg["lr"].intercept_.round(4))
print(coefs)
```

```python
# ① ความน่าจะเป็น → ② ตัดด้วย threshold เอง → ③ เทียบผล
proba = logreg.predict_proba(X_test)[:, 1]        # คอลัมน์ 1 = P(Purchased = 1) (เรียงตาม logreg.classes_)
rows = []
for t in [0.3, 0.5, 0.7]:
    pred_t = (proba >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, pred_t).ravel()
    rows.append({"threshold": t, "TN": tn, "FP": fp, "FN": fn, "TP": tp,
                 "accuracy": accuracy_score(y_test, pred_t), "precision": precision_score(y_test, pred_t),
                 "recall": recall_score(y_test, pred_t), "F1": f1_score(y_test, pred_t)})
print(pd.DataFrame(rows).round(4).to_string(index=False))
print("AUC:", round(roc_auc_score(y_test, proba), 3))      # ไม่ขึ้นกับ threshold

print("new customer P(buy) =", logreg.predict_proba(new_X)[0, 1].round(4))   # 0.5951 → ≥ 0.5 → ซื้อ
```

> [!example] ผลจริง (test 80 แถว)
> | threshold | TN | FP | FN | TP | accuracy | precision | recall | F1 |
> |---|---|---|---|---|---|---|---|---|
> | 0.3 | 37 | 14 | 3 | 26 | 0.7875 | 0.650 | **0.897** | **0.754** |
> | **0.5** (default) | 47 | 4 | 12 | 17 | **0.800** | 0.810 | 0.586 | 0.680 |
> | 0.7 | 49 | 2 | 15 | 14 | 0.7875 | **0.875** | 0.483 | 0.622 |
>
> **ลด threshold → ทายว่า "ซื้อ" ง่ายขึ้น → recall ↑ precision ↓** (FN ลดจาก 12 เหลือ 3 แต่ FP เพิ่มจาก 4 เป็น 14) · ตรงกับตาราง Riding Mowers ในสไลด์ KNN p.72 (cutoff 0.25 / 0.5 / 0.75)

> [!important] ⭐ ตีความ coefficient ของ logistic regression
> - **เครื่องหมาย:** + = เพิ่มโอกาสเป็นคลาส 1 · − = ลด
> - **odds ratio = $e^{b}$:** Age มี coef **2.197 ต่อ 1 SD** → odds ratio **9.0** = *"อายุเพิ่ม 1 SD (~10 ปี) odds ของการซื้อเพิ่มขึ้น 9 เท่า โดยที่ตัวแปรอื่นคงที่"* · EstimatedSalary OR **3.48** · Gender OR 1.13 (แทบไม่มีผล)
> - ถ้าไม่ scale (หน่วยจริง): coef ของ Age = 0.226 ต่อปี → $e^{0.226}$ = **1.25** = *"อายุเพิ่ม 1 ปี odds เพิ่ม 25%"*
> - ⚠️ coefficient **ไม่ใช่** "ความน่าจะเป็นเพิ่ม b" — มันเปลี่ยน **log-odds** ทีละ b
> - **เลือก threshold ตามเป้าหมาย:** หาลูกค้าให้ครบ → threshold ต่ำ (recall) · ไม่อยากรบกวนคนไม่สนใจ → threshold สูง (precision)

### ⚙️ RapidMiner — `Logistic Regression` + `Create Threshold` / `Apply Threshold`
**พารามิเตอร์ (ตามสไลด์ KNN p.23):** solver `AUTO` · reproducible ✅ · use regularization ❌ · **standardize ✅** (ทำให้เองข้างใน) · add intercept ✅ · **compute p-values ✅** · remove collinear columns ✅
- label ต้องเป็น **binominal** · ผล model → ตาราง **Coefficients**: Attribute · Coefficient · Std. Coefficient · Std. Error · z-Value · **p-Value**
- หลัง `Apply Model` ได้คอลัมน์ **`confidence(1)`** / **`confidence(0)`** (= predict_proba) และ `prediction`
- ⚠️ **ทดลองแล้ว (10 ต.ค.): `prediction` ของ Logistic Regression (H2O) ไม่ได้ตัดที่ 0.5** — H2O ใช้ threshold ที่ทำให้ F1 สูงสุดบน train (ดูใน model: `default threshold: 0.314` ในโจทย์ Pima) → ถ้าโจทย์กำหนด threshold (รวมถึง 0.5) ต้องใช้ **Create Threshold + Apply Threshold** เสมอ ([[PR 05 Logistic Regression & Threshold (RapidMiner)]])

**เปลี่ยน threshold (สไลด์ KNN p.69):**
```
… → Apply Model ─lab─→ Apply Threshold ─exa─→ Performance (Binominal Classification)
    Create Threshold ─output─↗ (port "thr")
Create Threshold: threshold = 0.3 · first class = 0 (negative) · second class = 1 (positive)
```
→ แถวที่ confidence(second class) ≥ 0.3 ถูกทายเป็น second class

---

## 5.4 Decision Tree ⭐⭐⭐

ทฤษฎี (Gini/Entropy/Information Gain/Gain Ratio คำนวณมือ, pruning): [[LEC 08 Decision Trees & Random Forest]]

```python
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree

# ① ดู overfitting: ความลึกเพิ่ม → train ↑ เรื่อย ๆ แต่ CV ขึ้นแล้วลง
rows = []
for depth in [1, 2, 3, 4, 6, 8, None]:
    r = cross_validate(DecisionTreeClassifier(max_depth=depth, random_state=42), X, y, cv=cv,
                       return_train_score=True)
    rows.append({"max_depth": depth, "train acc": r["train_score"].mean(), "CV acc": r["test_score"].mean()})
depth_table = pd.DataFrame(rows).round(4)
print(depth_table.to_string(index=False))
```

> [!example] ผลจริง — ภาพของ overfitting (ตรงกับกราฟสไลด์ Tree p.51/p.55)
> | max_depth | 1 | **2** | 3 | 4 | 6 | 8 | None (โตเต็ม) |
> |---|---|---|---|---|---|---|---|
> | train acc | 0.840 | 0.916 | 0.918 | 0.931 | 0.954 | 0.976 | **0.998** |
> | CV acc | 0.833 | **0.908** | 0.898 | 0.873 | 0.863 | 0.860 | **0.848** |
>
> *"tree ที่โตเต็มจำข้อมูล train ได้ 99.8% แต่ทำนายข้อมูลใหม่ได้แค่ 84.8% (ช่องว่าง 15 จุด) = **overfitting** · ความลึก 2 ให้ CV สูงสุด 90.8% → จำกัดความลึก (pre-pruning) ช่วยให้ generalize ดีขึ้น"* (W12 ของคุณก็ได้ depth 2 เหมือนกัน)

```python
# ② tree ที่เลือก + กฎ + ความสำคัญของ feature + ทำนายลูกค้าใหม่
grid = GridSearchCV(DecisionTreeClassifier(random_state=42),
                    {"criterion": ["gini", "entropy"], "max_depth": [2, 3, 4, 5],
                     "min_samples_leaf": [1, 5, 10]}, cv=cv, scoring="accuracy").fit(X, y)
print(grid.best_params_, round(grid.best_score_, 4))     # entropy · depth 2 · CV 0.91 — ตรงกับ W12 ของคุณ

tree = DecisionTreeClassifier(max_depth=3, random_state=42).fit(X, y)
print(export_text(tree, feature_names=list(X.columns)))                 # กฎ IF-THEN
print(pd.Series(tree.feature_importances_, index=X.columns).round(3))   # Age 0.605 · Salary 0.395 · Gender 0
print("new customer:", tree.predict(new_X), tree.predict_proba(new_X).round(4))

plt.figure(figsize=(12, 5))
plot_tree(tree, feature_names=list(X.columns), class_names=["No", "Buy"], filled=True, rounded=True, fontsize=8)
plt.savefig("/tmp/lab05_tree.png", dpi=100)
```

> [!tip] อ่านกฎจาก tree (โจทย์ "อธิบายผล")
> เดินจาก root → leaf: *"IF Age ≤ 42.5 AND EstimatedSalary > 90,500 THEN ซื้อ"* · *"IF Age > 42.5 THEN ซื้อ (เกือบทั้งหมด)"* · feature ที่ split แรก (root) = ตัวที่ลด impurity มากที่สุด (Age) · `predict_proba` ของ tree = **สัดส่วนคลาสใน leaf** ที่ข้อมูลตกลงไป

### ⚙️ RapidMiner — `Decision Tree`
| พารามิเตอร์ | default | หมายเหตุ |
|---|---|---|
| **criterion** | **`gain_ratio`** | อื่น ๆ: `information_gain` · `gini_index` · `accuracy` — ⚠️ sklearn default = gini |
| **maximal depth** | 10 | = `max_depth` |
| **apply pruning** | ✅ (confidence 0.1) | post-pruning |
| **apply prepruning** | ✅ — minimal gain 0.01 · **minimal leaf size 2** · minimal size for split 4 | pre-pruning (= `min_samples_leaf`, `min_samples_split`) |
- ผล **Tree** view (กราฟ) + **Description** (กฎเป็นข้อความ) · ความกว้างของเส้น = จำนวนแถว
- label ต้องเป็น nominal/binominal (ถ้า 0/1 → Numerical to Binominal)

---

## 5.5 Random Forest ⭐⭐⭐ (gap เต็ม)

**แนวคิด (สไลด์ Tree p.72):** *"Uses multiple (ensemble) classification models… Pick a random subset S of training samples. For each subset → grow a full tree… use **majority vote**"*
📚 นอกสไลด์ (scikit-learn User Guide §1.11, Breiman 2001): แต่ละต้นใช้ **bootstrap sample** (สุ่มแถวแบบใส่คืน) **และ** แต่ละ split สุ่ม **feature เพียงบางส่วน** (`max_features="sqrt"`) → ต้นไม้ไม่เหมือนกัน → ค่าเฉลี่ยของหลายต้นลด variance (overfit น้อยกว่า tree เดี่ยวที่โตเต็ม)

```python
from sklearn.ensemble import RandomForestClassifier

models = {
    "Tree (โตเต็ม)": DecisionTreeClassifier(random_state=42),
    "Tree max_depth=3": DecisionTreeClassifier(max_depth=3, random_state=42),
    "RF default (100 ต้น)": RandomForestClassifier(random_state=42),
    "RF min_samples_leaf=5": RandomForestClassifier(min_samples_leaf=5, random_state=42),
}
rows = []
for name, m in models.items():
    r = cross_validate(m, X, y, cv=cv, scoring=["accuracy", "f1"])
    rows.append({"model": name, "CV accuracy": r["test_accuracy"].mean(), "CV F1": r["test_f1"].mean()})
print(pd.DataFrame(rows).round(4).to_string(index=False))

rf = RandomForestClassifier(n_estimators=100, max_features="sqrt", oob_score=True, random_state=42).fit(X, y)
print("OOB accuracy:", round(rf.oob_score_, 4))         # ประเมินด้วยแถวที่ "ไม่ถูกสุ่ม" เข้าแต่ละต้น — ได้ฟรีไม่ต้อง CV
print(pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False).round(3))
```

> [!example] ผลจริง
> | model | CV accuracy | CV F1 |
> |---|---|---|
> | Tree (โตเต็ม) | 0.8475 | 0.7829 |
> | Tree max_depth=3 | 0.8975 | 0.8613 |
> | RF default (100 ต้น) | 0.8950 | 0.8542 |
> | **RF min_samples_leaf=5** | **0.9075** | **0.8762** |
>
> *"RF ดีกว่า tree ที่โตเต็มชัดเจน (+4.8 จุด accuracy) เพราะการโหวตของ 100 ต้นลด overfitting · เมื่อจำกัด leaf ≥ 5 ได้ดีที่สุด 90.75% · feature importance: Age 0.52, EstimatedSalary 0.47, Gender 0.01 → Gender แทบไม่ช่วยทำนาย"*
> ⚠️ ข้อเสีย RF (สไลด์ p.72): **ตีความยาก** (ไม่มีกฎเดียวให้อ่าน) · ต้องเลือกจำนวนต้น · ยัง overfit ได้ถ้าต้นลึกเกินและข้อมูลน้อย

| hyperparameter | sklearn | RapidMiner | ผล |
|---|---|---|---|
| จำนวนต้น | `n_estimators` (100) | **number of trees** (100) | มากขึ้น = เสถียรขึ้น ช้าลง (ไม่ overfit เพิ่ม) |
| feature ต่อ split | `max_features` (`"sqrt"`) | **guess subset ratio** ✅ (หรือ subset ratio) | น้อย = ต้นต่างกันมาก |
| ความลึก | `max_depth` (None) | **maximal depth** (10) | ลึก = overfit มากขึ้นต่อต้น |
| ขนาด leaf | `min_samples_leaf` (1) | apply prepruning → minimal leaf size | ใหญ่ = เรียบขึ้น |
| criterion | `criterion` (gini) | **criterion** (gain_ratio) | — |
| การรวมผล | majority / ค่าเฉลี่ย proba | **voting strategy**: `confidence vote` / `majority vote` | — |

### ⚙️ RapidMiner — `Random Forest`
- ผลมี **Random Forest Model** (ดูทีละต้น) · ความสำคัญของ feature: operator **`Weight by Forest`** (สร้าง forest จากข้อมูลแล้วให้ weight ต่อ attribute — อยู่ใน core) · `Weight by Tree Importance` มีเฉพาะเมื่อติดตั้ง extension เพิ่ม (ในเครื่องคุณตอนนี้ไม่มี)
- ประเมินใน `Cross Validation` เหมือน learner อื่น · RF **ไม่ต้อง Normalize**

---

## 🏋️ Drills (closed-book)

> [!question]- D1. (Python) จาก `W9/bank_dataset.csv` (target = Personal Loan, ตัด ID/ZIP) สร้าง LogisticRegression ใน Pipeline กับ StandardScaler แล้วหา recall ที่ threshold 0.5 และ 0.2 ด้วย 5-fold CV
> ```python
> from sklearn.model_selection import cross_val_predict
> bank = pd.read_csv("W9/bank_dataset.csv").drop(columns=["ID", "ZIP Code"])
> yl = bank.pop("Personal Loan")
> lr_bank = Pipeline([("s", StandardScaler()), ("lr", LogisticRegression(max_iter=1000))])
> cv5 = StratifiedKFold(5, shuffle=True, random_state=42)
> p = cross_val_predict(lr_bank, bank, yl, cv=cv5, method="predict_proba")[:, 1]
> for t in (0.5, 0.2):
>     print(t, "recall =", round(recall_score(yl, (p >= t).astype(int)), 3),
>           "precision =", round(precision_score(yl, (p >= t).astype(int)), 3))
> # ผลจริง: 0.5 → recall 0.633 / precision 0.813 · 0.2 → recall 0.808 / precision 0.592
> # threshold ต่ำลง → หาลูกค้าที่จะรับสินเชื่อเจอเพิ่มจาก 63% เป็น 81% แลกกับ precision ที่ลดลง
> ```

> [!question]- D2. coefficient ของ Income (หน่วยพันดอลลาร์ ไม่ scale) ใน logistic regression = 0.05 ตีความอย่างไร
> $e^{0.05} = 1.051$ → *"รายได้เพิ่ม 1,000 ดอลลาร์ odds ที่จะรับสินเชื่อเพิ่ม **5.1%** โดยที่ตัวแปรอื่นคงที่"* · รายได้เพิ่ม 10,000 → $e^{0.5}$ = 1.65 เท่า

> [!question]- D3. tree ได้ train accuracy 1.00 แต่ CV 0.82 ส่วน RF ได้ train 1.00 CV 0.90 จงอธิบายและเสนอวิธีปรับ tree
> tree เดี่ยว **overfit** (จำ train ได้หมดแต่ generalize ไม่ดี) · RF ก็ fit train ได้หมดเหมือนกันแต่การโหวตหลายต้นที่ต่างกันลด variance → CV ดีกว่า · ปรับ tree: **จำกัด max_depth / เพิ่ม min_samples_leaf (pre-pruning)** หรือ prune หลังโต แล้วเลือกค่าด้วย CV

> [!question]- D4. (RapidMiner) Linear Regression ใน RapidMiner ให้ coefficient แค่ 3 ตัว ทั้งที่ใส่ไป 5 ตัว และ sklearn ให้ครบ 5 ตัว เพราะอะไร
> **feature selection = M5 prime (default)** ตัด attribute ที่ไม่ช่วยออกให้เอง (และ eliminate colinear features ✅) → ตั้ง feature selection = **none** ถ้าต้องการให้ตรงกับ sklearn

> [!question]- D5. KNN regression k = 3 ทายราคาบ้านใหม่ เพื่อนบ้าน 3 หลังราคา 21, 24, 30 (พันดอลลาร์) ทายได้เท่าไร
> ค่าเฉลี่ย = (21 + 24 + 30)/3 = **25.0** (สไลด์ KNN p.44: *"use average of response values"*) · ถ้า weighted vote จะถ่วงด้วย 1/distance

---

**ถัดไป →** [[LAB 06 Clustering & Association]] · **กลับหน้าหลัก →** [[LAB 00 START HERE]]
