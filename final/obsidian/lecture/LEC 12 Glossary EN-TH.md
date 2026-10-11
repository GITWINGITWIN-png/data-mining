---
title: LEC 12 · Glossary EN–TH
exam: Lecture — จ. 19 ต.ค. 2569 16:00–19:00
tags: [final, lecture, glossary]
---

# LEC 12 · Glossary EN–TH
### ศัพท์ของเนื้อหา Final + คู่ที่สับสนบ่อย (ศัพท์มิดเทอม: [[11 Glossary EN-TH]])

**ลิงก์:** [[LEC 00 START HERE|หน้าหลัก Lecture]] · [[LEC 11 Formula Sheet]]

## Evaluation
| EN | TH / ความหมายสั้น |
|---|---|
| Training / Validation / Test set | ชุดฝึก (fit) / ชุดเลือกโมเดล-พารามิเตอร์ / ชุดวัดผลสุดท้าย |
| Hold-out | แบ่งครั้งเดียว (เช่น 80/20) |
| k-fold Cross-Validation | แบ่ง k ส่วน วน k รอบ เฉลี่ยผล |
| Stratified | รักษาสัดส่วนคลาสในทุกส่วน |
| LOOCV | k = n · test ทีละ 1 แถว |
| Random sub-sampling | hold-out ซ้ำหลายครั้งแล้วเฉลี่ย |
| Baseline (majority / naive rule) | โมเดลขั้นต่ำ: ทายคลาสส่วนมาก / ค่าเฉลี่ย |
| Hyperparameter | ค่าที่ตั้งก่อน train (k, max_depth) — ต่างจาก parameter ที่โมเดลเรียน (coefficient) |
| Confusion matrix | ตาราง actual × predicted |
| TP / FP / FN / TN | ทายบวกถูก / ทายบวกผิด (false alarm) / ทายลบผิด (false dismissal) / ทายลบถูก |
| Precision / Recall / F1 | ความแม่นของการทายบวก / ความครอบคลุมของบวกจริง / ค่าเฉลี่ยฮาร์มอนิก |
| Specificity | อัตราทายลบถูก |
| Threshold / Cutoff | จุดตัดความน่าจะเป็น |
| ROC / AUC | กราฟ TPR–FPR / พื้นที่ใต้กราฟ |
| Overfitting / Underfitting | จำข้อมูลฝึกเกิน / โมเดลง่ายเกิน |

## Models
| EN | TH / ความหมายสั้น |
|---|---|
| Lazy / Instance-based learner | เก็บข้อมูลไว้ คำนวณตอนทาย (KNN) |
| Eager learner | สร้างโมเดลก่อน (tree, logistic) |
| Curse of dimensionality | มิติมาก ระยะทางไร้ความหมาย ต้องใช้ข้อมูลเพิ่มแบบเอกซ์โพเนนเชียล |
| Odds / Log-odds (logit) | p/(1−p) / ln ของ odds |
| Sigmoid | ฟังก์ชัน S แปลง z เป็น p ∈ (0, 1) |
| Maximum likelihood | หาพารามิเตอร์ที่ทำให้ข้อมูลที่เห็นมีโอกาสเกิดสูงสุด |
| Odds ratio | $e^b$ — odds คูณเท่าไรเมื่อ x +1 |
| Impurity (Gini, Entropy) | ความไม่บริสุทธิ์ของ node |
| Information gain | entropy ที่ลดได้จากการ split |
| Gain ratio / Split info | IG ปรับด้วยจำนวน/ขนาด child |
| Pre-pruning / Post-pruning | หยุดตั้งแต่สร้าง / ตัดกิ่งหลังสร้างเต็ม |
| Greedy | เลือกดีที่สุดทีละขั้น ไม่ย้อนกลับ |
| Ensemble / Bagging / Bootstrap | รวมหลายโมเดล / สุ่มแบบใส่คืนแล้วรวม / สุ่มแบบใส่คืน |
| OOB (out-of-bag) | แถวที่ไม่ถูกสุ่มเข้าต้นนั้น ใช้ประเมินต้นนั้น |
| Feature importance | ความสำคัญของ feature (impurity ที่ลดรวม) |

## Preprocessing / PCA / Imbalance
| EN | TH / ความหมายสั้น |
|---|---|
| Imputation | เติมค่าว่าง |
| Standardization / Normalization | z-score / min-max |
| One-hot / Dummy / Ordinal encoding | แปลงหมวดเป็น 0/1 หลายคอลัมน์ / แบบ k−1 / เป็นลำดับ |
| Discretization (binning) | แปลงตัวเลขเป็นช่วง |
| Filter / Wrapper / Embedded | เลือก feature ด้วยสถิติ / ด้วยโมเดล / ระหว่างสร้างโมเดล |
| Redundant / Irrelevant feature | ซ้ำกับตัวอื่น / ไม่เกี่ยวกับ target |
| Data leakage / Target leakage | ข้อมูลนอก train รั่วเข้ามา / feature ที่รู้หลังผลลัพธ์ |
| Principal component / Loading / Score | ตัวแปรใหม่ / น้ำหนักของตัวแปรเดิม / ค่าของแต่ละแถวบน PC |
| Explained variance (ratio) | สัดส่วนความแปรปรวนที่ PC เก็บได้ |
| Eigenvalue / Eigenvector | ความแปรปรวนของ PC / ทิศของ PC (loadings) |
| Scree plot / Kaiser rule | กราฟ % variance ต่อ PC / เก็บ λ > 1 |
| Majority / Minority class | คลาสส่วนมาก / ส่วนน้อย |
| Imbalance ratio (IR) | majority ÷ minority |
| RUS / ROS / SMOTE / Near-Miss | สุ่มตัด majority / สุ่มซ้ำ minority / สังเคราะห์ minority / ตัด majority แบบเลือก |
| Cost-sensitive learning / Cost matrix | ให้ต้นทุนความผิดพลาดต่างกัน |
| Accuracy paradox | accuracy สูงแต่ไร้ประโยชน์เพราะทายคลาสใหญ่ |

