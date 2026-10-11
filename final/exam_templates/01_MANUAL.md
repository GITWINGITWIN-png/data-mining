# 📘 MANUAL: วิธีใช้ Template สอบ Lab (T01–T11)

> หาไฟล์จากคำในโจทย์: [00_INDEX.md](00_INDEX.md) · ทุกจุด ✏️ ของทุกไฟล์ (เลข cell): [02_CELL_MAP.md](02_CELL_MAP.md)

---

## ส่วนที่ 1 · เตรียมก่อนสอบ (คืนก่อนสอบ ทำครั้งเดียว)

1. **ดึงไฟล์ล่าสุด** ลงเครื่อง (`git pull`) ให้มีโฟลเดอร์ `final/exam_templates/`
2. **ตรวจ package** ใน kernel ที่จะใช้ (Python (dm-exam)) เปิด Terminal แล้วรัน:
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn imbalanced-learn mlxtend scipy openpyxl xlrd
   ```
   | package | ใช้ใน | ถ้าไม่มี |
   |---|---|---|
   | scikit-learn ≥ 1.2 | ทุกไฟล์ | `OneHotEncoder(sparse_output=…)` error → `pip install -U scikit-learn` |
   | imbalanced-learn | T04, T09 (`USE_SMOTE=True`) | `ModuleNotFoundError: imblearn` |
   | mlxtend | T11 | **ไม่ต้องมีก็ได้**: T11 มี Apriori ที่เขียนเองสำรองไว้ ผลเหมือนกัน |
   | xlrd / openpyxl | อ่าน `.xls` / `.xlsx` | `ImportError: Missing optional dependency 'xlrd'` |
   | scipy | T10 §7 (dendrogram) | มากับ scikit-learn อยู่แล้ว |
3. **เปิดทุกไฟล์ T01–T11 แล้วกด Run All หนึ่งรอบ** ต้องไม่มี error สีแดง (ข้อมูลตัวอย่างใส่ไว้แล้ว)
   ไฟล์ที่ช้าสุดคือ T08 (≈ 1–3 นาที) กับ T09 (≈ 1 นาที) เพราะมี GridSearch
4. อ่าน [00_INDEX.md](00_INDEX.md) ให้คุ้นว่าเรื่องไหนอยู่ไฟล์ไหน

---

## ส่วนที่ 2 · ขั้นตอนวันสอบ (ทุกไฟล์เหมือนกัน)

| ขั้น | ทำอะไร | หมายเหตุ |
|---|---|---|
| **1** | อ่านโจทย์ → เปิด [00_INDEX.md](00_INDEX.md) หาว่าใช้ไฟล์ไหน | โจทย์หลายส่วน → ใช้หลายไฟล์ (ดู INDEX ข้อ 5) |
| **2** | **Copy** ไฟล์ `Txx_….ipynb` ไปไว้ใน **โฟลเดอร์เดียวกับไฟล์ข้อมูลของโจทย์** แล้วเปลี่ยนชื่อ เช่น `6710503739_Q1.ipynb` | อย่าแก้ไฟล์ต้นฉบับ |
| **3** | แก้ cell **⚙️ CONFIG** (cell ที่ 2 จากบน) · อย่างน้อย `DATA_PATH`, `TARGET`, `POS_LABEL`, `ID_COL` | ไฟล์อยู่โฟลเดอร์เดียวกัน → `DATA_PATH = "data.csv"` |
| **4** | **Run All** | ถ้า error ให้ดู [ส่วนที่ 6](#ส่วนที่-6--error-ที่เจอบ่อย--วิธีแก้) |
| **5** | ดูผล **§1** (ตาราง `check()`) ว่าชื่อคอลัมน์/ชนิด/ค่าว่าง/สัดส่วน target ถูก → ถ้าผิดกลับไปแก้ CONFIG แล้ว Run All ใหม่ | ชื่อคอลัมน์ต้องตรงตัวพิมพ์เล็ก/ใหญ่ |
| **6** | ไปที่ § ที่โจทย์ถาม → แก้บรรทัดที่มี **`# ✏️`** (ถ้าโจทย์กำหนดค่า เช่น k, depth, threshold) → รันเฉพาะ cell นั้น (`Shift+Enter`) | รายการ ✏️ ทุกไฟล์: [02_CELL_MAP.md](02_CELL_MAP.md) |
| **7** | Copy ประโยค **`✍️ …`** ที่โปรแกรมพิมพ์ออกมา → วางใน cell **✍️ คำตอบ** ใต้ § นั้น แล้วเติม `…` ให้ครบ | ตอบให้ครบ: *ทำอะไร → ตั้งค่าอะไร → ได้ผลเท่าไร → แปลว่าอะไร* |
| **8** | ลบ § ที่โจทย์ไม่ได้ถาม (ลบทั้ง markdown + code ของ § นั้น) | **ห้ามลบ** cell CONFIG และ cell 🔧 helpers |
| **9** | เมนู **Restart Kernel and Run All** อีกครั้ง → ไม่มี error → Save → ส่ง | ไฟล์ส่งต้องรันได้บนเครื่องผู้ตรวจ (helpers อยู่ในไฟล์แล้ว) |

