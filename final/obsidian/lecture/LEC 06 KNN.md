---
title: LEC 06 · K-Nearest Neighbors
exam: Lecture — จ. 19 ต.ค. 2569 16:00–19:00
guideline: "Lecture ข้อ 4.1 — K-Nearest Neighbors: concept, distance calculation, ค่า k, classification และ prediction"
source: 69_1_Kitsana_KNN.pdf p.25–51 · Data_69_1-2.pdf p.17–31
tags: [final, lecture, knn, distance, lazy-learning]
---

# LEC 06 · K-Nearest Neighbors (KNN)
### "นกประเภทเดียวกันมักบินรวมฝูง" — ทายจากเพื่อนบ้านที่ใกล้ที่สุด

> [!abstract] guideline ข้อ 4.1: **concept · distance calculation · ค่า k · classification และ prediction**
> → [[#6.1 แนวคิด ⭐⭐⭐]] · [[#6.2 การคำนวณระยะทาง ⭐⭐⭐⭐]] · [[#6.3 การเลือก k ⭐⭐⭐]] · [[#6.4 Classification vs Prediction (Regression) ⭐⭐⭐]] · [[#6.5 Scaling — จำเป็นสำหรับ KNN ⭐⭐⭐]]

**ลิงก์:** [[LEC 00 START HERE|หน้าหลัก Lecture]] · [[LEC 05 Model Construction & Evaluation]] · [[LEC 07 Linear & Logistic Regression]] · ฝั่ง Lab: [[LAB 05 Supervised Models#5.1 K-Nearest Neighbors ⭐⭐⭐]] · ระยะทางแบบอื่น (binary, Jaccard, cosine): [[02 Data and Dataset Types]] (มิดเทอม)

---

## 6.1 แนวคิด ⭐⭐⭐

> [!quote] สไลด์ KNN p.25–28
> **"Birds of a feather flock together"** (นกประเภทเดียวกันมักบินรวมฝูง) · ใช้ได้ทั้ง **classification และ regression**
> **4 ขั้น (p.26):** (1) **Define K** (2) **Calculate distances** (Euclidean, Manhattan, cosine similarity) จากจุดใหม่ไปทุกจุดใน training (3) **Identify the K nearest neighbors** (4) **Predict** — classification = *most frequent class* · regression = **average** ของเพื่อนบ้าน k ตัว

> [!important] ⭐ KNN ต้องการ 3 อย่าง (p.33) และเป็น "lazy learner"
> 1. **ชุดข้อมูล training ที่เก็บไว้** (stored records) 2. **distance metric** 3. **ค่า k**
>
> **Instance-based / Lazy learning (p.31–32):** *"Data-driven, not model-driven"* — **ไม่สร้างโมเดลไว้ล่วงหน้า** แค่เก็บข้อมูล แล้วคำนวณตอนจะทาย → *"classifying unknown records is relatively expensive"*
> เทียบ **eager learner** (decision tree): สร้างโมเดล (กฎ) จาก training ก่อน ทายเร็ว

| | **Lazy (KNN)** | **Eager (Tree, Logistic)** |
|---|---|---|
| ตอน train | แค่เก็บข้อมูล (เร็ว) | สร้างโมเดล (ช้ากว่า) |
| ตอน predict | คำนวณระยะทางทุกจุด (**ช้า**) | ใช้โมเดล (เร็ว) |
| มีโมเดลให้อ่าน | ไม่มี | มี (กฎ / coefficient) |

---

## 6.2 การคำนวณระยะทาง ⭐⭐⭐⭐

> [!important] ⭐ สูตร (KNN p.35–36, Data p.20–23)
> **Euclidean (L2):** $d(i,j)=\sqrt{(x_{i1}-x_{j1})^2+(x_{i2}-x_{j2})^2+\dots+(x_{ip}-x_{jp})^2}$
> **Manhattan (L1, city block):** $d(i,j)=\lvert x_{i1}-x_{j1}\rvert+\lvert x_{i2}-x_{j2}\rvert+\dots+\lvert x_{ip}-x_{jp}\rvert$
> **Minkowski (Lq):** $d(i,j)=\left(\sum_k \lvert x_{ik}-x_{jk}\rvert^{q}\right)^{1/q}$ — q = 1 → Manhattan · q = 2 → Euclidean
> **Weighted Euclidean:** $\sqrt{w_1(x_{i1}-x_{j1})^2+\dots+w_p(x_{ip}-x_{jp})^2}$ (ให้ feature สำคัญมีน้ำหนักมาก)
> sklearn: `KNeighborsClassifier(n_neighbors=5, metric="minkowski", p=2)` (p.50) = Euclidean

> [!bug] 🐛 สไลด์ KNN p.36 พิมพ์ผิด 2 จุด
> 1. พจน์ที่สองเขียน $\lvert x_{i2}-x_{jp}\rvert$ → ที่ถูกคือ $\lvert x_{i2}-x_{j2}\rvert$
> 2. สูตร Euclidean / weighted พจน์สุดท้ายเขียนยกกำลัง **q** → ที่ถูกคือ **2**

> [!example]- 🧮 Data matrix 4 จุด (Data p.21) — คำนวณยืนยันแล้ว
> x1 = (1, 2) · x2 = (3, 5) · x3 = (2, 0) · x4 = (4, 5)
> | คู่ | Euclidean | Manhattan |
> |---|---|---|
> | x1–x2 | √(4+9) = **3.61** | 2+3 = **5** |
> | x1–x3 | √(1+4) = **2.24** | 1+2 = **3** |
> | x1–x4 | √(9+9) = **4.24** | **6** |
> | x2–x3 | √(1+25) = **5.10** | **6** |
> | x2–x4 | √(1+0) = **1.00** | **1** |
> | x3–x4 | √(4+25) = **5.39** | **7** |
> 🐛 สไลด์ Data p.21 พิมพ์ d(x3, x1) = **5.1** — ที่ถูกคือ **2.24** (คัดลอกมาจาก d(x3, x2)) — เจอตั้งแต่มิดเทอม ([[02 Data and Dataset Types]])

> [!example] ⭐ ทายด้วยมือ: Riding Mowers (KNN p.40–41) ครัวเรือนใหม่ Income = 60, Lot_Size = 20 (ค่าดิบ)
> ![[lec_knn_k.png]]
> เพื่อนบ้านใกล้สุด: (60.0, 18.4) **Owner** d = 1.600 · (61.5, 20.8) **Owner** d = 1.700 · (59.4, 16.0) **Nonowner** d = 4.045 · (64.8, 21.6) Owner d = 5.060 · (64.8, 17.2) Nonowner d = 5.557
> - **k = 1** → Owner · **k = 3** → Owner 2 : Nonowner 1 → **Owner** · **k = 5** → Owner 3 : 2 → **Owner**
> - ⚠️ สองตัวแปรนี้หน่วยต่างกัน (พันดอลลาร์ vs พันตารางฟุต) — การทายด้วยค่าดิบแบบนี้ทำได้ แต่ถ้าโจทย์ให้ scale ต้อง scale ก่อน (ดู 6.5)

---

## 6.3 การเลือก k ⭐⭐⭐

> [!quote] สไลด์ KNN p.37–39
> - **"choose that value of k which has lowest error rate in VALIDATION data"** (ตัวหนา+ขีดเส้นใต้)
> - **"Typically choose ODD value for k"** (กันเสียงเสมอใน 2 คลาส)
> - **k เล็กเกิน** → *"sensitive to noise points"* — จับ local structure แต่จับ noise ด้วย (**overfit**)
> - **k ใหญ่เกิน** → *"neighborhood may include points from other classes"* — เรียบเกิน พลาดโครงสร้างเฉพาะที่ (**underfit**)
> - **k = n** = **naïve rule** (ทายคลาสส่วนมากทุกแถว)

> [!example] ⭐ ตาราง XLMiner (p.42–43): 18 training · 6 validation · k = 1…18
> | k | 1 | 2–7 | **8** | 9 | 10 | 11 | 12 | 13 | 14 | 15–17 | 18 |
> |---|---|---|---|---|---|---|---|---|---|---|---|
> | % error train | **0.00** | 11–28 | 22.22 | 22.22 | 22.22 | 16.67 | 16.67 | 11.11 | 11.11 | 5.6–16.7 | 50.00 |
> | % error valid | 33.33 | 33.33 | **16.67** | 16.67 | 16.67 | 33.33 | **16.67** | 33.33 | 16.67 | 33.33 | 50.00 |
> - สไลด์: **"Best k appears to be k = 8. k = 9, 10, 14 also share low error rate, but best to choose lowest k."**
> - k = 1 train error **0%** = จำข้อมูล (overfit) แต่ validation 33% · k = 18 = naive rule 50%
> - 16.67% = 1/6 ของ validation · 33.33% = 2/6
> 🐛 สไลด์ลืม **k = 12** ซึ่งก็ได้ 16.67% เช่นกัน (ไม่เปลี่ยนคำตอบ — ยังเลือก k = 8 ที่ต่ำที่สุด)

---

## 6.4 Classification vs Prediction (Regression) ⭐⭐⭐

| | **Classification** | **Prediction (regression)** |
|---|---|---|
| target | categorical | numeric |
| รวมผลเพื่อนบ้าน | **majority vote** | **average** ของค่า y (p.44: *"Instead of majority vote… use average of response values"*) |
| แบบถ่วงน้ำหนัก | weighted vote | **weighted average** — *"weight decreasing with distance"* (p.44) |
| sklearn | `KNeighborsClassifier` | `KNeighborsRegressor` |

> [!example]- 🧮 Weighted average (1/d)
> เพื่อนบ้าน 3 ตัว: (d = 1, y = 20) · (d = 2, y = 30) · (d = 4, y = 40)
> **ค่าเฉลี่ยธรรมดา** = (20 + 30 + 40)/3 = **30**
> **ถ่วง 1/d:** w = 1, 0.5, 0.25 → (20·1 + 30·0.5 + 40·0.25)/(1.75) = 45/1.75 = **25.71** (เพื่อนบ้านใกล้มีผลมากกว่า)

---

## 6.5 Scaling — จำเป็นสำหรับ KNN ⭐⭐⭐

> [!quote] สไลด์ KNN p.45
> **"Attributes may have to be scaled to prevent distance measures from being dominated by one of the attributes"**
> ตัวอย่าง: height 1.5–1.8 m · weight 90–300 lb · income \$10K–\$1M → income ครองระยะทางทั้งหมด

> [!example] ⭐ Drill: scaling **เปลี่ยนคำตอบ** (คำนวณยืนยันแล้ว)
> training 10 คน (age, income พันบาท, y): (25,40,N) (35,60,N) (45,80,N) (20,20,N) (35,120,N) (52,18,N) (23,95,Y) (40,62,Y) (60,100,Y) (48,220,Y) · ลูกค้าใหม่ **(48, 142)** · k = 3
> **ค่าดิบ:** ใกล้สุด (35,120,N) d = 25.55 · (60,100,Y) d = 43.68 · (23,95,Y) d = 53.24 → Y 2 : N 1 → **Y**
> **min-max [0,1] (min/max จาก training):** ลูกค้าใหม่ = (0.700, 0.614) · ใกล้สุด (45,80,N) 0.316 · (35,120,N) 0.343 · (60,100,Y) 0.365 → N 2 : Y 1 → **N**
> **คำตอบพลิก** เพราะค่าดิบ income (ช่วง 18–220) กลบ age (ช่วง 20–60) · ⚠️ scale ข้อมูลใหม่ด้วย min/max **ของ training** (ไม่ใช่ของตัวเอง)

> 📚 RapidMiner `Normalize` (KNN p.59): **Z-transformation** (mean 0, variance 1 — *"less influenced by outliers"*) · **range transformation** (min-max — *"can be influenced by outliers"*)

---

## 6.6 จุดอ่อน — Curse of Dimensionality ⭐⭐

> [!quote] สไลด์ KNN p.46
> - *"Expected distance to nearest neighbor increases with p (number of predictors)"* → มิติมาก จุดทุกจุด "ไกลพอ ๆ กัน" ระยะทางเลยไม่ช่วยแยกคลาส = **curse of dimensionality**
> - *"Size of training set needed increases exponentially with p"* · *"slow on large training sets"*
> - **ทางแก้:** **ลดมิติด้วย PCA** ([[LEC 03 PCA]]) หรือ feature selection · ต้องหา optimal k

| ✅ Pros (p.48) | ❌ Cons (p.49) |
|---|---|
| ง่าย ไม่มีสมมติฐาน (linearity, normality) | ไวต่อ outlier/noise (โดยเฉพาะ k เล็ก) |
| จับ interaction ซับซ้อนได้ | curse of dimensionality |
| ใช้กับหลายคลาสได้ | ทายช้า (ต้องคำนวณระยะทางทุกจุด) |
| ไม่ต้องฝึกโมเดล | ต้อง scale + เลือก k |

---

## ✅ Self-Test — LEC 06

> [!question]- Q1. จุด A = (2, 3) กับ B = (5, 7) หา Euclidean, Manhattan, Minkowski q = 3
> ผลต่าง 3, 4 → Euclidean = √(9+16) = **5** · Manhattan = 3+4 = **7** · q = 3: (27+64)^(1/3) = 91^(1/3) = **4.50**

> [!question]- Q2. ทำไมนิยมเลือก k เป็นเลขคี่
> กันเสียงโหวตเสมอในปัญหา 2 คลาส (เช่น k = 4 อาจได้ 2 : 2)

> [!question]- Q3. k = 1 ได้ training error 0% แต่ validation error 33% บอกอะไร
> **overfitting** — k = 1 แต่ละจุด training เป็นเพื่อนบ้านที่ใกล้ที่สุดของตัวเอง จึงทายถูกหมดบน train แต่ไวต่อ noise บนข้อมูลใหม่

> [!question]- Q4. ทำไม KNN เรียกว่า lazy learner ข้อดีข้อเสียคืออะไร
> ไม่สร้างโมเดลตอน train แค่เก็บข้อมูล แล้วคำนวณระยะทางตอนทาย · ข้อดี: ไม่ต้องฝึก ปรับตามข้อมูลใหม่ได้ทันที · ข้อเสีย: ทายช้า ใช้หน่วยความจำ ไม่มีโมเดลให้อธิบาย

> [!question]- Q5. KNN regression k = 4 เพื่อนบ้านราคา 10, 12, 14, 20 ทายได้เท่าไร
> ค่าเฉลี่ย = 56/4 = **14**

> [!question]- Q6. ถ้าใช้ KNN กับข้อมูล 200 feature ควรทำอะไรก่อน เพราะอะไร
> **ลดมิติ** (PCA / feature selection) + scale เพราะ curse of dimensionality ทำให้ระยะทางไม่มีความหมายในมิติสูง

---

**กลับหน้าหลัก →** [[LEC 00 START HERE]] · **ถัดไป →** [[LEC 07 Linear & Logistic Regression]]
