---
title: LEC 13 · Exam Drills
exam: Lecture — จ. 19 ต.ค. 2569 16:00–19:00
tags: [final, lecture, drills, practice]
---

# LEC 13 · Exam Drills
### ฝึกครบทุกรูปแบบ (ไม่รู้รูปแบบข้อสอบจริง) — ทำก่อน แล้วค่อยกดเปิดเฉลย

> [!tip] วิธีใช้ — **18 ต.ค. ทำแบบจับเวลา 2 ชม.** (A 20 นาที · B 50 นาที · C 25 นาที · D 15 นาที · E 10 นาที) แล้วจดข้อที่พลาดท้ายหน้า
> **Part A** แนวคิด/ตัวเลือก · **Part B** คำนวณแสดงวิธีทำ · **Part C** อ่านตาราง/กราฟ · **Part D** สถานการณ์ · **Part E** หาที่ผิด · ท้ายหน้า: **กับดัก 15 ข้อ**
> เฉลยทุกข้อคำนวณยืนยันด้วยสคริปต์ (`final/obsidian/scripts/lec_numbers.py`)

**ลิงก์:** [[LEC 00 START HERE|หน้าหลัก Lecture]] · [[LEC 11 Formula Sheet]] · [[LEC 12 Glossary EN-TH]]

---

## Part A · แนวคิด / ตัวเลือก

> [!question]- A1. ข้อใดเป็น unsupervised learning: (ก) KNN (ข) Logistic Regression (ค) K-Means (ง) Random Forest
> **(ค) K-Means** — ไม่มี label · อีกสามข้อเป็น supervised

> [!question]- A2. ข้อใด **ไม่** จำเป็นต้อง scale ก่อน: (ก) KNN (ข) K-Means (ค) PCA (ง) Decision Tree
> **(ง)** — tree แบ่งด้วย threshold ทีละ feature (Tree p.70)

> [!question]- A3. "k = n ใน KNN เท่ากับอะไร"
> **naïve rule** — ทายคลาสส่วนมากทุกแถว = majority baseline (KNN p.39)

> [!question]- A4. hold-out เหมาะกับข้อมูลแบบไหน ทำไม
> ข้อมูล **มาก** — train และ test จะมีการกระจายคล้ายกัน (Tree p.73) · ข้อมูลน้อยใช้ k-fold / LOOCV

> [!question]- A5. ค่า Gini และ Entropy สูงสุดของปัญหา 2 คลาส และเกิดเมื่อใด
> Gini **0.5** · Entropy **1** · เมื่อคลาสกระจาย **50:50**

> [!question]- A6. ทำไม Information Gain ถึงชอบ attribute ที่มีค่าไม่ซ้ำเยอะ (เช่น ID) และอะไรแก้
> แบ่งจนลูกแทบ pure → IG สูงโดยไม่ generalize · **Gain Ratio** (หาร SplitInfo)

> [!question]- A7. Random Forest ทำให้ต้นไม้แต่ละต้นแตกต่างกันด้วย 2 วิธีอะไร
> **bootstrap sample** (สุ่มแถวแบบใส่คืน) + **สุ่ม feature บางส่วนในแต่ละ split**

> [!question]- A8. ลด threshold ของ logistic regression จาก 0.5 เป็น 0.2 → recall / precision เปลี่ยนอย่างไร
> recall **↑** · precision มัก **↓**

> [!question]- A9. odds ratio = 1 แปลว่าอะไร
> ตัวแปรนั้น **ไม่มีผล** ต่อ odds (coef = 0)

> [!question]- A10. PCA: PC ต่างกันเป็น "uncorrelated" หมายความว่า และมีประโยชน์อะไร
> corr ระหว่าง PC = 0 → ไม่มี multicollinearity เมื่อใช้เป็น predictor

> [!question]- A11. ทำไมต้อง standardize ก่อน PCA
> PCA หาทิศที่ variance สูงสุด → ตัวแปรหน่วยใหญ่ (sodium mg, Proline) ครอง PC1 (PCA p.16, 21)

> [!question]- A12. SMOTE สร้างข้อมูลใหม่อย่างไร
> เลือกจุด minority → หา k เพื่อนบ้าน minority → สุ่ม 1 ตัว → สร้างจุดบนเส้นระหว่างสองจุด ($X_i+\lambda(\bar X_i-X_i)$)

