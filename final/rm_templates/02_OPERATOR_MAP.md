# 🗺️ OPERATOR MAP: ทุก operator / parameter ในทุกไฟล์ R01–R11

> สร้างอัตโนมัติจากไฟล์ .rmp (`_build/make_opmap.py`) ตรงกับไฟล์จริงเสมอ
> วิธีใช้: [01_MANUAL.md](01_MANUAL.md) · หาไฟล์จากคำในโจทย์: [00_INDEX.md](00_INDEX.md)
> แถว **in CV** = operator ที่อยู่ข้างใน Cross Validation / Optimize (ดับเบิลคลิกเพื่อเข้าไปแก้)

---

## R01_data_handling

**โน้ตบน canvas:**

- ⚙️ แก้ก่อน (CONFIG) · 1. Read CSV (หลัก) → csv_file = ไฟล์โจทย์ (หรือใช้ Import Configuration Wizard) · 2. Read CSV (append) / Read CSV (lookup) → ไฟล์ที่ 2 / ตาราง lookup · ไม่ใช้ → ลบ operator + ลบ Append/Join แล้วต่อเส้นตรง · 3. Join → key_attributes (คู่คอลัมน์ key) + join_type (inner / left / right / outer) · 4. Set Role → attribute_name = คอลัมน์ id / label · ดูสถิติ: Results → แท็บ Statistics · กราฟ: Results → Visualizations (Histogram / Boxplot / Bar / Scatter)
- §1 Import · §4 Append (ต่อแถว) · §5 Join (เพิ่มคอลัมน์ด้วย key) → res 1 = ข้อมูลหลังรวม · คลิก res 1 → Statistics (missing / min / max / mean / ค่าที่พบบ่อย) · Visualizations วาดกราฟ
- §2 Select Attributes + Set Role · Select Attributes → attributes (คั่นด้วย \|) · invert_selection = true คือ 'ตัด' · Set Role → id / label
- §3 Filter Examples (กรองแถว) · condition_class = custom_filters → Add Entry: คอลัมน์ · เงื่อนไข (equals / > / ≥ / is missing) · ค่า · filters_logic_and = AND/OR
- §6 Aggregate (group by) · group_by_attributes = คอลัมน์กลุ่ม · aggregation_attributes → Edit List: คอลัมน์ + ฟังก์ชัน (sum / average / count / maximum …)
- §7 Pivot · group_by_attributes = แถว · column_grouping_attribute = คอลัมน์ · aggregation_attributes = ค่า + ฟังก์ชัน · สัดส่วนคลาส: Generate Attributes สร้าง 0/1 ก่อนแล้ว average
- §8 Generate Attributes (สร้างคอลัมน์ใหม่) · function_descriptions → Edit List: ชื่อใหม่ = สูตร เช่น tip / total_bill * 100 · if(x > 20, "high", "low")
- §9 Sort + Sample (ดูตัวอย่าง) · Sort → attribute_name + sorting_direction · Sample → sample = absolute / relative
- §10 Correlation Matrix · ใช้ได้กับคอลัมน์ตัวเลข · ผล = ตาราง r ทุกคู่ (Results → Correlation Matrix / Pairwise Table)

| operator | class | parameter ที่ตั้งไว้ (แก้ตามโจทย์) |
|---|---|---|
| Read CSV (หลัก) | `read_csv` | `csv_file`=…/p1_bills_week1.csv |
| Read CSV (append) | `read_csv` | `csv_file`=…/p1_bills_week2.csv |
| Read CSV (lookup) | `read_csv` | `csv_file`=…/p1_day_info.csv |
| Append | `append` | `merge_type`=all |
| Join | `concurrency:join` | `join_type`=left · `use_id_attribute_as_key`=false · `key_attributes`=[day:day] · `remove_double_attributes`=true |
| Multiply | `multiply` |  |
| Select Attributes | `select_attributes` | `attribute_filter_type`=subset · `attributes`=size · `invert_selection`=true |
| Set Role (id) | `set_role` | `attribute_name`=bill_id · `target_role`=id |
| Set Role (label) | `set_role` | `attribute_name`=tip · `target_role`=label |
| Filter Examples | `filter_examples` | `condition_class`=custom_filters · `filters_logic_and`=true · `filters_list`=[filters_entry_key:time.equals.Dinner, filters_entry_key:size.ge.4] |
| Aggregate | `aggregate` | `use_default_aggregation`=false · `group_by_attributes`=day · `aggregation_attributes`=[total_bill:sum, total_bill:average, tip:average, bill_id:count] |
| Generate Attributes (rate) | `generate_attributes` | `function_descriptions`=[is_smoker:if(smoker=="Yes", 1, 0)] |
| Pivot | `blending:pivot` | `group_by_attributes`=day · `column_grouping_attribute`=time · `aggregation_attributes`=[tip:average, is_smoker:average] |
| Generate Attributes | `generate_attributes` | `function_descriptions`=[tip_pct:tip / total_bill * 100, big_bill:if(total_bill > 20, "Yes", "No")] |
| Sort | `sort` | `attribute_name`=total_bill · `sorting_direction`=decreasing |
| Sample (10 rows) | `sample` | `sample`=absolute · `sample_size`=10 |
| Correlation Matrix | `correlation_matrix` |  |

---

## R02_preprocessing

**โน้ตบน canvas:**

- ⚙️ แก้ก่อน (CONFIG) · 1. Read CSV → csv_file · Declare Missing Value → ค่าที่แปลว่าว่าง เช่น ? (ไม่มี → ลบ operator) · 2. Set Role → attribute_name = label · 3. แต่ละแถว: แก้ attribute / attributes ให้ตรงคอลัมน์ของโจทย์ (ดูโน้ตเหลืองของแถวนั้น) · §1–§7 = ทำกับทั้งตาราง (สาธิต) · §8 = วิธีถูกต้องตอนสร้างโมเดล (fit บน train / ใน CV เท่านั้น)
- §0 ข้อมูลดิบ → res 1 · res 1 → Statistics: ดูจำนวน Missing ของแต่ละคอลัมน์ · ชนิด (nominal/numeric) · range
- §2 Missing: Replace Missing Values · default = average / minimum / maximum / zero / value (replenishment_value) · ตัดแถวแทน: Filter Examples (attr.is_not_missing.)
- §2b Missing: ตัดแถวที่ว่าง · Filter Examples → filters_list: body_mass_g.is_not_missing. (แก้ชื่อคอลัมน์)
- §3 Outlier: Detect Outlier (Distances) → ตัดแถว outlier · number_of_neighbors (k) · number_of_outliers (n แถวที่ไกลสุด) · ผลมีคอลัมน์ outlier = true/false → Filter Examples outlier.equals.false
- §4 Encoding: Nominal to Numerical (dummy = one-hot) · coding_type = dummy coding (one-hot) / unique integers (label encoding) / effect coding · attribute_filter_type = all หรือ subset
- §5a Standardization: Normalize (Z-transformation) · method = Z-transformation → mean 0, std 1 (RapidMiner ใช้ n−1)
- §5b Normalization: Normalize (range transformation 0–1) · method = range transformation · min = 0 · max = 1
- §6a Discretize by Binning (equal width) · attribute = คอลัมน์ · number_of_bins · range_name_type = short (ชื่อ range1, range2 …)
- §6b Discretize by Frequency (equal frequency) · จำนวนต่อช่วงเท่ากัน · ทนข้อมูลเบ้
- §6c Discretize by User Specification (ขอบกำหนดเอง) · classes → Edit List: ชื่อช่วง + upper limit (ค่าบนสุดของช่วง · ช่วงสุดท้ายใส่ Infinity)
- §7a Sample (สุ่ม 30%) · sample = relative · sample_ratio = 0.3 · (absolute → sample_size)
- §7b Sample (Stratified) — รักษาสัดส่วนคลาส · ต้องมี label · sample = relative · sample_ratio
- §8 ⭐ Split Data ไม่ให้ leak: Replace Missing + Normalize fit บน train → Apply Model (preprocessing model) กับ test · res = train ที่ preprocess แล้ว + test ที่ใช้ค่า mean/std จาก train · Split Data → partitions (0.7 / 0.3) · sampling_type = stratified
- §8b ⭐ เทียบก่อน/หลัง preprocessing: k-NN ไม่ normalize vs normalize (ทุกอย่างอยู่ใน Training pane ของ CV) · ดับเบิลคลิก CV เพื่อดูข้างใน · เปรียบเทียบ accuracy ใน res · เปลี่ยน learner ได้ (ลาก operator ใหม่แทน k-NN)
- §9 Feature selection: Weight by Information Gain → Select by Weights (top k) · weight_relation = top k · k = จำนวน feature · เปลี่ยนเป็น Weight by Correlation / Gini Index ได้ · ⚠️ ใช้ใน CV ถ้าจะวัดผลโมเดล

