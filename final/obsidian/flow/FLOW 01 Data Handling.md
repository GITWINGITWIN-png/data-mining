---
title: FLOW 01 · Data Handling & Visualization
tags: [final, flow, data-handling, visualization]
---

# FLOW 01 · Data Handling & Visualization
> template: Python **T01** · RapidMiner **R01** · กลับ [[FLOW 00 START HERE]]

## โจทย์หน้าตาแบบนี้
*"import และตรวจสอบข้อมูล"* · *"เลือกเฉพาะ…"* · *"กรองเฉพาะลูกค้าที่…"* · *"รวมข้อมูล 2 ไฟล์"* · *"เพิ่มข้อมูลจากตาราง…"* ·
*"สรุปยอดตามกลุ่ม"* · *"สร้าง pivot table"* · *"วาดกราฟและอธิบาย"*

```mermaid
flowchart LR
  A["Import"] --> B["Inspect<br/>shape · dtype · missing · สถิติ"]
  B --> C["Append<br/>ต่อแถว"]
  C --> D["Join<br/>เพิ่มคอลัมน์"]
  D --> E["Select + Set Role"]
  E --> F["Filter"]
  F --> G["Generate"]
  G --> H["Aggregate / Pivot"]
  H --> I["กราฟ + ตีความ"]
```

## ทีละขั้น

<!-- RM-CANVAS -->

> [!info]- 🖥️ วิธีอ่านภาพ RapidMiner ใต้แต่ละขั้น (สร้างจาก `R01_data_handling.rmp` จริง)
> กล่อง = operator (บน: ชื่อบน canvas · ล่าง: ชนิด) · ⧉ = มี subprocess (ดับเบิลคลิกเข้าไป) · ป้ายบนเส้น = port ย่อ (exa = example set · mod = model · pre = preprocessing model · per = performance · lab = labelled data · tra = training set · tes = test set · out = output · par = partition ของ Split Data / parameter set ของ Optimize · thr = threshold · wei = weights · fre = frequent sets · rul = rules) · ◯ res = ต่อออกผลลัพธ์ · กล่องเส้นประ = port ขอบ pane · สี: 🟪 อ่านข้อมูล · 🟦 จัดการข้อมูล · 🟩 preprocessing · 🟧 โมเดล · 🟨 apply · 🟥 ประเมิน/validation · ⬜ utility · มีเฉพาะ operator ของขั้นนั้น (ไฟล์จริงมี operator อื่นต่ออยู่ด้วย)

<!-- /RM-CANVAS -->

### ① Import → ② Inspect
- **ทำ:** อ่านไฟล์ → ดูจำนวนแถว/คอลัมน์ · ชนิดข้อมูล · ค่าว่าง · สถิติ (mean, median, min, max) · สัดส่วน label
- **ทำไม:** ทุกการตัดสินใจหลังจากนี้ขึ้นกับสิ่งที่เห็นตรงนี้ เช่น คอลัมน์ตัวเลขที่ถูกอ่านเป็นข้อความ (เพราะมี `?`) จะคำนวณไม่ได้, คอลัมน์ที่ว่าง 80% ควรตัด
- **ดู mean เทียบ median:** mean > median มาก = **เบ้ขวา** (มีค่าสูงผิดปกติดึง mean) → ใช้ median เป็นค่ากลางที่ทนกว่า
- **อยู่ที่:** T01 §1 · R01 res 1 → Statistics

### ③ Append (Concatenate) ก่อน ④ Join
- **Append** = ต่อ **แถว** (ไฟล์คอลัมน์เดียวกัน คนละช่วงเวลา/สาขา) · **Join** = เพิ่ม **คอลัมน์** จากอีกตารางด้วย key
- **ทำไม append ก่อน join:** ถ้า join ทีละไฟล์แล้วค่อยต่อ ต้อง join 2 รอบและเสี่ยงคอลัมน์ไม่ตรงกัน · ต่อแถวให้ครบก่อนแล้ว join ครั้งเดียว
- **ต้องตรวจหลัง append:** คอลัมน์ตรงกันไหม · id ซ้ำไหม (ข้อมูลซ้อนช่วงเวลา)
- **join type เลือกยังไง:**

