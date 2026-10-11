---
title: PR 04 · KNN Baseline CV Optimize (RapidMiner)
tags: [final, lab, practice, rapidminer]
---

# PR 04 · KNN Baseline CV Optimize — ไกด์ RapidMiner ทีละขั้น

> [!abstract] โจทย์ (เดียวกับไกด์ Python)
> ระบุสายพันธุ์องุ่นของไวน์จากเคมี 13 ค่า: baseline → k-NN ไม่ normalize → k-NN normalize → Optimize k ด้วย CV + Log

**ข้อมูล:** `final/practice/data/p4_wine.csv` · **เวลาแนะนำ:** 40 นาที
**ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · [[PR 00 START HERE#⚙️ ทักษะพื้นฐาน RapidMiner (อ่านก่อนไกด์แรก)|ทักษะพื้นฐาน RapidMiner]] · ทำใน Python: [[PR 04 KNN Baseline CV Optimize (Python)]]
**เฉลย process:** `final/practice/rm/P04_solution.rmp` — ทำเองให้เสร็จก่อน แล้วค่อย **File → Import Process…** เปิดเทียบ (ตัวเลขทุกตัวในไกด์มาจากการรันไฟล์นี้จริง)

> [!tip] เริ่มต้น: **File → New Process → Blank** · ทำทีละขั้น กด ▶ **Run** หลังทุกขั้นที่มี "ผลที่ควรเห็น" แล้วเทียบ · ไม่ตรง → หยุดหาสาเหตุก่อน
> ตัวเลขของคุณควร **ตรงเป๊ะ** ถ้าตั้ง **local random seed = 1992** ตามไกด์ (ยกเว้นบอกไว้ว่าอาจต่างเล็กน้อย)

---

## ขั้นที่ 1 · อ่าน + Set Role + Multiply
`Read CSV` → `Set Role` (cultivar → label) → `Multiply` · ▶ ดู Statistics: proline min 278 / max 1680 vs hue ~0.5–1.7 → ต้อง normalize

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
| baseline | 39.90% +/- 1.86% |
| k-NN raw | 67.84% +/- 13.31% |
| **k-NN normalized** | **96.11% +/- 4.57%** |

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
>   n5[["CV raw<br/><i>Cross Validation</i> ▣"]]:::new
>   n6[["CV normalized<br/><i>Cross Validation</i> ▣"]]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → inp"| n3
>   n3 -->|"out 1 → exa"| n4
>   n4 -->|"per 1"| res(("res"))
>   n3 -->|"out 2 → exa"| n5
>   n5 -->|"per 1"| res(("res"))
>   n3 -->|"out 3 → exa"| n6
>   n6 -->|"per 1"| res(("res"))
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
>     n1["Default Model"]:::new
>     n2(["tra"]):::port
>     n2 -->|"tra"| n1
>     n3(["mod"]):::port
>     n1 -->|"mod"| n3
>   end
>   subgraph P1["Testing"]
>     direction LR
>     n4["Apply Model"]:::new
>     n5["Performance (Classification)"]:::new
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
> **ข้างใน CV raw · Cross Validation (ดับเบิลคลิก)**
> ```mermaid
> flowchart LR
>   subgraph P0["Training"]
>     direction LR
>     n1["k-NN"]:::new
>     n2(["tra"]):::port
>     n2 -->|"tra"| n1
>     n3(["mod"]):::port
>     n1 -->|"mod"| n3
>   end
>   subgraph P1["Testing"]
>     direction LR
>     n4["Apply Model"]:::new
>     n5["Performance (Classification)"]:::new
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
> **ข้างใน CV normalized · Cross Validation (ดับเบิลคลิก)**
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
>     n7["Performance (Classification)"]:::new
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


---

## ขั้นที่ 3 · Optimize Parameters (Grid) หา k
1. Multiply **output 4** → **`Optimize Parameters (Grid)`** → ดับเบิลคลิกเข้าไป
2. ข้างใน: copy `CV normalized` มาวาง → ต่อ `inp` (input 1) → CV **exa** · ต่อ CV **per** → **`Log`** → ต่อ Log **through 1** → `per` ขอบขวา
3. ออกมาข้างนอก → เลือก Optimize → **Edit Parameter Settings…**: ซ้ายเลือก `k-NN` (ตัวใน CV) → กลางเลือก **k** → ➡ → ตั้ง **Min 1 · Max 30 · Steps 29 · Scale linear** → OK
4. เลือก **Log** (ข้างใน) → **log** → Edit List…:
   - column name `k` → operator `k-NN` → **parameter** → `k`
   - column name `accuracy` → operator `Cross Validation` → **value** → `performance main criterion`
5. ข้างนอก: ลาก **`Log to Data`** (log name = `Log`) → res · Optimize **per** และ **par** → res → ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Set Role"]:::op
>   n3["Multiply"]:::op
>   n4[["CV baseline<br/><i>Cross Validation</i> ▣"]]:::sub
>   n5[["CV raw<br/><i>Cross Validation</i> ▣"]]:::sub
>   n6[["CV normalized<br/><i>Cross Validation</i> ▣"]]:::sub
>   n7[["Optimize Parameters (Grid) ▣"]]:::new
>   n8["Log to Data"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → inp"| n3
>   n3 -->|"out 1 → exa"| n4
>   n4 -->|"per 1"| res(("res"))
>   n3 -->|"out 2 → exa"| n5
>   n5 -->|"per 1"| res(("res"))
>   n3 -->|"out 3 → exa"| n6
>   n6 -->|"per 1"| res(("res"))
>   n3 -->|"out 4 → inp 1"| n7
>   n8 -->|"exa"| res(("res"))
>   n7 -->|"per"| res(("res"))
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
>     n1[["CV normalized (copy)<br/><i>Cross Validation</i> ▣"]]:::new
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
> **ข้างใน CV normalized (copy) · Cross Validation (ดับเบิลคลิก)**
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
>     n7["Performance (Classification)"]:::new
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

**ผลที่ควรเห็น:** ParameterSet: **k-NN.k = 25** · accuracy **97.75%** · ตาราง Log to Data 30 แถว (k vs accuracy) → Visualizations → **Series/Lines**: x = k, y = accuracy

| k | 1 | 5 | 10 | 15 | 20 | 25 | 30 |
|---|---|---|---|---|---|---|---|
| accuracy | 95.51% | 96.07% | 96.07% | 96.07% | 96.63% | 97.75% | 97.75% |

> [!note] RapidMiner เลือก k = 25 ส่วน Python เลือก k = 5 — accuracy ต่างกันไม่ถึง 2% ในช่วง k กว้าง (folds และ z-score n−1 ต่างกัน) · เขียนในรายงานว่า "ช่วง k ประมาณ 13–30 ให้ผลใกล้เคียงกัน"

> [!success] เทียบ Python: baseline 0.399 · raw 0.686 · normalized 0.978
