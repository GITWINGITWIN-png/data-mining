---
title: PR 01 · Data Handling (RapidMiner)
tags: [final, lab, practice, rapidminer]
---

# PR 01 · Data Handling — ไกด์ RapidMiner ทีละขั้น

> [!abstract] โจทย์ (เดียวกับไกด์ Python)
> ร้านอาหารส่งบิล 2 สัปดาห์มาเป็น 2 ไฟล์ และตารางข้อมูลวันทำการแยกอีกไฟล์ จง append + join ให้เป็นตารางเดียว สร้าง tip% กรองโต๊ะใหญ่มื้อเย็น สรุปตามวัน และทำ pivot วัน × มื้อ

**ข้อมูล:** `final/practice/data/p1_bills_week1.csv · p1_bills_week2.csv · p1_day_info.csv` · **เวลาแนะนำ:** 40 นาที
**ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · [[PR 00 START HERE#⚙️ ทักษะพื้นฐาน RapidMiner (อ่านก่อนไกด์แรก)|ทักษะพื้นฐาน RapidMiner]] · ทำใน Python: [[PR 01 Data Handling (Python)]]
**เฉลย process:** `final/practice/rm/P01_solution.rmp` — ทำเองให้เสร็จก่อน แล้วค่อย **File → Import Process…** เปิดเทียบ (ตัวเลขทุกตัวในไกด์มาจากการรันไฟล์นี้จริง)

> [!tip] เริ่มต้น: **File → New Process → Blank** · ทำทีละขั้น กด ▶ **Run** หลังทุกขั้นที่มี "ผลที่ควรเห็น" แล้วเทียบ · ไม่ตรง → หยุดหาสาเหตุก่อน
> ตัวเลขของคุณควร **ตรงเป๊ะ** ถ้าตั้ง **local random seed = 1992** ตามไกด์ (ยกเว้นบอกไว้ว่าอาจต่างเล็กน้อย)

---

## ขั้นที่ 1 · อ่านไฟล์ 3 ไฟล์ (Read CSV)
1. แผง **Operators** → พิมพ์ `Read CSV` → ลากมาวาง **3 ตัว** (เรียงลงมา)
2. คลิกตัวแรก → แผง **Parameters**: **csv file** → กดไอคอน 📁 → เลือก `final/practice/data/p1_bills_week1.csv` · **column separators** = `,` (ค่า default `,;` ก็ได้) · ✅ **first row as names**
3. ตัวที่ 2 → `p1_bills_week2.csv` · ตัวที่ 3 → `p1_day_info.csv`
4. ดับเบิลคลิกชื่อ operator เพื่อเปลี่ยนชื่อเป็น `Read week1`, `Read week2`, `Read day_info` (อ่านง่ายตอน screenshot)
5. ต่อ port **out** ของ `Read week1` → port **res** ขอบขวา → ▶ Run

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read week1<br/><i>Read CSV</i>"]:::new
>   n2["Read week2<br/><i>Read CSV</i>"]:::new
>   n3["Read day_info<br/><i>Read CSV</i>"]:::new
>   n1 -.->|"out"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:** แท็บ ExampleSet — **130 examples**, 8 regular attributes (bill_id, total_bill, tip, sex, smoker, day, time, size) · แท็บ **Statistics** ไม่มี Missing
> 💡 ถ้าคอลัมน์ทั้งหมดรวมเป็นคอลัมน์เดียว = ตั้ง column separators ผิด

---

## ขั้นที่ 2 · ต่อสองสัปดาห์ (Append)
1. ลบเส้นที่ต่อไป res (คลิกเส้น → Delete) · ลาก **`Append`** มาวาง
2. `Read week1` **out** → `Append` **example set 1** · `Read week2` **out** → **example set 2** (port ใหม่โผล่เองเมื่อต่อเส้น)
3. Parameters: **merge type** = `all`
4. `Append` **merged set** → **res** → ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read week1<br/><i>Read CSV</i>"]:::op
>   n2["Read week2<br/><i>Read CSV</i>"]:::op
>   n3["Read day_info<br/><i>Read CSV</i>"]:::op
>   n4["Append"]:::new
>   n1 -->|"out → exa 1"| n4
>   n2 -->|"out → exa 2"| n4
>   n4 -.->|"mer"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

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

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read week1<br/><i>Read CSV</i>"]:::op
>   n2["Read week2<br/><i>Read CSV</i>"]:::op
>   n3["Read day_info<br/><i>Read CSV</i>"]:::op
>   n4["Append"]:::op
>   n5["Join"]:::new
>   n1 -->|"out → exa 1"| n4
>   n2 -->|"out → exa 2"| n4
>   n4 -->|"mer → lef"| n5
>   n3 -->|"out → rig"| n5
>   n5 -.->|"joi"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:** **244 examples**, **10 attributes** (เพิ่ม `is_weekend`, `open_hours`) · คอลัมน์ is_weekend ไม่มีค่าว่าง

---

## ขั้นที่ 4 · สร้าง tip_pct (Generate Attributes)
1. ลาก **`Generate Attributes`** ต่อจาก Join (**join** → **example set input**)
2. **function descriptions** → **Edit List…** → attribute name = `tip_pct` · function expressions = `tip / total_bill * 100` (กดไอคอนเครื่องคิดเลขเพื่อเปิด Expression editor ได้)
3. **example set output** → res → ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read week1<br/><i>Read CSV</i>"]:::op
>   n2["Read week2<br/><i>Read CSV</i>"]:::op
>   n3["Read day_info<br/><i>Read CSV</i>"]:::op
>   n4["Append"]:::op
>   n5["Join"]:::op
>   n6["Generate Attributes"]:::new
>   n1 -->|"out → exa 1"| n4
>   n2 -->|"out → exa 2"| n4
>   n4 -->|"mer → lef"| n5
>   n3 -->|"out → rig"| n5
>   n5 -->|"joi → exa"| n6
>   n6 -.->|"exa"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:** คอลัมน์ใหม่ `tip_pct` · แท็บ Statistics: average ≈ **16.08**, max ≈ **71.03**

---

## ขั้นที่ 5 · แยกข้อมูลไปหลายทาง (Multiply)
ลาก **`Multiply`** ต่อจาก Generate Attributes → จะใช้ output 1 / 2 / 3 / 4 สำหรับขั้นถัดไป (ข้อมูลชุดเดียวกันถูกก๊อปไปหลายเส้น)

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read week1<br/><i>Read CSV</i>"]:::op
>   n2["Read week2<br/><i>Read CSV</i>"]:::op
>   n3["Read day_info<br/><i>Read CSV</i>"]:::op
>   n4["Append"]:::op
>   n5["Join"]:::op
>   n6["Generate Attributes"]:::op
>   n7["Multiply"]:::new
>   n1 -->|"out → exa 1"| n4
>   n2 -->|"out → exa 2"| n4
>   n4 -->|"mer → lef"| n5
>   n3 -->|"out → rig"| n5
>   n5 -->|"joi → exa"| n6
>   n6 -->|"exa → inp"| n7
>   n7 -.->|"out 1"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```


---

## ขั้นที่ 6 · กรองโต๊ะใหญ่มื้อเย็น (Filter Examples)
1. `Multiply` **output 1** → **`Filter Examples`**
2. **condition class** = `custom_filters` → **filters** → **Add Filters…**
   - แถว 1: `time` · `=` · `Dinner`
   - แถว 2: `size` · `≥` · `4`
   - เลือก **Match all** (AND)
3. **example set output** → res → ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read week1<br/><i>Read CSV</i>"]:::op
>   n2["Read week2<br/><i>Read CSV</i>"]:::op
>   n3["Read day_info<br/><i>Read CSV</i>"]:::op
>   n4["Append"]:::op
>   n5["Join"]:::op
>   n6["Generate Attributes"]:::op
>   n7["Multiply"]:::op
>   n8["Filter Examples"]:::new
>   n1 -->|"out → exa 1"| n4
>   n2 -->|"out → exa 2"| n4
>   n4 -->|"mer → lef"| n5
>   n3 -->|"out → rig"| n5
>   n5 -->|"joi → exa"| n6
>   n6 -->|"exa → inp"| n7
>   n7 -->|"out 1 → exa"| n8
>   n8 -->|"exa"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:** **37 examples**

---

## ขั้นที่ 7 · สรุปตามวัน (Aggregate)
1. `Multiply` **output 2** → **`Aggregate`**
2. ☐ **use default aggregation** · **group by attributes** → เลือก `day`
3. **aggregation attributes** → Edit List… : (`bill_id`, `count`) · (`total_bill`, `average`) · (`tip_pct`, `average`)
4. ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read week1<br/><i>Read CSV</i>"]:::op
>   n2["Read week2<br/><i>Read CSV</i>"]:::op
>   n3["Read day_info<br/><i>Read CSV</i>"]:::op
>   n4["Append"]:::op
>   n5["Join"]:::op
>   n6["Generate Attributes"]:::op
>   n7["Multiply"]:::op
>   n8["Filter Examples"]:::op
>   n9["Aggregate"]:::new
>   n1 -->|"out → exa 1"| n4
>   n2 -->|"out → exa 2"| n4
>   n4 -->|"mer → lef"| n5
>   n3 -->|"out → rig"| n5
>   n5 -->|"joi → exa"| n6
>   n6 -->|"exa → inp"| n7
>   n7 -->|"out 1 → exa"| n8
>   n8 -->|"exa"| res(("res"))
>   n7 -->|"out 2 → exa"| n9
>   n9 -->|"exa"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:**

| day | count(bill_id) | average(total_bill) | average(tip_pct) |
|---|---|---|---|
| Fri | 19 | 17.15 | 16.99 |
| Sat | 87 | 20.44 | 15.32 |
| Sun | 76 | 21.41 | 16.69 |
| Thur | 62 | 17.68 | 16.13 |

→ tip% สูงสุดวัน **Fri (16.99%)** · บิลเยอะสุดวัน Sat (87) — ตรงกับ Python

---

## ขั้นที่ 8 · Pivot วัน × มื้อ (Pivot)
1. `Multiply` **output 3** → **`Pivot`**
2. **group by attributes** = `day` · **column grouping attribute** = `time` · **aggregation attributes** → Edit List… : (`tip_pct`, `average`)
3. ▶

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read week1<br/><i>Read CSV</i>"]:::op
>   n2["Read week2<br/><i>Read CSV</i>"]:::op
>   n3["Read day_info<br/><i>Read CSV</i>"]:::op
>   n4["Append"]:::op
>   n5["Join"]:::op
>   n6["Generate Attributes"]:::op
>   n7["Multiply"]:::op
>   n8["Filter Examples"]:::op
>   n9["Aggregate"]:::op
>   n10["Pivot"]:::new
>   n1 -->|"out → exa 1"| n4
>   n2 -->|"out → exa 2"| n4
>   n4 -->|"mer → lef"| n5
>   n3 -->|"out → rig"| n5
>   n5 -->|"joi → exa"| n6
>   n6 -->|"exa → inp"| n7
>   n7 -->|"out 1 → exa"| n8
>   n8 -->|"exa"| res(("res"))
>   n7 -->|"out 2 → exa"| n9
>   n9 -->|"exa"| res(("res"))
>   n7 -->|"out 3 → inp"| n10
>   n10 -->|"out"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

**ผลที่ควรเห็น:**

| day | average(tip_pct)_Dinner | average(tip_pct)_Lunch |
|---|---|---|
| Sun | 16.69 | ? |
| Sat | 15.32 | ? |
| Thur | 15.97 | 16.13 |
| Fri | 15.89 | 18.88 |

ช่อง `?` = **missing** (Sat/Sun ไม่มีมื้อกลางวัน) — ไม่ใช่ 0

---

## ขั้นที่ 9 · กราฟ (Results → Visualizations)
`Multiply` **output 4** → res → ▶ → ExampleSet → แท็บ **Visualizations**:
1. **Histogram**: Value column = `tip_pct` · bins 25 → ส่วนใหญ่ 10–20% หางขวายาว
2. **Boxplot**: Value = `tip_pct` · Group by/Color = `day` → median ใกล้กัน มี outlier ด้านบน
3. **Scatter**: x = `total_bill` · y = `tip` · Color = `time` → tip เพิ่มตามบิล
4. Screenshot ใส่รายงาน (`Shift+PrtSc`)

> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)
> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล
>
> **Process หลัก**
> ```mermaid
> flowchart LR
>   n1["Read week1<br/><i>Read CSV</i>"]:::op
>   n2["Read week2<br/><i>Read CSV</i>"]:::op
>   n3["Read day_info<br/><i>Read CSV</i>"]:::op
>   n4["Append"]:::op
>   n5["Join"]:::op
>   n6["Generate Attributes"]:::op
>   n7["Multiply"]:::op
>   n8["Filter Examples"]:::op
>   n9["Aggregate"]:::op
>   n10["Pivot"]:::op
>   n1 -->|"out → exa 1"| n4
>   n2 -->|"out → exa 2"| n4
>   n4 -->|"mer → lef"| n5
>   n3 -->|"out → rig"| n5
>   n5 -->|"joi → exa"| n6
>   n6 -->|"exa → inp"| n7
>   n7 -->|"out 1 → exa"| n8
>   n8 -->|"exa"| res(("res"))
>   n7 -->|"out 2 → exa"| n9
>   n9 -->|"exa"| res(("res"))
>   n7 -->|"out 3 → inp"| n10
>   n10 -->|"out"| res(("res"))
>   n7 -->|"out 4"| res(("res"))
>   classDef new fill:#ffe08a,stroke:#b8860b,color:#000
>   classDef op fill:#eef3fb,stroke:#5b7db1,color:#000
>   classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000
>   classDef port fill:#f2f2f2,stroke:#888,color:#333
> ```

> [!success] เทียบคำตอบ: 244 บิล · tip% เฉลี่ย 16.08 · Fri สูงสุด 16.99% · โต๊ะใหญ่มื้อเย็น 37 บิล (ตรงกับไกด์ Python ทุกตัว)