## Clustering / Association
| EN | TH / ความหมายสั้น |
|---|---|
| Unsupervised learning | เรียนรู้โดยไม่มี label |
| Centroid / Medoid | จุดเฉลี่ยของกลุ่ม / จุดจริงที่เป็นตัวแทน |
| WCSS / SSE / inertia | ผลรวมระยะ² ถึง centroid |
| Elbow method | หาจุดที่ WCSS เริ่มแบน |
| Silhouette | วัดความแน่น + ความแยก (−1 ถึง 1) |
| Cohesion / Separation | ความแน่นในกลุ่ม / ความห่างระหว่างกลุ่ม |
| Interpretability | อธิบายความหมายของกลุ่มได้ |
| K-Means++ | วิธีเลือก seed ให้กระจาย |
| Local optimum | คำตอบดีเฉพาะที่ (ขึ้นกับ seed) |
| Transaction / Itemset / k-itemset | ตะกร้า / เซตสินค้า / เซตขนาด k |
| Antecedent (premise) / Consequent (conclusion) | ฝั่งซ้าย / ฝั่งขวาของกฎ |
| Support count / Support | จำนวน / สัดส่วน transaction ที่มี itemset |
| Confidence / Lift | P(Y\|X) / confidence เทียบ P(Y) |
| Frequent (large) itemset | itemset ที่ support ≥ minsup |
| Candidate itemset (Cₖ) / Lₖ | ชุดที่ต้องนับ / ชุดที่ผ่าน minsup |
| Apriori principle (anti-monotone) | subset ของ frequent ต้อง frequent |
| Join / Prune | รวม L(k−1) เป็น Cₖ / ตัด candidate ที่ subset ไม่ frequent |
| FP-Growth | หา frequent itemsets ด้วย FP-tree (ไม่สร้าง candidate) |

---

## ⚠️ คู่ที่สับสนบ่อยที่สุด
| คู่ | จำว่า |
|---|---|
| **Precision vs Recall** | precision = "ที่**ทาย**ว่าใช่ ถูกกี่ %" (ตัวหาร = TP + **FP**) · recall = "ที่**ใช่จริง** เจอกี่ %" (ตัวหาร = TP + **FN**) |
| **Validation vs Test** | validation = ใช้**เลือก** · test = ใช้**รายงาน** ครั้งเดียว |
| **Standardization vs Normalization** | z-score (mean 0, sd 1) vs min-max ([0, 1]) |
| **Parameter vs Hyperparameter** | โมเดลเรียนเอง (coef, centroid) vs เราตั้ง (k, depth) |
| **Pre- vs Post-pruning** | หยุดระหว่างสร้าง vs ตัดหลังสร้างเสร็จ |
| **Information Gain vs Gain Ratio** | IG ชอบ attribute ค่าเยอะ · GR หารด้วย SplitInfo แก้ปัญหานี้ |
| **Gini vs Entropy** | max 0.5 vs max 1 (2 คลาส) · ได้ tree คล้ายกัน |
| **Bagging (RF) vs tree เดี่ยว** | หลายต้นสุ่มแถว + feature → variance ต่ำ |
| **ROS vs SMOTE** | copy จุดเดิม vs สร้างจุดใหม่บนเส้น |
| **RUS vs ROS** | ตัด majority vs เพิ่ม minority |
| **Cohesion vs Separation** | ในกลุ่มใกล้ (ต่ำดี) vs ระหว่างกลุ่มห่าง (สูงดี) |
| **Clustering vs Classification** | ไม่มี label (หากลุ่ม) vs มี label (ทายคลาส) |
| **Clustering vs Association** | "อะไรอยู่ด้วยกัน" (แถว) vs "อะไรเกิดด้วยกัน" (item) |
| **Support vs Confidence** | สัดส่วนของ **ทุก** transaction vs สัดส่วนใน transaction ที่มี **X** |
| **Confidence vs Lift** | P(Y\|X) vs P(Y\|X)/P(Y) — lift เทียบกับฐาน |
| **Loading vs Score (PCA)** | น้ำหนักของตัวแปร (ต่อ PC) vs ค่าของแต่ละแถว (ต่อ PC) |
| **Feature selection vs extraction** | เลือกตัวเดิม (ตีความได้) vs สร้างตัวใหม่ (PCA) |
| **Lazy vs Eager** | KNN (คำนวณตอนทาย) vs tree (สร้างโมเดลก่อน) |
| **Odds vs Probability** | p/(1−p) vs p · p = 0.5 → odds = 1 |

---

**กลับหน้าหลัก →** [[LEC 00 START HERE]]
