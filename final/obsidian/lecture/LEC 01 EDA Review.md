---
title: LEC 01 · EDA Review
exam: Lecture — จ. 19 ต.ค. 2569 16:00–19:00
guideline: "Lecture ข้อ 1 — Summary statistics และการแปลผล · Basic data visualization และการเลือกกราฟ · Correlation และข้อจำกัดในการตีความ"
source: midterm EDA_69_1.pdf (57 pp) → โน้ตมิดเทอม 03 · Lab W14/HW_1/Hospital EDA
tags: [final, lecture, eda, summary-statistics, visualization, correlation]
---

# LEC 01 · EDA Review
### สถิติสรุป · เลือกกราฟ · correlation และข้อจำกัด

> [!abstract] guideline ข้อ 1 (3 หัวข้อ) — เนื้อหาเต็มอยู่ในโน้ตมิดเทอม บทนี้คือ **สรุป + สิ่งที่ต้องตีความเป็น**
> 1. **Summary statistics และการแปลผล** → [[#1.1 Summary Statistics + การแปลผล ⭐⭐⭐]]
> 2. **Basic data visualization และการเลือกกราฟให้เหมาะสม** → [[#1.2 เลือกกราฟให้เหมาะ ⭐⭐⭐]]
> 3. **Correlation และข้อจำกัดในการตีความ** → [[#1.3 Correlation + ข้อจำกัด ⭐⭐⭐⭐]]

**ลิงก์:** [[LEC 00 START HERE|หน้าหลัก Lecture]] · เต็ม: [[03 Exploratory Data Analysis (EDA)]] (มิดเทอม) · ถัดไป [[LEC 02 Preprocessing, Feature Selection & Leakage]] · Lab: [[LAB 02 Data Handling & Visualization#2.8 Basic Charts + การตีความ ⭐⭐⭐]]

---

## 1.1 Summary Statistics + การแปลผล ⭐⭐⭐

ตารางสูตรเต็ม: [[03 Exploratory Data Analysis (EDA)#3.3 Phase 1: Statistical Summary ⭐⭐ (สูตรที่ออกแน่)]]

| กลุ่ม | ค่า | อ่านว่า |
|---|---|---|
| คุณภาพข้อมูล | count, missing, outlier | ข้อมูลครบไหม มีค่าแปลกไหม |
| แนวโน้มสู่ศูนย์กลาง | **mean · median · mode** | ค่า "ทั่วไป" |
| การกระจาย | range · variance · **SD** · CV = SD/mean | แกว่งมากแค่ไหน (CV เทียบข้ามหน่วยได้) |
| รูปร่าง | **Q1, Q2, Q3, IQR = Q3 − Q1** · **skewness** | เบ้ไหม มี outlier ไหม |

> [!important] ⭐⭐ กฎการแปลผลที่ต้องเขียนได้
> - **mean > median → เบ้ขวา (right/positive skew)** — มีค่าสูงมาก ๆ ดึงหาง (รายได้, ราคาบ้าน, capital-gain) · mean < median → เบ้ซ้าย
> - เกณฑ์ skewness: |s| < 0.5 เกือบสมมาตร · 0.5–1 ปานกลาง · ≥ 1 เบ้มาก ([[03 Exploratory Data Analysis (EDA)#3.4 Distribution Shape ⭐ (ทำไม skewed ต้องใช้ Median)]])
> - **เบ้/มี outlier → ใช้ median และ IQR** สรุปข้อมูล (และ impute) · สมมาตร → mean และ SD
> - **outlier:** นอก $[Q_1-1.5\,IQR,\ Q_3+1.5\,IQR]$ ([[03 Exploratory Data Analysis (EDA)#Outlier Detection ⭐⭐ (สูตรคำนวณได้)]])
> - **SD = 0** (ค่าคงที่) → ตัด attribute ทิ้งได้ (ไม่ให้ข้อมูล)
> - categorical: ใช้ **mode + ความถี่/สัดส่วน** · target → ดู **สัดส่วนคลาส** ทุกครั้ง (imbalanced?)

> [!example] ⭐ ตัวอย่างการแปลผล (ข้อมูลจริงที่ใช้ใน Lab)
> **Boston medv:** mean 22.55 · median 21.2 · SD 9.22 · skew **1.10** · max 50 (16 หลังพอดี)
> → *"ราคาบ้านเบ้ขวา (mean > median, skew > 1) มีบ้านราคาสูงจำนวนหนึ่ง · มีบ้าน 16 หลังที่ราคา = 50 พอดี ซึ่งน่าจะเป็นค่าที่ถูกตัดเพดาน (censored) ไม่ใช่ราคาจริง · ควรใช้ median เป็นตัวแทนราคาทั่วไป"*
> **Churn:** MonthlyCharges กลุ่ม churn mean 74.4 vs ไม่ churn 61.3 · target No 73.5% / Yes 26.5% → *"ไม่สมดุล ต้องระวัง accuracy"*

> [!example]- 🧮 Drill: ข้อมูล 2, 4, 4, 5, 7, 9, 30
> mean = 61/7 = **8.71** · median = **5** · mode = **4** · Q1 = 4, Q3 = 9 (วิธีมัธยฐานครึ่ง) → IQR = **5** · fence บน = 9 + 7.5 = **16.5** → **30 เป็น outlier**
> mean > median มาก → **เบ้ขวา** เพราะ 30 ดึงค่าเฉลี่ย → สรุปด้วย median 5 ดีกว่า mean 8.71

---

## 1.2 เลือกกราฟให้เหมาะ ⭐⭐⭐

ตารางเต็ม + ตัวอย่าง: [[03 Exploratory Data Analysis (EDA)#🎯 ตารางเลือกกราฟ]]

| อยากรู้ | ตัวแปร | กราฟ |
|---|---|---|
| การกระจาย / เบ้ไหม | 1 numeric | **Histogram** (เลือกจำนวน bin ให้เหมาะ) |
| outlier / เทียบการกระจายหลายกลุ่ม | numeric (× category) | **Boxplot** |
| จำนวนแต่ละหมวด | 1 categorical | **Bar chart** |
| ความสัมพันธ์ 2 ตัวเลข | 2 numeric | **Scatter plot** (+ สีตามคลาส) |
| ความสัมพันธ์หลายตัวพร้อมกัน | หลาย numeric | **Correlation heatmap** · pairplot |
| แนวโน้มตามเวลา/ลำดับ | time / ordered | **Line plot** (เช่น elbow, metric vs k) |
| 2 categorical | 2 categorical | stacked/grouped bar · contingency table |
| มิติสูง → ดูโครงสร้าง | หลาย numeric | **PCA scatter PC1 × PC2** ([[LEC 03 PCA]]) |

> [!warning] ข้อผิดพลาดที่พบบ่อย
> - เทียบกลุ่มขนาดต่างกันด้วยจำนวน (count) → ต้องใช้ **สัดส่วน / density (normalize)**
> - pie chart หลายหมวด → อ่านยาก ใช้ bar แทน
> - scatter **ไม่บอกความแรง** ของความสัมพันธ์ ต้องดู r (สไลด์ EDA: *"Not indicates the strength of relationship"*)

---

## 1.3 Correlation + ข้อจำกัด ⭐⭐⭐⭐

สูตร + เกณฑ์: [[03 Exploratory Data Analysis (EDA)#3.7 Bivariate: Numerical vs Numerical ⭐⭐]]
$$r=\frac{\text{Cov}(X,Y)}{s_Xs_Y}\in[-1,1]\qquad |r|>0.7\text{ strong}\cdot 0.3\text{–}0.7\text{ moderate}\cdot <0.3\text{ weak}$$

> [!danger] ⭐⭐⭐ ข้อจำกัดของ correlation — guideline ระบุ "ข้อจำกัดในการตีความ" ตรง ๆ
> 1. **Correlation ≠ Causation** — r สูงไม่ได้บอกว่า X เป็นเหตุของ Y (อาจมีตัวแปรที่สามเป็นเหตุของทั้งคู่ หรือบังเอิญ) · เช่น ชั่วโมงทำงานสัมพันธ์กับรายได้ ≠ ทำงานมากทำให้รวย
> 2. **วัดเฉพาะความสัมพันธ์เชิงเส้น** — $y=x^2$ มีความสัมพันธ์ชัดแต่ $r\approx 0$ → **ต้องดู scatter ประกอบเสมอ**
> 3. **ไวต่อ outlier** — จุดเดียวสร้าง/ทำลาย r ได้
> 4. **range restriction / กลุ่มย่อย** — ความสัมพันธ์ในแต่ละกลุ่มอาจต่างจากรวมทั้งหมด (📚 Simpson's paradox)
> 5. **r ไม่ใช่ความชัน** — r = 0.9 ไม่ได้แปลว่า y เพิ่ม 0.9 ต่อ x · บอกแค่ "ความแน่นรอบเส้นตรง"
> 6. ใช้กับ **ตัวเลข** — categorical ใช้ contingency table / χ² แทน

> [!important] ⭐ การใช้ correlation ในงานจริง (สไลด์ EDA p.43)
> - **predictor สัมพันธ์กันเองสูง** (Boston: rad–tax **0.91**, churn: tenure–TotalCharges **0.83**) → **multicollinearity** → เก็บตัวเดียว / รวม / regularization ([[09 Regression Analysis#Assumption 2 · No Multicollinearity ⭐⭐⭐]])
> - **predictor สัมพันธ์กับ target สูง** (Boston: lstat **−0.738**, rm **+0.696**) → ตัวแปรที่น่าใช้ทำนาย (filter feature selection — [[LEC 02 Preprocessing, Feature Selection & Leakage]])
> - **ทิศ:** tenure–churn **−0.35** → *"ลูกค้าเก่ามีแนวโน้มยกเลิกน้อยกว่า (สัมพันธ์ปานกลาง)"*

---

## ✅ Self-Test — LEC 01

> [!question]- Q1. รายได้ mean 45,000 median 32,000 บอกอะไร ควรรายงานค่าไหน
> **เบ้ขวา** (มีรายได้สูงมากบางคนดึง mean) → รายงาน **median** (และ IQR) เป็นตัวแทนรายได้ทั่วไป

> [!question]- Q2. ต้องการดูว่า tenure ต่างกันอย่างไรในแต่ละประเภทสัญญา ใช้กราฟอะไร
> **Boxplot** แยกตาม Contract (numeric × categorical) → เห็น median, IQR, outlier ของแต่ละกลุ่ม

> [!question]- Q3. r(ไอศกรีม, การจมน้ำ) = 0.85 สรุปว่ากินไอศกรีมทำให้จมน้ำได้ไหม
> **ไม่ได้** — correlation ≠ causation · มีตัวแปรที่สาม (**อากาศร้อน/ฤดูร้อน**) ทำให้ทั้งสองเพิ่มขึ้นพร้อมกัน

> [!question]- Q4. r(x, y) = 0.02 แต่ scatter เป็นรูปตัว U สรุปอย่างไร
> ไม่มีความสัมพันธ์ **เชิงเส้น** แต่มีความสัมพันธ์ **แบบไม่เชิงเส้น** ชัดเจน → Pearson r ไม่เหมาะ · ต้องดูกราฟ/ใช้โมเดลไม่เชิงเส้น

---

**กลับหน้าหลัก →** [[LEC 00 START HERE]] · **ถัดไป →** [[LEC 02 Preprocessing, Feature Selection & Leakage]]
