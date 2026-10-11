---
title: PR 09 · Association Rules (RapidMiner)
tags: [final, lab, practice, rapidminer]
---

# PR 09 · Association Rules — ไกด์ RapidMiner ทีละขั้น

> [!abstract] โจทย์ (เดียวกับไกด์ Python)
> ใบเสร็จซูเปอร์มาร์เก็ต 9,835 ใบ (ตาราง 0/1 ต่อสินค้า 169 ชนิด): FP-Growth min support 2% → Create Association Rules min confidence 30% → อ่าน support / confidence / lift

**ข้อมูล:** `final/practice/data/p9_groceries_onehot.csv` · **เวลาแนะนำ:** 30 นาที
**ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · [[PR 00 START HERE#⚙️ ทักษะพื้นฐาน RapidMiner (อ่านก่อนไกด์แรก)|ทักษะพื้นฐาน RapidMiner]] · ทำใน Python: [[PR 09 Association Rules (Python)]]
**เฉลย process:** `final/practice/rm/P09_solution.rmp` — ทำเองให้เสร็จก่อน แล้วค่อย **File → Import Process…** เปิดเทียบ (ตัวเลขทุกตัวในไกด์มาจากการรันไฟล์นี้จริง)

> [!tip] เริ่มต้น: **File → New Process → Blank** · ทำทีละขั้น กด ▶ **Run** หลังทุกขั้นที่มี "ผลที่ควรเห็น" แล้วเทียบ · ไม่ตรง → หยุดหาสาเหตุก่อน
> ตัวเลขของคุณควร **ตรงเป๊ะ** ถ้าตั้ง **local random seed = 1992** ตามไกด์ (ยกเว้นบอกไว้ว่าอาจต่างเล็กน้อย)

---

## ขั้นที่ 1 · อ่าน + id + binominal
1. `Read CSV` → `p9_groceries_onehot.csv` (170 คอลัมน์ — อ่านช้านิดหนึ่ง)
2. **`Set Role`**: `basket_id` → **`id`** (ไม่งั้นมันกลายเป็น "สินค้า")
3. **`Numerical to Binominal`**: attribute filter type `all` · min **0** · max **0** → 0 = false · 1 = true
4. ▶ **ผลที่ควรเห็น:** 9,835 examples · 1 special (id) · 169 binominal attributes · Statistics: whole milk true **2,513** (25.6%)

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::new
>   n2["Set Role"]:::new
>   n3["Numerical to Binominal"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -.->|"exa"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```


---

## ขั้นที่ 2 · FP-Growth
**`FP-Growth`**: input format `items in dummy coded columns` · **positive value** = `true` · min requirement `support` · **min support = 0.02** · ☐ find min number of itemsets → port **fre** → res → ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Set Role"]:::op
>   n3["Numerical to Binominal"]:::op
>   n4["FP-Growth"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → exa"| n4
>   n4 -.->|"fre"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:** Frequent Itemsets — **No. of Sets: 122** (เท่ากับ Python) · คลิกหัวคอลัมน์ Support เรียง: whole milk 0.256 · other vegetables 0.193 · rolls/buns 0.184 …

---

## ขั้นที่ 3 · Create Association Rules
**`Create Association Rules`** (ต่อจาก fre): criterion `confidence` · **min confidence = 0.3** → **rul** → res → ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read CSV"]:::op
>   n2["Set Role"]:::op
>   n3["Numerical to Binominal"]:::op
>   n4["FP-Growth"]:::op
>   n5["Create Association Rules"]:::new
>   n1 -->|"out → exa"| n2
>   n2 -->|"exa → exa"| n3
>   n3 -->|"exa → exa"| n4
>   n4 -->|"fre → ite"| n5
>   n5 -->|"rul"| res(("res"))
>   n5 -->|"ite"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:** AssociationRules **37 rules** (เท่ากับ Python 37) · คลิกหัวคอลัมน์ **Lift** เรียงมากไปน้อย:

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
| 0.02 | 122 | 37 |
| 0.05 | 31 | 3 |
(ค่าคำนวณด้วย Python ชุดเดียวกัน — FP-Growth ให้ผลเหมือน Apriori)
