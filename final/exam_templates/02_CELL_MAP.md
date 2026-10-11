# 🗺️ CELL MAP: ทุกจุดที่ต้องแก้ ในทุกไฟล์

> สร้างอัตโนมัติจาก notebook (`_build/make_cellmap.py`) ตรงกับโค้ดจริงเสมอ
> **cell #** = ลำดับ cell นับจาก 0 (cell 0 = หัวเรื่อง · cell 1 = ⚙️ CONFIG · cell 2 = 🔧 helpers ห้ามแก้)
> ทุกไฟล์: แก้ **CONFIG** ก่อนเสมอ → Run All → แล้วค่อยแก้บรรทัด ✏️ ใน § ที่โจทย์ถาม → รัน cell นั้นใหม่
> วิธีใช้แบบละเอียด: [01_MANUAL.md](01_MANUAL.md) · หาไฟล์จากคำในโจทย์: [00_INDEX.md](00_INDEX.md)

---

## T01 · Data Handling & Visualization (Import · Inspect · Select · Filter · Set Role · Join · Concatenate · Pivot · Charts)

ไฟล์ `T01_data_handling_viz.ipynb` · 35 cells

### ⚙️ CONFIG (cell 1)

| ตัวแปร | ค่าตัวอย่าง | ความหมาย / ตัวเลือก |
|---|---|---|
| `DATA_PATH` | `"../practice/data/p1_bills_week1.csv"` | ไฟล์หลัก (.csv / .xlsx / .xls) |
| `DATA_PATH_2` | `"../practice/data/p1_bills_week2.csv"` | ไฟล์ที่จะ "ต่อแถว" (concatenate/append) — ไม่มีใส่ None |
| `LOOKUP_PATH` | `"../practice/data/p1_day_info.csv"` | ไฟล์ที่จะ "join" เข้ามา — ไม่มีใส่ None |
| `JOIN_KEY` | `"day"` | คอลัมน์ที่ใช้จับคู่ (ชื่อต่างกัน 2 ฝั่ง → ใส่ tuple เช่น ("cust_id", "id")) |
| `JOIN_HOW` | `"left"` | "inner" = เฉพาะที่ตรงกัน · "left" = เก็บทุกแถวของไฟล์หลัก · "outer" = เก็บทั้งหมด |
| `ID_COL` | `"bill_id"` | คอลัมน์ id (ไม่มีใส่ None) |
| `TARGET` | `"tip"` | คอลัมน์ที่โจทย์สนใจ/label (ไม่มีใส่ None) |
| `SHEET` | `0` | ชื่อ/ลำดับ sheet ถ้าเป็น Excel |
| `CSV_SEP` | `","` | ตัวคั่น csv (บางไฟล์ใช้ ";") |
| `MISSING_MARKERS` | `["?", "", " ", "NA", "N/A", "null", "-"]` | ค่าที่แปลว่า "ว่าง" ในไฟล์นี้ |
| `SEED` | `42` |  |

### § ต่าง ๆ และบรรทัด ✏️ ที่แก้ได้

| cell # | § | ✏️ แก้ในเซลล์ (ถ้าโจทย์ต้องการ) |
|---|---|---|
| 3 | §1 Import + ตรวจข้อมูล (Inspect) — รันเสมอ | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 7 | §2 Select Attributes (เลือก/ตัดคอลัมน์) + Set Role | cell 8: `KEEP_COLS = None` — list ของคอลัมน์ที่ "เก็บ" เช่น ["total_bill", "tip", "day"] · None = เก็บทั้งหมด<br>cell 8: `DROP_THESE = []` — list ของคอลัมน์ที่ "ตัด" เช่น ["size"]<br>cell 8: `BY_TYPE = None` — "number" = เก็บเฉพาะตัวเลข · "category" = เฉพาะหมวดหมู่ · None = ไม่กรองตามชนิด |
| 10 | §3 Filter Examples (กรองแถว) | cell 11: `FILTER = "total_bill > 20 and smoker == 'Yes'"` — เงื่อนไข<br>cell 11: `DROP_MISSING_ROWS_IN = []` — ตัดแถวที่คอลัมน์เหล่านี้ว่าง (= Filter: is not missing)<br>cell 11: `print(f"⚠️ FILTER ใช้กับข้อมูลนี้ไม่ได้ ({type(e).__name__}: {e}) → แก` |
| 13 | §4 Concatenate / Append (ต่อแถว — ไฟล์คอลัมน์เดียวกัน เช่นข้อมูลคนละช่วงเวลา) | cell 14: `df = both.drop(columns="source")` — ใช้ข้อมูลที่ต่อแล้วเป็น df หลักต่อจากนี้ (ไม่ต้องการ → comment บรรทัดนี้) |
| 16 | §5 Join / Merge (เพิ่มคอลัมน์จากอีกตารางด้วย key) | cell 17: `df = joined` — ใช้ผล join เป็น df หลักต่อจากนี้ |
| 19 | §6 Aggregate / Group by | cell 20: `GROUP_BY = ["day"]` — จัดกลุ่มตาม (1 หรือหลายคอลัมน์)<br>cell 20: `AGG = {"total_bill": ["count", "mean", "sum"], "tip": ["mean", "max"]}` — คอลัมน์: [ฟังก์ชัน] |
| 22 | §7 Pivot table / Crosstab | cell 23: `PIV_INDEX, PIV_COLUMNS, PIV_VALUES, PIV_FUNC = "day", "time", "tip", "` — แถว, คอลัมน์, ค่า, ฟังก์ชัน (mean/sum/count/max)<br>cell 23: `RATE_OF = None` — หา "สัดส่วน" ของคลาส เช่น ("income", ">50K") → ใช้แทน PIV_VALUES · None = ไม่ใช้ |
| 25 | §8 Generate Attributes (สร้างคอลัมน์ใหม่) + แปลงชนิด | cell 26 — แก้/เพิ่มสูตรตามโจทย์ (ตัวอย่างใช้คอลัมน์ของข้อมูล tips — ข้อมูลอื่นให้เปลี่ยนชื่อคอลัมน์)<br>cell 26: `print(f"⚠️ สูตรตัวอย่างใช้คอลัมน์ {e} ที่ไม่มีในข้อมูลนี้ → แก้สูตร ✏️` |
| 27 | §9 กราฟพื้นฐาน + ตีความ | cell 28: `NUM_COL = "total_bill"` — ตัวเลขที่จะดูการกระจาย<br>cell 28: `CAT_COL = "day"` — หมวดหมู่ที่จะแยกกลุ่ม<br>cell 28: `X_COL, Y_COL = "total_bill", "tip"` — scatter<br>cell 28: `HUE = "smoker"` — ระบายสีตาม (เช่น label) · None ได้<br>cell 29: `STACK_GROUP, STACK_CLASS = "day", "smoker"` — กลุ่ม (แกน x), คลาสที่จะดูสัดส่วน |
| 30 | §10 Correlation heatmap (+ คู่ที่สัมพันธ์สูง) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 33 | §11 Save ผลลัพธ์ (ถ้าโจทย์ให้ส่งไฟล์) | cell 34: `OUT_PATH = "t01_result.csv"` — ชื่อไฟล์ผลลัพธ์ |