### รูปแบบ path ใน `DATA_PATH`
```python
DATA_PATH = "bank.csv"                          # ไฟล์อยู่โฟลเดอร์เดียวกับ notebook (แนะนำ)
DATA_PATH = "data/bank.csv"                     # อยู่ในโฟลเดอร์ย่อย
DATA_PATH = r"C:\Users\me\Desktop\exam\bank.csv" # Windows path เต็ม: ต้องมี r ข้างหน้า
DATA_PATH = "/Users/me/Desktop/exam/bank.csv"    # macOS path เต็ม
DATA_PATH = "sales.xlsx"; SHEET = "Sheet2"        # Excel หลาย sheet
```

---

## ส่วนที่ 3 · โครงสร้างทุกไฟล์ + สัญลักษณ์

```
cell 0  📄 หัวเรื่อง      : ใช้เมื่อโจทย์ถามอะไร + ขั้นตอนย่อของไฟล์นี้
cell 1  ⚙️ CONFIG         : ← แก้ที่นี่ก่อนเสมอ (path, ชื่อคอลัมน์, ค่าพารามิเตอร์ที่โจทย์กำหนด)
cell 2  🔧 IMPORTS+HELPERS: ไม่ต้องแก้ · import ครบ + ฟังก์ชันช่วย (load_data, check, evaluate …)
cell 3… §1, §2, …         : แต่ละ § = markdown อธิบาย → code → ✍️ คำตอบ
```

| สัญลักษณ์ | ความหมาย |
|---|---|
| `⚙️ CONFIG` | cell เดียวที่ **ต้อง** แก้ทุกครั้ง |
| `# ✏️` | บรรทัดที่ **แก้ได้ถ้าโจทย์กำหนด** (ไม่แก้ = ใช้ค่าตัวอย่าง/ค่าอัตโนมัติ) |
| `✍️` (ในผลลัพธ์) | ประโยคตีความสำเร็จรูป copy ไปตอบได้ |
| `**✍️ คำตอบ §n:**` (markdown) | แม่แบบคำตอบ: เติม `…` ด้วยตัวเลขจากผลลัพธ์ |
| `⭐` | § ที่ออกสอบบ่อย / เป็นหัวใจของไฟล์ |
| `⚠️` (ในผลลัพธ์) | คำเตือน เช่น คอลัมน์ไม่มี, overfit, ข้อมูลขาด → อ่านแล้วแก้ |

> 🛟 **Run All ไม่หยุดกลางทาง:** ถ้าบรรทัด ✏️ อ้างคอลัมน์ของข้อมูลตัวอย่างที่ไม่มีในข้อมูลโจทย์ (เช่น T01 `"total_bill"`)
> โปรแกรมจะเลือกคอลัมน์ชนิดเดียวกันให้ชั่วคราวและพิมพ์ `⚠️ ไม่มีคอลัมน์ … → ใช้ … แทนชั่วคราว` → **ต้องกลับไปแก้ ✏️ ให้ตรงโจทย์**

---

## ส่วนที่ 4 · ตัวแปร CONFIG ที่ใช้ร่วมกัน

