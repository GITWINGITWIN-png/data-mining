---
title: PR 06 · Decision Tree vs Random Forest (Python)
tags: [final, lab, practice, python]
---

# PR 06 · Decision Tree vs Random Forest — ไกด์ Python ทีละขั้น

> [!abstract] โจทย์
> โรงพยาบาลต้องการทำนายโรคหัวใจจากผลตรวจ 13 ค่า จงแสดง overfitting ของ tree ที่โตเต็ม หาความลึกที่เหมาะด้วย CV เปรียบเทียบกับ Random Forest และบอก feature ที่สำคัญ
>
> **สิ่งที่ต้องทำ:**
> 1. ดูข้อมูล + split 2. tree โตเต็ม (overfit) 3. depth curve 4. grid search tree 5. วาด tree 6. RF default/tuned 7. importance + ตารางเทียบ

**ข้อมูล:** `data/p6_heart.csv` (UCI Heart Disease Cleveland, 303 คน)
**เวลาแนะนำ:** 40 นาที · **ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · ทำโจทย์เดียวกันใน RapidMiner: [[PR 06 Decision Tree vs Random Forest (RapidMiner)]] · ทฤษฎี/สูตร: [[LAB 05 Supervised Models#5.4 Decision Tree ⭐⭐⭐]] · [[LEC 08 Decision Trees & Random Forest]]

> [!tip] เตรียมตัว (ครั้งแรกครั้งเดียว)
> 1. VS Code → **File → Open Folder…** → เลือกโฟลเดอร์ `data mining/final/practice`
> 2. สร้างไฟล์ใหม่ `p06_mywork.ipynb` ในโฟลเดอร์นั้น
> 3. มุมขวาบน **Select Kernel → Jupyter Kernel… → Python (dm-exam)**
> 4. ทำทีละขั้น: พิมพ์โค้ด (หรือ copy) ลง cell ใหม่ → `Shift+Enter` → **เทียบกับ "ผลที่ควรได้"** ถ้าไม่ตรง หยุดหาสาเหตุก่อนไปขั้นต่อไป
> 5. ลองทำแบบ closed-book: อ่านแค่หัวข้อขั้นกับคำอธิบาย แล้วเขียนโค้ดเอง ค่อยเปิดดูโค้ดในไกด์

---

## ขั้นที่ 1 · Import + ดูข้อมูล

ผู้ป่วย 303 คน · `target` = 1 เป็นโรคหัวใจ · หลายคอลัมน์เป็น **รหัสหมวด** (cp, restecg, slope, ca, thal) แม้เก็บเป็นตัวเลข

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, recall_score, f1_score

heart = pd.read_csv("data/p6_heart.csv")
print(heart.shape, "| missing:", heart.isna().sum().sum())
print(heart["target"].value_counts().to_dict())
print(heart.nunique().sort_values().head(8).to_dict())
X = heart.drop(columns="target"); y = heart["target"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=1992)
print(len(X_train), len(X_test))
```

**ผลที่ควรได้:**

```text
(303, 14) | missing: 0
{1: 165, 0: 138}
{'sex': 2, 'fbs': 2, 'target': 2, 'exang': 2, 'restecg': 3, 'slope': 3, 'thal': 4, 'cp': 4}
227 76
```

> [!check] อ่านผล
> ไม่มีค่าว่าง · เป็นโรค 165 / ไม่เป็น 138 (ค่อนข้างสมดุล) · tree **ไม่ต้อง scale และไม่ต้อง one-hot** รหัสหมวดก็ได้ (แต่ต้องรู้ว่ามันเป็นหมวด)

---

## ขั้นที่ 2 · Tree โตเต็ม: train vs test



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
full = DecisionTreeClassifier(random_state=1992).fit(X_train, y_train)
print("depth:", full.get_depth(), "| leaves:", full.get_n_leaves())
print("train acc:", round(full.score(X_train, y_train), 4), "| test acc:", round(full.score(X_test, y_test), 4))
```

**ผลที่ควรได้:**

```text
depth: 8 | leaves: 35
train acc: 1.0 | test acc: 0.7763
```

> [!check] อ่านผล
> train **1.0000** (จำได้หมด) แต่ test **0.7763** → **overfitting** · tree ลึก 8 ชั้น มี 35 ใบ

---

## ขั้นที่ 3 · กราฟความลึก vs train/CV accuracy



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
cv = StratifiedKFold(10, shuffle=True, random_state=1992)
rows = []
for d in range(1, 13):
    r = cross_validate(DecisionTreeClassifier(max_depth=d, random_state=1992), X_train, y_train, cv=cv, return_train_score=True)
    rows.append({"depth": d, "train": r["train_score"].mean(), "cv": r["test_score"].mean()})
dt = pd.DataFrame(rows).round(4)
print(dt.to_string(index=False))
plt.figure(figsize=(7, 3.5))
plt.plot(dt.depth, dt.train, "o-", label="train"); plt.plot(dt.depth, dt.cv, "s-", label="CV")
plt.xlabel("max_depth"); plt.ylabel("accuracy"); plt.legend(); plt.title("Tree depth vs accuracy")
best_d = int(dt.loc[dt.cv.idxmax(), "depth"])
```

**ผลที่ควรได้:**

```text
 depth  train     cv
     1 0.7538 0.6352
     2 0.7827 0.7628
     3 0.8644 0.7893
     4 0.9016 0.7630
     5 0.9462 0.7674
     6 0.9731 0.7239
     7 0.9873 0.7057
     8 0.9976 0.7105
     9 0.9995 0.7194
    10 1.0000 0.7194
    11 1.0000 0.7194
    12 1.0000 0.7194
```

**กราฟที่ควรได้:**

![[pr_p6_3.png]]

> [!check] อ่านผล
> CV สูงสุดที่ depth **3** (0.7893) · train เพิ่มเรื่อย ๆ จนใกล้ 1 แต่ CV ไม่เพิ่ม → ช่องว่าง = overfitting

---

## ขั้นที่ 4 · Optimize tree (criterion × depth × min leaf)



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
grid = GridSearchCV(DecisionTreeClassifier(random_state=1992),
                    {"criterion": ["gini", "entropy"], "max_depth": [2, 3, 4, 5, 6], "min_samples_leaf": [1, 5, 10, 20]},
                    cv=cv, scoring="accuracy").fit(X_train, y_train)
print(grid.best_params_, round(grid.best_score_, 4))
tree = grid.best_estimator_
print("test acc:", round(tree.score(X_test, y_test), 4))
print(export_text(tree, feature_names=list(X.columns), max_depth=3))
```

**ผลที่ควรได้:**

```text
{'criterion': 'entropy', 'max_depth': 3, 'min_samples_leaf': 10} 0.8156
test acc: 0.7763
|--- cp <= 0.50
|   |--- ca <= 0.50
|   |   |--- thal <= 2.50
|   |   |   |--- class: 1
|   |   |--- thal >  2.50
|   |   |   |--- class: 0
|   |--- ca >  0.50
|   |   |--- sex <= 0.50
|   |   |   |--- class: 0
|   |   |--- sex >  0.50
|   |   |   |--- class: 0
|--- cp >  0.50
|   |--- sex <= 0.50
|   |   |--- ca <= 0.50
|   |   |   |--- class: 1
|   |   |--- ca >  0.50
|   |   |   |--- class: 1
|   |--- sex >  0.50
|   |   |--- age <= 56.50
|   |   |   |--- class: 1
|   |   |--- age >  56.50
|   |   |   |--- class: 0
```

> [!check] อ่านผล
> best: **{'criterion': 'entropy', 'max_depth': 3, 'min_samples_leaf': 10}** · CV 0.8156 · test 0.7763
> root split = feature ที่ลด impurity มากที่สุด (บรรทัดแรกของ export_text)

---

## ขั้นที่ 5 · วาด tree



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
plt.figure(figsize=(14, 6))
plot_tree(tree, feature_names=list(X.columns), class_names=["healthy", "disease"], filled=True, max_depth=3, fontsize=8)
```

**กราฟที่ควรได้:**

![[pr_p6_5.png]]

> [!check] อ่านผล
> แต่ละกล่อง: เงื่อนไข · impurity · samples · value (จำนวนแต่ละคลาส) · class ที่ทาย · สีเข้ม = บริสุทธิ์มาก

---

## ขั้นที่ 6 · Random Forest default และ tuned



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
rf = RandomForestClassifier(n_estimators=300, random_state=1992, n_jobs=-1)
rf_cv = cross_validate(rf, X_train, y_train, cv=cv)["test_score"].mean()
rf_grid = GridSearchCV(RandomForestClassifier(n_estimators=300, random_state=1992, n_jobs=-1),
                       {"max_features": ["sqrt", 0.5], "min_samples_leaf": [1, 3, 5]}, cv=cv, scoring="accuracy").fit(X_train, y_train)
print("RF default CV:", round(rf_cv, 4))
print("RF tuned:", rf_grid.best_params_, round(rf_grid.best_score_, 4))
rf_best = rf_grid.best_estimator_
print("RF test acc:", round(rf_best.score(X_test, y_test), 4))
```

**ผลที่ควรได้:**

```text
RF default CV: 0.8334
RF tuned: {'max_features': 'sqrt', 'min_samples_leaf': 5} 0.8377
RF test acc: 0.8289
```

> [!check] อ่านผล
> RF default CV 0.8334 · tuned 0.8377 · test **0.8289**

---

## ขั้นที่ 7 · Feature importance + ตารางเปรียบเทียบ



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
imp = pd.Series(rf_best.feature_importances_, index=X.columns).sort_values(ascending=False).round(3)
print(imp.head(5))
base = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
comp = pd.DataFrame([
    {"model": "Majority baseline", "test acc": base.score(X_test, y_test), "recall": recall_score(y_test, base.predict(X_test))},
    {"model": "Tree (full)", "test acc": full.score(X_test, y_test), "recall": recall_score(y_test, full.predict(X_test))},
    {"model": "Tree (tuned)", "test acc": tree.score(X_test, y_test), "recall": recall_score(y_test, tree.predict(X_test))},
    {"model": "RF (tuned)", "test acc": rf_best.score(X_test, y_test), "recall": recall_score(y_test, rf_best.predict(X_test))},
]).round(4)
print(comp.to_string(index=False))
```

**ผลที่ควรได้:**

```text
ca         0.144
cp         0.143
thalach    0.139
thal       0.124
exang      0.085
dtype: float64
            model  test acc  recall
Majority baseline    0.5395  1.0000
      Tree (full)    0.7763  0.8049
     Tree (tuned)    0.7763  0.8049
       RF (tuned)    0.8289  0.8537
```

> [!check] อ่านผล
> feature สำคัญอันดับ 1–3: **ca, cp, thalach** · importance ไม่บอกทิศทาง (เพิ่มหรือลดความเสี่ยง)
> ⚠️ baseline ได้ recall **1.0** เพราะคลาสส่วนมากของข้อมูลนี้คือ "เป็นโรค" (target = 1) → ทายเป็นโรคทุกคน — accuracy 0.5395 · recall สูงจากการทายเหมาเป็นกับดัก ต้องดู precision/accuracy ประกอบ

---

## ✅ สรุปคำตอบ
| model | test acc | recall |
|---|---|---|
| Majority baseline | 0.5395 | 1.0 |
| Tree (full) | 0.7763 | 0.8049 |
| Tree (tuned) | 0.7763 | 0.8049 |
| RF (tuned) | 0.8289 | 0.8537 |

**ตีความ:** tree โตเต็มจำ train ได้ 100% แต่ test 0.7763 = overfitting · tree ที่ tune (depth 3, 8 ใบ) ได้ test **เท่ากัน** แต่ CV ดีกว่ามาก (0.8156 vs 0.7105 ที่ depth 8) และง่ายกว่ามาก → เลือกตัวที่ง่ายกว่า (parsimony) · RF รวม 300 ต้นที่ต่างกัน (bootstrap + สุ่ม feature) จึงเสถียรกว่า · ข้อมูล test แค่ 76 คน — ต่างกัน 1–2 คนก็เปลี่ยน accuracy ~1–3% ระวังการสรุป

> [!question]- ลองเองต่อ
> 1. ใช้ `ccp_alpha` (post-pruning) หา tree ที่ดีที่สุด
> 2. ทำนายผู้ป่วย age 60, sex 1, cp 0, trestbps 140, chol 260, fbs 0, restecg 1, thalach 130, exang 1, oldpeak 2.0, slope 1, ca 2, thal 3 ด้วย tree และ RF แล้วเทียบ predict_proba
