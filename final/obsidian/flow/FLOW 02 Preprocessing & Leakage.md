---
title: FLOW 02 · Preprocessing & Data Leakage
tags: [final, flow, preprocessing, leakage, scaling, encoding]
---

# FLOW 02 · Preprocessing & Data Leakage
> template: Python **T02** · RapidMiner **R02** · กลับ [[FLOW 00 START HERE]]

## โจทย์หน้าตาแบบนี้
*"จัดการ missing values"* · *"encode ตัวแปรหมวดหมู่"* · *"normalize / standardize"* · *"แบ่งช่วง (discretize)"* ·
*"สุ่มตัวอย่าง"* · *"แบ่งข้อมูลโดยไม่เกิด data leakage"* · *"เปรียบเทียบผลก่อนและหลัง preprocessing"*

```mermaid
flowchart TD
  A["ตรวจ missing / ชนิด / outlier<br/>(ทั้งตาราง = แค่ดู)"] --> B["ตัดคอลัมน์ที่ไม่ใช้ / leak"]
  B --> C["SPLIT train | test<br/>หรือกำหนด k-fold"]
  C --> D["fit บน train เท่านั้น:<br/>impute → encode → scale<br/>(→ SMOTE / feature selection)"]
  D --> E["transform test ด้วยค่าจาก train"]
  E --> F["โมเดล"]
  F --> G["ประเมิน: ก่อน vs หลัง preprocessing<br/>ด้วยโมเดลเดียวกัน folds เดียวกัน"]
```

> [!danger] กฎทองข้อเดียวของบทนี้
> **อะไรที่ "เรียนรู้ค่าจากข้อมูล" (mean, median, std, min/max, หมวดที่มี, PCA, SMOTE, การเลือก feature) ต้อง fit บน train เท่านั้น**
> แล้วเอาค่าที่ได้ไปใช้กับ test · Python ใช้ `Pipeline` · RapidMiner ใส่ใน **Training pane** ของ Cross Validation หรือ Apply Model (preprocessing model) กับ test

## ทีละขั้น

<!-- RM-CANVAS -->

> [!info]- 🖥️ วิธีอ่านภาพ RapidMiner ใต้แต่ละขั้น (สร้างจาก `R02_preprocessing.rmp` จริง)
> กล่อง = operator (บน: ชื่อบน canvas · ล่าง: ชนิด) · ⧉ = มี subprocess (ดับเบิลคลิกเข้าไป) · ป้ายบนเส้น = port ย่อ (exa = example set · mod = model · pre = preprocessing model · per = performance · lab = labelled data · tra = training set · tes = test set · out = output · par = partition ของ Split Data / parameter set ของ Optimize · thr = threshold · wei = weights · fre = frequent sets · rul = rules) · ◯ res = ต่อออกผลลัพธ์ · กล่องเส้นประ = port ขอบ pane · สี: 🟪 อ่านข้อมูล · 🟦 จัดการข้อมูล · 🟩 preprocessing · 🟧 โมเดล · 🟨 apply · 🟥 ประเมิน/validation · ⬜ utility · มีเฉพาะ operator ของขั้นนั้น (ไฟล์จริงมี operator อื่นต่ออยู่ด้วย)

<!-- /RM-CANVAS -->

