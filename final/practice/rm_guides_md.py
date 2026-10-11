"""เขียนไกด์ RapidMiner (PR 01–09) จากผลที่ batch runner รันจริง (final/practice/rm/out/)

ลำดับ:  python rm_guides.py   (สร้าง + รัน process)  →  python rm_guides_md.py  (เขียนไกด์)
"""
from pathlib import Path
import re
import pandas as pd
from rm_diagrams import inject

HERE = Path(__file__).resolve().parent
OUT = HERE / "rm" / "out"
VAULT = HERE.parent / "obsidian" / "practice"


def perf(tag):
    """PerformanceVector CSV → {criterion: (mean, std)}"""
    df = pd.read_csv(OUT / f"{tag}.csv")
    return {r.Criterion: (r.Value, r["Standard Deviation"]) for _, r in df.iterrows()}


def pct(tag, crit, sd=True):
    v, s = perf(tag)[crit]
    if pd.isna(v):
        return "?"
    return f"{v:.2%}" + (f" +/- {s:.2%}" if sd and not pd.isna(s) and s > 0 else "")


def num(tag, crit, fmt="{:,.1f}"):
    return fmt.format(perf(tag)[crit][0])


def head(no, topic, story, data, minutes, py_name):
    return f"""---
title: PR {no:02d} · {topic} (RapidMiner)
tags: [final, lab, practice, rapidminer]
---

# PR {no:02d} · {topic} — ไกด์ RapidMiner ทีละขั้น

> [!abstract] โจทย์ (เดียวกับไกด์ Python)
> {story}

**ข้อมูล:** `final/practice/data/{data}` · **เวลาแนะนำ:** {minutes} นาที
**ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · [[PR 00 START HERE#⚙️ ทักษะพื้นฐาน RapidMiner (อ่านก่อนไกด์แรก)|ทักษะพื้นฐาน RapidMiner]] · ทำใน Python: [[{py_name}]]
**เฉลย process:** `final/practice/rm/P{no:02d}_solution.rmp` — ทำเองให้เสร็จก่อน แล้วค่อย **File → Import Process…** เปิดเทียบ (ตัวเลขทุกตัวในไกด์มาจากการรันไฟล์นี้จริง)

> [!tip] เริ่มต้น: **File → New Process → Blank** · ทำทีละขั้น กด ▶ **Run** หลังทุกขั้นที่มี "ผลที่ควรเห็น" แล้วเทียบ · ไม่ตรง → หยุดหาสาเหตุก่อน
> ตัวเลขของคุณควร **ตรงเป๊ะ** ถ้าตั้ง **local random seed = 1992** ตามไกด์ (ยกเว้นบอกไว้ว่าอาจต่างเล็กน้อย)

---
"""


def write(name, text):
    VAULT.mkdir(parents=True, exist_ok=True)
    text = inject(int(name[3:5]), text)      # ภาพ canvas หลังแต่ละขั้น (rm_diagrams.py)
    (VAULT / name).write_text(text.strip() + "\n", encoding="utf-8")
    print("  ✓", name)