---

## T02 · Data Preprocessing (Missing · Outlier · Encoding · Scaling · Discretization · Sampling · Split ไม่ leak · Feature selection)

ไฟล์ `T02_preprocessing.ipynb` · 31 cells

### ⚙️ CONFIG (cell 1)

| ตัวแปร | ค่าตัวอย่าง | ความหมาย / ตัวเลือก |
|---|---|---|
| `DATA_PATH` | `"../practice/data/p2_penguins.csv"` |  |
| `TARGET` | `"species"` | label (ไม่มีใส่ None) |
| `POS_LABEL` | `None` | ถ้า target มี 2 คลาส: คลาสที่สนใจ (เช่น "Yes", 1, ">50K") · None = เลือกตัวท้ายตามตัวอักษร |
| `ID_COL` | `None` | คอลัมน์ id |
| `DROP_COLS` | `[]` | คอลัมน์ที่ตัดทิ้งแน่นอน (leak / ไม่เกี่ยว) |
| `MISSING_MARKERS` | `["?", "", " ", "NA", "N/A", "null", "-"]` |  |
| `ZERO_AS_MISSING` | `[]` | คอลัมน์ที่ค่า 0 เป็นไปไม่ได้ = ค่าว่าง (เช่น pima: ["glucose", "bmi", "blood_pressure"]) |
| `SCALE` | `"standard"` | "standard" (z-score) \| "minmax" (0–1) \| None |
| `TEST_SIZE` | `0.2` |  |
| `SEED` | `42` |  |
| `N_FOLDS` | `5` |  |
| `SHEET, CSV_SEP` | `0, ","` |  |

### § ต่าง ๆ และบรรทัด ✏️ ที่แก้ได้

