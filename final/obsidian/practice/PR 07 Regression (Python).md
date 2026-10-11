---
title: PR 07 · Regression (Python)
tags: [final, lab, practice, python]
---

# PR 07 · Regression — ไกด์ Python ทีละขั้น

> [!abstract] โจทย์
> บริษัทประกันต้องการประมาณค่ารักษาพยาบาลรายปีของลูกค้า จงสร้าง mean baseline, Linear Regression (ตีความ coefficient) และ KNN regressor (ก่อน/หลัง scale, optimize k) แล้วรายงาน MAE / RMSE / R²
>
> **สิ่งที่ต้องทำ:**
> 1. EDA ของ charges 2. encode + split 3. baseline vs linear 4. ตีความ coefficient 5. KNN regressor + optimize 6. ทำนายลูกค้าใหม่

**ข้อมูล:** `data/p7_insurance.csv` (Medical Cost Personal, 1,338 คน)
**เวลาแนะนำ:** 40 นาที · **ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · ทำโจทย์เดียวกันใน RapidMiner: [[PR 07 Regression (RapidMiner)]] · ทฤษฎี/สูตร: [[LAB 05 Supervised Models#5.2 Linear Regression ⭐⭐⭐]] · [[LEC 05 Model Construction & Evaluation#5.8 Regression Metrics ⭐⭐⭐]]

> [!tip] เตรียมตัว (ครั้งแรกครั้งเดียว)
> 1. VS Code → **File → Open Folder…** → เลือกโฟลเดอร์ `data mining/final/practice`
> 2. สร้างไฟล์ใหม่ `p07_mywork.ipynb` ในโฟลเดอร์นั้น
> 3. มุมขวาบน **Select Kernel → Jupyter Kernel… → Python (dm-exam)**
> 4. ทำทีละขั้น: พิมพ์โค้ด (หรือ copy) ลง cell ใหม่ → `Shift+Enter` → **เทียบกับ "ผลที่ควรได้"** ถ้าไม่ตรง หยุดหาสาเหตุก่อนไปขั้นต่อไป
> 5. ลองทำแบบ closed-book: อ่านแค่หัวข้อขั้นกับคำอธิบาย แล้วเขียนโค้ดเอง ค่อยเปิดดูโค้ดในไกด์

---

## ขั้นที่ 1 · Import + EDA ของ target

ค่ารักษาพยาบาลรายปี (`charges`) ของผู้ถือกรมธรรม์ 1,338 คน

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, KFold, cross_validate, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error, r2_score

ins = pd.read_csv("data/p7_insurance.csv")
print(ins.shape, "| missing:", ins.isna().sum().sum())
print(ins["charges"].describe().round(0))
print("skew:", round(ins["charges"].skew(), 3))
print(ins.groupby("smoker")["charges"].mean().round(0))
fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
sns.histplot(ins, x="charges", bins=40, ax=ax[0]); ax[0].set_title("charges")
sns.scatterplot(ins, x="age", y="charges", hue="smoker", s=12, ax=ax[1]); ax[1].set_title("age vs charges")
```

**ผลที่ควรได้:**

```text
(1338, 7) | missing: 0
count     1338.0
mean     13270.0
std      12110.0
min       1122.0
25%       4740.0
50%       9382.0
75%      16640.0
max      63770.0
Name: charges, dtype: float64
skew: 1.516
smoker
no      8434.0
yes    32050.0
Name: charges, dtype: float64
```

**กราฟที่ควรได้:**

![[pr_p7_1.png]]

> [!check] อ่านผล
> charges เบ้ขวา (skew 1.52, mean > median) · คนสูบบุหรี่จ่ายเฉลี่ย 32,050 vs ไม่สูบ 8,434 (~3.8 เท่า) · scatter เห็น 3 แถบตามอายุ (smoker แยกเป็นแถบบน)

---

## ขั้นที่ 2 · Encode categorical (drop_first) + split

linear regression ใช้ dummy แบบ **k−1** (`drop_first=True`) กัน dummy variable trap

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
X = pd.get_dummies(ins.drop(columns="charges"), columns=["sex", "smoker", "region"], drop_first=True, dtype=int)
y = ins["charges"]
print(list(X.columns))
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1992)
print(len(X_train), len(X_test))
```

**ผลที่ควรได้:**

```text
['age', 'bmi', 'children', 'sex_male', 'smoker_yes', 'region_northwest', 'region_southeast', 'region_southwest']
1070 268
```

> [!check] อ่านผล
> baseline ของแต่ละ dummy: sex = female · smoker = no · region = northeast (ตัวที่ถูกตัด)

---

## ขั้นที่ 3 · Mean baseline vs Linear Regression



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
def metrics(name, model):
    p = model.fit(X_train, y_train).predict(X_test)
    return {"model": name, "MAE": mean_absolute_error(y_test, p), "RMSE": root_mean_squared_error(y_test, p),
            "R2": r2_score(y_test, p)}
lin = LinearRegression()
rows = [metrics("Mean baseline", DummyRegressor(strategy="mean")), metrics("Linear Regression", lin)]
print(pd.DataFrame(rows).round(3).to_string(index=False))
```

**ผลที่ควรได้:**

```text
            model      MAE      RMSE     R2
    Mean baseline 8551.416 11499.334 -0.008
Linear Regression 3978.014  5746.375  0.748
```

> [!check] อ่านผล
> Linear Regression: MAE **3,978** · RMSE 5,746 · R² **0.748** — ดีกว่า baseline (R² -0.008) มาก

---

## ขั้นที่ 4 · ตีความ coefficient



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
coef = pd.Series(lin.coef_, index=X.columns).round(1)
print("intercept:", round(lin.intercept_, 1))
print(coef.sort_values(ascending=False))
```

**ผลที่ควรได้:**

```text
intercept: -11577.1
smoker_yes          23924.1
children              480.6
bmi                   328.6
age                   254.1
sex_male             -152.4
region_northwest     -323.4
region_southeast     -671.7
region_southwest     -802.2
dtype: float64
```

> [!check] อ่านผล
> - **smoker_yes = 23,924** → คนสูบบุหรี่ค่ารักษาสูงกว่าคนไม่สูบ ~23,924 ต่อปี **โดยตัวแปรอื่นคงที่**
> - **age = 254.1** → อายุ +1 ปี ค่ารักษา +254
> - **bmi = 328.6** → BMI +1 ค่ารักษา +329
> - region_* ติดลบ = ถูกกว่า northeast (baseline)

---

## ขั้นที่ 5 · KNN regressor: ก่อน/หลัง scale + optimize k (CV บน train)



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
kcv = KFold(5, shuffle=True, random_state=1992)
def cv_rmse(model):
    return -cross_validate(model, X_train, y_train, cv=kcv, scoring="neg_root_mean_squared_error")["test_score"].mean()
print("KNN raw k=5   :", round(cv_rmse(KNeighborsRegressor(5)), 0))
print("KNN scaled k=5:", round(cv_rmse(Pipeline([("sc", StandardScaler()), ("knn", KNeighborsRegressor(5))])), 0))
print("Linear        :", round(cv_rmse(LinearRegression()), 0))
g = GridSearchCV(Pipeline([("sc", StandardScaler()), ("knn", KNeighborsRegressor())]),
                 {"knn__n_neighbors": range(1, 31), "knn__weights": ["uniform", "distance"]},
                 cv=kcv, scoring="neg_root_mean_squared_error").fit(X_train, y_train)
print("best:", g.best_params_, "CV RMSE", round(-g.best_score_, 0))
rows.append(metrics(f"KNN tuned k={g.best_params_['knn__n_neighbors']}", g.best_estimator_))
print(pd.DataFrame(rows).round(3).to_string(index=False))
```

**ผลที่ควรได้:**

```text
KNN raw k=5   : 11659.0
KNN scaled k=5: 5788.0
Linear        : 6147.0
best: {'knn__n_neighbors': 11, 'knn__weights': 'distance'} CV RMSE 5690.0
            model      MAE      RMSE     R2
    Mean baseline 8551.416 11499.334 -0.008
Linear Regression 3978.014  5746.375  0.748
   KNN tuned k=11 3031.768  4942.649  0.814
```

> [!check] อ่านผล
> KNN tuned test RMSE 4,943 · R² 0.814 เทียบ Linear 5,746 / 0.748

---

## ขั้นที่ 6 · ทำนายลูกค้าใหม่



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
new = pd.DataFrame([{"age": 40, "bmi": 30.0, "children": 2, "sex_male": 1, "smoker_yes": 1,
                     "region_northwest": 0, "region_southeast": 1, "region_southwest": 0}])[X.columns]
print("Linear:", round(lin.predict(new)[0], 0), "| KNN:", round(g.best_estimator_.predict(new)[0], 0))
new_ns = new.assign(smoker_yes=0)
print("ถ้าไม่สูบ — Linear:", round(lin.predict(new_ns)[0], 0))
```

**ผลที่ควรได้:**

```text
Linear: 32509.0 | KNN: 31901.0
ถ้าไม่สูบ — Linear: 8585.0
```

> [!check] อ่านผล
> ต่างกันระหว่างสูบ/ไม่สูบใน Linear = coefficient ของ smoker_yes พอดี (23,924) — เพราะเป็นโมเดลเชิงเส้น

---

## ✅ สรุปคำตอบ
| model | MAE | RMSE | R2 |
|---|---|---|---|
| Mean baseline | 8551.416 | 11499.334 | -0.008 |
| Linear Regression | 3978.014 | 5746.375 | 0.748 |
| KNN tuned k=11 | 3031.768 | 4942.649 | 0.814 |

**ตีความ:** smoker เป็นปัจจัยใหญ่สุด · Linear ตีความง่าย · KNN ต้อง scale (ไม่ scale RMSE แย่มาก) · เลือกโมเดลตาม RMSE บน test + ความต้องการอธิบายผล

> [!question]- ลองเองต่อ
> 1. เพิ่ม feature `smoker_yes × bmi` (สูบ + อ้วน) ใน Linear แล้วดู R² (ความสัมพันธ์แบบ interaction)
> 2. ทำนาย log(charges) แทน charges แล้วเทียบ RMSE (หลังแปลงกลับ)
