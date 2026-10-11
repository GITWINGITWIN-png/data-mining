---
title: PR 02 · Preprocessing & PCA (Python)
tags: [final, lab, practice, python]
---

# PR 02 · Preprocessing & PCA — ไกด์ Python ทีละขั้น

> [!abstract] โจทย์
> นักชีววิทยาวัดนกเพนกวิน 344 ตัว 3 สายพันธุ์ ข้อมูลมีค่าว่างและหน่วยต่างกัน จงเตรียมข้อมูลสำหรับ KNN ทำนายสายพันธุ์ **โดยไม่เกิด data leakage** และใช้ PCA ดูภาพ 2 มิติ
>
> **สิ่งที่ต้องทำ:**
> 1. หาค่าว่าง 2. ตัดแถวที่ไม่มีการวัด 3. ดูสเกล 4. **split ก่อน** 5. impute mode 6. one-hot 7. standardize vs normalize 8. discretize 9. PCA + loadings 10. PCA plot 11. Pipeline + KNN + CV

**ข้อมูล:** `data/p2_penguins.csv` (Palmer Penguins)
**เวลาแนะนำ:** 50 นาที · **ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · ทำโจทย์เดียวกันใน RapidMiner: [[PR 02 Preprocessing & PCA (RapidMiner)]] · ทฤษฎี/สูตร: [[LAB 03 Preprocessing Recipes]]

> [!tip] เตรียมตัว (ครั้งแรกครั้งเดียว)
> 1. VS Code → **File → Open Folder…** → เลือกโฟลเดอร์ `data mining/final/practice`
> 2. สร้างไฟล์ใหม่ `p02_mywork.ipynb` ในโฟลเดอร์นั้น
> 3. มุมขวาบน **Select Kernel → Jupyter Kernel… → Python (dm-exam)**
> 4. ทำทีละขั้น: พิมพ์โค้ด (หรือ copy) ลง cell ใหม่ → `Shift+Enter` → **เทียบกับ "ผลที่ควรได้"** ถ้าไม่ตรง หยุดหาสาเหตุก่อนไปขั้นต่อไป
> 5. ลองทำแบบ closed-book: อ่านแค่หัวข้อขั้นกับคำอธิบาย แล้วเขียนโค้ดเอง ค่อยเปิดดูโค้ดในไกด์

---

## ขั้นที่ 1 · Import + หาค่าว่าง

Penguins 3 สายพันธุ์ · เป้าหมายสุดท้าย: เตรียมข้อมูลให้ KNN ทำนาย `species` โดย **ไม่ leak**

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder, KBinsDiscretizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier

peng = pd.read_csv("data/p2_penguins.csv")
print(peng.shape)
print(peng.isna().sum())
print(peng[peng.isna().any(axis=1)].head(6))
```

**ผลที่ควรได้:**

```text
(344, 7)
species               0
island                0
bill_length_mm        2
bill_depth_mm         2
flipper_length_mm     2
body_mass_g           2
sex                  11
dtype: int64
   species     island  bill_length_mm  bill_depth_mm  flipper_length_mm  body_mass_g  sex
3   Adelie  Torgersen             NaN            NaN                NaN          NaN  NaN
8   Adelie  Torgersen            34.1           18.1              193.0       3475.0  NaN
9   Adelie  Torgersen            42.0           20.2              190.0       4250.0  NaN
10  Adelie  Torgersen            37.8           17.1              186.0       3300.0  NaN
11  Adelie  Torgersen            37.8           17.3              180.0       3700.0  NaN
47  Adelie      Dream            37.5           18.9              179.0       2975.0  NaN
```

> [!check] อ่านผล
> ค่าว่าง: ตัวเลข 4 คอลัมน์ว่างคอลัมน์ละ 2 แถว (**แถวเดียวกัน** — ไม่มีการวัดเลย) · `sex` ว่าง 11 แถว

---

## ขั้นที่ 2 · ตัดแถวที่ไม่มีการวัดเลย

แถวที่ทุกตัวเลขว่าง ไม่มีข้อมูลให้ใช้ → ตัดทิ้ง (เป็นการ clean ที่ไม่ได้ "เรียนค่า" จากข้อมูล จึงทำก่อน split ได้)

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
num_cols = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
peng = peng.dropna(subset=num_cols, how="all").reset_index(drop=True)
print(peng.shape, "| sex ยังว่าง:", peng["sex"].isna().sum())
print(peng["species"].value_counts())
```

**ผลที่ควรได้:**

```text
(342, 7) | sex ยังว่าง: 9
species
Adelie       151
Gentoo       123
Chinstrap     68
Name: count, dtype: int64
```

> [!check] อ่านผล
> เหลือ 342 แถว · sex ยังว่าง 9 แถว (จะเติมด้วย mode จาก train) · คลาสไม่สมดุลเล็กน้อย (Adelie มากสุด)

---