| cell # | § | ✏️ แก้ในเซลล์ (ถ้าโจทย์ต้องการ) |
|---|---|---|
| 3 | §1 โหลด + สำรวจค่าว่าง (รันเสมอ) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 6 | §2 Missing-value handling — เลือกวิธี | cell 7: `MISS_METHOD = "median"` — "drop_rows" \| "drop_cols" \| "mean" \| "median" \| "mode" \| "constant" \| "group"<br>cell 7: `DROP_COL_THRESHOLD = 0.5` — ใช้กับ drop_cols: ตัดคอลัมน์ที่ว่างเกินสัดส่วนนี้<br>cell 7: `CONSTANT = "Unknown"` — ใช้กับ constant (หมวดหมู่) — ตัวเลขจะเติม 0<br>cell 7: `GROUP_COL = TARGET` — ใช้กับ group: เติม median/mode ตามกลุ่มนี้ |
| 9 | §3 Outliers (IQR rule: < Q1 − 1.5·IQR หรือ > Q3 + 1.5·IQR) | cell 10: `OUT_METHOD = None` — None = แค่นับ · "clip" = ตัดให้อยู่ในขอบ (winsorize) · "remove" = ลบแถว |
| 11 | §4 Encoding categorical attributes | cell 12: `ORDINAL_MAP = {}` — เช่น {"education": ["low", "mid", "high"]} (เรียงจากน้อยไปมาก)<br>cell 12: `BINARY_MAP  = {}` — เช่น {"smoker": {"yes": 1, "no": 0}}<br>cell 12: `DROP_FIRST  = False` — True = ตัด dummy ตัวแรก (กัน multicollinearity ใน linear/logistic regression) |
| 14 | §5 Standardization vs Normalization | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 17 | §6 Discretization (แบ่งช่วง / binning) | cell 18: `DISC_COL = "body_mass_g"` — คอลัมน์ที่จะแบ่ง<br>cell 18: `N_BINS   = 3` — จำนวนช่วง<br>cell 18: `LABELS   = ["Low", "Mid", "High"]` — ชื่อช่วง (ต้องยาว = N_BINS) · None = แสดงช่วงตัวเลข<br>cell 18: `USER_BINS = [0, 3500, 4500, np.inf]` — ขอบเขตกำหนดเอง (ขวาปิด: (a, b]) |
| 20 | §7 Sampling (สุ่มตัวอย่าง) | cell 21: `SAMPLE_FRAC = 0.3` — สัดส่วนที่สุ่ม (หรือใช้ n=… แทน) |
| 22 | §8 แบ่งข้อมูลโดย ไม่เกิด data leakage ⭐ (วิธีที่ถูกต้องตอนสร้างโมเดล) | cell 24: `MODEL_FOR_COMPARE = KNeighborsClassifier(n_neighbors=5)` — เปลี่ยนโมเดลได้ |
| 26 | §9 Feature selection | cell 27: `K_BEST = 3` — จำนวน feature ที่จะเลือก |
| 29 | §10 Save ข้อมูลที่ preprocess แล้ว (ถ้าโจทย์ให้ส่งไฟล์) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |

---

## T03 · PCA (Dimensionality Reduction + 2D Visualization)

ไฟล์ `T03_pca.ipynb` · 22 cells

### ⚙️ CONFIG (cell 1)

| ตัวแปร | ค่าตัวอย่าง | ความหมาย / ตัวเลือก |
|---|---|---|
| `DATA_PATH` | `"../practice/data/p4_wine.csv"` |  |
| `TARGET` | `"cultivar"` | คอลัมน์ class ไว้ "ระบายสี" กราฟ / เทียบโมเดล (ไม่มีใส่ None) |
| `POS_LABEL` | `None` |  |
| `ID_COL` | `None` | ชื่อ/รหัสแถว (ใช้เขียน label บนจุด ถ้ามี) |
| `DROP_COLS` | `[]` | คอลัมน์ที่ไม่ใช้ทำ PCA |
| `FEATURES` | `None` | list feature ที่จะใช้ · None = ตัวเลขทุกคอลัมน์ (ยกเว้น TARGET/ID/DROP) |
| `STANDARDIZE` | `True` | True = z-score ก่อน PCA (ปกติต้อง True) |
| `VAR_TARGET` | `0.80` | เกณฑ์ cumulative variance ที่โจทย์ถาม (0.80 / 0.90 / 0.95) |
| `N_LOADINGS` | `3` | แสดง loadings ของกี่ PC |
| `NEW_POINT` | `None` | dict ข้อมูลใหม่ที่จะแปลงเป็น PC เช่น {"alcohol": 13.0, ...} · None = ข้าม |
| `SEED, N_FOLDS` | `42, 5` |  |
| `MISSING_MARKERS, SHEET, CSV_SEP` | `["?", "", " ", "NA"], 0, ","` |  |

### § ต่าง ๆ และบรรทัด ✏️ ที่แก้ได้

| cell # | § | ✏️ แก้ในเซลล์ (ถ้าโจทย์ต้องการ) |
|---|---|---|
| 3 | §1 โหลด + เลือก feature ตัวเลข | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 5 | §2 Standardize → PCA (ทุก component) → ตาราง explained variance | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 9 | §3 Loadings — ตัวแปรไหนขับเคลื่อน PC แต่ละตัว | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 12 | §4 PCA 2D visualization (scatter PC1 × PC2 ระบายสีตาม class) + biplot | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 15 | §5 PCA ก่อนสร้างโมเดล — เทียบก่อน/หลัง (ไม่ leak: scaler + PCA อยู่ใน Pipeline) | cell 16: `MODEL = KNeighborsClassifier(n_neighbors=5)` — เปลี่ยนโมเดลได้ (เช่น LogisticRegression(max_iter=1000)) |
| 18 | §6 แปลงข้อมูลใหม่เป็นคะแนน PC (ใช้ scaler + PCA ตัวเดิม) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 20 | §7 Save คะแนน PC (ถ้าต้องส่ง) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |

---

## T04 · Imbalanced Classification (Undersampling · Oversampling · SMOTE · Cost-sensitive · Threshold)

ไฟล์ `T04_imbalanced_smote.ipynb` · 20 cells

### ⚙️ CONFIG (cell 1)