# ════════════════════════════════════ P1 ══════════════════════════════════════════════════════
agg = pd.read_csv(OUT / "p1_aggregate.csv")
piv = pd.read_csv(OUT / "p1_pivot.csv")
n_filter = len(pd.read_csv(OUT / "p1_filter.csv"))
allp1 = pd.read_csv(OUT / "p1_all.csv")
fri = agg[agg.day == "Fri"].iloc[0]
write("PR 01 Data Handling (RapidMiner).md", head(1, "Data Handling", "ร้านอาหารส่งบิล 2 สัปดาห์มาเป็น 2 ไฟล์ และตารางข้อมูลวันทำการแยกอีกไฟล์ จง append + join ให้เป็นตารางเดียว สร้าง tip% กรองโต๊ะใหญ่มื้อเย็น สรุปตามวัน และทำ pivot วัน × มื้อ",
    "p1_bills_week1.csv · p1_bills_week2.csv · p1_day_info.csv", 40, "PR 01 Data Handling (Python)") + f"""
## ขั้นที่ 1 · อ่านไฟล์ 3 ไฟล์ (Read CSV)
1. แผง **Operators** → พิมพ์ `Read CSV` → ลากมาวาง **3 ตัว** (เรียงลงมา)
2. คลิกตัวแรก → แผง **Parameters**: **csv file** → กดไอคอน 📁 → เลือก `final/practice/data/p1_bills_week1.csv` · **column separators** = `,` (ค่า default `,;` ก็ได้) · ✅ **first row as names**
3. ตัวที่ 2 → `p1_bills_week2.csv` · ตัวที่ 3 → `p1_day_info.csv`
4. ดับเบิลคลิกชื่อ operator เพื่อเปลี่ยนชื่อเป็น `Read week1`, `Read week2`, `Read day_info` (อ่านง่ายตอน screenshot)
5. ต่อ port **out** ของ `Read week1` → port **res** ขอบขวา → ▶ Run

**ผลที่ควรเห็น:** แท็บ ExampleSet — **130 examples**, 8 regular attributes (bill_id, total_bill, tip, sex, smoker, day, time, size) · แท็บ **Statistics** ไม่มี Missing
> 💡 ถ้าคอลัมน์ทั้งหมดรวมเป็นคอลัมน์เดียว = ตั้ง column separators ผิด

---

## ขั้นที่ 2 · ต่อสองสัปดาห์ (Append)
1. ลบเส้นที่ต่อไป res (คลิกเส้น → Delete) · ลาก **`Append`** มาวาง
2. `Read week1` **out** → `Append` **example set 1** · `Read week2` **out** → **example set 2** (port ใหม่โผล่เองเมื่อต่อเส้น)
3. Parameters: **merge type** = `all`
4. `Append` **merged set** → **res** → ▶

**ผลที่ควรเห็น:** **244 examples** (130 + 114) · ถ้า error "attributes are different" = คอลัมน์สองไฟล์ไม่ตรงกัน

---

## ขั้นที่ 3 · Join กับตารางวัน (Join — left)
1. ลาก **`Join`** มาวาง · `Append` **merged set** → `Join` **left** · `Read day_info` **out** → `Join` **right**
2. Parameters:

| parameter | ค่า |
|---|---|
| **join type** | `left` (เก็บบิลทุกใบ) |
| **use id attribute as key** | ☐ เอาออก |
| **key attributes** → Edit List… | left key attribute = `day` · right key attribute = `day` |
| **remove double attributes** | ✅ |

3. `Join` **join** → **res** → ▶

**ผลที่ควรเห็น:** **{len(allp1)} examples**, **10 attributes** (เพิ่ม `is_weekend`, `open_hours`) · คอลัมน์ is_weekend ไม่มีค่าว่าง

---

## ขั้นที่ 4 · สร้าง tip_pct (Generate Attributes)
1. ลาก **`Generate Attributes`** ต่อจาก Join (**join** → **example set input**)
2. **function descriptions** → **Edit List…** → attribute name = `tip_pct` · function expressions = `tip / total_bill * 100` (กดไอคอนเครื่องคิดเลขเพื่อเปิด Expression editor ได้)
3. **example set output** → res → ▶

**ผลที่ควรเห็น:** คอลัมน์ใหม่ `tip_pct` · แท็บ Statistics: average ≈ **{allp1.tip_pct.mean():.2f}**, max ≈ **{allp1.tip_pct.max():.2f}**

---

## ขั้นที่ 5 · แยกข้อมูลไปหลายทาง (Multiply)
ลาก **`Multiply`** ต่อจาก Generate Attributes → จะใช้ output 1 / 2 / 3 / 4 สำหรับขั้นถัดไป (ข้อมูลชุดเดียวกันถูกก๊อปไปหลายเส้น)

---

## ขั้นที่ 6 · กรองโต๊ะใหญ่มื้อเย็น (Filter Examples)
1. `Multiply` **output 1** → **`Filter Examples`**
2. **condition class** = `custom_filters` → **filters** → **Add Filters…**
   - แถว 1: `time` · `=` · `Dinner`
   - แถว 2: `size` · `≥` · `4`
   - เลือก **Match all** (AND)
3. **example set output** → res → ▶

**ผลที่ควรเห็น:** **{n_filter} examples**

---

## ขั้นที่ 7 · สรุปตามวัน (Aggregate)
1. `Multiply` **output 2** → **`Aggregate`**
2. ☐ **use default aggregation** · **group by attributes** → เลือก `day`
3. **aggregation attributes** → Edit List… : (`bill_id`, `count`) · (`total_bill`, `average`) · (`tip_pct`, `average`)
4. ▶

**ผลที่ควรเห็น:**

| day | count(bill_id) | average(total_bill) | average(tip_pct) |
|---|---|---|---|
""" + "\n".join(f"| {r.day} | {r['count(bill_id)']} | {r['average(total_bill)']:.2f} | {r['average(tip_pct)']:.2f} |" for _, r in agg.iterrows()) + f"""

→ tip% สูงสุดวัน **Fri ({fri['average(tip_pct)']:.2f}%)** · บิลเยอะสุดวัน Sat (87) — ตรงกับ Python

---

## ขั้นที่ 8 · Pivot วัน × มื้อ (Pivot)
1. `Multiply` **output 3** → **`Pivot`**
2. **group by attributes** = `day` · **column grouping attribute** = `time` · **aggregation attributes** → Edit List… : (`tip_pct`, `average`)
3. ▶

**ผลที่ควรเห็น:**

| day | average(tip_pct)_Dinner | average(tip_pct)_Lunch |
|---|---|---|
""" + "\n".join(f"| {r.day} | {r.iloc[1]:.2f} | {'?' if pd.isna(r.iloc[2]) else f'{r.iloc[2]:.2f}'} |" for _, r in piv.iterrows()) + """

ช่อง `?` = **missing** (Sat/Sun ไม่มีมื้อกลางวัน) — ไม่ใช่ 0

---

## ขั้นที่ 9 · กราฟ (Results → Visualizations)
`Multiply` **output 4** → res → ▶ → ExampleSet → แท็บ **Visualizations**:
1. **Histogram**: Value column = `tip_pct` · bins 25 → ส่วนใหญ่ 10–20% หางขวายาว
2. **Boxplot**: Value = `tip_pct` · Group by/Color = `day` → median ใกล้กัน มี outlier ด้านบน
3. **Scatter**: x = `total_bill` · y = `tip` · Color = `time` → tip เพิ่มตามบิล
4. Screenshot ใส่รายงาน (`Shift+PrtSc`)

> [!success] เทียบคำตอบ: 244 บิล · tip% เฉลี่ย 16.08 · Fri สูงสุด 16.99% · โต๊ะใหญ่มื้อเย็น 37 บิล (ตรงกับไกด์ Python ทุกตัว)
""")

