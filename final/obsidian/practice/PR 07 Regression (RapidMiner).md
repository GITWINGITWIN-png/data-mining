---
title: PR 07 · Regression (RapidMiner)
tags: [final, lab, practice, rapidminer]
---

# PR 07 · Regression — ไกด์ RapidMiner ทีละขั้น

> [!abstract] โจทย์ (เดียวกับไกด์ Python)
> ประมาณค่ารักษาพยาบาล: mean baseline vs Linear Regression vs k-NN regression บน hold-out 80/20 + หา k ด้วย CV

**ข้อมูล:** `final/practice/data/p7_insurance.csv` · **เวลาแนะนำ:** 40 นาที
**ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · [[PR 00 START HERE#⚙️ ทักษะพื้นฐาน RapidMiner (อ่านก่อนไกด์แรก)|ทักษะพื้นฐาน RapidMiner]] · ทำใน Python: [[PR 07 Regression (Python)]]
**เฉลย process:** `final/practice/rm/P07_solution.rmp` — ทำเองให้เสร็จก่อน แล้วค่อย **File → Import Process…** เปิดเทียบ (ตัวเลขทุกตัวในไกด์มาจากการรันไฟล์นี้จริง)

> [!tip] เริ่มต้น: **File → New Process → Blank** · ทำทีละขั้น กด ▶ **Run** หลังทุกขั้นที่มี "ผลที่ควรเห็น" แล้วเทียบ · ไม่ตรง → หยุดหาสาเหตุก่อน
> ตัวเลขของคุณควร **ตรงเป๊ะ** ถ้าตั้ง **local random seed = 1992** ตามไกด์ (ยกเว้นบอกไว้ว่าอาจต่างเล็กน้อย)

---

## ขั้นที่ 1 · อ่าน + Set Role + encode
1. `Read CSV` → `Set Role` (charges → label)
2. **`Nominal to Numerical`**: coding type `dummy coding` · ✅ **use comparison groups** → comparison groups → Edit List: `sex` = `female` · `smoker` = `no` · `region` = `northeast` (= dummy แบบ k−1 · baseline ตามนี้)
3. ▶ **ผลที่ควรเห็น:** คอลัมน์ `sex = male`, `smoker = yes`, `region = northwest/southeast/southwest`

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::new
>   n2["Set Role"]:::new
>   n3["Nominal to Numerical"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -.->|"exa"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```


---

## ขั้นที่ 2 · Split Data 80/20
`Split Data`: ratio 0.8 / 0.2 · sampling type **`shuffled sampling`** (label เป็นตัวเลข stratified ไม่ได้) · seed **1992**
ต่อ **`Multiply`** ที่ partition 1 (train) และอีกตัวที่ partition 2 (test)

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Set Role"]:::op
>   n3["Nominal to Numerical"]:::op
>   n4["Split Data"]:::new
>   n5["Multiply (train)"]:::new
>   n6["Multiply (test)"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → exa"| n4
>   n4 -->|"par 1 → inp"| n5
>   n4 -->|"par 2 → inp"| n6
>   n5 -.->|"out 1"| res(("res"))
>   n6 -.->|"out 1"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```


---

## ขั้นที่ 3 · Baseline + Linear Regression
| โมเดล | train | test | ตั้งค่า |
|---|---|---|---|
| baseline | `Default Model` (tra) | `Apply Model` | method = **`average`** |
| linear | `Linear Regression` (tra) | `Apply Model` | **feature selection = `none`** (default คือ M5 prime ซึ่งตัดตัวแปรเอง) |

ทั้งคู่ → **`Performance (Regression)`**: ✅ root mean squared error · ✅ absolute error · ✅ squared correlation → ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Set Role"]:::op
>   n3["Nominal to Numerical"]:::op
>   n4["Split Data"]:::op
>   n5["Multiply (train)"]:::op
>   n6["Multiply (test)"]:::op
>   n7["Default Model"]:::new
>   n8["Apply Model"]:::new
>   n9["Performance (Regression)"]:::new
>   n10["Linear Regression"]:::new
>   n11["Apply Model"]:::new
>   n12["Performance (Regression)"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → exa"| n4
>   n4 -->|"par 1 → inp"| n5
>   n4 -->|"par 2 → inp"| n6
>   n5 -->|"out 1 → tra"| n7
>   n7 -->|"mod → mod"| n8
>   n6 -->|"out 1 → unl"| n8
>   n8 -->|"lab → lab"| n9
>   n9 -->|"per"| res(("res"))
>   n5 -->|"out 2 → tra"| n10
>   n10 -->|"mod → mod"| n11
>   n6 -->|"out 2 → unl"| n11
>   n11 -->|"lab → lab"| n12
>   n12 -->|"per"| res(("res"))
>   n11 -->|"mod"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:**

| | RMSE | absolute error (MAE) | squared correlation (≈ R²) |
|---|---|---|---|
| baseline | 11,309.7 | 8,652.8 | 0.000 |
| **Linear Regression** | 5,743.1 | 4,099.0 | 0.742 |

**โมเดล (แท็บ Description / Weights ของ LinearRegression):**
```text
- 276.452 * sex = male
+ 24038.867 * smoker = yes
- 856.469 * region = southwest
- 1183.450 * region = southeast
- 461.414 * region = northwest
+ 255.972 * age
+ 348.976 * bmi
+ 457.374 * children
- 11972.799
```
→ **smoker = yes ≈ +24,039** ต่อปี (ตัวอื่นคงที่) · age +256/ปี · bmi +349/หน่วย — ใกล้เคียง Python (23,924 · 254 · 329)

---

## ขั้นที่ 4 · k-NN regression (normalize ด้วยค่าจาก train)
1. train → **`Normalize`** (Z) → **`k-NN`** (k = **10**, ✅ weighted vote)
2. **`Apply Model`** 1: mod ← Normalize **pre** · unl ← test → **`Apply Model`** 2: mod ← k-NN · unl ← Apply Model 1 → `Performance (Regression)` → ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Set Role"]:::op
>   n3["Nominal to Numerical"]:::op
>   n4["Split Data"]:::op
>   n5["Multiply (train)"]:::op
>   n6["Multiply (test)"]:::op
>   n7["Default Model"]:::op
>   n8["Apply Model"]:::op
>   n9["Performance (Regression)"]:::op
>   n10["Linear Regression"]:::op
>   n11["Apply Model"]:::op
>   n12["Performance (Regression)"]:::op
>   n13["Normalize"]:::new
>   n14["k-NN"]:::new
>   n15["Apply Model 1 (normalize test)"]:::new
>   n16["Apply Model 2"]:::new
>   n17["Performance (Regression)"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → exa"| n4
>   n4 -->|"par 1 → inp"| n5
>   n4 -->|"par 2 → inp"| n6
>   n5 -->|"out 1 → tra"| n7
>   n7 -->|"mod → mod"| n8
>   n6 -->|"out 1 → unl"| n8
>   n8 -->|"lab → lab"| n9
>   n9 -->|"per"| res(("res"))
>   n5 -->|"out 2 → tra"| n10
>   n10 -->|"mod → mod"| n11
>   n6 -->|"out 2 → unl"| n11
>   n11 -->|"lab → lab"| n12
>   n12 -->|"per"| res(("res"))
>   n11 -->|"mod"| res(("res"))
>   n5 -->|"out 3 → exa"| n13
>   n13 -->|"exa → tra"| n14
>   n13 -->|"pre → mod"| n15
>   n6 -->|"out 3 → unl"| n15
>   n14 -->|"mod → mod"| n16
>   n15 -->|"lab → unl"| n16
>   n16 -->|"lab → lab"| n17
>   n17 -->|"per"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:** RMSE **4,797.3** · MAE 3,052.3 · squared correlation 0.817 → ดีกว่า Linear

---

## ขั้นที่ 5 · หา k ด้วย CV บน train (Optimize + Log)
Optimize Parameters (Grid) ครอบ Cross Validation (folds **5**, `shuffled sampling`, seed 1992 · Training: Normalize → k-NN (weighted vote) → Group Models · Testing: Apply Model → Performance (Regression) main criterion = `root_mean_squared_error`) · k = 1…30 · Log (k, value performance main criterion)

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Set Role"]:::op
>   n3["Nominal to Numerical"]:::op
>   n4["Split Data"]:::op
>   n5["Multiply (train)"]:::op
>   n6["Multiply (test)"]:::op
>   n7["Default Model"]:::op
>   n8["Apply Model"]:::op
>   n9["Performance (Regression)"]:::op
>   n10["Linear Regression"]:::op
>   n11["Apply Model"]:::op
>   n12["Performance (Regression)"]:::op
>   n13["Normalize"]:::op
>   n14["k-NN"]:::op
>   n15["Apply Model 1 (normalize test)"]:::op
>   n16["Apply Model 2"]:::op
>   n17["Performance (Regression)"]:::op
>   n18[["Optimize Parameters (Grid) ▣"]]:::new
>   n19["Log to Data"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → exa"| n4
>   n4 -->|"par 1 → inp"| n5
>   n4 -->|"par 2 → inp"| n6
>   n5 -->|"out 1 → tra"| n7
>   n7 -->|"mod → mod"| n8
>   n6 -->|"out 1 → unl"| n8
>   n8 -->|"lab → lab"| n9
>   n9 -->|"per"| res(("res"))
>   n5 -->|"out 2 → tra"| n10
>   n10 -->|"mod → mod"| n11
>   n6 -->|"out 2 → unl"| n11
>   n11 -->|"lab → lab"| n12
>   n12 -->|"per"| res(("res"))
>   n11 -->|"mod"| res(("res"))
>   n5 -->|"out 3 → exa"| n13
>   n13 -->|"exa → tra"| n14
>   n13 -->|"pre → mod"| n15
>   n6 -->|"out 3 → unl"| n15
>   n14 -->|"mod → mod"| n16
>   n15 -->|"lab → unl"| n16
>   n16 -->|"lab → lab"| n17
>   n17 -->|"per"| res(("res"))
>   n5 -->|"out 4 → inp 1"| n18
>   n19 -->|"exa"| res(("res"))
>   n18 -->|"per"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```
>
> **ข้างใน Optimize Parameters (Grid) (ดับเบิลคลิก)**
> ```mermaid
> flowchart LR
>   subgraph P0["ข้างใน"]
>     direction LR
>     n1[["Cross Validation ▣"]]:::new
>     n2["Log"]:::new
>     n3(["inp 1"]):::port
>     n3 -->|"exa"| n1
>     n1 -->|"per 1 → thr 1"| n2
>     n4(["per"]):::port
>     n2 -->|"thr 1"| n4
>   end
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
>     n1["Normalize"]:::new
>     n2["k-NN"]:::new
>     n3["Group Models"]:::new
>     n4(["tra"]):::port
>     n4 -->|"exa"| n1
>     n1 -->|"exa → tra"| n2
>     n1 -->|"pre → mod 1"| n3
>     n2 -->|"mod → mod 2"| n3
>     n5(["mod"]):::port
>     n3 -->|"mod"| n5
>   end
>   subgraph P1["Testing"]
>     direction LR
>     n6["Apply Model"]:::new
>     n7["Performance (Regression)"]:::new
>     n8(["mod"]):::port
>     n8 -->|"mod"| n6
>     n9(["tes"]):::port
>     n9 -->|"unl"| n6
>     n6 -->|"lab → lab"| n7
>     n10(["per 1"]):::port
>     n7 -->|"per"| n10
>   end
>   n5 -.->|"ส่งโมเดลไป test fold"| n8
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:** k ที่ RMSE ต่ำสุด = **3** (CV RMSE 5,681) · k = 1 แย่มาก (18,331)
> Optimize เลือก "ค่าที่ดีที่สุด" ของ RMSE ได้ถูก เพราะ RapidMiner รู้ว่า RMSE ยิ่งน้อยยิ่งดี

> [!success] เทียบ Python: Linear RMSE 5,746 · R² 0.748 · KNN tuned RMSE 4,943 — ใกล้เคียงกัน (split เดียวกันไม่ได้ เพราะคนละเครื่องมือ)