| ตัวแปร | ค่าตัวอย่าง | ความหมาย / ตัวเลือก |
|---|---|---|
| `DATA_PATH` | `"../practice/data/p3_breast_cancer_imbalanced.csv"` |  |
| `TARGET` | `"diagnosis"` |  |
| `POS_LABEL` | `"malignant"` | คลาสส่วนน้อย/คลาสที่สนใจ (= 1) |
| `ID_COL` | `None` |  |
| `DROP_COLS` | `[]` |  |
| `SCALE` | `"standard"` |  |
| `MODEL_NAME` | `"LogReg"` | โมเดลหลักที่จะลอง resampling: "LogReg" \| "KNN" \| "Tree" \| "RF" |
| `PRIMARY_METRIC` | `"f1"` | metric ที่ใช้เลือก: "f1" \| "recall" \| "precision" |
| `SMOTE_K` | `5` | k_neighbors ของ SMOTE |
| `EVAL_MODE` | `"cv"` | "cv" = stratified k-fold · "holdout" = แบ่ง train/test |
| `N_FOLDS, TEST_SIZE, SEED` | `5, 0.2, 42` |  |
| `MISSING_MARKERS, SHEET, CSV_SEP` | `["?", "", " ", "NA"], 0, ","` |  |

### § ต่าง ๆ และบรรทัด ✏️ ที่แก้ได้

| cell # | § | ✏️ แก้ในเซลล์ (ถ้าโจทย์ต้องการ) |
|---|---|---|
| 3 | §1 โหลด + ดูความไม่สมดุล | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 5 | §2 ทำไม accuracy หลอก — majority baseline | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 7 | §3 Resampling บน training set (สาธิต: จำนวนก่อน/หลัง — test ไม่ถูกแตะ) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 9 | §4 เปรียบเทียบ: ไม่ทำอะไร vs Under vs Over vs SMOTE vs class_weight ⭐ | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 12 | §5 Confusion matrix: ไม่ resample vs SMOTE (cross_val_predict — ทุกแถวถูกทำนายตอนอยู่ใน validation fold) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 15 | §6 ❌ วิธีผิด: SMOTE ทั้งตารางก่อน CV (data leakage) — ไว้ตอบคำถาม "ทำไมห้าม" | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 17 | §7 ปรับ threshold (อีกทางแก้ imbalance — ไม่ต้อง resample) | cell 18: `THRESHOLDS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]` |
| 19 | §8 เลือก metric ให้เหมาะกับปัญหา (copy ไปตอบ) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |

---

## T05 · K-Nearest Neighbors (Distance · Classification · Regression · เลือก k · Scale ก่อน/หลัง)

ไฟล์ `T05_knn.ipynb` · 22 cells

### ⚙️ CONFIG (cell 1)

| ตัวแปร | ค่าตัวอย่าง | ความหมาย / ตัวเลือก |
|---|---|---|
| `DATA_PATH` | `"../data/riding_mowers.csv"` |  |
| `TARGET` | `"Ownership"` |  |
| `POS_LABEL` | `"Owner"` |  |
| `ID_COL` | `None` |  |
| `DROP_COLS` | `[]` |  |
| `NEW_POINT` | `{"Income": 60, "Lot_Size": 20}` | ข้อมูลใหม่ (dict / list ของ dict / path .csv) · None = ข้าม |
| `K` | `3` | k ที่โจทย์กำหนด |
| `METRIC` | `"euclidean"` | "euclidean" \| "manhattan" \| "minkowski" (ใช้ P_MINKOWSKI) |
| `P_MINKOWSKI` | `3` |  |
| `WEIGHTS` | `"uniform"` | "uniform" = vote เท่ากัน \| "distance" = ใกล้กว่าเสียงดังกว่า (1/d) |
| `SCALE` | `"standard"` | "standard" \| "minmax" \| None  (KNN ควร scale เสมอ) |
| `K_MAX` | `25` | ลอง k = 1..K_MAX ตอนหา k ที่ดีที่สุด |
| `EVAL_MODE` | `"cv"` | "cv" \| "holdout" |
| `N_FOLDS, TEST_SIZE, SEED` | `5, 0.2, 42` |  |
| `MISSING_MARKERS, SHEET, CSV_SEP` | `["?", "", " ", "NA"], 0, ","` |  |

### § ต่าง ๆ และบรรทัด ✏️ ที่แก้ได้

| cell # | § | ✏️ แก้ในเซลล์ (ถ้าโจทย์ต้องการ) |
|---|---|---|
| 3 | §1 โหลด + ภาพข้อมูล (2 feature แรก) + จุดใหม่ | cell 4: `fx, fy = nums[:2]` — เปลี่ยนคู่แกนที่จะวาดได้ |
| 5 | §2 คำนวณระยะทางด้วยมือ → k เพื่อนบ้านใกล้สุด → vote | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 8 | §3 KNN แบบ hold-out (train/test) — scaler fit บน train เท่านั้น | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 10 | §4 CV: baseline vs KNN ไม่ scale vs scale (เปรียบเทียบก่อน/หลัง preprocessing) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 13 | §5 เลือก k ที่ดีที่สุด (k-curve + GridSearchCV) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 16 | §6 โมเดลสุดท้าย → ทำนายข้อมูลใหม่ (probability = สัดส่วน vote) | cell 17: `final = grid.best_estimator_` — หรือใช้ make_pipe(knn_model(K), X).fit(X, y) ถ้าโจทย์บังคับ k |
| 19 | §7 KNN Regression (ทำนายตัวเลข = ค่าเฉลี่ยของ y ของ k เพื่อนบ้าน) | cell 20: `REG_DATA_PATH = "../mock_lab/mock2_regression_pca/data/housing.csv"`<br>cell 20: `REG_TARGET    = "medv"` — target ตัวเลข<br>cell 20: `REG_DROP      = []`<br>cell 20: `REG_NEW       = None` — dict ข้อมูลใหม่ · None = ข้าม<br>cell 20: `REG_K         = 5` |

