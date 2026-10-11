---
title: PR 06 · Decision Tree vs Random Forest (RapidMiner)
tags: [final, lab, practice, rapidminer]
---

# PR 06 · Decision Tree vs Random Forest — ไกด์ RapidMiner ทีละขั้น

> [!abstract] โจทย์ (เดียวกับไกด์ Python)
> ทำนายโรคหัวใจ: tree โตเต็ม (train vs CV) · หา maximal depth ด้วย Optimize · เทียบ Random Forest

**ข้อมูล:** `final/practice/data/p6_heart.csv` · **เวลาแนะนำ:** 40 นาที
**ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · [[PR 00 START HERE#⚙️ ทักษะพื้นฐาน RapidMiner (อ่านก่อนไกด์แรก)|ทักษะพื้นฐาน RapidMiner]] · ทำใน Python: [[PR 06 Decision Tree vs Random Forest (Python)]]
**เฉลย process:** `final/practice/rm/P06_solution.rmp` — ทำเองให้เสร็จก่อน แล้วค่อย **File → Import Process…** เปิดเทียบ (ตัวเลขทุกตัวในไกด์มาจากการรันไฟล์นี้จริง)

> [!tip] เริ่มต้น: **File → New Process → Blank** · ทำทีละขั้น กด ▶ **Run** หลังทุกขั้นที่มี "ผลที่ควรเห็น" แล้วเทียบ · ไม่ตรง → หยุดหาสาเหตุก่อน
> ตัวเลขของคุณควร **ตรงเป๊ะ** ถ้าตั้ง **local random seed = 1992** ตามไกด์ (ยกเว้นบอกไว้ว่าอาจต่างเล็กน้อย)

---

## ขั้นที่ 1 · อ่าน + label
`Read CSV` → **`Numerical to Binominal`** (attribute `target`, min 0 max 0 → 1 = true = เป็นโรค) → **`Set Role`** (target → label) → **`Multiply`**

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::new
>   n2["Numerical to Binominal"]:::new
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

**ผลที่ควรเห็น:** 303 examples · target: true 165 / false 138

---

## ขั้นที่ 2 · Tree โตเต็ม: train accuracy
1. Multiply → **`Decision Tree`**: criterion `gini_index` · maximal depth **30** · ☐ apply pruning · ☐ apply prepruning
2. **`Apply Model`**: mod ← tree · unl ← Multiply (อีกเส้น = ข้อมูลเดียวกับที่ train) → **`Performance (Binominal Classification)`** (positive class = `true`) → ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Numerical to Binominal"]:::op
>   n3["Set Role"]:::op
>   n4["Multiply"]:::op
>   n5["Decision Tree (train acc)"]:::new
>   n6["Apply Model (train acc)"]:::new
>   n7["Performance (Binominal Classification)"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → inp"| n4
>   n4 -->|"out 4 → tra"| n5
>   n5 -->|"mod → mod"| n6
>   n4 -->|"out 6 → unl"| n6
>   n6 -->|"lab → lab"| n7
>   n7 -->|"per"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:** accuracy **100.00%** บนข้อมูลที่ใช้ train — จำได้หมด · ดูโมเดล → แท็บ Tree: ต้นใหญ่มาก

---

## ขั้นที่ 3 · CV ของ tree โตเต็ม vs depth 3 vs Random Forest
Cross Validation ×3: folds **10** · stratified · seed **1992** · Testing: Apply Model → Performance (Binominal, positive class `true`, main criterion `accuracy`)

| CV | Training pane |
|---|---|
| tree full | Decision Tree (depth 30, ไม่ prune) |
| tree depth 3 | Decision Tree (maximal depth **3**, ไม่ prune) |
| RF | **`Random Forest`**: number of trees **300** · criterion `gini_index` · maximal depth 10 · ✅ guess subset ratio · ✅ local random seed 1992 |

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Numerical to Binominal"]:::op
>   n3["Set Role"]:::op
>   n4["Multiply"]:::op
>   n5[["CV tree full<br/><i>Cross Validation</i> ▣"]]:::new
>   n6[["CV tree depth 3<br/><i>Cross Validation</i> ▣"]]:::new
>   n7[["CV Random Forest<br/><i>Cross Validation</i> ▣"]]:::new
>   n8["Decision Tree (train acc)"]:::op
>   n9["Apply Model (train acc)"]:::op
>   n10["Performance (Binominal Classification)"]:::op
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → inp"| n4
>   n4 -->|"out 1 → exa"| n5
>   n5 -->|"per 1"| res(("res"))
>   n4 -->|"out 2 → exa"| n6
>   n6 -->|"per 1"| res(("res"))
>   n4 -->|"out 3 → exa"| n7
>   n7 -->|"per 1"| res(("res"))
>   n4 -->|"out 4 → tra"| n8
>   n8 -->|"mod → mod"| n9
>   n4 -->|"out 6 → unl"| n9
>   n9 -->|"lab → lab"| n10
>   n10 -->|"per"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```
>
> **ข้างใน CV tree full · Cross Validation (ดับเบิลคลิก)**
> ```mermaid
> flowchart LR
>   subgraph P0["Training"]
>     direction LR
>     n1["Decision Tree"]:::new
>     n2(["tra"]):::port
>     n2 -->|"tra"| n1
>     n3(["mod"]):::port
>     n1 -->|"mod"| n3
>   end
>   subgraph P1["Testing"]
>     direction LR
>     n4["Apply Model"]:::new
>     n5["Performance (Binominal Classification)"]:::new
>     n6(["mod"]):::port
>     n6 -->|"mod"| n4
>     n7(["tes"]):::port
>     n7 -->|"unl"| n4
>     n4 -->|"lab → lab"| n5
>     n8(["per 1"]):::port
>     n5 -->|"per"| n8
>   end
>   n3 -.->|"ส่งโมเดลไป test fold"| n6
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```
>
> **ข้างใน CV tree depth 3 · Cross Validation (ดับเบิลคลิก)**
> ```mermaid
> flowchart LR
>   subgraph P0["Training"]
>     direction LR
>     n1["Decision Tree"]:::new
>     n2(["tra"]):::port
>     n2 -->|"tra"| n1
>     n3(["mod"]):::port
>     n1 -->|"mod"| n3
>   end
>   subgraph P1["Testing"]
>     direction LR
>     n4["Apply Model"]:::new
>     n5["Performance (Binominal Classification)"]:::new
>     n6(["mod"]):::port
>     n6 -->|"mod"| n4
>     n7(["tes"]):::port
>     n7 -->|"unl"| n4
>     n4 -->|"lab → lab"| n5
>     n8(["per 1"]):::port
>     n5 -->|"per"| n8
>   end
>   n3 -.->|"ส่งโมเดลไป test fold"| n6
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```
>
> **ข้างใน CV Random Forest · Cross Validation (ดับเบิลคลิก)**
> ```mermaid
> flowchart LR
>   subgraph P0["Training"]
>     direction LR
>     n1["Random Forest"]:::new
>     n2(["tra"]):::port
>     n2 -->|"tra"| n1
>     n3(["mod"]):::port
>     n1 -->|"mod"| n3
>   end
>   subgraph P1["Testing"]
>     direction LR
>     n4["Apply Model"]:::new
>     n5["Performance (Binominal Classification)"]:::new
>     n6(["mod"]):::port
>     n6 -->|"mod"| n4
>     n7(["tes"]):::port
>     n7 -->|"unl"| n4
>     n4 -->|"lab → lab"| n5
>     n8(["per 1"]):::port
>     n5 -->|"per"| n8
>   end
>   n3 -.->|"ส่งโมเดลไป test fold"| n6
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:**

| | accuracy (CV) | recall | f measure |
|---|---|---|---|
| tree full | 76.87% +/- 9.84% | 78.01% | 78.47% |
| tree depth 3 | 73.24% +/- 8.37% | 83.36% | 76.69% |
| **Random Forest** | **82.18% +/- 8.65%** | 86.72% | 84.10% |

→ tree โตเต็ม: train **100%** แต่ CV 76.87% = **overfitting** · RF ดีที่สุด

---

## ขั้นที่ 4 · Optimize maximal depth (1–12) + Log
ครอบ CV (tree depth 3) ด้วย **`Optimize Parameters (Grid)`** → Edit Parameter Settings: `Decision Tree` → **maximal_depth** → Min 1 · Max 12 · Steps 11 · linear · ใส่ **`Log`** (depth = parameter maximal_depth · accuracy = value performance main criterion ของ CV) → `Log to Data` → ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Numerical to Binominal"]:::op
>   n3["Set Role"]:::op
>   n4["Multiply"]:::op
>   n5[["CV tree full<br/><i>Cross Validation</i> ▣"]]:::sub
>   n6[["CV tree depth 3<br/><i>Cross Validation</i> ▣"]]:::sub
>   n7[["CV Random Forest<br/><i>Cross Validation</i> ▣"]]:::sub
>   n8["Decision Tree (train acc)"]:::op
>   n9["Apply Model (train acc)"]:::op
>   n10["Performance (Binominal Classification)"]:::op
>   n11[["Optimize Parameters (Grid) ▣"]]:::new
>   n12["Log to Data"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → inp"| n4
>   n4 -->|"out 1 → exa"| n5
>   n5 -->|"per 1"| res(("res"))
>   n4 -->|"out 2 → exa"| n6
>   n6 -->|"per 1"| res(("res"))
>   n4 -->|"out 3 → exa"| n7
>   n7 -->|"per 1"| res(("res"))
>   n4 -->|"out 4 → tra"| n8
>   n8 -->|"mod → mod"| n9
>   n4 -->|"out 6 → unl"| n9
>   n9 -->|"lab → lab"| n10
>   n10 -->|"per"| res(("res"))
>   n4 -->|"out 5 → inp 1"| n11
>   n12 -->|"exa"| res(("res"))
>   n11 -->|"per"| res(("res"))
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
>     n1[["CV tree (copy)<br/><i>Cross Validation</i> ▣"]]:::new
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
> **ข้างใน CV tree (copy) · Cross Validation (ดับเบิลคลิก)**
> ```mermaid
> flowchart LR
>   subgraph P0["Training"]
>     direction LR
>     n1["Decision Tree"]:::new
>     n2(["tra"]):::port
>     n2 -->|"tra"| n1
>     n3(["mod"]):::port
>     n1 -->|"mod"| n3
>   end
>   subgraph P1["Testing"]
>     direction LR
>     n4["Apply Model"]:::new
>     n5["Performance (Binominal Classification)"]:::new
>     n6(["mod"]):::port
>     n6 -->|"mod"| n4
>     n7(["tes"]):::port
>     n7 -->|"unl"| n4
>     n4 -->|"lab → lab"| n5
>     n8(["per 1"]):::port
>     n5 -->|"per"| n8
>   end
>   n3 -.->|"ส่งโมเดลไป test fold"| n6
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:**

| depth | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CV acc | 54.5% | 72.6% | 73.3% | 82.2% | 76.2% | 78.9% | 78.2% | 76.6% | 76.6% | 76.9% | 76.9% | 76.9% |

→ ดีที่สุดที่ **depth 4** (82.18%) · ลึกกว่านั้น CV ลดลงแล้วคงที่ (overfit)

> [!note] RapidMiner tree (depth 3) ต่ำกว่า Python (0.79) — implementation และ folds ต่างกัน · ทิศทางเหมือนกัน: จำกัดความลึกเหมาะ ๆ ดีกว่าโตเต็ม และ RF ดีที่สุด
