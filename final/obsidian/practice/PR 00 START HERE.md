---
title: PR 00 · START HERE — โจทย์ฝึก Lab ทีละขั้น
exam: Lab — จ. 12 ต.ค. 2569 09:00–12:00
tags: [final, lab, practice, MOC]
---

# 🏋️ PR 00 · START HERE
## โจทย์ฝึก Lab 9 ชุด — ไกด์ทำตามทีละขั้น แยก Python / RapidMiner

> [!info] วิธีใช้
> - แต่ละโจทย์มี **ไกด์ 2 ไฟล์** (Python และ RapidMiner) เป็นโจทย์และข้อมูลเดียวกัน
> - ไกด์บอกทีละขั้นว่า **พิมพ์/กดอะไร** แล้วจะได้ **ผลอะไร** — ตัวเลขทุกตัวมาจากการรันจริง
>   - Python: ผมรันโค้ดทุก cell (`final/practice/py_guides_*.py`)
>   - RapidMiner: ผมรัน process เฉลยด้วย batch runner (`final/practice/rm/P0X_solution.rmp`)
> - ไกด์ RapidMiner มี **🔌 ภาพ canvas หลังทุกขั้น** (mermaid) วาดจาก process เฉลยจริง: 🟨 = operator ที่เพิ่มในขั้นนั้น · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · Cross Validation / Optimize มีภาพ "ข้างใน" แยก (Training | Testing)
> - **ข้อมูล:** `final/practice/data/` — ส่วนใหญ่มาจากแหล่งภายนอกที่คุณยังไม่เคยใช้ (seaborn, UCI, R datasets) แหล่งที่มาอยู่ใน `final/practice/make_practice_data.py`
> - ทำแบบ **closed-book** ได้: อ่านแค่หัวข้อของแต่ละขั้น ลองทำเอง แล้วค่อยดูรายละเอียด

---

## 🗺️ โจทย์ทั้งหมด

