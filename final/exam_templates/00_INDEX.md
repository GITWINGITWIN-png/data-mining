# 📇 INDEX: โจทย์ถามอะไร → เปิดไฟล์ไหน § ไหน

> สมุด index สำหรับสอบ Lab (จ. 12 ต.ค. 2569 09:00–12:00 · E11-S603)
> อ่านโจทย์ → หา **คำในโจทย์** ในหน้านี้ → เปิด `Txx` → ไปที่ **§** → ทำตาม [01_MANUAL.md](01_MANUAL.md)
> ตำแหน่ง ✏️ ทั้งหมดของทุกไฟล์อยู่ใน [02_CELL_MAP.md](02_CELL_MAP.md)

---

## 0 · ตัดสินใจใน 10 วินาที

```
โจทย์ให้ข้อมูลมา
│
├─ ไม่มีคอลัมน์คำตอบ (label)
│   ├─ "แบ่งกลุ่ม / segment / cluster / K-Means / centroid"            → T10 Clustering
│   └─ "ซื้อด้วยกัน / ตะกร้า / transaction / itemset / rule / lift"      → T11 Association Rules
│
├─ มี label เป็น "ตัวเลข" (ราคา, ค่าใช้จ่าย, คะแนน)                       → T06 Linear Regression
│   └─ ถามว่า "KNN ทำนายตัวเลข"                                          → T05 §7
│
├─ มี label เป็น "หมวด/คลาส" (Yes/No, ชนิด, ผ่าน/ไม่ผ่าน)
│   ├─ ให้ลองหลายโมเดล / baseline / optimize / เลือกโมเดล               → T09 Workflow (ไฟล์หลัก)
│   ├─ เจาะจง KNN (ระยะทาง, k, scale)                                   → T05 KNN
│   ├─ เจาะจง Logistic (probability, threshold, coefficient)            → T07 Logistic
│   ├─ เจาะจง Decision Tree / Random Forest (gini, entropy, depth)      → T08 Tree & RF
│   └─ คลาสไม่สมดุล / SMOTE / undersampling / oversampling              → T04 Imbalanced
│
└─ ไม่ได้ให้สร้างโมเดล แค่จัดการข้อมูล
    ├─ import, ตรวจ, select, filter, set role, join, concat, pivot, กราฟ  → T01 Data Handling
    ├─ missing, outlier, encoding, scaling, discretize, sampling, leak     → T02 Preprocessing
    └─ PCA, ลดมิติ, explained variance, loadings, plot 2 มิติ               → T03 PCA
```

---

## 1 · ไฟล์ทั้งหมด

| ไฟล์ | เรื่อง | ข้อมูลตัวอย่างที่ใส่ไว้ |
|---|---|---|
| **T01** `T01_data_handling_viz.ipynb` | Import · Inspect · Select · Filter · Set Role · Concatenate · Join · Aggregate · Pivot · Generate · กราฟ · Correlation | tips (3 ไฟล์ สำหรับ concat/join) |
| **T02** `T02_preprocessing.ipynb` | Missing · Outlier · Encoding · Scaling · Discretization · Sampling · Split ไม่ leak · Feature selection | penguins |
| **T03** `T03_pca.ipynb` | PCA · explained variance · จำนวน PC · loadings · 2D plot · biplot · PCA ก่อนโมเดล | wine |
| **T04** `T04_imbalanced_smote.ipynb` | Under/Over/SMOTE/class_weight · SMOTE ใน fold · leakage demo · threshold · เลือก metric | breast cancer (imbalanced) |
| **T05** `T05_knn.ipynb` | ระยะทางด้วยมือ · vote · hold-out · scale ก่อน/หลัง · เลือก k · ทำนาย · KNN regression | riding mowers (+ housing) |
| **T06** `T06_linear_regression.ipynb` | สมการ · coefficient · simple/multiple · MAE/MSE/RMSE/R² · baseline · เทียบโมเดล · ทำนาย | insurance |
| **T07** `T07_logistic_regression.ipynb` | probability · sigmoid ด้วยมือ · odds ratio · threshold · ROC · tune C · ทำนาย | pima diabetes |
| **T08** `T08_decision_tree_rf.ipynb` | Gini/Entropy/Gain/Gain ratio ด้วยมือ · วาดต้นไม้ · กฎ IF-THEN · overfitting · tune · RF · ทำนาย | heart (+ weather) |
| **T09** `T09_classification_workflow.ipynb` | Workflow ครบ: baseline → 4 โมเดล → optimize → ก่อน/หลัง → เลือก → ทำนาย | bank-data (pep) |
| **T10** `T10_clustering.ipynb` | เตรียมข้อมูล · เลือก k (elbow/silhouette/DB) · centroid/profile · จุดใหม่ · cohesion/separation · PCA plot · dendrogram · K-Means มือ | utilities (+ จุด A1–A9) |
| **T11** `T11_association_rules.ipynb` | แปลง transaction · item ขายดี · frequent itemsets · Apriori/FP-Growth · rules · support/conf/lift · ผลของ min support · Apriori มือ | groceries (+ BeautyCo, bank) |

