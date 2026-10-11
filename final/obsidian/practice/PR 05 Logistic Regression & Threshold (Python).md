---
title: PR 05 · Logistic Regression & Threshold (Python)
tags: [final, lab, practice, python]
---

# PR 05 · Logistic Regression & Threshold — ไกด์ Python ทีละขั้น

> [!abstract] โจทย์
> คลินิกต้องการคัดกรองผู้ป่วยเบาหวานจากผลตรวจ 8 ค่า จงจัดการค่าว่างแฝง สร้าง Logistic Regression ตีความ odds ratio และเลือก threshold ที่เหมาะกับการคัดกรอง
>
> **สิ่งที่ต้องทำ:**
> 1. หา 0 ที่เป็นค่าว่าง 2. 0 → NaN + split 3. pipeline + coefficient/odds 4. predict_proba + threshold 0.5 5. เทียบหลาย threshold 6. ทำนายผู้ป่วยใหม่

**ข้อมูล:** `data/p5_pima_diabetes.csv` (Pima Indians Diabetes, 768 คน)
**เวลาแนะนำ:** 40 นาที · **ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · ทำโจทย์เดียวกันใน RapidMiner: [[PR 05 Logistic Regression & Threshold (RapidMiner)]] · ทฤษฎี/สูตร: [[LAB 05 Supervised Models#5.3 Logistic Regression ⭐⭐⭐⭐ (gap ใหญ่)]] · [[LEC 07 Linear & Logistic Regression]]

> [!tip] เตรียมตัว (ครั้งแรกครั้งเดียว)
> 1. VS Code → **File → Open Folder…** → เลือกโฟลเดอร์ `data mining/final/practice`
> 2. สร้างไฟล์ใหม่ `p05_mywork.ipynb` ในโฟลเดอร์นั้น
> 3. มุมขวาบน **Select Kernel → Jupyter Kernel… → Python (dm-exam)**
> 4. ทำทีละขั้น: พิมพ์โค้ด (หรือ copy) ลง cell ใหม่ → `Shift+Enter` → **เทียบกับ "ผลที่ควรได้"** ถ้าไม่ตรง หยุดหาสาเหตุก่อนไปขั้นต่อไป
> 5. ลองทำแบบ closed-book: อ่านแค่หัวข้อขั้นกับคำอธิบาย แล้วเขียนโค้ดเอง ค่อยเปิดดูโค้ดในไกด์

---

## ขั้นที่ 1 · Import + หาค่าว่างแฝง (0 ที่เป็นไปไม่ได้)

Pima 768 คน · target `diabetes` (1 = เป็นเบาหวาน) · glucose/BP/BMI = 0 เป็นไปไม่ได้ทางการแพทย์

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score, roc_auc_score

pima = pd.read_csv("data/p5_pima_diabetes.csv")
zero_cols = ["glucose", "blood_pressure", "skin_thickness", "insulin", "bmi"]
print((pima[zero_cols] == 0).sum())
print(pima["diabetes"].value_counts(normalize=True).round(3))
```

**ผลที่ควรได้:**

```text
glucose             5
blood_pressure     35
skin_thickness    227
insulin           374
bmi                11
dtype: int64
diabetes
0    0.651
1    0.349
Name: proportion, dtype: float64
```

> [!check] อ่านผล
> insulin เป็น 0 ถึง 374 แถว · skin 227 · เป็นเบาหวาน 34.9%

---

## ขั้นที่ 2 · แปลง 0 → NaN แล้ว split



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
pima[zero_cols] = pima[zero_cols].replace(0, np.nan)
X = pima.drop(columns="diabetes"); y = pima["diabetes"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=1992)
print(len(X_train), len(X_test), "| NaN ใน train:", X_train.isna().sum().sum())
```

**ผลที่ควรได้:**

```text
576 192 | NaN ใน train: 479
```

> [!check] อ่านผล
> train 576 / test 192 · median ที่จะเติมต้องคำนวณจาก train (อยู่ใน pipeline ขั้นถัดไป)

---

## ขั้นที่ 3 · Pipeline: impute median → scale → logistic



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
logreg = Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler()),
                   ("lr", LogisticRegression(max_iter=1000))]).fit(X_train, y_train)
coef = pd.DataFrame({"coef (per 1 SD)": logreg["lr"].coef_[0], "odds ratio": np.exp(logreg["lr"].coef_[0])},
                    index=X.columns).sort_values("coef (per 1 SD)", ascending=False).round(3)
print("intercept:", logreg["lr"].intercept_.round(3))
print(coef)
```

**ผลที่ควรได้:**

```text
intercept: [-0.835]
                coef (per 1 SD)  odds ratio