| ตัวแปร | ใส่อะไร | ตัวอย่าง |
|---|---|---|
| `DATA_PATH` | path ไฟล์ข้อมูล (.csv / .xlsx / .xls) | `"bank.csv"` |
| `TARGET` | ชื่อคอลัมน์คำตอบ (label) · ไม่มีใส่ `None` | `"Churn"` |
| `POS_LABEL` | คลาสที่ "สนใจ" = 1 (positive) สำหรับ precision/recall/F1 · ต้องพิมพ์ให้ตรงค่าในข้อมูล (ตัวพิมพ์/ชนิด) | `"Yes"`, `1`, `">50K"`, `"malignant"` |
| `ID_COL` | คอลัมน์รหัส (ไม่ใช้เป็น feature) | `"customerID"`, `None` |
| `DROP_COLS` | คอลัมน์ที่ต้องตัด: รั่วคำตอบ (leak), รู้หลังเกิดผล, ไม่เกี่ยว | `["TotalCharges"]` |
| `FEATURES` | ถ้าโจทย์บอก "ใช้เฉพาะตัวแปร …" · `None` = ใช้ทุกคอลัมน์ที่เหลือ | `["age", "income"]` |
| `EVAL_MODE` | `"cv"` = k-fold · `"holdout"` = แบ่ง train/test | ตามโจทย์ |
| `N_FOLDS` / `TEST_SIZE` | จำนวน fold / สัดส่วน test | `10` / `0.3` |
| `SEED` | random seed ที่โจทย์กำหนด (ผลจะตรงกับเฉลย) | `1992` |
| `SCALE` | `"standard"` (z-score) · `"minmax"` (0–1) · `None` | KNN/Logistic/K-Means ควร scale · Tree ไม่ต้อง |
| `MISSING_MARKERS` | ค่าที่แปลว่า "ว่าง" ในไฟล์ | `["?", "", " ", "NA", "-"]` |
| `ZERO_AS_MISSING` | คอลัมน์ที่ค่า 0 เป็นไปไม่ได้ (เช่น BMI = 0) → ถือเป็นค่าว่าง (T02, T07) | `["bmi", "glucose"]` |
| `SHEET` / `CSV_SEP` | sheet ของ Excel / ตัวคั่น csv (`;` ระบบหาให้อัตโนมัติ) | `0` / `","` |
| `NEW_DATA` / `NEW_POINT` | ข้อมูลใหม่ที่จะทำนาย: dict 1 แถว · list ของ dict · path .csv · `None` = ข้าม | `{"age": 40, "income": 50000}` |
| `PRIMARY_METRIC` | metric ที่ใช้เลือกโมเดล (T04, T09) | `"f1"` (ไม่สมดุล) · `"recall"` (พลาดคนป่วยแพง) · `"accuracy"` (สมดุล) |

**load_data ทำให้อัตโนมัติ:** ตัดช่องว่างชื่อคอลัมน์/ค่า · แปลง `?`/ช่องว่างเป็น NaN · คอลัมน์ตัวเลขที่ถูกอ่านเป็นข้อความ (เพราะมี `?`) แปลงกลับเป็นตัวเลข ·
อ่านไฟล์ภาษาไทยจาก Excel (cp874) และไฟล์มี BOM · ไฟล์คั่นด้วย `;`

---

## ส่วนที่ 5 · คู่มือรายไฟล์ (ถ้าโจทย์แบบนี้ → แก้ตรงไหน)

### T01 · Data Handling & Visualization
**ใช้เมื่อ:** import/ตรวจ · select/filter · set role · concat · join · group by · pivot · สร้างคอลัมน์ · กราฟ · correlation
**CONFIG:** `DATA_PATH`, `ID_COL`, `TARGET` · มีไฟล์ที่ 2 ให้ต่อแถว → `DATA_PATH_2` · มีไฟล์ lookup ให้ join → `LOOKUP_PATH`, `JOIN_KEY`, `JOIN_HOW` (ไม่มีใส่ `None`)

