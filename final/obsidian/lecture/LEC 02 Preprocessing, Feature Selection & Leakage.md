---
title: LEC 02 · Preprocessing, Feature Selection & Leakage
exam: Lecture — จ. 19 ต.ค. 2569 16:00–19:00
guideline: "Lecture ข้อ 2 — Missing values และ outliers · Standardization และ normalization · Encoding และ discretization · Feature selection · การหลีกเลี่ยง data leakage"
source: midterm Pre_processing_69_1.pdf (105 pp) → โน้ตมิดเทอม 04 · 69_1_Kitsana_KNN.pdf p.52–60 · 69_1_Tree.pdf p.46
tags: [final, lecture, preprocessing, missing-values, scaling, encoding, feature-selection, data-leakage]
---

# LEC 02 · Preprocessing, Feature Selection & Leakage
### เตรียมข้อมูลให้ถูก — และทำโดยไม่ "แอบดู" test set

> [!abstract] guideline ข้อ 2 (5 หัวข้อแรก — PCA และ imbalanced แยกไป [[LEC 03 PCA]] · [[LEC 04 Imbalanced Classification]])
> 1. Missing values และ outliers → [[#2.1 Missing Values ⭐⭐⭐]] · [[#2.2 Outliers ⭐⭐]]
> 2. Standardization และ normalization → [[#2.3 Standardization vs Normalization ⭐⭐⭐]]
> 3. Encoding และ discretization → [[#2.4 Encoding ⭐⭐⭐]] · [[#2.5 Discretization ⭐⭐]]
> 4. Feature selection → [[#2.6 Feature Selection ⭐⭐⭐]]
> 5. **การหลีกเลี่ยง data leakage** → [[#2.7 Data Leakage ⭐⭐⭐⭐]]

**ลิงก์:** [[LEC 00 START HERE|หน้าหลัก Lecture]] · เต็ม: [[04 Data Pre-processing]] (มิดเทอม) · Lab: [[LAB 03 Preprocessing Recipes]] · ถัดไป [[LEC 03 PCA]]

---

## 2.1 Missing Values ⭐⭐⭐

เต็ม: [[04 Data Pre-processing#4.2 Missing Values ⭐⭐ (guideline ข้อ 3.1 + 3.2)]]

| วิธี | ใช้เมื่อ | ข้อเสีย |
|---|---|---|
| **ลบแถว** (listwise) | missing น้อยและสุ่ม | เสียข้อมูล · bias ถ้า missing ไม่สุ่ม |
| **ลบคอลัมน์** | missing มากเกิน (เช่น > 50–70%) | เสียตัวแปร |
| **mean** | numeric สมมาตร | ไวต่อ outlier · ลด variance |
| **median** | numeric **เบ้/มี outlier** | — |
| **mode** | **categorical** | อาจเพิ่มน้ำหนักหมวดที่พบบ่อย |
| **ค่าคงที่ / "Unknown"** | missing มีความหมาย (ไม่ตอบ, ยังไม่มีค่า) | — |
| **model-based** (KNN imputer, regression) | ตัวแปรสัมพันธ์กัน | ซับซ้อน · ต้อง fit ใน train |
> ⚠️ ค่าว่าง "แฝง" ต้องหาก่อน: `?` (adult), ช่องว่าง (churn TotalCharges), `-1` (cereals), 0 ที่เป็นไปไม่ได้
> ⚠️ ค่าที่ใช้เติม (mean/median/mode) **ต้องคำนวณจาก training set** → [[#2.7 Data Leakage ⭐⭐⭐⭐]]

## 2.2 Outliers ⭐⭐

เต็ม: [[04 Data Pre-processing#4.3 Noise vs. Outliers ⭐⭐ (guideline ข้อ 3.3 — ระบุชื่อคู่นี้ตรง ๆ)]]
- **ตรวจ:** IQR rule ($Q_1-1.5IQR$, $Q_3+1.5IQR$) · z-score (|z| > 3) · boxplot · scatter
- **outlier ≠ error เสมอไป** — อาจเป็นค่าจริงที่หายาก (fraud!) → ต้องตัดสินด้วยโดเมน: แก้ (ถ้าผิด) · ตัด · **cap/winsorize** · transform (log) · ใช้วิธีที่ทน (median, tree)
- **ผลกระทบ:** mean, SD, min-max scaling, linear regression, **K-Means** (centroid = mean) ไวต่อ outlier · tree, median, IQR ทน

## 2.3 Standardization vs Normalization ⭐⭐⭐

เต็ม: [[04 Data Pre-processing#4.7 Feature Scaling ⭐⭐ (guideline ข้อ 3.7 — สูตรออกแน่)]]

| | **Standardization (z-score)** | **Normalization (min-max)** |
|---|---|---|
| สูตร | $z=\dfrac{x-\mu}{\sigma}$ | $x'=\dfrac{x-\min}{\max-\min}$ |
| ผล | mean 0 · SD 1 | ช่วง [0, 1] |
| outlier | ทนกว่า (KNN p.59: *"less influenced by outliers"*) | ไว (*"can be influenced by outliers"*) |
| เหมาะ | ค่อนข้าง normal · PCA · regularized models | ต้องการช่วงจำกัด · ข้อมูลไม่มี outlier |

> [!important] ต้อง scale เมื่อไหร่
> **ต้อง:** วิธีที่ใช้ระยะทาง/ขนาด — **KNN** (KNN p.45) · **K-Means** · **PCA** · **SMOTE** · logistic/linear ที่มี regularization
> **ไม่ต้อง:** **Decision Tree / Random Forest** (Tree p.70 *"no need for feature scaling"*)
> 📌 scaler **fit บน train** แล้ว transform test และข้อมูลใหม่ด้วยค่าเดิม (KNN p.58: `sc.fit_transform(X_train)` → `sc.transform(X_test)`)

> [!example]- 🧮 Drill: x = [10, 20, 30, 40, 100]
> min-max: (x − 10)/90 → **0, 0.111, 0.222, 0.333, 1** (ค่าส่วนใหญ่ถูกบีบใกล้ 0 เพราะ outlier 100)
> z-score: μ = 40, σ (population) = √[(900 + 400 + 100 + 0 + 3600)/5] = √1000 = 31.62 → **−0.95, −0.63, −0.32, 0, 1.90**

## 2.4 Encoding ⭐⭐⭐

เต็ม: [[04 Data Pre-processing#4.5 Encoding: Categorical → Numerical ⭐⭐ (guideline ข้อ 3.5)]]

| วิธี | ใช้กับ | หมายเหตุ |
|---|---|---|
| **One-hot / dummy** | nominal (ไม่มีลำดับ) | k คอลัมน์ · regression ใช้ **k−1** (dummy variable trap) |
| **Ordinal / label encoding** | ordinal (Low < Med < High) | **ห้ามใช้กับ nominal ใน KNN/linear** — สร้างลำดับและระยะทางปลอม |
| **Binary (true/false)** | association rules (item = attribute=value) | [[LEC 10 Association Rules]] |
| target encoding | category จำนวนมาก | 📚 เสี่ยง leakage — ต้อง fit ใน train |

## 2.5 Discretization ⭐⭐

เต็ม: [[04 Data Pre-processing#4.6 Discretization: Numerical → Categorical ⭐⭐ (guideline ข้อ 3.6)]]
- **Unsupervised:** **equal width** (ช่วงกว้างเท่า — ข้อมูลเบ้ทำให้บางช่วงว่าง) · **equal frequency** (จำนวนเท่า) · k-means
- **Supervised:** entropy-based (ตัดให้ label แยกดีที่สุด)
- **ใช้เพื่อ:** association rules (ต้องเป็น item) · ลด noise · ตีความง่าย · tree บางชนิด
- ⚠️ เสียข้อมูลรายละเอียด · ขอบช่วงที่เรียนจากข้อมูลต้อง fit บน train

## 2.6 Feature Selection ⭐⭐⭐

เต็ม: [[04 Data Pre-processing#Feature Subset Selection]] · [[04 Data Pre-processing#2 แนวทาง: Filter vs Wrapper ⭐]]

> [!important] ⭐ ทำไมต้องเลือก feature
> ลด overfitting · โมเดลง่าย ตีความได้ (parsimony) · เร็ว · ลด curse of dimensionality (KNN) · ลด multicollinearity · ไม่ต้องเก็บข้อมูลตัวแปรที่ไม่ใช้
> ตัดทิ้งแน่: **redundant** (ซ้ำกับตัวอื่น — education ↔ educational-num) · **irrelevant** (ID) · **constant** (variance = 0) · **leaky** (ข้อมูลที่รู้หลังเกิดผล)

| แนวทาง | วิธี | ตัวอย่าง | ข้อดี / ข้อเสีย |
|---|---|---|---|
| **Filter** | ให้คะแนนแต่ละ feature ด้วยสถิติ **ก่อน** สร้างโมเดล | correlation กับ target · χ² · information gain · variance threshold | เร็ว · ไม่ดู interaction |
| **Wrapper** | ใช้ **โมเดลจริง** ประเมิน subset | **forward / backward selection** ([[09 Regression Analysis#9.11 Reducing Number of Predictors ⭐⭐]]) · exhaustive | แม่นกว่า · ช้า · เสี่ยง overfit |
| **Embedded** | เลือกระหว่างสร้างโมเดล | **Decision Tree** (Tree p.46: *"most informative attributes… avoids over-fitting"*) · RF importance · Lasso | สมดุล |
| **Extraction** (ไม่ใช่ selection) | สร้าง feature ใหม่ | **PCA** ([[LEC 03 PCA]]) | ลดมิติแต่ตีความยาก |

---

## 2.7 Data Leakage ⭐⭐⭐⭐

![[lec_leakage.png]]

> [!quote] สไลด์ KNN p.60 — คำต่อคำ
> **"Data leakage occurs when information from outside the training dataset is used to create the model."**
> **"…when data that should only be in the test set is included in the training set."**
> **ตัวอย่างปัญหา:** *"Normalization is performed using statistics (mean, variance) computed from the ENTIRE DATASET BEFORE SPLITTING → the test set indirectly influences training."*
> **"Always split the dataset into training and test sets first, then apply preprocessing separately."**

> [!important] ⭐⭐⭐ รูปแบบของ leakage ที่ต้องจับได้
> | รูปแบบ | ตัวอย่าง | แก้ |
> |---|---|---|
> | **preprocessing ก่อน split** | scale / impute / encode-target ด้วยสถิติของข้อมูลทั้งชุด | split ก่อน → fit บน train |
> | **resampling ก่อน split / CV** | SMOTE ทั้งชุดแล้วค่อยแบ่ง (Imbalanced p.21) | SMOTE เฉพาะ training fold (p.22) |
> | **feature selection ด้วยข้อมูลทั้งชุด** | เลือก feature จาก corr กับ y ทั้งชุด แล้ว CV | ทำใน pipeline ทุก fold |
> | **tune ด้วย test** | เลือก k จาก accuracy บน test | ใช้ validation / CV |
> | **target leakage** | feature ที่เกิด**หลัง** ผลลัพธ์ (เช่น "จำนวนวันค้างชำระ" ใช้ทำนายการผิดนัด) | ตัดออก · ถามว่า "ตอนทำนายจริงรู้ค่านี้ไหม" |
> | **duplicate ข้ามชุด** | แถวเดียวกันอยู่ทั้ง train และ test | ลบซ้ำก่อน split |
> | **scale test ด้วยค่าของ test เอง** | โค้ด R สไลด์ KNN p.51: `test_set[-3] = scale(test_set[-3])` | ใช้ mean/SD ของ train |

> [!bug] 🐛 ตัวอย่าง leakage ในสไลด์เอง (ข้อสอบ "หาที่ผิด")
> - **KNN p.56:** X มีค่า Age 38.78 และ Salary 63,777.78 = **ค่าเฉลี่ยของทั้ง 9 แถวที่ไม่ว่าง** → เติม missing ก่อน split (ค่าเฉลี่ยรวม test)
> - **KNN p.51 (R):** scale test set ด้วยสถิติของ test เอง
> - **Imbalanced p.20–21:** SMOTE ก่อน CV / ก่อน split
> - **W7 ของคุณ:** `imputer.fit(X)` ก่อน `train_test_split`

> [!tip] ⭐ เครื่องมือกัน leakage
> **Python:** `Pipeline` / `ColumnTransformer` / `imblearn.Pipeline` → `cross_validate` / `GridSearchCV` fit ทุกขั้นใหม่ในแต่ละ fold
> **RapidMiner:** วาง preprocessing ใน **Training pane** ของ Cross Validation + **Group Models** (Tree p.76) · หรือ `Split Data` → Normalize บน partition train → `Apply Model` (preprocessing model) กับ test (KNN p.59)
> **คำถามทดสอบตัวเอง:** *"ขั้นนี้ใช้ข้อมูลจาก test (หรือจากอนาคต) หรือเปล่า?"*

---

## ✅ Self-Test — LEC 02

> [!question]- Q1. ทำไม `StandardScaler().fit_transform(X)` แล้วค่อย `train_test_split` ถึงผิด
> mean/SD ถูกคำนวณจากทุกแถวรวม test → ข้อมูลจาก test รั่วเข้าไปในการเตรียม train (leakage) → ผลประเมินดีเกินจริง · ที่ถูก: split ก่อน → `fit` บน train → `transform` test

> [!question]- Q2. ข้อมูลรายได้มี missing 5% และเบ้ขวา ควร impute ด้วยอะไร
> **median** (จาก training set) — mean ถูกค่าสูงดึง

> [!question]- Q3. Filter vs Wrapper vs Embedded ยกตัวอย่างอย่างละ 1
> Filter: เลือกตาม |correlation| กับ target · Wrapper: backward elimination ด้วย linear regression · Embedded: feature importance ของ decision tree / Lasso

> [!question]- Q4. ทำไมไม่ควรใช้ label encoding (France = 0, Spain = 1, Germany = 2) กับ KNN
> KNN คำนวณระยะทาง → France กับ Germany ห่าง 2 แต่ France กับ Spain ห่าง 1 ทั้งที่ประเทศไม่มีลำดับ → ใช้ **one-hot**

> [!question]- Q5. feature "จำนวนครั้งที่ติดต่อฝ่ายเก็บหนี้" ใช้ทำนายว่าลูกค้าจะผิดนัดชำระได้ไหม
> ระวัง **target leakage** — ถ้าค่านี้เกิดขึ้น **หลัง** ลูกค้าผิดนัดแล้ว ตอนทำนายจริง (ก่อนผิดนัด) จะยังไม่รู้ค่านี้ → ต้องตัดออก

---

**กลับหน้าหลัก →** [[LEC 00 START HERE]] · **ถัดไป →** [[LEC 03 PCA]]