| # | หัวข้อ | ข้อมูล | Python | RapidMiner | ครอบคลุม (Lab guideline) |
|---|---|---|---|---|---|
| 1 | Data Handling | ร้านอาหาร (tips) 3 ไฟล์ | [[PR 01 Data Handling (Python)\|Python]] | [[PR 01 Data Handling (RapidMiner)\|RapidMiner]] | import · **append · join · filter · aggregate · pivot** · charts · correlation/outlier |
| 2 | Preprocessing & PCA | นกเพนกวิน | [[PR 02 Preprocessing & PCA (Python)\|Python]] | [[PR 02 Preprocessing & PCA (RapidMiner)\|RapidMiner]] | missing · encoding · standardize/normalize · discretize · **PCA 2D** · split ไม่ leak |
| 3 | Imbalanced & SMOTE | มะเร็งเต้านม (IR 8.9) | [[PR 03 Imbalanced & SMOTE (Python)\|Python]] | [[PR 03 Imbalanced & SMOTE (RapidMiner)\|RapidMiner]] | baseline · **RUS · ROS · SMOTE ใน CV** · วิธีผิด vs ถูก |
| 4 | KNN · Baseline · CV · Optimize | ไวน์ 3 สายพันธุ์ | [[PR 04 KNN Baseline CV Optimize (Python)\|Python]] | [[PR 04 KNN Baseline CV Optimize (RapidMiner)\|RapidMiner]] | **Default Model** · ก่อน/หลัง scale · **Optimize Parameters + Log** · confusion matrix |
| 5 | Logistic & Threshold | เบาหวาน Pima | [[PR 05 Logistic Regression & Threshold (Python)\|Python]] | [[PR 05 Logistic Regression & Threshold (RapidMiner)\|RapidMiner]] | 0 → missing · **odds ratio** · **predict_proba / Create Threshold** |
| 6 | Tree vs Random Forest | โรคหัวใจ | [[PR 06 Decision Tree vs Random Forest (Python)\|Python]] | [[PR 06 Decision Tree vs Random Forest (RapidMiner)\|RapidMiner]] | **overfitting** · optimize depth · **RF** · importance |
| 7 | Regression | ค่ารักษาพยาบาล | [[PR 07 Regression (Python)\|Python]] | [[PR 07 Regression (RapidMiner)\|RapidMiner]] | mean baseline · **Linear Regression + coef** · **KNN regressor** · MAE/RMSE/R² |
| 8 | K-Means | ไวน์ (ไม่บอก label) | [[PR 08 K-Means Clustering (Python)\|Python]] | [[PR 08 K-Means Clustering (RapidMiner)\|RapidMiner]] | normalize · **elbow / silhouette / DB** · centroid · PCA plot |
| 9 | Association Rules | ใบเสร็จ 9,835 ใบ | [[PR 09 Association Rules (Python)\|Python]] | [[PR 09 Association Rules (RapidMiner)\|RapidMiner]] | transactions → items · **Apriori / FP-Growth** · support/confidence/**lift** |

---

## 📅 แนะนำลำดับ (เหลือ ส. 10 – อา. 11 ต.ค.)

> [!important] จุดอ่อนของคุณคือ **RapidMiner** (ไม่เคยสร้าง CV / Optimize / Tree / LogReg / k-Means / FP-Growth) → ทำฝั่ง RapidMiner ให้ครบก่อน ส่วน Python เลือกทำข้อที่ไม่เคยทำ
> | ช่วง | ทำ | เวลา |
> |---|---|---|
> | **ส. 10 คืนนี้** | PR 01 (RM) · PR 04 (RM) — สองไฟล์นี้สอนทักษะ RM ที่ใช้ทุกข้อ (Append/Join/Pivot · CV · Optimize · Log) | ~1.5 ชม. |
> | **อา. 11 เช้า** | PR 03 (RM) · PR 05 (RM) · PR 06 (RM) | ~2 ชม. |
> | **อา. 11 บ่าย** | PR 07 (RM) · PR 08 (RM) · PR 09 (RM) · PR 02 (RM) | ~2 ชม. |
> | **อา. 11 เย็น** | Python ที่ไม่เคยทำ: **PR 05** (threshold) · **PR 06** (RF) · **PR 07** (KNN regressor) · **PR 01** (merge/pivot) | ~1.5 ชม. |
> | **จ. 12 เช้า** | อ่าน [[LAB 09 Cheat Sheet]] + กับดักด้านล่าง | 20 นาที |

---

## ⚙️ ทักษะพื้นฐาน RapidMiner (อ่านก่อนไกด์แรก)

| ทำอะไร | วิธี |
|---|---|
| เปิดโปรแกรม | `~/App/ai-studio-2026.1.1/Altair/RapidMiner/AI Studio 2026.1.1/AI-Studio.sh` · Process ใหม่: **File → New Process → Blank** |
| วาง operator | แผง **Operators** (ซ้ายล่าง) → พิมพ์ชื่อในช่องค้นหา → **ลาก** มาวางบน canvas |
| ตั้งค่า | คลิก operator → แผง **Parameters** (ขวา) · ไม่เห็นพารามิเตอร์ → กด **Show advanced parameters** (ล่างแผง) |
| ต่อเส้น | ลากจากครึ่งวงกลม (port) ด้าน **ขวา** ของตัวหนึ่ง → port ด้าน **ซ้าย** ของอีกตัว · ลบเส้น: คลิกเส้น → `Delete` |
| ส่งผลไปดู | ต่อเส้นไปที่ port **res** บนขอบขวาของ canvas (ต่อได้หลายเส้น = หลายแท็บผล) |
| รัน | ปุ่ม ▶ **Run** (แถบบน) หรือ `F11` → โปรแกรมสลับไป **Results** · กลับมาแก้: ปุ่ม **Design** |
| Subprocess | operator ที่มีไอคอน ▣ (Cross Validation, Optimize Parameters) → **ดับเบิลคลิก** เข้าไปข้างใน · ออก: ปุ่ม ⬆ หรือชื่อ Process ด้านบน |
| ก๊อป operator | เลือก → `Ctrl+C` / `Ctrl+V` (ข้างใน subprocess ติดมาด้วย) |
| Edit List / Enumeration | พารามิเตอร์ที่เป็นรายการ (key attributes, aggregation attributes, partitions, log) → กดปุ่ม **Edit List…** → **Add Entry** |
| ดูข้อมูลกลางทาง | คลิกขวา operator → **Breakpoint After** → รันจะหยุดให้ดู |
| Error / คำเตือน | แท็บ **Problems** (ล่าง) บอกสาเหตุ · ไอคอนสีเหลือง/แดงที่ operator · มักมี **Quick Fix** |
| เปิด process เฉลย | **File → Import Process…** → `final/practice/rm/P0X_solution.rmp` |
| บันทึก/ส่ง | `Ctrl+S` (ใน repository) · ส่งเป็นไฟล์: **File → Export Process…** |

**ผลลัพธ์ใน Results view:**
- **ExampleSet**: แท็บ **Data** (ตาราง) · **Statistics** (min/max/avg/missing) · **Visualizations** (กราฟ)
- **PerformanceVector**: `accuracy: 96.11% +/- 4.57%` = ค่าเฉลี่ย ± sd ข้าม fold
- **ตาราง confusion matrix:** แถว = **pred.** · คอลัมน์ = **true** (กลับกับ sklearn)

---

## 🐛 กับดักที่เจอจริงตอนสร้างไกด์ (จำไว้ใช้ในห้องสอบ)

> [!warning] ทุกข้อพิสูจน์จากการรันจริงบนเครื่องคุณ
> 1. **Logistic Regression (H2O) ไม่ได้ตัดที่ 0.5** — prediction ใช้ threshold ที่ทำให้ F1 สูงสุด (P5 ได้ 0.314) → โจทย์กำหนด threshold ต้องใช้ **Create Threshold + Apply Threshold** เอง
> 2. **positive class** — ใน `Performance (Binominal Classification)` ให้ติ๊ก **manually set positive class** ทุกครั้ง (ไม่งั้นอาจคิด precision/recall ให้อีกคลาส) · `Set Positive Value` ทดลองแล้วไม่มีผลกับ Performance
> 3. **label 0/1** → ต้อง `Numerical to Binominal` ก่อน `Set Role` ไม่งั้นได้ regression
> 4. **multi-class (3 คลาส)** → ใช้ `Performance (Classification)` ไม่ใช่ Binominal
> 5. **regression + Cross Validation / Split Data** → sampling type `shuffled sampling` (stratified ใช้กับ label ตัวเลขไม่ได้)
> 6. **Linear Regression** default feature selection = **M5 prime** → ตั้ง `none`
> 7. **SMOTE Upsampling** ports = **exa** (เข้า) → **ups** (ออก) · ต้องอยู่ใน **Training pane**
> 8. **FP-Growth** — ต้องมี `Set Role` (id) + `Numerical to Binominal`/`Nominal to Binominal` (ติ๊ก **transform binominal** ถ้ามีคอลัมน์ Yes/No) · positive value = `true`
> 9. **Cluster Distance Performance** แสดง avg within centroid distance / Davies Bouldin **ติดลบ** → อ่านค่าสัมบูรณ์ · ต่ำ = ดี · ใน Log ใช้ value `avg_within_distance`
> 10. **ผล hold-out แกว่งตาม split** (P5: recall@0.5 แกว่ง 0.45–0.66 แค่เปลี่ยน split) → ตัวเลขของ Python กับ RapidMiner ต่างกันเล็กน้อยได้ (split คนละแบบ · z-score หาร n−1 vs n · mean vs median) ให้ดู **ทิศทาง** และเขียนอธิบาย

---

## 🔁 สร้างใหม่ทั้งหมด
```bash
cd ~/Projects/"data mining"/final/practice
../.venv/bin/python -I make_practice_data.py    # ข้อมูล
../.venv/bin/python py_guides_a.py              # ไกด์ Python 1–5 (รันโค้ดจริง)
../.venv/bin/python py_guides_b.py              # ไกด์ Python 6–9
../.venv/bin/python rm_guides.py                # สร้าง + รัน process เฉลย RapidMiner (Java 17 batch)
../.venv/bin/python rm_guides_md.py             # ไกด์ RapidMiner จากผลรันจริง
```

**กลับไปคลัง Lab →** [[LAB 00 START HERE]]