> [!question]- A13. ข้อเสียของ random oversampling และ random undersampling
> ROS: copy ซ้ำ → **overfitting** · RUS: ทิ้งข้อมูล → **miss important concepts** ของ majority (Imbalanced p.16)

> [!question]- A14. Apriori principle คืออะไร
> **subset ของ frequent itemset ต้อง frequent** ⟺ superset ของ itemset ที่ไม่ frequent ไม่ frequent → prune candidate

> [!question]- A15. lift = 0.8 หมายความว่า
> X กับ Y สัมพันธ์ **เชิงลบ** — ซื้อ X แล้วมีโอกาสซื้อ Y **น้อยกว่า** คนทั่วไป 20%

> [!question]- A16. cohesion กับ separation ของ clustering คืออะไร อยากได้ค่าแบบไหน
> cohesion = ความแน่นในกลุ่ม (WCSS ต่ำ) · separation = ความห่างระหว่างกลุ่ม (สูง)

> [!question]- A17. ทำไม elbow ถึงห้ามเลือก k ที่ WCSS ต่ำสุด
> WCSS ลดลงเสมอเมื่อ k เพิ่ม จน k = n → 0 → ต้องดูจุดที่การลดเริ่มแบน

> [!question]- A18. data leakage คืออะไร ยกตัวอย่าง 2 แบบ
> ใช้ข้อมูลนอก training (เช่นจาก test/อนาคต) สร้างโมเดล · ① scale ทั้งชุดก่อน split ② SMOTE ก่อน CV (หรือ tune ด้วย test, target leakage)

---

## Part B · คำนวณ (แสดงวิธีทำ)

> [!question]- B1. KNN k = 3 (ดู scaling) — training: (25,40,N) (35,60,N) (45,80,N) (20,20,N) (35,120,N) (52,18,N) (23,95,Y) (40,62,Y) (60,100,Y) (48,220,Y) [age, income] · ลูกค้าใหม่ (48, 142) · ทายด้วย (ก) ค่าดิบ (ข) min-max
> **(ก) Euclidean ดิบ** 3 ใกล้สุด: (35,120,N) **25.55** · (60,100,Y) **43.68** · (23,95,Y) **53.24** → Y 2 : N 1 → **Y**
> **(ข) min-max** (age: min 20 max 60 · income: min 18 max 220) → ลูกค้าใหม่ = ((48−20)/40, (142−18)/202) = **(0.700, 0.614)**
> 3 ใกล้สุด: (45,80,N) **0.316** · (35,120,N) **0.343** · (60,100,Y) **0.365** → N 2 : Y 1 → **N**
> **คำตอบพลิก** — income ช่วงกว้าง (18–220) ครองระยะทางเมื่อไม่ scale

> [!question]- B2. KNN regression k = 3 เพื่อนบ้าน (d = 0.5, y = 10) · (d = 1.0, y = 16) · (d = 2.0, y = 22) หา ŷ แบบธรรมดาและแบบถ่วง 1/d
> ธรรมดา: (10 + 16 + 22)/3 = **16** · ถ่วง: w = 2, 1, 0.5 → (20 + 16 + 11)/3.5 = 47/3.5 = **13.43**

> [!question]- B3. node มี 6 Yes / 4 No แบ่งเป็น A (4 Yes, 0 No) และ B (2 Yes, 4 No) หา Entropy parent, IG, SplitInfo, Gain Ratio, Gini gain
> H(parent) = −0.6 log₂0.6 − 0.4 log₂0.4 = **0.971** · H(A) = 0 · H(B) = H(⅓, ⅔) = **0.918**
> IG = 0.971 − (4/10·0 + 6/10·0.918) = 0.971 − 0.551 = **0.420**
> SplitInfo = H(0.4, 0.6) = **0.971** → GR = 0.420/0.971 = **0.433**
> Gini(parent) = 1 − 0.36 − 0.16 = **0.48** · Gini(B) = 1 − 1/9 − 4/9 = 0.444 → Gini_split = 0.6·0.444 = **0.267** → gain = **0.213**