# ════════════════════════════════════ P2 ══════════════════════════════════════════════════════
bins = pd.read_csv(OUT / "p2_mass_bins.csv")
pcatext = (OUT / "p2_pca_model.txt").read_text()
pc1 = re.search(r"PC 1:(.*)", pcatext).group(1).strip()
pc2 = re.search(r"PC 2:(.*)", pcatext).group(1).strip()
write("PR 02 Preprocessing & PCA (RapidMiner).md", head(2, "Preprocessing & PCA", "เตรียมข้อมูลนกเพนกวิน (มีค่าว่าง, categorical, หน่วยต่างกัน) ให้ k-NN ทำนายสายพันธุ์โดยไม่ leak · discretize น้ำหนัก · PCA 2 มิติ",
    "p2_penguins.csv", 45, "PR 02 Preprocessing & PCA (Python)") + f"""
## ขั้นที่ 1 · อ่านไฟล์ + ดูค่าว่าง
`Read CSV` → `p2_penguins.csv` → res → ▶ → แท็บ **Statistics**
**ผลที่ควรเห็น:** **344 examples** · ตัวเลข 4 คอลัมน์ Missing = **2** · `sex` Missing = **11** · species / island / sex เป็น polynominal

---

## ขั้นที่ 2 · ตัดแถวที่ไม่มีการวัด (Filter Examples)
`Filter Examples` → condition class `custom_filters` → Add Filters: `body_mass_g` · **is not missing** → ▶
**ผลที่ควรเห็น:** **342 examples** (การตัดแถวที่ว่างทั้งแถวไม่ได้ "เรียนค่า" จึงทำนอก CV ได้)

---

## ขั้นที่ 3 · Set Role
`Set Role`: attribute name = `species` · target role = `label` → ▶ → ExampleSet บอก **1 special attribute** (คอลัมน์ species เปลี่ยนสี)
ต่อ **`Multiply`** ต่อท้าย (จะใช้ 3 ทาง)

---

## ขั้นที่ 4 · Discretize น้ำหนักเป็น 3 ช่วงจำนวนเท่ากัน
1. Multiply **output 2** → **`Discretize by Frequency`**: attribute filter type `single` · attribute `body_mass_g` · **number of bins** = 3 · range name type `short`
2. ต่อ **`Aggregate`**: group by attributes = `body_mass_g` และ `species` (กด Select Attributes… → ✅ include special attributes ถ้ามองไม่เห็น species) · aggregation: (`island`, `count`) → ▶

**ผลที่ควรเห็น:**

| body_mass_g | species | count |
|---|---|---|
""" + "\n".join(f"| {r.body_mass_g} | {r.species} | {r['count(island)']} |" for _, r in bins.iterrows()) + f"""

→ ช่วงหนักสุด (range3) เป็น Gentoo เกือบทั้งหมด

---

## ขั้นที่ 5 · PCA 2 มิติ (Select Attributes → Normalize → PCA)
1. Multiply **output 1** → **`Select Attributes`**: attribute filter type = `value_type` · value type = `numeric` (เหลือตัวเลข 4 ตัว + label)
2. → **`Normalize`**: method = `Z-transformation` (**ต้อง normalize ก่อน PCA**)
3. → **`Principal Component Analysis`**: dimensionality reduction = `fixed number` · number of components = `2`
4. port **exa** → res · port **pre** (PCA model) → res → ▶

**ผลที่ควรเห็น:**
- PCA model → แท็บ **Eigenvalues**: PC1 Proportion of Variance ≈ **0.688** · PC2 ≈ **0.193** · Cumulative ≈ **0.882**
- แท็บ **Eigenvectors** (loadings):
  - `PC 1: {pc1}`
  - `PC 2: {pc2}`
  - (เครื่องหมายอาจกลับด้านจาก Python — ความหมายเหมือนเดิม)
- ExampleSet → Visualizations → **Scatter**: x = `pc_1` · y = `pc_2` · Color = `species` → Gentoo แยกออกชัดตาม PC1

---

## ขั้นที่ 6 · k-NN ใน Cross Validation โดย preprocessing อยู่ใน Training pane
1. Multiply **output 3** → **`Cross Validation`**: number of folds = **5** · sampling type = `stratified sampling` · ✅ use local random seed · local random seed = **1992**
2. **ดับเบิลคลิก** Cross Validation → เห็น 2 ช่อง
   - **Training** (ซ้าย): `tra` → **`Replace Missing Values`** (default = `average`, ✅ return preprocessing model — ค่า "average" ของ nominal = mode) → **`Nominal to Numerical`** (coding type `dummy coding`) → **`Normalize`** (Z) → **`k-NN`** (k = 5) → **`Group Models`**
     - ต่อ port **pre** ของ Replace Missing / Nominal to Numerical / Normalize เข้า Group Models **models in 1, 2, 3** และ **mod** ของ k-NN เข้า **models in 4** → **model out** → `mod` ขอบขวา
   - **Testing** (ขวา): `mod` → **`Apply Model`** (mod) · `tes` → Apply Model (unl) → **`Performance (Classification)`** (✅ accuracy) → `per`
3. ขึ้นมาข้างนอก (ปุ่ม ⬆) → Cross Validation **per** → res → ▶

**ผลที่ควรเห็น:** accuracy **{pct('p2_knn', 'accuracy')}**
**ทดลองเพิ่ม:** ลบ `Normalize` ออกจาก Training pane (เหลือ group models 2 ตัว) → accuracy เหลือ **{pct('p2_knn_raw', 'accuracy')}** → scaling สำคัญมากกับ k-NN

> [!warning] ทำไมต้องอยู่ใน Training pane — Replace Missing / Normalize "เรียนค่า" (mean, std) จากข้อมูล ถ้าวางนอก CV ค่าจะรวม test fold = leakage · Group Models ส่งค่าที่เรียนจาก training fold ไปใช้กับ test fold

> [!success] เทียบ Python: Python ได้ CV 0.9890 (sklearn ใช้ median และ split คนละแบบ — ต่างกันเล็กน้อยได้)
""")