---

## T06 · Linear Regression (Equation · Coefficients · Prediction · MAE/MSE/RMSE/R² · Baseline · เทียบโมเดล regression)

ไฟล์ `T06_linear_regression.ipynb` · 21 cells

### ⚙️ CONFIG (cell 1)

| ตัวแปร | ค่าตัวอย่าง | ความหมาย / ตัวเลือก |
|---|---|---|
| `DATA_PATH` | `"../practice/data/p7_insurance.csv"` |  |
| `TARGET` | `"charges"` | ตัวเลขที่จะทำนาย |
| `ID_COL` | `None` |  |
| `DROP_COLS` | `[]` |  |
| `FEATURES` | `None` | list feature ที่โจทย์ให้ใช้ · None = ทุกคอลัมน์ที่เหลือ |
| `SIMPLE_X` | `"age"` | ตัวแปรเดียวสำหรับ simple linear regression (None = ข้าม §3) |
| `DROP_FIRST` | `True` | one-hot ตัด dummy ตัวแรก (reference category) → ตีความ coef ง่าย ไม่ซ้ำซ้อน |
| `NEW_DATA` | `{"age": 40, "sex": "male", "bmi": 30.0, "children": 2, "s…` | None = ข้าม |
| `EVAL_MODE` | `"holdout"` | "holdout" (train/test) \| "cv" |
| `TEST_SIZE, N_FOLDS, SEED` | `0.2, 5, 42` |  |
| `MISSING_MARKERS, SHEET, CSV_SEP` | `["?", "", " ", "NA"], 0, ","` |  |

### § ต่าง ๆ และบรรทัด ✏️ ที่แก้ได้

| cell # | § | ✏️ แก้ในเซลล์ (ถ้าโจทย์ต้องการ) |
|---|---|---|
| 3 | §1 โหลด + EDA ของ target + correlation กับ target | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 5 | §2 แบ่ง train/test (fit ทุกอย่างบน train) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 7 | §3 Simple linear regression: $\hat y = b_0 + b_1 x$ | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 9 | §4 Multiple linear regression — สมการเต็ม + coefficient (หน่วยเดิม → ตีความได้) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 12 | §5 Evaluation: mean baseline vs simple vs multiple (MAE / MSE / RMSE / R²) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 15 | §6 เทียบโมเดล regression อื่น + optimize (CV บน train) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 18 | §7 ทำนายข้อมูลใหม่ | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |

---

## T07 · Logistic Regression (Probability · Threshold · Coefficients / Odds ratio · Evaluation · ROC)

ไฟล์ `T07_logistic_regression.ipynb` · 20 cells

### ⚙️ CONFIG (cell 1)

| ตัวแปร | ค่าตัวอย่าง | ความหมาย / ตัวเลือก |
|---|---|---|
| `DATA_PATH` | `"../practice/data/p5_pima_diabetes.csv"` |  |
| `TARGET` | `"diabetes"` |  |
| `POS_LABEL` | `1` | คลาสที่สนใจ (= 1) |
| `ID_COL` | `None` |  |
| `DROP_COLS` | `[]` |  |
| `FEATURES` | `None` | list feature ที่โจทย์ให้ใช้ · None = ทั้งหมด |
| `ZERO_AS_MISSING` | `["glucose", "blood_pressure", "skin_thickness", "insulin"…` | ข้อมูลอื่นใส่ [] |
| `THRESHOLD` | `0.3` | threshold ที่โจทย์ให้ลอง (เทียบกับ 0.5) |
| `THRESHOLDS` | `[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]` |  |
| `NEW_DATA` | `{"pregnancies": 2, "glucose": 150, "blood_pressure": 70, …` |  |
| `SCALE` | `"standard"` |  |
| `TEST_SIZE, N_FOLDS, SEED` | `0.2, 5, 42` |  |
| `MISSING_MARKERS, SHEET, CSV_SEP` | `["?", "", " ", "NA"], 0, ","` |  |

### § ต่าง ๆ และบรรทัด ✏️ ที่แก้ได้

| cell # | § | ✏️ แก้ในเซลล์ (ถ้าโจทย์ต้องการ) |
|---|---|---|
| 3 | §1 โหลด + เตรียม X / y + split | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 5 | §2 Fit + baseline (hold-out และ CV) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 7 | §3 Coefficients → Odds ratio (ตีความ) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 10 | §4 คำนวณความน่าจะเป็นด้วยมือ (แถวแรกของ test) — ตรวจกับ predict_proba | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 12 | §5 Threshold — ตาราง confusion matrix + metrics ทุก threshold ⭐ | cell 13: `SOURCE = "holdout"` — "holdout" = ใช้ test set · "cv" = cross_val_predict ทั้งชุด |
| 16 | §6 Tune C (regularization) + เทียบก่อน/หลัง (CV) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 18 | §7 ทำนายข้อมูลใหม่ (probability + คำตัดสินที่ threshold 0.5 และ THRESHOLD) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |

