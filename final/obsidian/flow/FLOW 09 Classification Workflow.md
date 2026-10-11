---
title: FLOW 09 · Classification Workflow ครบวงจร (Baseline → Models → Optimize → Compare → Select → Predict)
tags: [final, flow, workflow, baseline, cross-validation, grid-search]
---

# FLOW 09 · Classification Workflow ครบวงจร ⭐
> template: Python **T09** · RapidMiner **R09** · กลับ [[FLOW 00 START HERE]]
> โจทย์ใหญ่ของ Lab มักเป็นแบบนี้ · บทอื่น (FLOW 04–08) คือการเจาะทีละชิ้นของ flow นี้

## โจทย์หน้าตาแบบนี้
*"สร้าง workflow ตั้งแต่ preprocessing จนถึง evaluation"* · *"สร้าง baseline แล้วเปรียบเทียบ"* · *"ใช้ hold-out หรือ cross-validation"* ·
*"optimize parameters"* · *"เปรียบเทียบก่อนและหลัง optimization"* · *"ควรเลือกโมเดลใด เพราะอะไร"*

```mermaid
flowchart TD
  A["① ตรวจข้อมูล + กำหนด label / positive / metric"] --> B["② ตัด id / leak"]
  B --> C["③ วิธีประเมิน: hold-out หรือ k-fold CV<br/>(stratified · seed คงที่)"]
  C --> D["④ preprocessing ใน pipeline<br/>impute · one-hot · scale (เฉพาะ KNN/Logistic)"]
  D --> E["⑤ Baseline (majority)"]
  E --> F["⑥ โมเดล default: KNN · Logistic · Tree · RF"]
  F --> G["⑦ Optimize: GridSearch ด้วย CV บน train"]
  G --> H["⑧ ตาราง ก่อน vs หลัง optimize"]
  H --> I["⑨ เลือกโมเดล: metric + overfit + ตีความได้"]
  I --> J["⑩ confusion matrix + test ครั้งเดียว (hold-out)"]
  J --> K["⑪ fit ทั้งชุด → ทำนายข้อมูลใหม่"]
```

## ทีละขั้น

<!-- RM-CANVAS -->

> [!info]- 🖥️ วิธีอ่านภาพ RapidMiner ใต้แต่ละขั้น (สร้างจาก `R09_classification_workflow.rmp` จริง)
> กล่อง = operator (บน: ชื่อบน canvas · ล่าง: ชนิด) · ⧉ = มี subprocess (ดับเบิลคลิกเข้าไป) · ป้ายบนเส้น = port ย่อ (exa = example set · mod = model · pre = preprocessing model · per = performance · lab = labelled data · tra = training set · tes = test set · out = output · par = partition ของ Split Data / parameter set ของ Optimize · thr = threshold · wei = weights · fre = frequent sets · rul = rules) · ◯ res = ต่อออกผลลัพธ์ · กล่องเส้นประ = port ขอบ pane · สี: 🟪 อ่านข้อมูล · 🟦 จัดการข้อมูล · 🟩 preprocessing · 🟧 โมเดล · 🟨 apply · 🟥 ประเมิน/validation · ⬜ utility · มีเฉพาะ operator ของขั้นนั้น (ไฟล์จริงมี operator อื่นต่ออยู่ด้วย)

<!-- /RM-CANVAS -->

### ① กำหนด label · positive class · metric ก่อนเริ่ม
- **ทำไมก่อน:** metric คือ "กติกาการแข่ง" — ต้องตั้งก่อนเห็นผล ไม่งั้นจะเลือก metric ที่ทำให้โมเดลที่ชอบดูดี
- สมดุล → accuracy ได้ · ไม่สมดุล → F1 / recall · ดู [[FLOW 04 Imbalanced Classification]]

### ② ตัด id / leak · ③ เลือกวิธีประเมิน
| | hold-out | k-fold CV |
|---|---|---|
| ทำ | แบ่ง train/test ครั้งเดียว (เช่น 70/30) | แบ่ง k ส่วน วน k รอบ ทุกแถวเป็น validation 1 ครั้ง |
| ข้อดี | เร็ว · เหมือนสถานการณ์จริง | ค่าเสถียรกว่า · ใช้ข้อมูลคุ้ม · ได้ std |
| ข้อเสีย | ผลขึ้นกับการสุ่มครั้งเดียว | ช้ากว่า k เท่า |
| ใช้เมื่อ | ข้อมูลเยอะ | ข้อมูลน้อย/กลาง |