### ① ตรวจ (ทั้งตารางได้ เพราะแค่ "ดู")
- ค่าว่างแฝง: `?`, `-`, ช่องว่าง, **ค่า 0 ที่เป็นไปไม่ได้** (BMI = 0, ความดัน = 0) → ต้องประกาศเป็น missing ก่อน ไม่งั้นโมเดลคิดว่า 0 คือค่าจริง
- ดู % missing ต่อคอลัมน์ → ตัดสินใจวิธีจัดการ
- **อยู่ที่:** T02 §1 · R02 res 1 (Statistics)

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: Read CSV → Declare Missing Value (? → ว่าง) → Set Role → Multiply
> ```mermaid
> flowchart LR
>   n0["Read CSV"]:::data
>   n1["Declare Missing Value"]:::clean
>   n2["Set Role"]:::blend
>   n3["Multiply"]:::util
>   n0 -->|"out"| n1
>   n1 -->|"exa"| n2
>   n2 -->|"exa"| n3
>   nR0(("res")):::res
>   n3 -->|"out 1"| nR0
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

### ② เลือกวิธีจัดการ missing
| วิธี | ใช้เมื่อ | ทำไม |
|---|---|---|
| ลบแถว | ว่างน้อยมาก (< 5%) และสุ่ม | ง่าย ไม่บิดข้อมูล แต่เสียแถว |
| ลบคอลัมน์ | ว่างเกินครึ่ง | เติมไปก็เดาเกือบทั้งคอลัมน์ |
| **median** | ตัวเลขเบ้/มี outlier | median ไม่ถูก outlier ดึง |
| mean | ตัวเลขสมมาตร | — |
| mode | หมวดหมู่ | ค่าที่พบบ่อยสุดเป็นการเดาที่ปลอดภัยสุด |
| ตามกลุ่ม | ค่าต่างกันชัดตามกลุ่ม (เช่น น้ำหนักตามสายพันธุ์) | แม่นกว่าค่ากลางรวม |

**ทำไมเติมด้วยค่าจาก train:** median ของทั้งตารางรวมข้อมูล test ไว้ด้วย = test "สอน" โมเดลทางอ้อม · **อยู่ที่:** T02 §2 · R02 §2

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: เติมค่าว่าง หรือ ตัดแถวที่ว่าง
> ```mermaid
> flowchart LR
>   n0["Multiply"]:::util
>   n1["Replace Missing Values"]:::clean
>   n2["Filter Examples (not missing)<br/><i>Filter Examples</i>"]:::blend
>   n0 -->|"out 2"| n1
>   nR0(("res")):::res
>   n1 -->|"exa"| nR0
>   n0 -->|"out 3"| n2
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

### ③ Outlier
- ตรวจด้วย IQR: < Q1 − 1.5·IQR หรือ > Q3 + 1.5·IQR
- **ไม่ต้องลบเสมอ:** outlier ที่เป็นค่าจริง (คนรายได้สูงจริง) มีข้อมูล · ลบเฉพาะที่เป็นข้อผิดพลาด หรือ clip เมื่อโมเดลไวต่อค่าสุดขั้ว (linear, KNN)
- **อยู่ที่:** T02 §3 · R02 §3

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: Detect Outlier ใช้ระยะทาง → เลือกเฉพาะตัวเลข + เติมค่าว่างก่อน → กรอง outlier = false
> ```mermaid
> flowchart LR
>   n0["Multiply"]:::util
>   n1["Select Attributes (numeric)<br/><i>Select Attributes</i>"]:::blend
>   n2["Replace Missing (outlier)<br/><i>Replace Missing Values</i>"]:::clean
>   n3["Detect Outlier (Distances)"]:::clean
>   n4["Filter Examples (no outlier)<br/><i>Filter Examples</i>"]:::blend
>   n0 -->|"out 4"| n1
>   n1 -->|"exa"| n2
>   n2 -->|"exa"| n3
>   n3 -->|"exa"| n4
>   nR0(("res")):::res
>   n4 -->|"exa"| nR0
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

### ④ Encoding
| ชนิด | วิธี | ทำไม |
|---|---|---|
| หมวดหมู่ไม่มีลำดับ (สี, เมือง) | **one-hot / dummy** | ถ้าใส่ 1, 2, 3 โมเดลจะคิดว่า "เมือง 3 > เมือง 1" ซึ่งไม่มีความหมาย |
| หมวดหมู่มีลำดับ (low < mid < high) | ordinal 0, 1, 2 | ลำดับมีความหมายจริง |
| 2 ค่า (yes/no) | 0/1 | — |
| linear / logistic regression | dummy **ตัดตัวแรก** (reference) | ไม่งั้นคอลัมน์ dummy รวมกัน = 1 เสมอ → collinear, coefficient ตีความไม่ได้ |

**อยู่ที่:** T02 §4 · R02 §4

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: Nominal to Numerical (dummy coding = one-hot)
> ```mermaid
> flowchart LR
>   n0["Multiply"]:::util
>   n1["Nominal to Numerical"]:::clean
>   n0 -->|"out 5"| n1
>   nR0(("res")):::res
>   n1 -->|"exa"| nR0
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

### ⑤ Scaling
| วิธี | สูตร | ใช้เมื่อ |
|---|---|---|
| **Standardization (z-score)** | (x − mean) / std → mean 0, std 1 | ค่าเริ่มต้นที่ดี · ทนต่อ outlier กว่า min-max |
| **Normalization (min-max)** | (x − min) / (max − min) → 0..1 | อยากได้ช่วงคงที่ · ข้อมูลไม่มี outlier รุนแรง |

