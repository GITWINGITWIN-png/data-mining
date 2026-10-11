---
title: LAB 07 · Reading & Explaining Results
exam: Lab — จ. 12 ต.ค. 2569 09:00–12:00
guideline: "Lab › อ่านและอธิบายผลลัพธ์จากกราฟ ตาราง และ evaluation metrics"
tags: [final, lab, interpretation]
---

# LAB 07 · Reading & Explaining Results
### อ่านผลให้เป็น → เขียนคำอธิบายที่ได้คะแนน

> [!quote] guideline: *"ข้อสอบจะเน้นทั้ง ความเข้าใจในแนวคิด การเลือกวิธีที่เหมาะสม การสร้าง workflow อย่างถูกต้อง และ**การตีความผล** ไม่ใช่เพียงการจำคำสั่งหรือ syntax เท่านั้น"*
> → คะแนนส่วนใหญ่ไม่ได้อยู่ที่ "รันได้" แต่อยู่ที่ **"อธิบายได้ว่าตัวเลขนี้แปลว่าอะไร และจึงเลือกอะไร"**

**ลิงก์:** [[LAB 00 START HERE|หน้าหลัก Lab]] · ก่อนหน้า [[LAB 06 Clustering & Association]] · ถัดไป [[LAB 08 Mock Exams]] · ประโยคสำเร็จรูป: [[LAB 09 Cheat Sheet#6. ประโยคตีความสำเร็จรูป]]

## โครงคำตอบ 4 ขั้น (ใช้กับทุกผล)

> [!important] **ตัวเลข → เทียบ → เหตุผล → ข้อสรุป/การตัดสินใจ**
> 1. **ตัวเลข:** อ้างค่าจริง (อย่าเขียน "ดีขึ้น" เฉย ๆ) — *"F1 = 0.880"*
> 2. **เทียบ:** กับ baseline / โมเดลอื่น / ก่อน-หลัง — *"สูงกว่า KNN ที่ไม่ scale (0.702) 0.178"*
> 3. **เหตุผล:** ทำไมถึงเป็นแบบนั้น (เชื่อมกับแนวคิด) — *"เพราะ KNN ใช้ระยะทาง และ Salary มีสเกลใหญ่"*
> 4. **ข้อสรุป:** เลือกอะไร / แนะนำอะไร / ข้อจำกัด — *"จึงเลือก KNN + StandardScaler · ข้อจำกัด: ทดสอบบนข้อมูล 400 แถว"*

---

## 7.1 Confusion matrix

**ตัวอย่าง (KNN, 10-fold CV, Social Network Ads):**

| | pred 0 | pred 1 |
|---|---|---|
| **actual 0** | TN = 236 | FP = 21 |
| **actual 1** | FN = 14 | TP = 129 |

- **อ่าน:** ทายถูก 236 + 129 = 365/400 = **91.25%** · พลาด 2 แบบ: **FP = 21** (ทายว่าซื้อแต่ไม่ซื้อ = เสียงบโฆษณา) · **FN = 14** (คนจะซื้อแต่โมเดลพลาด = เสียโอกาสขาย)
- **precision** (คลาส 1) = 129/(129+21) = **0.860** · **recall** = 129/(129+14) = **0.902**
- **เขียน:** *"โมเดลหาคนที่จะซื้อเจอ 90.2% (recall) และในคนที่ทายว่าซื้อ ถูกจริง 86.0% (precision) · ความผิดพลาดหลักคือ FP 21 ราย ถ้าค่าโฆษณาต่อคนสูง ควรเพิ่ม threshold"*
- ⚠️ **RapidMiner** เรียง *แถว = pred., คอลัมน์ = true* — อ่านหัวตารางก่อนทุกครั้ง · มีแถว **class precision** และคอลัมน์ **class recall** ให้เลย

## 7.2 classification_report

```
              precision    recall  f1-score   support
           0      0.944     0.918     0.931       257
           1      0.860     0.902     0.881       143
    accuracy                          0.912       400
   macro avg      0.902     0.910     0.906       400
weighted avg      0.914     0.912     0.913       400
```
- **แถว 0 / 1** = metric เมื่อถือว่าคลาสนั้นเป็น positive · **support** = จำนวนจริงของคลาสนั้น (257 : 143 → ไม่สมดุลเล็กน้อย)
- **macro avg** = ค่าเฉลี่ยธรรมดาของสองคลาส (ให้คลาสเล็กมีน้ำหนักเท่าคลาสใหญ่) · **weighted avg** = ถ่วงด้วย support (ใกล้ accuracy)
- ข้อมูลไม่สมดุล → **รายงานแถวของคลาสส่วนน้อย/คลาสที่สนใจ** ไม่ใช่ weighted avg

## 7.3 ผล Cross Validation (mean ± std)

- **RapidMiner:** `accuracy: 90.50% +/- 6.10% (micro average: 90.50%)` · **Python:** `test_accuracy` 10 ค่า → mean, std
- **อ่าน:** mean = ประสิทธิภาพที่คาดหวังบนข้อมูลใหม่ · **std** = ความผันผวนระหว่าง fold (ข้อมูลน้อย → std สูง)
- **เทียบสองโมเดล:** ถ้าต่างกัน **น้อยกว่า std** → *"แทบไม่ต่างกันทางปฏิบัติ"* → เลือกตัวที่ง่าย/เร็วกว่า

## 7.4 ตาราง Grid search / Optimize Parameters

| k | F1 (RapidMiner) |
|---|---|
| 1 | 0.799 |
| 5 | 0.871 |
| **11** | **0.880** |
| 15 | 0.869 |

- **k เล็กมาก (1)** → F1 ต่ำ เพราะไวต่อ noise (overfit) · **k ใหญ่** → เริ่มลดลง เพราะ "เรียบเกินไป" (underfit) · **ค่าดีที่สุดอยู่ตรงกลาง** (สไลด์ KNN p.38)
- **เขียน:** *"F1 เพิ่มจาก 0.799 (k=1) และคงที่ราว 0.87–0.88 ในช่วง k = 5–13 → เลือก k = 11 ที่ F1 สูงสุด แต่ค่าใกล้เคียงหลายค่า แสดงว่าโมเดลไม่ไวต่อ k ในช่วงนี้"*

## 7.5 Train vs CV (overfitting)

| max_depth | 2 | 4 | 8 | โตเต็ม |
|---|---|---|---|---|
| train | 0.916 | 0.931 | 0.976 | **0.998** |
| CV | **0.908** | 0.873 | 0.860 | 0.848 |

- **อ่าน:** train ↑ เรื่อย ๆ แต่ CV ลดหลัง depth 2 → **ช่องว่างกว้างขึ้น = overfitting** (สไลด์ Tree p.51 *"test error increases while training error steadily decreases"*)
- train และ CV **ต่ำทั้งคู่** → underfitting (โมเดลง่ายเกิน)

## 7.6 Coefficient table

**Linear Regression:** `medv = −3.841 − 0.633·lstat + 5.465·rm`
- เครื่องหมาย = ทิศ · ขนาด = เปลี่ยนกี่หน่วยของ y ต่อ 1 หน่วย x **โดยตัวอื่นคงที่**
- RapidMiner ให้ **p-Value**: < 0.05 = มีนัยสำคัญ → ตัวแปรช่วยอธิบาย y จริง · p สูง → พิจารณาตัดออก (ทวน [[09 Regression Analysis#9.6 Multiple Linear Regression ⭐⭐]])
- เทียบ "ความสำคัญ" ระหว่างตัวแปร ต้องใช้ **standardized coefficient** (หน่วยต่างกันเทียบตรง ๆ ไม่ได้)

**Logistic Regression:** coef (ต่อ 1 SD): Age 2.197 → **odds ratio 9.0**
- *"อายุเพิ่ม 1 SD odds ของการซื้อเพิ่ม 9 เท่า โดยตัวแปรอื่นคงที่"* · OR < 1 = ลดโอกาส · OR ≈ 1 = ไม่มีผล

## 7.7 Decision Tree / Feature importance

- **อ่าน tree:** root = feature ที่ลด impurity มากที่สุด · แต่ละ leaf = 1 กฎ IF–THEN · ตัวเลขใน leaf = จำนวนแถวแต่ละคลาส → ความมั่นใจ
- **feature importance** (รวมเป็น 1): Age 0.52 · EstimatedSalary 0.47 · Gender 0.01 → *"Gender แทบไม่มีผลต่อการตัดสินใจซื้อ"*
- ⚠️ importance บอก "ใช้มากแค่ไหน" ไม่บอก **ทิศทาง** (ต่างจาก coefficient)

## 7.8 PCA

| | PC1 | PC2 |
|---|---|---|
| explained variance | 18.6% | 16.9% |
| cumulative | 18.6% | **35.5%** |
| loading สูงสุด | Age 0.62, Experience 0.62 | Income 0.53, CCAvg 0.50 |

- **อ่าน:** 2 PC เก็บข้อมูลได้แค่ **35.5%** → ภาพ 2D ไม่ได้แสดงข้อมูลทั้งหมด · PC1 ≈ "อายุ/ประสบการณ์" · PC2 ≈ "รายได้/การใช้บัตร"
- scatter สีตาม label: คลาสแยกกันตามแกนไหน → แกนนั้นสัมพันธ์กับ label · ถ้าทับกันมาก **ไม่ได้แปลว่าแยกไม่ได้** (อาจแยกได้ในมิติอื่น)
- เครื่องหมาย loading กลับด้านได้ระหว่าง Python กับ RapidMiner (PC1 = −0.622·Age) — ความหมายเหมือนเดิม

## 7.9 Elbow / Silhouette / Centroid table

- **Elbow:** หา k ที่ WCSS "เริ่มแบน" — ห้ามเลือก k ที่ WCSS ต่ำสุด (ต่ำสุดเสมอที่ k = n)
- **Silhouette:** −1…1 · ยิ่งสูงยิ่งดี (> 0.5 แยกชัด, 0.2–0.5 พอใช้, < 0.2 ซ้อนกัน) · Utilities ได้สูงสุด 0.248 ที่ k = 5 → *"กลุ่มซ้อนกันพอสมควร"*
- **Davies–Bouldin:** ต่ำ = ดี (RapidMiner แสดงติดลบ)
- **Centroid table (z-score):** หา |z| > ~0.8 ของแต่ละกลุ่ม → ตั้งชื่อกลุ่ม → แนะนำธุรกิจ (ดูตัวอย่าง 4 กลุ่ม Utilities ใน [[LAB 06 Clustering & Association#ตีความ centroid — หัวใจของโจทย์ clustering ⭐⭐⭐]])
- **cohesion** (ใกล้กันในกลุ่ม: WCSS, avg within centroid distance ต่ำ) + **separation** (ห่างระหว่างกลุ่ม: ระยะ centroid ไกล) + **interpretability** (อธิบายได้) = 3 เกณฑ์ของ guideline

## 7.10 Association rules table

| Premises → Conclusion | Support | Confidence | Lift |
|---|---|---|---|
| Eye_Enhancer → Eye_Palette | 0.321 | 0.899 | 2.360 |
| Glossy_Lips → Base_Makeup | 0.356 | 0.727 | 1.355 |

- เรียงด้วย **lift** (ความสัมพันธ์จริง) ไม่ใช่แค่ confidence
- กฎสองทิศ (A→B และ B→A) มี **support และ lift เท่ากัน** แต่ **confidence ต่างกัน** (หารด้วย support ของฝั่งซ้าย)
- **เขียน:** support = ครอบคลุมกี่ % ของทุก transaction · confidence = ในคนซื้อ X กี่ % ซื้อ Y · lift = เทียบกับโอกาสทั่วไปกี่เท่า → **ข้อเสนอ** (bundle, วางใกล้กัน, แนะนำสินค้า)

## 7.11 Regression metrics

| | MAE | MSE | RMSE | R² |
|---|---|---|---|---|
| Mean baseline | 6.256 | 75.045 | 8.663 | −0.023 |
| Linear Regression | 3.189 | 24.291 | 4.929 | 0.669 |

- *"Linear Regression ทายราคาพลาดเฉลี่ย 3.19 พันดอลลาร์ (MAE) ดีกว่าการทายค่าเฉลี่ยทุกหลัง (6.26) ราวครึ่งหนึ่ง · อธิบายความแปรปรวนได้ 66.9%"*
- RMSE > MAE มาก → มี error ก้อนใหญ่บางแถว (outlier) · R² ของ mean baseline ≈ 0 (บน test ติดลบได้)

---

## 🏋️ Drills — เขียนตีความเองก่อนดูเฉลย

> [!question]- D1. โมเดล A: accuracy 0.86, recall 0.40 · โมเดล B: accuracy 0.80, recall 0.75 (ข้อมูล churn 26% churn) ธนาคารต้องการ "รักษาลูกค้าที่จะยกเลิกให้ได้มากที่สุด" เลือกตัวไหน
> **B** — เป้าหมายคือหา churn ให้เจอ (ลด FN) → metric หลักคือ **recall** · A มี accuracy สูงกว่าแต่หาคน churn เจอแค่ 40% · accuracy 0.86 ของ A สูงกว่า majority baseline (0.74) ไม่มาก · ควรรายงาน precision ของ B ด้วย เพื่อดูต้นทุนแคมเปญที่ส่งให้คนไม่ churn

> [!question]- D2. PCA: PC1 explained 0.62 · loading: Income 0.71, Spending 0.69, Age 0.05 เขียนตีความ
> *"PC1 อธิบายความแปรปรวนได้ 62% และถูกขับเคลื่อนโดย Income กับ Spending (loading ≈ 0.7 ทิศเดียวกัน) เกือบเท่ากัน ส่วน Age แทบไม่มีผล → PC1 คือ 'กำลังซื้อ' ลูกค้าที่ค่า PC1 สูงมีทั้งรายได้และการใช้จ่ายสูง"*

> [!question]- D3. RapidMiner แสดง `Davies Bouldin: -0.904` (k = 6) และ `-1.177` (k = 4) k ไหนดีกว่าตาม DB
> RapidMiner คูณ −1 ให้ → ค่าจริง 0.904 vs 1.177 · DB **ต่ำ = ดี** → **k = 6** ดีกว่าตาม DB · แต่ต้องดู interpretability ประกอบ (k = 6 มีกลุ่มสมาชิก 1 ตัวสองกลุ่ม = NY, San Diego อาจเป็น outlier)

> [!question]- D4. tree ได้ train 0.99 CV 0.85 · RF ได้ train 0.99 CV 0.90 · logistic ได้ train 0.84 CV 0.83 เขียนสรุป
> tree เดี่ยว overfit (ช่องว่าง 0.14) · RF ลด overfitting จากการรวมหลายต้น ได้ CV ดีที่สุด 0.90 · logistic ไม่ overfit (train ≈ CV) แต่ CV ต่ำกว่า → อาจ underfit เพราะความสัมพันธ์ไม่เป็นเชิงเส้น · **เลือก RF** (ถ้าต้องการอธิบายง่าย ใช้ tree ที่ prune แล้วแทนได้)

---

**ถัดไป →** [[LAB 08 Mock Exams]] · **กลับหน้าหลัก →** [[LAB 00 START HERE]]