---

## T08 · Decision Tree & Random Forest (Gini/Entropy/Gain · Tree construction · Rules · Overfitting · Parameters · RF)

ไฟล์ `T08_decision_tree_rf.ipynb` · 23 cells

### ⚙️ CONFIG (cell 1)

| ตัวแปร | ค่าตัวอย่าง | ความหมาย / ตัวเลือก |
|---|---|---|
| `DATA_PATH` | `"../practice/data/p6_heart.csv"` |  |
| `TARGET` | `"target"` |  |
| `POS_LABEL` | `1` |  |
| `ID_COL` | `None` |  |
| `DROP_COLS` | `[]` |  |
| `CRITERION` | `"gini"` | "gini" \| "entropy" (= information gain) |
| `MAX_DEPTH` | `3` | ความลึกที่โจทย์กำหนด (None = โตจนสุด) |
| `MIN_LEAF` | `1` | min_samples_leaf |
| `N_TREES` | `100` | Random Forest n_estimators |
| `NEW_DATA` | `None` | dict ข้อมูลใหม่ / path .csv · None = ใช้แถวแรกของ test เป็นตัวอย่าง |
| `EVAL_MODE` | `"cv"` |  |
| `SCALE` | `None` | tree ไม่ต้อง scale |
| `TEST_SIZE, N_FOLDS, SEED` | `0.2, 5, 42` |  |
| `MISSING_MARKERS, SHEET, CSV_SEP` | `["?", "", " ", "NA"], 0, ","` |  |

### § ต่าง ๆ และบรรทัด ✏️ ที่แก้ได้

| cell # | § | ✏️ แก้ในเซลล์ (ถ้าโจทย์ต้องการ) |
|---|---|---|
| 3 | §0 คำนวณ impurity ด้วยมือ — เลือก attribute ที่ดีที่สุดเป็น root | cell 4: `IMP_PATH   = "../data/weather.csv"` — ข้อมูลเล็กที่โจทย์ให้คำนวณมือ (ใช้ DATA_PATH ก็ได้)<br>cell 4: `IMP_TARGET = "Class"`<br>cell 4: `IMP_DROP   = []` — เช่น ["Tid"] |
| 6 | §1 โหลด + split | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 8 | §2 Decision Tree (ตามที่โจทย์กำหนด) → วาดต้นไม้ + กฎ IF-THEN + feature importance | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 12 | §3 Overfitting — train vs CV accuracy ตาม max_depth | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 14 | §4 Tune Decision Tree (GridSearchCV: max_depth × min_samples_leaf × criterion) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 16 | §5 Random Forest (bagging หลายต้น + สุ่ม feature ทุก split → variance ต่ำกว่า, overfit น้อยกว่า) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 18 | §6 เปรียบเทียบ baseline vs DT vs RF (ก่อน/หลัง optimize) ⭐ | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 21 | §7 ทำนายข้อมูลใหม่ + อธิบายเส้นทางในต้นไม้ | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |

---

## T09 · Classification Workflow ครบวงจร (Baseline → หลายโมเดล → Optimize → เทียบก่อน/หลัง → เลือกโมเดล → ทำนาย)

ไฟล์ `T09_classification_workflow.ipynb` · 21 cells

### ⚙️ CONFIG (cell 1)

| ตัวแปร | ค่าตัวอย่าง | ความหมาย / ตัวเลือก |
|---|---|---|
| `DATA_PATH` | `"../mock_lab/mock3_cluster_assoc/data/bank-data.csv"` |  |
| `TARGET` | `"pep"` |  |
| `POS_LABEL` | `"YES"` | คลาสที่สนใจ (= 1) |
| `ID_COL` | `"id"` |  |
| `DROP_COLS` | `[]` | คอลัมน์ที่ตัด (leak / ไม่เกี่ยว) |
| `EVAL_MODE` | `"cv"` | "cv" = k-fold ทั้งชุด · "holdout" = tune ด้วย CV บน train แล้ววัดบน test |
| `PRIMARY_METRIC` | `"f1"` | "f1" \| "accuracy" \| "recall" \| "precision" (เลือกตามโจทย์/ความไม่สมดุล) |
| `SCALE` | `"standard"` | สำหรับ KNN / Logistic (Tree/RF ไม่ scale อัตโนมัติ) |
| `USE_SMOTE` | `False` | True = ใส่ SMOTE ใน pipeline (เฉพาะ training fold) |
| `NEW_DATA` | `None` | dict / list / path .csv ของข้อมูลใหม่ · None = ข้าม |
| `TEST_SIZE, N_FOLDS, SEED` | `0.2, 10, 42` |  |
| `MISSING_MARKERS, SHEET, CSV_SEP` | `["?", "", " ", "NA"], 0, ","` |  |

### § ต่าง ๆ และบรรทัด ✏️ ที่แก้ได้