---

## 2 · ตาม Lab Examination Guideline (69_1_Guideline.pdf) ข้อต่อข้อ

### Data Handling and Visualization
| หัวข้อในประกาศ | ไฟล์ § |
|---|---|
| Import และตรวจสอบข้อมูล | **T01 §1** (ทุกไฟล์ §1 ก็ทำให้) |
| ใช้ pandas, NumPy, matplotlib, scikit-learn | ทุกไฟล์ (cell 🔧 import ไว้หมดแล้ว) |
| สร้าง basic charts และตีความ | **T01 §9** (hist/box/count/scatter + stacked bar) · **T01 §10** (heatmap) |
| Select attributes | **T01 §2** |
| Filter examples | **T01 §3** |
| Set role (id / label) | **T01 §2** (ส่วนล่าง) · ในโมเดล = `ID_COL`, `TARGET` ใน CONFIG |
| Join | **T01 §5** |
| Concatenate / Append | **T01 §4** |
| Pivot | **T01 §7** (pivot_table + crosstab + สัดส่วนคลาส `RATE_OF`) |
| Aggregate / Group by | **T01 §6** |

### Data Preprocessing
| หัวข้อ | ไฟล์ § |
|---|---|
| Missing-value handling | **T02 §1–§2** · ค่า 0 ที่เป็นไปไม่ได้ → `ZERO_AS_MISSING` (T02, T07) |
| Outliers | **T02 §3** |
| Encoding categorical | **T02 §4** (one-hot / ordinal / binary map) |
| Standardization / Normalization | **T02 §5** · เทียบผลก่อน/หลัง scale: **T02 §8** (cell 2), **T05 §4** |
| Discretization | **T02 §6** (equal width / equal frequency / กำหนดเอง) · สำหรับ association: **T11** `BINS` |
| Sampling | **T02 §7** (random / stratified) |
| SMOTE / under / over sampling | **T04 §3–§5** |
| PCA + 2D visualization | **T03 §2–§4** · PCA ก่อนโมเดล **T03 §5** · cluster บน PCA **T10 §6** |
| แบ่งข้อมูลไม่ให้ leak | **T02 §8** ⭐ · SMOTE ผิดวิธี **T04 §6** · Feature selection ใน pipeline **T02 §9** |

### Model Construction and Evaluation
| หัวข้อ | ไฟล์ § |
|---|---|
| สร้าง baseline model | **T09 §3–§4** · T04 §2 · T05 §4 · T06 §5 (mean baseline) · T08 §6 |
| Hold-out หรือ cross-validation | `EVAL_MODE` ใน CONFIG (T04, T05, T06, T08, T09) · **T09 §2** อธิบาย |
| Optimize parameters | **T09 §5** (ทุกโมเดล) · T05 §5 (k) · T07 §6 (C) · T08 §4 (depth/leaf/criterion) · T06 §6 (regression) |
| เปรียบเทียบก่อน/หลัง preprocessing | **T02 §8** (ไม่ scale vs z vs min-max) · **T05 §4** · T03 §5 (PCA) · T04 §4 (resampling) |
| เปรียบเทียบก่อน/หลัง optimization | **T09 §6** ⭐ · T07 §6 · T08 §6 |
| K-NN | **T05** |
| Linear Regression | **T06** |
| Logistic Regression | **T07** |
| Decision Tree (+ Random Forest) | **T08** |
| Clustering | **T10** |
| Association Rules | **T11** |
| อ่าน/อธิบายผลจากกราฟ ตาราง metrics | บรรทัด `✍️` ที่พิมพ์ออกมาทุก § + cell **✍️ คำตอบ** (แม่แบบประโยค) |

---

## 3 · ค้นจากคำในโจทย์ (EN / TH)