| operator | class | parameter ที่ตั้งไว้ (แก้ตามโจทย์) |
|---|---|---|
| Read CSV | `read_csv` | `csv_file`=…/p2_penguins.csv |
| Declare Missing Value | `declare_missing_value` | `attribute_filter_type`=all · `mode`=nominal · `nominal_value`=? |
| Set Role | `set_role` | `attribute_name`=species · `target_role`=label |
| Multiply | `multiply` |  |
| Replace Missing Values | `replace_missing_values` | `default`=average |
| Filter Examples (not missing) | `filter_examples` | `condition_class`=custom_filters · `filters_list`=[filters_entry_key:body_mass_g.is_not_missing.] |
| Select Attributes (numeric) | `select_attributes` | `attribute_filter_type`=value_type · `value_type`=numeric · `include_special_attributes`=false |
| Replace Missing (outlier) | `replace_missing_values` | `default`=average |
| Detect Outlier (Distances) | `detect_outlier_distances` | `number_of_neighbors`=10 · `number_of_outliers`=10 · `distance_function`=euclidian distance |
| Filter Examples (no outlier) | `filter_examples` | `condition_class`=custom_filters · `filters_list`=[filters_entry_key:outlier.equals.false] |
| Nominal to Numerical | `nominal_to_numerical` | `coding_type`=dummy coding |
| Normalize (Z) | `normalize` | `method`=Z-transformation |
| Normalize (0-1) | `normalize` | `method`=range transformation · `min`=0.0 · `max`=1.0 |
| Discretize by Binning | `discretize_by_bins` | `attribute_filter_type`=single · `attribute`=body_mass_g · `number_of_bins`=3 · `range_name_type`=short |
| Discretize by Frequency | `discretize_by_frequency` | `attribute_filter_type`=single · `attribute`=body_mass_g · `number_of_bins`=3 · `range_name_type`=short |
| Discretize by User Specification | `discretize_by_user_specification` | `attribute_filter_type`=single · `attribute`=body_mass_g · `classes`=[Low:3500, Mid:4500, High:Infinity] |
| Sample (relative) | `sample` | `sample`=relative · `sample_ratio`=0.3 |
| Sample (Stratified) | `sample_stratified` | `sample`=relative · `sample_ratio`=0.3 |
| Split Data | `split_data` | `partitions`=[0.7, 0.3] · `sampling_type`=stratified sampling |
| Replace Missing (train) | `replace_missing_values` | `default`=average · `return_preprocessing_model`=true |
| Normalize (train) | `normalize` | `method`=Z-transformation |
| Apply Model (missing → test) | `apply_model` |  |
| Apply Model (normalize → test) | `apply_model` |  |
| Multiply (compare) | `multiply` |  |
| CV kNN raw | `concurrency:cross_validation` | `number_of_folds`=5 · `sampling_type`=stratified sampling |
| ↳ Replace Missing Values (kNN raw) | `replace_missing_values` | `default`=average · `return_preprocessing_model`=true |
| ↳ Nominal to Numerical (kNN raw) | `nominal_to_numerical` | `coding_type`=dummy coding · `return_preprocessing_model`=true |
| ↳ k-NN (kNN raw) | `k_nn` | `k`=5 |
| ↳ Group Models (kNN raw) | `group_models` |  |
| ↳ Apply Model (kNN raw) | `apply_model` |  |
| ↳ Performance (kNN raw) | `performance_classification` | `main_criterion`=accuracy |
| CV kNN normalized | `concurrency:cross_validation` | `number_of_folds`=5 · `sampling_type`=stratified sampling |
| ↳ Replace Missing Values (kNN normalized) | `replace_missing_values` | `default`=average · `return_preprocessing_model`=true |
| ↳ Nominal to Numerical (kNN normalized) | `nominal_to_numerical` | `coding_type`=dummy coding · `return_preprocessing_model`=true |
| ↳ Normalize (kNN normalized) | `normalize` | `method`=Z-transformation |
| ↳ k-NN (kNN normalized) | `k_nn` | `k`=5 |
| ↳ Group Models (kNN normalized) | `group_models` |  |
| ↳ Apply Model (kNN normalized) | `apply_model` |  |
| ↳ Performance (kNN normalized) | `performance_classification` | `main_criterion`=accuracy |
| Weight by Information Gain | `weight_by_information_gain` | `normalize_weights`=false · `sort_weights`=true · `sort_direction`=descending |
| Select by Weights | `select_by_weights` | `weight_relation`=top k · `k`=3 |

---

## R03_pca

**โน้ตบน canvas:**

- ⚙️ แก้ก่อน (CONFIG) · 1. Read CSV → csv_file · Set Role → label (ไว้ระบายสีกราฟ · ไม่มี label → ลบ Set Role) · 2. Select Attributes → ตัด id / คอลัมน์ที่ไม่ใช่ตัวเลข (PCA ใช้ตัวเลขเท่านั้น) · 3. PCA → dimensionality_reduction = keep variance (variance_threshold 0.8/0.9/0.95) หรือ fixed number (number_of_components) · ผล PCA model (res) → แท็บ Eigenvalues (variance / cumulative) · Eigenvectors (loadings) · กราฟ 2D: res scores → Visualizations → Scatter pc_1 × pc_2 สีตาม label
- §2–§3 Normalize → PCA (keep variance 0.95) → res: scores + model (eigenvalues / loadings) · จำนวน PC ที่ต้องใช้ = ดู Cumulative Variance ใน Eigenvalues · loadings = Eigenvectors
- §4 PCA 2 components → scatter 2D · number_of_components = 2 · res → Visualizations → Scatter: x = pc_1, y = pc_2, color = label
- §5 ⭐ เทียบโมเดลก่อน/หลัง PCA (Normalize + PCA อยู่ใน Training pane ของ CV = ไม่ leak) · เปลี่ยนจำนวน PC: ดับเบิลคลิก CV kNN + PCA → PCA → number_of_components