## ขั้นที่ 3 · ดูสเกลของแต่ละตัวแปร (ทำไมต้อง scale)



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
print(peng[num_cols].describe().loc[["mean", "std", "min", "max"]].round(1))
```

**ผลที่ควรได้:**

```text
      bill_length_mm  bill_depth_mm  flipper_length_mm  body_mass_g
mean            43.9           17.2              200.9       4201.8
std              5.5            2.0               14.1        802.0
min             32.1           13.1              172.0       2700.0
max             59.6           21.5              231.0       6300.0
```

> [!check] อ่านผล
> body_mass_g หลักพัน (std 802) แต่ bill_depth_mm หลักสิบ (std 2.0) → ถ้าไม่ scale KNN/PCA จะเห็นแค่ body_mass

---

## ขั้นที่ 4 · Split ก่อน preprocessing (กัน leakage)

แบ่ง 80/20 แบบ **stratify** — ล็อก test ไว้ ห้ามใช้คำนวณ mean/mode ใด ๆ

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
X = peng.drop(columns="species")
y = peng["species"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=1992)
print(len(X_train), len(X_test))
print(y_train.value_counts(normalize=True).round(3))
```

**ผลที่ควรได้:**

```text
273 69
species
Adelie       0.443
Gentoo       0.359
Chinstrap    0.198
Name: proportion, dtype: float64
```

> [!check] อ่านผล
> train 273 / test 69 · สัดส่วนคลาสใน train เท่ากับข้อมูลเดิม (stratify)

---

## ขั้นที่ 5 · Impute: เติม sex ด้วย mode ของ train

fit imputer บน train → transform ทั้ง train และ test

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
sex_imp = SimpleImputer(strategy="most_frequent").fit(X_train[["sex"]])
print("mode ที่เรียนจาก train:", sex_imp.statistics_)
X_train_sex = sex_imp.transform(X_train[["sex"]])
X_test_sex = sex_imp.transform(X_test[["sex"]])
print("ค่าว่างหลังเติม:", pd.isna(X_train_sex).sum(), pd.isna(X_test_sex).sum())
```

**ผลที่ควรได้:**

```text
mode ที่เรียนจาก train: ['MALE']
ค่าว่างหลังเติม: 0 0
```

> [!check] อ่านผล
> mode = **MALE** · เติมแล้วไม่มีค่าว่าง

---

## ขั้นที่ 6 · Encode: one-hot ของ island และ sex

nominal ไม่มีลำดับ → one-hot · `handle_unknown="ignore"` กัน test เจอค่าที่ train ไม่มี

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
ohe.fit(X_train[["island"]].assign(sex=X_train_sex.ravel()))
print(ohe.get_feature_names_out())
```

**ผลที่ควรได้:**

```text
['island_Biscoe' 'island_Dream' 'island_Torgersen' 'sex_FEMALE' 'sex_MALE']
```

> [!check] อ่านผล
> ได้ 5 คอลัมน์ใหม่ (island 3 + sex 2)

---

## ขั้นที่ 7 · Scale: standardize vs normalize

เทียบสองวิธีบน train (fit บน train เท่านั้น)

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
std = StandardScaler().fit(X_train[num_cols])
mm = MinMaxScaler().fit(X_train[num_cols])
z = pd.DataFrame(std.transform(X_test[num_cols]), columns=num_cols)
m = pd.DataFrame(mm.transform(X_test[num_cols]), columns=num_cols)
print("z-score test (mean, std):"); print(z.agg(["mean", "std"]).round(2))
print("min-max test (min, max):"); print(m.agg(["min", "max"]).round(2))
```

**ผลที่ควรได้:**

```text
z-score test (mean, std):
      bill_length_mm  bill_depth_mm  flipper_length_mm  body_mass_g
mean           -0.03          -0.10              -0.01        -0.07
std             0.94           1.06               0.91         1.08
min-max test (min, max):
     bill_length_mm  bill_depth_mm  flipper_length_mm  body_mass_g
min           -0.04          -0.02               0.14        -0.05
max            0.83           0.95               0.98         1.08
```

> [!check] อ่านผล
> z-score ของ **test** มี mean ไม่เป็น 0 เป๊ะ — **ถูกต้องแล้ว** เพราะใช้ mean/std ของ train · min-max ของ test อาจเกิน [0, 1] เล็กน้อยด้วยเหตุผลเดียวกัน

---

## ขั้นที่ 8 · Discretize: body_mass เป็น 3 ช่วงจำนวนเท่ากัน

equal frequency (quantile) — ขอบช่วงเรียนจาก train

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
kb = KBinsDiscretizer(n_bins=3, encode="ordinal", strategy="quantile").fit(X_train[["body_mass_g"]])
print("ขอบช่วง:", kb.bin_edges_[0].round(0))
bins = kb.transform(X_train[["body_mass_g"]]).ravel()
print(pd.crosstab(pd.Series(bins, name="mass_bin", index=X_train.index), y_train))
```

**ผลที่ควรได้:**