| โจทย์บอกว่า | แก้ |
|---|---|
| "เลือกเฉพาะคอลัมน์ … / ตัด …" | §2 `KEEP_COLS` / `DROP_THESE` |
| "เลือกเฉพาะตัวเลข" | §2 `BY_TYPE = "number"` |
| "ตั้ง … เป็น id / label" | CONFIG `ID_COL`, `TARGET` (§2 แสดงผล set role) |
| "กรองเฉพาะ age > 30 และ gender = Male" | §3 `FILTER = "age > 30 and gender == 'Male'"` (ชื่อคอลัมน์มีขีด/ช่องว่าง → ใส่ backtick: `` "`native-country` == 'Thailand'" ``) |
| "ตัดแถวที่ … ว่าง" | §3 `DROP_MISSING_ROWS_IN = ["…"]` |
| "ต่อข้อมูลสองช่วงเวลา (append)" | CONFIG `DATA_PATH_2` → §4 |
| "join ตารางลูกค้ากับตารางคำสั่งซื้อ" | CONFIG `LOOKUP_PATH`, `JOIN_KEY` (ชื่อไม่ตรงกัน → `("cust_id", "id")`), `JOIN_HOW` → §5 |
| "ยอดรวม/ค่าเฉลี่ยตามกลุ่ม" | §6 `GROUP_BY`, `AGG = {"คอลัมน์": ["sum", "mean"]}` |
| "pivot table แถว × คอลัมน์" | §7 `PIV_INDEX, PIV_COLUMNS, PIV_VALUES, PIV_FUNC` |
| "สัดส่วนคนที่ income >50K ตาม education × gender" | §7 `PIV_INDEX="education"`, `PIV_COLUMNS="gender"`, `RATE_OF=("income", ">50K")` |
| "สร้างคอลัมน์ใหม่" | §8 แก้สูตรตัวอย่าง (`df["ใหม่"] = …`) |
| "วาดกราฟการกระจาย / เปรียบเทียบกลุ่ม / scatter" | §9 `NUM_COL`, `CAT_COL`, `X_COL`, `Y_COL`, `HUE` · stacked bar: `STACK_GROUP`, `STACK_CLASS` |
| "ตัวแปรไหนสัมพันธ์กันมาก" | §10 (อัตโนมัติ) |
| "บันทึกผลเป็นไฟล์" | §11 `OUT_PATH` |

⚠️ §4 และ §5 **เปลี่ยน `df` หลัก** (ต่อแถว/เพิ่มคอลัมน์) ไม่ต้องการ → comment บรรทัด `df = …` ที่มี ✏️

### T02 · Data Preprocessing
**ใช้เมื่อ:** missing · outlier · encoding · scaling · discretization · sampling · split ไม่ leak · feature selection
**CONFIG:** `DATA_PATH`, `TARGET`, `POS_LABEL`, `ID_COL`, `DROP_COLS`, `ZERO_AS_MISSING`, `SCALE`

| โจทย์บอกว่า | แก้ |
|---|---|
| "จัดการค่าว่างด้วย median / mean / mode / ลบแถว / ลบคอลัมน์ / ค่าคงที่ / ตามกลุ่ม" | §2 `MISS_METHOD` (+ `DROP_COL_THRESHOLD`, `CONSTANT`, `GROUP_COL`) |
| "จัดการ outlier" | §3 `OUT_METHOD = "clip"` หรือ `"remove"` (`None` = แค่นับ) |
| "encode ตัวแปรลำดับ (low<mid<high)" | §4 `ORDINAL_MAP = {"edu": ["low", "mid", "high"]}` |
| "แปลง yes/no เป็น 1/0" | §4 `BINARY_MAP = {"smoker": {"yes": 1, "no": 0}}` |
| "one-hot แบบตัด dummy ตัวแรก" | §4 `DROP_FIRST = True` |
| "standardize vs normalize" | §5 (แสดงทั้ง 2 แบบอัตโนมัติ) |
| "แบ่ง … เป็น 3 ช่วง" | §6 `DISC_COL`, `N_BINS`, `LABELS`, `USER_BINS` (ขอบกำหนดเอง) |
| "สุ่ม 30% / stratified sample" | §7 `SAMPLE_FRAC` |
| "แบ่ง train/test ไม่ให้ leak + เทียบก่อน/หลัง scale" | §8 ⭐ (`MODEL_FOR_COMPARE` เปลี่ยนโมเดลได้) |
| "เลือก feature k ตัว" | §9 `K_BEST` |
| "ตัด feature แล้วใช้ข้อมูลที่ตัดต่อ / ส่งไฟล์" | §9b `FS_DROP` (ตัดเอง) · `FS_USE_KBEST` (เก็บ top-`K_BEST`) → ได้ `Xtr_fs`/`Xte_fs` + `t02_*_selected.csv` |

⚠️ §1–§7 = **สาธิตบนทั้งตาราง** (ตอบคำถาม "ทำอย่างไร/ผลเป็นอย่างไร") · ตอนสร้างโมเดลจริงใช้ §8 (fit บน train เท่านั้น)

### T03 · PCA
**CONFIG:** `DATA_PATH`, `TARGET` (ไว้ระบายสีกราฟ · ไม่มีใส่ `None`), `ID_COL`, `FEATURES`, `STANDARDIZE=True`, `VAR_TARGET` (เช่น 0.90), `N_LOADINGS`, `NEW_POINT`