| operator | class | parameter ที่ตั้งไว้ (แก้ตามโจทย์) |
|---|---|---|
| Read CSV | `read_csv` | `csv_file`=…/p4_wine.csv |
| Set Role | `set_role` | `attribute_name`=cultivar · `target_role`=label |
| Select Attributes | `select_attributes` | `attribute_filter_type`=value_type · `value_type`=numeric · `include_special_attributes`=false |
| Multiply | `multiply` |  |
| Normalize (pca) | `normalize` | `method`=Z-transformation |
| PCA (keep variance) | `principal_component_analysis` | `dimensionality_reduction`=keep variance · `variance_threshold`=0.95 |
| Normalize (2D) | `normalize` | `method`=Z-transformation |
| PCA (2 components) | `principal_component_analysis` | `dimensionality_reduction`=fixed number · `number_of_components`=2 |
| Multiply (compare) | `multiply` |  |
| CV kNN | `concurrency:cross_validation` | `number_of_folds`=5 · `sampling_type`=stratified sampling |
| ↳ Normalize (kNN) | `normalize` | `method`=Z-transformation |
| ↳ k-NN (kNN) | `k_nn` | `k`=5 |
| ↳ Group Models (kNN) | `group_models` |  |
| ↳ Apply Model (kNN) | `apply_model` |  |
| ↳ Performance (kNN) | `performance_classification` | `main_criterion`=accuracy |
| CV kNN + PCA | `concurrency:cross_validation` | `number_of_folds`=5 · `sampling_type`=stratified sampling |
| ↳ Normalize (kNN + PCA) | `normalize` | `method`=Z-transformation |
| ↳ PCA (kNN + PCA) | `principal_component_analysis` | `dimensionality_reduction`=fixed number · `number_of_components`=2 |
| ↳ k-NN (kNN + PCA) | `k_nn` | `k`=5 |
| ↳ Group Models (kNN + PCA) | `group_models` |  |
| ↳ Apply Model (kNN + PCA) | `apply_model` |  |
| ↳ Performance (kNN + PCA) | `performance_classification` | `main_criterion`=accuracy |

---

## R04_imbalanced_smote

**โน้ตบน canvas:**

- ⚙️ แก้ก่อน (CONFIG) · 1. Read CSV → csv_file · Set Role → label · 2. ทุก Performance (ในแต่ละ CV) → positive_class = คลาสส่วนน้อย/ที่สนใจ (ตอนนี้ = malignant) · 3. Sample (undersample) → sample_size_per_class: ใส่ชื่อคลาส + จำนวน (= จำนวนของคลาสส่วนน้อยใน training fold) · 4. SMOTE ต้องติดตั้ง Operator Toolbox (Extensions → Marketplace) · ไม่มี → ลบแถว SMOTE ทั้ง 2 แถว · ดู res: recall / precision / F1 ของคลาสส่วนน้อย ไม่ใช่ accuracy อย่างเดียว · resample อยู่ใน Training pane = ไม่แตะ test fold
- §1 ดูความไม่สมดุล → res 1 (Statistics ของ label) ·
- §2 Baseline (Default Model = mode) → accuracy สูงแต่ recall = 0 · ดับเบิลคลิก CV → Training pane เห็น resampling + learner · Testing pane = Apply Model + Performance
- §4a ไม่ resample (Decision Tree) · ดับเบิลคลิก CV → Training pane เห็น resampling + learner · Testing pane = Apply Model + Performance
- §4b Undersampling: Sample (balance_data) ใน Training pane · ดับเบิลคลิก CV → Training pane เห็น resampling + learner · Testing pane = Apply Model + Performance
- §4c SMOTE ใน Training pane (Operator Toolbox) · ดับเบิลคลิก CV → Training pane เห็น resampling + learner · Testing pane = Apply Model + Performance
- §6 ❌ วิธีผิด: SMOTE ทั้งตารางก่อน CV (leak) → ผลดีเกินจริง (ไว้ตอบคำถาม 'ทำไมห้าม') · เทียบ res กับ §4c · synthetic ที่สร้างจากจุดใน test fold รั่วเข้า training

| operator | class | parameter ที่ตั้งไว้ (แก้ตามโจทย์) |
|---|---|---|
| Read CSV | `read_csv` | `csv_file`=…/p3_breast_cancer_imbalanced.csv |
| Set Role | `set_role` | `attribute_name`=diagnosis · `target_role`=label |
| Multiply | `multiply` |  |
| CV Baseline | `concurrency:cross_validation` | `number_of_folds`=5 · `sampling_type`=stratified sampling |
| ↳ Default Model (Baseline) | `default_model` | `method`=mode |
| ↳ Apply Model (Baseline) | `apply_model` |  |
| ↳ Performance (Baseline) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=malignant |
| CV Tree | `concurrency:cross_validation` | `number_of_folds`=5 · `sampling_type`=stratified sampling |
| ↳ Decision Tree (Tree) | `concurrency:parallel_decision_tree` | `criterion`=gini_index · `maximal_depth`=4 · `apply_pruning`=false · `apply_prepruning`=false |
| ↳ Apply Model (Tree) | `apply_model` |  |
| ↳ Performance (Tree) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=malignant |
| CV Undersample | `concurrency:cross_validation` | `number_of_folds`=5 · `sampling_type`=stratified sampling |
| ↳ Sample (undersample) (Undersample) | `sample` | `sample`=absolute · `balance_data`=true · `sample_size_per_class`=[benign:32, malignant:32] |
| ↳ Decision Tree (Undersample) | `concurrency:parallel_decision_tree` | `criterion`=gini_index · `maximal_depth`=4 · `apply_pruning`=false · `apply_prepruning`=false |
| ↳ Apply Model (Undersample) | `apply_model` |  |
| ↳ Performance (Undersample) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=malignant |
| CV SMOTE | `concurrency:cross_validation` | `number_of_folds`=5 · `sampling_type`=stratified sampling |
| ↳ SMOTE Upsampling (SMOTE) | `operator_toolbox:smote` | `number_of_neighbours`=5 · `normalize`=true · `equalize_classes`=true · `auto_detect_minority_class`=true |
| ↳ Decision Tree (SMOTE) | `concurrency:parallel_decision_tree` | `criterion`=gini_index · `maximal_depth`=4 · `apply_pruning`=false · `apply_prepruning`=false |
| ↳ Apply Model (SMOTE) | `apply_model` |  |
| ↳ Performance (SMOTE) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=malignant |
| SMOTE (WRONG, before CV) | `operator_toolbox:smote` | `number_of_neighbours`=5 · `normalize`=true · `equalize_classes`=true · `auto_detect_minority_class`=true |
| CV WRONG | `concurrency:cross_validation` | `number_of_folds`=5 · `sampling_type`=stratified sampling |
| ↳ Decision Tree (WRONG) | `concurrency:parallel_decision_tree` | `criterion`=gini_index · `maximal_depth`=4 · `apply_pruning`=false · `apply_prepruning`=false |
| ↳ Apply Model (WRONG) | `apply_model` |  |
| ↳ Performance (WRONG) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=malignant |

---

## R05_knn

**โน้ตบน canvas:**