# ════════════════════════════════════ P3 ══════════════════════════════════════════════════════
write("PR 03 Imbalanced & SMOTE (RapidMiner).md", head(3, "Imbalanced & SMOTE", "ผลชิ้นเนื้อ 397 ราย มีมะเร็ง 40 ราย เปรียบเทียบ baseline / tree / tree + undersampling / tree + SMOTE ใน 5-fold CV โดย resample **เฉพาะ training fold** และวัดด้วย recall/F1 ของ malignant",
    "p3_breast_cancer_imbalanced.csv", 35, "PR 03 Imbalanced & SMOTE (Python)") + f"""
> [!important] ต้องมี extension **Operator Toolbox** (มี operator `SMOTE Upsampling`) — เครื่องคุณติดตั้งแล้ว ✓

## ขั้นที่ 1 · อ่าน + Set Role + Multiply
`Read CSV` (`p3_breast_cancer_imbalanced.csv`) → `Set Role` (diagnosis → label) → `Multiply` → ▶ ดู Statistics ของ diagnosis
**ผลที่ควรเห็น:** 397 examples · diagnosis: benign **357** / malignant **40** → IR = 8.93

---

## ขั้นที่ 2 · แม่แบบ Cross Validation (ทำครั้งเดียวแล้ว copy)
1. Multiply **output 1** → `Cross Validation`: folds **5** · `stratified sampling` · seed **1992**
2. Testing pane: `Apply Model` → **`Performance (Binominal Classification)`**: ✅ accuracy, precision, recall, f measure · main criterion = `f_measure` · ✅ **manually set positive class** → positive class = `malignant` (ถ้าไม่เห็นกด *Show advanced parameters*)
3. เลือก Cross Validation → `Ctrl+C`, `Ctrl+V` อีก 3 ครั้ง → ต่อ Multiply output 2, 3, 4 · เปลี่ยนชื่อเป็น `CV baseline`, `CV tree`, `CV RUS`, `CV SMOTE`

> ⚠️ ถ้าไม่ตั้ง positive class เอง RapidMiner อาจคิด precision/recall ให้ **benign** → baseline จะได้ recall 1.0 ดูดีผิด ๆ

---

## ขั้นที่ 3 · Training pane ของแต่ละ CV
| CV | Training pane | ตั้งค่า |
|---|---|---|
| **baseline** | `tra` → **`Default Model`** → `mod` | method = `mode` |
| **tree** | `tra` → **`Decision Tree`** → `mod` | criterion `gini_index` · maximal depth **4** · ☐ apply pruning · ☐ apply prepruning |
| **RUS** | `tra` → **`Sample`** → `Decision Tree` (เหมือนบน) → `mod` | Sample: sample `absolute` · ✅ **balance data** · sample size per class → Edit List: `benign` = **32**, `malignant` = **32** (fold ละ 32 ราย malignant) · ✅ local random seed 1992 |
| **SMOTE** | `tra` → **`SMOTE Upsampling`** (port **exa** → **ups**) → `Decision Tree` → `mod` | number of neighbours **5** · ✅ normalize · ✅ equalize classes · ✅ auto detect minority class · ✅ local random seed 1992 |

ต่อ **per** ของทั้ง 4 CV → res → ▶ (จะได้ PerformanceVector 4 แท็บ)

---

## ขั้นที่ 4 · ผลที่ควรเห็น
| CV | accuracy | precision (malignant) | recall (malignant) | f measure |
|---|---|---|---|---|
""" + "\n".join(f"| {name} | {pct(t,'accuracy',False)} | {pct(t,'precision',False)} | {pct(t,'recall',False)} | {pct(t,'f_measure',False)} |"
                 for name, t in [("baseline", "p3_baseline"), ("tree", "p3_tree"), ("RUS", "p3_rus"), ("SMOTE", "p3_smote")]) + f"""

(ใน RapidMiner แต่ละช่องแสดงแบบ `xx% +/- yy%` = ค่าเฉลี่ย ± sd ข้าม fold) · precision ของ baseline เป็น `unknown` (ไม่มีการทาย malignant เลย)

**อ่านผล:** baseline accuracy {pct('p3_baseline','accuracy',False)} แต่ recall 0 · tree ไม่ resample ได้ F1 ดีสุด · **RUS / SMOTE เพิ่ม recall** ({pct('p3_tree','recall',False)} → {pct('p3_rus','recall',False)} / {pct('p3_smote','recall',False)}) แลกกับ precision ที่ลดลง → งานคัดกรองมะเร็งให้น้ำหนัก recall → เลือก SMOTE หรือ RUS

> [!bug] วิธีที่ผิด (สไลด์ Imbalanced p.20): วาง SMOTE Upsampling **ก่อน** Cross Validation → ลองทำดู แล้ว f measure จะสูงขึ้นมากเกินจริง เพราะ test fold มีจุดสังเคราะห์

> [!success] เทียบ Python: ทิศทางเดียวกัน (Python: tree F1 0.773 · RUS recall 0.90 · SMOTE recall 0.825) — ตัวเลขต่างเล็กน้อยเพราะ tree และ fold คนละ implementation
""")

# ════════════════════════════════════ P4 ══════════════════════════════════════════════════════
log4 = pd.read_csv(OUT / "p4_opt_log.csv").sort_values("k")
best4 = log4.loc[log4.accuracy.idxmax()]
write("PR 04 KNN Baseline CV Optimize (RapidMiner).md", head(4, "KNN Baseline CV Optimize", "ระบุสายพันธุ์องุ่นของไวน์จากเคมี 13 ค่า: baseline → k-NN ไม่ normalize → k-NN normalize → Optimize k ด้วย CV + Log",
    "p4_wine.csv", 40, "PR 04 KNN Baseline CV Optimize (Python)") + f"""
## ขั้นที่ 1 · อ่าน + Set Role + Multiply
`Read CSV` → `Set Role` (cultivar → label) → `Multiply` · ▶ ดู Statistics: proline min 278 / max 1680 vs hue ~0.5–1.7 → ต้อง normalize

---

## ขั้นที่ 2 · 3 Cross Validation: baseline / raw / normalized
ทุกตัว: number of folds **10** · `stratified sampling` · seed **1992** · Testing pane: `Apply Model` → **`Performance (Classification)`** (✅ accuracy) — label มี 3 คลาส จึงใช้ตัวนี้ (ไม่ใช่ Binominal)

| CV | Training pane |
|---|---|
| baseline | `Default Model` (method `mode`) |
| raw | `k-NN` (k = 5) |
| normalized | `Normalize` (Z) → `k-NN` (k = 5) → `Group Models` (Normalize **pre** → models in 1 · k-NN **mod** → models in 2) |

▶ **ผลที่ควรเห็น:**

| | accuracy |
|---|---|
| baseline | {pct('p4_baseline','accuracy')} |
| k-NN raw | {pct('p4_knn_raw','accuracy')} |
| **k-NN normalized** | **{pct('p4_knn_norm','accuracy')}** |

---

## ขั้นที่ 3 · Optimize Parameters (Grid) หา k
1. Multiply **output 4** → **`Optimize Parameters (Grid)`** → ดับเบิลคลิกเข้าไป
2. ข้างใน: copy `CV normalized` มาวาง → ต่อ `inp` (input 1) → CV **exa** · ต่อ CV **per** → **`Log`** → ต่อ Log **through 1** → `per` ขอบขวา
3. ออกมาข้างนอก → เลือก Optimize → **Edit Parameter Settings…**: ซ้ายเลือก `k-NN` (ตัวใน CV) → กลางเลือก **k** → ➡ → ตั้ง **Min 1 · Max 30 · Steps 29 · Scale linear** → OK
4. เลือก **Log** (ข้างใน) → **log** → Edit List…:
   - column name `k` → operator `k-NN` → **parameter** → `k`
   - column name `accuracy` → operator `Cross Validation` → **value** → `performance main criterion`
5. ข้างนอก: ลาก **`Log to Data`** (log name = `Log`) → res · Optimize **per** และ **par** → res → ▶

**ผลที่ควรเห็น:** ParameterSet: **k-NN.k = {int(best4.k)}** · accuracy **{best4.accuracy:.2%}** · ตาราง Log to Data 30 แถว (k vs accuracy) → Visualizations → **Series/Lines**: x = k, y = accuracy

| k | 1 | 5 | 10 | 15 | 20 | 25 | 30 |
|---|---|---|---|---|---|---|---|
| accuracy | """ + " | ".join(f"{log4[log4.k == k].accuracy.iloc[0]:.2%}" for k in [1, 5, 10, 15, 20, 25, 30]) + f""" |

> [!note] RapidMiner เลือก k = {int(best4.k)} ส่วน Python เลือก k = 5 — accuracy ต่างกันไม่ถึง 2% ในช่วง k กว้าง (folds และ z-score n−1 ต่างกัน) · เขียนในรายงานว่า "ช่วง k ประมาณ 13–30 ให้ผลใกล้เคียงกัน"

> [!success] เทียบ Python: baseline 0.399 · raw 0.686 · normalized 0.978
""")