| โจทย์บอกว่า | ดู/แก้ |
|---|---|
| "ต้องใช้กี่ PC ถึงอธิบาย 90%" | CONFIG `VAR_TARGET = 0.90` → §2 |
| "PC1 มาจากตัวแปรอะไร (loadings)" | §3 |
| "plot 2 มิติ ระบายสีตาม class" | §4 |
| "PCA ก่อนโมเดลดีขึ้นไหม" | §5 (`MODEL` เปลี่ยนโมเดลได้) |
| "แปลงข้อมูลใหม่เป็น PC" | CONFIG `NEW_POINT` → §6 |

### T04 · Imbalanced (Under / Over / SMOTE)
**CONFIG:** `DATA_PATH`, `TARGET`, `POS_LABEL` (**คลาสส่วนน้อย**), `MODEL_NAME` (`"LogReg"`/`"KNN"`/`"Tree"`/`"RF"`), `PRIMARY_METRIC`, `SMOTE_K`, `EVAL_MODE`

| โจทย์บอกว่า | ดู/แก้ |
|---|---|
| "ทำไม accuracy หลอก" | §2 (majority baseline) |
| "ทำ SMOTE / undersampling / oversampling แล้วเทียบ" | §4 ⭐ |
| "จำนวนคลาสก่อน/หลัง resample" | §3 |
| "confusion matrix ก่อน/หลัง SMOTE" | §5 |
| "ทำไมห้าม SMOTE ก่อน split" | §6 (แสดงผลที่ดีเกินจริง) |
| "ลด threshold แทน resample" | §7 `THRESHOLDS` |
| "ควรใช้ metric อะไร" | §8 |

### T05 · KNN
**CONFIG:** `DATA_PATH`, `TARGET`, `POS_LABEL`, `NEW_POINT`, `K`, `METRIC` (`"euclidean"`/`"manhattan"`), `WEIGHTS`, `SCALE`, `K_MAX`, `EVAL_MODE`

| โจทย์บอกว่า | ดู/แก้ |
|---|---|
| "คำนวณระยะจากจุดใหม่ถึงทุกจุด / หาเพื่อนบ้าน k ตัว / vote" | CONFIG `NEW_POINT`, `K`, `METRIC` → §2 (ถ้าโจทย์ไม่ให้ scale → `SCALE = None`) |
| "train/test" | §3 |
| "เทียบก่อน/หลัง normalize" | §4 |
| "หา k ที่ดีที่สุด" | §5 (`K_MAX`) |
| "ทำนายข้อมูลใหม่" | §6 · โจทย์บังคับ k → แก้ ✏️ `final = make_pipe(knn_model(K), X).fit(X, y)` |
| "KNN ทำนายตัวเลข (regression)" | §7 `REG_DATA_PATH`, `REG_TARGET`, `REG_K`, `REG_NEW` |

### T06 · Linear Regression
**CONFIG:** `DATA_PATH`, `TARGET` (ตัวเลข), `FEATURES`, `SIMPLE_X` (ตัวแปรเดียวของ simple LR), `DROP_FIRST`, `NEW_DATA`, `EVAL_MODE`

| โจทย์บอกว่า | ดู |
|---|---|
| "สมการ y = b0 + b1x" | §3 |
| "สมการเต็ม / ตีความ coefficient" | §4 |
| "MAE, MSE, RMSE, R² + เทียบ baseline (ค่าเฉลี่ย)" | §5 |
| "ลองโมเดลอื่น / optimize" | §6 |
| "ทำนายข้อมูลใหม่" | §7 |

### T07 · Logistic Regression
**CONFIG:** `DATA_PATH`, `TARGET`, `POS_LABEL`, `FEATURES`, `ZERO_AS_MISSING` (**ข้อมูลอื่นใส่ `[]`**), `THRESHOLD`, `THRESHOLDS`, `NEW_DATA`

| โจทย์บอกว่า | ดู/แก้ |
|---|---|
| "coefficient / odds ratio / ตัวแปรไหนเพิ่มโอกาส" | §3 |
| "คำนวณ probability ด้วยสมการ" | §4 |
| "เปลี่ยน threshold เป็น 0.3 แล้วเทียบ" | CONFIG `THRESHOLD = 0.3` → §5 (`SOURCE = "holdout"` หรือ `"cv"`) |
| "ROC / AUC" | §5 |
| "tune C" | §6 |
| "ทำนายข้อมูลใหม่ (probability)" | §7 |