| cell # | § | ✏️ แก้ในเซลล์ (ถ้าโจทย์ต้องการ) |
|---|---|---|
| 3 | §1 โหลด + ตรวจข้อมูล | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 5 | §2 แบ่งข้อมูล + กำหนดวิธีประเมิน | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 7 | §3 Baseline + โมเดล default + grid สำหรับ optimize (✏️ แก้ค่าตามโจทย์ได้ที่นี่) | cell 8: `MODELS = {` — ชื่อ: (pipeline, ข้อความ settings)<br>cell 8: `GRIDS = {` — ช่วงค่าที่จะลอง (ชื่อ model__<parameter>) |
| 9 | §4 Baseline vs โมเดล default ⭐ | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 12 | §5 Optimize parameters (GridSearchCV บน train/CV — เลือกด้วย PRIMARY_METRIC) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 14 | §6 เปรียบเทียบก่อน vs หลัง optimize ⭐ | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 16 | §7 เลือกโมเดลสุดท้าย → confusion matrix | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 19 | §8 ทำนายข้อมูลใหม่ | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |

---

## T10 · Clustering (K-Means · เลือก k · Centroid/Profile · Cohesion/Separation · Hierarchical/Dendrogram)

ไฟล์ `T10_clustering.ipynb` · 25 cells

### ⚙️ CONFIG (cell 1)

| ตัวแปร | ค่าตัวอย่าง | ความหมาย / ตัวเลือก |
|---|---|---|
| `DATA_PATH` | `"../data/utilities.csv"` |  |
| `ID_COL` | `"Company"` | ชื่อ/รหัสแถว (ไม่ใช้คำนวณ ใช้ติดป้าย) |
| `LABEL_COL` | `None` | ถ้าข้อมูลมี class จริง (ไว้เทียบหลัง cluster เท่านั้น ห้ามใช้ตอน cluster) · None = ไม่มี |
| `DROP_COLS` | `[]` | คอลัมน์ที่ไม่ใช้ |
| `FEATURES` | `None` | list feature ที่ใช้ cluster · None = ตัวเลขทุกคอลัมน์ที่เหลือ |
| `SCALE` | `"standard"` | "standard" (z-score) \| "minmax" \| None — K-Means ใช้ระยะทาง ควร scale |
| `K_RANGE` | `range(2, 9)` | ช่วง k ที่ลอง |
| `K_FINAL` | `4` | k ที่ใช้จริง (None = เลือก k ที่ silhouette สูงสุด) |
| `N_INIT` | `50` | จำนวนรอบสุ่ม centroid เริ่มต้น (เลือกรอบที่ WCSS ต่ำสุด) |
| `MAX_ITER` | `300` |  |
| `NEW_POINT` | `{"Fixed_charge": 1.10, "RoR": 11.0, "Cost": 160, "Load_fa…` |  |
| `LINKAGE` | `"ward"` | hierarchical: "ward" \| "complete" \| "average" \| "single" |
| `SEED` | `42` |  |
| `MISSING_MARKERS, SHEET, CSV_SEP` | `["?", "", " ", "NA"], 0, ","` |  |

### § ต่าง ๆ และบรรทัด ✏️ ที่แก้ได้

| cell # | § | ✏️ แก้ในเซลล์ (ถ้าโจทย์ต้องการ) |
|---|---|---|
| 3 | §1 เตรียมข้อมูล: ตัด id/label · เลือก feature ตัวเลข · จัดการค่าว่าง · scale | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 6 | §2 เลือกจำนวน cluster k | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 9 | §3 K-Means ด้วย k ที่เลือก → สมาชิก · centroid (หน่วยเดิม + z-score) · profile · ตั้งชื่อกลุ่ม | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 12 | §4 จุดใหม่อยู่ cluster ไหน (scale ด้วย scaler ตัวเดิม → หา centroid ที่ใกล้สุด) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 14 | §5 Cohesion & Separation + silhouette ต่อกลุ่ม | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 16 | §6 ภาพ cluster บน PCA 2D (ใส่ชื่อจุด) | cell 17 — scatter 2 feature เดิม ( เลือกคู่) |
| 19 | §7 Hierarchical clustering + Dendrogram | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 21 | §8 เทียบกับ label จริง (ถ้ามี — ใช้ประเมินภายนอกเท่านั้น) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 23 | §9 K-Means ทีละรอบด้วยมือ (โจทย์ให้จุดเล็ก ๆ + centroid เริ่มต้น) | cell 24: `HAND_POINTS = {"A1": (3, 8), "A2": (9, 4), "A3": (4, 9), "A4": (2, 2),` — ชื่อ: (x, y, ...)<br>cell 24: `HAND_INIT   = ["A1", "A4", "A7"]` — ชื่อจุดที่เป็น seed · หรือพิกัดตรง ๆ เช่น [(2, 10), (5, 8), (1, 2)]<br>cell 24: `HAND_DIST   = "euclidean"` — "euclidean" \| "manhattan"<br>cell 24: `HAND_SHOW_SQUARED = False` — True = แสดงระยะยกกำลังสอง (ไม่ถอดราก) แบบที่บางโจทย์ใช้ |

---

## T11 · Association Rules (Transaction data · Frequent itemsets · Apriori / FP-Growth · Rules · Support / Confidence / Lift)

ไฟล์ `T11_association_rules.ipynb` · 25 cells

### ⚙️ CONFIG (cell 1)