> [!question]- B4. Weather (9 P, 5 N): Outlook แบ่งเป็น sunny (2P, 3N), overcast (4P, 0N), rain (3P, 2N) หา Gain(Outlook) และ Gain Ratio
> H(S) = **0.940** · H(sunny) = H(rain) = **0.971** · H(overcast) = 0
> E = 5/14·0.971 + 0 + 5/14·0.971 = **0.694** → **Gain = 0.247**
> SplitInfo = H(5/14, 4/14, 5/14) = **1.577** → GR = **0.156**

> [!question]- B5. (สไลด์ Tree p.41) parent (6, 6) แบ่งเป็น N1 (5, 2), N2 (1, 4) หา Gini split และ gain
> Gini(N1) = 1 − (5/7)² − (2/7)² = 1 − 0.510 − 0.082 = **0.408** · Gini(N2) = 1 − 0.04 − 0.64 = **0.320**
> split = 7/12·0.408 + 5/12·0.320 = **0.371** · gain = 0.5 − 0.371 = **0.129** (สไลด์พิมพ์ 0.194 / 0.528 / 0.333 — ผิด)

> [!question]- B6. Fraud: TN = 950, FP = 30, FN = 15, TP = 5 หา accuracy, precision, recall, F1 (fraud) และ accuracy ของ majority baseline
> accuracy = 955/1000 = **0.955** · precision = 5/35 = **0.143** · recall = 5/20 = **0.25** · F1 = 10/55 = **0.182**
> baseline (ทาย legit ทั้งหมด) = 980/1000 = **0.98** → โมเดลแพ้ baseline ด้าน accuracy แต่ baseline จับ fraud ได้ 0

> [!question]- B7. 10 แถว (actual, P(1)): (1, .92) (1, .81) (0, .74) (1, .66) (0, .55) (1, .42) (0, .35) (1, .31) (0, .18) (0, .07) หา confusion matrix และ metric ที่ threshold 0.5 และ 0.3
> **t = 0.5:** ทาย 1 = .92, .81, .74, .66, .55 → TP 3 · FP 2 · FN 2 · TN 3 → acc **0.6** · P **0.6** · R **0.6** · F1 **0.6**
> **t = 0.3:** ทาย 1 = 8 แถวแรก → TP 5 · FP 3 · FN 0 · TN 2 → acc **0.7** · P **0.625** · R **1.0** · F1 **0.769**

> [!question]- B8. logistic: ln(p/(1−p)) = −4 + 0.05·Income + 0.8·Married · คน Income = 60, Married = 1 หา z, p, คลาส (t = 0.5) และ odds ratio ของสองตัวแปร
> z = −4 + 3 + 0.8 = **−0.2** · p = 1/(1 + e^{0.2}) = **0.450** → **คลาส 0**
> OR(Income) = e^{0.05} = **1.051** (+5.1% odds ต่อ 1 หน่วย) · OR(Married) = e^{0.8} = **2.23**

> [!question]- B9. y = 3, 5, 2.5, 7 · ŷ = 2.5, 5, 4, 8 หา MAE, MSE, RMSE, R²
> e = 0.5, 0, −1.5, −1 → **MAE 0.75** · **MSE 0.875** · **RMSE 0.935** · ȳ = 4.375, SST = 12.6875, SSE = 3.5 → **R² 0.724**

> [!question]- B10. 5-fold accuracy 80, 88, 85, 78, 84% รายงานผล
> mean **83%** · sd (n−1) **4.0%** → "83.0% ± 4.0%"

> [!question]- B11. PCA บนข้อมูล standardize 5 ตัวแปร eigenvalue = 2.2, 1.3, 0.8, 0.5, 0.2 หา explained variance แต่ละ PC, จำนวน PC ที่ถึง 80% และตาม Kaiser
> total = 5 → 44%, 26%, 16%, 10%, 4% · สะสม 44 → 70 → **86%** → **3 PC** · Kaiser (λ > 1) → **2 PC**

> [!question]- B12. K-Means k = 2 จุด P1 (1,2) P2 (2,1) P3 (1,1) P4 (6,6) P5 (7,7) P6 (6,8) · seed = P1, P4 รันจน converge หา centroid และ SSE
> **รอบ 1** (ระยะ² ถึง (1,2) / (6,6)): P2 2 / 41 → C1 · P3 1 / 50 → C1 · P5 61 / 2 → C2 · P6 61 / 4 → C2
> C1 = {P1, P2, P3} → **(1.333, 1.333)** · C2 = {P4, P5, P6} → **(6.333, 7)**
> **รอบ 2:** ไม่มีใครย้าย → converge · SSE = 1.333 (C1) + 2.667 (C2) = **4.0**

