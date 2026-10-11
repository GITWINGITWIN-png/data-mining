---
title: PR 04 · KNN Baseline CV Optimize (Python)
tags: [final, lab, practice, python]
---

# PR 04 · KNN Baseline CV Optimize — ไกด์ Python ทีละขั้น

> [!abstract] โจทย์
> โรงบ่มไวน์ต้องการระบุสายพันธุ์องุ่นจากผลวิเคราะห์ทางเคมี 13 ค่า จงสร้าง baseline, KNN ก่อน/หลัง scale, optimize k ด้วย CV, แสดง top-5, confusion matrix และทำนายไวน์ใหม่
>
> **สิ่งที่ต้องทำ:**
> 1. ดูสเกล 2. baseline + KNN raw + KNN scaled 3. grid search k × weights 4. กราฟ k 5. confusion matrix 6. ทำนายไวน์ใหม่

**ข้อมูล:** `data/p4_wine.csv` (UCI Wine, 178 ตัวอย่าง 3 คลาส)
**เวลาแนะนำ:** 40 นาที · **ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · ทำโจทย์เดียวกันใน RapidMiner: [[PR 04 KNN Baseline CV Optimize (RapidMiner)]] · ทฤษฎี/สูตร: [[LAB 04 Workflow, Baseline & Evaluation]] · [[LAB 05 Supervised Models#5.1 K-Nearest Neighbors ⭐⭐⭐]]

> [!tip] เตรียมตัว (ครั้งแรกครั้งเดียว)
> 1. VS Code → **File → Open Folder…** → เลือกโฟลเดอร์ `data mining/final/practice`
> 2. สร้างไฟล์ใหม่ `p04_mywork.ipynb` ในโฟลเดอร์นั้น
> 3. มุมขวาบน **Select Kernel → Jupyter Kernel… → Python (dm-exam)**
> 4. ทำทีละขั้น: พิมพ์โค้ด (หรือ copy) ลง cell ใหม่ → `Shift+Enter` → **เทียบกับ "ผลที่ควรได้"** ถ้าไม่ตรง หยุดหาสาเหตุก่อนไปขั้นต่อไป
> 5. ลองทำแบบ closed-book: อ่านแค่หัวข้อขั้นกับคำอธิบาย แล้วเขียนโค้ดเอง ค่อยเปิดดูโค้ดในไกด์

---

## ขั้นที่ 1 · Import + ดูสเกล

ไวน์ 178 ตัวอย่าง จากองุ่น 3 สายพันธุ์ · ทำนาย `cultivar` ด้วย KNN

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold, cross_validate, GridSearchCV, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import confusion_matrix, classification_report

wine = pd.read_csv("data/p4_wine.csv")
X = wine.drop(columns="cultivar")
y = wine["cultivar"]
print(wine.shape)
print(y.value_counts())
print(X.agg(["min", "max"]).T.sort_values("max", ascending=False).head(4))
```

**ผลที่ควรได้:**

```text
(178, 14)
cultivar
cultivar_1    71
cultivar_0    59
cultivar_2    48
Name: count, dtype: int64
                      min      max
proline            278.00  1680.00
magnesium           70.00   162.00
alcalinity_of_ash   10.60    30.00
alcohol             11.03    14.83
```

> [!check] อ่านผล
> 13 feature · proline ช่วงหลักร้อย–พัน ขณะที่ตัวอื่นหลักหน่วย → **KNN ต้อง scale**

---

## ขั้นที่ 2 · Baseline + KNN ไม่ scale + KNN scale (folds เดียวกัน)



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
cv = StratifiedKFold(10, shuffle=True, random_state=1992)
def run(name, model):
    r = cross_validate(model, X, y, cv=cv, scoring=["accuracy", "f1_macro"])
    return {"model": name, "accuracy": round(r["test_accuracy"].mean(), 4), "f1_macro": round(r["test_f1_macro"].mean(), 4)}
rows = [run("Majority baseline", DummyClassifier(strategy="most_frequent")),
        run("KNN k=5 (raw)", KNeighborsClassifier(n_neighbors=5)),
        run("KNN k=5 (scaled)", Pipeline([("sc", StandardScaler()), ("knn", KNeighborsClassifier(n_neighbors=5))]))]
print(pd.DataFrame(rows).to_string(index=False))
```

**ผลที่ควรได้:**

```text
            model  accuracy  f1_macro
Majority baseline    0.3993    0.1901
    KNN k=5 (raw)    0.6863    0.6637
 KNN k=5 (scaled)    0.9775    0.9781
```

> [!check] อ่านผล
> baseline 0.3993 · KNN ไม่ scale 0.6863 · **scale แล้ว 0.9775** (เพิ่ม 0.291)
> multi-class → ใช้ **f1_macro** (เฉลี่ย F1 ของทุกคลาส)

---

## ขั้นที่ 3 · Optimize k และ weights ด้วย GridSearchCV

ใช้ **cv เดิม** · เลือกด้วย accuracy

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
pipe = Pipeline([("sc", StandardScaler()), ("knn", KNeighborsClassifier())])
grid = GridSearchCV(pipe, {"knn__n_neighbors": list(range(1, 31, 2)), "knn__weights": ["uniform", "distance"]},
                    cv=cv, scoring="accuracy").fit(X, y)
res = pd.DataFrame(grid.cv_results_)
top5 = res.sort_values(["mean_test_score", "param_knn__n_neighbors"], ascending=[False, True])[
    ["param_knn__n_neighbors", "param_knn__weights", "mean_test_score", "std_test_score"]].head(5).round(4)
print(grid.best_params_, round(grid.best_score_, 4))
print(top5.to_string(index=False))
```

**ผลที่ควรได้:**

```text
{'knn__n_neighbors': 5, 'knn__weights': 'uniform'} 0.9775
 param_knn__n_neighbors param_knn__weights  mean_test_score  std_test_score
                      5            uniform           0.9775          0.0372
                      5           distance           0.9775          0.0372
                     17            uniform           0.9775          0.0276
                     17           distance           0.9775          0.0276
                     19           distance           0.9775          0.0276
```

> [!check] อ่านผล
> best = **k 5, uniform** accuracy 0.9775 · หลายค่า k ได้ผลใกล้กัน

---

## ขั้นที่ 4 · กราฟ accuracy vs k



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
u = res[res["param_knn__weights"] == "uniform"]
plt.figure(figsize=(7, 3.5))
plt.errorbar(u["param_knn__n_neighbors"], u["mean_test_score"], yerr=u["std_test_score"], marker="o", capsize=3)
plt.xlabel("k"); plt.ylabel("CV accuracy"); plt.title("Choosing k (uniform)")
```

**กราฟที่ควรได้:**

![[pr_p4_4.png]]

> [!check] อ่านผล
> k = 1 ได้ 0.9552 · k = 5 ได้ 0.9775 · k = 29 ได้ 0.9605 · error bar = std ข้าม fold (ช่วง k กว้างให้ผลใกล้กัน → เลือก k ที่ดีสุดตัวเล็กที่สุด)

---

## ขั้นที่ 5 · Confusion matrix + classification report จาก CV



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
best = grid.best_estimator_
pred = cross_val_predict(best, X, y, cv=cv)
labels = sorted(y.unique())
print(pd.DataFrame(confusion_matrix(y, pred, labels=labels), index=labels, columns=labels))
print(classification_report(y, pred, digits=3))
```

**ผลที่ควรได้:**

```text
            cultivar_0  cultivar_1  cultivar_2
cultivar_0          59           0           0
cultivar_1           2          67           2
cultivar_2           0           0          48
              precision    recall  f1-score   support

  cultivar_0      0.967     1.000     0.983        59
  cultivar_1      1.000     0.944     0.971        71
  cultivar_2      0.960     1.000     0.980        48

    accuracy                          0.978       178
   macro avg      0.976     0.981     0.978       178
weighted avg      0.978     0.978     0.977       178
```

> [!check] อ่านผล
> แถว = actual · คอลัมน์ = predicted · ผิดพลาดน้อยมาก ส่วนใหญ่สับสนระหว่าง cultivar_1 กับคลาสอื่น

---

## ขั้นที่ 6 · ทำนายไวน์ใหม่

ไวน์ใหม่ 1 ขวด (ใช้ค่าเฉลี่ยของ cultivar_0 ปัดเศษ) → pipeline scale ให้เองด้วยค่าจาก train

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
new = X[y == "cultivar_0"].mean().round(2).to_frame().T
best.fit(X, y)
print(best.predict(new), best.predict_proba(new).round(3))
```

**ผลที่ควรได้:**

```text
['cultivar_0'] [[1. 0. 0.]]
```

> [!check] อ่านผล
> ทายเป็น **cultivar_0** · `predict_proba` = สัดส่วนโหวตของเพื่อนบ้าน

---

## ✅ สรุปคำตอบ
| model | accuracy | f1_macro |
|---|---|---|
| Majority baseline | 0.3993 | 0.1901 |
| KNN k=5 (raw) | 0.6863 | 0.6637 |
| KNN k=5 (scaled) | 0.9775 | 0.9781 |
| KNN tuned k=5 uniform | 0.9775 | — |

**ตีความ:** scaling เป็นตัวเปลี่ยนผลมากที่สุด · tune k ช่วยเพิ่มอีกเล็กน้อย/เท่าเดิม · ทุกโมเดลชนะ baseline มาก

> [!question]- ลองเองต่อ
> 1. ใช้ `metric="manhattan"` แล้วเทียบ
> 2. ใช้ hold-out 70/30 แทน CV แล้วรันหลาย random_state — ผลแกว่งแค่ไหน (เหตุผลที่ CV ดีกว่า)