- **stratified:** รักษาสัดส่วนคลาสในทุกส่วน · **seed คงที่:** ทุกโมเดลถูกประเมินบนการแบ่ง **เดียวกัน** → เทียบกันได้ยุติธรรม
- train / validation / test: train = เรียน · validation = เลือก parameter · test = วัดครั้งสุดท้ายครั้งเดียว (ใน CV, fold ที่ถูกพักคือ validation)

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: Select Attributes ตัด id → Set Role → Multiply
> ```mermaid
> flowchart LR
>   n0["Read CSV"]:::data
>   n1["Select Attributes"]:::blend
>   n2["Set Role"]:::blend
>   n3["Multiply"]:::util
>   n0 -->|"out"| n1
>   n1 -->|"exa"| n2
>   n2 -->|"exa"| n3
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

### ④ preprocessing ใน pipeline
- **ทำไม:** ทุก fold ต้อง fit imputer/scaler ใหม่จาก training fold ของตัวเอง (ดู [[FLOW 02 Preprocessing & Leakage]])
- scale เฉพาะโมเดลที่ใช้ระยะทาง/gradient (KNN, Logistic) · Tree/RF ไม่ต้อง

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: ข้างใน CV kNN: Replace Missing → Nominal to Numerical → Normalize → k-NN → Group Models
> ```mermaid
> flowchart LR
>   subgraph S["CV kNN · Cross Validation"]
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
>       p1x1["Performance (Binominal)"]:::eval
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

### ⑤ Baseline
- **ทำไม:** ตอบคำถาม "โมเดลเรียนรู้อะไรจริงไหม" · ไม่มี baseline พูดไม่ได้ว่า 85% ดีหรือไม่
- majority = ทายคลาสที่พบบ่อยสุดเสมอ (Python `DummyClassifier`, RapidMiner `Default Model`)
- ตัวอย่าง T09 (bank-data, pep): baseline accuracy **0.543** · F1 **0** (ไม่เคยทาย YES)

### ⑥ โมเดล default
- ใช้ค่าเริ่มต้นก่อน → ได้จุดเทียบสำหรับ "ก่อน optimize"
- ตัวอย่าง T09 (10-fold CV, F1): KNN 0.701 · Logistic 0.561 · Tree 0.833 · RF **0.838**

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: baseline + 4 โมเดล ด้วย CV ชุดเดียวกัน (seed เดียวกัน)
> ```mermaid
> flowchart LR
>   n0["Multiply"]:::util
>   n1["Multiply (default)<br/><i>Multiply</i>"]:::util
>   n2["CV Baseline<br/><i>Cross Validation</i><br/>⧉"]:::eval
>   n3["CV kNN<br/><i>Cross Validation</i><br/>⧉"]:::eval
>   n4["CV LogReg<br/><i>Cross Validation</i><br/>⧉"]:::eval
>   n5["CV Tree<br/><i>Cross Validation</i><br/>⧉"]:::eval
>   n6["CV RF<br/><i>Cross Validation</i><br/>⧉"]:::eval
>   n0 -->|"out 1"| n1
>   n1 -->|"out 1"| n2
>   nR0(("res")):::res
>   n2 -->|"per 1"| nR0
>   n1 -->|"out 2"| n3
>   nR1(("res")):::res
>   n3 -->|"per 1"| nR1
>   n1 -->|"out 3"| n4
>   nR2(("res")):::res
>   n4 -->|"per 1"| nR2
>   n1 -->|"out 4"| n5
>   nR3(("res")):::res
>   n5 -->|"per 1"| nR3
>   n1 -->|"out 5"| n6
>   nR4(("res")):::res
>   n6 -->|"per 1"| nR4
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

### ⑦ Optimize (GridSearch + CV บน train)
- ลองทุกชุด parameter → เลือกชุดที่ CV metric ดีที่สุด
- **ทำไมต้อง CV ไม่ใช่ test:** ถ้าเลือก parameter จาก test, ค่า test ที่รายงานจะ "ดีเกินจริง" เพราะเราจูนให้เข้ากับ test แล้ว
- parameter ที่ควร tune: KNN `k`, `weights` · Logistic `C`, `class_weight` · Tree `max_depth`, `min_samples_leaf`, `criterion` · RF `n_estimators`, `max_depth`

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: Optimize kNN / Tree → Log to Data (ตาราง) + par (ค่าที่ดีที่สุด)
> ```mermaid
> flowchart LR
>   n0["Multiply"]:::util
>   n1["Optimize Parameters (kNN)<br/><i>Optimize Parameters (Grid)</i><br/>⧉"]:::eval
>   n2["Log to Data (kNN)<br/><i>Log to Data</i>"]:::util
>   n3["Optimize Parameters (Tree)<br/><i>Optimize Parameters (Grid)</i><br/>⧉"]:::eval
>   n4["Log to Data (Tree)<br/><i>Log to Data</i>"]:::util
>   n0 -->|"out 2"| n1
>   nR0(("res")):::res
>   n2 -->|"exa"| nR0
>   nR1(("res")):::res
>   n1 -->|"par"| nR1
>   n0 -->|"out 3"| n3
>   nR2(("res")):::res
>   n4 -->|"exa"| nR2
>   nR3(("res")):::res
>   n3 -->|"par"| nR3
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

