# 📇 INDEX (RapidMiner): โจทย์ถามอะไร → เปิด process ไหน § ไหน

> คู่กับชุด Python `../exam_templates/` (T01–T11): **R01–R11 ใช้เลขบทและเลข § เดียวกัน**
> อ่านโจทย์ → หาคำในหน้านี้ → Import `Rxx_….rmp` → ไปที่แถว § บน canvas (โน้ตเหลือง) → ทำตาม [01_MANUAL.md](01_MANUAL.md)
> ทุก operator / parameter ของทุกไฟล์: [02_OPERATOR_MAP.md](02_OPERATOR_MAP.md)

---

## 0 · ตัดสินใจใน 10 วินาที

```
มี label ไหม?
├─ ไม่มี: "แบ่งกลุ่ม / k-Means / centroid"                 → R10 Clustering
│         "ซื้อด้วยกัน / itemset / rule / lift"             → R11 Association Rules
├─ label เป็นตัวเลข                                        → R06 Linear Regression (KNN regression → R05 §7)
├─ label เป็นคลาส
│   ├─ หลายโมเดล / baseline / optimize / เลือกโมเดล       → R09 Workflow
│   ├─ KNN (ระยะทาง, k, normalize)                         → R05
│   ├─ Logistic (threshold, coefficient)                    → R07
│   ├─ Decision Tree / Random Forest / gain                 → R08
│   └─ ไม่สมดุล / SMOTE / undersample                       → R04
└─ ไม่สร้างโมเดล: import / select / filter / join / append / pivot → R01
                  missing / encoding / normalize / discretize / sample / leak → R02
                  PCA / 2D                                     → R03
```

## 1 · ไฟล์ทั้งหมด

| ไฟล์ | แถว (§) บน canvas | ข้อมูลตัวอย่าง |
|---|---|---|
| **R01** `R01_data_handling.rmp` | §1 Import · §4 Append · §5 Join · §2 Select + Set Role · §3 Filter · §6 Aggregate · §7 Pivot · §8 Generate · §9 Sort/Sample · §10 Correlation | tips 3 ไฟล์ |
| **R02** `R02_preprocessing.rmp` | §2 Replace Missing / ตัดแถว · §3 Outlier · §4 Nominal→Numerical · §5 Normalize Z / 0–1 · §6 Discretize 3 แบบ · §7 Sample / Stratified · §8 Split ไม่ leak + เทียบก่อน/หลัง · §9 Feature selection | penguins |
| **R03** `R03_pca.rmp` | §2–3 PCA keep variance (eigenvalues/loadings) · §4 PCA 2D · §5 kNN ก่อน/หลัง PCA ใน CV | wine |
| **R04** `R04_imbalanced_smote.rmp` | §1 ดูสัดส่วน · §2 baseline · §4 Tree / Undersample / SMOTE ใน CV · §6 ❌ SMOTE ก่อน CV | breast cancer |
| **R05** `R05_knn.rmp` | §2 Cross Distances (ระยะถึงจุดใหม่) · §3 hold-out · §4 baseline vs raw vs normalize · §5 optimize k · §6 ทำนายจุดใหม่ · §7 KNN regression | riding mowers + housing |
| **R06** `R06_linear_regression.rmp` | §3 simple LR · §4–5 multiple LR + baseline (hold-out) · §6 LR vs kNN vs Tree (CV) · §7 ทำนาย | insurance |
| **R07** `R07_logistic_regression.rmp` | §1–3 split + LR (coefficients) · §5 threshold default / 0.5 / 0.3 · §2/§6 baseline vs LR (CV) · §7 ทำนาย | pima |
| **R08** `R08_decision_tree_rf.rmp` | §0 Weight by Info Gain / Gain Ratio / Gini (root) · §2 ต้นไม้ + กฎ · §3 train acc (overfit) · §6 baseline vs tree vs RF · §4 optimize depth · §5 RF ทำนาย | weather + heart |
| **R09** `R09_classification_workflow.rmp` | §4 baseline vs kNN / LogReg / Tree / RF (CV) · §5 optimize kNN k + Tree depth × criterion · §6–8 โมเดลสุดท้าย → ทำนาย | bank-data (pep) |
| **R10** `R10_clustering.rmp` | §3 k-Means + performance + centroid · §3b profile · §2 elbow (k = 2…10) · §4 จุดใหม่ · §6 PCA 2D · §7 hierarchical + flatten | utilities |
| **R11** `R11_association_rules.rmp` | A ตาราง 0/1 (Excel) · B ตารางลูกค้า → discretize → binominal · C 0/1 ใหญ่ (CSV) → FP-Growth → Rules | BeautyCo · bank · groceries |

## 2 · ตาม Lab Examination Guideline

