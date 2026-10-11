# 📘 MANUAL (RapidMiner): วิธีใช้ process R01–R11

> หา process จากคำในโจทย์: [00_INDEX.md](00_INDEX.md) · ทุก operator / parameter: [02_OPERATOR_MAP.md](02_OPERATOR_MAP.md)
> ชุด Python คู่กัน: [../exam_templates/01_MANUAL.md](../exam_templates/01_MANUAL.md)

---

## ส่วนที่ 1 · เตรียมก่อนสอบ (คืนนี้)

1. `git pull` ให้มีโฟลเดอร์ `final/rm_templates/`
2. **ทดสอบทั้งชุดในคำสั่งเดียว** (ใช้สคริปต์ batch เดิมที่เคยใช้):
   ```bash
   bash final/mock_lab/run_rm.sh final/rm_templates/*.rmp
   ```
   ต้องขึ้น ✓ ครบ 11 ไฟล์ · ถ้า ✗ ให้ดูข้อความ error ใต้ชื่อไฟล์ (ส่วนที่ 6)
3. **Import ทีละไฟล์ใน AI Studio:** File → **Import Process…** → เลือก `Rxx_….rmp` → กด ▶ Run → ดู Results
4. Extension ที่ต้องมี: **Operator Toolbox** (SMOTE ใน R04) · H2O / Concurrency / Blending มากับ AI Studio อยู่แล้ว
5. path ข้อมูลในไฟล์ตั้งไว้เป็น `/home/panguin/Projects/data mining/...` ถ้าโฟลเดอร์ repo อยู่ที่อื่น สร้างใหม่ได้ด้วย
   `RM_ROOT="/path/to/data mining" python final/rm_templates/_build/build_rm.py`

> ⚠️ process ชุดนี้สร้างด้วยโปรแกรมและตรวจแบบ static กับ source code ของ RapidMiner + process เฉลยเดิม 24 ไฟล์ที่เคยรันผ่าน
> แต่ **ยังไม่ได้กด Run ใน RapidMiner จริง** → ต้องทำข้อ 2 หรือ 3 ในเครื่องก่อนสอบ

---

## ส่วนที่ 2 · ขั้นตอนวันสอบ

| ขั้น | ทำอะไร |
|---|---|
| **1** | อ่านโจทย์ → [00_INDEX.md](00_INDEX.md) → เลือก `Rxx` |
| **2** | File → Import Process… → `Rxx_….rmp` → **File → Save Process as…** ลง Local Repository ชื่อใหม่ (เช่น `6710503739_Q1`) |
| **3** | อ่าน **โน้ตสีเขียว ⚙️ แก้ก่อน (CONFIG)** มุมซ้ายบน → แก้ตามข้อ 1, 2, 3, … |
| **4** | **Read CSV** → คลิก operator → แผง Parameters: `csv_file` → เลือกไฟล์โจทย์ (หรือกด **Import Configuration Wizard** เพื่อกำหนดชนิดคอลัมน์) |
| **5** | **Set Role** → `attribute_name` = คอลัมน์ label / id (เลือกจาก dropdown หลังรัน Read CSV 1 ครั้ง) |
| **6** | ลบแถว (§) ที่โจทย์ไม่ถาม: ลากคลุม operator ของแถวนั้น → Delete (port ของ Multiply จะว่าง ไม่เป็นไร) |
| **7** | แก้ parameter ตามโจทย์ในแถวที่ใช้ (โน้ตเหลืองของแถวบอกว่าแก้อะไร) · operator ใน CV → **ดับเบิลคลิก CV** เพื่อเข้าไปแก้ แล้วกดลูกศรย้อนกลับ (breadcrumb) |
| **8** | ▶ **Run** (F11) → แท็บ Results: แต่ละ res มีแท็บของตัวเอง |
| **9** | เขียนคำตอบ: ตัวเลขจาก Results + process (screenshot canvas) + เหตุผล · ส่งไฟล์: **File → Export Process…** (.rmp) ถ้าโจทย์ให้ส่ง |