```text
ขอบช่วง: [2850. 3725. 4600. 6050.]
species   Adelie  Chinstrap  Gentoo
mass_bin                           
0.0           61         28       0
1.0           54         25      14
2.0            6          1      84
```

> [!check] อ่านผล
> ขอบช่วง ≈ 3725 และ 4600 g · ช่วงหนักสุด (2) แทบเป็น Gentoo ทั้งหมด → body mass แยก Gentoo ได้ดี

---

## ขั้นที่ 9 · PCA บนตัวเลข 4 ตัว (standardize ก่อน)

explained variance + loadings · ใช้เพื่อ **ดูภาพ** จึง fit กับข้อมูลทั้งชุดได้ (descriptive)

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
Z = StandardScaler().fit_transform(peng[num_cols])
pca = PCA().fit(Z)
print("explained:", pca.explained_variance_ratio_.round(4))
print("cumulative:", pca.explained_variance_ratio_.cumsum().round(4))
load = pd.DataFrame(pca.components_[:2].T, index=num_cols, columns=["PC1", "PC2"]).round(3)
print(load)
```

**ผลที่ควรได้:**

```text
explained: [0.6884 0.1931 0.0913 0.0271]
cumulative: [0.6884 0.8816 0.9729 1.    ]
                     PC1    PC2
bill_length_mm     0.455  0.597
bill_depth_mm     -0.400  0.798
flipper_length_mm  0.576  0.002
body_mass_g        0.548  0.084
```

> [!check] อ่านผล
> PC1 68.8% · PC2 19.3% · รวม **88.2%** → 2 มิติเก็บข้อมูลได้เกือบหมด
> PC1: flipper, body_mass, bill_length (+) vs bill_depth (−) → "ขนาดตัว" · PC2 ขับด้วย bill_depth / bill_length → "รูปทรงปาก"

---

## ขั้นที่ 10 · กราฟ PC1 × PC2 ระบายสีตาม species



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
P = pca.transform(Z)[:, :2]
fig, ax = plt.subplots(figsize=(6, 5))
for sp in peng["species"].unique():
    mk = (peng["species"] == sp).to_numpy()
    ax.scatter(P[mk, 0], P[mk, 1], s=15, label=sp)
ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.0%})"); ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.0%})")
ax.legend(); ax.set_title("Penguins PCA")
```

**กราฟที่ควรได้:**

![[pr_p2_10.png]]

> [!check] อ่านผล
> Gentoo แยกออกชัดตาม PC1 (ตัวใหญ่) · Adelie กับ Chinstrap แยกกันตาม PC2 (รูปปาก)

---

## ขั้นที่ 11 · รวมทุกอย่างใน Pipeline + KNN (แบบที่ใช้ในข้อสอบจริง)

ทุกขั้นที่เรียนค่าจากข้อมูลอยู่ใน Pipeline → CV จะ fit ใหม่ในทุก fold = **ไม่ leak**

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
prep = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), num_cols),
    ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                      ("oh", OneHotEncoder(handle_unknown="ignore"))]), ["island", "sex"]),
])
model = Pipeline([("prep", prep), ("knn", KNeighborsClassifier(n_neighbors=5))])
cv = StratifiedKFold(5, shuffle=True, random_state=1992)
acc = cross_val_score(model, X_train, y_train, cv=cv)
model.fit(X_train, y_train)
test_acc = model.score(X_test, y_test)
raw = cross_val_score(KNeighborsClassifier(5), X_train[num_cols].fillna(X_train[num_cols].median()), y_train, cv=cv)
print("CV acc (pipeline):", acc.round(3), "mean", acc.mean().round(4))
print("test acc:", round(test_acc, 4))
print("CV acc ถ้าไม่ scale:", raw.mean().round(4))
```

**ผลที่ควรได้:**

```text
CV acc (pipeline): [1.    0.982 0.982 0.981 1.   ] mean 0.989
test acc: 0.9855
CV acc ถ้าไม่ scale: 0.7653
```

> [!check] อ่านผล
> CV accuracy **0.9890** · test **0.9855** · ถ้าไม่ scale เหลือ 0.7653 → scaling ช่วยมาก

---

## ✅ สรุปคำตอบ
| คำถาม | คำตอบ |
|---|---|
| ค่าว่าง | ตัวเลขว่าง 2 แถว (ตัดทิ้ง) · sex ว่าง 11 → mode ของ train = MALE |
| PC1 + PC2 | 88.2% |
| CV / test accuracy (KNN k=5 + pipeline) | 0.9890 / 0.9855 |
| ไม่ scale | 0.7653 |

> [!question]- ลองเองต่อ
> 1. เปลี่ยน StandardScaler เป็น MinMaxScaler ใน pipeline แล้วเทียบ CV accuracy
> 2. ทำ PCA โดย **ไม่** standardize แล้วดูว่า PC1 อธิบายได้กี่ % และ loading ของ body_mass เท่าไร (ทำไม?)
> 3. เพิ่ม PCA(n_components=2) เข้าไปใน pipeline ก่อน KNN แล้วเทียบผล
