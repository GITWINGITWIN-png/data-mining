---
title: LAB 03 · Preprocessing Recipes
exam: Lab — จ. 12 ต.ค. 2569 09:00–12:00
guideline: "Lab › Data Preprocessing (ทั้ง 7 ข้อ)"
tags: [final, lab, preprocessing, smote, pca, leakage, rapidminer]
---

# LAB 03 · Preprocessing Recipes
### Missing · Encoding · Scaling · Discretization · Sampling/SMOTE · PCA · Split ไม่ให้ leak

> [!abstract] guideline Lab ข้อ "Data Preprocessing"
> 1. Missing-value handling → [[#3.1 Missing Values ⭐⭐]]
> 2. Encoding categorical attributes → [[#3.2 Encoding Categorical Attributes ⭐⭐⭐]]
> 3. Standardization และ normalization → [[#3.3 Standardization vs Normalization ⭐⭐⭐]]
> 4. Discretization → [[#3.4 Discretization ⭐⭐]]
> 5. Sampling และ SMOTE → [[#3.5 Sampling & SMOTE ⭐⭐⭐]]
> 6. PCA และ 2D visualization → [[#3.6 PCA + 2D Visualization ⭐⭐⭐]]
> 7. **แบ่งข้อมูลอย่างถูกต้องโดยไม่เกิด data leakage** → [[#3.7 Split โดยไม่เกิด Data Leakage ⭐⭐⭐⭐]] ← **ข้อที่ถูกเน้นซ้ำทั้งใน Lab และ Lecture guideline**

**ลิงก์:** [[LAB 00 START HERE|หน้าหลัก Lab]] · ก่อนหน้า [[LAB 02 Data Handling & Visualization]] · ถัดไป [[LAB 04 Workflow, Baseline & Evaluation]] · ทฤษฎี: [[04 Data Pre-processing]] (มิดเทอม)

> [!warning] 🕳️ Gap ของคุณในบทนี้
> - RapidMiner: **ไม่เคยใช้ Discretize, Sample, SMOTE Upsampling, PCA, Numerical to Binominal** · Normalize เคยใช้แค่ Z-transformation (W7)
> - Python: ไม่เคยใช้ `KBinsDiscretizer` · `imblearn` ไม่มีใน env เก่า (HW1/.venv) → **ใช้ `final/.venv`**
> - ตัวอย่าง "ผิด" ในงานเก่าที่ต้องไม่ทำซ้ำ: **W7 เติม missing ด้วยค่าเฉลี่ยของข้อมูลทั้งชุดก่อน split** (ทั้ง Python และ RapidMiner)

> [!important] กฎข้อเดียวที่คุมทั้งบท
> **อะไรก็ตามที่ "เรียนรู้ค่าจากข้อมูล" (mean, std, min/max, mode, bin edges, PCA components, ตัวอย่างสังเคราะห์ของ SMOTE) ต้องเรียนจาก training data เท่านั้น** แล้วค่อย "นำไปใช้" (transform) กับ test / ข้อมูลใหม่
> → ใน Python คือ `fit` บน train · `transform` บน test (หรือยัดทุกอย่างใส่ `Pipeline`)
> → ใน RapidMiner คือวาง operator พวกนี้ไว้ใน **Training pane** ของ `Cross Validation` (หรือฝั่ง training ของ `Split Data`) แล้วส่ง **preprocessing model** ไปใช้กับ test

---

## 3.0 ตั้งต้น

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

adult = pd.read_csv("HW5/adult.csv").replace("?", np.nan)    # adult ใช้ "?" แทนค่าว่าง
churn = pd.read_csv("W14/customer_churn_69_1(in).csv")
churn["TotalCharges"] = pd.to_numeric(churn["TotalCharges"], errors="coerce")
```

---

## 3.1 Missing Values ⭐⭐

### เลือกวิธีให้เหมาะ (ทวน [[04 Data Pre-processing#🎯 Statistical Imputation — หัวใจของ guideline ข้อ 3.2]])

| สถานการณ์ | วิธี | เหตุผลที่ต้องเขียนในคำตอบ |
|---|---|---|
| ค่าว่างน้อยมาก (< ~5%) และสุ่ม | **ตัดแถว** (`dropna`) | เสียข้อมูลน้อย ไม่ทำให้การกระจายเพี้ยน |
| คอลัมน์ว่างเยอะมาก (เช่น Cabin 77%) | **ตัดคอลัมน์** | เติมไปก็เป็นค่าเดาส่วนใหญ่ |
| ตัวเลข การกระจายสมมาตร | **mean** | — |
| ตัวเลข **เบ้ (skewed)** / มี outlier | **median** | mean ถูกหางดึง median ไม่ไหว |
| categorical | **mode** หรือ **ค่าคงที่ "Unknown"** | "Unknown" เก็บข้อมูลว่า "ไม่ตอบ" ไว้ได้ (ใช้ใน HW5) |
| ค่าว่างมีความหมาย (เช่น TotalCharges ว่างเพราะ tenure = 0) | **ค่าคงที่ตามความหมาย** (0) | ไม่ใช่ข้อมูลหาย แต่ "ยังไม่มีค่า" |

```python
print(adult.isna().mean().loc[lambda s: s > 0].round(4))   # workclass/occupation ~5.7% · native-country ~1.8%
print(churn.loc[churn["TotalCharges"].isna(), "tenure"].unique())   # [0] → ว่างเพราะเพิ่งสมัคร
```

### 🐍 Python — แบบถูกต้อง (เรียนค่าจาก train เท่านั้น)

```python
from sklearn.impute import SimpleImputer

X = adult.drop(columns="income")
y = (adult["income"] == ">50K").astype(int)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)       # ① split ก่อนเสมอ

num_cols = ["age", "hours-per-week", "capital-gain"]
cat_cols = ["workclass", "occupation", "native-country"]

num_imp = SimpleImputer(strategy="median").fit(X_train[num_cols])         # ② fit บน train
cat_imp = SimpleImputer(strategy="most_frequent").fit(X_train[cat_cols])

X_train_num = num_imp.transform(X_train[num_cols])                        # ③ transform ทั้งคู่
X_test_num = num_imp.transform(X_test[num_cols])
X_test_cat = cat_imp.transform(X_test[cat_cols])
print(cat_imp.statistics_)        # ค่า mode ที่เรียนได้จาก train: ['Private' 'Prof-specialty' 'United-States']
```

> [!tip] ทางลัดที่ไม่ leak: ใส่ imputer ไว้ใน `Pipeline`/`ColumnTransformer` → ดู [[#3.7 Split โดยไม่เกิด Data Leakage ⭐⭐⭐⭐]]
> ส่วน `df.fillna(df.mean())` **ก่อน split** = ใช้ค่าเฉลี่ยที่รวม test ไปด้วย = leakage (ผิดแบบเดียวกับ W7 และสไลด์ KNN p.56)

### ⚙️ RapidMiner — `Replace Missing Values`

| พารามิเตอร์ | ค่า |
|---|---|
| attribute filter type | `all` หรือ `subset` (เลือกคอลัมน์) |
| **default** | `average` · `minimum` · `maximum` · `zero` · `value` (ใส่ค่าคงที่ใน **replenishment value**) · `none` |
| **columns → Edit List** | ตั้งวิธีเฉพาะรายคอลัมน์ เช่น `TotalCharges` = `zero`, `occupation` = `value` |
| return preprocessing model | ✅ ถ้าจะเอาค่าที่เรียนได้ไปใช้กับ test (port **pre** → `Apply Model`) |

> RapidMiner ไม่มี "median" ใน `Replace Missing Values` → ใช้ `average` หรือคำนวณ median เอง (`Aggregate`) แล้วใส่เป็น `value` · ค่าว่างของ nominal ด้วย `average` จะได้ **mode**
> อ่าน "?" เป็นค่าว่าง: ตอน **Read CSV/Import** ตั้ง ✅ *read not matching values as missings* หรือใช้ `Replace` / `Declare Missing Value` (ค่า "?")

---

## 3.2 Encoding Categorical Attributes ⭐⭐⭐

| วิธี | ใช้เมื่อ | ตัวอย่าง |
|---|---|---|
| **One-hot (dummy)** | nominal ไม่มีลำดับ (Contract, PaymentMethod) | `Contract_Two year = 1/0` |
| **One-hot แบบ k−1** (`drop_first`) | linear / logistic regression (กัน multicollinearity — dummy trap) | Toyota: Fuel_Type → Diesel, Petrol (CNG = baseline) |
| **Ordinal** | มีลำดับ (education levels, Low<Med<High) | Low=0, Med=1, High=2 |
| **Label encoding** | **target** ของ classification | Yes=1, No=0 |
| **Binary (true/false) ทุกค่า** | association rules (ต้องเป็น item) | `Glossy_Lips = true` |

> ⚠️ **ห้ามใช้ label/ordinal encoding กับ nominal แล้วส่งเข้า KNN / linear model** — โมเดลจะคิดว่า "Spain (2) > France (0)" และระยะทางมีความหมาย ซึ่งไม่จริง · **tree ไม่ค่อยเดือดร้อน**

### 🐍 Python

```python
# get_dummies — เร็ว เหมาะกับการสำรวจ / ข้อมูลชุดเดียว
small = churn[["Contract", "InternetService", "tenure"]]
pd.get_dummies(small, columns=["Contract", "InternetService"], drop_first=True, dtype=int).head(3)
```

```python
# OneHotEncoder — ใช้ใน Pipeline (จำหมวดจาก train · test เจอหมวดใหม่ก็ไม่พัง)
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
ohe.fit(churn[["Contract"]])
print(ohe.get_feature_names_out())          # ['Contract_Month-to-month' 'Contract_One year' 'Contract_Two year']

edu_order = [["Preschool", "1st-4th", "5th-6th", "7th-8th", "9th", "10th", "11th", "12th",
              "HS-grad", "Some-college", "Assoc-voc", "Assoc-acdm", "Bachelors", "Masters",
              "Prof-school", "Doctorate"]]
ord_enc = OrdinalEncoder(categories=edu_order)                 # ระบุลำดับเอง ไม่งั้นเรียงตามตัวอักษร
edu_num = ord_enc.fit_transform(adult[["education"]]).ravel() + 1
print((edu_num == adult["educational-num"]).all())             # True → educational-num คือ education ที่ encode แล้ว
```

> [!tip] ⭐ ใช้ประโยคนี้ตอบเรื่อง feature ซ้ำซ้อน
> *"`education` กับ `educational-num` เป็นข้อมูลเดียวกัน (ordinal encode ตรงกัน 100%) → เก็บไว้ตัวเดียว ไม่งั้นเป็น redundant feature"*

### ⚙️ RapidMiner

| Operator | ทำอะไร | พารามิเตอร์สำคัญ |
|---|---|---|
| **`Nominal to Numerical`** | nominal → ตัวเลข | **coding type**: `dummy coding` (one-hot) · `effect coding` · `unique integers` (label encoding) · ✅ **use comparison groups** = one-hot แบบ k−1 (เลือก baseline) |
| **`Nominal to Binominal`** | ทุกค่า → คอลัมน์ true/false | ใช้ก่อน FP-Growth กับข้อมูล nominal |
| **`Numerical to Binominal`** | ตัวเลข → true/false | **min/max**: ค่าในช่วง [min, max] = `false` นอกช่วง = `true` → 0/1 ใช้ min = max = 0 |
| **`Numerical to Polynominal`** | ตัวเลขที่จริง ๆ เป็นรหัส (เช่น Education 1/2/3) → nominal | — |
| **`Map`** | แทนค่าเอง (เช่น "Y"→"Yes") | value mappings |

---

## 3.3 Standardization vs Normalization ⭐⭐⭐

| | **Standardization (z-score)** | **Normalization (min-max)** |
|---|---|---|
| สูตร | $z = \dfrac{x-\mu}{\sigma}$ | $x' = \dfrac{x-\min}{\max-\min}$ |
| ช่วงผล | ค่าเฉลี่ย 0, sd 1 (ไม่จำกัดช่วง) | **[0, 1]** |
| ต่อ outlier | ทนกว่า | **ไวมาก** (outlier ตัวเดียวบีบข้อมูลที่เหลือให้เบียดกัน) |
| sklearn | `StandardScaler` | `MinMaxScaler` |
| RapidMiner `Normalize` → method | **`Z-transformation`** | **`range transformation`** (min 0, max 1) |

> [!important] ต้อง scale เมื่อไหร่
> **ต้อง:** อะไรที่ใช้ **ระยะทาง** หรือ **ขนาดของค่า** — **KNN, K-Means, PCA, SMOTE** (หาเพื่อนบ้าน), logistic/linear ที่มี regularization
> **ไม่ต้อง:** **Decision Tree / Random Forest** (แบ่งทีละ feature ด้วย threshold — สไลด์ Tree p.70: *"no need for feature scaling"*) · Linear Regression ธรรมดา (ผลทำนายเท่าเดิม แค่ coefficient เปลี่ยนหน่วย)
> ภาพพิสูจน์ว่า scaling เปลี่ยนคำตอบ KNN ได้จริง: [[04 Data Pre-processing#4.7 Feature Scaling ⭐⭐ (guideline ข้อ 3.7 — สูตรออกแน่)]]

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

cols = ["tenure", "MonthlyCharges"]
tr, te = train_test_split(churn[cols], test_size=0.2, random_state=42)

std = StandardScaler().fit(tr)            # เรียน mean/std จาก train
mm = MinMaxScaler().fit(tr)               # เรียน min/max จาก train
print(std.mean_.round(2), std.scale_.round(2))
te_std = std.transform(te)                # ใช้ค่าจาก train กับ test
print(te_std.mean(axis=0).round(3))       # ไม่เป็น 0 เป๊ะ — ถูกต้องแล้ว (test ไม่ได้ถูกใช้คิด mean)

# ข้อมูลใหม่ 1 แถว → ใช้ scaler ตัวเดิม (เหมือน W11 ที่ทำนายจุดใหม่)
new_customer = pd.DataFrame({"tenure": [5], "MonthlyCharges": [95.0]})
print(std.transform(new_customer).round(3))
```

> [!warning] ⚠️ ทำไมผล z-score ของ RapidMiner ต่างจาก Python นิดหน่อย
> RapidMiner `Normalize (Z-transformation)` หารด้วย **sample std ($n-1$)** · sklearn `StandardScaler` หารด้วย **population std ($n$)**
> ยืนยันแล้วกับสไลด์ clustering p.30 (Arizona `Fixed_charge` = **−0.293** ตรงกับ $n-1$; ถ้าใช้ $n$ ได้ −0.300) → **ถ้าได้ตัวเลขต่างกันหลักทศนิยมที่ 2–3 ไม่ใช่ความผิด** ให้เขียนอธิบายในรายงานได้เลย

### ⚙️ RapidMiner — `Normalize`
- **method:** `Z-transformation` · `range transformation` (ตั้ง min/max) · `proportion transformation` · `interquartile range`
- เลือกคอลัมน์ด้วย attribute filter type (ปกติ `all` — label/id ไม่ถูกแตะเพราะเป็น special)
- port **pre** (preprocessing model) → ต่อเข้า `Apply Model` เพื่อ normalize test/ข้อมูลใหม่ **ด้วยค่าจาก train** (แบบ W7 ที่คุณทำถูกแล้ว)

---

## 3.4 Discretization ⭐⭐

**เมื่อไหร่ใช้:** (1) **Association rules** ต้องการ item แบบ categorical → ต้องแปลงอายุ/รายได้เป็นช่วงก่อน (HW8) · (2) ทำให้ตีความง่าย (age group) · (3) ลด noise
ทฤษฎีและการคำนวณมือ: [[04 Data Pre-processing#4.6 Discretization: Numerical → Categorical ⭐⭐ (guideline ข้อ 3.6)]]

| วิธี | ความหมาย | Python | RapidMiner |
|---|---|---|---|
| **Equal width** | ทุกช่วงกว้างเท่ากัน | `pd.cut(x, bins=3)` · `KBinsDiscretizer(strategy="uniform")` | **`Discretize by Binning`** (number of bins) |
| **Equal frequency** | ทุกช่วงมีจำนวนแถวเท่ากัน | `pd.qcut(x, q=3)` · `strategy="quantile"` | **`Discretize by Frequency`** |
| **กำหนดขอบเอง** | ตามความหมาย/โดเมน | `pd.cut(x, bins=[...], labels=[...])` | **`Discretize by User Specification`** (class name + upper limit) |
| **ขนาดช่วงคงที่** | ช่วงละ n แถว | — | `Discretize by Size` |
| **K-means** | ช่วงตามกลุ่มที่ k-means หาเจอ | `strategy="kmeans"` | — |
| **Supervised (entropy)** | ตัดช่วงให้ label แยกกันดีที่สุด | — | `Discretize by Entropy` |

```python
age = adult["age"]
equal_width = pd.cut(age, bins=3)                                   # ช่วงกว้างเท่ากัน
equal_freq = pd.qcut(age, q=3, labels=["YOUNG", "MIDDLE", "SENIOR"])   # จำนวนเท่ากัน
domain = pd.cut(age, bins=[0, 25, 45, 65, 120], labels=["<=25", "26-45", "46-65", "65+"])
print(equal_width.value_counts().sort_index())   # ช่วงสูงอายุแทบว่าง เพราะ age เบ้ขวา
print(equal_freq.value_counts().sort_index())    # ราว ๆ 1/3 เท่ากัน
```

```python
from sklearn.preprocessing import KBinsDiscretizer

kb = KBinsDiscretizer(n_bins=4, encode="ordinal", strategy="quantile")
kb.fit(adult[["hours-per-week"]])                 # เรียนขอบช่วงจาก train (ในตัวอย่างนี้ใช้ทั้งชุดเพื่อสำรวจ)
print(kb.bin_edges_[0])                           # ขอบช่วงที่ได้ — มีน้อยกว่า 4 ช่วงได้ถ้าค่าซ้ำเยอะ (40 ชม.)
```

> [!warning] กับดัก discretization
> - **ข้อมูลเบ้ + equal width** → บางช่วงแทบไม่มีข้อมูล (HW8: income เบ้ขวา ใช้ equal width ช่วง HIGH จะว่าง → เลือก equal frequency)
> - **ขอบช่วงก็เป็น "ค่าที่เรียนจากข้อมูล"** ถ้าใช้ทำโมเดลทำนาย ต้อง fit บน train เท่านั้น
> - สไลด์ Apriori p.32: discretize ไม่ดีอาจ "useless" — ทุกค่าตกช่วงเดียว (เช่น weight ทั้งหมดอยู่ 60–80)

---

## 3.5 Sampling & SMOTE ⭐⭐⭐

ทฤษฎีเต็ม: [[LEC 04 Imbalanced Classification]]

| เทคนิค | ทำอะไร | ข้อเสีย (สไลด์ Imbalanced p.16) |
|---|---|---|
| **Random Under-Sampling (RUS)** | สุ่มตัดคลาสส่วนมากให้เท่าคลาสส่วนน้อย | ทิ้งข้อมูล → อาจพลาด concept ของคลาสส่วนมาก |
| **Random Over-Sampling (ROS)** | สุ่มซ้ำ (copy) คลาสส่วนน้อย | ข้อมูลซ้ำ → **overfitting** |
| **SMOTE** | **สร้างจุดใหม่บนเส้นระหว่างจุด minority กับเพื่อนบ้าน k ตัว** | ต้องเป็นตัวเลข + ควร scale ก่อน · อาจสร้างจุดในเขตคลาสอื่น |
| **Stratified sampling** | สุ่มโดยรักษาสัดส่วนคลาส | ไม่ได้แก้ imbalance — แค่ไม่ทำให้แย่ลง (ใช้ตอน split / CV) |

> [!important] ⭐⭐⭐ กฎเหล็ก (สไลด์ Imbalanced p.22: *"Do not apply SMOTE before Cross-Validation"*)
> **resample เฉพาะ training data / training fold เท่านั้น** · test/validation ต้องเป็น **ข้อมูลจริงที่สัดส่วนจริง**
> ถ้า SMOTE ก่อน split → จุดสังเคราะห์ที่ "เกือบเหมือน" จุดใน test หลุดไปอยู่ใน train → ผลประเมินดีเกินจริง

### 🐍 Python

```python
from collections import Counter
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

Xc = pd.get_dummies(churn.drop(columns=["customerID", "Churn"]).fillna({"TotalCharges": 0}),
                    drop_first=True, dtype=int)
yc = (churn["Churn"] == "Yes").astype(int)
Xc_tr, Xc_te, yc_tr, yc_te = train_test_split(Xc, yc, test_size=0.2, stratify=yc, random_state=42)
print("train:", Counter(yc_tr))                         # {0: 4139, 1: 1495}

X_rus, y_rus = RandomUnderSampler(random_state=42).fit_resample(Xc_tr, yc_tr)
X_ros, y_ros = RandomOverSampler(random_state=42).fit_resample(Xc_tr, yc_tr)
X_sm, y_sm = SMOTE(k_neighbors=5, random_state=42).fit_resample(
    StandardScaler().fit_transform(Xc_tr), yc_tr)      # SMOTE ใช้ระยะทาง → scale ก่อน
print("RUS:", Counter(y_rus), " ROS:", Counter(y_ros), " SMOTE:", Counter(y_sm))
# test (Xc_te, yc_te) ไม่ถูกแตะเลย ✓
```

```python
# ใช้ใน Cross Validation → ต้องใช้ Pipeline ของ imblearn (ไม่ใช่ของ sklearn) เพื่อให้ SMOTE ทำงานเฉพาะ training fold
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.tree import DecisionTreeClassifier

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
smote_tree = ImbPipeline([("scale", StandardScaler()),
                          ("smote", SMOTE(random_state=42)),
                          ("tree", DecisionTreeClassifier(max_depth=6, random_state=42))])
scores = cross_validate(smote_tree, Xc, yc, cv=cv, scoring=["accuracy", "recall", "f1"])
print({k: v.mean().round(3) for k, v in scores.items() if k.startswith("test_")})
```

> ตัวอย่างเต็มเทียบ E0 (ไม่ sample) / E1 (RUS) / E2 (SMOTE) อยู่ในงานของคุณ: `W14/6710503739_Imbalanced_InClass.ipynb` (E2 ชนะด้วย F1 0.585)

### ⚙️ RapidMiner

| Operator | ใช้ทำ | พารามิเตอร์ |
|---|---|---|
| **`Sample`** | สุ่มตัด / **balance** | sample = `absolute`/`relative` · ✅ **balance data** → **sample size per class** (เช่น No = 1500, Yes = 1500) = RUS |
| **`Sample (Stratified)`** | สุ่มรักษาสัดส่วน label | sample size / ratio |
| **`Sample (Bootstrapping)`** | สุ่มแบบใส่คืน (ซ้ำได้) | ใช้ทำ ROS เองได้ |
| **`SMOTE Upsampling`** *(Operator Toolbox)* | SMOTE | **number of neighbours** = 5 · **normalize** ✅ · **equalize classes** ✅ · **auto detect minority class** ✅ · nominal change rate 0.5 · local random seed |

> [!warning] ⚙️ วางให้ถูกที่ — ใน **Training pane** ของ `Cross Validation`
> ```
> Cross Validation
> ├─ Training:  [training set] → SMOTE Upsampling → Decision Tree → [model]
> └─ Testing:   [model] + [test set] → Apply Model → Performance → [performance]
> ```
> สไลด์ Imbalanced p.20 วาง SMOTE **ก่อน** Cross Validation — เป็นตัวอย่างที่ **ขัดกับกฎ p.22** ของสไลด์เอง ถ้าโจทย์ถามว่าแบบไหนถูก ตอบตาม p.22
>
> **ไม่มี Operator Toolbox?** (เครื่องคุณติดตั้งแล้ว ✅ — ทางสำรองนี้ไว้ใช้ถ้าเครื่องอื่นไม่มี) ทางสำรอง ROS ใน Training pane:
> `Multiply` → ทางที่ 1 ส่งต่อตรง · ทางที่ 2 `Filter Examples` (Churn = Yes) → `Sample (Bootstrapping)` (sample ratio ≈ 1.8) → `Append` สองทางเข้าด้วยกัน → learner

---

## 3.6 PCA + 2D Visualization ⭐⭐⭐

ทฤษฎี + การตีความ loadings: [[LEC 03 PCA]]

**2 การใช้งานที่ต้องแยกให้ออก (จาก W13 sheet Part III vs Part IV):**
1. **PCA เพื่อสร้างโมเดล** (ลดมิติก่อน KNN) → ต้องอยู่ **ใน CV / Pipeline** (เรียน component จาก training fold)
2. **PCA เพื่อ visualization** (PC1 vs PC2 ระบายสีตาม label) → ทำกับข้อมูลทั้งชุดได้ เพราะเป็น **descriptive** ไม่ได้ใช้วัดผลโมเดล — *"This visualization is for interpretation; it is not an unbiased performance estimate"* (W13 Part IV)

```python
from sklearn.decomposition import PCA

bank = pd.read_csv("W9/bank_dataset.csv").drop(columns=["ID", "ZIP Code"])
yb = bank.pop("Personal Loan")
Zb = StandardScaler().fit_transform(bank)         # ⭐ standardize ก่อน PCA เสมอ (ไม่งั้นตัวที่หน่วยใหญ่ครองหมด)

pca = PCA().fit(Zb)                                # เก็บทุก component ไว้ดู explained variance
evr = pd.DataFrame({"explained": pca.explained_variance_ratio_,
                    "cumulative": pca.explained_variance_ratio_.cumsum()},
                   index=[f"PC{i+1}" for i in range(len(bank.columns))]).round(4)
print(evr.head(4))                                 # PC1 0.1862 · PC2 0.1688 · สะสม 0.3550 (ตรงกับ W13)
print("ต้องใช้กี่ PC ถึง 80%:", int((evr["cumulative"] < 0.80).sum() + 1))

loadings = pd.DataFrame(pca.components_[:2].T, index=bank.columns, columns=["PC1", "PC2"]).round(3)
print(loadings.reindex(loadings["PC1"].abs().sort_values(ascending=False).index).head(3))
```

```python
scores = PCA(n_components=2).fit_transform(Zb)
fig, ax = plt.subplots(figsize=(6, 5))
for cls, color in [(0, "#0072B2"), (1, "#D55E00")]:
    m = (yb == cls).to_numpy()
    ax.scatter(scores[m, 0], scores[m, 1], s=8, alpha=0.5, color=color, label=f"Personal Loan = {cls}")
ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
ax.legend()
plt.savefig("/tmp/lab03_pca.png", dpi=100)
```

> [!important] ⭐ ประโยคตีความ PCA สำเร็จรูป
> *"PC1 อธิบายความแปรปรวนได้ **18.6%** PC2 **16.9%** รวม **35.5%** → ภาพ 2 มิตินี้เก็บข้อมูลได้แค่ราวหนึ่งในสาม **ห้ามสรุปว่าคลาสแยกไม่ได้จากภาพนี้อย่างเดียว** · PC1 มี loading สูงที่ **Age, Experience** (ทิศเดียวกัน) → PC1 ≈ 'ความอาวุโส' · ลูกค้าที่รับ Personal Loan กระจุกด้าน [ทิศที่เห็น] ของ PC2 ซึ่งสัมพันธ์กับ Income/CCAvg"*
> **เลือกจำนวน component:** cumulative explained variance ถึงเกณฑ์ (80–90%) หรือดูจุดหักของ scree plot · หรือเลือกด้วย CV ถ้าใช้ทำโมเดล (W13: ได้ 8 components)

### ⚙️ RapidMiner — `Principal Component Analysis`
1. `Normalize` (Z-transformation) **ก่อน** PCA เสมอ (RapidMiner PCA ใช้ covariance matrix → ตัวแปรหน่วยใหญ่ครอง PC1 — สไลด์ PCA p.16–17 และ Wine p.21: Proline ครอง PC1 99.8%)
2. **dimensionality reduction:** `keep variance` (ตั้ง **variance threshold** เช่น 0.95) หรือ `fixed number` (ตั้ง **number of components** = 2 สำหรับ visualization)
3. ผล (Results → PCA model): แท็บ **Eigenvalues** = Proportion of Variance + **Cumulative Variance** · แท็บ **Eigenvectors** = **loadings**
4. ผล ExampleSet มีคอลัมน์ใหม่ `pc_1`, `pc_2`, … → Visualizations → **Scatter**: x = pc_1, y = pc_2, **color = label**
5. ใช้ทำโมเดล: วาง `Normalize` → `PCA` ใน **Training pane** ของ Cross Validation แล้ว `Group Models` ส่ง (normalize model + PCA model + learner) ไป Testing

---

## 3.7 Split โดยไม่เกิด Data Leakage ⭐⭐⭐⭐

> [!quote] นิยาม (สไลด์ KNN p.60)
> **"Data leakage occurs when information from outside the training dataset is used to create the model."**
> ตัวอย่างในสไลด์: *"Normalization is performed using statistics (mean, variance) computed from **the entire dataset before splitting**"*
> **"Always split the dataset into training and test sets first, then apply preprocessing separately."**

### ✅ / ❌ ลำดับที่ถูกและผิด

| ❌ ผิด (leak) | ✅ ถูก |
|---|---|
| `fillna(df.mean())` → split | split → `SimpleImputer.fit(X_train)` |
| `StandardScaler().fit_transform(X)` → split | split → `scaler.fit(X_train)` → `transform(X_test)` |
| `SMOTE().fit_resample(X, y)` → split (สไลด์ Imbalanced p.21) | split → SMOTE เฉพาะ train / ใน `imblearn.Pipeline` |
| PCA ทั้งชุด → CV | PCA ใน Pipeline (W13 Part III) |
| scale test ด้วย mean/std **ของ test เอง** (โค้ด R สไลด์ KNN p.51) | scale test ด้วย **ค่าของ train** |
| เลือก feature ด้วย correlation กับ y จากข้อมูลทั้งชุด → CV | ทำ feature selection ใน Pipeline |
| tune hyperparameter บน test set แล้วรายงานผล test นั้น | tune ด้วย CV บน train · test ใช้ครั้งเดียวตอนท้าย |

### 🐍 Python — แม่แบบที่ใช้ได้ทุกโจทย์ (`ColumnTransformer` + `Pipeline`)

```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import f1_score

data = churn.drop(columns=["customerID"])
X = data.drop(columns="Churn")
y = (data["Churn"] == "Yes").astype(int)
num_cols = X.select_dtypes(include="number").columns.tolist()
cat_cols = X.select_dtypes(exclude="number").columns.tolist()

preprocess = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                      ("scale", StandardScaler())]), num_cols),
    ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                      ("onehot", OneHotEncoder(handle_unknown="ignore"))]), cat_cols),
])
model = Pipeline([("prep", preprocess), ("knn", KNeighborsClassifier(n_neighbors=15))])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
model.fit(X_train, y_train)                       # imputer/scaler/encoder เรียนจาก train เท่านั้น
print("test F1:", round(f1_score(y_test, model.predict(X_test)), 3))

cv_f1 = cross_validate(model, X_train, y_train, cv=cv, scoring="f1")["test_score"]
print("5-fold CV F1 (บน train):", cv_f1.mean().round(3), "±", cv_f1.std().round(3))
```

> **ทำไม Pipeline กัน leak ได้:** `cross_validate` / `GridSearchCV` เรียก `model.fit(training fold)` → ทุกขั้นใน Pipeline ถูก fit ใหม่ในแต่ละ fold และแค่ `transform` validation fold

### ⚙️ RapidMiner — 2 แบบที่ถูก

**แบบ A: Hold-out (`Split Data`)** — แบบที่คุณทำใน W7
```
Retrieve → Set Role → Split Data (0.8 / 0.2, sampling type = stratified sampling, seed)
  partition 1 (train) → Normalize ──exa──→ k-NN ──mod──┐
                           └──pre──┐                   │
  partition 2 (test)  ────────→ Apply Model (pre) → Apply Model (k-NN) → Performance
```

**แบบ B: Cross Validation + `Group Models`** (สไลด์ Tree p.76)
```
Cross Validation
├─ Training:  tra → Normalize ─exa→ k-NN ─mod→ Group Models (in 1 = Normalize pre, in 2 = k-NN mod) → mod
└─ Testing:   mod + tes → Apply Model → Performance (Binominal Classification) → per
```
> **Group Models** มัดโมเดล preprocessing + โมเดลทำนายเป็นก้อนเดียว → Apply Model ครั้งเดียวใน Testing ก็ normalize test fold ด้วยค่าจาก training fold อัตโนมัติ (ไฟล์ตัวอย่างที่รันทดสอบแล้ว: `final/mock_lab/recipes/knn_cv_normalize.rmp`)

> [!tip] วิธีตรวจว่า RapidMiner process ไม่ leak
> ไล่ดูว่ามี operator ที่ "เรียนจากข้อมูล" (Normalize, Replace Missing Values, PCA, SMOTE, Sample, Discretize, Select by Weights) วาง **นอก** Training pane / ก่อน Split Data หรือเปล่า — ถ้ามี = leak (ยกเว้นการ clean ที่ไม่เรียนค่า เช่น ตัด ID, แปลงชนิด, Filter แถวผิดรูปแบบ)

---

## 🏋️ Drills (closed-book)

> [!question]- D1. โค้ดนี้ผิดตรงไหน แก้อย่างไร (มาจากสไลด์ Imbalanced p.21)
> `X_res, y_res = SMOTE().fit_resample(X, y)` → `train_test_split(X_res, y_res)` → `model.fit(X_train)` → `model.score(X_test)`
> **ผิด:** SMOTE ก่อน split → test มีจุดสังเคราะห์ที่สร้างจาก (และเกือบซ้ำกับ) จุดใน train + test ไม่ได้มีสัดส่วนคลาสจริง → score สูงเกินจริง
> **แก้:** split (stratify) ก่อน → SMOTE เฉพาะ train · หรือ `imblearn.Pipeline([("smote", SMOTE()), ("clf", ...)])` + `cross_validate`

> [!question]- D2. ข้อมูลรายได้เบ้ขวามาก มีค่าว่าง 3% ต้องใช้กับ KNN ควร impute และ scale ด้วยอะไร เพราะอะไร
> **median** (ทนต่อหางยาว/outlier) และ **StandardScaler** (หรือ RobustScaler) — min-max จะถูก outlier บีบให้ค่าส่วนใหญ่ไปกองใกล้ 0 · ทั้งสองขั้น fit บน train เท่านั้น

> [!question]- D3. (RapidMiner) จงเรียง operator สำหรับ: ข้อมูลมี Gender (Male/Female), Education (1/2/3 เป็นรหัส), label = 0/1 → KNN ใน 5-fold CV ที่ไม่ leak
> `Read CSV` → `Numerical to Binominal` (label, min=max=0) → `Numerical to Polynominal` (Education) → `Set Role` (label) → `Nominal to Numerical` (dummy coding: Gender, Education) → `Cross Validation` [Training: `Normalize` (Z) → `k-NN` → `Group Models` · Testing: `Apply Model` → `Performance (Binominal Classification)`]
> หมายเหตุ: Nominal to Numerical นอก CV ไม่ leak เพราะไม่ได้เรียน "ค่าสถิติ" (แค่ดูว่ามีหมวดอะไร)

> [!question]- D4. PCA ให้ explained variance ratio = [0.41, 0.22, 0.15, 0.09, 0.07, 0.06] ต้องใช้กี่ component เพื่อเก็บความแปรปรวน ≥ 80%
> สะสม: 0.41 → 0.63 → 0.78 → **0.87** → ต้องใช้ **4 components** (3 ตัวได้แค่ 78%)

> [!question]- D5. ทำไม Decision Tree ไม่ต้อง scale แต่ KNN ต้อง
> Tree แบ่งข้อมูลทีละ feature ด้วย threshold (เช่น Age < 30) การคูณ/บวกค่าคงที่ไม่เปลี่ยนลำดับ → split เดิม · KNN ใช้ระยะทางรวมทุก feature → feature ที่หน่วยใหญ่ (Salary หลักหมื่น) กลบ feature หน่วยเล็ก (Age หลักสิบ)

---

**ถัดไป →** [[LAB 04 Workflow, Baseline & Evaluation]] · **กลับหน้าหลัก →** [[LAB 00 START HERE]]
