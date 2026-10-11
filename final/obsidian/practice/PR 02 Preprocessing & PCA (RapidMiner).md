---
title: PR 02 · Preprocessing & PCA (RapidMiner)
tags: [final, lab, practice, rapidminer]
---

# PR 02 · Preprocessing & PCA — ไกด์ RapidMiner ทีละขั้น

> [!abstract] โจทย์ (เดียวกับไกด์ Python)
> เตรียมข้อมูลนกเพนกวิน (มีค่าว่าง, categorical, หน่วยต่างกัน) ให้ k-NN ทำนายสายพันธุ์โดยไม่ leak · discretize น้ำหนัก · PCA 2 มิติ

**ข้อมูล:** `final/practice/data/p2_penguins.csv` · **เวลาแนะนำ:** 45 นาที
**ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · [[PR 00 START HERE#⚙️ ทักษะพื้นฐาน RapidMiner (อ่านก่อนไกด์แรก)|ทักษะพื้นฐาน RapidMiner]] · ทำใน Python: [[PR 02 Preprocessing & PCA (Python)]]
**เฉลย process:** `final/practice/rm/P02_solution.rmp` — ทำเองให้เสร็จก่อน แล้วค่อย **File → Import Process…** เปิดเทียบ (ตัวเลขทุกตัวในไกด์มาจากการรันไฟล์นี้จริง)

> [!tip] เริ่มต้น: **File → New Process → Blank** · ทำทีละขั้น กด ▶ **Run** หลังทุกขั้นที่มี "ผลที่ควรเห็น" แล้วเทียบ · ไม่ตรง → หยุดหาสาเหตุก่อน
> ตัวเลขของคุณควร **ตรงเป๊ะ** ถ้าตั้ง **local random seed = 1992** ตามไกด์ (ยกเว้นบอกไว้ว่าอาจต่างเล็กน้อย)

---

## ขั้นที่ 1 · อ่านไฟล์ + ดูค่าว่าง
`Read CSV` → `p2_penguins.csv` → res → ▶ → แท็บ **Statistics**

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::new
>   n1 -.->|"out"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:** **344 examples** · ตัวเลข 4 คอลัมน์ Missing = **2** · `sex` Missing = **11** · species / island / sex เป็น polynominal

---

## ขั้นที่ 2 · ตัดแถวที่ไม่มีการวัด (Filter Examples)
`Filter Examples` → condition class `custom_filters` → Add Filters: `body_mass_g` · **is not missing** → ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Filter Examples"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -.->|"exa"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:** **342 examples** (การตัดแถวที่ว่างทั้งแถวไม่ได้ "เรียนค่า" จึงทำนอก CV ได้)

---

## ขั้นที่ 3 · Set Role
`Set Role`: attribute name = `species` · target role = `label` → ▶ → ExampleSet บอก **1 special attribute** (คอลัมน์ species เปลี่ยนสี)
ต่อ **`Multiply`** ต่อท้าย (จะใช้ 3 ทาง)

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Filter Examples"]:::op
>   n3["Set Role"]:::new
>   n4["Multiply"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → inp"| n4
>   n4 -.->|"out 1"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```


---

## ขั้นที่ 4 · Discretize น้ำหนักเป็น 3 ช่วงจำนวนเท่ากัน
1. Multiply **output 2** → **`Discretize by Frequency`**: attribute filter type `single` · attribute `body_mass_g` · **number of bins** = 3 · range name type `short`
2. ต่อ **`Aggregate`**: group by attributes = `body_mass_g` และ `species` (กด Select Attributes… → ✅ include special attributes ถ้ามองไม่เห็น species) · aggregation: (`island`, `count`) → ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Filter Examples"]:::op
>   n3["Set Role"]:::op
>   n4["Multiply"]:::op
>   n5["Discretize by Frequency"]:::new
>   n6["Aggregate"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → inp"| n4
>   n4 -->|"out 2 → exa"| n5
>   n5 -->|"exa → exa"| n6
>   n6 -->|"exa"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:**

| body_mass_g | species | count |
|---|---|---|
| range1 | Adelie | 81 |
| range1 | Chinstrap | 36 |
| range2 | Adelie | 63 |
| range2 | Chinstrap | 31 |
| range2 | Gentoo | 18 |
| range3 | Adelie | 7 |
| range3 | Chinstrap | 1 |
| range3 | Gentoo | 105 |

→ ช่วงหนักสุด (range3) เป็น Gentoo เกือบทั้งหมด

---

## ขั้นที่ 5 · PCA 2 มิติ (Select Attributes → Normalize → PCA)
1. Multiply **output 1** → **`Select Attributes`**: attribute filter type = `value_type` · value type = `numeric` (เหลือตัวเลข 4 ตัว + label)
2. → **`Normalize`**: method = `Z-transformation` (**ต้อง normalize ก่อน PCA**)
3. → **`Principal Component Analysis`**: dimensionality reduction = `fixed number` · number of components = `2`
4. port **exa** → res · port **pre** (PCA model) → res → ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Filter Examples"]:::op
>   n3["Set Role"]:::op
>   n4["Multiply"]:::op
>   n5["Select Attributes"]:::new
>   n6["Normalize"]:::new
>   n7["PCA<br/><i>Principal Component Analysis</i>"]:::new
>   n8["Discretize by Frequency"]:::op
>   n9["Aggregate"]:::op
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → inp"| n4
>   n4 -->|"out 1 → exa"| n5
>   n5 -->|"exa → exa"| n6
>   n6 -->|"exa → exa"| n7
>   n7 -->|"exa"| res(("res"))
>   n7 -->|"pre"| res(("res"))
>   n4 -->|"out 2 → exa"| n8
>   n8 -->|"exa → exa"| n9
>   n9 -->|"exa"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:**
- PCA model → แท็บ **Eigenvalues**: PC1 Proportion of Variance ≈ **0.688** · PC2 ≈ **0.193** · Cumulative ≈ **0.882**
- แท็บ **Eigenvectors** (loadings):
  - `PC 1: + 0.455 * bill_length_mm - 0.400 * bill_depth_mm + 0.576 * flipper_length_mm + 0.548 * body_mass_g`
  - `PC 2: - 0.597 * bill_length_mm - 0.798 * bill_depth_mm - 0.002 * flipper_length_mm - 0.084 * body_mass_g`
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

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Filter Examples"]:::op
>   n3["Set Role"]:::op
>   n4["Multiply"]:::op
>   n5["Select Attributes"]:::op
>   n6["Normalize"]:::op
>   n7["PCA<br/><i>Principal Component Analysis</i>"]:::op
>   n8["Discretize by Frequency"]:::op
>   n9["Aggregate"]:::op
>   n10[["Cross Validation ▣"]]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → inp"| n4
>   n4 -->|"out 1 → exa"| n5
>   n5 -->|"exa → exa"| n6
>   n6 -->|"exa → exa"| n7
>   n7 -->|"exa"| res(("res"))
>   n7 -->|"pre"| res(("res"))
>   n4 -->|"out 2 → exa"| n8
>   n8 -->|"exa → exa"| n9
>   n9 -->|"exa"| res(("res"))
>   n4 -->|"out 3 → exa"| n10
>   n10 -->|"per 1"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```
>
> **ข้างใน Cross Validation (ดับเบิลคลิก)**
> ```mermaid
> flowchart LR
>   subgraph P0["Training"]
>     direction LR
>     n1["Replace Missing Values"]:::new
>     n2["Nominal to Numerical"]:::new
>     n3["Normalize"]:::new
>     n4["k-NN"]:::new
>     n5["Group Models"]:::new
>     n6(["tra"]):::port
>     n6 -->|"exa"| n1
>     n1 -->|"exa → exa"| n2
>     n2 -->|"exa → exa"| n3
>     n3 -->|"exa → tra"| n4
>     n1 -->|"pre → mod 1"| n5
>     n2 -->|"pre → mod 2"| n5
>     n3 -->|"pre → mod 3"| n5
>     n4 -->|"mod → mod 4"| n5
>     n7(["mod"]):::port
>     n5 -->|"mod"| n7
>   end
>   subgraph P1["Testing"]
>     direction LR
>     n8["Apply Model"]:::new
>     n9["Performance (Classification)"]:::new
>     n10(["mod"]):::port
>     n10 -->|"mod"| n8
>     n11(["tes"]):::port
>     n11 -->|"unl"| n8
>     n8 -->|"lab → lab"| n9
>     n12(["per 1"]):::port
>     n9 -->|"per"| n12
>   end
>   n7 -.->|"ส่งโมเดลไป test fold"| n10
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:** accuracy **99.71% +/- 0.65%**
**ทดลองเพิ่ม:** ลบ `Normalize` ออกจาก Training pane (เหลือ group models 2 ตัว) → accuracy เหลือ **75.72% +/- 4.04%** → scaling สำคัญมากกับ k-NN

> [!warning] ทำไมต้องอยู่ใน Training pane — Replace Missing / Normalize "เรียนค่า" (mean, std) จากข้อมูล ถ้าวางนอก CV ค่าจะรวม test fold = leakage · Group Models ส่งค่าที่เรียนจาก training fold ไปใช้กับ test fold

> [!success] เทียบ Python: Python ได้ CV 0.9890 (sklearn ใช้ median และ split คนละแบบ — ต่างกันเล็กน้อยได้)