| หัวข้อ | RapidMiner (operator) | ไฟล์ § |
|---|---|---|
| Import และตรวจข้อมูล | Read CSV / Read Excel → Results: Statistics | R01 §1 |
| สร้าง basic charts + ตีความ | Results → **Visualizations** (Histogram, Boxplot, Bar, Scatter) | R01 res 1 (ทุกไฟล์ที่ต่อข้อมูลออก res) |
| Select attributes | Select Attributes | R01 §2 |
| Filter examples | Filter Examples (custom_filters) | R01 §3 |
| Set role | Set Role | R01 §2 · ทุกไฟล์ |
| Join | Join | R01 §5 |
| Concatenate | Append | R01 §4 |
| Pivot | Pivot (+ Generate Attributes สำหรับสัดส่วน) | R01 §7 |
| Missing values | Declare Missing Value · Replace Missing Values · Filter Examples (is_not_missing) | R02 §2 · R07 |
| Encoding | Nominal to Numerical (dummy / unique integers) · Nominal to Binominal · Numerical to Binominal | R02 §4 · R06 · R11 |
| Standardization / normalization | Normalize (Z-transformation / range transformation) | R02 §5 |
| Discretization | Discretize by Binning / Frequency / User Specification | R02 §6 · R11 B |
| Sampling | Sample · Sample (Stratified) | R02 §7 |
| SMOTE | SMOTE Upsampling (Operator Toolbox) ใน Training pane | R04 §4c |
| PCA + 2D | Normalize → PCA → Visualizations Scatter | R03 · R10 §6 |
| แบ่งข้อมูลไม่ leak | Split Data + Apply Model (preprocessing model) · preprocessing ใน Training pane ของ CV | R02 §8 · R04 · ทุก CV |
| Baseline | Default Model (mode / average) | R09 §4 · R04 §2 · R05 §4 · R06 §4 · R07 · R08 §6 |
| Hold-out / CV | Split Data · Cross Validation | R05 §3 / §4 · R06 · R07 |
| Optimize parameters | Optimize Parameters (Grid) + Log + Log to Data | R05 §5 · R08 §4 · R09 §5 · R10 §2 |
| ก่อน/หลัง preprocessing | 2 CV คู่กัน (ไม่มี vs มี operator ใน Training pane) | R02 §8b · R03 §5 · R05 §4 · R04 §4 |
| ก่อน/หลัง optimization | CV default vs Optimize (parameter set) | R09 §4 vs §5 · R08 §6 vs §4 |
| K-NN | k-NN | R05 |
| Linear Regression | Linear Regression + Performance (Regression) | R06 |
| Logistic Regression | Logistic Regression (H2O) + Create/Apply Threshold | R07 |
| Decision Tree | Decision Tree · Random Forest | R08 |
| Clustering | k-Means + Cluster Distance Performance · Agglomerative + Flatten | R10 |
| Association Rules | FP-Growth + Create Association Rules | R11 |

## 3 · ค้นจากคำในโจทย์

| คำในโจทย์ | ไฟล์ § |
|---|---|
| accuracy / precision / recall / F1 / confusion matrix | Performance (Binominal) ทุกไฟล์ → res → แท็บ **Description/Table** |
| AUC / ROC | คลิก Performance (Binominal) → ติ๊ก `AUC` แล้ว Run ใหม่ (res มีกราฟ ROC) · หรือ Python T07 §5 |
| baseline | Default Model (R09 §4) |
| centroid / profile | R10 §3 (cluster model → Centroid Table) · §3b |
| cohesion / Davies–Bouldin | R10 §3 (Cluster Distance Performance) |
| correlation | R01 §10 |
| cross distances / ระยะทางถึงจุดใหม่ | R05 §2 |
| dendrogram / hierarchical | R10 §7 |
| discretize / binning | R02 §6 · R11 B |
| elbow / เลือก k (cluster) | R10 §2 |
| feature selection / weight | R02 §9 · R08 §0 |
| filter | R01 §3 |
| FP-Growth / frequent itemsets | R11 |
| gain / gini / gain ratio / root | R08 §0 |
| hold-out / Split Data | R05 §3 · R06 §4 · R07 · R02 §8 |
| join / append | R01 §4–§5 |
| k ที่ดีที่สุด | R05 §5 · R09 §5 |
| leakage / SMOTE ก่อน split | R04 §6 · R02 §8 |
| lift / confidence / support | R11 (rules table) |
| max depth / overfitting | R08 §3–§4 |
| missing values | R02 §2 |
| new data / ทำนาย | R05 §6 · R06 §7 · R07 §7 · R08 §5 · R09 §6–8 · R10 §4 |
| normalize / z-score / min-max | R02 §5 |
| one-hot / dummy | R02 §4 · R06 |
| outlier | R02 §3 |
| PCA | R03 |
| pivot / aggregate | R01 §6–§7 |
| RMSE / MAE / R² | Performance (Regression) R06 · R05 §7 (R² = squared_correlation) |
| sample / stratified | R02 §7 |
| SMOTE / undersample | R04 |
| threshold | R07 §5 |

## 4 · ทำใน RapidMiner ไม่ได้ / ไม่สะดวก → ใช้ Python

| โจทย์ | ใช้ |
|---|---|
| Apriori ทีละขั้น (C1 → L1 → C2 …) | Python T11 §7 |
| K-Means ทีละรอบจาก seed ที่กำหนด | Python T10 §9 |
| ข้อมูลตะกร้าแบบ `milk,bread,eggs` ต่อบรรทัด | Python T11 (หรือแปลงเป็นตาราง 0/1 แล้วใช้ R11 A/C) |
| คำนวณ probability logistic ด้วยมือ | Python T07 §4 |
| ประโยคตีความสำเร็จรูป | Python ทุกไฟล์ (บรรทัด ✍️) |