# ════════════════════════════════════ P5 ══════════════════════════════════════════════════════
mt = (OUT / "p5_model.txt").read_text()
dthr = re.search(r"default threshold: ([0-9.]+)", mt).group(1)
auc = re.search(r"AUC: ([0-9.]+)", mt).group(1)
write("PR 05 Logistic Regression & Threshold (RapidMiner).md", head(5, "Logistic Regression & Threshold", "คัดกรองเบาหวาน: แปลง 0 ที่เป็นไปไม่ได้เป็นค่าว่าง → split 75/25 → เติมค่าว่างด้วยค่าจาก train → Logistic Regression → เทียบ threshold 0.5 กับ 0.3",
    "p5_pima_diabetes.csv", 40, "PR 05 Logistic Regression & Threshold (Python)") + f"""
## ขั้นที่ 1 · อ่าน + เตรียม label
`Read CSV` → **`Numerical to Binominal`** (attribute filter type `single` · attribute `diabetes` · min 0 · max 0 → 0 = false, 1 = true) → **`Set Role`** (diabetes → label) → ▶
**ผลที่ควรเห็น:** 768 examples · diabetes binominal: false 500 / true 268

---

## ขั้นที่ 2 · 0 → missing (Declare Missing Value)
**`Declare Missing Value`**: attribute filter type `subset` → เลือก glucose, blood_pressure, skin_thickness, insulin, bmi · **mode** = `numeric` · **numeric value** = `0` → ▶
**ผลที่ควรเห็น (Statistics → Missing):** glucose 5 · blood_pressure 35 · skin_thickness 227 · **insulin 374** · bmi 11

---

## ขั้นที่ 3 · Split Data 75 / 25
**`Split Data`**: partitions → Edit Enumeration → เพิ่ม 2 แถว ratio **0.75** และ **0.25** · sampling type `stratified sampling` · ✅ local random seed **1992**

---

## ขั้นที่ 4 · เติมค่าว่างด้วยค่าจาก train + Logistic Regression
1. partition 1 (train) → **`Replace Missing Values`** (default `average`) → **`Logistic Regression`** (tra)
   - Logistic Regression: solver `AUTO` · ✅ reproducible · ☐ use regularization · ✅ standardize · ✅ compute p-values · ✅ remove collinear columns
2. **`Apply Model`** (ตัวที่ 1): mod ← Replace Missing **pre** · unl ← partition 2 (test) → เติม test ด้วย mean ของ **train**
3. **`Apply Model`** (ตัวที่ 2): mod ← Logistic **mod** · unl ← Apply Model 1 **lab**
4. ▶ ดู ExampleSet ผลลัพธ์: มีคอลัมน์ `confidence(true)`, `confidence(false)`, `prediction(diabetes)`
5. ดูโมเดล (Logistic Regression **mod** → res): แท็บ **Coefficients** (coefficient · std. coefficient · p-value) และ **Variable Importances** — ผลจริง: **glucose 39.4%** · pregnancies 18.2% · bmi 17.9% · pedigree 11.5% · ที่เหลือน้อยมาก (insulin 0.7%) → ลำดับเดียวกับ odds ratio ใน Python

> [!warning] ⚠️ สิ่งที่ผมเจอจากการรันจริง: **prediction ของ Logistic Regression (H2O) ไม่ได้ตัดที่ 0.5**
> โมเดลบอก `default threshold: {float(dthr):.3f}` — H2O เลือก threshold ที่ทำให้ F1 สูงสุดบน train ให้เอง (AUC train = {float(auc):.3f})
> → ถ้าโจทย์บอก "threshold 0.5" ต้องใส่ **Create Threshold 0.5 + Apply Threshold** เองทุกครั้ง (ขั้นที่ 5)

---

## ขั้นที่ 5 · กำหนด threshold เอง (Create Threshold + Apply Threshold)
1. **`Multiply`** ต่อจาก Apply Model 2
2. **`Create Threshold`**: threshold **0.5** · first class `false` · second class `true` → **`Apply Threshold`** (exa ← Multiply, thr ← Create Threshold)
3. → **`Performance (Binominal Classification)`**: ✅ accuracy, precision, recall, f measure · ✅ manually set positive class = `true`
4. ทำซ้ำอีกชุดด้วย threshold **0.3** → ▶

**ผลที่ควรเห็น (test 192 คน):**

| threshold | accuracy | precision | recall | f measure |
|---|---|---|---|---|
| default ของ H2O ({float(dthr):.3f}) | {pct('p5_default','accuracy',False)} | {pct('p5_default','precision',False)} | {pct('p5_default','recall',False)} | {pct('p5_default','f_measure',False)} |
| **0.5** | {pct('p5_t050','accuracy',False)} | {pct('p5_t050','precision',False)} | {pct('p5_t050','recall',False)} | {pct('p5_t050','f_measure',False)} |
| **0.3** | {pct('p5_t030','accuracy',False)} | {pct('p5_t030','precision',False)} | {pct('p5_t030','recall',False)} | {pct('p5_t030','f_measure',False)} |

**อ่านผล:** ลด threshold 0.5 → 0.3 → recall เพิ่มจาก {pct('p5_t050','recall',False)} เป็น {pct('p5_t030','recall',False)} (หาผู้ป่วยเจอเพิ่มมาก) แลกกับ precision ที่ลดลง → งานคัดกรองเลือก 0.3

> [!note] ทำไม recall ที่ 0.5 ต่างจาก Python (0.701) — test set คนละชุด (split ต่างกัน) + RapidMiner เติมด้วย mean แทน median · ทดลองใน Python เปลี่ยน split 30 แบบ recall@0.5 แกว่งตั้งแต่ **0.45 ถึง 0.66** → hold-out ครั้งเดียวแกว่งได้มาก เหตุผลที่ควรใช้ CV
""")