> [!question]- B13. silhouette ของจุด (2, 2) ที่อยู่กลุ่ม A = {(1,1), (2,2), (1,3)} · กลุ่มอื่น B = {(6,5), (7,6)}
> a = (√2 + √2)/2 = **1.414** · b = (5 + √41)/2 = (5 + 6.403)/2 = **5.702** → s = (5.702 − 1.414)/5.702 = **0.752**

> [!question]- B14. Apriori minsup count = 3: T1 {Bread, Butter, Milk} · T2 {Bread, Butter} · T3 {Bread, Milk} · T4 {Butter, Milk} · T5 {Bread, Butter, Milk, Jam} · T6 {Bread, Jam} หา L1, L2, L3 และ confidence/lift ของ Bread → Butter, Milk → Butter
> C1: Bread 5 · Butter 4 · Milk 4 · Jam 2 → **L1 = {Bread, Butter, Milk}**
> C2: {Bread, Butter} 3 · {Bread, Milk} 3 · {Butter, Milk} 3 → **L2 = ทั้งสาม**
> C3: {Bread, Butter, Milk} (prune ผ่าน — ทุก 2-subset ∈ L2) → count = 2 (T1, T5) → **L3 = ∅**
> Bread → Butter: conf = 3/5 = **0.60** · lift = 0.6/(4/6) = **0.90** (< 1!)
> Milk → Butter: conf = 3/4 = **0.75** · lift = 0.75/(4/6) = **1.125**
> ⚠️ Bread อยู่ใน 5/6 ตะกร้า → กฎที่มี Bread มี confidence ดูดีแต่ lift < 1

> [!question]- B15. 90% ซื้อ coffee · 25% ซื้อ tea · 20% ซื้อทั้งคู่ หา support, confidence, lift ของ tea → coffee
> s = **0.20** · c = 0.20/0.25 = **0.80** · lift = 0.80/0.90 = **0.89** → ไม่สัมพันธ์เชิงบวก (Apriori p.25)

> [!question]- B16. ข้อมูล 4,000 ปกติ / 250 ผิดปกติ หา IR ระดับความรุนแรง และ accuracy ของ majority baseline
> IR = 16 : 1 → **Moderate** · baseline = 4000/4250 = **94.1%**

---

## Part C · อ่านตาราง / กราฟ

> [!question]- C1. ตาราง validation error ของ KNN: k = 1 → 30% · 3 → 22% · 5 → 18% · 7 → 18% · 9 → 20% · 15 → 26% · 25 → 35% เลือก k และอธิบายรูปทรง
> **k = 5** (ต่ำสุด 18% · เสมอกับ 7 → เลือกค่าน้อยกว่า ตามสไลด์ p.43) · k เล็ก error สูงเพราะไวต่อ noise (overfit) · k ใหญ่ error สูงเพราะเรียบเกิน (underfit) → รูปตัว U

> [!question]- C2. Decision tree: depth 2 → train 0.85 CV 0.84 · depth 5 → 0.92 / 0.86 · depth 10 → 0.99 / 0.80 อธิบายและเลือก depth
> depth 10 = **overfitting** (train 0.99 แต่ CV ตก 0.80) · depth 2 อาจ underfit เล็กน้อย · **เลือก depth 5** (CV สูงสุด 0.86)

> [!question]- C3. PCA loadings PC1: Income 0.58 · Spending 0.55 · CreditLimit 0.52 · Age 0.08 · PC1 explained 61% ตีความ
> PC1 = **"กำลังซื้อ/ฐานะทางการเงิน"** (Income, Spending, CreditLimit loading สูงทิศเดียวกัน) · Age แทบไม่เกี่ยว · PC1 เก็บความแปรปรวน 61% → ลูกค้าต่างกันมากที่สุดในมิติกำลังซื้อ

> [!question]- C4. elbow: WCSS k = 1–6 = 1000, 520, 300, 260, 235, 220 · silhouette k = 2–6 = 0.41, 0.55, 0.47, 0.40, 0.38 เลือก k
> **k = 3** — WCSS ลดมากถึง k = 3 แล้วแบน · silhouette สูงสุดที่ k = 3 (0.55) → สองวิธียืนยันกัน

