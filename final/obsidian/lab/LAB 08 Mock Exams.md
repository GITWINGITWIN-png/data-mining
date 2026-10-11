---
title: LAB 08 · Mock Exams
exam: Lab — จ. 12 ต.ค. 2569 09:00–12:00
tags: [final, lab, mock]
---

# LAB 08 · Mock Exams
### ข้อสอบ Lab จำลอง 3 ชุด — ทำจริงจับเวลา แล้วค่อยเปิดเฉลย

**ลิงก์:** [[LAB 00 START HERE|หน้าหลัก Lab]] · ก่อนหน้า [[LAB 07 Reading & Explaining Results]] · [[LAB 09 Cheat Sheet]]

> [!important] วิธีใช้
> 1. เปิด `question.ipynb` (kernel **Python (dm-exam)**) **จับเวลา** · ห้ามเปิด `solution.ipynb` จนกว่าจะหมดเวลา
> 2. ทำทุกข้อให้ครบ **โค้ด → ผล → คำตอบ/ตีความ** (cell "คำตอบ" ใต้ทุกข้อ)
> 3. ทำส่วน RapidMiner ของชุดนั้น (สร้างเองจากศูนย์ ห้าม import เฉลยก่อน)
> 4. เทียบกับ `solution.ipynb` / `solution_*.rmp` → จดสิ่งที่พลาดลงท้ายโน้ตนี้ ([[#📝 สิ่งที่พลาด (กรอกเอง)]])
>
> ไฟล์อยู่ใน `final/mock_lab/` · ข้อมูลอยู่ใน `<mock>/data/` (สร้างด้วย `make_data.py` — seed คงที่) · **เฉลยทุกชุดรันจริงแล้ว** ตัวเลขในเฉลยตรงกับ output

| ชุด | หัวข้อ | เวลา | guideline ที่ครอบคลุม |
|---|---|---|---|
| **Mock 1** · `mock1_classification/` | ธนาคารหาลูกค้ารายได้ > 50K (adult) | 90 นาที Python + 60 นาที RapidMiner | **append + join** · pivot · charts · `?` missing · encoding · discretization · **leakage-safe pipeline** · **majority baseline** · KNN / LogReg / Tree / **RF** · CV · **optimize** · **SMOTE ใน CV** · **threshold** · เลือก metric · ทำนายคนใหม่ |
| **Mock 2** · `mock2_regression_pca/` | ราคาบ้าน (Boston) | 75 นาที | EDA · correlation + multicollinearity · **mean baseline** · Linear Regression + ตีความ coef · MAE/MSE/RMSE/R² · **KNN regressor ก่อน/หลัง scale** · optimize k · **PCA** explained variance / loadings / 2D plot |
| **Mock 3** · `mock3_cluster_assoc/` | จัดกลุ่มบริษัทไฟฟ้า + cross-sell PEP | 75 นาที | preprocessing สำหรับ clustering · **K-Means + เลือก k** (elbow/silhouette/DB) · **ตีความ centroid** · cohesion/separation · PCA plot · **discretize → items** · **Apriori** · support/confidence/lift · ผลของ min support |

> **แนะนำลำดับ:** 10 ต.ค. ทำ **Mock 1 ครบ 3 ชม.** (เสมือนสอบจริง) · 11 ต.ค. ทำ Mock 2 + Mock 3 (ฝั่ง RapidMiner เป็นหลัก เพราะเป็นจุดอ่อน)

---

## Mock 1 — เฉลยย่อ (เปิดหลังทำเสร็จ)

> [!example]- ตัวเลขสำคัญ + จุดให้คะแนนที่คาด
> **A** · work = 3,500 + 2,499 = 5,999 แถว · inner join ได้ 5,999 × 16 (key ไม่ซ้ำ) · missing: workclass 368, occupation 369, native-country 118 · > 50K = **23.9%** (ไม่สมดุล)
> **B** · ตัด person_id (id), fnlwgt (น้ำหนักสำมะโน), educational-num (**ซ้ำกับ education**), income (target) · preprocessing ใน `ColumnTransformer` → fit ในแต่ละ fold · age 4 กลุ่ม equal frequency: 4.0% → 24.5% → **37.4%** → 31.9%
> **C** (5-fold, seed 1992)
> | model | accuracy | precision | recall | F1 |
> |---|---|---|---|---|
> | Majority | 0.761 | 0 | 0 | 0 |
> | KNN k=5 | 0.816 | 0.628 | 0.569 | 0.597 |
> | LogReg | **0.848** | 0.736 | 0.571 | 0.642 |
> | Tree d=5 | 0.835 | **0.777** | 0.442 | 0.559 |
> | RF 100 | 0.841 | 0.691 | 0.609 | **0.647** |
>
> **D** · KNN best k = 25 (F1 0.613) · RF best leaf = 3 (F1 0.650) · **SMOTE:** LogReg recall 0.571 → **0.832** (F1 0.672) · **threshold 0.3:** recall **0.779**, F1 0.680
> **E** · metric = **recall** (+ F1) → LogReg + threshold 0.3 (หรือ + SMOTE) · ลูกค้าใหม่ P(> 50K) = **0.002** → ไม่เสนอ
> **RapidMiner (solution_partC.rmp, รันจริง):** Default Model accuracy 0.761 recall 0 · k-NN (k = 25) F1 0.578 · RF F1 0.629 — ต่ำกว่า Python เล็กน้อย (RF ของ RapidMiner ใช้ maximal depth 20 + criterion gini_index, z-score n−1)
> ⚠️ ต้องติ๊ก **manually set positive class = `>50K`** ใน Performance — ถ้าไม่ติ๊ก RapidMiner คิด precision/recall ให้ `<=50K` (baseline จะได้ recall = 1.0 ดูดีผิดปกติ)

## Mock 2 — เฉลยย่อ

> [!example]- ตัวเลขสำคัญ
> **A** · medv เบ้ขวา (skew 1.10) · **16 หลังที่ medv = 50** (ถูกตัดเพดาน) · top |r|: lstat −0.738, rm +0.696, ptratio −0.508 · **rad–tax r = 0.91** → multicollinearity
> **B** (test 20%)
> | model | MAE | RMSE | R² |
> |---|---|---|---|
> | Mean baseline | 7.019 | 10.304 | −0.029 |
> | LinReg 13 ตัว | 3.889 | 6.013 | 0.649 |
> | LinReg (lstat, rm) | 4.562 | 6.638 | 0.573 |
> สมการ **medv = −1.616 − 0.610·lstat + 5.050·rm** · coef ของ nox (−16.4) ใหญ่เพราะ SD ของ nox แค่ 0.116 → เทียบความสำคัญต้อง standardize
> **C** · CV RMSE: KNN raw 6.318 → **KNN scaled 4.436** (−30%) · LinReg 4.678 · best k = 6 distance → test RMSE **5.008** R² **0.757**
> **D** · PC1 47.2% · ถึง 80% ต้อง **5 PC** · eigenvalue > 1 = **3 PC** · PC1 = indus/nox/tax (+), dis (−) → "เขตอุตสาหกรรม" · บ้านราคาต่ำมี PC1 เฉลี่ย +2.24 · ราคาสูง −1.84
> **RapidMiner (รันจริง):** LinReg hold-out RMSE 5.574 (split คนละแบบกับ Python) · k-NN CV RMSE raw **6.431** → scaled **4.563** (ผลแบบเดียวกัน) · PCA keep variance 0.8

## Mock 3 — เฉลยย่อ

> [!example]- ตัวเลขสำคัญ
> **A** · ต้อง normalize (Sales 3,300–17,441 vs Fixed_charge 0.75–1.49) · silhouette สูงสุด k = 5 (0.248) รอง k = 4 (0.234) · **k = 4**: Idaho/Nevada/Puget (ขายมาก เชื้อเพลิงถูก) · Boston/NY/Hawaiian/New England/Pacific/San Diego/United (เชื้อเพลิงแพง) · Commonwealth/Madison/Northern/Wisconsin/Virginia (nuclear) · Arizona/Central/Florida/Kentucky/Oklahoma/Southern/Texas (ต้นทุนต่ำ) · บริษัทใหม่ → กลุ่มต้นทุนต่ำ · PC1+PC2 = 50.9%
> **B** · ตัด id, region, sex (50/50), current_act (75.8% YES) · 600 × 19 items · min support 0.10: 413 itemsets, 215 rules, 8 กฎ → pep=YES · อันดับ 1 **{SENIOR, income HIGH, children 1-2} → pep=YES** s 0.105 c 0.940 **lift 2.059** · min support 0.20 → **0 กฎ** ที่ทำนาย pep=YES
> **RapidMiner (รันจริง):** k-Means k = 4 (seed 1992) ได้ avg within centroid distance 3.666 / DB 1.256 — **แบ่งต่างจาก sklearn** (Boston, NY ไปอยู่กลุ่ม nuclear) = local optimum คนละจุด (sklearn ได้ 3.654 ดีกว่าเล็กน้อย) · FP-Growth + rules ได้ ~216 กฎ (ใกล้ Python 215) · ⚠️ `Nominal to Binominal` ต้องติ๊ก **transform binominal** ไม่งั้นคอลัมน์ YES/NO ไม่ถูกแปลงและ FP-Growth error

---

## 📝 สิ่งที่พลาด (กรอกเอง)

| ชุด / ข้อ | พลาดอะไร | ต้องทบทวนที่ |
|---|---|---|
| | | |
| | | |

---

**กลับหน้าหลัก →** [[LAB 00 START HERE]]
