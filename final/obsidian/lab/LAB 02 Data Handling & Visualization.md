---
title: LAB 02 · Data Handling & Visualization
exam: Lab — จ. 12 ต.ค. 2569 09:00–12:00
guideline: "Lab › Data Handling and Visualization (ทั้ง 4 ข้อ)"
tags: [final, lab, pandas, rapidminer, join, pivot, visualization]
---

# LAB 02 · Data Handling & Visualization
### นำเข้า ตรวจ คัดเลือก รวมตาราง และวาดกราฟ — ทั้ง Python และ RapidMiner

> [!abstract] guideline Lab ข้อ "Data Handling and Visualization"
> 1. **Import และตรวจสอบข้อมูล** → [[#2.1 Import & Inspect ⭐⭐]]
> 2. **ใช้ pandas, NumPy, matplotlib และ scikit-learn** → ทั้งบท
> 3. **สร้าง basic charts และตีความผล** → [[#2.8 Basic Charts + การตีความ ⭐⭐⭐]]
> 4. **Select attributes, filter examples, set role, join, concatenate และ pivot** → [[#2.2 Select Attributes ⭐]] ถึง [[#2.7 Pivot / Aggregate ⭐⭐⭐]]
>
> ⚠️ **ข้อ 4 ใช้ชื่อ operator ของ RapidMiner ตรงตัว** (Select Attributes, Filter Examples, Set Role, Join, Append, Pivot) → มีโอกาสสูงว่าโจทย์ส่วนนี้จะสั่งให้ทำใน RapidMiner

**ลิงก์:** [[LAB 00 START HERE|หน้าหลัก Lab]] · ก่อนหน้า [[LAB 01 Setup & Exam-Day]] · ถัดไป [[LAB 03 Preprocessing Recipes]] · [[LAB 09 Cheat Sheet]]

> [!warning] 🕳️ Gap ของคุณในบทนี้ (จากการไล่งานเก่าทั้งหมด)
> - **ไม่เคยใช้ `pd.merge`, `pivot_table` และ `pd.concat` แบบต่อแถวเลย** (concat เคยใช้ครั้งเดียวแบบ `axis=1` ใน HW8 เพื่อโชว์ตาราง)
> - RapidMiner: เคยใช้ `Join` แค่แบบ **inner** (W5/W6 ETL) · **ไม่เคยใช้ `Append`, `Pivot`, role `id`**
> - **ไม่เคยวาดกราฟใน RapidMiner**
>
> → ฝึก Drill ท้ายบท **ทั้งสองเครื่องมือ** อย่างน้อยรอบละครั้ง

> [!tip] วิธีรันโค้ดในบทนี้
> โค้ดทุกบล็อก **รันทดสอบแล้ว** ด้วย env `final/.venv` (pandas 3.0 · sklearn 1.9) โดยเปิด notebook ที่โฟลเดอร์ `data mining/` (path ในโค้ดเป็น relative เช่น `W14/...`) — บล็อกต่อกันเหมือน cell ใน notebook เดียว

---

## 2.0 ตั้งต้น — import ที่ใช้ทั้งบท

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", 50)   # ให้ head() โชว์ครบทุกคอลัมน์
```

---

## 2.1 Import & Inspect ⭐⭐

### 🐍 Python

```python
churn = pd.read_csv("W14/customer_churn_69_1(in).csv")     # CSV
beauty = pd.read_excel("W10/BeautyCo_68.xls")              # Excel .xls ต้องมี xlrd · .xlsx ใช้ openpyxl
# ถ้าไฟล์ Excel มีหลายชีต: pd.ExcelFile(path).sheet_names แล้ว read_excel(path, sheet_name="ชื่อชีต")

print(churn.shape)          # (แถว, คอลัมน์) — เช็กว่าอ่านครบ
churn.info()                # ชนิดข้อมูล + จำนวนค่าไม่ว่างของแต่ละคอลัมน์
churn.head()
```

**ตรวจ 5 อย่างทุกครั้งที่ได้ข้อมูลใหม่** (นี่คือ "ตรวจสอบข้อมูล" ที่ guideline ต้องการ):

```python
# 1) สถิติสรุป — ตัวเลข และ categorical แยกกัน
churn.describe().T                         # count / mean / std / min / quartiles / max
churn.describe(exclude="number").T         # count / unique / top / freq

# 2) ค่าว่าง "จริง"
churn.isna().sum().sort_values(ascending=False).head()

# 3) ค่าว่าง "แฝง" (sentinel) — ช่องว่าง, "?", -1 ที่ไม่ใช่ค่าจริง
(churn == " ").sum().loc[lambda s: s > 0]   # TotalCharges มี " " 11 แถว → pandas เลยอ่านเป็นข้อความ!

# 4) ชนิดข้อมูลผิด — ตัวเลขที่ถูกอ่านเป็นข้อความ
churn["TotalCharges"] = pd.to_numeric(churn["TotalCharges"], errors="coerce")   # " " → NaN
print(churn["TotalCharges"].isna().sum())   # 11

# 5) แถวซ้ำ + การกระจายของ target
print(churn.duplicated().sum())
churn["Churn"].value_counts(normalize=True)   # No 0.735 / Yes 0.265 → imbalanced
```

> [!important] ⭐ ประโยคตีความ "ผลการตรวจข้อมูล" สำเร็จรูป
> *"ชุดข้อมูลมี **7,043 แถว 21 คอลัมน์** · `TotalCharges` ถูกอ่านเป็นข้อความเพราะมีช่องว่าง 11 แถว (ลูกค้าที่ tenure = 0) จึงแปลงเป็นตัวเลขและถือว่าเป็นค่าว่าง · target `Churn` มีสัดส่วน No 73.5% / Yes 26.5% → **ข้อมูลไม่สมดุล** ต้องระวังการใช้ accuracy"*

> [!warning] pandas 3 — ข้อความเป็น dtype `str` ไม่ใช่ `object` แล้ว
> โค้ดเก่า `df.select_dtypes(include="object")` ยังใช้ได้แต่มี warning ว่าจะเลิกรองรับ
> **ใช้ `df.select_dtypes(exclude="number")` แทน** — ได้คอลัมน์ categorical ครบทั้ง pandas 2 และ 3

### ⚙️ RapidMiner

| ทำอะไร | วิธี |
|---|---|
| นำเข้า | **Repository → Import Data** (wizard 5 ขั้น: เลือกไฟล์ → ดูตัวอย่าง → *Format your columns* ← **ตั้งชนิดและ role ได้ตรงนี้** → เลือกที่เก็บใน repository) แล้วลาก data จาก repository มาวาง = operator `Retrieve` · หรือใช้ operator **`Read CSV`** / **`Read Excel`** แล้วกด **Import Configuration Wizard** |
| ดูข้อมูล | กด ▶ Run → แท็บ **Results** → ExampleSet มี 3 มุมมอง: **Data** (ตาราง) · **Statistics** (min/max/average/deviation/**missing** ต่อคอลัมน์ + กราฟเล็ก) · **Visualizations** |
| ดูข้อมูลกลางทาง | คลิกขวา operator → **Breakpoint After** → รัน process จะหยุดให้ดูข้อมูล ณ จุดนั้น |
| แก้ชนิดคอลัมน์ | ตอน import (Format your columns → เปลี่ยน type) หรือ operator `Nominal to Numerical`, `Numerical to Polynominal`, `Parse Numbers` |

> [!tip] ดู "ชนิดข้อมูล" ใน RapidMiner ให้เป็น
> **polynominal** = ข้อความหลายค่า · **binominal** = ข้อความ 2 ค่าพอดี (เช่น Yes/No) · **integer/real** = ตัวเลข · **date_time**
> learner หลายตัว **ต้องการ label เป็น binominal/polynominal** ถ้า label เป็นตัวเลข 0/1 จะกลายเป็นงาน regression → ใช้ **`Numerical to Binominal`** ก่อน `Set Role`

---

## 2.2 Select Attributes ⭐

**เมื่อไหร่ใช้:** ตัดคอลัมน์ที่ไม่ควรเข้าโมเดล — **ID** (ไม่มีความหมาย, ทำให้ overfit), คอลัมน์ซ้ำซ้อน (เช่น `education` กับ `educational-num` บอกสิ่งเดียวกัน), คอลัมน์ที่ "รู้ผลล่วงหน้า" (leakage)

### 🐍 Python

```python
X_cols = churn.columns.drop(["customerID", "Churn"])       # ทุกคอลัมน์ยกเว้น ID และ target
subset = churn[["tenure", "MonthlyCharges", "Contract", "Churn"]]   # เลือกตามชื่อ
numeric_only = churn.select_dtypes(include="number")       # เลือกตามชนิด
no_id = churn.drop(columns=["customerID"])                  # ตัดออก
```

### ⚙️ RapidMiner — `Select Attributes`

| พารามิเตอร์ | ค่าที่ใช้บ่อย | หมายเหตุ |
|---|---|---|
| **attribute filter type** | `single` (ตัวเดียว) · `subset` (ติ๊กเลือกหลายตัว) · `regular expression` · `value type` (เช่นเอาเฉพาะ numeric) · `no missing values` | `subset` ใช้บ่อยที่สุด → กด **Select Attributes…** แล้วย้ายชื่อไปฝั่งขวา |
| **invert selection** | ✅ = "**ตัด**ตัวที่เลือกออก" | ใช้ตอนอยากตัดแค่ 1–2 คอลัมน์ |
| **include special attributes** | ปกติ ❌ | ถ้าไม่ติ๊ก label/id จะ **ไม่ถูกแตะ** (ปลอดภัย) |

> [!tip] ทางเลือกที่ดีกว่าการลบ ID ทิ้ง: **`Set Role` → id**
> RapidMiner **ไม่เอาคอลัมน์ role `id` ไปเป็น feature** แต่ยังเก็บไว้ในตาราง → หลัง `Apply Model` ยังรู้ว่าแถวไหนคือลูกค้าคนไหน

---

## 2.3 Filter Examples ⭐

**เมื่อไหร่ใช้:** เลือก "แถว" — ตัดแถวผิดปกติ (เช่น Experience < 0 ใน W9), เลือกกลุ่มย่อย (เช่น Purchase == 1 ใน HW6), ตัดแถวที่ไม่มี label

### 🐍 Python

```python
long_term = churn[churn["tenure"] >= 24]                                   # เงื่อนไขเดียว
fiber_m2m = churn[(churn["InternetService"] == "Fiber optic")
                  & (churn["Contract"] == "Month-to-month")]               # และ → &  (ต้องมีวงเล็บ!)
either    = churn[(churn["tenure"] < 3) | (churn["MonthlyCharges"] > 100)]  # หรือ → |
in_list   = churn[churn["PaymentMethod"].isin(["Electronic check", "Mailed check"])]
mid_range = churn[churn["MonthlyCharges"].between(50, 80)]                  # รวมขอบ
complete  = churn.dropna(subset=["TotalCharges"])                           # ตัดแถวที่ค่าว่าง
same_q    = churn.query("tenure >= 24 and Contract == 'Two year'")          # เขียนแบบ SQL
print(len(long_term), len(fiber_m2m), len(complete))
```

> [!warning] กับดัก pandas
> - ใช้ `and`/`or` กับ Series ไม่ได้ → **ต้องใช้ `&` / `|` และครอบแต่ละเงื่อนไขด้วยวงเล็บ**
> - หลัง filter แล้วจะแก้ค่า ให้ต่อท้าย `.copy()` เช่น `sub = df[df.x > 0].copy()` ไม่งั้นได้ `SettingWithCopyWarning`

### ⚙️ RapidMiner — `Filter Examples`

| พารามิเตอร์ | ค่า |
|---|---|
| **condition class** | `custom_filters` (ตั้งเงื่อนไขเอง) · `no_missing_attributes` (ตัดแถวที่มีค่าว่าง) · `missing_labels` / `no_missing_labels` · `correct_predictions` / `wrong_predictions` (หลัง Apply Model) |
| **filters** (กด **Add Filters…**) | เลือก attribute · comparator (`=`, `≠`, `<`, `≥`, `contains`, `is missing`…) · ค่า · เลือก **Match all** (AND) หรือ **Match any** (OR) |
| **invert filter** | ✅ = เก็บแถวที่ **ไม่** ตรงเงื่อนไข |

> port: **exa** = แถวที่ผ่าน · **ori** = ข้อมูลเดิมทั้งหมด · **unm** = แถวที่ไม่ผ่าน (มีในเวอร์ชันใหม่ — ใช้แยกข้อมูลสองกลุ่มได้ในขั้นเดียว)

**ทางเลือก:** `Filter Example Range` (เลือกแถวที่ i ถึง j) · `Remove Duplicates`

---

## 2.4 Set Role ⭐⭐

> [!important] Role คืออะไร (สำคัญมากใน RapidMiner — Python ไม่มีแนวคิดนี้ตรง ๆ)
> | Role | ความหมาย | ใน Python เทียบกับ |
> |---|---|---|
> | **regular** | feature ที่ใช้สร้างโมเดล (ค่า default) | คอลัมน์ใน `X` |
> | **label** | target ที่ต้องการทำนาย | `y` |
> | **id** | ตัวระบุแถว ไม่ใช้สร้างโมเดล | คอลัมน์ที่ตัดออกจาก X แต่เก็บไว้ดู |
> | **prediction** / **confidence** | สร้างโดย `Apply Model` | `predict()` / `predict_proba()` |
> | **cluster** | สร้างโดย `k-Means` | `labels_` |
>
> **learner ทุกตัวต้องมี label 1 คอลัมน์** (ยกเว้น clustering/association) · **Performance ต้องมีทั้ง label และ prediction**

### 🐍 Python — "Set Role" = แยก X / y เอง

```python
y = churn["Churn"].map({"No": 0, "Yes": 1})        # label → ตัวเลข 0/1 (positive = 1 = Yes)
ids = churn["customerID"]                          # "id" เก็บไว้ต่างหาก
X = churn.drop(columns=["customerID", "Churn"])    # regular attributes
print(X.shape, y.mean().round(3))
```

### ⚙️ RapidMiner — `Set Role`

- **attribute name** = `Churn` · **target role** = `label`
- ตั้งหลาย role พร้อมกันใน operator เดียว: **set additional roles → Edit List** → เพิ่ม `customerID` = `id`
- ถ้า label ใน CSV เป็น 0/1 → ใส่ **`Numerical to Binominal`** (attribute = label, min = 0, max = 0 → ค่า 0 กลายเป็น `false`, ค่าอื่นเป็น `true`) **ก่อน** Set Role

> [!warning] กับดัก "positive class" ใน RapidMiner
> `Performance (Binominal Classification)` คิด precision/recall ของ **ค่าที่ 2 ของ binominal mapping** — ซึ่งขึ้นกับลำดับที่เจอในข้อมูล ไม่ใช่ "Yes" เสมอ!
> **วิธีกัน (ทดสอบกับ batch run แล้วว่าได้ผล):** ใน `Performance (Binominal Classification)` ติ๊ก **manually set positive class** แล้วตั้ง **positive class** = `Yes` · แล้วเช็กในผลว่า precision/recall เป็นของคลาสที่ถูก (เช่น majority baseline ต้องได้ recall = 0 ไม่ใช่ 1)
> ⚠️ operator `Set Positive Value` มีในเครื่อง แต่ทดลองแล้ว **ไม่เปลี่ยนผลของ Performance** — อย่าพึ่งมัน

---

## 2.5 Join ⭐⭐⭐

**เมื่อไหร่ใช้:** ข้อมูลอยู่ 2 ตาราง มี **คอลัมน์ key ร่วมกัน** (เช่น customer_id) → ต่อ "แนวนอน" ให้ได้ตารางเดียว (เหมือน SQL JOIN จาก ETL มิดเทอม)

```python
customers = pd.DataFrame({"cust_id": [1, 2, 3, 4],
                          "name": ["Ann", "Bo", "Cy", "Di"],
                          "segment": ["A", "B", "A", "C"]})
orders = pd.DataFrame({"cust_id": [1, 1, 2, 5],
                       "amount": [100, 250, 80, 40]})

inner = pd.merge(customers, orders, on="cust_id", how="inner")   # เฉพาะ key ที่มีทั้งสองฝั่ง
left  = pd.merge(customers, orders, on="cust_id", how="left")    # เก็บลูกค้าทุกคน (ไม่มี order → NaN)
right = pd.merge(customers, orders, on="cust_id", how="right")   # เก็บ order ทุกแถว
outer = pd.merge(customers, orders, on="cust_id", how="outer", indicator=True)  # ทุกแถวทั้งสองฝั่ง
print({k: len(v) for k, v in dict(inner=inner, left=left, right=right, outer=outer).items()})
outer
```

| how | ผล (แถว) | ใครหายไป |
|---|---|---|
| `inner` | **3** (Ann×2, Bo×1) | Cy, Di (ไม่มี order) และ order ของ cust 5 (ไม่มีลูกค้า) |
| `left` | **5** | order ของ cust 5 |
| `right` | **4** | Cy, Di |
| `outer` | **6** | ไม่มีใครหาย · คอลัมน์ `_merge` บอกว่าแถวมาจาก `both` / `left_only` / `right_only` |

```python
# key ชื่อไม่ตรงกันสองฝั่ง → left_on / right_on
orders2 = orders.rename(columns={"cust_id": "customer"})
pd.merge(customers, orders2, left_on="cust_id", right_on="customer", how="inner").head(2)

# ตรวจความถูกต้องของ key: validate="one_to_many" จะ error ทันทีถ้าฝั่ง customers มี key ซ้ำ
checked = pd.merge(customers, orders, on="cust_id", how="left", validate="one_to_many")
```

> [!warning] กับดัก join
> - **แถวเพิ่มขึ้นผิดปกติ** = key ซ้ำทั้งสองฝั่ง (many-to-many) → เช็ก `df.key.duplicated().sum()` ก่อน join เสมอ
> - **join แล้วได้ NaN** ในตาราง left = แถวนั้นไม่มีคู่ → ต้องตัดสินใจว่าจะเติมค่า (เช่น amount = 0) หรือตัดทิ้ง
> - คอลัมน์ชื่อซ้ำ (ไม่ใช่ key) จะได้ `_x`, `_y` ต่อท้าย → ตั้ง `suffixes=("_cust", "_ord")`

### ⚙️ RapidMiner — `Join`

- **ต่อ port:** ตารางแรก → **left** · ตารางที่สอง → **right** · ผล → **join**
- **join type:** `inner` / `left` / `right` / `outer` (ความหมายเดียวกับ pandas)
- **key:** ติ๊ก **use id attribute as key** (ต้อง `Set Role` key เป็น id ทั้งสองตารางก่อน) **หรือ** เอาติ๊กออกแล้วตั้ง **key attributes → Edit List** (left key = `cust_id`, right key = `cust_id`)
- **remove double attributes** ✅ = ตัดคอลัมน์ชื่อซ้ำจากฝั่งขวา
- key ต้องเป็น **ชนิดเดียวกัน** ทั้งสองฝั่ง (integer กับ integer) ไม่งั้น error *attributes type mismatch*

---

## 2.6 Concatenate / Append ⭐⭐

**เมื่อไหร่ใช้:** ข้อมูลชุดเดียวกันถูกแบ่งเป็นหลายไฟล์ (เช่น ไตรมาส 1 + ไตรมาส 2) → ต่อ "แนวตั้ง" (เพิ่มแถว) · **คอลัมน์ต้องตรงกัน**

```python
q1 = churn.iloc[:3000]
q2 = churn.iloc[3000:]
stacked = pd.concat([q1, q2], ignore_index=True)          # ต่อแถว + รีเซ็ต index 0..n-1
print(len(q1), len(q2), len(stacked))                     # 3000 4043 7043

# ต่อ "คอลัมน์" (axis=1) — แถวต้องเรียงตรงกัน · ส่วนใหญ่ใช้ merge ดีกว่า
side = pd.concat([churn[["tenure"]], churn[["Churn"]]], axis=1)

# เช็กก่อนต่อแถวว่าคอลัมน์ตรงกันไหม
print(set(q1.columns) ^ set(q2.columns))                  # set() = ตรงกันหมด
```

> [!warning] กับดัก concat
> ถ้าคอลัมน์ไม่ตรงกัน pandas **ไม่ error** แต่เติม NaN ให้คอลัมน์ที่อีกฝั่งไม่มี → เช็ก `set(a.columns) ^ set(b.columns)` ก่อนเสมอ

### ⚙️ RapidMiner — `Append`

- ต่อ port **example set 1**, **example set 2**, … (port ใหม่โผล่เองเมื่อต่อเส้น) → ผลที่ **merged set**
- **attribute ต้องชื่อและชนิดตรงกันทุกตัว** ไม่งั้น error → ใช้ `Rename` / `Select Attributes` ปรับก่อน
- `merge type` = `all` (ปกติ)

---

## 2.7 Pivot / Aggregate ⭐⭐⭐

**เมื่อไหร่ใช้:** สรุปตารางไขว้ (cross-tab) เช่น "อัตรา churn ตาม Contract × InternetService" — ใช้ตอบโจทย์ "จงสรุป/เปรียบเทียบกลุ่ม"

```python
# groupby + agg = "Aggregate" (สรุปทีละกลุ่ม)
by_contract = (churn.groupby("Contract")
                    .agg(n=("Churn", "size"),
                         churn_rate=("Churn", lambda s: (s == "Yes").mean()),
                         avg_monthly=("MonthlyCharges", "mean"))
                    .round(3)
                    .sort_values("churn_rate", ascending=False))
by_contract
```

```python
# pivot_table = "Pivot" (กลุ่มแถว × กลุ่มคอลัมน์)
churn["is_churn"] = (churn["Churn"] == "Yes").astype(int)
rate = pd.pivot_table(churn, index="Contract", columns="InternetService",
                      values="is_churn", aggfunc="mean", margins=True, margins_name="All")
rate.round(3)
```

```python
# crosstab = นับความถี่ไขว้ · normalize="index" → สัดส่วนต่อแถว
pd.crosstab(churn["Contract"], churn["Churn"], normalize="index").round(3)
```

> [!important] ⭐ ตีความตาราง pivot (ตัวอย่างประโยค)
> *"ลูกค้าสัญญา **Month-to-month** มีอัตรา churn **42.7%** สูงกว่าสัญญา **Two year (2.8%)** ประมาณ 15 เท่า · และในทุกประเภทสัญญา ผู้ใช้ **Fiber optic** churn สูงกว่า DSL → กลุ่มเสี่ยงที่สุดคือ Month-to-month + Fiber optic ควรเป็นเป้าหมายแคมเปญรักษาลูกค้า"*
>
> สูตรประโยค: **[กลุ่มที่สูงสุด] มี [ค่า] สูงกว่า [กลุ่มต่ำสุด] [กี่เท่า/กี่ %] → [ข้อสรุปเชิงธุรกิจ]**

```python
# melt = de-pivot (ตารางกว้าง → ยาว) — ใช้ตอนต้องวาด seaborn แยกสีตามกลุ่ม
long = rate.drop(index="All", columns="All").reset_index().melt(
    id_vars="Contract", var_name="InternetService", value_name="churn_rate")
long.head(3)
```

### ⚙️ RapidMiner — `Aggregate` และ `Pivot`

| Operator | พารามิเตอร์หลัก | เทียบ pandas |
|---|---|---|
| **`Aggregate`** | **group by attributes** = `Contract` · **aggregation attributes → Edit List**: (`MonthlyCharges`, `average`), (`customerID`, `count`) | `groupby().agg()` |
| **`Pivot`** | **group by attributes** = `Contract` (เป็นแถว) · **column grouping attribute** = `InternetService` (กลายเป็นคอลัมน์) · **aggregation attributes**: (`MonthlyCharges`, `average`) | `pivot_table(index, columns, values, aggfunc)` |
| **`De-Pivot`** | attribute name / series of attributes | `melt()` |

> [!tip] อัตรา churn ใน RapidMiner (เพราะ aggregate "mean ของ Yes/No" ไม่ได้)
> `Generate Attributes` สร้าง `is_churn = if(Churn=="Yes", 1, 0)` → แล้ว `Pivot`/`Aggregate` ด้วย function `average` ของ `is_churn`

---

## 2.8 Basic Charts + การตีความ ⭐⭐⭐

### 🎯 ตารางเลือกกราฟ (ทวนจากมิดเทอม [[03 Exploratory Data Analysis (EDA)#🎯 ตารางเลือกกราฟ]])

| คำถาม | ชนิดตัวแปร | กราฟ | seaborn / matplotlib | RapidMiner (Visualizations) |
|---|---|---|---|---|
| การกระจายของตัวแปรเดียว | numeric | **Histogram** | `sns.histplot` | Histogram |
| ค่ากลาง/การกระจาย/outlier, เทียบกลุ่ม | numeric × category | **Boxplot** | `sns.boxplot` | Boxplot |
| ความถี่ของแต่ละกลุ่ม | category | **Bar / Count** | `sns.countplot` | Bar |
| ความสัมพันธ์ 2 ตัวแปร | numeric × numeric | **Scatter** | `sns.scatterplot(hue=)` | Scatter (color = label) |
| correlation หลายตัวพร้อมกัน | numeric ทั้งหมด | **Heatmap** | `sns.heatmap(df.corr())` | `Correlation Matrix` operator |
| แนวโน้มตามลำดับ (k, เวลา) | numeric ตามลำดับ | **Line** | `plt.plot` | Series |

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

sns.histplot(churn, x="MonthlyCharges", hue="Churn", stat="density",
             common_norm=False, ax=axes[0, 0])                  # normalized → เทียบรูปทรงได้แม้กลุ่มขนาดไม่เท่า
axes[0, 0].set_title("MonthlyCharges by Churn")

sns.boxplot(churn, x="Contract", y="tenure", ax=axes[0, 1])
axes[0, 1].set_title("tenure by Contract")

sns.countplot(churn, x="InternetService", hue="Churn", ax=axes[1, 0])
axes[1, 0].set_title("Churn count by InternetService")

num = churn[["tenure", "MonthlyCharges", "TotalCharges", "is_churn"]]
sns.heatmap(num.corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=axes[1, 1])
axes[1, 1].set_title("Correlation")

plt.tight_layout()
plt.savefig("/tmp/lab02_charts.png", dpi=100)   # ในห้องสอบใช้ plt.show() ก็พอ
```

> [!important] ⭐ ประโยคตีความกราฟ — โครง "สิ่งที่เห็น → ตัวเลข → ความหมาย"
> | กราฟ | ตัวอย่างประโยค |
> |---|---|
> | Histogram | *"MonthlyCharges ของกลุ่ม churn กระจุกที่ **70–110** ขณะที่กลุ่มไม่ churn มียอดสูงที่ **~20** (ลูกค้าไม่มีอินเทอร์เน็ต) → ลูกค้าที่จ่ายแพงมีแนวโน้มยกเลิกมากกว่า"* |
> | Boxplot | *"median ของ tenure ในสัญญา Two year สูงกว่า Month-to-month ชัดเจน กล่องแทบไม่ซ้อนกัน → ประเภทสัญญาสัมพันธ์กับอายุการเป็นลูกค้า"* |
> | Countplot | *"Fiber optic มีจำนวน churn มากที่สุดทั้งจำนวนและสัดส่วน"* (⚠️ จำนวนเยอะอาจเพราะกลุ่มใหญ่ → ต้องดู **สัดส่วน** จาก crosstab ประกอบ) |
> | Heatmap | *"tenure กับ TotalCharges มี r = 0.83 (สัมพันธ์บวกสูง — ระวัง multicollinearity) · tenure กับ churn r = −0.35 (อยู่นานยิ่งไม่ยกเลิก)"* |
> | Scatter | *"จุดสองคลาสแยกกันตามแนว Age × Salary → feature 2 ตัวนี้น่าจะแยกคลาสได้ดี"* |

> [!warning] ข้อจำกัดที่ต้องเขียนกำกับเสมอ (กันโดนหักคะแนน)
> - **correlation ≠ causation** และ $r$ วัดแค่ **ความสัมพันธ์เชิงเส้น** — $r \approx 0$ อาจสัมพันธ์แบบโค้งก็ได้
> - กราฟ count เทียบกลุ่มขนาดไม่เท่ากัน → **ใช้สัดส่วน/normalize**
> - outlier ใน boxplot = จุดนอก $Q_1 - 1.5\,IQR$ / $Q_3 + 1.5\,IQR$ — ต้องตรวจว่าเป็น **error หรือค่าจริงที่หายาก** ก่อนตัดทิ้ง

### ⚙️ RapidMiner — Visualizations

1. รัน process → Results → ExampleSet → แท็บ **Visualizations**
2. เลือก **Chart type** (Histogram / Boxplot / Scatter / Bar / Series / Pie)
3. ตั้ง **Value columns** (แกน), **Color** = label เพื่อแยกคลาส · Histogram ตั้งจำนวน **bins**
4. **Correlation heatmap:** operator **`Correlation Matrix`** → ผล "Correlation Matrix" มีมุมมอง Pairwise Table และแบบสีแดง/น้ำเงิน
5. **Screenshot ใส่รายงาน:** ปุ่ม export ที่มุมกราฟ หรือ screenshot ทั้งหน้าจอ (Linux: `PrtSc` / `Shift+PrtSc` เลือกพื้นที่)

---

## 🏋️ Drills (closed-book — ทำเองก่อน แล้วค่อยกดดูเฉลย)

> [!question]- D1. (Python) จาก `HW5/adult.csv` จงนับจำนวน `'?'` ในแต่ละคอลัมน์ แปลงเป็น NaN แล้วหาสัดส่วนคนที่ `income == '>50K'` แยกตาม `education` เรียงจากมากไปน้อย 3 อันดับแรก
> ```python
> adult = pd.read_csv("HW5/adult.csv")
> print((adult == "?").sum().loc[lambda s: s > 0])      # workclass 2799 · occupation 2809 · native-country 857
> adult = adult.replace("?", np.nan)
> top3 = (adult.assign(rich=(adult["income"] == ">50K").astype(int))
>              .groupby("education")["rich"].mean()
>              .sort_values(ascending=False).head(3).round(3))
> print(top3)                                            # Prof-school / Doctorate / Masters
> ```

> [!question]- D2. (Python) ทำ pivot ค่าเฉลี่ย `hours-per-week` ของ adult โดยแถว = `gender` คอลัมน์ = `income` แล้วตีความ 1 ประโยค
> ```python
> hp = pd.pivot_table(adult, index="gender", columns="income", values="hours-per-week", aggfunc="mean").round(1)
> print(hp)
> # Female: 35.9 vs 40.7 · Male: 40.7 vs 46.3
> # ตีความ: ทั้งชายและหญิง กลุ่ม >50K ทำงานต่อสัปดาห์มากกว่ากลุ่ม <=50K ราว 5 ชม. (4.8 และ 5.6)
> #         และชายทำงานมากกว่าหญิงในทุกกลุ่มรายได้ — แต่เป็นความสัมพันธ์ ไม่ได้แปลว่าชั่วโมงงานเป็นเหตุของรายได้
> ```

> [!question]- D3. (RapidMiner) เขียนลำดับ operator สำหรับ: อ่าน `customers.csv` และ `orders.csv` → เก็บลูกค้าทุกคนแม้ไม่มี order → หายอดรวม amount ต่อ segment
> `Read CSV (customers)` → **left** ของ `Join` · `Read CSV (orders)` → **right** · Join: **join type = left**, key attributes = cust_id ↔ cust_id → `Replace Missing Values` (amount → zero) → `Aggregate` (group by = segment, aggregation = amount : sum)
> **คำถามต่อ:** ถ้าใช้ inner join ผลเปลี่ยนอย่างไร? → ลูกค้าที่ไม่มี order หายไป ยอดรวมต่อ segment ไม่เปลี่ยน แต่ "จำนวนลูกค้า" ต่อ segment จะผิด

> [!question]- D4. (ทั้งสองเครื่องมือ) churn: label เป็น Yes/No แต่ RapidMiner ให้ precision = 0.93 ทั้งที่ Python ให้ 0.55 — สาเหตุที่เป็นไปได้มากที่สุดคืออะไร
> **positive class คนละตัว** — RapidMiner คิด precision ของคลาส "No" (ค่าที่ 2 ใน mapping) ขณะที่ Python ตั้ง pos_label = Yes → แก้ด้วยการติ๊ก **manually set positive class** = Yes ใน Performance แล้วรันใหม่

> [!question]- D5. (ตีความ) heatmap ให้ r(tenure, TotalCharges) = 0.83 และ r(tenure, churn) = −0.35 จงเขียนข้อสรุปพร้อมข้อจำกัด 1 ข้อ
> tenure กับ TotalCharges สัมพันธ์เชิงบวกสูง (เพราะยอดรวม ≈ ค่ารายเดือน × จำนวนเดือน) → ใส่ทั้งคู่ใน linear/logistic model อาจเกิด **multicollinearity** · tenure สัมพันธ์เชิงลบปานกลางกับการยกเลิก → ลูกค้าเก่ายกเลิกน้อยกว่า · **ข้อจำกัด:** correlation ไม่ได้บอกเหตุ-ผล และวัดแค่ความสัมพันธ์เชิงเส้น

---

**ถัดไป →** [[LAB 03 Preprocessing Recipes]] · **กลับหน้าหลัก →** [[LAB 00 START HERE]]