> [!question]- C5. ตาราง rules: (1) {Diaper} → {Beer} s 0.30 c 0.60 lift 1.50 · (2) {Bread} → {Milk} s 0.40 c 0.80 lift 0.95 · (3) {Wine} → {Cheese} s 0.05 c 0.90 lift 3.0 · เลือกกฎสำหรับโปรโมชันใหญ่ทั่วร้าน
> **กฎ (1)** — lift > 1 (สัมพันธ์จริง) และ support 30% (ครอบคลุมลูกค้ามาก) · กฎ (2) confidence สูงแต่ lift < 1 · กฎ (3) lift สูงสุดแต่ support 5% → เหมาะเป็นโปรเฉพาะกลุ่ม ไม่ใช่ทั่วร้าน

> [!question]- C6. logistic coefficients (positive = churn): tenure −0.06 · MonthlyCharges +0.02 · Contract_TwoYear −1.4 ตีความ
> tenure: e^{−0.06} = 0.94 → อยู่นานขึ้น 1 เดือน odds churn ลด 6% · MonthlyCharges: e^{0.02} = 1.02 → ค่ารายเดือน +1 odds +2% · Contract Two year: e^{−1.4} = **0.25** → odds churn เหลือ 1/4 ของ baseline (month-to-month) — ทั้งหมด "โดยตัวแปรอื่นคงที่"

> [!question]- C7. ตาราง: Majority acc 0.76 F1 0 · KNN acc 0.82 F1 0.60 · LogReg acc 0.85 F1 0.64 · LogReg + SMOTE acc 0.81 F1 0.67 recall 0.83 · โจทย์ต้องการหาลูกค้าเป้าหมายให้ได้มากที่สุด เลือกอะไร
> **LogReg + SMOTE** — recall สูงสุด (0.83) และ F1 สูงสุด (0.67) · accuracy ต่ำกว่า LogReg แต่ accuracy ไม่ใช่เป้าหมาย · ทุกโมเดลดีกว่า majority (F1 0)

---

## Part D · สถานการณ์ (ข้อเขียน)

> [!question]- D1. โรงพยาบาลต้องการทำนายผู้ป่วยมะเร็ง (2% ของข้อมูล) ออกแบบ workflow ตั้งแต่ต้นจนจบ พร้อมเหตุผล
> 1) EDA: ดูสัดส่วนคลาส (IR 49 : 1 moderate), missing, outlier · 2) **split stratified** (ล็อก test) · 3) preprocessing **ใน pipeline**: impute (median/mode), encode, scale · 4) **baseline** majority (acc 98% recall 0) + predictive baseline · 5) โมเดล: logistic (ตีความได้), RF (ทน imbalance) · 6) จัดการ imbalance **เฉพาะ training fold**: SMOTE / class_weight / ปรับ threshold · 7) **stratified k-fold CV** + tune ด้วย **recall/F1** (พลาดผู้ป่วยแพงมาก) · 8) ประเมิน test ครั้งเดียว: confusion matrix, recall, precision, F1 · 9) เลือก threshold ตามต้นทุน FN vs FP · 10) อธิบายด้วย odds ratio / feature importance

> [!question]- D2. เลือก metric หลักพร้อมเหตุผล: (ก) กรอง spam (ข) ตรวจโรคเบื้องต้น (ค) ทำนายราคาบ้าน (ง) จัดอันดับลูกค้าเพื่อโทรหาตามลำดับ
> (ก) **precision** — ส่งอีเมลจริงไปถังขยะ (FP) เสียหายมาก · (ข) **recall** — พลาดผู้ป่วย (FN) อันตราย · (ค) **RMSE/MAE** (+ R²) · (ง) 📚 **AUC** — วัดการจัดอันดับ ไม่ขึ้นกับ threshold

