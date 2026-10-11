---
title: LEC 04 · Imbalanced Classification
exam: Lecture — จ. 19 ต.ค. 2569 16:00–19:00
guideline: "Lecture ข้อ 2 — Imbalanced classification: undersampling, oversampling, SMOTE · หลักการใช้ sampling/SMOTE เฉพาะ training data · (ข้อ 3) เลือก metric สำหรับ imbalanced"
source: 69_1_imbalanced.pdf (24 pp) · W14
tags: [final, lecture, imbalanced, smote, undersampling, oversampling, cost-sensitive]
---

# LEC 04 · Imbalanced Classification
### เมื่อคลาสที่สนใจเป็นคลาสส่วนน้อย

> [!abstract] guideline: **undersampling · oversampling · SMOTE · ใช้ sampling/SMOTE เฉพาะ training data** + เลือก metric
> → [[#4.1 นิยาม + Imbalance Ratio ⭐⭐⭐]] · [[#4.2 ผลกระทบ + Accuracy Paradox ⭐⭐⭐⭐]] · [[#4.3 เทคนิครับมือ ⭐⭐⭐]] · [[#4.4 SMOTE ⭐⭐⭐⭐]] · [[#4.5 Sampling เฉพาะ Training Data ⭐⭐⭐⭐]]

**ลิงก์:** [[LEC 00 START HERE|หน้าหลัก Lecture]] · [[LEC 05 Model Construction & Evaluation#5.9 เลือก Metric ให้เหมาะกับปัญหา ⭐⭐⭐⭐]] · Lab: [[LAB 03 Preprocessing Recipes#3.5 Sampling & SMOTE ⭐⭐⭐]] · งานของคุณ: W14 (E0/E1/E2)

---

## 4.1 นิยาม + Imbalance Ratio ⭐⭐⭐

> [!quote] สไลด์ p.2, 6
> ข้อมูลที่คลาสหนึ่ง (**majority**) มีมากกว่าอีกคลาส (**minority**) มาก · **"Most of the time, class of interest is MINORITY class"** (fraud, churn, โรค, ลูกค้าตอบรับ)
> **"Models tend to favor the majority class… leads to low performance metrics such as RECALL and F1-score for minority classes"**

> [!important] ⭐ Imbalance Ratio (p.8)
> $$IR=\frac{\text{จำนวน majority}}{\text{จำนวน minority}}$$
> | ระดับ (p.8) | IR |
> |---|---|
> | Mild | < 10 : 1 |
> | Moderate | 10 : 1 – 100 : 1 |
> | Severe | > 100 : 1 |
> | Extreme | > 1000 : 1 |
> *"Even mild imbalance can significantly affect model performance"*

> [!example] ตัวอย่าง IR จากสไลด์ (คำนวณยืนยันแล้ว)
> - 10,000 class A vs 100 class B → **100 : 1** (p.7)
> - Telco churn: No **5,174** / Yes **1,869** → IR = **2.77** (p.3 · W14 ของคุณ)
> - Internet service (p.5, 8): Active 63,679 vs Claim 30,239 → **2.11** · vs Overdue 14,718 → **4.33** · vs Other 8,686 → **7.33**
> - Department counts (p.4): max/min = 799/162 = **4.93**

**ชนิด imbalance (p.9):** **Between-class** (ขนาดคลาสต่างกัน — วัดด้วย IR) · **Within-class** (กลุ่มย่อยในคลาสเดียวกันกระจายไม่เท่ากัน — small disjuncts) · **Multi-class imbalance**

---

## 4.2 ผลกระทบ + Accuracy Paradox ⭐⭐⭐⭐

![[lec_smote_paradox.png]]

> [!example] ⭐⭐ Fraud confusion matrix (p.11) — ออกสอบแน่
> | | Pred Legit | Pred Fraud |
> |---|---|---|
> | **Actual Legit** | 950 | 30 |
> | **Actual Fraud** | 15 | 5 |
> **accuracy = (950 + 5)/1000 = 95.5%** · precision(fraud) = 5/35 = **14.29%** · recall(fraud) = 5/20 = **25.0%** · F1(fraud) = 2·5/(10 + 30 + 15) = **0.182**
> precision(legit) = 950/965 = 98.45% · recall(legit) = 950/980 = 96.94%
> **โมเดลที่ทาย "Legit" ทุกแถว → accuracy 980/1000 = 98%** (สูงกว่าโมเดลจริง!) แต่จับ fraud ได้ **0**
> สไลด์: *"Low Precision, Recall and F1-score even with High Accuracy"* · *"Can use Cost-Matrix for model evaluation"*

> [!important] ผลกระทบ 3 ข้อ (p.10)
> 1. **"Biased towards the Majority Class"**
> 2. **"Difficulties Learning Minority Class Characteristics"** (ตัวอย่างน้อยเกินจะเห็นรูปแบบ)
> 3. **"Model may simply predict the majority class most of the time"**
> → **metric:** ใช้ **recall / precision / F1 ของคลาสส่วนน้อย**, confusion matrix, cost — **ไม่ใช้ accuracy เดี่ยว ๆ**

---

## 4.3 เทคนิครับมือ ⭐⭐⭐

> [!important] ⭐ 4 แนวทาง (p.12)
> 1. **Algorithms less affected:** ensemble — **XGBoost, Random Forest, Boosting**
> 2. **Cost-Sensitive Learning** (p.14): cost matrix $C(i,j)$ (i = predicted, j = true) · *"No cost for correct classification · Cost of misclassifying minority examples is higher than the contrary case · Minimizes the overall cost"* · 📚 sklearn: `class_weight="balanced"`
> 3. **Over-sampling** คลาสส่วนน้อย
> 4. **Under-sampling** คลาสส่วนมาก

| | วิธี | ข้อดี | ❌ ข้อเสีย (p.16) |
|---|---|---|---|
| **RUS** Random Under-Sampling | สุ่มตัดคลาสส่วนมากให้เท่าส่วนน้อย | เร็ว ข้อมูลเล็กลง | *"cause the classifier to **miss important concepts** pertaining to the majority class"* (ทิ้งข้อมูล) |
| **Near-Miss** | under-sample แบบเลือกจุด majority ที่ใกล้ minority | เก็บจุดที่ยาก | ไวต่อ noise |
| **ROS** Random Over-Sampling | **ทำซ้ำ (replicate)** จุด minority | ไม่ทิ้งข้อมูล | *"does not really get new data"* → **over-fitting** |
| **SMOTE** | **สร้างจุดสังเคราะห์ใหม่** | ไม่ใช่การ copy ลด overfit เมื่อเทียบ ROS | ต้องเป็นตัวเลข + scale · อาจสร้างจุดในเขตคลาสอื่น (ถ้า minority กระจัดกระจาย) |
| **Hybrid** | over + under ร่วมกัน | สมดุลข้อดี | ซับซ้อนกว่า |

---

## 4.4 SMOTE ⭐⭐⭐⭐

> [!quote] Synthetic Minority Over-sampling Technique (p.17) — *"A powerful method. Create artificial data."*
> สำหรับแต่ละจุด minority $X_i$:
> 1. หา **K nearest neighbors** (ที่เป็น minority ด้วยกัน) ของ $X_i$
> 2. **สุ่มเลือก** 1 ตัวจากเพื่อนบ้าน $\bar X_i$
> 3. **สร้างจุดใหม่แบบสุ่มบนเส้นตรง** ระหว่าง $X_i$ กับ $\bar X_i$
> 📚 สูตร (Chawla et al. 2002): $X_{new}=X_i+\lambda(\bar X_i-X_i),\ \lambda\sim U(0,1)$

> [!example]- 🧮 Drill: $X_i$ = (2, 3), เพื่อนบ้าน $\bar X_i$ = (4, 7), λ = 0.25
> $X_{new}$ = (2, 3) + 0.25·(2, 4) = **(2.5, 4.0)** — อยู่บนเส้นเชื่อมสองจุด ห่างจาก $X_i$ หนึ่งในสี่

**พารามิเตอร์:** `k_neighbors` (default 5) · `sampling_strategy` (เช่น "auto" = เพิ่มจนเท่าคลาสส่วนมาก) · RapidMiner `SMOTE Upsampling` (p.20): number of neighbours 5 · normalize ✅ · equalize classes ✅ · auto detect minority class ✅

---

## 4.5 Sampling เฉพาะ Training Data ⭐⭐⭐⭐

> [!danger] ⭐⭐⭐ กฎเหล็ก (p.22–23)
> **"Correct pattern: RESAMPLE ONLY THE TRAINING FOLD"** · **"Do not apply SMOTE before Cross-Validation"**
> ```
> Training fold:   Training data → SMOTE → Decision Tree → Trained model
> Validation fold: Original validation data (NO SMOTE) → Apply trained model → Accuracy, Precision, Recall, F1
> ```
> **"Key idea: SMOTE learns synthetic samples from training data only. This keeps the evaluation fair."** · ทำซ้ำ 5 รอบ (5-fold) ทุกแถวเป็น validation 1 ครั้ง

> [!important] ทำไม SMOTE ก่อน split / ก่อน CV ถึงผิด (2 เหตุผล)
> 1. **Leakage:** จุดสังเคราะห์สร้างจากจุดจริงที่อาจไปอยู่ใน test → test มีจุดที่ "เกือบซ้ำ" กับ train → ผลดีเกินจริง
> 2. **test ไม่สะท้อนโลกจริง:** โลกจริงมี fraud 2% ไม่ใช่ 50% → ต้องวัดบนสัดส่วนจริง

> [!bug] 🐛 สไลด์เองมีตัวอย่าง "ผิด" 2 หน้า (ใช้ตอบข้อ "หาที่ผิด")
> - **p.21 (Python):** `X_res, y_res = SMOTE().fit_resample(X, y)` → **แล้วค่อย** `train_test_split(X_res, y_res)` = SMOTE ก่อน split ❌
> - **p.20 (RapidMiner):** `SMOTE Upsampling` วาง**ก่อน** `Cross Validation` ❌
> - **ที่ถูก (p.22):** `imblearn.pipeline.Pipeline([("smote", SMOTE()), ("classifier", DecisionTreeClassifier())])` + `cross_validate(model, X, y, cv=StratifiedKFold(5, shuffle=True))` ✅

> [!example] W14 ของคุณ (Telco churn, IR 2.77, 5-fold, tree เดียวกัน)
> | | accuracy | precision | recall | **F1** | FN |
> |---|---|---|---|---|---|
> | E0 ไม่ sample | **0.765** | **0.565** | 0.498 | 0.529 | 939 |
> | E1 RUS 300/300 | 0.695 | 0.451 | 0.698 | 0.548 | 565 |
> | **E2 SMOTE** | 0.738 | 0.505 | **0.698** | **0.585** | 565 |
> **อ่าน:** sampling ทั้งสองแบบ **เพิ่ม recall มาก** (FN ลด 374) แลกกับ accuracy/precision ลด · SMOTE ได้ F1 ดีสุด เพราะได้ recall เท่า RUS แต่ FP น้อยกว่า (1,284 vs 1,585) — RUS ทิ้งข้อมูล majority ไปมาก

---

## ✅ Self-Test — LEC 04

> [!question]- Q1. ข้อมูล 9,500 ปกติ / 500 ผิดปกติ หา IR และระดับ
> IR = 9500/500 = **19 : 1** → **Moderate** (10–100)

> [!question]- Q2. ROS ต่างจาก SMOTE อย่างไร ทำไม SMOTE มักดีกว่า
> ROS **copy** จุดเดิมซ้ำ → โมเดลจำจุดเดิม (overfit) · SMOTE **สร้างจุดใหม่** บนเส้นระหว่างเพื่อนบ้าน → ขยายบริเวณของ minority ให้กว้างขึ้น generalize ดีกว่า

> [!question]- Q3. ทำไม SMOTE ต้องทำหลัง scaling (หรือ normalize เอง)
> SMOTE หาเพื่อนบ้านด้วยระยะทาง (KNN) → ถ้าไม่ scale ตัวแปรหน่วยใหญ่ครองระยะทาง เพื่อนบ้านที่ได้ไม่สมเหตุสมผล · scaler ก็ต้อง fit บน training fold เท่านั้น

> [!question]- Q4. หลัง SMOTE โมเดลได้ recall เพิ่มแต่ precision ลด อธิบาย
> training มี minority มากขึ้น → โมเดลทาย minority ง่ายขึ้น → จับ positive ได้มากขึ้น (TP ↑ FN ↓) แต่ทายผิดเป็น positive มากขึ้นด้วย (FP ↑)

> [!question]- Q5. นอกจาก resampling มีวิธีอื่นรับมือ imbalanced อะไรบ้าง
> cost-sensitive learning (cost matrix / class_weight) · ใช้ ensemble (RF, boosting) · ปรับ threshold · ใช้ metric ที่เหมาะ (F1, recall, AUC)

---

**กลับหน้าหลัก →** [[LEC 00 START HERE]] · **ถัดไป →** [[LEC 05 Model Construction & Evaluation]]