**ทำไมต้อง scale:** โมเดลที่ใช้ **ระยะทาง** (KNN, K-Means) หรือ **gradient/regularization** (logistic) ให้น้ำหนักตามขนาดตัวเลข → ตัวแปรหลักหมื่น (รายได้) จะกลบตัวแปรหลักหน่วย (จำนวนบุตร)
**ไม่ต้อง scale:** Decision Tree / Random Forest (แบ่งด้วย threshold ทีละตัวแปร ไม่ใช้ระยะทาง)
**อยู่ที่:** T02 §5 · R02 §5

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: Normalize: Z-transformation vs range transformation
> ```mermaid
> flowchart LR
>   n0["Multiply"]:::util
>   n1["Normalize (Z)<br/><i>Normalize</i>"]:::clean
>   n2["Normalize (0-1)<br/><i>Normalize</i>"]:::clean
>   n0 -->|"out 6"| n1
>   nR0(("res")):::res
>   n1 -->|"exa"| nR0
>   n0 -->|"out 7"| n2
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

### ⑥ Discretization
| วิธี | ผล | ใช้เมื่อ |
|---|---|---|
| equal width | ช่วงกว้างเท่ากัน | ข้อมูลกระจายสม่ำเสมอ · ข้อมูลเบ้ → บางช่วงแทบว่าง |
| **equal frequency** | จำนวนต่อช่วงเท่ากัน | ข้อมูลเบ้ (รายได้) |
| กำหนดเอง | ตามความหมาย (เด็ก/ผู้ใหญ่/สูงอายุ) | มีเกณฑ์ทางธุรกิจ |

**ทำไมต้อง discretize:** association rules ใช้ได้แต่ item (ค่าหมวดหมู่) · บางครั้งทำให้ตีความง่ายขึ้น · **อยู่ที่:** T02 §6 · R02 §6

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: Discretize 3 แบบ
> ```mermaid
> flowchart LR
>   n0["Multiply"]:::util
>   n1["Discretize by Binning"]:::clean
>   n2["Discretize by Frequency"]:::clean
>   n3["Discretize by User Specification<br/><i>Discretize by User Spec.</i>"]:::clean
>   n0 -->|"out 8"| n1
>   nR0(("res")):::res
>   n1 -->|"exa"| nR0
>   n0 -->|"out 9"| n2
>   nR1(("res")):::res
>   n2 -->|"exa"| nR1
>   n0 -->|"out 10"| n3
>   nR2(("res")):::res
>   n3 -->|"exa"| nR2
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

