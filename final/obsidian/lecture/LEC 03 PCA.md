---
title: LEC 03 · PCA (Dimension Reduction)
exam: Lecture — จ. 19 ต.ค. 2569 16:00–19:00
guideline: "Lecture ข้อ 2 — PCA: concept, number of components, explained variance, loadings และการใช้ PCA เพื่อ visualization"
source: 69_1_DimReduction_and_PCA.pdf (27 pp — Shmueli DMBA ch.4 Breakfast Cereals) · W13
tags: [final, lecture, pca, dimension-reduction, explained-variance, loadings]
---

# LEC 03 · PCA — Principal Component Analysis
### สร้างตัวแปรใหม่ไม่กี่ตัวที่เก็บ "ข้อมูล (ความแปรปรวน)" ไว้ได้มากที่สุด

> [!abstract] guideline: **concept · number of components · explained variance · loadings · PCA for visualization**
> → [[#3.1 แนวคิด ⭐⭐⭐]] · [[#3.2 ตัวอย่าง 2 ตัวแปร — Calories & Rating ⭐⭐⭐]] · [[#3.3 ต้อง Normalize ก่อน PCA ⭐⭐⭐⭐]] · [[#3.4 Explained Variance & จำนวน Component ⭐⭐⭐⭐]] · [[#3.5 Loadings — ตีความ PC ⭐⭐⭐]] · [[#3.6 PCA เพื่อ Visualization / Clustering / Classification ⭐⭐⭐]]

**ลิงก์:** [[LEC 00 START HERE|หน้าหลัก Lecture]] · [[LEC 02 Preprocessing, Feature Selection & Leakage]] · [[LEC 06 KNN]] (curse of dimensionality) · Lab: [[LAB 03 Preprocessing Recipes#3.6 PCA + 2D Visualization ⭐⭐⭐]] · มิดเทอม: [[04 Data Pre-processing#Feature Reduction / PCA]]

---

## 3.1 แนวคิด ⭐⭐⭐

> [!quote] สไลด์ PCA p.7–9, 15
> **"PCA finds new variables (principal components) that capture MAXIMUM VARIANCE in the data."**
> **"The new variables are LINEAR COMBINATIONS of the original variables, are UNCORRELATED, and are RANKED by variance explained."**
> **"Information" = total variance** (ผลรวมความแปรปรวนของทุกตัวแปร) · *"Usually the first few Z variables contain most of the information, and so the rest can be dropped."*

> [!important] ⭐ 4 คุณสมบัติของ PC (p.14)
> 1. $Z_i = a_{i1}X_1 + a_{i2}X_2 + \dots + a_{ip}X_p$ — **weights $a$ = loadings**
> 2. **Var(Z₁) ≥ Var(Z₂) ≥ …** — PC1 เก็บความแปรปรวนมากที่สุด
> 3. **PC ไม่สัมพันธ์กัน** (corr(Z₁, Z₂) = 0) → แก้ปัญหา multicollinearity ได้
> 4. **ผลรวม Var(Z) = ผลรวม Var(X) เดิม** (ข้อมูลไม่หาย แค่หมุนแกน) — ใช้ PC ทั้งหมด = ข้อมูลเดิมครบ

**ทำไมต้องลดมิติ** (มิดเทอม 4.8): curse of dimensionality · ลดเวลา/หน่วยความจำ · **มองภาพได้ (2D/3D)** · ลด noise · ลด redundancy

> 📚 **กลไกทางคณิตศาสตร์** (สไลด์ไม่ได้ให้สูตร — Jolliffe; scikit-learn §2.5):
> 1. center ข้อมูล (ลบค่าเฉลี่ย) [+ หาร SD ถ้า standardize]
> 2. covariance matrix $\Sigma=\frac{1}{n-1}X^\top X$
> 3. eigen-decomposition $\Sigma v=\lambda v$ → **eigenvector $v$ = loadings** · **eigenvalue $\lambda$ = variance ของ PC นั้น**
> 4. **explained variance ratio** $=\lambda_i/\sum_j\lambda_j$ · score $=X_{\text{centered}}\,v$

---

## 3.2 ตัวอย่าง 2 ตัวแปร — Calories & Rating ⭐⭐⭐

> [!example] ⭐ Breakfast Cereals (p.10–14)
> Var(calories) = **379.63** · Var(rating) = **197.32** → total ≈ 577 → calories มีส่วน **379.63/577 = 66%**
> **ผล PCA (p.12):**
> | | Z1 | Z2 |
> |---|---|---|
> | weight: calories | **−0.847** | 0.532 |
> | weight: rating | **0.532** | 0.847 |
> | Variance | **498.02** | 78.93 |
> | Variance % | **86.32%** | 13.68% |
> → Z1 ตัวเดียวเก็บได้ **86%** (มากกว่าตัวแปรเดิมตัวไหน ๆ ที่เก็บได้แค่ 66%) · 498 + 79 = 577 (variance เท่าเดิม)
> **ตีความ:** Z1 = −0.847·calories + 0.532·rating → **Z1 สูง = แคลอรีต่ำ + rating สูง** (ซีเรียลสุขภาพที่คนชอบ)
> **scores (p.13):** 100%_Bran 44.92 · All-Bran_with_Extra_Fiber **75.31** (สูงสุด — แคลอรีต่ำ rating สูง) · Basic_4 −22.57

> [!example]- 🧮 PCA ด้วยมือ 2×2 (📚 drill — คำนวณยืนยันแล้ว)
> covariance matrix $\begin{bmatrix}10 & 5\\ 5 & 5.2\end{bmatrix}$ · eigenvalue หาจาก $\lambda^2-15.2\lambda+(52-25)=0$
> → $\lambda=\frac{15.2\pm\sqrt{231.04-108}}{2}=\frac{15.2\pm11.09}{2}$ → **λ₁ = 13.15, λ₂ = 2.05**
> explained: PC1 = 13.15/15.2 = **86.5%** · PC2 = **13.5%** · eigenvector PC1 ≈ (0.846, 0.533) (เครื่องหมายกลับได้)

---

## 3.3 ต้อง Normalize ก่อน PCA ⭐⭐⭐⭐

![[lec_pca_scree.png]]

> [!warning] ⭐⭐ กับดักอันดับ 1 ของ PCA (p.16–17)
> **ไม่ normalize (13 ตัวแปร):** PC1 ≈ **sodium** (loading 0.98) · PC2 ≈ **potassium** (0.99) · 2 PC แรก = **92.78%** — ดูดีแต่หลอก!
> → เพราะ sodium/potassium วัดเป็น **mg** (ค่าหลักร้อย variance หลักพัน) ขณะที่ตัวอื่นเป็นกรัม → PCA "เห็น" แค่ตัวแปรที่หน่วยใหญ่
> สไลด์ p.17: *"Normalize: divide by std. deviation (may subtract mean first)"* · *"RapidMiner: use correlation matrix option to use normalized variables"*
>
> **standardize แล้ว (p.18):** variance % = 27.66 · 24.34 · 14.35 · 8.40 · 7.46 · 5.56 → สะสม 27.66 → 51.99 → 66.35 → 74.75 → **82.20** → 87.77
> → *"First component accounts for smaller part of variance; need more components"* · ต้องใช้ **5 PC** ถึง 80%
>
> **Wine data (p.20–21) ยืนยันซ้ำ:** ไม่ normalize → PC1 = **Proline** (loading 1.000, SD 351.5) อธิบาย **99.83%** — ตัวแปรเดียวครองหมด

> [!tip] standardize = PCA บน **correlation matrix** · ไม่ standardize = PCA บน **covariance matrix**
> หลัง standardize ทุกตัวแปรมี variance = 1 → total variance = จำนวนตัวแปร (13) → eigenvalue/13 = % explained (เช่น 3.595/13 = 27.66%)

---

## 3.4 Explained Variance & จำนวน Component ⭐⭐⭐⭐

| เกณฑ์เลือกจำนวน PC | วิธี | cereals (standardized) |
|---|---|---|
| **Cumulative explained variance** | เก็บ PC จนสะสม ≥ 80–90% | 80% → **5 PC** · 87.77% → 6 PC |
| 📚 **Kaiser rule** | เก็บ PC ที่ eigenvalue > 1 (เมื่อ standardize — ดีกว่าตัวแปรเดิม 1 ตัว) | 3.60, 3.16, 1.87, 1.09 → **4 PC** |
| 📚 **Scree plot (elbow)** | หาจุดที่กราฟ % variance หักลงแล้วแบน | — |
| **ตามงาน** | visualization → **2 PC** · ทำโมเดล → เลือกด้วย **CV** (W13 ได้ 8) | — |

> [!quote] Best practices (p.27)
> **"Standardize data before applying PCA · Interpretability of PCs can be difficult · DON'T ALWAYS RELY ON FIRST TWO PCs — CHECK EXPLAINED VARIANCE · Combine with domain knowledge"**

---

## 3.5 Loadings — ตีความ PC ⭐⭐⭐

> [!example] ⭐ PC1 ของ cereals (standardized, p.19)
> loading: calories **+0.324** · cups **+0.279** · protein **−0.302** · fiber **−0.440** · potass **−0.383** · rating **−0.453**
> สไลด์: **"High scores on PC-1 mean that the cereal is HIGH in calories and the amount per bowl, and LOW in protein, fiber, and potassium. And, with a LOW consumer rating."**
> **PC-2** most affected by **weight of a serving** (0.435) · **PC-3** by **carbohydrate** (0.564)

> [!important] วิธีตีความ loadings
> 1. ดู **|loading| ที่ใหญ่** (เช่น > 0.3) ของแต่ละ PC
> 2. **เครื่องหมายเดียวกัน** = เคลื่อนไปทางเดียวกัน · **ตรงข้าม** = ขัดกัน
> 3. ตั้งชื่อ PC ตามกลุ่มตัวแปรนั้น (W13: PC1 = Age + Experience → "ความอาวุโส")
> 4. ⚠️ **เครื่องหมายทั้ง PC กลับด้านได้** (Python vs RapidMiner) — ความหมายเท่าเดิม

---

## 3.6 PCA เพื่อ Visualization / Clustering / Classification ⭐⭐⭐

| การใช้ | วิธี | สไลด์ |
|---|---|---|
| **Visualization (EDA)** | scatter **PC1 vs PC2** ระบายสีตามคลาส/กลุ่ม — *"Plot PC1 vs PC2 to uncover structure"* | p.5–6, 22 |
| **PCA ก่อน K-Means** (Alternative 1) | standardize → PCA 2–3 PC → K-Means → plot · ✅ ลด noise เห็นภาพง่าย · ❌ อาจเสียการตีความ | p.24 |
| **PCA หลัง K-Means** (Alternative 2) | K-Means บนข้อมูลเต็ม → PCA **เฉพาะเพื่อวาด/อธิบาย** กลุ่ม · ✅ กลุ่มใช้ข้อมูลครบ · ❌ ไม่ช่วยลด noise | p.25 |
| **Classification** | PCA เป็น feature ให้ KNN/LogReg (แก้ curse of dimensionality + multicollinearity) | p.26 |

> [!warning] PCA กับ data leakage (W13 Part III vs IV)
> - **ใช้ทำโมเดล:** PCA ต้อง **fit ใน training fold** แต่ละรอบ (อยู่ใน Pipeline / Training pane) — *"Explain why PCA must be learned separately inside every training fold"*
> - **ใช้ visualize:** fit กับข้อมูลทั้งชุดได้ เพราะเป็น descriptive — *"not an unbiased performance estimate"*

> [!example] W13 ของคุณ (Personal Loan, 11 predictors, standardized)
> PC1 **18.62%** · PC2 **16.88%** · สะสม **35.50%** → ภาพ 2D เก็บได้แค่ 1/3 · PC1 = Age/Experience/Income · PC2 = Income/CCAvg/Experience · PCA + KNN (8 comp) F1 0.755 < KNN ไม่ใช้ PCA 0.771 → **PCA ไม่ช่วย** (ข้อมูลไม่ได้มีมิติสูงขนาดนั้น)

---

## ✅ Self-Test — LEC 03

> [!question]- Q1. PCA ไม่ normalize แล้ว PC1 อธิบาย 99% และ loading ของ Proline = 1.0 สรุปว่า Proline สำคัญที่สุดได้ไหม
> **ไม่ได้** — Proline มีหน่วย/SD ใหญ่สุด (351.5) PCA บน covariance จึงถูกครอบงำโดยตัวแปรนั้น · ต้อง standardize ก่อนแล้วดู PCA ใหม่

> [!question]- Q2. eigenvalues (standardized, 6 ตัวแปร) = 2.4, 1.5, 0.9, 0.6, 0.4, 0.2 หา % ของ PC1, จำนวน PC ตาม Kaiser และตาม 80%
> total = 6 · PC1 = 2.4/6 = **40%** · Kaiser (> 1): **2 PC** · สะสม 40 → 65 → 80% → **3 PC**

> [!question]- Q3. ทำไม PC ถึงไม่สัมพันธ์กัน และเป็นประโยชน์อย่างไรกับ regression
> PC ถูกสร้างให้ตั้งฉากกัน (eigenvector ของ covariance matrix) → corr = 0 → ใช้เป็น predictor ได้โดยไม่มี multicollinearity

> [!question]- Q4. ข้อเสียหลักของการใช้ PC แทนตัวแปรเดิม
> **ตีความยาก** — PC เป็นผลรวมถ่วงของทุกตัวแปร ไม่มีหน่วยจริง (p.27) · และเป็นวิธี unsupervised ไม่รับประกันว่า PC ที่ variance สูงจะช่วยทำนาย label

> [!question]- Q5. PCA ก่อน กับ หลัง K-Means ต่างกันอย่างไร
> ก่อน: clustering บน PC (ลด noise/มิติ แต่ตีความกลุ่มยากขึ้น) · หลัง: clustering บนข้อมูลเต็ม แล้วใช้ PCA แค่วาดภาพอธิบาย

---

**กลับหน้าหลัก →** [[LEC 00 START HERE]] · **ถัดไป →** [[LEC 04 Imbalanced Classification]]