### อ่านผลใน Results
| ผล | ดูที่ |
|---|---|
| ExampleSet (ตาราง) | **Data** (ตาราง) · **Statistics** (missing, min/max/average, ค่าที่พบบ่อย) · **Visualizations** (กราฟ) |
| PerformanceVector | **Performance** → criterion แต่ละตัว + **confusion matrix** (table view) · ค่า ± = std ระหว่าง fold |
| Model | **Description** (สมการ / กฎ) · Decision Tree → **Graph** · k-Means → **Centroid Table / Centroid Chart** · Hierarchical → **Dendrogram** |
| PCA model | **Eigenvalues** (Proportion of Variance / Cumulative) · **Eigenvectors** (loadings) |
| Weights | ตาราง attribute → weight (เรียงมาก→น้อย) |
| Log to Data | ตารางผลของทุกค่าที่ optimize → Visualizations → Line |
| Association Rules | **Table**: Premises → Conclusion, Support, Confidence, Lift (คลิกหัวคอลัมน์เพื่อเรียง) · **Graph** |

---

## ส่วนที่ 3 · หลักการต่อ process ที่ต้องรู้

| หลัก | ใน RapidMiner |
|---|---|
| ต่อผลไปหลายทาง | **Multiply** (output 1, 2, 3, …) · output port หนึ่งต่อได้เส้นเดียว |
| ไม่ให้ leak | preprocessing ที่ "เรียนจากข้อมูล" (Normalize, Replace Missing, PCA, SMOTE, Sample) อยู่ใน **Training pane** ของ Cross Validation → **Group Models** รวม preprocessing model + model ส่งไป Testing |
| Hold-out ไม่ leak | Split Data → preprocessing บน partition 1 → `preprocessing model` → **Apply Model** กับ partition 2 |
| label ต้องเป็น nominal สำหรับ classification | label 0/1 → **Numerical to Binominal** (ได้ false/true) ก่อน Set Role |
| learner ที่ต้องการตัวเลขล้วน (k-NN แบบระยะ, Linear Regression) | **Nominal to Numerical** (dummy coding) |
| positive class | Performance (Binominal) → `manually_set_positive_class` = true · `positive_class` = ค่าคลาสบวก |
| ข้อมูลใหม่ | Read CSV (new) → (Apply Model ของ preprocessing) → Apply Model ของโมเดล → `prediction(label)` + `confidence(…)` |

---

## ส่วนที่ 4 · CONFIG ที่แก้บ่อย (ทุกไฟล์)

| operator | parameter | แก้เป็น |
|---|---|---|
| Read CSV | `csv_file` · `column_separators` | ไฟล์โจทย์ · `;` ถ้าไฟล์คั่นด้วย ; |
| Read Excel | `excel_file` · `sheet_number` | ไฟล์ · sheet |
| Set Role | `attribute_name` · `target_role` | label / id |
| Numerical to Binominal | `attribute` | label ที่เป็น 0/1 (label เป็นคำอยู่แล้ว → ลบ operator) |
| Select Attributes | `attributes` (คั่น `\|`) · `invert_selection` | คอลัมน์ที่เก็บ / ตัด |
| Performance (Binominal) | `positive_class` · `main_criterion` | คลาสบวก · f_measure / accuracy / recall |
| Cross Validation | `number_of_folds` · `local_random_seed` | ตามโจทย์ |
| Split Data | `partitions` (ratio) · `local_random_seed` | 0.7 / 0.3 · seed |
| Process (คลิกพื้นที่ว่าง) | `random_seed` | seed ที่โจทย์กำหนด |

---

## ส่วนที่ 5 · คู่มือรายไฟล์ (โจทย์แบบนี้ → แก้ตรงไหน)

### R01 · Data Handling
| โจทย์ | แก้ |
|---|---|
| ไม่มีไฟล์ที่ 2 / ไม่ต้อง join | ลบ Read CSV (append)/(lookup) + Append/Join → ต่อ Read CSV (หลัก) → Multiply ตรง |
| join คนละชื่อ key | Join → `key_attributes` → Edit List: left = ชื่อฝั่งซ้าย, right = ชื่อฝั่งขวา · `join_type` |
| เลือก/ตัดคอลัมน์ | §2 Select Attributes → `attributes` + `invert_selection` |
| กรองแถว | §3 Filter Examples → Edit filters: คอลัมน์ · เงื่อนไข · ค่า (หลายเงื่อนไข → `filters_logic_and`) |
| group by | §6 Aggregate → `group_by_attributes` · `aggregation_attributes` |
| pivot | §7 Pivot → แถว `group_by_attributes` · คอลัมน์ `column_grouping_attribute` · ค่า `aggregation_attributes` · สัดส่วนคลาส → แก้สูตรใน Generate Attributes (rate) |
| สร้างคอลัมน์ | §8 Generate Attributes → `function_descriptions` |
| กราฟ | res ของข้อมูล → **Visualizations** |
| correlation | §10 (เฉพาะคอลัมน์ตัวเลข) |

