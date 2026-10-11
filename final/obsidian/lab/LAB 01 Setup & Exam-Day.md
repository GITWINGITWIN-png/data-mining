---
title: LAB 01 · Setup & Exam-Day
exam: Lab — จ. 12 ต.ค. 2569 09:00–12:00 · E11-S603 · โน้ตบุ๊กตัวเอง
tags: [final, lab, setup, rapidminer, exam-day]
---

# LAB 01 · Setup & Exam-Day
### เตรียมเครื่องให้พร้อม + แผน 3 ชั่วโมงในห้องสอบ + โครงรายงาน

**ลิงก์:** [[LAB 00 START HERE|หน้าหลัก Lab]] · ถัดไป [[LAB 02 Data Handling & Visualization]] · [[LAB 09 Cheat Sheet]]

> [!danger] ทำให้เสร็จ **ก่อนคืนวันอาทิตย์ 11 ต.ค.** — วันสอบไม่มีเวลาแก้เครื่อง
> ทุกข้อด้านล่างตรวจกับเครื่องคุณแล้ว (7 ต.ค.) · ข้อที่ยังไม่ผ่านมีแค่ **Operator Toolbox (SMOTE)**

---

## ✅ Checklist คืนนี้ (7 ต.ค.)

### 1. Python env สำหรับสอบ — `final/.venv` ✅ (สร้างให้แล้ว)

| แพ็กเกจ | เวอร์ชัน |
|---|---|
| pandas / numpy | 3.0.6 / 2.5.3 |
| scikit-learn | 1.9.1 |
| imbalanced-learn (SMOTE) | 0.14.2 |
| mlxtend (Apriori/FP-Growth) | 0.25.0 |
| matplotlib / seaborn | 3.11.2 / 0.13.2 |
| xlrd / openpyxl | อ่าน .xls / .xlsx |

- **เลือก kernel:** ใน VS Code เปิด `.ipynb` → มุมขวาบน **Select Kernel** → **Jupyter Kernel…** → **Python (dm-exam)** · ใน Jupyter Lab: Kernel → Change Kernel → Python (dm-exam)
- **ทดสอบ:** cell แรกรัน `import pandas, sklearn, imblearn, mlxtend; print(sklearn.__version__)` ต้องได้ `1.9.1`
- ⚠️ อย่าใช้ `.venv` ที่ root ของโปรเจกต์ (เสีย — symlink ชี้ไป snap ที่ไม่มีแล้ว) และ `HW1/.venv` (ไม่มี imblearn)
- **ถ้า env พัง สร้างใหม่ได้ใน 1 นาที (ไม่ต้องใช้เน็ต เพราะไฟล์อยู่ใน cache ของ uv แล้ว):**
  ```bash
  cd ~/Projects/"data mining"          # ~ ต้องอยู่นอกเครื่องหมายคำพูด ไม่งั้น shell ไม่แปลงเป็น home
  env -u VIRTUAL_ENV uv venv final/.venv --python /usr/bin/python3
  env -u VIRTUAL_ENV uv pip install --python final/.venv/bin/python pandas numpy matplotlib seaborn \
      scikit-learn imbalanced-learn mlxtend xlrd openpyxl jupyter ipykernel nbconvert
  final/.venv/bin/python -m ipykernel install --user --name dm-exam --display-name "Python (dm-exam)"
  ```

### 2. RapidMiner (Altair AI Studio 2026.1.1) — ✅ Operator Toolbox ติดตั้งแล้ว (ตรวจ 10 ต.ค.)

- เปิดโปรแกรม: `~/App/ai-studio-2026.1.1/Altair/RapidMiner/AI Studio 2026.1.1/AI-Studio.sh`
- **ติดตั้ง Operator Toolbox** (มี operator **SMOTE Upsampling** — core ไม่มี SMOTE):
  1. เมนู **Extensions → Marketplace (Updates and Extensions)…**
  2. แท็บ Search → พิมพ์ **Operator Toolbox** → ติ๊ก → **Install** (ต้องต่อเน็ต และอาจต้อง login บัญชี Altair/RapidMiner)
  3. รีสตาร์ตโปรแกรม → ช่องค้นหาในแผง **Operators** พิมพ์ `SMOTE` → ต้องเจอ **SMOTE Upsampling**
  4. Import ไฟล์ `final/mock_lab/recipes/smote_cv_REQUIRES_OPERATOR_TOOLBOX.rmp` แล้วกด ▶ ต้องรันได้