| คำในโจทย์ | ไฟล์ § |
|---|---|
| accuracy, precision, recall, F1, confusion matrix | `show_cm()` · T09 §7 · T07 §5 · T04 §5 |
| accuracy หลอก / imbalanced metric | T04 §2, §8 |
| adjusted rand index / เทียบ cluster กับ label | T10 §8 |
| aggregate, group by, ค่าเฉลี่ยตามกลุ่ม | T01 §6 |
| antecedent / consequent / LHS / RHS | T11 §4 |
| append, concatenate, ต่อแถว, union | T01 §4 |
| Apriori ทีละขั้น, C1 L1 C2 L2, candidate, prune | T11 §7 |
| baseline, majority, ZeroR, default model | T09 §4 · T04 §2 · T06 §5 |
| bar chart, boxplot, histogram, scatter | T01 §9 |
| biplot | T03 §4 |
| binning, discretize, แบ่งช่วง, equal width / frequency | T02 §6 · T11 (`BINS`) |
| centroid, profile, ตั้งชื่อกลุ่ม | T10 §3 |
| class_weight, cost-sensitive | T04 §4 · T09 `GRIDS` |
| coefficient, intercept, สมการ (linear) | T06 §3–§4 |
| coefficient, odds ratio (logistic) | T07 §3 |
| cohesion, separation, WCSS, SSE | T10 §2, §5 |
| correlation, heatmap, ความสัมพันธ์ | T01 §10 · T06 §1 (กับ target) |
| crosstab, สัดส่วนคลาสตามกลุ่ม | T01 §7, §9 (stacked bar) |
| cross-validation, k-fold | `EVAL_MODE="cv"` · T09 §2 |
| Davies–Bouldin | T10 §2 |
| dendrogram, hierarchical, linkage | T10 §7 |
| distance, Euclidean, Manhattan, ระยะทางด้วยมือ | T05 §2 |
| elbow, เลือกจำนวน cluster | T10 §2 |
| encoding, one-hot, dummy, label encoding | T02 §4 |
| entropy, gini, information gain, gain ratio | T08 §0 |
| explained variance, scree, จำนวน PC | T03 §2 |
| feature importance | T08 §2, §5 |
| feature selection, SelectKBest, ตัด feature | T02 §9 (คะแนน) · §9b (ตัดจริง + save) |
| filter, เงื่อนไข, query | T01 §3 |
| FP-Growth | T11 (`ALGO="fpgrowth"`) |
| frequent itemsets, min support | T11 §3 |
| GridSearch, tune, optimize, hyper-parameter | T09 §5 · T05 §5 · T07 §6 · T08 §4 |
| hold-out, train/test split | `EVAL_MODE="holdout"` · T02 §8 |
| IF-THEN rules (tree) | T08 §2 |
| join, merge, lookup, inner/left/outer | T01 §5 |
| k ที่ดีที่สุด (KNN) | T05 §5 |
| K-Means ด้วยมือ, initial centroid, iteration | T10 §9 |
| K-Means, n_init, max_iter | T10 §3 (CONFIG `N_INIT`, `MAX_ITER`) |
| leakage, ห้าม scale/SMOTE ก่อน split | T02 §8 · T04 §6 |
| lift, confidence, support (ตีความ) | T11 §4–§5 |
| loadings, PC ไหนมาจากตัวแปรไหน | T03 §3 |
| MAE, MSE, RMSE, R² | T06 §5 · T05 §7 (KNN reg) |
| max_depth, min_samples_leaf, overfitting | T08 §3–§4 |
| min confidence / min support เปลี่ยนแล้วเกิดอะไร | T11 §6 |
| missing values, ค่าว่าง, `?` | T02 §1–§2 |
| new data, ข้อมูลใหม่, ทำนาย, predict | `NEW_DATA` / `NEW_POINT` ใน CONFIG: T05 §6 · T06 §7 · T07 §7 · T08 §7 · T09 §8 · T10 §4 · T03 §6 |
| normalization, min-max, z-score, standardize | T02 §5 |
| outlier, IQR | T02 §3 · T01 §9 (นับ) |
| PCA, ลดมิติ | T03 |
| pivot table | T01 §7 |
| probability, sigmoid, predict_proba | T07 §4, §7 |
| Random Forest, n_estimators | T08 §5 · T09 |
| regression อื่น (KNN/Tree/RF reg) | T06 §6 · T05 §7 |
| ROC, AUC | T07 §5 |
| sampling, สุ่มตัวอย่าง, stratified sample | T02 §7 |
| select attributes, ตัดคอลัมน์ | T01 §2 |
| set role, id, label | T01 §2 · CONFIG `ID_COL` / `TARGET` |
| silhouette | T10 §2, §5 |
| SMOTE, oversampling, undersampling | T04 §3–§5 |
| summary statistics, describe, skew | T01 §1 |
| threshold (logistic) | T07 §5 · T04 §7 |
| ตะกร้าสินค้า, market basket, transaction | T11 §1 |
| ทำนายกลุ่มของจุดใหม่ (cluster) | T10 §4 |