glucose                   1.103       3.013
bmi                       0.628       1.874
pregnancies               0.383       1.467
pedigree                  0.318       1.374
age                       0.148       1.160
insulin                   0.022       1.023
skin_thickness           -0.012       0.988
blood_pressure           -0.141       0.869
```

> [!check] อ่านผล
> glucose มีผลมากที่สุด: odds ratio **3.01** → glucose เพิ่ม 1 SD odds ของเบาหวานคูณ 3.01 (ตัวอื่นคงที่) · ตัวที่ OR ≈ 1 แทบไม่มีผล

---

## ขั้นที่ 4 · ความน่าจะเป็น → threshold 0.5



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
proba = logreg.predict_proba(X_test)[:, 1]
print("5 คนแรก P(diabetes):", proba[:5].round(3))
pred = (proba >= 0.5).astype(int)
tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()
print(f"TN={tn} FP={fp} FN={fn} TP={tp}")
print("acc", round(accuracy_score(y_test, pred), 3), "precision", round(precision_score(y_test, pred), 3),
      "recall", round(recall_score(y_test, pred), 3), "F1", round(f1_score(y_test, pred), 3))
print("AUC", round(roc_auc_score(y_test, proba), 3))
```

**ผลที่ควรได้:**

```text
5 คนแรก P(diabetes): [0.05  0.23  0.168 0.577 0.918]
TN=102 FP=23 FN=20 TP=47
acc 0.776 precision 0.671 recall 0.701 F1 0.686
AUC 0.857
```

> [!check] อ่านผล
> ที่ 0.5: recall **0.701** → พลาดผู้ป่วยไป 20 คน (FN) — สำหรับการคัดกรองถือว่ามากเกินไป

---

## ขั้นที่ 5 · เทียบหลาย threshold



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
rows = []
for t in [0.2, 0.3, 0.4, 0.5, 0.6]:
    p = (proba >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, p).ravel()
    rows.append({"threshold": t, "TP": tp, "FN": fn, "FP": fp, "TN": tn,
                 "precision": round(precision_score(y_test, p), 3), "recall": round(recall_score(y_test, p), 3),
                 "F1": round(f1_score(y_test, p), 3)})
thr = pd.DataFrame(rows)
print(thr.to_string(index=False))
```

**ผลที่ควรได้:**

```text
 threshold  TP  FN  FP  TN  precision  recall    F1
       0.2  65   2  62  63      0.512   0.970 0.670
       0.3  59   8  44  81      0.573   0.881 0.694
       0.4  52  15  31  94      0.627   0.776 0.693
       0.5  47  20  23 102      0.671   0.701 0.686
       0.6  38  29  16 109      0.704   0.567 0.628
```

> [!check] อ่านผล
> threshold ↓ → recall ↑ precision ↓ · ที่ 0.3: recall 0.881 (FN 8) F1 0.694

---

## ขั้นที่ 6 · ทำนายผู้ป่วยใหม่



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
patient = pd.DataFrame([{"pregnancies": 2, "glucose": 150, "blood_pressure": 70, "skin_thickness": np.nan,
                         "insulin": np.nan, "bmi": 33.5, "pedigree": 0.5, "age": 45}])
p_new = logreg.predict_proba(patient)[0, 1]
print("P(diabetes) =", round(p_new, 3), "→ threshold 0.3:", int(p_new >= 0.3), "| threshold 0.5:", int(p_new >= 0.5))
```

**ผลที่ควรได้:**

```text
P(diabetes) = 0.585 → threshold 0.3: 1 | threshold 0.5: 1
```

> [!check] อ่านผล
> P = **0.585** · ค่าว่าง (skin, insulin) ถูกเติมด้วย median ของ train ให้อัตโนมัติ

---

## ✅ สรุปคำตอบ
| คำถาม | คำตอบ |
|---|---|
| ค่าว่างแฝง | 0 ใน 5 คอลัมน์ → NaN → median (จาก train) |
| ตัวแปรสำคัญสุด | glucose (OR 3.01 ต่อ 1 SD) |
| AUC | 0.857 |
| threshold สำหรับคัดกรอง | ต่ำกว่า 0.5 (เช่น 0.3: recall 0.881) เพราะพลาดผู้ป่วยแพงกว่าตรวจซ้ำ |

| threshold | TP | FN | FP | TN | precision | recall | F1 |
|---|---|---|---|---|---|---|---|
| 0.2 | 65 | 2 | 62 | 63 | 0.512 | 0.97 | 0.67 |
| 0.3 | 59 | 8 | 44 | 81 | 0.573 | 0.881 | 0.694 |
| 0.4 | 52 | 15 | 31 | 94 | 0.627 | 0.776 | 0.693 |
| 0.5 | 47 | 20 | 23 | 102 | 0.671 | 0.701 | 0.686 |
| 0.6 | 38 | 29 | 16 | 109 | 0.704 | 0.567 | 0.628 |

> [!question]- ลองเองต่อ
> 1. ทำ 5-fold CV ด้วย `cross_val_predict(method="predict_proba")` แล้วหา threshold ที่ F1 สูงสุด
> 2. ลองไม่แปลง 0 → NaN แล้วดูว่า coefficient ของ insulin เปลี่ยนอย่างไร