# ════════════════════════════════════ P6 ══════════════════════════════════════════════════════
log6 = pd.read_csv(OUT / "p6_opt_log.csv").sort_values("depth")
best6 = log6.loc[log6.accuracy.idxmax()]
write("PR 06 Decision Tree vs Random Forest (RapidMiner).md", head(6, "Decision Tree vs Random Forest", "ทำนายโรคหัวใจ: tree โตเต็ม (train vs CV) · หา maximal depth ด้วย Optimize · เทียบ Random Forest",
    "p6_heart.csv", 40, "PR 06 Decision Tree vs Random Forest (Python)") + f"""
## ขั้นที่ 1 · อ่าน + label
`Read CSV` → **`Numerical to Binominal`** (attribute `target`, min 0 max 0 → 1 = true = เป็นโรค) → **`Set Role`** (target → label) → **`Multiply`**
**ผลที่ควรเห็น:** 303 examples · target: true 165 / false 138

---

## ขั้นที่ 2 · Tree โตเต็ม: train accuracy
1. Multiply → **`Decision Tree`**: criterion `gini_index` · maximal depth **30** · ☐ apply pruning · ☐ apply prepruning
2. **`Apply Model`**: mod ← tree · unl ← Multiply (อีกเส้น = ข้อมูลเดียวกับที่ train) → **`Performance (Binominal Classification)`** (positive class = `true`) → ▶

**ผลที่ควรเห็น:** accuracy **{pct('p6_train_full','accuracy',False)}** บนข้อมูลที่ใช้ train — จำได้หมด · ดูโมเดล → แท็บ Tree: ต้นใหญ่มาก

---

## ขั้นที่ 3 · CV ของ tree โตเต็ม vs depth 3 vs Random Forest
Cross Validation ×3: folds **10** · stratified · seed **1992** · Testing: Apply Model → Performance (Binominal, positive class `true`, main criterion `accuracy`)

| CV | Training pane |
|---|---|
| tree full | Decision Tree (depth 30, ไม่ prune) |
| tree depth 3 | Decision Tree (maximal depth **3**, ไม่ prune) |
| RF | **`Random Forest`**: number of trees **300** · criterion `gini_index` · maximal depth 10 · ✅ guess subset ratio · ✅ local random seed 1992 |

**ผลที่ควรเห็น:**

| | accuracy (CV) | recall | f measure |
|---|---|---|---|
| tree full | {pct('p6_tree_full','accuracy')} | {pct('p6_tree_full','recall',False)} | {pct('p6_tree_full','f_measure',False)} |
| tree depth 3 | {pct('p6_tree_d3','accuracy')} | {pct('p6_tree_d3','recall',False)} | {pct('p6_tree_d3','f_measure',False)} |
| **Random Forest** | **{pct('p6_rf','accuracy')}** | {pct('p6_rf','recall',False)} | {pct('p6_rf','f_measure',False)} |

→ tree โตเต็ม: train **100%** แต่ CV {pct('p6_tree_full','accuracy',False)} = **overfitting** · RF ดีที่สุด

---

## ขั้นที่ 4 · Optimize maximal depth (1–12) + Log
ครอบ CV (tree depth 3) ด้วย **`Optimize Parameters (Grid)`** → Edit Parameter Settings: `Decision Tree` → **maximal_depth** → Min 1 · Max 12 · Steps 11 · linear · ใส่ **`Log`** (depth = parameter maximal_depth · accuracy = value performance main criterion ของ CV) → `Log to Data` → ▶

**ผลที่ควรเห็น:**

| depth | """ + " | ".join(str(int(d)) for d in log6.depth) + """ |
|---|""" + "---|" * len(log6) + """
| CV acc | """ + " | ".join(f"{a:.1%}" for a in log6.accuracy) + f""" |

→ ดีที่สุดที่ **depth {int(best6.depth)}** ({best6.accuracy:.2%}) · ลึกกว่านั้น CV ลดลงแล้วคงที่ (overfit)

> [!note] RapidMiner tree (depth 3) ต่ำกว่า Python (0.79) — implementation และ folds ต่างกัน · ทิศทางเหมือนกัน: จำกัดความลึกเหมาะ ๆ ดีกว่าโตเต็ม และ RF ดีที่สุด
""")

