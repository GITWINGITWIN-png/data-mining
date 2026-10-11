---
title: PR 03 · Imbalanced & SMOTE (Python)
tags: [final, lab, practice, python]
---

# PR 03 · Imbalanced & SMOTE — ไกด์ Python ทีละขั้น

> [!abstract] โจทย์
> โรงพยาบาลมีผลตรวจชิ้นเนื้อ 397 ราย มีมะเร็ง (malignant) เพียง 40 ราย จงสร้างโมเดลที่หามะเร็งได้ดี และเปรียบเทียบการไม่ resample / RUS / ROS / SMOTE โดยทำ resampling **เฉพาะ training fold**
>
> **สิ่งที่ต้องทำ:**
> 1. IR 2. majority baseline 3. tree ไม่ resample 4. RUS/ROS/SMOTE ใน pipeline 5. ดูผล SMOTE ต่อจำนวนแถว 6. เทียบกับวิธีผิด (SMOTE ก่อน CV)

**ข้อมูล:** `data/p3_breast_cancer_imbalanced.csv` (UCI Breast Cancer Wisconsin, 10 feature กลุ่ม mean)
**เวลาแนะนำ:** 35 นาที · **ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · ทำโจทย์เดียวกันใน RapidMiner: [[PR 03 Imbalanced & SMOTE (RapidMiner)]] · ทฤษฎี/สูตร: [[LEC 04 Imbalanced Classification]] · [[LAB 03 Preprocessing Recipes#3.5 Sampling & SMOTE ⭐⭐⭐]]

> [!tip] เตรียมตัว (ครั้งแรกครั้งเดียว)
> 1. VS Code → **File → Open Folder…** → เลือกโฟลเดอร์ `data mining/final/practice`
> 2. สร้างไฟล์ใหม่ `p03_mywork.ipynb` ในโฟลเดอร์นั้น
> 3. มุมขวาบน **Select Kernel → Jupyter Kernel… → Python (dm-exam)**
> 4. ทำทีละขั้น: พิมพ์โค้ด (หรือ copy) ลง cell ใหม่ → `Shift+Enter` → **เทียบกับ "ผลที่ควรได้"** ถ้าไม่ตรง หยุดหาสาเหตุก่อนไปขั้นต่อไป
> 5. ลองทำแบบ closed-book: อ่านแค่หัวข้อขั้นกับคำอธิบาย แล้วเขียนโค้ดเอง ค่อยเปิดดูโค้ดในไกด์

---

## ขั้นที่ 1 · Import + Imbalance Ratio

ผลตรวจชิ้นเนื้อ 397 ราย · target = `diagnosis` (malignant = มะเร็ง = **positive**)

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

bc = pd.read_csv("data/p3_breast_cancer_imbalanced.csv")
X = bc.drop(columns="diagnosis")
y = (bc["diagnosis"] == "malignant").astype(int)
counts = y.value_counts()
IR = counts[0] / counts[1]
print(counts.to_dict(), "IR =", round(IR, 2))
```

**ผลที่ควรได้:**

```text
{0: 357, 1: 40} IR = 8.93
```

> [!check] อ่านผล
> benign 357 : malignant 40 → **IR = 8.93** (mild, < 10) แต่คลาสที่สนใจมีแค่ 10.1%

---

## ขั้นที่ 2 · Baseline: ทาย benign ทุกคน



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
cv = StratifiedKFold(5, shuffle=True, random_state=1992)
scoring = ["accuracy", "precision", "recall", "f1"]
def run(name, model):
    r = cross_validate(model, X, y, cv=cv, scoring=scoring)
    return {"model": name, **{m: round(float(r[f"test_{m}"].mean()), 4) for m in scoring}}
import warnings; warnings.filterwarnings("ignore")
rows = [run("Majority baseline", DummyClassifier(strategy="most_frequent"))]
print(rows[0])
```

**ผลที่ควรได้:**

```text
{'model': 'Majority baseline', 'accuracy': 0.8992, 'precision': 0.0, 'recall': 0.0, 'f1': 0.0}
```

> [!check] อ่านผล
> accuracy **0.8992** โดยหามะเร็งไม่เจอเลย (recall 0) → **ห้ามใช้ accuracy ตัดสิน**

---

## ขั้นที่ 3 · E0: Decision Tree ไม่ทำอะไรกับ imbalance



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
tree = DecisionTreeClassifier(max_depth=4, random_state=1992)
rows.append(run("E0 tree (no sampling)", Pipeline([("sc", StandardScaler()), ("tree", tree)])))
print(rows[-1])
```

**ผลที่ควรได้:**

```text
{'model': 'E0 tree (no sampling)', 'accuracy': 0.9571, 'precision': 0.8343, 'recall': 0.75, 'f1': 0.7727}
```

> [!check] อ่านผล
> recall = 0.7500 · F1 = 0.7727

---

## ขั้นที่ 4 · E1–E3: RUS / ROS / SMOTE — ใส่ใน imblearn Pipeline

sampler อยู่ **ใน** Pipeline → ทำเฉพาะ training fold · validation fold เป็นข้อมูลจริง

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
for name, sampler in [("E1 RUS", RandomUnderSampler(random_state=1992)),
                      ("E2 ROS", RandomOverSampler(random_state=1992)),
                      ("E3 SMOTE", SMOTE(k_neighbors=5, random_state=1992))]:
    rows.append(run(name, Pipeline([("sc", StandardScaler()), ("sample", sampler), ("tree", tree)])))
table = pd.DataFrame(rows)
print(table.to_string(index=False))
```

**ผลที่ควรได้:**

```text
                model  accuracy  precision  recall     f1
    Majority baseline    0.8992     0.0000   0.000 0.0000
E0 tree (no sampling)    0.9571     0.8343   0.750 0.7727
               E1 RUS    0.8916     0.4910   0.900 0.6318
               E2 ROS    0.9119     0.5868   0.825 0.6648
             E3 SMOTE    0.9193     0.5859   0.825 0.6745
```

> [!check] อ่านผล
> ดูคอลัมน์ **recall และ F1** ไม่ใช่ accuracy:
> - **E0 (ไม่ resample) ได้ F1 สูงสุด 0.7727** แต่ recall 0.750 (พลาดมะเร็ง 25%)
> - **RUS ได้ recall สูงสุด 0.900** แต่ precision ตกเหลือ 0.491
> - SMOTE: recall 0.825 · precision 0.586 · F1 0.6745 (ดีกว่า RUS/ROS ด้าน F1)
> → **resampling เพิ่ม recall แลกกับ precision** — จะเลือกตัวไหนขึ้นกับเป้าหมาย

---

## ขั้นที่ 5 · SMOTE ทำอะไรกับจำนวนแถว (ใน training fold เดียว)

ดูผลของ SMOTE บน train ของ fold แรก

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
tr_idx, va_idx = next(cv.split(X, y))
Xs, ys = SMOTE(random_state=1992).fit_resample(StandardScaler().fit_transform(X.iloc[tr_idx]), y.iloc[tr_idx])
print("ก่อน:", y.iloc[tr_idx].value_counts().to_dict(), "→ หลัง:", pd.Series(ys).value_counts().to_dict())
print("validation fold (ไม่ถูกแตะ):", y.iloc[va_idx].value_counts().to_dict())
```

**ผลที่ควรได้:**

```text
ก่อน: {0: 285, 1: 32} → หลัง: {0: 285, 1: 285}
validation fold (ไม่ถูกแตะ): {0: 72, 1: 8}
```

> [!check] อ่านผล
> SMOTE สร้าง malignant สังเคราะห์จนเท่า benign · validation fold ยังเป็นสัดส่วนจริง

---

## ขั้นที่ 6 · วิธีที่ผิด: SMOTE ก่อน CV (ดูว่าผลดีเกินจริงแค่ไหน)

**ห้ามทำในข้อสอบ** — ทำเพื่อเห็นผลของ leakage

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
X_bad, y_bad = SMOTE(random_state=1992).fit_resample(StandardScaler().fit_transform(X), y)
bad = cross_val_score(tree, X_bad, y_bad, cv=cv, scoring="f1").mean()
print("F1 แบบผิด (SMOTE ก่อน CV):", round(bad, 4), "| แบบถูก:", table.f1.iloc[4])
```

**ผลที่ควรได้:**

```text
F1 แบบผิด (SMOTE ก่อน CV): 0.9502 | แบบถูก: 0.6745
```

> [!check] อ่านผล
> แบบผิดได้ F1 **0.9502** สูงกว่าแบบถูก (0.6745) — เพราะ validation มีจุดสังเคราะห์ที่เกือบซ้ำกับ train และสัดส่วนไม่ใช่โลกจริง (สไลด์ Imbalanced p.22)

---

## ✅ สรุปคำตอบ
| model | accuracy | precision | recall | f1 |
|---|---|---|---|---|
| Majority baseline | 0.8992 | 0.0 | 0.0 | 0.0 |
| E0 tree (no sampling) | 0.9571 | 0.8343 | 0.75 | 0.7727 |
| E1 RUS | 0.8916 | 0.491 | 0.9 | 0.6318 |
| E2 ROS | 0.9119 | 0.5868 | 0.825 | 0.6648 |
| E3 SMOTE | 0.9193 | 0.5859 | 0.825 | 0.6745 |

**เลือกอย่างไร (ตัวอย่างคำตอบ):** งานคัดกรองมะเร็ง การพลาดผู้ป่วย (FN) อันตรายกว่าการส่งตรวจซ้ำ (FP) → ให้น้ำหนัก **recall** → เลือก **SMOTE** (recall 0.825 และ F1 ดีกว่า RUS) หรือ RUS ถ้าต้องการ recall สูงสุด · ถ้าโจทย์ให้ใช้ **F1** เป็นเกณฑ์ → E0 (0.7727) ชนะ · baseline accuracy 0.8992 แต่ recall 0 → accuracy ใช้ตัดสินไม่ได้
**SMOTE ก่อน CV** ให้ F1 0.9502 (ดีเกินจริง) — ผิดหลัก "sampling เฉพาะ training data"

> [!question]- ลองเองต่อ
> 1. ใช้ `class_weight="balanced"` ใน DecisionTreeClassifier (ไม่ resample) แล้วเทียบ F1
> 2. เปลี่ยนโมเดลเป็น RandomForest แล้วดูว่ายังต้องใช้ SMOTE ไหม