### R02 · Preprocessing
| โจทย์ | แก้ |
|---|---|
| ค่าว่างเป็น `?` / `-` | Declare Missing Value → `nominal_value` |
| เติมค่าว่าง | §2 Replace Missing Values → `default` (average / minimum / zero / value) |
| ตัดแถวที่ว่าง | §2b Filter Examples → `ชื่อคอลัมน์.is_not_missing.` |
| outlier | §3 → `number_of_neighbors`, `number_of_outliers` |
| one-hot / label encoding | §4 Nominal to Numerical → `coding_type` |
| z-score / 0–1 | §5a / §5b |
| แบ่งช่วง | §6a/b/c → `attribute`, `number_of_bins`, `classes` |
| สุ่ม | §7 → `sample_ratio` |
| split ไม่ leak / เทียบก่อน-หลัง normalize | §8 / §8b |
| เลือก feature | §9 → `k` ใน Select by Weights (เปลี่ยน weighting operator ได้) |

### R03 · PCA
| โจทย์ | แก้ |
|---|---|
| กี่ PC ได้ 90% | PCA (keep variance) → `variance_threshold` = 0.9 → ดู Eigenvalues Cumulative |
| loadings | res PCA model → Eigenvectors |
| plot 2D | res PCA (2 components) → Visualizations → Scatter pc_1 × pc_2, Color = label |
| PCA ก่อนโมเดล | §5 → ดับเบิลคลิก CV kNN + PCA → PCA `number_of_components` |

### R04 · Imbalanced
| โจทย์ | แก้ |
|---|---|
| คลาสบวก | ทุก Performance ข้างใน CV → `positive_class` |
| undersample | Sample (undersample) → `sample_size_per_class` (ชื่อคลาส = จำนวน) |
| SMOTE | SMOTE Upsampling → `number_of_neighbours` |
| ทำไมห้าม SMOTE ก่อน split | §6 เทียบกับ §4c |
| เปลี่ยน learner | ดับเบิลคลิก CV → ลบ Decision Tree → ลาก learner ใหม่ → ต่อ port เดิม |

### R05 · KNN
| โจทย์ | แก้ |
|---|---|
| ระยะทางจุดใหม่ + เพื่อนบ้าน k | §2 Cross Distances → `k`, `numerical_measure` · Read CSV (new point) |
| k ที่โจทย์กำหนด | k-NN ทุกตัว → `k` |
| Manhattan | k-NN → `measure_types` = NumericalMeasures, `numerical_measure` = ManhattanDistance |
| เลือก k | §5 Optimize → Edit Parameter Settings (min/max/steps) · res Log to Data |
| ทำนาย | §6 k-NN (final) → `k` |
| KNN regression | §7 → Read CSV (regression), Set Role (regression) |

### R06 · Linear Regression
| โจทย์ | แก้ |
|---|---|
| simple LR | §3 Select Attributes (simple) → `x\|label` |
| สมการ / coefficient | res model (Linear Regression) → Description / Data |
| MAE / RMSE / R² | Performance (Regression) → R² = `squared_correlation` |
| ไม่มีคอลัมน์หมวดหมู่ | ลบ Nominal to Numerical (ต่อ Set Role → Multiply ตรง · §7 ลบ Apply Model (dummy new)) |
| Linear Regression default ของ RapidMiner | `feature_selection` = M5 prime (ตัดตัวแปรเอง) · template ตั้ง none = ใช้ทุกตัว |

### R07 · Logistic Regression
| โจทย์ | แก้ |
|---|---|
| threshold 0.3 / 0.6 | Create Threshold → `threshold` |
| ไม่มีค่า 0 ที่เป็น missing | ลบ Declare Missing Value |
| coefficient / odds ratio | res model → Coefficients (odds ratio = e^coef) |
| ⚠️ prediction ของ H2O | ไม่ใช่ threshold 0.5 → ใช้ผลของ Performance (t=0.5) เมื่อโจทย์ถาม 0.5 |