### ⑦ Sampling
- **random** = สุ่มเฉย ๆ · **stratified** = รักษาสัดส่วนคลาสเท่าเดิม → ใช้เสมอเมื่อ label ไม่สมดุล (ไม่งั้น test อาจแทบไม่มีคลาสส่วนน้อย)
- **อยู่ที่:** T02 §7 · R02 §7

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: Sample · Sample (Stratified)
> ```mermaid
> flowchart LR
>   n0["Multiply"]:::util
>   n1["Sample (relative)<br/><i>Sample</i>"]:::blend
>   n2["Sample (Stratified)"]:::blend
>   n0 -->|"out 11"| n1
>   nR0(("res")):::res
>   n1 -->|"exa"| nR0
>   n0 -->|"out 12"| n2
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

### ⑧ ⭐ Split ไม่ leak + เทียบก่อน/หลัง
- **ลำดับที่ถูก:** split → fit preprocessing บน train → transform test
- **เทียบก่อน/หลัง ต้องคุมตัวแปร:** โมเดลเดียวกัน · folds เดียวกัน (seed เดียวกัน) · ต่างกันแค่ preprocessing → ความต่างของผลมาจาก preprocessing จริง
- **อยู่ที่:** T02 §8 · R02 §8 / §8b

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: Hold-out ไม่ leak: fit บน train → เส้น pre ส่ง 'ค่าที่เรียนจาก train' ไปใช้กับ test ผ่าน Apply Model
> ```mermaid
> flowchart LR
>   n0["Multiply"]:::util
>   n1["Split Data"]:::blend
>   n2["Replace Missing (train)<br/><i>Replace Missing Values</i>"]:::clean
>   n3["Normalize (train)<br/><i>Normalize</i>"]:::clean
>   n4["Apply Model (missing → test)<br/><i>Apply Model</i>"]:::score
>   n5["Apply Model (normalize → test)<br/><i>Apply Model</i>"]:::score
>   n0 -->|"out 13"| n1
>   n1 -->|"par 1"| n2
>   n2 -->|"exa"| n3
>   n2 -->|"pre"| n4
>   n1 -->|"par 2"| n4
>   n3 -->|"pre"| n5
>   n4 -->|"lab"| n5
>   nR0(("res")):::res
>   n3 -->|"exa"| nR0
>   nR1(("res")):::res
>   n5 -->|"lab"| nR1
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

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: ข้างใน Cross Validation: preprocessing อยู่ใน Training → Group Models มัดรวมกับโมเดล → Testing ใช้กับ test fold
> ทุก fold fit ค่าใหม่จาก training fold ของตัวเอง = ไม่ leak
> ```mermaid
> flowchart LR
>   subgraph S["CV kNN normalized · Cross Validation"]
>     direction LR
>     subgraph P0["Training"]
>       direction LR
>       p0x0["Replace Missing Values"]:::clean
>       p0x1["Nominal to Numerical"]:::clean
>       p0x2["Normalize"]:::clean
>       p0x3["k-NN"]:::model
>       p0x4["Group Models"]:::model
>       p0xL0(["tra"]):::port
>       p0xL0 --> p0x0
>       p0x0 -->|"exa"| p0x1
>       p0x1 -->|"exa"| p0x2
>       p0x2 -->|"exa"| p0x3
>       p0x0 -->|"pre"| p0x4
>       p0x1 -->|"pre"| p0x4
>       p0x2 -->|"pre"| p0x4
>       p0x3 -->|"mod"| p0x4
>       p0xP0(["mod"]):::port
>       p0x4 -->|"mod"| p0xP0
>     end
>     subgraph P1["Testing"]
>       direction LR
>       p1x0["Apply Model"]:::score
>       p1x1["Performance (Classification)"]:::eval
>       p1xL0(["mod"]):::port
>       p1xL0 --> p1x0
>       p1xL1(["tes"]):::port
>       p1xL1 --> p1x0
>       p1x0 -->|"lab"| p1x1
>       p1xP0(["per 1"]):::port
>       p1x1 -->|"per"| p1xP0
>     end
>     P0 ~~~ P1
>   end
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

### ⑨ Feature selection (ต้องอยู่ใน pipeline ด้วย)
- เลือก feature ด้วยทั้งตาราง = ใช้ความสัมพันธ์กับ label ใน test ช่วยเลือก → leak · **อยู่ที่:** T02 §9 · R02 §9

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: Weight by Information Gain → Select by Weights (top k)
> ```mermaid
> flowchart LR
>   n0["Multiply"]:::util
>   n1["Weight by Information Gain"]:::clean
>   n2["Select by Weights"]:::clean
>   n0 -->|"out 15"| n1
>   n1 -->|"exa"| n2
>   n1 -->|"wei"| n2
>   nR0(("res")):::res
>   n2 -->|"wei"| nR0
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

## ตัวอย่างผลจริง (T02, penguins, KNN k=5, 5-fold CV, macro F1)
| | F1 |
|---|---|
| Majority baseline | 0.2043 |
| KNN ไม่ scale | 0.7490 |
| KNN + z-score | **0.9904** |
| KNN + min-max | 0.9870 |

**อ่าน:** body_mass_g (หลักพัน) กลบ bill_depth (หลักสิบ) ในระยะทาง → ไม่ scale ได้ 0.749 · scale แล้วทุกตัวแปรมีน้ำหนักเท่ากัน → 0.990

## กับดัก
- `StandardScaler().fit_transform(X)` ทั้งตารางก่อน split → leak (มักดูไม่ต่าง แต่ **ผิดหลัก** = เสียคะแนน)
- ลืมค่า 0 ที่เป็น missing
- one-hot แล้วลืมทำแบบเดียวกันกับข้อมูลใหม่ (คอลัมน์ไม่ตรงกัน) → ใช้ preprocessing model / Pipeline เดิม
- scale label (ไม่ต้อง)

## โครงคำตอบ
> พบ missing ที่ … (…%) และค่า 0 ที่เป็นไปไม่ได้ใน … → เติมด้วย median เพราะ … เบ้ · encode … ด้วย one-hot เพราะไม่มีลำดับ ·
> standardize เพราะใช้ KNN ที่คิดระยะทางและตัวแปรมีหน่วยต่างกัน (… หลักพัน vs … หลักสิบ) · แบ่ง train/test แบบ stratified ก่อน แล้ว fit
> imputer/scaler บน train เท่านั้นเพื่อกัน data leakage · ผล: ก่อน scale F1 … → หลัง … (+…)