- ⚙️ แก้ก่อน (CONFIG) · 1. Read CSV → csv_file · Set Role → label · (label เป็น 0/1 → เพิ่ม Numerical to Binominal ก่อน Set Role) · 2. Read CSV (new point) → ไฟล์ข้อมูลใหม่ (คอลัมน์เดียวกัน ไม่ต้องมี label) — สร้างใน Excel/Notepad 1 แถว · 3. k-NN → k · measure_types = NumericalMeasures · numerical_measure = EuclideanDistance / ManhattanDistance · 4. Performance → positive_class = คลาสที่สนใจ (ตอนนี้ = Owner)
- §2 ระยะจากจุดใหม่ถึงทุกจุด (Cross Distances) → k จุดใกล้สุด · only_top_k = true · k = 3 · ไม่ normalize ตามตำรา (ถ้าโจทย์ให้ normalize ต้อง Normalize ทั้งสองฝั่งด้วยค่าจากข้อมูล train)
- §3 Hold-out: Split Data 70/30 → Normalize (fit train) → k-NN → Apply กับ test → Performance · partitions = 0.7 / 0.3 · ไม่ normalize → ลบ Normalize + Apply Model (normalize) แล้วต่อเส้นตรง
- §4 ⭐ CV: baseline vs k-NN ไม่ normalize vs k-NN + normalize (เทียบก่อน/หลัง preprocessing) · number_of_folds ใน CV แต่ละตัว · k ใน k-NN ข้างใน CV
- §5 ⭐ Optimize Parameters (Grid): k = 1…15 + Log → ตาราง k vs F1 · parameter set = k ที่ดีที่สุด · แก้ช่วง: Optimize Parameters → Edit Parameter Settings (k-NN (opt).k: min, max, steps) · กราฟ: Log to Data → Visualizations → Line
- §6 โมเดลสุดท้าย (ทั้งชุด) → ทำนายจุดใหม่ (prediction + confidence = สัดส่วน vote) · k ของ k-NN (final) = ค่าที่ดีที่สุดจาก §5 หรือค่าที่โจทย์กำหนด
- §7 KNN Regression (label ตัวเลข) → Performance (Regression): RMSE / MAE / R² · Read CSV (regression) → ไฟล์ · Set Role (regression) → label ตัวเลข · k ใน k-NN

| operator | class | parameter ที่ตั้งไว้ (แก้ตามโจทย์) |
|---|---|---|
| Read CSV | `read_csv` | `csv_file`=…/riding_mowers.csv |
| Set Role | `set_role` | `attribute_name`=Ownership · `target_role`=label |
| Multiply | `multiply` |  |
| Read CSV (new point) | `read_csv` | `csv_file`=…/new_mower.csv |
| Multiply (new) | `multiply` |  |
| Cross Distances | `cross_distances` | `measure_types`=NumericalMeasures · `numerical_measure`=EuclideanDistance · `only_top_k`=true · `k`=3 · `search_for`=nearest |
| Split Data | `split_data` | `partitions`=[0.7, 0.3] · `sampling_type`=stratified sampling |
| Normalize (hold-out) | `normalize` | `method`=Z-transformation |
| k-NN (hold-out) | `k_nn` | `k`=3 |
| Apply Model (normalize test) | `apply_model` |  |
| Apply Model (kNN test) | `apply_model` |  |
| Performance (hold-out) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=Owner |
| Multiply (compare) | `multiply` |  |
| CV Baseline | `concurrency:cross_validation` | `number_of_folds`=5 · `sampling_type`=stratified sampling |
| ↳ Default Model (Baseline) | `default_model` | `method`=mode |
| ↳ Apply Model (Baseline) | `apply_model` |  |
| ↳ Performance (Baseline) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=Owner |
| CV kNN raw | `concurrency:cross_validation` | `number_of_folds`=5 · `sampling_type`=stratified sampling |
| ↳ k-NN (kNN raw) | `k_nn` | `k`=3 |
| ↳ Apply Model (kNN raw) | `apply_model` |  |
| ↳ Performance (kNN raw) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=Owner |
| CV kNN normalized | `concurrency:cross_validation` | `number_of_folds`=5 · `sampling_type`=stratified sampling |
| ↳ Normalize (kNN normalized) | `normalize` | `method`=Z-transformation |
| ↳ k-NN (kNN normalized) | `k_nn` | `k`=3 |
| ↳ Group Models (kNN normalized) | `group_models` |  |
| ↳ Apply Model (kNN normalized) | `apply_model` |  |
| ↳ Performance (kNN normalized) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=Owner |
| Optimize Parameters (k) | `concurrency:optimize_parameters_grid` | `parameters`=[k-NN (opt).k:[1.0;15.0;14;linear]] |
| ↳ CV opt | `concurrency:cross_validation` | `number_of_folds`=5 · `sampling_type`=stratified sampling |
| ↳ ↳ Normalize (opt) | `normalize` | `method`=Z-transformation |
| ↳ ↳ k-NN (opt) | `k_nn` | `k`=5 |
| ↳ ↳ Group Models (opt) | `group_models` |  |
| ↳ ↳ Apply Model (opt) | `apply_model` |  |
| ↳ ↳ Performance (opt) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=Owner |
| ↳ Log (k) | `log` | `log`=[k:operator.k-NN (opt).parameter.k, f_measure:operator.CV opt.value.performance main criterion] |
| Log to Data (k) | `log_to_data` | `log_name`=Log (k) |
| Normalize (final) | `normalize` | `method`=Z-transformation |
| k-NN (final) | `k_nn` | `k`=3 |
| Apply Model (normalize new) | `apply_model` |  |
| Apply Model (kNN new) | `apply_model` |  |
| Read CSV (regression) | `read_csv` | `csv_file`=…/housing.csv |
| Set Role (regression) | `set_role` | `attribute_name`=medv · `target_role`=label |
| CV kNN regression | `concurrency:cross_validation` | `number_of_folds`=10 · `sampling_type`=shuffled sampling |
| ↳ Normalize (kNN regression) | `normalize` | `method`=Z-transformation |
| ↳ k-NN (kNN regression) | `k_nn` | `k`=5 |
| ↳ Group Models (kNN regression) | `group_models` |  |
| ↳ Apply Model (kNN regression) | `apply_model` |  |
| ↳ Performance (kNN regression) | `performance_regression` | `main_criterion`=root_mean_squared_error |

---

## R06_linear_regression

**โน้ตบน canvas:**

- ⚙️ แก้ก่อน (CONFIG) · 1. Read CSV → csv_file · Set Role → label (ตัวเลขที่จะทำนาย) · 2. Nominal to Numerical → comparison_groups: คอลัมน์หมวดหมู่ + ค่าอ้างอิง (reference) · ไม่มีคอลัมน์หมวดหมู่ → ลบ · 3. Select Attributes (simple) → x ตัวเดียว + label · 4. Read CSV (new) → ข้อมูลใหม่ (คอลัมน์เดียวกัน) · สมการ: res model → แท็บ Description/Data: Coefficient · p-value · y = intercept + Σ coef × x
- §3 Simple linear regression (x ตัวเดียว) บนข้อมูลทั้งหมด → สมการ y = b0 + b1·x · Select Attributes → attributes = age\|charges (x\|label)
- §4–§5 ⭐ Multiple LR + baseline (mean) บน hold-out 80/20 → MAE / RMSE / R² (squared_correlation) · Split Data → partitions · Linear Regression → feature_selection = none (ใช้ทุกตัว) / M5 prime · model = สมการเต็ม
- §6 เทียบใน CV: LR vs k-NN regression vs Decision Tree regression · ดู RMSE ต่ำสุด / R² สูงสุด
- §7 ทำนายข้อมูลใหม่: dummy coding เดิม (preprocessing model) → Linear Regression (ทั้งชุด) ·