### T08 · Decision Tree & Random Forest
**CONFIG:** `DATA_PATH`, `TARGET`, `POS_LABEL`, `CRITERION`, `MAX_DEPTH`, `MIN_LEAF`, `N_TREES`, `NEW_DATA`, `EVAL_MODE`

| โจทย์บอกว่า | ดู/แก้ |
|---|---|
| "คำนวณ entropy / gini / gain เลือก root" | §0: `IMP_PATH`, `IMP_TARGET`, `IMP_DROP` (ข้อมูลเล็กแยกต่างหาก) |
| "สร้างต้นไม้ depth = 3 / วาด / เขียนกฎ" | CONFIG `MAX_DEPTH`, `CRITERION` → §2 |
| "overfitting" | §3 |
| "tune tree" | §4 |
| "random forest / จำนวนต้น" | §5 |
| "เทียบ baseline vs DT vs RF ก่อน/หลัง optimize" | §6 ⭐ |
| "ทำนาย + อธิบายเส้นทาง" | §7 |

> RapidMiner Decision Tree ใช้ **gain_ratio** + pruning เป็น default · sklearn ใช้ **gini** ไม่ prune → ผลต่างกันได้

### T09 · Classification Workflow (ไฟล์หลักสำหรับโจทย์ classification)
**CONFIG:** `DATA_PATH`, `TARGET`, `POS_LABEL`, `ID_COL`, `DROP_COLS`, `EVAL_MODE`, `PRIMARY_METRIC`, `USE_SMOTE`, `NEW_DATA`, `N_FOLDS`, `SEED`

| โจทย์บอกว่า | แก้ |
|---|---|
| "ใช้เฉพาะ KNN และ Decision Tree" | §3 ลบรายการที่ไม่ใช้ออกจาก `MODELS` และ `GRIDS` |
| "KNN k = 7" / "tree depth = 4" | §3 ค่าใน `MODELS` เช่น `KNeighborsClassifier(n_neighbors=7)` และแก้ข้อความ settings |
| "optimize k ช่วง 1–20" | §3 `GRIDS["KNN"] = {"model__n_neighbors": list(range(1, 21))}` |
| "hold-out 70/30" | CONFIG `EVAL_MODE = "holdout"`, `TEST_SIZE = 0.3` |
| "10-fold CV" | CONFIG `EVAL_MODE = "cv"`, `N_FOLDS = 10` |
| "ข้อมูลไม่สมดุล" | CONFIG `USE_SMOTE = True`, `PRIMARY_METRIC = "f1"` หรือ `"recall"` |
| "เลือกโมเดลด้วย accuracy" | CONFIG `PRIMARY_METRIC = "accuracy"` |

ผลที่ได้: §4 baseline vs default ⭐ · §5 GridSearch · §6 ก่อน vs หลัง ⭐ · §7 โมเดลสุดท้าย + confusion matrix + โครงคำตอบ 4 ขั้น · §8 ทำนาย

### T10 · Clustering (K-Means)
**CONFIG:** `DATA_PATH`, `ID_COL` (ชื่อแถว), `LABEL_COL` (class จริงถ้ามี ใช้เทียบเท่านั้น), `DROP_COLS`, `FEATURES`, `SCALE`, `K_RANGE`, `K_FINAL`, `N_INIT`, `MAX_ITER`, `NEW_POINT`, `LINKAGE`

| โจทย์บอกว่า | ดู/แก้ |
|---|---|
| "เตรียมข้อมูล (ตัด id, normalize)" | §1 |
| "เลือกจำนวน cluster (elbow / silhouette)" | CONFIG `K_RANGE` → §2 · ให้ระบบเลือก → `K_FINAL = None` |
| "k = 3 ตามโจทย์" | CONFIG `K_FINAL = 3` |
| "centroid / อธิบายแต่ละกลุ่ม / ตั้งชื่อ" | §3 |
| "จุดใหม่อยู่กลุ่มไหน" | CONFIG `NEW_POINT` (ชื่อ key ต้องตรงคอลัมน์ · ไม่มี → `None`) → §4 |
| "cohesion / separation" | §5 |
| "plot cluster" | §6 (PCA 2D) · คู่แกนเดิม: แก้ `FX, FY` |
| "hierarchical / dendrogram" | §7 `LINKAGE` |
| "เทียบกับ class จริง" | CONFIG `LABEL_COL` → §8 |
| "K-Means ด้วยมือ seed A1, A4, A7" | §9 `HAND_POINTS`, `HAND_INIT` |