> [!example]+ 🖥️ RapidMiner: ข้างใน Optimize Tree
> ```mermaid
> flowchart LR
>   subgraph S["Optimize Parameters (Tree) · Optimize Parameters (Grid)"]
>     direction LR
>     subgraph P0["ข้างใน"]
>       direction LR
>       p0x0["CV opt Tree<br/><i>Cross Validation</i><br/>⧉"]:::eval
>       p0x1["Log"]:::util
>       p0xL0(["inp 1"]):::port
>       p0xL0 --> p0x0
>       p0x0 -->|"per 1"| p0x1
>       p0xP0(["per"]):::port
>       p0x1 -->|"thr 1"| p0xP0
>     end
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

### ⑧ ตาราง ก่อน vs หลัง ⭐
ตัวอย่าง T09 (F1):

| โมเดล | ก่อน | หลัง | เปลี่ยน | ค่าที่ได้ |
|---|---|---|---|---|
| KNN | 0.701 | 0.727 | +0.026 | k = 19, distance |
| Logistic | 0.561 | 0.593 | +0.032 | C = 1, balanced |
| **Decision Tree** | 0.833 | **0.876** | **+0.044** | gini, depth 6, leaf 5 |
| Random Forest | 0.838 | 0.842 | +0.004 | leaf 5 |

**อ่าน:** Tree ดีขึ้นมากสุดเพราะต้นไม้ default โตเต็ม (overfit) → จำกัด depth/leaf ช่วยมาก · RF แทบไม่เปลี่ยนเพราะ default ของ RF ดีอยู่แล้ว (การเฉลี่ยลด overfit ให้เอง) ·
Logistic ต่ำสุด → บ่งว่าความสัมพันธ์ใน bank-data น่าจะไม่เป็นเชิงเส้น/มี interaction ระหว่างตัวแปร ซึ่งต้นไม้จับได้เอง แต่ logistic (เส้นตรงใน log-odds) จับไม่ได้

### ⑨ เลือกโมเดล — ไม่ใช่แค่ตัวเลขสูงสุด
1. metric หลักสูงสุด (ต่างกันเกิน std ไหม? ถ้าต่างกันน้อยกว่า std ถือว่าพอ ๆ กัน)
2. ไม่ overfit (train vs validation ไม่ห่างมาก)
3. ตีความได้ (Tree อธิบายได้เป็นกฎ · RF/KNN ยากกว่า)
4. ต้นทุนของ FN/FP ในโจทย์
- ตัวอย่าง T09: เลือก **Decision Tree (optimized)** F1 0.876 — สูงสุดและอธิบายเป็นกฎได้

### ⑩ confusion matrix
- บอกว่าพลาดแบบไหน (FN หรือ FP) → เชื่อมกับโจทย์ธุรกิจ · hold-out: วัดบน test **ครั้งเดียว** ตอนจบ

### ⑪ fit ทั้งชุด → ทำนาย
- เลือกเสร็จแล้วใช้ข้อมูลทั้งหมด train โมเดลสุดท้าย (ได้ข้อมูลมากสุด) · ข้อมูลใหม่ผ่าน pipeline เดียวกันอัตโนมัติ

<!-- RM-CANVAS -->

> [!example]+ 🖥️ RapidMiner: โมเดลสุดท้าย (fit ทั้งชุด) → ทำนายข้อมูลใหม่
> ```mermaid
> flowchart LR
>   n0["Multiply"]:::util
>   n1["Decision Tree (final)<br/><i>Decision Tree</i>"]:::model
>   n2["Read CSV (new)<br/><i>Read CSV</i>"]:::data
>   n3["Apply Model (new)<br/><i>Apply Model</i>"]:::score
>   n0 -->|"out 4"| n1
>   n1 -->|"mod"| n3
>   n2 -->|"out"| n3
>   nR0(("res")):::res
>   n3 -->|"lab"| nR0
>   nR1(("res")):::res
>   n3 -->|"mod"| nR1
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

## กับดัก
- ไม่มี baseline · ใช้ accuracy กับข้อมูลไม่สมดุล
- แต่ละโมเดลใช้ split/seed ต่างกัน → เทียบไม่ได้
- tune ด้วย test · รายงานผล test หลายรอบแล้วเลือกตัวที่ดีสุด
- บอก "โมเดล A ดีกว่า" ทั้งที่ต่างกัน 0.005 แต่ std 0.05

## โครงคำตอบ (4 ขั้น)
1. **Process:** อ่าน → ตัด … → pipeline (impute median/mode + one-hot + z-score) → 10-fold stratified CV (seed …) → baseline + 4 โมเดล → GridSearch
2. **Settings:** metric หลัก F1 เพราะ … · grid: …
3. **Results:** ตาราง default / optimized (ค่าเฉลี่ย ± std)
4. **Interpretation:** baseline F1 … → ทุกโมเดลชนะ · … ดีสุด (…) · optimize ช่วย … มากสุดเพราะ … · เลือก … เพราะ … · confusion matrix: FN … FP … → …