| operator | class | parameter ที่ตั้งไว้ (แก้ตามโจทย์) |
|---|---|---|
| Read CSV | `read_csv` | `csv_file`=…/p7_insurance.csv |
| Set Role | `set_role` | `attribute_name`=charges · `target_role`=label |
| Nominal to Numerical | `nominal_to_numerical` | `coding_type`=dummy coding · `use_comparison_groups`=true · `return_preprocessing_model`=true · `comparison_groups`=[sex:female, smoker:no, region:northeast] |
| Multiply | `multiply` |  |
| Select Attributes (simple) | `select_attributes` | `attribute_filter_type`=subset · `attributes`=age\|charges · `include_special_attributes`=false |
| Linear Regression (simple) | `linear_regression` | `feature_selection`=none · `eliminate_colinear_features`=true · `use_bias`=true |
| Split Data | `split_data` | `partitions`=[0.8, 0.2] · `sampling_type`=shuffled sampling |
| Multiply (train) | `multiply` |  |
| Multiply (test) | `multiply` |  |
| Default Model (mean) | `default_model` | `method`=average |
| Apply Model (Baseline mean) | `apply_model` |  |
| Performance (Baseline mean) | `performance_regression` | `main_criterion`=root_mean_squared_error |
| Linear Regression | `linear_regression` | `feature_selection`=none · `eliminate_colinear_features`=true · `use_bias`=true |
| Apply Model (Linear Regression) | `apply_model` |  |
| Performance (Linear Regression) | `performance_regression` | `main_criterion`=root_mean_squared_error |
| Multiply (compare) | `multiply` |  |
| CV LR | `concurrency:cross_validation` | `number_of_folds`=5 · `sampling_type`=shuffled sampling |
| ↳ Linear Regression (LR) | `linear_regression` | `feature_selection`=none |
| ↳ Apply Model (LR) | `apply_model` |  |
| ↳ Performance (CV LR) | `performance_regression` | `main_criterion`=root_mean_squared_error |
| CV kNN reg | `concurrency:cross_validation` | `number_of_folds`=5 · `sampling_type`=shuffled sampling |
| ↳ Normalize (kNN reg) | `normalize` | `method`=Z-transformation |
| ↳ k-NN (kNN reg) | `k_nn` | `k`=10 |
| ↳ Group Models (kNN reg) | `group_models` |  |
| ↳ Apply Model (kNN reg) | `apply_model` |  |
| ↳ Performance (CV kNN reg) | `performance_regression` | `main_criterion`=root_mean_squared_error |
| CV Tree reg | `concurrency:cross_validation` | `number_of_folds`=5 · `sampling_type`=shuffled sampling |
| ↳ Decision Tree (Tree reg) | `concurrency:parallel_decision_tree` | `criterion`=least_square · `maximal_depth`=5 · `apply_pruning`=false · `apply_prepruning`=false |
| ↳ Apply Model (Tree reg) | `apply_model` |  |
| ↳ Performance (CV Tree reg) | `performance_regression` | `main_criterion`=root_mean_squared_error |
| Linear Regression (final) | `linear_regression` | `feature_selection`=none |
| Read CSV (new) | `read_csv` | `csv_file`=…/new_insurance.csv |
| Apply Model (dummy new) | `apply_model` |  |
| Apply Model (LR new) | `apply_model` |  |

---

## R07_logistic_regression

**โน้ตบน canvas:**

- ⚙️ แก้ก่อน (CONFIG) · 1. Read CSV → csv_file · Numerical to Binominal → label 0/1 (label เป็นคำอยู่แล้ว → ลบ) · Set Role → label · 2. Declare Missing Value → คอลัมน์ที่ค่า 0 เป็นไปไม่ได้ (ข้อมูลอื่น → ลบ operator) · 3. Create Threshold → threshold · first_class = คลาสลบ · second_class = คลาสบวก (ตอนนี้ false / true) · 4. Performance → positive_class = คลาสบวก (true) · ⚠️ H2O Logistic Regression ตัดสินที่ threshold ที่ทำให้ F1 สูงสุด (ไม่ใช่ 0.5) → อยากได้ 0.5 ต้องใช้ Create/Apply Threshold
- §1–§3 Split 75/25 → Replace Missing (fit train) → Logistic Regression → Apply กับ test · res model = coefficients (+ p-value) · odds ratio = e^coef
- §5 ⭐ Threshold: default ของ H2O vs 0.5 vs 0.3 → confusion matrix + precision / recall / F1 · เพิ่ม threshold อื่น: copy Create Threshold + Apply Threshold + Performance แล้วต่อจาก Multiply (scored test) port ถัดไป
- §2 / §6 Baseline vs Logistic ใน 10-fold CV (Replace Missing อยู่ใน Training pane) ·
- §7 ทำนายข้อมูลใหม่ → confidence(true) = ความน่าจะเป็น · prediction ตาม threshold ของ H2O · Read CSV (new) → ไฟล์ข้อมูลใหม่ (ไม่ต้องมี label)

| operator | class | parameter ที่ตั้งไว้ (แก้ตามโจทย์) |
|---|---|---|
| Read CSV | `read_csv` | `csv_file`=…/p5_pima_diabetes.csv |
| Numerical to Binominal | `numerical_to_binominal` | `attribute_filter_type`=single · `attribute`=diabetes · `min`=0.0 · `max`=0.0 |
| Set Role | `set_role` | `attribute_name`=diabetes · `target_role`=label |
| Declare Missing Value | `declare_missing_value` | `attribute_filter_type`=subset · `attributes`=glucose\|blood_pressure\|skin_thickness\|insulin\|bmi · `mode`=numeric · `numeric_value`=0.0 |
| Multiply | `multiply` |  |
| Split Data | `split_data` | `partitions`=[0.75, 0.25] · `sampling_type`=stratified sampling |
| Replace Missing Values | `replace_missing_values` | `default`=average · `return_preprocessing_model`=true |
| Logistic Regression | `h2o:logistic_regression` |  |
| Apply Model (impute test) | `apply_model` |  |
| Apply Model (logistic) | `apply_model` |  |
| Multiply (model) | `multiply` |  |
| Multiply (scored test) | `multiply` |  |
| Performance (H2O default) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=true |
| Create Threshold 0.5 | `create_threshold` | `threshold`=0.5 · `first_class`=false · `second_class`=true |
| Apply Threshold 0.5 | `apply_threshold` |  |
| Performance (t=0.5) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=true |
| Create Threshold 0.3 | `create_threshold` | `threshold`=0.3 · `first_class`=false · `second_class`=true |
| Apply Threshold 0.3 | `apply_threshold` |  |
| Performance (t=0.3) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=true |
| Multiply (CV) | `multiply` |  |
| CV Baseline | `concurrency:cross_validation` | `number_of_folds`=10 · `sampling_type`=stratified sampling |
| ↳ Default Model (Baseline) | `default_model` | `method`=mode |
| ↳ Apply Model (Baseline) | `apply_model` |  |
| ↳ Performance (CV Baseline) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=true |
| CV LogReg | `concurrency:cross_validation` | `number_of_folds`=10 · `sampling_type`=stratified sampling |
| ↳ Replace Missing Values (LogReg) | `replace_missing_values` | `default`=average · `return_preprocessing_model`=true |
| ↳ Logistic Regression (LogReg) | `h2o:logistic_regression` |  |
| ↳ Group Models (LogReg) | `group_models` |  |
| ↳ Apply Model (LogReg) | `apply_model` |  |
| ↳ Performance (CV LogReg) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=true |
| Read CSV (new) | `read_csv` | `csv_file`=…/new_pima.csv |
| Apply Model (impute new) | `apply_model` |  |
| Apply Model (logistic new) | `apply_model` |  |

---

## R08_decision_tree_rf

**โน้ตบน canvas:**