### T11 · Association Rules
**CONFIG:** `DATA_PATH`, `FORMAT`, `ID_COL`, `DROP_COLS`, `BINS`, `MIN_SUPPORT`, `MIN_CONFIDENCE`, `ALGO`, `TARGET_ITEM`, `SORT_BY`

| ข้อมูลหน้าตาแบบนี้ | ตั้ง |
|---|---|
| `milk,bread,eggs` (1 บรรทัด = 1 ตะกร้า) | `FORMAT = "basket"` (หรือ `"auto"`) |
| ตาราง 0/1 หรือ Y/N ต่อสินค้า + คอลัมน์รหัส | `FORMAT = "onehot"`, `ID_COL = "Trans."` |
| 2 คอลัมน์ `tid, item` | `FORMAT = "long"`, `LONG_TID = "tid"`, `LONG_ITEM = "item"` |
| ตารางลูกค้า (age, income, married, pep…) | `FORMAT = "table"`, `ID_COL = "id"`, `BINS = {"age": 3, "income": 3, "children": [-1, 0, 2, 10]}`, `BIN_LABELS = ["LOW", "MID", "HIGH"]` |

| โจทย์บอกว่า | ดู/แก้ |
|---|---|
| "min support 20%, min confidence 70%" | `MIN_SUPPORT = 0.2`, `MIN_CONFIDENCE = 0.7` |
| "min support = 3 ครั้ง (จาก N ตะกร้า)" | `MIN_SUPPORT = 3 / N` |
| "ใช้ FP-Growth (เหมือน RapidMiner)" | `ALGO = "fpgrowth"` |
| "สินค้าขายดี" | §2 |
| "frequent itemsets" | §3 |
| "กฎ + ตีความ support / confidence / lift" | §4 ⭐ |
| "กฎที่ทำนายว่าลูกค้าจะซื้อ pep" | `TARGET_ITEM = "pep=YES"` → §4 cell 2 |
| "แสดงวิธีคำนวณกฎ …" | `RULE_TO_EXPLAIN = (["A"], ["B"])` → §5 |
| "ถ้าเพิ่ม min support จะเกิดอะไร" | §6 (`SUP_GRID`, `CONF_GRID`) |
| "Apriori ทีละขั้นจากตะกร้า 5 ใบ" | §7 `SMALL_TRANSACTIONS`, `SMALL_MINSUP`, `SMALL_MINCONF` |

---

## ส่วนที่ 6 · Error ที่เจอบ่อย + วิธีแก้

| Error | สาเหตุ | แก้ |
|---|---|---|
| `FileNotFoundError` | path ผิด | วาง notebook กับไฟล์ข้อมูลโฟลเดอร์เดียวกัน · Windows ใช้ `r"C:\…"` · ดูชื่อไฟล์ (นามสกุล .csv/.xlsx) |
| `KeyError: 'xxx'` | ชื่อคอลัมน์ไม่ตรง (ตัวพิมพ์/ช่องว่าง) | ดูชื่อจริงในตาราง §1 · แก้ CONFIG / ✏️ |
| `ValueError: POS_LABEL=… ไม่อยู่ใน [...]` | ค่า positive ไม่ตรง | copy ค่าจากข้อความ error เช่น `"Yes"` หรือ `1` (ตัวเลขไม่ต้องมี "") |
| `ModuleNotFoundError: imblearn / mlxtend` | ยังไม่ติดตั้ง | `pip install imbalanced-learn mlxtend` แล้ว **Restart kernel** |
| `TypeError: … sparse_output` | scikit-learn เก่ากว่า 1.2 | `pip install -U scikit-learn` |
| `Missing optional dependency 'xlrd'` | อ่าน .xls | `pip install xlrd` |
| `ValueError: could not convert string to float` | มีคอลัมน์ข้อความที่ไม่ได้ผ่าน pipeline | ใช้ `make_pipe(...)` ของ template (one-hot ให้อัตโนมัติ) · หรือใส่คอลัมน์นั้นใน `DROP_COLS` |
| `Input contains NaN` (ในโค้ดที่เขียนเอง) | มีค่าว่าง | ใช้ `make_pipe` (มี imputer) หรือ `df.dropna()` |
| `n_splits=5 cannot be greater than the number of members in each class` | คลาสน้อยเกิน | ลด `N_FOLDS` (เช่น 3) |
| `Expected n_neighbors <= n_samples` | k มากกว่าจำนวนแถว | ลด `K` / `K_MAX` |
| ⚠️ `ไม่มีคอลัมน์ … → ใช้ … แทนชั่วคราว` | ✏️ ยังเป็นชื่อคอลัมน์ข้อมูลตัวอย่าง | แก้บรรทัด ✏️ ใน § นั้น |
| รันนานมาก | GridSearch บนข้อมูลใหญ่ | ลดค่าใน grid (`GRIDS`, `K_MAX`) หรือ `N_FOLDS = 5` |
| กราฟไม่ขึ้น | — | รัน cell นั้นใหม่ · ตรวจว่า `plt.show()` อยู่ท้าย |