| join | เก็บอะไร | ใช้เมื่อ |
|---|---|---|
| inner | เฉพาะ key ที่มีทั้งสองฝั่ง | ต้องการเฉพาะแถวที่ข้อมูลครบ |
| **left** | ทุกแถวของตารางหลัก (ไม่เจอคู่ = ว่าง) | **ห้ามแถวหลักหาย** (นิยมสุด) |
| outer | ทุกแถวทั้งสองฝั่ง | อยากเห็นว่าอะไรจับคู่ไม่ได้ |

- **ต้องตรวจหลัง join:** จำนวนแถวเพิ่มขึ้นไหม (ถ้าเพิ่ม = key ในตาราง lookup ซ้ำ → แถวถูกคูณ) · มีกี่แถวที่จับคู่ไม่ได้
- **อยู่ที่:** T01 §4–§5 · R01 Append / Join

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: Append (exa 1 + exa 2) → Join (lef + rig) → Multiply แตกสำเนาให้แต่ละ §
> ```mermaid
> flowchart LR
>   n0["Read CSV (หลัก)<br/><i>Read CSV</i>"]:::data
>   n1["Read CSV (append)<br/><i>Read CSV</i>"]:::data
>   n2["Read CSV (lookup)<br/><i>Read CSV</i>"]:::data
>   n3["Append"]:::blend
>   n4["Join"]:::blend
>   n5["Multiply"]:::util
>   n0 -->|"out"| n3
>   n1 -->|"out"| n3
>   n3 -->|"mer"| n4
>   n2 -->|"out"| n4
>   n4 -->|"joi"| n5
>   nR0(("res")):::res
>   n5 -->|"out 1"| nR0
>   classDef data fill:#e8dcf5,stroke:#7b52ab,color:#000
>   classDef blend fill:#dceefb,stroke:#3a7bbf,color:#000
>   classDef clean fill:#d9f2e6,stroke:#2e8b57,color:#000
>   classDef model fill:#ffe7c2,stroke:#d4860b,color:#000
>   classDef score fill:#fff6b3,stroke:#b8a400,color:#000
>   classDef eval fill:#fcd9d9,stroke:#c0392b,color:#000
>   classDef util fill:#eeeeee,stroke:#777,color:#000
>   classDef port fill:#ffffff,stroke:#999,stroke-dasharray:3 3,color:#555
>   classDef res fill:#ffffff,stroke:#333,stroke-width:2px,color:#000
> ```

<!-- /RM-CANVAS -->

### ⑤ Select Attributes + Set Role
- **ตัด:** id (ไม่มีความหมาย) · คอลัมน์ที่รู้หลังเกิดผล (leak) · คอลัมน์ซ้ำซ้อน · ค่าว่างเยอะมาก
- **Set Role:** บอกโปรแกรมว่าคอลัมน์ไหนคือ id (ไว้ติดป้าย) และไหนคือ label (คำตอบ) → โปรแกรมจะไม่ใช้สองอย่างนี้เป็น feature
- **ทำไมสำคัญ:** ถ้าไม่ตั้ง id ใน RapidMiner, k-NN จะเอา id ไปคิดระยะทางด้วย → ผลผิดโดยไม่มี error
- **อยู่ที่:** T01 §2 · R01 §2

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: Select Attributes → Set Role (id) → Set Role (label)
> ```mermaid
> flowchart LR
>   n0["Multiply"]:::util
>   n1["Select Attributes"]:::blend
>   n2["Set Role (id)<br/><i>Set Role</i>"]:::blend
>   n3["Set Role (label)<br/><i>Set Role</i>"]:::blend
>   n0 -->|"out 2"| n1
>   n1 -->|"exa"| n2
>   n2 -->|"exa"| n3
>   nR0(("res")):::res
>   n3 -->|"exa"| nR0
>   classDef data fill:#e8dcf5,stroke:#7b52ab,color:#000
>   classDef blend fill:#dceefb,stroke:#3a7bbf,color:#000
>   classDef clean fill:#d9f2e6,stroke:#2e8b57,color:#000
>   classDef model fill:#ffe7c2,stroke:#d4860b,color:#000
>   classDef score fill:#fff6b3,stroke:#b8a400,color:#000
>   classDef eval fill:#fcd9d9,stroke:#c0392b,color:#000
>   classDef util fill:#eeeeee,stroke:#777,color:#000
>   classDef port fill:#ffffff,stroke:#999,stroke-dasharray:3 3,color:#555
>   classDef res fill:#ffffff,stroke:#333,stroke-width:2px,color:#000
> ```