> [!question]- D3. ห้างต้องการแบ่งกลุ่มลูกค้าจากยอดซื้อ ความถี่ อายุ เพศ ช่องทาง เลือกวิธี + preprocessing + การเลือก k + การประเมิน
> **K-Means** · preprocessing: เลือก attribute ที่เกี่ยวข้อง, ตัด ID, one-hot เพศ/ช่องทาง, **standardize** (ยอดซื้อสเกลใหญ่), จัดการ outlier (ลูกค้า VIP มาก ๆ) · เลือก k: **elbow + silhouette** + ขนาดกลุ่มที่ทีมการตลาดใช้ได้ · ประเมิน: **cohesion** (WCSS), **separation** (ระยะ centroid, DB), **interpretability** (centroid table ตั้งชื่อกลุ่ม เช่น "ซื้อบ่อยยอดน้อย", "VIP") · ใช้ K-Means++ และหลาย n_init

> [!question]- D4. ร้านกาแฟอยากจัดเซต จงอธิบายขั้นตอนตั้งแต่ข้อมูลใบเสร็จจนได้คำแนะนำ
> ใบเสร็จ → transaction (list สินค้า) → **one-hot/binary** · เลือก minsup (เช่น 5–10% ตามขนาดกลุ่มที่สนใจ) → **Apriori/FP-Growth** หา frequent itemsets → สร้างกฎ (minconf เช่น 60–70%) → **กรอง lift > 1** เรียงตาม lift + support → ตีความ (support = ครอบคลุม, confidence = โอกาสซื้อต่อ, lift = แรงกว่าบังเอิญ) → จัดเซต/วางสินค้า/แนะนำตอนสั่ง · ระวังกฎที่ confidence สูงเพราะสินค้าขายดีอยู่แล้ว (lift < 1)

> [!question]- D5. ทำนายราคาบ้าน มีตัวแปร 13 ตัว บางคู่ corr 0.9 เปรียบเทียบ Linear Regression กับ KNN regressor พร้อมวิธีประเมินที่ถูก
> baseline = ทายค่าเฉลี่ย (R² ≈ 0) · Linear: ตีความ coefficient ได้ แต่ multicollinearity ทำให้ coef ไม่เสถียร → ตัด/รวมตัวแปร · KNN: ต้อง standardize + เลือก k ด้วย CV · จับความไม่เชิงเส้นได้ · ประเมินด้วย **k-fold CV บน train** (RMSE, MAE, R²) แล้ว test ครั้งเดียว · เลือกตามเป้าหมาย: ทำนายแม่นสุด (อาจเป็น KNN — Mock 2: RMSE 5.01 vs 6.01) vs อธิบายปัจจัย (Linear)

---

## Part E · หาที่ผิด

> [!question]- E1. `X = StandardScaler().fit_transform(X)` → `train_test_split(X, y)` → `knn.fit(X_train)` → `knn.score(X_test)`
> **leakage** — scaler ใช้ mean/SD รวม test · แก้: split ก่อน → `fit` scaler บน train → transform test (หรือ Pipeline)

> [!question]- E2. `X_res, y_res = SMOTE().fit_resample(X, y)` → `cross_val_score(tree, X_res, y_res, cv=5)`
> SMOTE ก่อน CV → validation fold มีจุดสังเคราะห์ (และไม่ใช่สัดส่วนจริง) → ผลดีเกินจริง · แก้: `imblearn.Pipeline([SMOTE, tree])` + `cross_val_score` (Imbalanced p.22)

> [!question]- E3. "เราเลือก k = 7 เพราะได้ accuracy บน test สูงสุด และรายงาน accuracy นี้เป็นผลสุดท้าย"
> test ถูกใช้เลือก k → ผลลำเอียง · แก้: เลือก k ด้วย validation/CV แล้วประเมิน test ครั้งเดียว

> [!question]- E4. "โมเดลได้ accuracy 97% บนข้อมูลที่มี fraud 3% จึงสรุปว่าโมเดลดีมาก"
> majority baseline ก็ได้ 97% → ต้องดู recall/precision/F1 ของ fraud และ confusion matrix

> [!question]- E5. "ใช้ Customer_ID เป็น root ของ tree เพราะ Information Gain สูงสุด (= 1.0)"
> ID แบ่งเป็น leaf ละ 1 แถว (pure) → IG สูงสุดแต่ไม่ generalize (overfit) · ตัด ID ทิ้ง หรือใช้ Gain Ratio (Student ID ได้ GR 0.231 < Car Type 0.408)