---

## ส่วนที่ 7 · ฟังก์ชันช่วย (ใช้เขียน cell เพิ่มเองได้ทุกไฟล์)

| ฟังก์ชัน | ทำอะไร | ตัวอย่าง |
|---|---|---|
| `load_data(path)` | อ่านไฟล์ + ทำความสะอาด | `df2 = load_data("other.csv")` |
| `check(df, target)` | ตาราง dtype/missing/unique + สัดส่วน target | `check(df, "Churn")` |
| `make_xy(df)` | แยก X / y (ตัด ID/DROP_COLS, y = 0/1 ตาม POS_LABEL) | `X, y = make_xy(df)` |
| `make_pipe(model, X, scale=…)` | Pipeline: impute + scale + one-hot + model (ไม่ leak) | `make_pipe(KNeighborsClassifier(7), X)` |
| `evaluate(name, model, X, y)` | CV → accuracy/precision/recall/F1 (1 แถว) | `rows.append(evaluate("KNN7", p, X, y))` |
| `evaluate_holdout(name, model, Xtr, ytr, Xte, yte)` | hold-out → metrics | |
| `evaluate_reg(name, model, X, y)` | CV regression → MAE/MSE/RMSE/R² | |
| `results_table(rows, sort_by=…)` | รวมแถวเป็นตาราง | `results_table(rows, "f1")` |
| `say_compare(table, "f1", "Majority baseline")` | พิมพ์ประโยค ✍️ เปรียบเทียบ | |
| `show_cm(y_true, y_pred)` | confusion matrix + TN/FP/FN/TP + report | |
| `top_k(grid)` | ตารางผล GridSearchCV เรียงจากดีสุด | |
| `new_data(dict/list/path)` + `align_new(df_new, X)` | เตรียมข้อมูลใหม่ให้คอลัมน์ตรงกับตอน train | |

ตัวอย่างเพิ่มโมเดลเองใน cell ใหม่ (ไฟล์ไหนก็ได้ที่มี `X, y`):
```python
rows = [evaluate("Majority baseline", DummyClassifier(strategy="most_frequent"), X, y),
        evaluate("KNN k=7", make_pipe(KNeighborsClassifier(n_neighbors=7), X), X, y, settings="k=7, z-score"),
        evaluate("Tree d=4", make_pipe(DecisionTreeClassifier(max_depth=4, random_state=SEED), X, scale=None), X, y)]
t = results_table(rows, sort_by="f1")
say_compare(t, "f1", "Majority baseline")
```

---

## ส่วนที่ 8 · โครงคำตอบเชิงตีความ (ใช้ได้ทุกข้อ)

1. **Process:** ทำอะไรตามลำดับ (อ่านข้อมูล → ตัด … → preprocess … → แบ่งข้อมูล … → โมเดล … → ประเมิน …)
2. **Settings:** ค่าที่ตั้ง (seed, k, depth, folds, threshold, min support …) และ **เหตุผล**
3. **Results:** ตัวเลขจากตาราง (อ้าง metric + ค่า)
4. **Interpretation:** แปลว่าอะไร · ดีกว่า baseline เท่าไร · ทำไมเลือกโมเดลนี้ · ข้อจำกัด / ข้อเสนอแนะ

> คำตอบที่ดี = มีตัวเลข + มีเหตุผล + เชื่อมกับโจทย์ (ธุรกิจ/ผลเสียของ FN vs FP)