---

## 4 · โจทย์คำนวณมือ (ใช้ตรวจคำตอบ / แสดงวิธีทำ)

| โจทย์ | ไฟล์ § | แก้อะไร |
|---|---|---|
| ระยะ Euclidean/Manhattan → k เพื่อนบ้าน → vote | T05 §2 | `DATA_PATH`, `NEW_POINT`, `K`, `METRIC`, `SCALE=None` ถ้าโจทย์ไม่ scale |
| Entropy / Gini / Gain / Gain ratio เลือก root | T08 §0 | `IMP_PATH`, `IMP_TARGET`, `IMP_DROP` |
| ความน่าจะเป็น logistic จากสมการ | T07 §4 | แถวแรกของ test (หรือแก้ในเซลล์) |
| สมการ linear regression / ทำนายค่า | T06 §3–§4, §7 | `SIMPLE_X`, `NEW_DATA` |
| K-Means ทีละรอบ (seed ที่โจทย์ให้) | T10 §9 | `HAND_POINTS`, `HAND_INIT` |
| Apriori ทีละขั้น + support/confidence/lift | T11 §7 | `SMALL_TRANSACTIONS`, `SMALL_MINSUP`, `SMALL_MINCONF` |
| support/confidence/lift ของกฎ 1 ข้อ | T11 §5 | `RULE_TO_EXPLAIN` |
| PCA: แปลงจุดใหม่เป็น PC score | T03 §6 | `NEW_POINT` |

---

## 5 · โจทย์แบบผสม (ข้อสอบจริงมักมาหลายส่วน)

| โจทย์แบบ | ลำดับไฟล์ |
|---|---|
| "join/concat ไฟล์ แล้วสร้างโมเดลทำนาย" | T01 §4–§5 → `df.to_csv` (T01 §11) → ใส่ไฟล์ที่ได้เป็น `DATA_PATH` ของ T09 |
| "preprocess แล้วเทียบก่อน/หลัง" | T02 §1–§8 (หรือ T05 §4 สำหรับ KNN) |
| "ข้อมูลไม่สมดุล สร้างโมเดลที่ดีที่สุด" | T04 (เลือกวิธี resample) → T09 `USE_SMOTE=True`, `PRIMARY_METRIC="f1"` หรือ `"recall"` |
| "PCA แล้วเอาไปทำโมเดล / cluster" | T03 §5 (โมเดล) · T10 §6 (cluster บน PCA) |
| "cluster แล้วอธิบายกลุ่ม แล้วหากฎ" | T10 → บันทึก `t10_clusters.csv` → T11 `FORMAT="table"`, `BINS` ตามต้องการ |
| "หลายโมเดล + optimize + เลือก + ทำนายข้อมูลใหม่" | T09 ทั้งไฟล์ |

---

## 6 · ถ้าโจทย์บังคับ RapidMiner

> ⭐ **ชุด process สำเร็จรูป R01–R11 (เลขบท/§ ตรงกับ T01–T11):** [`../rm_templates/00_INDEX.md`](../rm_templates/00_INDEX.md) · คู่มือ [`../rm_templates/01_MANUAL.md`](../rm_templates/01_MANUAL.md)

| ต้องการ | เปิด |
|---|---|
| process สำเร็จรูป (.rmp) Import ผ่าน File → Import Process | `../mock_lab/recipes/*.rmp` (join/pivot, PCA, KNN+CV, optimize k, logreg threshold, tree vs RF, elbow, k-means, FP-Growth, linreg, SMOTE) |
| ไกด์ทีละขั้นพร้อมภาพ canvas | `../obsidian/practice/PR 01–09 (RapidMiner).md` |
| สรุปทฤษฎี / สูตร / คำอธิบาย | `../obsidian/lab/LAB 09 Cheat Sheet.md` · `../obsidian/lecture/LEC 11 Formula Sheet.md` |