- ⚙️ แก้ก่อน (CONFIG) · 1. Read CSV → csv_file · Numerical to Binominal → label 0/1 (label เป็นคำอยู่แล้ว → ลบ) · Set Role → label · 2. Decision Tree → criterion (gini_index / information_gain / gain_ratio) · maximal_depth · apply_pruning · 3. Read CSV (hand) + Set Role (hand) → ข้อมูลเล็กที่โจทย์ให้คำนวณ gain ด้วยมือ · 4. Performance → positive_class = true · RapidMiner default = gain_ratio + pruning · ดูต้นไม้: res model → Graph / Description (กฎ IF-THEN)
- §0 คำนวณ impurity: Weight by Information Gain / Gain Ratio / Gini Index → ค่าสูงสุด = root · normalize_weights = false (ค่าจริง) · ใช้กับ attribute หมวดหมู่ · ตรวจคำตอบที่คำนวณมือ
- §2 Decision Tree (depth 3) บนข้อมูลทั้งหมด → ต้นไม้ + กฎ + feature importance (Weight by Tree Importance) · res model → Graph (ต้นไม้) / Description (กฎ IF-THEN)
- §3 Overfitting: train accuracy ของต้นไม้เต็ม (Apply กับข้อมูลเดิม) — เทียบกับ CV ใน §6 ·
- §6 ⭐ CV: baseline vs Tree เต็ม vs Tree depth 3 vs Random Forest ·
- §4 ⭐ Optimize maximal_depth 1…12 (+ Log) → ตาราง depth vs accuracy (หาจุด overfit) · เพิ่ม parameter: Edit Parameter Settings → criterion / minimal_leaf_size
- §5 Random Forest บนข้อมูลทั้งหมด → ทำนายข้อมูลใหม่ · Read CSV (new) → ไฟล์ข้อมูลใหม่ · number_of_trees

| operator | class | parameter ที่ตั้งไว้ (แก้ตามโจทย์) |
|---|---|---|
| Read CSV (hand) | `read_csv` | `csv_file`=…/weather.csv |
| Set Role (hand) | `set_role` | `attribute_name`=Class · `target_role`=label |
| Multiply (hand) | `multiply` |  |
| Weight By Information Gain | `weight_by_information_gain` | `normalize_weights`=false · `sort_weights`=true · `sort_direction`=descending |
| Weight By Information Gain Ratio | `weight_by_information_gain_ratio` | `normalize_weights`=false · `sort_weights`=true · `sort_direction`=descending |
| Weight By Gini Index | `weight_by_gini_index` | `normalize_weights`=false · `sort_weights`=true · `sort_direction`=descending |
| Read CSV | `read_csv` | `csv_file`=…/p6_heart.csv |
| Numerical to Binominal | `numerical_to_binominal` | `attribute_filter_type`=single · `attribute`=target · `min`=0.0 · `max`=0.0 |
| Set Role | `set_role` | `attribute_name`=target · `target_role`=label |
| Multiply | `multiply` |  |
| Decision Tree (show) | `concurrency:parallel_decision_tree` | `criterion`=gini_index · `maximal_depth`=3 · `apply_pruning`=false · `apply_prepruning`=false |
| Decision Tree (full) | `concurrency:parallel_decision_tree` | `criterion`=gini_index · `maximal_depth`=30 · `apply_pruning`=false · `apply_prepruning`=false |
| Apply Model (train acc) | `apply_model` |  |
| Performance (train acc) | `performance_binominal_classification` | `main_criterion`=accuracy · `manually_set_positive_class`=true · `positive_class`=true |
| Multiply (compare) | `multiply` |  |
| CV Baseline | `concurrency:cross_validation` | `number_of_folds`=10 · `sampling_type`=stratified sampling |
| ↳ Default Model (Baseline) | `default_model` | `method`=mode |
| ↳ Apply Model (Baseline) | `apply_model` |  |
| ↳ Performance (Baseline) | `performance_binominal_classification` | `main_criterion`=accuracy · `manually_set_positive_class`=true · `positive_class`=true |
| CV Tree full | `concurrency:cross_validation` | `number_of_folds`=10 · `sampling_type`=stratified sampling |
| ↳ Decision Tree (Tree full) | `concurrency:parallel_decision_tree` | `criterion`=gini_index · `maximal_depth`=30 · `apply_pruning`=false · `apply_prepruning`=false |
| ↳ Apply Model (Tree full) | `apply_model` |  |
| ↳ Performance (Tree full) | `performance_binominal_classification` | `main_criterion`=accuracy · `manually_set_positive_class`=true · `positive_class`=true |
| CV Tree d3 | `concurrency:cross_validation` | `number_of_folds`=10 · `sampling_type`=stratified sampling |
| ↳ Decision Tree (Tree d3) | `concurrency:parallel_decision_tree` | `criterion`=gini_index · `maximal_depth`=3 · `apply_pruning`=false · `apply_prepruning`=false |
| ↳ Apply Model (Tree d3) | `apply_model` |  |
| ↳ Performance (Tree d3) | `performance_binominal_classification` | `main_criterion`=accuracy · `manually_set_positive_class`=true · `positive_class`=true |
| CV Random Forest | `concurrency:cross_validation` | `number_of_folds`=10 · `sampling_type`=stratified sampling |
| ↳ Random Forest (Random Forest) | `concurrency:parallel_random_forest` | `number_of_trees`=100 · `criterion`=gini_index · `maximal_depth`=10 · `guess_subset_ratio`=true · `voting_strategy`=confidence vote |
| ↳ Apply Model (Random Forest) | `apply_model` |  |
| ↳ Performance (Random Forest) | `performance_binominal_classification` | `main_criterion`=accuracy · `manually_set_positive_class`=true · `positive_class`=true |
| Optimize Parameters (depth) | `concurrency:optimize_parameters_grid` | `parameters`=[Decision Tree (opt).maximal_depth:[1.0;12.0;11;linear]] |
| ↳ CV opt | `concurrency:cross_validation` | `number_of_folds`=10 · `sampling_type`=stratified sampling |
| ↳ ↳ Decision Tree (opt) | `concurrency:parallel_decision_tree` | `criterion`=gini_index · `maximal_depth`=3 · `apply_pruning`=false · `apply_prepruning`=false |
| ↳ ↳ Apply Model (opt) | `apply_model` |  |
| ↳ ↳ Performance (opt) | `performance_binominal_classification` | `main_criterion`=accuracy · `manually_set_positive_class`=true · `positive_class`=true |
| ↳ Log (depth) | `log` | `log`=[depth:operator.Decision Tree (opt).parameter.maximal_depth, accuracy:operator.CV opt.value.performance main criterion] |
| Log to Data (depth) | `log_to_data` | `log_name`=Log (depth) |
| Random Forest (final) | `concurrency:parallel_random_forest` | `number_of_trees`=100 · `criterion`=gini_index · `maximal_depth`=10 · `guess_subset_ratio`=true · `voting_strategy`=confidence vote |
| Read CSV (new) | `read_csv` | `csv_file`=…/new_heart.csv |
| Apply Model (new) | `apply_model` |  |

---

## R09_classification_workflow

**โน้ตบน canvas:**

- ⚙️ แก้ก่อน (CONFIG) · 1. Read CSV → csv_file · Select Attributes → ตัด id / คอลัมน์ leak (invert_selection = true) · 2. Set Role → label · (label 0/1 → เพิ่ม Numerical to Binominal ก่อน) · 3. ทุก Performance → positive_class (ตอนนี้ = YES) · main_criterion (f_measure / accuracy / recall) · 4. ไม่ใช้โมเดลไหน → ลบ CV ของโมเดลนั้น · hold-out แทน CV → ดู R05 §3 · ผล: res ของแต่ละ CV = performance (เทียบกันในตารางคำตอบ) · ดับเบิลคลิก CV เพื่อแก้พารามิเตอร์ของโมเดล
- §4 ⭐ Baseline vs โมเดล default (10-fold CV) — preprocessing ทั้งหมดอยู่ใน Training pane · KNN / Logistic: Replace Missing + dummy + Normalize · Tree / RF: ไม่ต้อง normalize
- §5 ⭐ Optimize k-NN: k = 1…31 (+ Log) · Edit Parameter Settings เพื่อเปลี่ยนช่วง
- §5 ⭐ Optimize Decision Tree: maximal_depth 2…12 × criterion (+ Log) ·
- §6–§8 โมเดลสุดท้าย (ใส่ค่าที่ดีที่สุดจาก §5 เอง) → ทำนายข้อมูลใหม่ · Decision Tree (final) → maximal_depth / criterion ตามผล optimize · Read CSV (new) → ไฟล์ใหม่