# ════════════════════════════════════ P7 ══════════════════════════════════════════════════════
log7 = pd.read_csv(OUT / "p7_opt_log.csv").sort_values("k")
best7 = log7.loc[log7.rmse.idxmin()]
lmod = [ln.strip() for ln in (OUT / "p7_linreg_model.txt").read_text().splitlines()[1:] if ln.strip()]
lmod[0] = lmod[0].split("]: ")[-1] if "]: " in lmod[0] else lmod[0]
lmod = [re.sub(r"^\d\d\.\d\d\.\d{4} [\d:]+ ", "", x) for x in lmod]
write("PR 07 Regression (RapidMiner).md", head(7, "Regression", "ประมาณค่ารักษาพยาบาล: mean baseline vs Linear Regression vs k-NN regression บน hold-out 80/20 + หา k ด้วย CV",
    "p7_insurance.csv", 40, "PR 07 Regression (Python)") + f"""
## ขั้นที่ 1 · อ่าน + Set Role + encode
1. `Read CSV` → `Set Role` (charges → label)
2. **`Nominal to Numerical`**: coding type `dummy coding` · ✅ **use comparison groups** → comparison groups → Edit List: `sex` = `female` · `smoker` = `no` · `region` = `northeast` (= dummy แบบ k−1 · baseline ตามนี้)
3. ▶ **ผลที่ควรเห็น:** คอลัมน์ `sex = male`, `smoker = yes`, `region = northwest/southeast/southwest`

---

## ขั้นที่ 2 · Split Data 80/20
`Split Data`: ratio 0.8 / 0.2 · sampling type **`shuffled sampling`** (label เป็นตัวเลข stratified ไม่ได้) · seed **1992**
ต่อ **`Multiply`** ที่ partition 1 (train) และอีกตัวที่ partition 2 (test)

---

## ขั้นที่ 3 · Baseline + Linear Regression
| โมเดล | train | test | ตั้งค่า |
|---|---|---|---|
| baseline | `Default Model` (tra) | `Apply Model` | method = **`average`** |
| linear | `Linear Regression` (tra) | `Apply Model` | **feature selection = `none`** (default คือ M5 prime ซึ่งตัดตัวแปรเอง) |

ทั้งคู่ → **`Performance (Regression)`**: ✅ root mean squared error · ✅ absolute error · ✅ squared correlation → ▶

**ผลที่ควรเห็น:**

| | RMSE | absolute error (MAE) | squared correlation (≈ R²) |
|---|---|---|---|
| baseline | {num('p7_baseline','root_mean_squared_error')} | {num('p7_baseline','absolute_error')} | {num('p7_baseline','squared_correlation','{:.3f}')} |
| **Linear Regression** | {num('p7_linreg','root_mean_squared_error')} | {num('p7_linreg','absolute_error')} | {num('p7_linreg','squared_correlation','{:.3f}')} |

**โมเดล (แท็บ Description / Weights ของ LinearRegression):**
```text
{chr(10).join(lmod)}
```
→ **smoker = yes ≈ +24,039** ต่อปี (ตัวอื่นคงที่) · age +256/ปี · bmi +349/หน่วย — ใกล้เคียง Python (23,924 · 254 · 329)

---

## ขั้นที่ 4 · k-NN regression (normalize ด้วยค่าจาก train)
1. train → **`Normalize`** (Z) → **`k-NN`** (k = **10**, ✅ weighted vote)
2. **`Apply Model`** 1: mod ← Normalize **pre** · unl ← test → **`Apply Model`** 2: mod ← k-NN · unl ← Apply Model 1 → `Performance (Regression)` → ▶

**ผลที่ควรเห็น:** RMSE **{num('p7_knn','root_mean_squared_error')}** · MAE {num('p7_knn','absolute_error')} · squared correlation {num('p7_knn','squared_correlation','{:.3f}')} → ดีกว่า Linear

---

## ขั้นที่ 5 · หา k ด้วย CV บน train (Optimize + Log)
Optimize Parameters (Grid) ครอบ Cross Validation (folds **5**, `shuffled sampling`, seed 1992 · Training: Normalize → k-NN (weighted vote) → Group Models · Testing: Apply Model → Performance (Regression) main criterion = `root_mean_squared_error`) · k = 1…30 · Log (k, value performance main criterion)

**ผลที่ควรเห็น:** k ที่ RMSE ต่ำสุด = **{int(best7.k)}** (CV RMSE {best7.rmse:,.0f}) · k = 1 แย่มาก ({log7[log7.k == 1].rmse.iloc[0]:,.0f})
> Optimize เลือก "ค่าที่ดีที่สุด" ของ RMSE ได้ถูก เพราะ RapidMiner รู้ว่า RMSE ยิ่งน้อยยิ่งดี

> [!success] เทียบ Python: Linear RMSE 5,746 · R² 0.748 · KNN tuned RMSE 4,943 — ใกล้เคียงกัน (split เดียวกันไม่ได้ เพราะคนละเครื่องมือ)
""")

# ════════════════════════════════════ P8 ══════════════════════════════════════════════════════
el = pd.read_csv(OUT / "p8_elbow.csv").sort_values("k")
ct = pd.read_csv(OUT / "p8_crosstab.csv")
match = ct.groupby("cluster")["count(alcohol)"].max().sum() / ct["count(alcohol)"].sum()
write("PR 08 K-Means Clustering (RapidMiner).md", head(8, "K-Means Clustering", "จัดกลุ่มไวน์ 178 ขวดที่ไม่รู้สายพันธุ์: normalize → elbow ด้วย Optimize → k-Means k = 3 → ประเมิน + ตีความ centroid → เทียบสายพันธุ์จริง",
    "p8_wine_unlabeled.csv", 35, "PR 08 K-Means Clustering (Python)") + f"""
## ขั้นที่ 1 · อ่าน + กัน cultivar ไม่ให้ถูกใช้ + Normalize
`Read CSV` → **`Set Role`** (cultivar → `label`) → **`Normalize`** (Z) → `Multiply`
> k-Means ใช้เฉพาะ **regular attributes** → ตั้ง cultivar เป็น label (special) = ไม่ถูกใช้คำนวณระยะ แต่ยังอยู่ในตารางให้ตรวจทีหลัง

---

## ขั้นที่ 2 · Elbow: Optimize Parameters ครอบ k-Means
1. Multiply → **`Optimize Parameters (Grid)`** → ข้างใน: `inp` → **`k-Means`** (exa) → **`Cluster Distance Performance`** (exa ← k-Means **clu** (clustered set) · clu ← k-Means **mod** (cluster model)) · main criterion = `Avg. within centroid distance` → **`Log`** → `per`
2. Edit Parameter Settings: `k-Means` → **k** → Min 2 · Max 8 · Steps 6 · linear
3. k-Means: max runs **20** · ✅ determine good start values · ✅ local random seed **1992**
4. Log: (`k` ← k-Means parameter k) · (`avg_within` ← Cluster Distance Performance **value** `avg_within_distance`)
5. ข้างนอก: `Log to Data` → res → ▶ → Visualizations → Lines: x = k, y = avg_within

**ผลที่ควรเห็น:**

| k | """ + " | ".join(str(int(k)) for k in el.k) + """ |
|---|""" + "---|" * len(el) + """
| avg within centroid distance | """ + " | ".join(f"{v:.2f}" for v in el.avg_within) + f""" |

→ ลดมากจาก k = 2 → 3 ({el.avg_within.iloc[0]:.2f} → {el.avg_within.iloc[1]:.2f}) แล้วค่อย ๆ แบน → **elbow ที่ k = 3**

---

## ขั้นที่ 3 · k-Means k = 3 + ประเมิน
Multiply → **`k-Means`** (k **3**, max runs 20, good start values, seed 1992) → **`Cluster Distance Performance`** (main criterion `Davies Bouldin`) → ▶

**ผลที่ควรเห็น:**
- Cluster Model: Cluster 0 **62** items · Cluster 1 **65** · Cluster 2 **51**
- PerformanceVector: Avg. within centroid distance **{perf('p8_k3_perf')['Avg. within centroid distance'][0]:.3f}** · Davies Bouldin **{perf('p8_k3_perf')['Davies Bouldin'][0]:.3f}** (ติดลบเพราะ RapidMiner ถือว่ามากดี → อ่านค่าสัมบูรณ์ · ต่ำ = ดี)
- Cluster Model → **Centroid Table**: ดู z-score ของแต่ละกลุ่ม (proline, alcohol, flavanoids, color_intensity, hue) แล้วตั้งชื่อกลุ่ม · **Heat Map** ช่วยเห็นเร็ว

---

## ขั้นที่ 4 · เทียบกับสายพันธุ์จริง (Aggregate)
ต่อ Cluster Distance Performance **exa** → **`Aggregate`**: group by attributes = `cluster` และ `cultivar` (✅ include special attributes) · aggregation (`alcohol`, `count`) → ▶

**ผลที่ควรเห็น:**

| cluster | cultivar | count |
|---|---|---|
""" + "\n".join(f"| {r.cluster} | {r.cultivar} | {r['count(alcohol)']} |" for _, r in ct.iterrows()) + f"""

→ แต่ละ cluster ตรงกับสายพันธุ์เดียวเกือบทั้งหมด = **{match:.1%}** (เท่ากับ Python) · เลข cluster อาจสลับจาก Python ได้ ดูที่สมาชิก
""")