### R08 · Decision Tree & RF
| โจทย์ | แก้ |
|---|---|
| gain / gini เลือก root | §0 Read CSV (hand) + Set Role (hand) → weight สูงสุด = root |
| depth / criterion | Decision Tree → `maximal_depth`, `criterion` · pruning → `apply_pruning` |
| overfit | §3 (train acc) เทียบ §6 (CV) |
| optimize | §4 → Edit Parameter Settings |
| RF | Random Forest → `number_of_trees`, `maximal_depth` |

### R09 · Workflow
| โจทย์ | แก้ |
|---|---|
| ใช้แค่บางโมเดล | ลบ CV ของโมเดลที่ไม่ใช้ |
| ค่า parameter ของโมเดล | ดับเบิลคลิก CV → learner |
| optimize ตัวอื่น | Optimize → Edit Parameter Settings: เลือก operator + parameter + ช่วง |
| โมเดลสุดท้าย | Decision Tree (final) → ใส่ค่าที่ดีที่สุด (หรือเปลี่ยนเป็น learner อื่น) |

### R10 · Clustering
| โจทย์ | แก้ |
|---|---|
| k | Clustering → `k` |
| เลือก k | §2 → ช่วง k ใน Optimize · ดู avg_within (elbow) |
| ไม่ normalize | ลบ Normalize (และ Apply Model (normalize new)) |
| label จริงในข้อมูล | Set Role อีกตัว (label) หรือ Select Attributes ตัดออก — **ห้ามใช้คำนวณ cluster** |
| hierarchical | §7 → `mode`, Flatten → `number_of_clusters` |

### R11 · Association
| โจทย์ | แก้ |
|---|---|
| min support / confidence | FP-Growth → `min_support` · Create Association Rules → `min_confidence` |
| ตาราง 0/1 เป็น CSV | ใช้แถว C (Read CSV) แทน A |
| ตาราง Y/N หรือ yes/no | แถว B: Nominal to Binominal (ไม่ต้อง discretize ถ้าไม่มีตัวเลข) |
| ตัวเลขต้องแบ่งช่วง | แถว B: Discretize by Frequency / User Specification |
| ดู lift | rules → Table → คลิกหัวคอลัมน์ Lift |

---

## ส่วนที่ 6 · Error ที่เจอบ่อย

| ข้อความ | แก้ |
|---|---|
| `File ... does not exist` / Read CSV สีแดง | csv_file ผิด → เลือกไฟล์ใหม่ |
| `The attribute 'xxx' is missing` | ชื่อคอลัมน์ใน Set Role / Select / Filter ไม่ตรง (ตัวพิมพ์ / ช่องว่าง) |
| `... does not have a label attribute` | ยังไม่ Set Role label / Set Role อยู่หลัง operator ที่ต้องการ label / **Select Attributes ตัด label ทิ้ง**: ถ้า `include_special_attributes` = true ตัวกรอง (เช่น value_type = numeric) จะลบ label ที่เป็นคำด้วย → ตั้งเป็น **false** (special attribute ผ่านไปเสมอ) |
| `... cannot handle numerical label` / `polynominal label` | label เป็นตัวเลข → Numerical to Binominal · label 3 คลาสขึ้นไป → ใช้ **Performance (Classification)** แทน Binominal |
| `... cannot handle nominal attributes` | Nominal to Numerical ก่อน learner (ใน Training pane) |
| `... cannot handle missing values` | Replace Missing Values ก่อน learner |
| `positive class ... not found` | `positive_class` ไม่ตรงค่าจริง (เช่น true / Yes / 1) |
| `Unknown operator ... operator_toolbox:smote` | ติดตั้ง Operator Toolbox แล้ว restart |
| Davies Bouldin ติดลบ | RapidMiner แสดงเป็นค่าลบ (ยิ่งใกล้ 0 ยิ่งดี) |
| ค่า Normalize ต่างจาก Python เล็กน้อย | RapidMiner ใช้ std แบบ n−1 · sklearn ใช้ n |
