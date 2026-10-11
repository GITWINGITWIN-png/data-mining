---
title: PR 03 · Imbalanced & SMOTE (RapidMiner)
tags: [final, lab, practice, rapidminer]
---

# PR 03 · Imbalanced & SMOTE — ไกด์ RapidMiner ทีละขั้น

> [!abstract] โจทย์ (เดียวกับไกด์ Python)
> ผลชิ้นเนื้อ 397 ราย มีมะเร็ง 40 ราย เปรียบเทียบ baseline / tree / tree + undersampling / tree + SMOTE ใน 5-fold CV โดย resample **เฉพาะ training fold** และวัดด้วย recall/F1 ของ malignant

**ข้อมูล:** `final/practice/data/p3_breast_cancer_imbalanced.csv` · **เวลาแนะนำ:** 35 นาที
**ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · [[PR 00 START HERE#⚙️ ทักษะพื้นฐาน RapidMiner (อ่านก่อนไกด์แรก)|ทักษะพื้นฐาน RapidMiner]] · ทำใน Python: [[PR 03 Imbalanced & SMOTE (Python)]]
**เฉลย process:** `final/practice/rm/P03_solution.rmp` — ทำเองให้เสร็จก่อน แล้วค่อย **File → Import Process…** เปิดเทียบ (ตัวเลขทุกตัวในไกด์มาจากการรันไฟล์นี้จริง)

> [!tip] เริ่มต้น: **File → New Process → Blank** · ทำทีละขั้น กด ▶ **Run** หลังทุกขั้นที่มี "ผลที่ควรเห็น" แล้วเทียบ · ไม่ตรง → หยุดหาสาเหตุก่อน
> ตัวเลขของคุณควร **ตรงเป๊ะ** ถ้าตั้ง **local random seed = 1992** ตามไกด์ (ยกเว้นบอกไว้ว่าอาจต่างเล็กน้อย)

---

> [!important] ต้องมี extension **Operator Toolbox** (มี operator `SMOTE Upsampling`) — เครื่องคุณติดตั้งแล้ว ✓

## ขั้นที่ 1 · อ่าน + Set Role + Multiply
`Read CSV` (`p3_breast_cancer_imbalanced.csv`) → `Set Role` (diagnosis → label) → `Multiply` → ▶ ดู Statistics ของ diagnosis

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::new
>   n2["Set Role"]:::new
>   n3["Multiply"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → inp"| n3
>   n3 -.->|"out 1"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:** 397 examples · diagnosis: benign **357** / malignant **40** → IR = 8.93

---

## ขั้นที่ 2 · แม่แบบ Cross Validation (ทำครั้งเดียวแล้ว copy)
1. Multiply **output 1** → `Cross Validation`: folds **5** · `stratified sampling` · seed **1992**
2. Testing pane: `Apply Model` → **`Performance (Binominal Classification)`**: ✅ accuracy, precision, recall, f measure · main criterion = `f_measure` · ✅ **manually set positive class** → positive class = `malignant` (ถ้าไม่เห็นกด *Show advanced parameters*)
3. เลือก Cross Validation → `Ctrl+C`, `Ctrl+V` อีก 3 ครั้ง → ต่อ Multiply output 2, 3, 4 · เปลี่ยนชื่อเป็น `CV baseline`, `CV tree`, `CV RUS`, `CV SMOTE`

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Set Role"]:::op
>   n3["Multiply"]:::op
>   n4[["CV baseline<br/><i>Cross Validation</i> ▣"]]:::new
>   n5[["CV tree<br/><i>Cross Validation</i> ▣"]]:::new
>   n6[["CV RUS<br/><i>Cross Validation</i> ▣"]]:::new
>   n7[["CV SMOTE<br/><i>Cross Validation</i> ▣"]]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → inp"| n3
>   n3 -->|"out 1 → exa"| n4
>   n4 -->|"per 1"| res(("res"))
>   n3 -->|"out 2 → exa"| n5
>   n5 -->|"per 1"| res(("res"))
>   n3 -->|"out 3 → exa"| n6
>   n6 -->|"per 1"| res(("res"))
>   n3 -->|"out 4 → exa"| n7
>   n7 -->|"per 1"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```
>
> **ข้างใน CV baseline · Cross Validation (ดับเบิลคลิก)**
> ```mermaid
> flowchart LR
>   subgraph P0["Training"]
>     direction LR
>   end
>   subgraph P1["Testing"]
>     direction LR
>     n1["Apply Model"]:::new
>     n2["Performance (Binominal Classification)"]:::new
>     n3(["mod"]):::port
>     n3 -->|"mod"| n1
>     n4(["tes"]):::port
>     n4 -->|"unl"| n1
>     n1 -->|"lab → lab"| n2
>     n5(["per 1"]):::port
>     n2 -->|"per"| n5
>   end
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

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

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **ข้างใน CV baseline · Cross Validation (ดับเบิลคลิก)**
> ```mermaid
> flowchart LR
>   subgraph P0["Training"]
>     direction LR
>     n1["Default Model"]:::new
>     n2(["tra"]):::port
>     n2 -->|"tra"| n1
>     n3(["mod"]):::port
>     n1 -->|"mod"| n3
>   end
>   subgraph P1["Testing"]
>     direction LR
>     n4["Apply Model"]:::op
>     n5["Performance (Binominal Classification)"]:::op
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
> **ข้างใน CV tree · Cross Validation (ดับเบิลคลิก)**
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
>     n4["Apply Model"]:::op
>     n5["Performance (Binominal Classification)"]:::op
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
> **ข้างใน CV RUS · Cross Validation (ดับเบิลคลิก)**
> ```mermaid
> flowchart LR
>   subgraph P0["Training"]
>     direction LR
>     n1["Sample"]:::new
>     n2["Decision Tree"]:::new
>     n3(["tra"]):::port
>     n3 -->|"exa"| n1
>     n1 -->|"exa → tra"| n2
>     n4(["mod"]):::port
>     n2 -->|"mod"| n4
>   end
>   subgraph P1["Testing"]
>     direction LR
>     n5["Apply Model"]:::op
>     n6["Performance (Binominal Classification)"]:::op
>     n7(["mod"]):::port
>     n7 -->|"mod"| n5
>     n8(["tes"]):::port
>     n8 -->|"unl"| n5
>     n5 -->|"lab → lab"| n6
>     n9(["per 1"]):::port
>     n6 -->|"per"| n9
>   end
>   n4 -.->|"ส่งโมเดลไป test fold"| n7
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```
>
> **ข้างใน CV SMOTE · Cross Validation (ดับเบิลคลิก)**
> ```mermaid
> flowchart LR
>   subgraph P0["Training"]
>     direction LR
>     n1["SMOTE Upsampling"]:::new
>     n2["Decision Tree"]:::new
>     n3(["tra"]):::port
>     n3 -->|"exa"| n1
>     n1 -->|"ups → tra"| n2
>     n4(["mod"]):::port
>     n2 -->|"mod"| n4
>   end
>   subgraph P1["Testing"]
>     direction LR
>     n5["Apply Model"]:::op
>     n6["Performance (Binominal Classification)"]:::op
>     n7(["mod"]):::port
>     n7 -->|"mod"| n5
>     n8(["tes"]):::port
>     n8 -->|"unl"| n5
>     n5 -->|"lab → lab"| n6
>     n9(["per 1"]):::port
>     n6 -->|"per"| n9
>   end
>   n4 -.->|"ส่งโมเดลไป test fold"| n7
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```


---

## ขั้นที่ 4 · ผลที่ควรเห็น
| CV | accuracy | precision (malignant) | recall (malignant) | f measure |
|---|---|---|---|---|
| baseline | 89.93% | ? | 0.00% | ? |
| tree | 94.98% | 78.89% | 68.33% | 71.06% |
| RUS | 85.64% | 42.63% | 90.00% | 56.99% |
| SMOTE | 88.94% | 48.26% | 80.00% | 59.45% |

(ใน RapidMiner แต่ละช่องแสดงแบบ `xx% +/- yy%` = ค่าเฉลี่ย ± sd ข้าม fold) · precision ของ baseline เป็น `unknown` (ไม่มีการทาย malignant เลย)

**อ่านผล:** baseline accuracy 89.93% แต่ recall 0 · tree ไม่ resample ได้ F1 ดีสุด · **RUS / SMOTE เพิ่ม recall** (68.33% → 90.00% / 80.00%) แลกกับ precision ที่ลดลง → งานคัดกรองมะเร็งให้น้ำหนัก recall → เลือก SMOTE หรือ RUS

> [!bug] วิธีที่ผิด (สไลด์ Imbalanced p.20): วาง SMOTE Upsampling **ก่อน** Cross Validation → ลองทำดู แล้ว f measure จะสูงขึ้นมากเกินจริง เพราะ test fold มีจุดสังเคราะห์

> [!success] เทียบ Python: ทิศทางเดียวกัน (Python: tree F1 0.773 · RUS recall 0.90 · SMOTE recall 0.825) — ตัวเลขต่างเล็กน้อยเพราะ tree และ fold คนละ implementation