<!-- /RM-CANVAS -->

### ⑥ Filter → ⑦ Generate
- **Filter** ก่อนสรุป เพราะโจทย์มักถามเฉพาะกลุ่ม ("เฉพาะมื้อเย็น") · ตอบเสมอว่าเหลือกี่แถวจากเท่าไร
- **Generate** สร้างตัวแปรที่ตอบโจทย์ได้ตรงกว่า เช่น `tip_pct = tip / total_bill × 100` (เปรียบเทียบข้ามบิลขนาดต่างกันได้ยุติธรรม)
- **อยู่ที่:** T01 §3, §8 · R01 §3, §8

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: Filter Examples · Generate Attributes (แต่ละตัวรับสำเนาจาก Multiply)
> ```mermaid
> flowchart LR
>   n0["Multiply"]:::util
>   n1["Filter Examples"]:::blend
>   n2["Generate Attributes"]:::blend
>   n0 -->|"out 3"| n1
>   nR0(("res")):::res
>   n1 -->|"exa"| nR0
>   n0 -->|"out 6"| n2
>   nR1(("res")):::res
>   n2 -->|"exa"| nR1
>   classDef data fill:#e8dcf5,stroke:#7b52ab,color:#000
>   classDef blend fill:#dceefb,stroke:#3a7bbf,color:#000
>   classDef clean fill:#d9f2e6,stroke:#2e8b57,color:#000
>   classDef model fill:#ffe7c2,stroke:#d4860b,color:#000
>   classDef score fill:#fff6b3,stroke:#b8a400,color:#000
>   classDef eval fill:#fcd9d9,stroke:#c0392b,color:#000
>   classDef util fill:#eeeeee,stroke:#777,color:#000
>   classDef port fill:#ffffff,stroke:#999,stroke-dasharray:3 3,color:#555
>   classDef res fill:#ffffff,stroke:#333,stroke-width:2px,color:#000
> ```

<!-- /RM-CANVAS -->

### ⑧ Aggregate / Pivot
- **Aggregate** = สรุปตามกลุ่ม 1 มิติ (ยอดรวมต่อวัน) · **Pivot** = 2 มิติ (วัน × มื้อ)
- **สัดส่วนคลาส** (เช่น % churn ตาม Contract) → สร้างคอลัมน์ 0/1 แล้ว pivot ด้วย **average** (ค่าเฉลี่ยของ 0/1 = สัดส่วน)
- **อยู่ที่:** T01 §6–§7 · R01 §6–§7

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: Aggregate · Generate (คอลัมน์ 0/1) → Pivot (average = สัดส่วน)
> ```mermaid
> flowchart LR
>   n0["Multiply"]:::util
>   n1["Aggregate"]:::blend
>   n2["Generate Attributes (rate)<br/><i>Generate Attributes</i>"]:::blend
>   n3["Pivot"]:::blend
>   n0 -->|"out 4"| n1
>   nR0(("res")):::res
>   n1 -->|"exa"| nR0
>   n0 -->|"out 5"| n2
>   n2 -->|"exa"| n3
>   nR1(("res")):::res
>   n3 -->|"out"| nR1
>   classDef data fill:#e8dcf5,stroke:#7b52ab,color:#000
>   classDef blend fill:#dceefb,stroke:#3a7bbf,color:#000
>   classDef clean fill:#d9f2e6,stroke:#2e8b57,color:#000
>   classDef model fill:#ffe7c2,stroke:#d4860b,color:#000
>   classDef score fill:#fff6b3,stroke:#b8a400,color:#000
>   classDef eval fill:#fcd9d9,stroke:#c0392b,color:#000
>   classDef util fill:#eeeeee,stroke:#777,color:#000
>   classDef port fill:#ffffff,stroke:#999,stroke-dasharray:3 3,color:#555
>   classDef res fill:#ffffff,stroke:#333,stroke-width:2px,color:#000
> ```