- ถ้าติดตั้งไม่ได้: ใช้ทางสำรอง ROS ([[LAB 03 Preprocessing Recipes#3.5 Sampling & SMOTE ⭐⭐⭐]]) หรือทำข้อ SMOTE ใน Python (ถ้าโจทย์อนุญาต)
- **ถ้าโปรแกรมเปิดไม่ขึ้น** (เช่นหลังอัปเดต Java): สั่งเปิดด้วย Java 17
  ```bash
  JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 ~/App/ai-studio-2026.1.1/Altair/RapidMiner/"AI Studio 2026.1.1"/AI-Studio.sh
  ```
- **Import recipe ทั้งหมดเก็บไว้ใน repository** (ใช้เป็นแม่แบบตอนสอบถ้าเปิดไฟล์ได้): File → **Import Process…** → เลือกไฟล์ใน `final/mock_lab/recipes/` → File → Save Process as… → Local Repository / `final_recipes`

| ไฟล์ recipe (ทุกไฟล์รันทดสอบแล้ว) | สอนอะไร | อยู่ในบท |
|---|---|---|
| `join_append_pivot.rmp` | Join (left) · Append · Replace Missing · Aggregate · Generate Attributes · Pivot | [[LAB 02 Data Handling & Visualization\|LAB 02]] |
| `pca_bank.rmp` | Select Attributes · Numerical to Binominal · Set Role · Normalize · PCA | [[LAB 03 Preprocessing Recipes\|LAB 03]] |
| `knn_cv_normalize.rmp` | Cross Validation + Normalize ใน Training pane + Group Models | LAB 03–04 |
| `baseline_vs_knn.rmp` | Default Model (majority) vs k-NN ด้วย folds เดียวกัน | [[LAB 04 Workflow, Baseline & Evaluation\|LAB 04]] |
| `optimize_knn_k.rmp` | Optimize Parameters (Grid) + Log + Log to Data | LAB 04 |
| `logreg_threshold.rmp` | Split Data · Logistic Regression · Create/Apply Threshold | [[LAB 05 Supervised Models\|LAB 05]] |
| `tree_vs_rf.rmp` | Decision Tree vs Random Forest ใน CV | LAB 05 |
| `linreg_boston.rmp` | Linear Regression (feature selection = none) · Performance (Regression) | LAB 05 |
| `kmeans_utilities.rmp` | k-Means · Cluster Distance Performance | [[LAB 06 Clustering & Association\|LAB 06]] |
| `elbow_kmeans.rmp` | Optimize Parameters ครอบ k-Means → elbow | LAB 06 |
| `fpgrowth_beautyco.rmp` | Read Excel · Numerical to Binominal · FP-Growth · Create Association Rules | LAB 06 |
| `smote_cv_REQUIRES_OPERATOR_TOOLBOX.rmp` | SMOTE Upsampling ใน Training pane | LAB 03 |

### 3. Export รายงานเป็น PDF — ทางที่ทดสอบแล้วว่าเร็วและไม่พัง ✅

```bash
# ใน terminal (รันโค้ดทั้งหมดใหม่ + ได้ไฟล์ .html)
cd โฟลเดอร์งาน
~/Projects/"data mining"/final/.venv/bin/jupyter nbconvert --to html --execute 6710503739_lab.ipynb
firefox 6710503739_lab.html      # → Ctrl+P → Destination: Save to PDF → Save
```
- หรือใน VS Code: ปุ่ม **…** บน notebook → **Export** → HTML → เปิดใน Firefox → Print → Save to PDF
- ❌ **อย่าใช้ `--to pdf`** ในวันสอบ — ต้องใช้ XeLaTeX + pandoc + แพตช์ (เคยทำใน HW แต่ใช้เวลาและพังง่าย)
- ภาษาไทยใน markdown cell แสดงใน HTML/Firefox ได้ปกติ (ทดสอบแล้ว)

### 4. อื่น ๆ
- [ ] ชาร์จแบต 100% + เอาสายชาร์จไป · ปิด auto-update ของระบบ
- [ ] ทดลอง screenshot: `PrtSc` (ทั้งจอ) / `Shift+PrtSc` (เลือกพื้นที่) → ไฟล์ไปอยู่ `~/Pictures/Screenshots`
- [ ] (ถ้าสอบเปิดไฟล์ได้) เปิด Obsidian vault นี้ไว้ + เปิด [[LAB 09 Cheat Sheet]] เป็นแท็บแรก
- [ ] ทำ Mock 1 แบบจับเวลา 3 ชม. อย่างน้อย 1 ครั้ง ([[LAB 08 Mock Exams]])

---

## RapidMiner — พื้นฐานที่ต้องคล่องก่อนเข้าห้อง

| เรื่อง | วิธี |
|---|---|
| หา operator | แผง **Operators** → พิมพ์ชื่อในช่องค้นหา (เร็วกว่าไล่ต้นไม้) → ลากวาง |
| ตั้งค่า | คลิก operator → แผง **Parameters** (ขวา) · ปุ่ม **Show advanced parameters** ถ้าหาพารามิเตอร์ไม่เจอ |
| ต่อเส้น | ลากจาก port ขวาของตัวหนึ่ง → port ซ้ายของอีกตัว · สีของ port/เส้นบอกชนิดข้อมูล (ExampleSet, Model, Performance ต่างสีกัน) — ต่อผิดชนิดจะต่อไม่ติดหรือขึ้น error |
| ชื่อ port ที่เจอบ่อย | `exa` example set · `ori` original · `pre` preprocessing model · `tra` training · `mod` model · `unl` unlabelled · `lab` labelled · `per` performance · `tes` test set · `res` result (ขอบขวาของ canvas) |
| เข้า/ออก subprocess | ดับเบิลคลิก operator ที่มีไอคอน ▣ (Cross Validation, Optimize, Subprocess) · ออกด้วยปุ่ม ⬆ หรือ breadcrumb ด้านบน |
| รัน | ▶ (F11) · ผลอยู่ใน **Results** view (สลับ Design ↔ Results ด้วยปุ่มแถบบนสุด) · ทุก port ที่ต่อไป `res` จะเป็น 1 แท็บผล |
| ดูข้อมูลกลางทาง | คลิกขวา operator → **Breakpoint After** |
| ⚠️ สีเหลือง/แดงที่ operator | **Problems** แท็บล่าง บอกสาเหตุ + มี Quick Fix (เช่น "insert Numerical to Binominal") |
| บันทึก | Ctrl+S (เก็บใน repository) · ส่งเป็นไฟล์: **File → Export Process…** → `.rmp` |
| ส่งข้อมูลผลออก | ต่อ `Write CSV` / `Write Excel` หรือในแท็บผล → ปุ่ม export |

> [!warning] error ที่เจอบ่อยที่สุดใน RapidMiner + วิธีแก้
> | ข้อความ / อาการ | สาเหตุ | แก้ |
> |---|---|---|
> | *"…does not have sufficient capabilities for numerical label"* / ได้ regression แทน classification | label เป็นตัวเลข 0/1 | `Numerical to Binominal` ที่ label ก่อน `Set Role` |
> | *"…does not have capabilities for polynominal attributes"* (k-NN, Logistic, SMOTE) | มี attribute ข้อความ | `Nominal to Numerical` (dummy coding) |
> | *"A performance measuring operator is required to execute Cross Validation"* | ไม่ได้ต่อ `per` ใน Testing pane | ต่อ Performance → port `per` ขอบขวา |
> | *"The attribute 'X' does not exist"* | ชื่อผิด/มีช่องว่าง (RapidMiner ตัดช่องว่างท้ายชื่อคอลัมน์ Excel ให้เอง) | เลือกจาก dropdown แทนพิมพ์ |
> | precision/recall ดูกลับด้าน | positive class เป็นอีกคลาส | ใน `Performance (Binominal Classification)` ติ๊ก **manually set positive class** → ใส่ positive class |
> | ผลใน CV ดีเกินจริง | Normalize/SMOTE/PCA อยู่นอก Training pane | ย้ายเข้าไปใน CV + `Group Models` |

---

## ⏱️ แผน 3 ชั่วโมงในห้องสอบ (09:00–12:00)

| เวลา | ทำอะไร |
|---|---|
| **09:00–09:10** | อ่าน **ทุกข้อ** ก่อน · จดว่าแต่ละข้อ **บังคับเครื่องมือ** อะไร (RapidMiner / Python) · **ต้องส่งอะไร** (.rmp / .xml / .ipynb / PDF / screenshot) · คะแนนแต่ละข้อ |
| **09:10–09:15** | สร้างโฟลเดอร์ `6710503739_final_lab/` · copy ข้อมูลเข้าไป · เปิด notebook ใหม่ วาง **template cell** จาก [[LAB 09 Cheat Sheet#1. Template cell แรกของ notebook]] · RapidMiner: Import Data เข้า repository |
| **09:15–11:15** | ทำทีละข้อ ตามลำดับ **คะแนนมาก + มั่นใจ** ก่อน · ทุกข้อทำครบ 4 อย่าง: **process → ตั้งค่า → ผล → คำตอบ/ตีความ** (เขียนคำตอบทันทีที่ได้ผล อย่าเก็บไว้ทีหลัง) · **ติดเกิน 15 นาที → ข้ามก่อน** |
| ทุก ~15 นาที | **Ctrl+S** ทั้งสองโปรแกรม · RapidMiner Export Process เป็นระยะ · screenshot process + ผลของข้อที่เสร็จเก็บใส่โฟลเดอร์ |
| **11:15–11:40** | กลับไปข้อที่ข้าม · ตรวจว่าทุกข้อมี "ตีความ" · **Restart & Run All** notebook ให้แน่ใจว่ารันได้จากต้น |
| **11:40–11:55** | Export รายงาน (HTML → PDF) · ตั้งชื่อไฟล์ตามโจทย์ · ตรวจว่าไฟล์เปิดได้ |
| **11:55** | ส่ง |

---

## 📄 โครงรายงานต่อข้อ (ตามรูปแบบส่งงาน W13: *"process screenshots, settings, result tables, PCA plot and answers"*)

```markdown
## ข้อ 2 — Optimized KNN

**Process:** ![screenshot ของ process](q2_process.png)   ← หรือบอกว่า process อยู่ในไฟล์ไหน
**Settings:** Normalize = Z-transformation (ใน Training pane) · Cross Validation 5 folds, stratified, seed 1992
              · Optimize k = 1…10 · main criterion = F1
**Results:**
| Rank | k | Accuracy | Recall | F1 |
|---|---|---|---|---|
| 1 | … | … | … | … |

**Answer / Interpretation:** best k = … เพราะ … · เทียบ baseline แล้ว F1 เพิ่มจาก … เป็น … ·
metric ที่สำคัญที่สุดคือ recall เพราะโจทย์ต้องการ "หาลูกค้าให้ได้มากที่สุด"
```

> [!tip] ในหัวข้อ Settings ให้เขียน **ทุกอย่างที่ทำให้คนอื่นทำซ้ำได้**: วิธี split/CV + จำนวน fold + seed · preprocessing (อยู่ตรงไหนของ workflow) · ค่าพารามิเตอร์ที่ใช้ · metric ที่ใช้เลือก

---

**ถัดไป →** [[LAB 02 Data Handling & Visualization]] · **กลับหน้าหลัก →** [[LAB 00 START HERE]]
