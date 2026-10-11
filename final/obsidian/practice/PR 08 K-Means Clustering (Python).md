---
title: PR 08 · K-Means Clustering (Python)
tags: [final, lab, practice, python]
---

# PR 08 · K-Means Clustering — ไกด์ Python ทีละขั้น

> [!abstract] โจทย์
> โรงบ่มไวน์ได้ไวน์ 178 ขวดที่ไม่รู้สายพันธุ์ จงจัดกลุ่มด้วย K-Means เลือกจำนวนกลุ่มด้วย elbow/silhouette/DB อธิบายลักษณะแต่ละกลุ่ม แสดงบน PCA และจัดกลุ่มไวน์ขวดใหม่
>
> **สิ่งที่ต้องทำ:**
> 1. เตรียมข้อมูล + scale 2. k = 2…8 3. profile k = 3 4. PCA plot 5. เทียบสายพันธุ์จริง 6. ขวดใหม่

**ข้อมูล:** `data/p8_wine_unlabeled.csv` (UCI Wine — คอลัมน์ cultivar ใช้ตรวจคำตอบเท่านั้น)
**เวลาแนะนำ:** 35 นาที · **ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · ทำโจทย์เดียวกันใน RapidMiner: [[PR 08 K-Means Clustering (RapidMiner)]] · ทฤษฎี/สูตร: [[LAB 06 Clustering & Association#6.2 K-Means + เลือกจำนวน cluster ⭐⭐⭐]] · [[LEC 09 Clustering]]

> [!tip] เตรียมตัว (ครั้งแรกครั้งเดียว)
> 1. VS Code → **File → Open Folder…** → เลือกโฟลเดอร์ `data mining/final/practice`
> 2. สร้างไฟล์ใหม่ `p08_mywork.ipynb` ในโฟลเดอร์นั้น
> 3. มุมขวาบน **Select Kernel → Jupyter Kernel… → Python (dm-exam)**
> 4. ทำทีละขั้น: พิมพ์โค้ด (หรือ copy) ลง cell ใหม่ → `Shift+Enter` → **เทียบกับ "ผลที่ควรได้"** ถ้าไม่ตรง หยุดหาสาเหตุก่อนไปขั้นต่อไป
> 5. ลองทำแบบ closed-book: อ่านแค่หัวข้อขั้นกับคำอธิบาย แล้วเขียนโค้ดเอง ค่อยเปิดดูโค้ดในไกด์

---

## ขั้นที่ 1 · Import + เตรียมข้อมูล (ไม่ใช้ label)

จัดกลุ่มไวน์ 178 ขวดจากเคมี 13 ค่า · **ตัด `cultivar` ออก** (เก็บไว้ตรวจทีหลังเท่านั้น)

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.decomposition import PCA

wine = pd.read_csv("data/p8_wine_unlabeled.csv")
truth = wine.pop("cultivar")
scaler = StandardScaler().fit(wine)
Z = scaler.transform(wine)
print(wine.shape, "| scaled mean≈0:", Z.mean(axis=0).round(2)[:4], "std≈1:", Z.std(axis=0).round(2)[:4])
```

**ผลที่ควรได้:**

```text
(178, 13) | scaled mean≈0: [-0. -0. -0. -0.] std≈1: [1. 1. 1. 1.]
```

> [!check] อ่านผล
> 13 feature standardize แล้ว · ถ้าไม่ scale proline (หลักพัน) จะครองระยะทาง

---

## ขั้นที่ 2 · K-Means k = 2…8: WCSS, silhouette, Davies–Bouldin



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
rows = []
for k in range(2, 9):
    km = KMeans(n_clusters=k, n_init=20, random_state=1992).fit(Z)
    rows.append({"k": k, "WCSS": round(km.inertia_, 1), "silhouette": round(silhouette_score(Z, km.labels_), 4),
                 "DB": round(davies_bouldin_score(Z, km.labels_), 4)})
ks = pd.DataFrame(rows)
print(ks.to_string(index=False))
fig, ax = plt.subplots(1, 2, figsize=(10, 3.5))
ax[0].plot(ks.k, ks.WCSS, "o-"); ax[0].set_title("Elbow (WCSS)"); ax[0].set_xlabel("k")
ax[1].plot(ks.k, ks.silhouette, "o-", color="tab:red"); ax[1].set_title("Silhouette"); ax[1].set_xlabel("k")
best_k = int(ks.loc[ks.silhouette.idxmax(), "k"])
```

**ผลที่ควรได้:**

```text
 k   WCSS  silhouette     DB
 2 1658.8      0.2593 1.5260
 3 1277.9      0.2849 1.3892
 4 1175.4      0.2586 1.8170
 5 1108.8      0.2536 1.6449
 6 1044.5      0.1941 1.8585
 7  987.0      0.1803 1.8193
 8  933.0      0.2001 1.6631
```

**กราฟที่ควรได้:**

![[pr_p8_2.png]]

> [!check] อ่านผล
> silhouette สูงสุดที่ **k = 3** (0.2849) · elbow เห็นการหักชัดที่ k = 3 · DB ต่ำสุดที่ k = 3

---

## ขั้นที่ 3 · K-Means k = 3 + profile ของกลุ่ม

ดูค่าเฉลี่ยของแต่ละกลุ่มในหน่วยเดิม + z-score ของ centroid

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
km3 = KMeans(n_clusters=3, n_init=20, random_state=1992).fit(Z)
lab = km3.labels_
print("ขนาดกลุ่ม:", np.bincount(lab))
prof = wine.groupby(lab)[["alcohol", "flavanoids", "color_intensity", "proline", "malic_acid", "hue"]].mean().round(2)
print(prof)
zc = pd.DataFrame(km3.cluster_centers_, columns=wine.columns)[["alcohol", "flavanoids", "color_intensity", "proline", "hue"]].round(2)
print(zc)
```

**ผลที่ควรได้:**

```text
ขนาดกลุ่ม: [65 51 62]
   alcohol  flavanoids  color_intensity  proline  malic_acid   hue
0    12.25        2.05             2.97   510.17        1.90  1.06
1    13.13        0.82             7.23   619.06        3.31  0.69
2    13.68        3.00             5.45  1100.23        2.00  1.07
   alcohol  flavanoids  color_intensity  proline   hue
0    -0.93        0.02            -0.90    -0.75  0.46
1     0.16       -1.22             0.94    -0.41 -1.16
2     0.84        0.98             0.17     1.13  0.47
```

> [!check] อ่านผล
> ตั้งชื่อกลุ่มจาก z-score ที่โดดเด่น (|z| > ~0.8):
> - **กลุ่ม 2** (62 ขวด): proline z = +1.13 · alcohol +0.84 · flavanoids +0.98 → **"เข้มข้น แอลกอฮอล์สูง proline สูง"**
> - **กลุ่ม 1** (51 ขวด): flavanoids -1.22 · hue -1.16 · color +0.94 → **"สีเข้ม flavanoids ต่ำ"**
> - **กลุ่ม 0** (65 ขวด): alcohol -0.93 · color -0.90 · proline -0.75 → **"เบา สีอ่อน แอลกอฮอล์ต่ำ"**

---

## ขั้นที่ 4 · ดูภาพบน PCA 2D



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
pca = PCA(n_components=2).fit(Z)
P = pca.transform(Z)
plt.figure(figsize=(6, 5))
plt.scatter(P[:, 0], P[:, 1], c=lab, cmap="viridis", s=18)
C2 = pca.transform(km3.cluster_centers_)
plt.scatter(C2[:, 0], C2[:, 1], marker="X", s=200, c="red")
plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.0%})"); plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.0%})")
plt.title("K-Means k=3 on PCA")
```

**กราฟที่ควรได้:**

![[pr_p8_4.png]]

> [!check] อ่านผล
> PC1+PC2 = 55.4% · 3 กลุ่มแยกกันชัดในภาพ (separation ดี)

---

## ขั้นที่ 5 · ตรวจกับ label จริง (เฉพาะเพื่อเช็ก — ในงานจริงไม่มี label)



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
print(pd.crosstab(pd.Series(lab, name="cluster"), truth))
match = pd.crosstab(lab, truth).max(axis=1).sum() / len(truth)
print("สัดส่วนที่ตรงกับสายพันธุ์จริง:", round(match, 4))
```

**ผลที่ควรได้:**

```text
cultivar  cultivar_0  cultivar_1  cultivar_2
cluster                                     
0                  0          65           0
1                  0           3          48
2                 59           3           0
สัดส่วนที่ตรงกับสายพันธุ์จริง: 0.9663
```

> [!check] อ่านผล
> แต่ละ cluster ตรงกับ cultivar หนึ่งเกือบทั้งหมด → **96.6%** ตรง · แปลว่าเคมีของไวน์แบ่งตามสายพันธุ์ได้เองโดยไม่ต้องบอก label

---

## ขั้นที่ 6 · จัดกลุ่มไวน์ขวดใหม่

ต้อง transform ด้วย **scaler ตัวเดิม** ก่อน predict

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
new = wine.iloc[[0]].copy()
new["alcohol"] = 13.0; new["proline"] = 600
print(new[["alcohol", "proline", "flavanoids"]])
print("cluster:", km3.predict(scaler.transform(new))[0])
```

**ผลที่ควรได้:**

```text
   alcohol  proline  flavanoids
0     13.0      600        3.06
cluster: 2
```

> [!check] อ่านผล
> ได้ cluster **2**

---

## ✅ สรุปคำตอบ
| k | WCSS | silhouette | DB |
|---|---|---|---|
| 2 | 1658.8 | 0.2593 | 1.526 |
| 3 | 1277.9 | 0.2849 | 1.3892 |
| 4 | 1175.4 | 0.2586 | 1.817 |
| 5 | 1108.8 | 0.2536 | 1.6449 |
| 6 | 1044.5 | 0.1941 | 1.8585 |
| 7 | 987.0 | 0.1803 | 1.8193 |
| 8 | 933.0 | 0.2001 | 1.6631 |

**k ที่เลือก = 3** (silhouette สูงสุด + elbow + ตีความได้) · ตรงกับสายพันธุ์ 96.6%
**cohesion:** WCSS ที่ k = 3 = 1277.9 · **separation:** กลุ่มแยกกันใน PCA plot · **interpretability:** profile ต่างกันชัด

> [!question]- ลองเองต่อ
> 1. รัน K-Means **โดยไม่ scale** แล้วดู crosstab กับ cultivar — แย่ลงเท่าไร เพราะอะไร
> 2. ใช้ `init="random", n_init=1` หลาย random_state แล้วดูว่า WCSS เปลี่ยนไหม (local optimum)