<!-- /RM-CANVAS -->

### ⑨ กราฟ + ตีความ
| อยากรู้ | กราฟ | ทำไมกราฟนี้ |
|---|---|---|
| การกระจายของตัวเลข 1 ตัว | histogram / boxplot | เห็นรูปร่าง (เบ้/สมมาตร) และ outlier |
| ตัวเลขเทียบระหว่างกลุ่ม | boxplot แยกกลุ่ม | เห็นทั้งค่ากลางและการกระจายของแต่ละกลุ่ม |
| จำนวน/สัดส่วนในแต่ละหมวด | bar / stacked bar 100% | หมวดหมู่ไม่มีลำดับ ต้องเทียบความสูง |
| ความสัมพันธ์ตัวเลข 2 ตัว | scatter | เห็นทิศทาง ความแรง และรูปแบบไม่เชิงเส้น |
| หลายตัวพร้อมกัน | correlation heatmap | สรุป r ทุกคู่ในภาพเดียว |

> [!warning] correlation ≠ causation · r วัดแค่ความสัมพันธ์ **เชิงเส้น** (r ≈ 0 อาจยังสัมพันธ์แบบโค้งได้)

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: กราฟ = Results → Visualizations ของ res ข้อมูล · Correlation Matrix → mat
> ```mermaid
> flowchart LR
>   n0["Multiply"]:::util
>   n1["Correlation Matrix"]:::eval
>   n0 -->|"out 8"| n1
>   nR0(("res")):::res
>   n1 -->|"mat"| nR0
>   classDef data fill:#e8dcf5,stroke:#7b52ab,color:#000
>   classDef blend fill:#dceefb,stroke:#3a7bbf,color:#000
>   classDef clean fill:#d9f2e6,stroke:#2e8b57,color:#000
>   classDef model fill:#ffe7c2,stroke:#d4860b,color:#000
>   classDef score fill:#fff6b3,stroke:#b8a400,color:#000
>   classDef eval fill:#fcd9d9,stroke:#c0392b,color:#000
>   classDef util fill:#eeeeee,stroke:#777,color:#000
>   classDef port fill:#ffffff,stroke:#999,stroke-dasharray:3 3,color:#555
>   classDef res fill:#ffffff,stroke:#333,stroke-width:2px,color:#000
> ```

<!-- /RM-CANVAS -->

## ตัวอย่างผลจริง (T01, ข้อมูล tips)
- `total_bill`: mean 19.79 > median 17.80, skew 1.13 → **เบ้ขวา** · outlier (IQR) 9 ค่า
- median ตามวัน: Sun 19.63 สูงสุด · Fri 15.38 ต่ำสุด
- r(total_bill, tip) = 0.676 → สัมพันธ์เชิงบวกค่อนข้างแรง (บิลใหญ่ ทิปมาก) แต่ไม่ได้แปลว่าบิลใหญ่ "ทำให้" ทิปมาก

## กับดัก
- join แล้วแถวเพิ่มโดยไม่สังเกต (key ซ้ำในตาราง lookup)
- ใช้ mean อธิบายข้อมูลเบ้ (ควรอ้าง median ด้วย)
- กราฟเส้นกับหมวดหมู่ที่ไม่มีลำดับ
- ลืมบอกว่ากรองแล้วเหลือกี่แถว

## โครงคำตอบ
> ข้อมูลมี … แถว … คอลัมน์ · รวม 2 ไฟล์ด้วย append ได้ … แถว แล้ว join (left) กับ … ด้วย key … (จับคู่ไม่ได้ … แถว) ·
> กรองเงื่อนไข … เหลือ … แถว · จาก pivot พบว่า … สูงสุดที่ … (…) ต่ำสุดที่ … (…) · กราฟ … แสดงว่า … (รูปร่าง/ค่ากลาง/ความต่างระหว่างกลุ่ม)