# ════════════════════════════════════ P9 ══════════════════════════════════════════════════════
rules_txt = (OUT / "p9_rules.txt").read_text()
n_shown = rules_txt.count("-->")
more = re.search(r"\.\.\. (\d+) other rules", rules_txt)
n_rules = n_shown + (int(more.group(1)) if more else 0)
n_sets = re.search(r"Frequent Item Sets \((\d+)\)", (OUT / "p9_itemsets.txt").read_text()).group(1)
write("PR 09 Association Rules (RapidMiner).md", head(9, "Association Rules", "ใบเสร็จซูเปอร์มาร์เก็ต 9,835 ใบ (ตาราง 0/1 ต่อสินค้า 169 ชนิด): FP-Growth min support 2% → Create Association Rules min confidence 30% → อ่าน support / confidence / lift",
    "p9_groceries_onehot.csv", 30, "PR 09 Association Rules (Python)") + f"""
## ขั้นที่ 1 · อ่าน + id + binominal
1. `Read CSV` → `p9_groceries_onehot.csv` (170 คอลัมน์ — อ่านช้านิดหนึ่ง)
2. **`Set Role`**: `basket_id` → **`id`** (ไม่งั้นมันกลายเป็น "สินค้า")
3. **`Numerical to Binominal`**: attribute filter type `all` · min **0** · max **0** → 0 = false · 1 = true
4. ▶ **ผลที่ควรเห็น:** 9,835 examples · 1 special (id) · 169 binominal attributes · Statistics: whole milk true **2,513** (25.6%)

---

## ขั้นที่ 2 · FP-Growth
**`FP-Growth`**: input format `items in dummy coded columns` · **positive value** = `true` · min requirement `support` · **min support = 0.02** · ☐ find min number of itemsets → port **fre** → res → ▶

**ผลที่ควรเห็น:** Frequent Itemsets — **No. of Sets: {n_sets}** (เท่ากับ Python) · คลิกหัวคอลัมน์ Support เรียง: whole milk 0.256 · other vegetables 0.193 · rolls/buns 0.184 …

---

## ขั้นที่ 3 · Create Association Rules
**`Create Association Rules`** (ต่อจาก fre): criterion `confidence` · **min confidence = 0.3** → **rul** → res → ▶

**ผลที่ควรเห็น:** AssociationRules **{n_rules} rules** (เท่ากับ Python 37) · คลิกหัวคอลัมน์ **Lift** เรียงมากไปน้อย:

| Premises | Conclusion | Support | Confidence | Lift |
|---|---|---|---|---|
| whole milk, other vegetables | root vegetables | 0.023 | 0.310 | 2.842 |
| whole milk, root vegetables | other vegetables | 0.023 | 0.474 | 2.450 |
| root vegetables | other vegetables | 0.047 | 0.435 | 2.247 |
| whipped/sour cream | other vegetables | 0.029 | 0.403 | 2.082 |
| butter | whole milk | 0.028 | 0.497 | 1.946 |

**อ่านกฎแรก:** 2.3% ของทุกตะกร้ามีนม + ผักอื่น + ผักราก · ในตะกร้าที่มีนม + ผักอื่น 31% มีผักรากด้วย · **มากกว่าปกติ 2.84 เท่า** → วางผักรากใกล้โซนผัก/นม หรือจัดโปรชุดทำอาหาร
มุมมอง **Graph** ของ AssociationRules แสดงเป็นเครือข่าย (whole milk และ other vegetables อยู่กลาง)

---

## ขั้นที่ 4 · ทดลองเปลี่ยน min support
เปลี่ยน FP-Growth min support → 0.01 และ 0.05 แล้ว ▶ ใหม่ (min confidence 0.3 เท่าเดิม)

| min support | frequent itemsets | rules |
|---|---|---|
| 0.01 | 333 | 125 |
| 0.02 | {n_sets} | {n_rules} |
| 0.05 | 31 | 3 |
(ค่าคำนวณด้วย Python ชุดเดียวกัน — FP-Growth ให้ผลเหมือน Apriori)
""")