| operator | class | parameter ที่ตั้งไว้ (แก้ตามโจทย์) |
|---|---|---|
| Read CSV | `read_csv` | `csv_file`=…/bank-data.csv |
| Select Attributes | `select_attributes` | `attribute_filter_type`=subset · `attributes`=id · `invert_selection`=true |
| Set Role | `set_role` | `attribute_name`=pep · `target_role`=label |
| Multiply | `multiply` |  |
| Multiply (default) | `multiply` |  |
| CV Baseline | `concurrency:cross_validation` | `number_of_folds`=10 · `sampling_type`=stratified sampling |
| ↳ Default Model (Baseline) | `default_model` | `method`=mode |
| ↳ Apply Model (Baseline) | `apply_model` |  |
| ↳ Performance (Baseline) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=YES |
| CV kNN | `concurrency:cross_validation` | `number_of_folds`=10 · `sampling_type`=stratified sampling |
| ↳ Replace Missing Values (kNN) | `replace_missing_values` | `default`=average · `return_preprocessing_model`=true |
| ↳ Nominal to Numerical (kNN) | `nominal_to_numerical` | `coding_type`=dummy coding · `return_preprocessing_model`=true |
| ↳ Normalize (kNN) | `normalize` | `method`=Z-transformation |
| ↳ k-NN (kNN) | `k_nn` | `k`=5 |
| ↳ Group Models (kNN) | `group_models` |  |
| ↳ Apply Model (kNN) | `apply_model` |  |
| ↳ Performance (kNN) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=YES |
| CV LogReg | `concurrency:cross_validation` | `number_of_folds`=10 · `sampling_type`=stratified sampling |
| ↳ Replace Missing Values (LogReg) | `replace_missing_values` | `default`=average · `return_preprocessing_model`=true |
| ↳ Nominal to Numerical (LogReg) | `nominal_to_numerical` | `coding_type`=dummy coding · `return_preprocessing_model`=true |
| ↳ Logistic Regression (LogReg) | `h2o:logistic_regression` |  |
| ↳ Group Models (LogReg) | `group_models` |  |
| ↳ Apply Model (LogReg) | `apply_model` |  |
| ↳ Performance (LogReg) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=YES |
| CV Tree | `concurrency:cross_validation` | `number_of_folds`=10 · `sampling_type`=stratified sampling |
| ↳ Decision Tree (Tree) | `concurrency:parallel_decision_tree` | `criterion`=gini_index · `maximal_depth`=10 · `apply_pruning`=false · `apply_prepruning`=false |
| ↳ Apply Model (Tree) | `apply_model` |  |
| ↳ Performance (Tree) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=YES |
| CV RF | `concurrency:cross_validation` | `number_of_folds`=10 · `sampling_type`=stratified sampling |
| ↳ Random Forest (RF) | `concurrency:parallel_random_forest` | `number_of_trees`=100 · `criterion`=gini_index · `maximal_depth`=10 · `guess_subset_ratio`=true · `voting_strategy`=confidence vote |
| ↳ Apply Model (RF) | `apply_model` |  |
| ↳ Performance (RF) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=YES |
| Optimize Parameters (kNN) | `concurrency:optimize_parameters_grid` | `parameters`=[k-NN (opt kNN).k:[1.0;31.0;15;linear]] |
| ↳ CV opt kNN | `concurrency:cross_validation` | `number_of_folds`=10 · `sampling_type`=stratified sampling |
| ↳ ↳ Replace Missing Values (opt kNN) | `replace_missing_values` | `default`=average · `return_preprocessing_model`=true |
| ↳ ↳ Nominal to Numerical (opt kNN) | `nominal_to_numerical` | `coding_type`=dummy coding · `return_preprocessing_model`=true |
| ↳ ↳ Normalize (opt kNN) | `normalize` | `method`=Z-transformation |
| ↳ ↳ k-NN (opt kNN) | `k_nn` | `k`=5 |
| ↳ ↳ Group Models (opt kNN) | `group_models` |  |
| ↳ ↳ Apply Model (opt kNN) | `apply_model` |  |
| ↳ ↳ Performance (opt kNN) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=YES |
| ↳ Log (kNN) | `log` | `log`=[k:operator.k-NN (opt kNN).parameter.k, f_measure:operator.CV opt kNN.value.performance main criterion] |
| Log to Data (kNN) | `log_to_data` | `log_name`=Log (kNN) |
| Optimize Parameters (Tree) | `concurrency:optimize_parameters_grid` | `parameters`=[Decision Tree (opt Tree).maximal_depth:[2.0;12.0;10;linear], Decision Tree (opt Tree).criterion:gini_index,information_gain,gain_ratio] |
| ↳ CV opt Tree | `concurrency:cross_validation` | `number_of_folds`=10 · `sampling_type`=stratified sampling |
| ↳ ↳ Decision Tree (opt Tree) | `concurrency:parallel_decision_tree` | `criterion`=gini_index · `maximal_depth`=5 · `apply_pruning`=false · `apply_prepruning`=false |
| ↳ ↳ Apply Model (opt Tree) | `apply_model` |  |
| ↳ ↳ Performance (opt Tree) | `performance_binominal_classification` | `main_criterion`=f_measure · `manually_set_positive_class`=true · `positive_class`=YES |
| ↳ Log (Tree) | `log` | `log`=[depth:operator.Decision Tree (opt Tree).parameter.maximal_depth, criterion:operator.Decision Tree (opt Tree).parameter.criterion, f_measure:operator.CV opt Tree.value.performance main criterion] |
| Log to Data (Tree) | `log_to_data` | `log_name`=Log (Tree) |
| Decision Tree (final) | `concurrency:parallel_decision_tree` | `criterion`=gini_index · `maximal_depth`=6 · `apply_pruning`=false · `apply_prepruning`=false |
| Read CSV (new) | `read_csv` | `csv_file`=…/new_bank.csv |
| Apply Model (new) | `apply_model` |  |

---

## R10_clustering

**โน้ตบน canvas:**

- ⚙️ แก้ก่อน (CONFIG) · 1. Read CSV → csv_file · Set Role → id = ชื่อ/รหัสแถว (ไม่ใช้คำนวณ) · มี label จริง → Set Role (label) หรือ Select Attributes ตัดออก · 2. Clustering (k-Means) → k · max_runs · measure_types = NumericalMeasures / EuclideanDistance · 3. Read CSV (new) → จุดใหม่ (คอลัมน์ feature เดียวกัน) · centroid: res cluster model → Centroid Table (ค่า normalize แล้ว: + สูงกว่าค่าเฉลี่ย, − ต่ำกว่า) · กราฟ: Visualizations / Centroid Chart
- §3 ⭐ k-Means (k = 4) → Cluster Distance Performance (avg within centroid distance + Davies–Bouldin) · res: clustered set (คอลัมน์ cluster) · cluster model (centroid) · performance (cohesion) · main_criterion เปลี่ยนได้
- §3b Profile แต่ละกลุ่มในหน่วยเดิม: Aggregate average ตาม cluster · group_by = cluster · ค่าเฉลี่ยของ feature (เป็นค่า normalize — อยากได้หน่วยเดิม Join กลับกับข้อมูลดิบด้วย id)
- §2 ⭐ เลือก k: Optimize Parameters k = 2…10 + Log (avg within centroid distance → หา elbow) · Log to Data → Visualizations → Line (x = k) · Davies–Bouldin ของ k ที่เลือก ดูใน performance ของ §3 (RapidMiner แสดงค่าติดลบ: ใกล้ 0 = ดี)
- §4 จุดใหม่อยู่ cluster ไหน: Normalize ด้วยค่าเดิม (preprocessing model) → Apply cluster model ·
- §6 ภาพ cluster บน PCA 2D → Visualizations → Scatter pc_1 × pc_2 color = cluster ·
- §7 Hierarchical (Agglomerative) → dendrogram (res: Dendrogram) → Flatten Clustering = ตัดเป็น k กลุ่ม · mode = SingleLink / CompleteLink / AverageLink · number_of_clusters

