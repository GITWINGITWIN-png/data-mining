---
title: LEC 08 · Decision Trees & Random Forest
exam: Lecture — จ. 19 ต.ค. 2569 16:00–19:00
guideline: "Lecture ข้อ 4.4 — Decision Trees และ Random Forest: concept, tree construction, parameters, overfitting และ evaluation"
source: 69_1_Tree.pdf (77 pp) · 69_1_imbalanced.pdf p.12–13 · HW10
tags: [final, lecture, decision-tree, entropy, gini, information-gain, gain-ratio, pruning, random-forest]
---

# LEC 08 · Decision Trees & Random Forest
### แบ่งข้อมูลทีละคำถามจน "บริสุทธิ์" — และรวมหลายต้นให้เสถียร

> [!abstract] guideline ข้อ 4.4: **concept · tree construction · parameters · overfitting · evaluation** (ทั้ง Tree และ RF)
> → [[#8.1 แนวคิด ⭐⭐]] · [[#8.2 Tree Construction — อัลกอริทึม ⭐⭐⭐]] · [[#8.3 Impurity Measures ⭐⭐⭐⭐]] · [[#8.4 Information Gain — Weather ⭐⭐⭐⭐]] · [[#8.5 Gini Split ⭐⭐⭐]] · [[#8.6 Gain Ratio ⭐⭐⭐]] · [[#8.7 Overfitting & Pruning ⭐⭐⭐⭐]] · [[#8.8 Parameters ⭐⭐]] · [[#8.9 Random Forest ⭐⭐⭐]] · [[#8.10 Evaluation ⭐⭐]]

**ลิงก์:** [[LEC 00 START HERE|หน้าหลัก Lecture]] · [[LEC 05 Model Construction & Evaluation]] · Lab: [[LAB 05 Supervised Models#5.4 Decision Tree ⭐⭐⭐]] · งานของคุณ: HW10 (IG ด้วยมือ), W12 (tree + CV)

---

## 8.1 แนวคิด ⭐⭐

> [!quote] สไลด์ Tree p.2–4
> **"Easy to understand, implement and use · computationally cheap · support classification and prediction"**
> โครงสร้าง **divide-and-conquer**: **internal node** = ทดสอบ attribute · **branch** = ผลการทดสอบ · **leaf** = คลาส (classification tree) หรือค่าตัวเลข (regression tree)
> ทุกเส้นทาง root → leaf = **กฎ IF-THEN** 1 ข้อ (p.3, 63): *"IF (Income > 92.5) AND (Education < 1.5) AND (Family ≤ 2.5) THEN Class = 0"*

> [!example] ตัวอย่าง Tid/Cheat (p.47–49, 64–69)
> ```
> Refund = Yes → NO
> Refund = No → MarSt = Married → NO
>               MarSt = Single/Divorced → TaxInc < 80K → NO
>                                         TaxInc > 80K → YES
> ```
> **ทดสอบ record ใหม่** (Refund = No, Married, 80K) → Refund = No → Married → **Cheat = "No"**
> ⚠️ p.49: *"There could be more than one tree that fits the same data!"* (tree ที่ root เป็น MarSt ก็ fit ได้)

---

## 8.2 Tree Construction — อัลกอริทึม ⭐⭐⭐

> [!important] ⭐ ขั้นตอนทั่วไป (สไลด์ p.7, Hunt's algorithm) — **recursive partitioning**
> 1. ถ้า records ใน node **อยู่คลาสเดียวกันหมด** → เป็น **leaf** หยุด
> 2. **ทดสอบทุก attribute (ทุก test condition)** → เลือกตัวที่ **"Highest Gain of Impurity Reduction"**
> 3. **แบ่ง (split)** ข้อมูลตามค่าของ attribute นั้น
> 4. **ทำซ้ำ** ข้อ 1–3 กับแต่ละ node ลูก
>
> หยุดเมื่อ (p.50): node pure · ไม่มี attribute เหลือ · *"or even earlier"* (pre-pruning)
> เป็น **greedy** — เลือก split ที่ดีที่สุด "ตอนนี้" ไม่ย้อนกลับ → *"May not find the best tree"* (p.71)

**Test condition (p.29–32):**
| ชนิด attribute | 2-way split | multi-way split |
|---|---|---|
| nominal {A, B, C} | {A} vs {B, C} ฯลฯ — มี $2^{k-1}-1$ แบบ (k = 3 → 3 แบบ) | แยกทุกค่า |
| continuous | `Taxable Income > 80K?` (หา cut ที่ดีที่สุด) | discretize เป็นช่วง |

---

## 8.3 Impurity Measures ⭐⭐⭐⭐

![[lec_impurity_gain.png]]

> [!important] ⭐⭐ สูตร (p.23, 26)
> $$\text{GINI}(t)=1-\sum_j[p(j\mid t)]^2\qquad\text{Entropy}(t)=-\sum_j p(j\mid t)\log_2 p(j\mid t)$$
> | | min | max (n_c คลาส) | max 2 คลาส |
> |---|---|---|---|
> | Gini | **0** (pure) | $1-\frac{1}{n_c}$ | **0.5** |
> | Entropy | **0** (pure) | $\log_2 n_c$ | **1** |
> | Misclassification error | 0 | — | 0.5 (สไลด์ไม่ให้สูตร · 📚 $1-\max_j p(j\mid t)$) |
> p.24: **High impurity** = 50/50 · **Low impurity** = ส่วนใหญ่คลาสเดียว (70/30) · **Zero impurity** = คลาสเดียว

> [!example]- 🧮 ค่ามาตรฐานจากสไลด์ (p.23, 25, 27) — ใช้เช็กการคำนวณ
> | (C1, C2) | Gini | Entropy |
> |---|---|---|
> | (0, 6) | 0.000 | 0 |
> | (1, 5) | 1 − (1/6)² − (5/6)² = **0.278** | **0.65** |
> | (2, 4) | 1 − (2/6)² − (4/6)² = **0.444** | **0.92** |
> | (3, 3) | **0.500** | **1.00** |

---

## 8.4 Information Gain — Weather ⭐⭐⭐⭐

> [!important] ⭐ สูตร (p.34)
> $$\text{GAIN}_{split}=\text{Entropy}(p)-\sum_{i=1}^{k}\frac{n_i}{n}\,\text{Entropy}(i)$$
> = **Entropy ของ parent − ค่าเฉลี่ยถ่วงน้ำหนักของ entropy ลูก** · *"Choose the split that achieves most reduction (maximizes GAIN)"*

> [!example] ⭐⭐ Weather 14 records (p.8, 36–39) — ฝึกจนทำได้ใน 5 นาที
> | # | Outlook | Temp | Humidity | Windy | Class |
> |---|---|---|---|---|---|
> | 1 | sunny | hot | high | false | N |
> | 2 | sunny | hot | high | true | N |
> | 3 | overcast | hot | high | false | P |
> | 4 | rain | mild | high | false | P |
> | 5 | rain | cool | normal | false | P |
> | 6 | rain | cool | normal | true | N |
> | 7 | overcast | cool | normal | true | P |
> | 8 | sunny | mild | high | false | N |
> | 9 | sunny | cool | normal | false | P |
> | 10 | rain | mild | normal | false | P |
> | 11 | sunny | mild | normal | true | P |
> | 12 | overcast | mild | high | true | P |
> | 13 | overcast | hot | normal | false | P |
> | 14 | rain | mild | high | true | N |
>
> **① parent:** 9 P, 5 N → $H=-\frac{9}{14}\log_2\frac{9}{14}-\frac{5}{14}\log_2\frac{5}{14}=0.410+0.530=\mathbf{0.940}$
> **② แยกตาม Outlook:** sunny (2P, 3N) H = **0.971** · overcast (4P, 0N) H = **0** · rain (3P, 2N) H = **0.971**
> **③ เฉลี่ยถ่วง:** $\frac{5}{14}(0.971)+\frac{4}{14}(0)+\frac{5}{14}(0.971)=\mathbf{0.694}$
> **④ Gain(Outlook) = 0.940 − 0.694 = 0.247** (สไลด์ p.10 ปัด 0.246)
>
> | attribute | Gain |
> |---|---|
> | **Outlook** | **0.247** ← root |
> | Humidity | 0.152 |
> | Windy | 0.048 |
> | Temperature | 0.029 |
>
> **⑤ ทำต่อในกิ่ง:** sunny → Gain(Humidity) = **0.971** (high = N ทั้งหมด, normal = P ทั้งหมด) · rain → Gain(Windy) = **0.971** · overcast → leaf P
> **Tree สุดท้าย (p.15):** outlook = sunny → humidity (high → N, normal → P) · overcast → P · rain → windy (true → N, false → P)

> [!tip] เทคนิคคำนวณ log₂ ในห้องสอบ
> $\log_2 x=\frac{\ln x}{\ln 2}=\frac{\log_{10}x}{0.301}$ · จำค่าที่ใช้บ่อย: H(1/2, 1/2) = 1 · H(1/3, 2/3) = 0.918 · H(1/4, 3/4) = 0.811 · H(2/5, 3/5) = 0.971 · H(1/5, 4/5) = 0.722 · H(9/14, 5/14) = 0.940

---

## 8.5 Gini Split ⭐⭐⭐

> [!important] สูตร (p.40) — ใช้ใน **CART**, SLIQ, SPRINT
> $$\text{GINI}_{split}=\sum_{i=1}^{k}\frac{n_i}{n}\,\text{GINI}(i)\qquad\text{Gini gain}=\text{GINI(parent)}-\text{GINI}_{split}$$

> [!bug] 🐛 สไลด์ p.41 คำนวณผิด — ตัวอย่าง binary attribute B
> parent (C1 = 6, C2 = 6) Gini = 0.500 · split B?: **N1 = (5, 2)**, **N2 = (1, 4)**
> | | สไลด์ | **ที่ถูก** |
> |---|---|---|
> | Gini(N1) = 1 − (5/7)² − (2/7)² | 0.194 | **0.408** |
> | Gini(N2) = 1 − (1/5)² − (4/5)² | 0.528 | **0.320** |
> | Gini(children) = 7/12·N1 + 5/12·N2 | 0.333 | **0.371** |
> | Gain = 0.5 − Gini(children) | 0.167 | **0.129** |
> ถ้าข้อสอบให้ตัวเลขแบบสไลด์ ให้คำนวณใหม่เองและเขียนกำกับ

> [!example]- 🧮 Weather ด้วย Gini (เทียบกับ entropy)
> Gini(parent) = 1 − (9/14)² − (5/14)² = **0.459**
> | attribute | Gini_split | Gini gain |
> |---|---|---|
> | **Outlook** | 0.343 | **0.116** |
> | Humidity | 0.367 | 0.092 |
> | Windy | 0.429 | 0.031 |
> | Temperature | 0.441 | 0.019 |
> ได้ **ลำดับเดียวกัน** กับ IG — สไลด์ p.42: *"Entropy and GINI produce similar tree structure"*

> [!example]- 🧮 Tid/Cheat (3 Yes, 7 No)
> H = **0.881** · Gini = **0.42** · Refund: IG 0.192, Gini gain 0.077 · **Marital (Married vs Single/Divorced): IG 0.281, Gini gain 0.120** ← ดีกว่า · Taxable Income > 80K: IG 0.192

---

## 8.6 Gain Ratio ⭐⭐⭐

> [!important] ⭐ ปัญหาของ Information Gain (p.43–44)
> **"Information-gain with a large number of child nodes tends to be higher"** → attribute ที่มีค่าไม่ซ้ำเยอะ (เช่น **Student ID**) แบ่งจน leaf มี 1 แถว (pure) → IG สูงสุด แต่ **ไม่ generalize** (overfit)
> $$\text{Gain Ratio}=\frac{\text{Information Gain}}{\text{SplitInfo}}\qquad\text{SplitInfo}=-\sum_{j=1}^{m}p(j)\log_2 p(j)$$
> p(j) = สัดส่วน records ใน child j · SplitInfo **เพิ่มตามจำนวน child** (max = log m เมื่อเท่ากันหมด) → ทำหน้าที่ **normalization factor**
> 🐛 สไลด์ p.44 พิมพ์ "log(mm)" → ที่ถูกคือ **log m**

> [!example] ⭐ Own Car / Car Type / Student ID (p.21, 43) — คำนวณยืนยันแล้ว (parent 10 C0, 10 C1 → H = 1)
> | attribute | ลูก | IG | SplitInfo | **Gain Ratio** | Gini_split |
> |---|---|---|---|---|---|
> | Own Car | Yes (6, 4) · No (4, 6) | 0.029 | 1.000 | 0.029 | 0.480 |
> | Car Type | Family (1, 3) · Sports (8, 0) · Luxury (1, 7) | 0.620 | 1.522 | **0.408** | 0.163 |
> | Student ID | 20 leaves ละ 1 แถว | **1.000** | log₂20 = 4.322 | 0.231 | 0 |
> **IG เลือก Student ID** (ผิด — จำข้อมูล) · **Gain Ratio เลือก Car Type** (ถูก) → นี่คือเหตุผลที่ C4.5 ใช้ gain ratio · ตรงกับ HW10 Ex1 ของคุณ (Car Type IG 0.620, Customer ID ห้ามใช้)
> Weather: GR(Outlook) = 0.247/1.577 = **0.156** · GR(Humidity) = 0.152/1.000 = 0.152 → Outlook ยังชนะ

> [!note] อัลกอริทึม (p.42, 45)
> **ID3** = Information Gain · **C4.5** = Gain Ratio (สไลด์ p.34 เขียนว่า IG "used in C4.5" — 📚 ตามตำรา ID3 ใช้ IG, C4.5 ใช้ gain ratio) · **CART** = Gini (binary split) · RapidMiner `Decision Tree` default = **gain_ratio**

---

## 8.7 Overfitting & Pruning ⭐⭐⭐⭐

![[lec_tree_overfit.png]]

> [!quote] นิยาม (p.51, 55 — หน้าเหมือนกัน 2 หน้า)
> **"Underfitting: when model is too simple, both training and test errors are large."**
> **"Overfitting: when the test error increases while the training error steadily decreases. The size of the tree will become same as the size of the training data → too specific to the training → cannot generalize very well."**
> p.56: *"Natural end of process is 100% purity in each leaf. This OVERFITS the data… Past a certain point, the error rate for the validation data starts to increase."*

> [!example] ภาพข้างบน (Social Network Ads, 10-fold) — ตัวเลขจริง
> depth 2: train 0.916 · CV **0.908** (ดีที่สุด) → depth โตเต็ม: train **0.998** · CV 0.848 → ช่องว่าง 15 จุด = overfitting · RF ได้ CV 0.908 แม้ต้นจะลึก

> [!important] ⭐⭐ 2 วิธีกัน overfitting
> | | **Pre-pruning (early stopping)** p.57–61 | **Post-pruning** p.62 |
> |---|---|---|
> | เมื่อไร | **ระหว่าง** สร้าง tree | **หลัง** สร้างเต็มแล้ว |
> | วิธี | หยุดแตกกิ่งถ้า: ทุก record คลาสเดียว · ทุก attribute ค่าเท่ากัน · impurity ต่ำกว่า threshold · **จำนวน record < threshold** (exception threshold — node ที่มี 10 จาก 1,000,000 แถว "insignificant") · class 99% เป็นคลาสเดียว (classification threshold) · **χ² test** บอกว่าคลาสไม่ขึ้นกับ feature | *"Grow decision tree to its entirety, then cut off nodes or subtrees… **bottom-up**"* · แทน subtree ด้วย leaf ถ้า impurity ไม่เกิน threshold · ตัดกิ่งที่ *"will not do well on the future data"* โดยดู **validation dataset** |
> | sklearn | `max_depth`, `min_samples_leaf`, `min_samples_split`, `min_impurity_decrease` | `ccp_alpha` (cost-complexity pruning) |
> | RapidMiner | apply prepruning (minimal gain, minimal leaf size, minimal size for split) | apply pruning (confidence) |

---

## 8.8 Parameters ⭐⭐

| ความหมาย | sklearn `DecisionTreeClassifier` | RapidMiner `Decision Tree` |
|---|---|---|
| วัด impurity | `criterion` = `gini` (default) / `entropy` | `criterion` = **gain_ratio** (default) / information_gain / gini_index / accuracy |
| ความลึกสูงสุด | `max_depth` (None) | maximal depth (10) |
| ขนาด leaf ขั้นต่ำ | `min_samples_leaf` (1) | minimal leaf size (2) |
| ขนาดขั้นต่ำที่จะแบ่ง | `min_samples_split` (2) | minimal size for split (4) |
| gain ขั้นต่ำ | `min_impurity_decrease` | minimal gain (0.01) |
| post-prune | `ccp_alpha` | apply pruning + confidence (0.1) |
> **ค่าที่ทำให้ tree ง่ายขึ้น (กัน overfit):** max_depth ↓ · min_samples_leaf ↑ · min_impurity_decrease ↑ · ccp_alpha ↑

**Pros / Cons (p.70–71):** ✅ ถูก เร็ว ตีความง่าย (ถ้าเล็ก) · **feature selection อัตโนมัติ** (p.46 embedded) · ไม่มีสมมติฐานทางสถิติ · **"no need for feature scaling"** · ใช้กับ linear และ non-linear · ❌ tree ใหญ่ตีความยาก · **greedy** · **noise → overfitting** ถ้าโตเต็ม

---

## 8.9 Random Forest ⭐⭐⭐

> [!quote] สไลด์ Tree p.72 (ซ้ำ Imbalanced p.13) — เนื้อหาทั้งหมดที่สไลด์ให้
> **"Uses multiple (ensemble) classification models… Joint decision of multiple classification models generates higher accuracy than using a single classification model."**
> **"K different decision trees: Pick a random subset S of training samples. For each subset → grow a full tree. Given a new data point X: classify X using each of the trees. Use MAJORITY VOTE: class predicted most often."**
> **Dis-advantages:** *"Difficult interpretability · overfitting can easily occur · need to choose the number of trees"*

> [!important] 📚 กลไกที่ต้องเข้าใจเพิ่ม (Breiman 2001; scikit-learn User Guide §1.11)
> 1. **Bootstrap sampling (bagging):** แต่ละต้นได้ training set สุ่มแบบ**ใส่คืน** ขนาด n เท่าเดิม (≈ 63% ของแถวไม่ซ้ำ)
> 2. **Random feature subset ต่อ split:** แต่ละ node ลองแค่ `max_features` ตัว (classification default = √p) → ต้นไม้แต่ละต้น **ไม่เหมือนกัน (decorrelated)**
> 3. **รวมผล:** classification = majority vote (หรือเฉลี่ยความน่าจะเป็น) · regression = ค่าเฉลี่ย
> 4. **ทำไมดีกว่า tree เดี่ยว:** tree เดี่ยวที่โตเต็ม **variance สูง** (ข้อมูลเปลี่ยนนิดเดียว ต้นเปลี่ยนมาก) → เฉลี่ยหลายต้นที่ต่างกันลด variance โดย bias แทบเท่าเดิม
> 5. **OOB (out-of-bag) error:** แถวที่ไม่ถูกสุ่มเข้าต้นไหน ใช้ทดสอบต้นนั้น → ประเมินผลได้โดยไม่ต้องแยก test
> 6. **Feature importance:** impurity ที่ลดได้รวมทุกต้น → บอกว่า feature ไหนสำคัญ (แต่ไม่บอกทิศทาง)

| parameter | sklearn | ผล |
|---|---|---|
| จำนวนต้น | `n_estimators` (100) | มากขึ้น → เสถียรขึ้น ช้าลง (ไม่ทำให้ overfit เพิ่ม) |
| feature ต่อ split | `max_features` ("sqrt") | น้อย → ต้นต่างกันมาก |
| ความลึก / leaf | `max_depth`, `min_samples_leaf` | คุม overfit ของแต่ละต้น |
| bootstrap | `bootstrap=True` | — |
> Imbalanced p.12: ensemble (RF, XGBoost, boosting) เป็นกลุ่ม *"algorithms less affected"* โดย imbalance

> [!example] ผลจริง (Social Network Ads, 10-fold CV)
> Tree โตเต็ม 0.848 · Tree depth 3 0.898 · RF default 0.895 · **RF min_samples_leaf = 5: 0.908** · importance: Age 0.52, Salary 0.47, Gender 0.01

---

## 8.10 Evaluation ⭐⭐

- ใช้ CV / hold-out + metrics มาตรฐาน ([[LEC 05 Model Construction & Evaluation]]) · tree ให้ `predict_proba` = **สัดส่วนคลาสใน leaf** → ปรับ threshold ได้
- สไลด์ p.73–76 วาง evaluation methods ไว้ท้ายบท Tree: hold-out · random sub-sampling · **k-fold CV** (ตัวอย่าง 80/88/85/78/84 → 83%) · LOOCV · Group Models
- เปรียบเทียบ **train vs CV** เพื่อตรวจ overfitting · เลือก depth / leaf size ด้วย CV

---

## ✅ Self-Test — LEC 08

> [!question]- Q1. node มี 8 Yes 2 No หา Entropy และ Gini
> p = 0.8, 0.2 → H = −0.8 log₂0.8 − 0.2 log₂0.2 = 0.258 + 0.464 = **0.722** · Gini = 1 − 0.64 − 0.04 = **0.32**

> [!question]- Q2. parent (10 Yes, 10 No) แบ่งเป็น A (8 Yes, 2 No) และ B (2 Yes, 8 No) หา Information Gain
> H(parent) = 1 · H(A) = H(B) = 0.722 · เฉลี่ยถ่วง = 0.722 → **IG = 0.278**

> [!question]- Q3. ทำไม Information Gain ชอบ attribute ที่มีค่าเยอะ แก้อย่างไร
> แบ่งละเอียดจน child แทบ pure (entropy ≈ 0) → IG สูงโดยไม่มีพลังทำนาย · แก้ด้วย **Gain Ratio** (หารด้วย SplitInfo ที่โตตามจำนวน child) หรือไม่ใช้ attribute ประเภท ID

> [!question]- Q4. pre-pruning กับ post-pruning ต่างกันอย่างไร
> pre: หยุดตั้งแต่ตอนสร้าง (เกณฑ์ depth, จำนวนแถวขั้นต่ำ, gain ขั้นต่ำ, χ²) · post: สร้างเต็มแล้วตัดกิ่งจากล่างขึ้นบนด้วย validation data · post มักได้ tree ดีกว่าแต่ใช้เวลามากกว่า

> [!question]- Q5. Random Forest ต่างจากการสร้าง tree 100 ต้นด้วยข้อมูลชุดเดียวกันอย่างไร
> ถ้าข้อมูลและ feature เหมือนกันทุกต้น tree ที่ได้จะเหมือนกันหมด โหวตก็ได้ผลเดิม · RF ทำให้ต้นต่างกันด้วย **bootstrap sample** + **สุ่ม feature ต่อ split** → การเฉลี่ยจึงลด variance ได้

> [!question]- Q6. ทำไม decision tree ไม่ต้อง scale
> split ใช้ threshold ทีละ feature (x ≤ c) · การเปลี่ยนสเกลแบบเชิงเส้นไม่เปลี่ยนลำดับของค่า → ได้ split และ tree เดิม

---

**กลับหน้าหลัก →** [[LEC 00 START HERE]] · **ถัดไป →** [[LEC 09 Clustering]]
