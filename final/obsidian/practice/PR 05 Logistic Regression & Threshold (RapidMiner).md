---
title: PR 05 · Logistic Regression & Threshold (RapidMiner)
tags: [final, lab, practice, rapidminer]
---

# PR 05 · Logistic Regression & Threshold — ไกด์ RapidMiner ทีละขั้น

> [!abstract] โจทย์ (เดียวกับไกด์ Python)
> คัดกรองเบาหวาน: แปลง 0 ที่เป็นไปไม่ได้เป็นค่าว่าง → split 75/25 → เติมค่าว่างด้วยค่าจาก train → Logistic Regression → เทียบ threshold 0.5 กับ 0.3

**ข้อมูล:** `final/practice/data/p5_pima_diabetes.csv` · **เวลาแนะนำ:** 40 นาที
**ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · [[PR 00 START HERE#⚙️ ทักษะพื้นฐาน RapidMiner (อ่านก่อนไกด์แรก)|ทักษะพื้นฐาน RapidMiner]] · ทำใน Python: [[PR 05 Logistic Regression & Threshold (Python)]]
**เฉลย process:** `final/practice/rm/P05_solution.rmp` — ทำเองให้เสร็จก่อน แล้วค่อย **File → Import Process…** เปิดเทียบ (ตัวเลขทุกตัวในไกด์มาจากการรันไฟล์นี้จริง)

> [!tip] เริ่มต้น: **File → New Process → Blank** · ทำทีละขั้น กด ▶ **Run** หลังทุกขั้นที่มี "ผลที่ควรเห็น" แล้วเทียบ · ไม่ตรง → หยุดหาสาเหตุก่อน
> ตัวเลขของคุณควร **ตรงเป๊ะ** ถ้าตั้ง **local random seed = 1992** ตามไกด์ (ยกเว้นบอกไว้ว่าอาจต่างเล็กน้อย)

---

## ขั้นที่ 1 · อ่าน + เตรียม label
`Read CSV` → **`Numerical to Binominal`** (attribute filter type `single` · attribute `diabetes` · min 0 · max 0 → 0 = false, 1 = true) → **`Set Role`** (diabetes → label) → ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::new
>   n2["Numerical to Binominal"]:::new
>   n3["Set Role"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -.->|"exa"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:** 768 examples · diabetes binominal: false 500 / true 268

---

## ขั้นที่ 2 · 0 → missing (Declare Missing Value)
**`Declare Missing Value`**: attribute filter type `subset` → เลือก glucose, blood_pressure, skin_thickness, insulin, bmi · **mode** = `numeric` · **numeric value** = `0` → ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Numerical to Binominal"]:::op
>   n3["Set Role"]:::op
>   n4["Declare Missing Value"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → exa"| n4
>   n4 -.->|"exa"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น (Statistics → Missing):** glucose 5 · blood_pressure 35 · skin_thickness 227 · **insulin 374** · bmi 11

---

## ขั้นที่ 3 · Split Data 75 / 25
**`Split Data`**: partitions → Edit Enumeration → เพิ่ม 2 แถว ratio **0.75** และ **0.25** · sampling type `stratified sampling` · ✅ local random seed **1992**

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Numerical to Binominal"]:::op
>   n3["Set Role"]:::op
>   n4["Declare Missing Value"]:::op
>   n5["Split Data"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → exa"| n4
>   n4 -->|"exa → exa"| n5
>   n5 -.->|"par 1"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```


---

## ขั้นที่ 4 · เติมค่าว่างด้วยค่าจาก train + Logistic Regression
1. partition 1 (train) → **`Replace Missing Values`** (default `average`) → **`Logistic Regression`** (tra)
   - Logistic Regression: solver `AUTO` · ✅ reproducible · ☐ use regularization · ✅ standardize · ✅ compute p-values · ✅ remove collinear columns
2. **`Apply Model`** (ตัวที่ 1): mod ← Replace Missing **pre** · unl ← partition 2 (test) → เติม test ด้วย mean ของ **train**
3. **`Apply Model`** (ตัวที่ 2): mod ← Logistic **mod** · unl ← Apply Model 1 **lab**
4. ▶ ดู ExampleSet ผลลัพธ์: มีคอลัมน์ `confidence(true)`, `confidence(false)`, `prediction(diabetes)`
5. ดูโมเดล (Logistic Regression **mod** → res): แท็บ **Coefficients** (coefficient · std. coefficient · p-value) และ **Variable Importances** — ผลจริง: **glucose 39.4%** · pregnancies 18.2% · bmi 17.9% · pedigree 11.5% · ที่เหลือน้อยมาก (insulin 0.7%) → ลำดับเดียวกับ odds ratio ใน Python

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Numerical to Binominal"]:::op
>   n3["Set Role"]:::op
>   n4["Declare Missing Value"]:::op
>   n5["Split Data"]:::op
>   n6["Replace Missing Values"]:::new
>   n7["Logistic Regression"]:::new
>   n8["Apply Model 1 (เติม test)"]:::new
>   n9["Apply Model 2"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → exa"| n4
>   n4 -->|"exa → exa"| n5
>   n5 -->|"par 1 → exa"| n6
>   n6 -->|"exa → tra"| n7
>   n6 -->|"pre → mod"| n8
>   n5 -->|"par 2 → unl"| n8
>   n7 -->|"mod → mod"| n9
>   n8 -->|"lab → unl"| n9
>   n9 -->|"mod"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

> [!warning] ⚠️ สิ่งที่ผมเจอจากการรันจริง: **prediction ของ Logistic Regression (H2O) ไม่ได้ตัดที่ 0.5**
> โมเดลบอก `default threshold: 0.314` — H2O เลือก threshold ที่ทำให้ F1 สูงสุดบน train ให้เอง (AUC train = 0.846)
> → ถ้าโจทย์บอก "threshold 0.5" ต้องใส่ **Create Threshold 0.5 + Apply Threshold** เองทุกครั้ง (ขั้นที่ 5)

---

## ขั้นที่ 5 · กำหนด threshold เอง (Create Threshold + Apply Threshold)
1. **`Multiply`** ต่อจาก Apply Model 2
2. **`Create Threshold`**: threshold **0.5** · first class `false` · second class `true` → **`Apply Threshold`** (exa ← Multiply, thr ← Create Threshold)
3. → **`Performance (Binominal Classification)`**: ✅ accuracy, precision, recall, f measure · ✅ manually set positive class = `true`
4. ทำซ้ำอีกชุดด้วย threshold **0.3** → ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Numerical to Binominal"]:::op
>   n3["Set Role"]:::op
>   n4["Declare Missing Value"]:::op
>   n5["Split Data"]:::op
>   n6["Replace Missing Values"]:::op
>   n7["Logistic Regression"]:::op
>   n8["Apply Model 1 (เติม test)"]:::op
>   n9["Apply Model 2"]:::op
>   n10["Multiply"]:::new
>   n11["Performance (threshold อัตโนมัติ)<br/><i>Performance (Binominal Classification)</i>"]:::new
>   n12["Create Threshold 0.5"]:::new
>   n13["Apply Threshold 0.5"]:::new
>   n14["Performance (0.5)<br/><i>Performance (Binominal Classification)</i>"]:::new
>   n15["Create Threshold 0.3"]:::new
>   n16["Apply Threshold 0.3"]:::new
>   n17["Performance (0.3)<br/><i>Performance (Binominal Classification)</i>"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → exa"| n4
>   n4 -->|"exa → exa"| n5
>   n5 -->|"par 1 → exa"| n6
>   n6 -->|"exa → tra"| n7
>   n6 -->|"pre → mod"| n8
>   n5 -->|"par 2 → unl"| n8
>   n7 -->|"mod → mod"| n9
>   n8 -->|"lab → unl"| n9
>   n9 -->|"lab → inp"| n10
>   n10 -->|"out 1 → lab"| n11
>   n11 -->|"per"| res(("res"))
>   n10 -->|"out 2 → exa"| n13
>   n12 -->|"out → thr"| n13
>   n13 -->|"exa → lab"| n14
>   n14 -->|"per"| res(("res"))
>   n10 -->|"out 3 → exa"| n16
>   n15 -->|"out → thr"| n16
>   n16 -->|"exa → lab"| n17
>   n17 -->|"per"| res(("res"))
>   n9 -->|"mod"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น (test 192 คน):**

| threshold | accuracy | precision | recall | f measure |
|---|---|---|---|---|
| default ของ H2O (0.314) | 77.60% | 63.95% | 82.09% | 71.90% |
| **0.5** | 73.96% | 68.09% | 47.76% | 56.14% |
| **0.3** | 76.04% | 61.80% | 82.09% | 70.51% |

**อ่านผล:** ลด threshold 0.5 → 0.3 → recall เพิ่มจาก 47.76% เป็น 82.09% (หาผู้ป่วยเจอเพิ่มมาก) แลกกับ precision ที่ลดลง → งานคัดกรองเลือก 0.3

> [!note] ทำไม recall ที่ 0.5 ต่างจาก Python (0.701) — test set คนละชุด (split ต่างกัน) + RapidMiner เติมด้วย mean แทน median · ทดลองใน Python เปลี่ยน split 30 แบบ recall@0.5 แกว่งตั้งแต่ **0.45 ถึง 0.66** → hold-out ครั้งเดียวแกว่งได้มาก เหตุผลที่ควรใช้ CV