| operator | class | parameter ที่ตั้งไว้ (แก้ตามโจทย์) |
|---|---|---|
| Read CSV | `read_csv` | `csv_file`=…/utilities.csv |
| Set Role | `set_role` | `attribute_name`=Company · `target_role`=id |
| Normalize | `normalize` | `method`=Z-transformation |
| Multiply | `multiply` |  |
| Clustering | `concurrency:k_means` | `add_cluster_attribute`=true · `k`=4 · `max_runs`=50 · `determine_good_start_values`=true · `measure_types`=NumericalMeasures · `numerical_measure`=EuclideanDistance · `max_optimization_steps`=100 |
| Cluster Distance Performance | `cluster_distance_performance` | `main_criterion`=Avg. within centroid distance · `main_criterion_only`=false |
| Multiply (clustered) | `multiply` |  |
| Multiply (cluster model) | `multiply` |  |
| Aggregate (profile) | `aggregate` | `use_default_aggregation`=true · `default_aggregation_function`=average · `group_by_attributes`=cluster |
| Optimize Parameters (k) | `concurrency:optimize_parameters_grid` | `parameters`=[Clustering (opt).k:[2.0;10.0;8;linear]] |
| ↳ Clustering (opt) | `concurrency:k_means` | `add_cluster_attribute`=true · `k`=2 · `max_runs`=50 · `determine_good_start_values`=true |
| ↳ Cluster Distance Performance (opt) | `cluster_distance_performance` | `main_criterion`=Avg. within centroid distance · `main_criterion_only`=false |
| ↳ Log (k) | `log` | `log`=[k:operator.Clustering (opt).parameter.k, avg_within:operator.Cluster Distance Performance (opt).value.avg_within_distance] |
| Log to Data (k) | `log_to_data` | `log_name`=Log (k) |
| Read CSV (new) | `read_csv` | `csv_file`=…/new_utility.csv |
| Set Role (new) | `set_role` | `attribute_name`=Company · `target_role`=id |
| Apply Model (normalize new) | `apply_model` |  |
| Apply Model (cluster new) | `apply_model` |  |
| PCA (2D) | `principal_component_analysis` | `dimensionality_reduction`=fixed number · `number_of_components`=2 |
| Clustering (Agglomerative) | `agglomerative_clustering` | `mode`=CompleteLink · `measure_types`=NumericalMeasures · `numerical_measure`=EuclideanDistance |
| Flatten Clustering | `flatten_clustering` | `number_of_clusters`=4 |

---

## R11_association_rules

**โน้ตบน canvas:**

- ⚙️ แก้ก่อน (CONFIG) · 1. เลือกแถวที่ตรงกับหน้าตาข้อมูล (A = ตาราง 0/1 ต่อสินค้า · B = ตารางลูกค้า/attribute) แล้วลบแถวที่ไม่ใช้ · 2. Read Excel / Read CSV → ไฟล์ · Set Role → id = รหัสตะกร้า/ลูกค้า · 3. FP-Growth → min_support (สัดส่วน เช่น 0.2) · Create Association Rules → min_confidence · 4. ข้อมูลแบบ 'ตะกร้าคั่นด้วย comma ต่อบรรทัด' → แปลงด้วย Python T11 แล้วใช้แถว A · ผล: res rules → Table (Premises → Conclusion · Support · Confidence · Lift) · เรียงตาม Lift ได้ · res itemsets = frequent itemsets
- A · ตาราง 0/1 (BeautyCo): Read Excel → Set Role id → Numerical to Binominal (0/1 → false/true) → FP-Growth → Rules · min_support = 0.2 · min_confidence = 0.7 · ไฟล์ .csv ใช้ Read CSV แทน Read Excel
- B · ตารางลูกค้า (bank): ตัด id/คอลัมน์ไม่ให้ข้อมูล → Discretize ตัวเลข → Nominal to Binominal → FP-Growth → Rules · Discretize by Frequency → attributes (age\|income) + number_of_bins · Discretize by User Specification → children · Nominal to Binominal → transform_binominal = true
- C · ตาราง 0/1 ขนาดใหญ่ (groceries 169 สินค้า) — เหมือน A แต่ Read CSV · min_support = 0.02 · min_confidence = 0.3

| operator | class | parameter ที่ตั้งไว้ (แก้ตามโจทย์) |
|---|---|---|
| Read Excel (A) | `read_excel` | `excel_file`=…/BeautyCo_68.xls · `sheet_number`=1 |
| Set Role (A) | `set_role` | `attribute_name`=Trans. · `target_role`=id |
| Numerical to Binominal (A) | `numerical_to_binominal` | `attribute_filter_type`=all · `min`=0.0 · `max`=0.0 |
| FP-Growth (A) | `concurrency:fp_growth` | `input_format`=items in dummy coded columns · `positive_value`=true · `min_requirement`=support · `min_support`=0.2 · `find_min_number_of_itemsets`=false · `max_items_per_itemset`=0 |
| Create Association Rules (A) | `create_association_rules` | `criterion`=confidence · `min_confidence`=0.7 |
| Read CSV (B) | `read_csv` | `csv_file`=…/bank-data.csv |
| Select Attributes (B) | `select_attributes` | `attribute_filter_type`=subset · `attributes`=id\|region\|sex\|current_act · `invert_selection`=true |
| Discretize by Frequency (B) | `discretize_by_frequency` | `attribute_filter_type`=subset · `attributes`=age\|income · `number_of_bins`=3 · `range_name_type`=short |
| Discretize by User Specification (B) | `discretize_by_user_specification` | `attribute_filter_type`=single · `attribute`=children · `classes`=[0:0.5, 1-2:2.5, 3+:Infinity] |
| Nominal to Binominal (B) | `nominal_to_binominal` | `attribute_filter_type`=all · `transform_binominal`=true |
| FP-Growth (B) | `concurrency:fp_growth` | `input_format`=items in dummy coded columns · `positive_value`=true · `min_requirement`=support · `min_support`=0.1 · `find_min_number_of_itemsets`=false |
| Create Association Rules (B) | `create_association_rules` | `criterion`=confidence · `min_confidence`=0.7 |
| Read CSV (C) | `read_csv` | `csv_file`=…/p9_groceries_onehot.csv |
| Set Role (C) | `set_role` | `attribute_name`=basket_id · `target_role`=id |
| Numerical to Binominal (C) | `numerical_to_binominal` | `attribute_filter_type`=all · `min`=0.0 · `max`=0.0 |
| FP-Growth (C) | `concurrency:fp_growth` | `input_format`=items in dummy coded columns · `positive_value`=true · `min_requirement`=support · `min_support`=0.02 · `find_min_number_of_itemsets`=false |
| Create Association Rules (C) | `create_association_rules` | `criterion`=confidence · `min_confidence`=0.3 |