| ตัวแปร | ค่าตัวอย่าง | ความหมาย / ตัวเลือก |
|---|---|---|
| `DATA_PATH` | `"../practice/data/p9_groceries_baskets.csv"` |  |
| | | ตัวอย่างอื่น: "../../W10/BeautyCo_68.xls" (FORMAT="onehot", ID_COL="Trans.") |
| | | "../mock_lab/mock3_cluster_assoc/data/bank-data.csv" (FORMAT="table", ID_COL="id", BINS ด้านล่าง) |
| `FORMAT` | `"auto"` | "basket" \| "onehot" \| "long" \| "table" \| "auto" |
| `ID_COL` | `None` | คอลัมน์รหัสตะกร้า/ลูกค้า (ไม่ใช่สินค้า) เช่น "Trans." · None = ไม่มี |
| `DROP_COLS` | `[]` | คอลัมน์ที่ไม่เอามาหากฎ (เช่น region, sex ที่ไม่ให้ข้อมูล) |
| `LONG_TID, LONG_ITEM` | `"tid", "item"` | ใช้เมื่อ FORMAT = "long" |
| `BASKET_SEP` | `","` | ตัวคั่นสินค้าในไฟล์ basket |
| | | FORMAT = "table": คอลัมน์ตัวเลขต้อง discretize ก่อน |
| `BINS` | `{}` | {"age": 3, "income": 3} = แบ่ง 3 ช่วง · {"children": [-1, 0, 2, 10]} = กำหนดขอบเอง |
| `BIN_METHOD` | `"frequency"` | "frequency" (equal frequency, เหมาะกับข้อมูลเบ้) \| "width" (equal width) |
| `BIN_LABELS` | `None` | เช่น ["LOW", "MID", "HIGH"] · None = ใช้ช่วงตัวเลข |
| `ALGO` | `"apriori"` | "apriori" \| "fpgrowth" (ผลเหมือนกัน fpgrowth เร็วกว่า · RapidMiner ใช้ FP-Growth) |
| `MIN_SUPPORT` | `0.02` | สัดส่วน (0.02 = 2% ของตะกร้า) · โจทย์ให้เป็น "จำนวนครั้ง" → หารด้วยจำนวนตะกร้า |
| `MIN_CONFIDENCE` | `0.30` |  |
| `MAX_LEN` | `None` | ขนาด itemset สูงสุด (None = ไม่จำกัด) |
| `TARGET_ITEM` | `None` | สนใจกฎที่ "ทำนาย" item นี้ เช่น "pep=YES" / "whole milk" · None = ทุกกฎ |
| `SORT_BY` | `"lift"` | "lift" \| "confidence" \| "support" |
| `TOP_N` | `10` |  |
| `RULE_TO_EXPLAIN` | `None` | (["root vegetables"], ["other vegetables"]) = คำนวณมือกฎนี้ · None = ใช้กฎอันดับ 1 |
| `SEED` | `42` |  |
| `MISSING_MARKERS, SHEET, CSV_SEP` | `["?", "", " ", "NA"], 0, ","` |  |

### § ต่าง ๆ และบรรทัด ✏️ ที่แก้ได้

| cell # | § | ✏️ แก้ในเซลล์ (ถ้าโจทย์ต้องการ) |
|---|---|---|
| 3 | §0 เครื่องมือ association (mlxtend ถ้ามี · ถ้าไม่มีใช้ Apriori ที่เขียนเองด้านล่าง — ผลเหมือนกัน) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 5 | §1 โหลด + แปลงเป็นตาราง transaction (True/False) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 8 | §2 สำรวจ: จำนวน item ต่อตะกร้า + item ที่พบบ่อย (support ของ 1-itemset) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 10 | §3 Frequent itemsets (Apriori / FP-Growth, min support) | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 13 | §4 สร้างกฎ (min confidence) → เรียงตาม lift ⭐ | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 17 | §5 คำนวณกฎด้วยมือ (นับจากตาราง) — ตรวจสูตร / ตอบโจทย์ "แสดงวิธีคำนวณ" | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |
| 19 | §6 ผลของการเปลี่ยน min support / min confidence | cell 20: `SUP_GRID  = [MIN_SUPPORT / 2, MIN_SUPPORT, MIN_SUPPORT * 2, MIN_SUPPOR` — ค่า min support ที่ลอง<br>cell 20: `CONF_GRID = [0.2, 0.3, 0.5, 0.7, 0.9]` — ค่า min confidence ที่ลอง |
| 21 | §7 Apriori ทีละขั้นบนข้อมูลเล็ก (ตอบโจทย์คำนวณมือ: C1 → L1 → C2 → L2 → …) | cell 22: `SMALL_TRANSACTIONS = [` — ตัวอย่างในตำรา (Tan et al.) — แทนด้วยข้อมูลโจทย์<br>cell 22: `SMALL_MINSUP  = 3` — min support count (≥ 1 = จำนวนครั้ง · < 1 = สัดส่วน)<br>cell 22: `SMALL_MINCONF = 0.6` |
| 23 | §8 กราฟ support × confidence (สี = lift) + บันทึกกฎ | — (ไม่ต้องแก้ ใช้ค่าจาก CONFIG) |

