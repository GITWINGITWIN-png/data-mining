---
title: PR 08 · K-Means Clustering (RapidMiner)
tags: [final, lab, practice, rapidminer]
---

# PR 08 · K-Means Clustering — ไกด์ RapidMiner ทีละขั้น

> [!abstract] โจทย์ (เดียวกับไกด์ Python)
> จัดกลุ่มไวน์ 178 ขวดที่ไม่รู้สายพันธุ์: normalize → elbow ด้วย Optimize → k-Means k = 3 → ประเมิน + ตีความ centroid → เทียบสายพันธุ์จริง

**ข้อมูล:** `final/practice/data/p8_wine_unlabeled.csv` · **เวลาแนะนำ:** 35 นาที
**ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · [[PR 00 START HERE#⚙️ ทักษะพื้นฐาน RapidMiner (อ่านก่อนไกด์แรก)|ทักษะพื้นฐาน RapidMiner]] · ทำใน Python: [[PR 08 K-Means Clustering (Python)]]
**เฉลย process:** `final/practice/rm/P08_solution.rmp` — ทำเองให้เสร็จก่อน แล้วค่อย **File → Import Process…** เปิดเทียบ (ตัวเลขทุกตัวในไกด์มาจากการรันไฟล์นี้จริง)

> [!tip] เริ่มต้น: **File → New Process → Blank** · ทำทีละขั้น กด ▶ **Run** หลังทุกขั้นที่มี "ผลที่ควรเห็น" แล้วเทียบ · ไม่ตรง → หยุดหาสาเหตุก่อน
> ตัวเลขของคุณควร **ตรงเป๊ะ** ถ้าตั้ง **local random seed = 1992** ตามไกด์ (ยกเว้นบอกไว้ว่าอาจต่างเล็กน้อย)

---

## ขั้นที่ 1 · อ่าน + กัน cultivar ไม่ให้ถูกใช้ + Normalize
`Read CSV` → **`Set Role`** (cultivar → `label`) → **`Normalize`** (Z) → `Multiply`

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::new
>   n2["Set Role"]:::new
>   n3["Normalize"]:::new
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

> k-Means ใช้เฉพาะ **regular attributes** → ตั้ง cultivar เป็น label (special) = ไม่ถูกใช้คำนวณระยะ แต่ยังอยู่ในตารางให้ตรวจทีหลัง

---

## ขั้นที่ 2 · Elbow: Optimize Parameters ครอบ k-Means
1. Multiply → **`Optimize Parameters (Grid)`** → ข้างใน: `inp` → **`k-Means`** (exa) → **`Cluster Distance Performance`** (exa ← k-Means **clu** (clustered set) · clu ← k-Means **mod** (cluster model)) · main criterion = `Avg. within centroid distance` → **`Log`** → `per`
2. Edit Parameter Settings: `k-Means` → **k** → Min 2 · Max 8 · Steps 6 · linear
3. k-Means: max runs **20** · ✅ determine good start values · ✅ local random seed **1992**
4. Log: (`k` ← k-Means parameter k) · (`avg_within` ← Cluster Distance Performance **value** `avg_within_distance`)
5. ข้างนอก: `Log to Data` → res → ▶ → Visualizations → Lines: x = k, y = avg_within

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Set Role"]:::op
>   n3["Normalize"]:::op
>   n4["Multiply"]:::op
>   n5[["Optimize Parameters (k)<br/><i>Optimize Parameters (Grid)</i> ▣"]]:::new
>   n6["Log to Data"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → inp"| n4
>   n4 -->|"out 2 → inp 1"| n5
>   n6 -->|"exa"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```
>
> **ข้างใน Optimize Parameters (k) · Optimize Parameters (Grid) (ดับเบิลคลิก)**
> ```mermaid
> flowchart LR
>   subgraph P0["ข้างใน"]
>     direction LR
>     n1["Clustering (opt)<br/><i>k-Means</i>"]:::new
>     n2["Cluster Distance Performance (opt)"]:::new
>     n3["Log"]:::new
>     n4(["inp 1"]):::port
>     n4 -->|"exa"| n1
>     n1 -->|"clu → exa"| n2
>     n1 -->|"clu → clu"| n2
>     n2 -->|"per → thr 1"| n3
>     n5(["per"]):::port
>     n3 -->|"thr 1"| n5
>   end
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:**

| k | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|
| avg within centroid distance | 9.27 | 7.14 | 6.57 | 6.20 | 5.86 | 5.52 | 5.20 |

→ ลดมากจาก k = 2 → 3 (9.27 → 7.14) แล้วค่อย ๆ แบน → **elbow ที่ k = 3**

---

## ขั้นที่ 3 · k-Means k = 3 + ประเมิน
Multiply → **`k-Means`** (k **3**, max runs 20, good start values, seed 1992) → **`Cluster Distance Performance`** (main criterion `Davies Bouldin`) → ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Set Role"]:::op
>   n3["Normalize"]:::op
>   n4["Multiply"]:::op
>   n5["Clustering<br/><i>k-Means</i>"]:::new
>   n6["Cluster Distance Performance"]:::new
>   n7[["Optimize Parameters (k)<br/><i>Optimize Parameters (Grid)</i> ▣"]]:::sub
>   n8["Log to Data"]:::op
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → inp"| n4
>   n4 -->|"out 1 → exa"| n5
>   n5 -->|"clu → exa"| n6
>   n5 -->|"clu → clu"| n6
>   n6 -->|"per"| res(("res"))
>   n6 -->|"clu"| res(("res"))
>   n4 -->|"out 2 → inp 1"| n7
>   n8 -->|"exa"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:**
- Cluster Model: Cluster 0 **62** items · Cluster 1 **65** · Cluster 2 **51**
- PerformanceVector: Avg. within centroid distance **-7.139** · Davies Bouldin **-1.389** (ติดลบเพราะ RapidMiner ถือว่ามากดี → อ่านค่าสัมบูรณ์ · ต่ำ = ดี)
- Cluster Model → **Centroid Table**: ดู z-score ของแต่ละกลุ่ม (proline, alcohol, flavanoids, color_intensity, hue) แล้วตั้งชื่อกลุ่ม · **Heat Map** ช่วยเห็นเร็ว

---

## ขั้นที่ 4 · เทียบกับสายพันธุ์จริง (Aggregate)
ต่อ Cluster Distance Performance **exa** → **`Aggregate`**: group by attributes = `cluster` และ `cultivar` (✅ include special attributes) · aggregation (`alcohol`, `count`) → ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Set Role"]:::op
>   n3["Normalize"]:::op
>   n4["Multiply"]:::op
>   n5["Clustering<br/><i>k-Means</i>"]:::op
>   n6["Cluster Distance Performance"]:::op
>   n7["Aggregate"]:::new
>   n8[["Optimize Parameters (k)<br/><i>Optimize Parameters (Grid)</i> ▣"]]:::sub
>   n9["Log to Data"]:::op
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → inp"| n4
>   n4 -->|"out 1 → exa"| n5
>   n5 -->|"clu → exa"| n6
>   n5 -->|"clu → clu"| n6
>   n6 -->|"per"| res(("res"))
>   n6 -->|"exa → exa"| n7
>   n7 -->|"exa"| res(("res"))
>   n6 -->|"clu"| res(("res"))
>   n4 -->|"out 2 → inp 1"| n8
>   n9 -->|"exa"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:**

| cluster | cultivar | count |
|---|---|---|
| cluster_0 | cultivar_0 | 59 |
| cluster_0 | cultivar_1 | 3 |
| cluster_1 | cultivar_1 | 65 |
| cluster_2 | cultivar_1 | 3 |
| cluster_2 | cultivar_2 | 48 |

→ แต่ละ cluster ตรงกับสายพันธุ์เดียวเกือบทั้งหมด = **96.6%** (เท่ากับ Python) · เลข cluster อาจสลับจาก Python ได้ ดูที่สมาชิก