> [!question]- E6. "แปลงจังหวัด (กรุงเทพ = 1, เชียงใหม่ = 2, ภูเก็ต = 3) แล้วใช้ KNN"
> label encoding สร้างลำดับ/ระยะทางปลอม (ภูเก็ตห่างกรุงเทพ 2 เท่าของเชียงใหม่) → ใช้ **one-hot**

> [!question]- E7. "เลือก k = 10 สำหรับ K-Means เพราะ WCSS ต่ำที่สุด"
> WCSS ลดลงเสมอเมื่อ k เพิ่ม → ต้องใช้ elbow (จุดเริ่มแบน) / silhouette / การตีความ

> [!question]- E8. "กฎ {Bread} → {Milk} confidence 85% จึงควรจัดโปรโมชันคู่นี้" (Milk อยู่ใน 90% ของตะกร้า)
> lift = 0.85/0.90 = **0.94** < 1 → ซื้อ Bread แล้วซื้อ Milk น้อยกว่าคนทั่วไป → confidence สูงเพราะ Milk ขายดีอยู่แล้ว

> [!question]- E9. "PCA (ไม่ normalize) ได้ PC1 = 95% จึงใช้ 1 component พอ"
> ถ้าไม่ normalize PC1 อาจเป็นแค่ตัวแปรที่หน่วยใหญ่สุด (cereals: sodium · wine: Proline 99.8%) → standardize แล้วทำใหม่

> [!question]- E10. (สไลด์ Tree p.41) Gini(N1 = 5,2) = 0.194 · Gini(N2 = 1,4) = 0.528
> ผิด — ที่ถูก **0.408** และ **0.320** · split = **0.371** · gain **0.129**

> [!question]- E11. (สไลด์ Data p.21) d(x1 = (1,2), x3 = (2,0)) = 5.1
> ผิด — √(1 + 4) = **2.24** (5.1 คือ d(x2, x3))

> [!question]- E12. "logistic coefficient ของ Age = 0.3 → อายุเพิ่ม 1 ปี ความน่าจะเป็นเพิ่ม 0.3"
> coefficient เปลี่ยน **log-odds** ไม่ใช่ probability → odds คูณ e^{0.3} = **1.35** (เพิ่ม 35%) · ผลต่อ p ขึ้นกับระดับ p ปัจจุบัน

---

## 🎯 กับดักที่พลาดบ่อย — อ่านก่อนเข้าห้อง

> [!warning] 15 ข้อ
> 1. **accuracy บนข้อมูลไม่สมดุล** → ต้องเทียบ majority baseline เสมอ
> 2. **precision ↔ recall สลับ** — ตัวหาร: precision = TP + **FP** (ที่ทายว่าใช่) · recall = TP + **FN** (ที่ใช่จริง)
> 3. **orientation ของ confusion matrix** — อ่านหัวแถว/คอลัมน์ก่อนคำนวณ (สไลด์ KNN p.66 แถว = predicted)
> 4. **preprocessing / SMOTE / PCA ก่อน split** = leakage
> 5. **tune ด้วย test** = ผลลำเอียง
> 6. **ลืม scale** สำหรับ KNN / K-Means / PCA · **scale tree** โดยไม่จำเป็น (ไม่ผิด แต่ไม่ช่วย)
> 7. **IG กับ attribute ประเภท ID** → ใช้ Gain Ratio / ตัดทิ้ง
> 8. **log₂ ไม่ใช่ ln** ใน entropy · 0·log 0 = 0
> 9. **ตีความ logistic coef เป็นความน่าจะเป็น** → ต้องเป็น log-odds / odds ratio
> 10. **ลืม "โดยตัวแปรอื่นคงที่"** ตอนตีความ coefficient
> 11. **elbow เลือก WCSS ต่ำสุด** → ผิด
> 12. **confidence สูงแต่ lift < 1**
> 13. **support ของกฎ** = support ของ X ∪ Y (ไม่ใช่ของ X)
> 14. **K-Means ผลต่างกันแต่ละรอบ** = local optimum (ไม่ใช่ผิด) → K-Means++ + n_init
> 15. **PCA ไม่ normalize** → PC1 = ตัวแปรหน่วยใหญ่

---

## 📝 ข้อที่พลาด (กรอกเอง)
| ข้อ | พลาดเพราะ | ทบทวนที่ |
|---|---|---|
| | | |

---

**กลับหน้าหลัก →** [[LEC 00 START HERE]]
