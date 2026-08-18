---
title: Exam Drills — ชุดฝึกทำข้อสอบ
chapter: 12
tags: [midterm, practice, drills]
---

# 12 · Exam Drills
### ชุดฝึกทำข้อสอบ — เขียนตามรูปแบบที่คาดว่าจะออกจริง

> [!warning] วิธีใช้ให้ได้ผล
> **ปิดเฉลยแล้วทำจริงบนกระดาษก่อน** อย่าเพิ่งกด — การอ่านเฉลยผ่าน ๆ ให้ความรู้สึกว่า "เข้าใจแล้ว" ทั้งที่ยังทำไม่ได้
> ข้อที่ทำผิด ให้กลับไปอ่านบทที่ลิงก์ไว้แล้ว **ทำใหม่อีกรอบในวันถัดไป**

> [!info] มิดเทอมคือ **Lecture + Lab (On-site) 30%**
> → มีทั้งข้อทฤษฎีและข้อปฏิบัติ ชุดนี้แบ่งเป็น **Part A ทฤษฎี** · **Part B คำนวณ** · **Part C ออกแบบ/SQL** · **Part D สถานการณ์**

**ลิงก์:** [[00 START HERE|หน้าหลัก]] · [[10 Formula Sheet]] · [[11 Glossary EN-TH]]

---

## Part A · ทฤษฎีและการจำแนก (ข้อสั้น)

> [!question]- A1. จงจำแนกว่าแต่ละข้อความเป็น Data / Information / Knowledge / Action
> (ก) `38.5°C` · (ข) "อุณหภูมิเฉลี่ยของผู้ป่วยในวอร์ดคือ 38.5°C" · (ค) "ผู้ป่วยที่มีไข้เกิน 38°C นานกว่า 3 วัน มักติดเชื้อแบคทีเรีย" · (ง) "สั่งตรวจเพาะเชื้อในผู้ป่วยที่ไข้เกิน 3 วัน"
>
> **เฉลย:** (ก) **Data** — ตัวเลขลอย ๆ · (ข) **Information** — มี context (เฉลี่ย, ของใคร) · (ค) **Knowledge** — เป็นกฎที่ใช้ตัดสินใจได้ · (ง) **Action** — เป็นคำสั่งให้ลงมือทำ
> → [[01 Introduction to Data Analytics#1.2 Data vs. Information vs. Knowledge ⭐ ออกสอบแน่]]

> [!question]- A2. จงจำแนกประเภท analytics ของแต่ละคำถาม
> (ก) "ไตรมาสที่แล้วสาขาไหนขายดีที่สุด" · (ข) "เดือนหน้ายอดขายจะเป็นเท่าไร" · (ค) "ทำไมยอดขายสาขาลาดพร้าวถึงตก" · (ง) "ควรจัดโปรโมชั่นอะไรกับลูกค้ากลุ่มนี้"
>
> **เฉลย:** (ก) **Descriptive** (*What happened?*) · (ข) **Predictive** (*What will happen?*) · (ค) **Diagnostic** (*Why did it happen?*) · (ง) **Prescriptive** (*What should we do?*)
> → [[01 Introduction to Data Analytics#1.3 Types of Analytics ⭐⭐ ออกสอบแน่นอนที่สุด]]

> [!question]- A3. จงระบุระดับการวัด (Nominal / Ordinal / Interval / Ratio) และสถิติที่ใช้ได้
> (ก) หมายเลขห้องเรียน · (ข) ระดับความพึงพอใจ (แย่/พอใช้/ดี/ดีมาก) · (ค) ปี พ.ศ. · (ง) รายได้ต่อเดือน
>
> **เฉลย:**
> (ก) **Nominal** — ใช้ mode, entropy, χ² test (ห้ามใช้ mean)
> (ข) **Ordinal** — ใช้ median, percentiles, rank correlation
> (ค) **Interval** — ไม่มีศูนย์แท้ (ปี 0 ไม่ได้แปลว่า "ไม่มีเวลา") → ใช้ mean, SD, Pearson แต่บอกว่า "2000 มากเป็น 2 เท่าของ 1000" ไม่ได้
> (ง) **Ratio** — มีศูนย์แท้ (0 บาท = ไม่มีรายได้) → ใช้ได้ทุกอย่างรวมถึง geometric mean
> → [[02 Data and Dataset Types#ตาราง Stevens' scale — 4 ระดับ (Nominal → Ordinal → Interval → Ratio) ⭐]]

> [!question]- A4. Noise กับ Outlier ต่างกันอย่างไร และแต่ละอย่างจัดการอย่างไร
> **เฉลย:**
> | | **Noise** | **Outlier** |
> |---|---|---|
> | ขนาด | เบี่ยงเบน **เล็ก ๆ สุ่ม ๆ** จากสัญญาณจริง | เบี่ยงเบน **อย่างมีนัยสำคัญ** โดดออกจากแนวโน้ม |
> | สาเหตุ | เซนเซอร์ไม่แม่น, ข้อจำกัดการวัด, สัญญาณรบกวน | กรอกผิด, ระบบขัดข้อง, **เหตุการณ์หายากแต่จริง** |
> | จัดการ | **Smoothing** (Binning / Regression / Clustering) | **Keep / Remove / Transform** ตามบริบท |
>
> ⚠️ **"Outliers should NOT be removed automatically. They must be analyzed using domain knowledge."**
> → [[04 Data Pre-processing#4.3 Noise vs. Outliers ⭐⭐ (guideline ข้อ 3.3 — ระบุชื่อคู่นี้ตรง ๆ)]]

> [!question]- A5. เขียนตาราง OLTP vs OLAP อย่างน้อย 6 ประเด็น
> **เฉลย:**
> | ประเด็น | OLTP | OLAP |
> |---|---|---|
> | การดำเนินการ | **Mostly updates** | **Mostly reads / read-only** |
> | ชนิด query | **Pre-defined** | **Ad-hoc** |
> | Data model | **Normalized** | **De-normalized** |
> | ข้อมูลย้อนหลัง | เก็บไม่นาน | **เก็บนาน** |
> | Optimize เพื่อ | **writes + small queries** | **queries ที่กินข้อมูลก้อนใหญ่** |
> | Transaction | **เล็กจำนวนมาก** | **query ยาวและซับซ้อน** |
> | ฐานข้อมูล | elementary data | **synthesized data จากหลายแหล่ง** |
> → [[05 Data Warehouse Concepts#5.3 OLTP vs OLAP ⭐⭐⭐ (guideline ข้อ 4.2 — ออกแน่นอน)]]

> [!question]- A6. อธิบาย Degenerate Dimension, Role-Playing Dimension และ Factless Fact Table พร้อมตัวอย่าง
> **เฉลย:**
> - **Degenerate Dimension** = *"dimension keys without corresponding dimension tables"* — dimension key ที่อยู่ใน fact แต่ **ไม่มีตาราง dimension** เพราะไม่มี attribute อื่นให้บรรยาย · **ตัวอย่าง: Transaction Number, Order Number, Invoice Number** · มักเป็นส่วนหนึ่งของ PK ของ fact table
> - **Role-Playing Dimension** = *"one physical representation but referred to more than once (different roles)"* · **ตัวอย่าง: Dim_Date ถูกใช้เป็น OrderDate, ShipDate, InvoiceDate** · แก้ปัญหา join ด้วย **VIEW**
> - **Factless Fact Table** = fact table ที่ **ไม่มี measure** — บันทึกเหตุการณ์ที่ไม่มีตัวเลขให้วัด · **ตัวอย่าง: การเช็คชื่อเข้าเรียน** · วิเคราะห์ด้วย **`COUNT(*)`**
> → [[06 Multi-Dimensional Design]]

---

## Part B · การคำนวณ (แสดงวิธีทำ)

> [!question]- B1. ข้อมูล `12, 15, 18, 22, 25, 28, 31, 35, 90` จงหา Q1, Q3, IQR และระบุ outlier
> **เฉลย:** เรียงแล้ว n = 9 · **Median (Q2) = 25** (ตัวที่ 5)
> ครึ่งล่าง = `12, 15, 18, 22` → **Q1 = (15+18)/2 = 16.5**
> ครึ่งบน = `28, 31, 35, 90` → **Q3 = (31+35)/2 = 33**
> **IQR = 33 − 16.5 = 16.5**
> รั้วล่าง = $16.5 - 1.5(16.5) = 16.5 - 24.75 = \mathbf{-8.25}$
> รั้วบน = $33 + 1.5(16.5) = 33 + 24.75 = \mathbf{57.75}$
> **→ 90 > 57.75 จึงเป็น outlier** (ตัวเดียว)
> → [[03 Exploratory Data Analysis (EDA)#Outlier Detection ⭐⭐ (สูตรคำนวณได้)]]

> [!question]- B2. จงทำ smoothing ทั้ง 3 แบบกับ `5, 9, 13, 20, 24, 28, 31, 39, 47` (3 bins แบบ equal-frequency)
> **เฉลย:** Bin1 = `5, 9, 13` · Bin2 = `20, 24, 28` · Bin3 = `31, 39, 47`
>
> **(ก) By bin MEANS:** Bin1 = (5+9+13)/3 = **9** · Bin2 = (20+24+28)/3 = **24** · Bin3 = (31+39+47)/3 = **39**
> → `9, 9, 9, 24, 24, 24, 39, 39, 39`
>
> **(ข) By bin MEDIANS:** **9**, **24**, **39**
> → `9, 9, 9, 24, 24, 24, 39, 39, 39` *(บังเอิญเท่ากับ mean เพราะแต่ละ bin สมมาตรพอดี)*
>
> **(ค) By bin BOUNDARIES:** Bin1 (ขอบ 5, 13): `5`→5, `9`→ ห่าง 4 กับ 4 เท่ากัน เลือกขอบล่าง →**5**, `13`→13 ⇒ `5, 5, 13`
> Bin2 (ขอบ 20, 28): `20`→20, `24`→ ห่าง 4 กับ 4 →**20**, `28`→28 ⇒ `20, 20, 28`
> Bin3 (ขอบ 31, 47): `31`→31, `39`→ ห่าง 8 กับ 8 →**31**, `47`→47 ⇒ `31, 31, 47`
> → [[04 Data Pre-processing#Smoothing by Binning — ต้องคำนวณเป็น ⭐⭐]]

> [!question]- B3. ข้อมูล `20, 40, 60, 80, 100` จงทำ Z-score และ Min-Max scaling
> **เฉลย:** $\mu = 300/5 = 60$
> $\sigma = \sqrt{\dfrac{(-40)^2+(-20)^2+0^2+20^2+40^2}{5}} = \sqrt{\dfrac{1600+400+0+400+1600}{5}} = \sqrt{800} \approx 28.28$
> $\min = 20$, $\max = 100$, range = 80
>
> | $x$ | **Z-score** $(x-60)/28.28$ | **Min-Max** $(x-20)/80$ |
> |---|---|---|
> | 20 | **−1.41** | **0.00** |
> | 40 | **−0.71** | **0.25** |
> | 60 | **0.00** | **0.50** |
> | 80 | **+0.71** | **0.75** |
> | 100 | **+1.41** | **1.00** |
> → [[04 Data Pre-processing#4.7 Feature Scaling ⭐⭐ (guideline ข้อ 3.7 — สูตรออกแน่)]]

> [!question]- B4. Jack และ Mary มีผลตรวจ 6 รายการ (asymmetric binary) — Jack `1,0,1,0,0,1` · Mary `1,1,1,0,0,0` จงหา asymmetric distance และ Jaccard
> **เฉลย:** เทียบตำแหน่งต่อตำแหน่ง:
> - $q$ (1,1): ตำแหน่ง 1, 3 → **2**
> - $r$ (1,0): ตำแหน่ง 6 → **1**
> - $s$ (0,1): ตำแหน่ง 2 → **1**
> - $t$ (0,0): ตำแหน่ง 4, 5 → **2** *(ไม่นับ เพราะ asymmetric)*
>
> $$d_{\text{asym}}=\frac{r+s}{q+r+s}=\frac{1+1}{2+1+1}=\frac{2}{4}=\mathbf{0.5}$$
> $$\text{Jaccard}=\frac{q}{q+r+s}=\frac{2}{4}=\mathbf{0.5}\qquad(\text{ตรวจ: }0.5+0.5=1 \;✓)$$
> → [[02 Data and Dataset Types#2.8 Dissimilarity / Similarity สำหรับ Binary Data ⭐ ตัวอย่างคำนวณที่ออกได้]]

> [!question]- B5. ⭐ ข้อสอบเต็มรูปแบบ: จงหาสมการถดถอย, R² และตีความ จากข้อมูลชั่วโมงอ่านหนังสือ vs คะแนนสอบ
> | ชั่วโมง $x$ | 2 | 4 | 6 | 8 | 10 |
> |---|---|---|---|---|---|
> | คะแนน $y$ | 45 | 51 | 61 | 66 | 77 |
>
> ---
> **เฉลย — ขั้นที่ 1: ตารางผลรวม**
>
> | $x$ | $y$ | $xy$ | $x^2$ |
> |---|---|---|---|
> | 2 | 45 | 90 | 4 |
> | 4 | 51 | 204 | 16 |
> | 6 | 61 | 366 | 36 |
> | 8 | 66 | 528 | 64 |
> | 10 | 77 | 770 | 100 |
> | **Σ = 30** | **Σ = 300** | **Σ = 1958** | **Σ = 220** |
>
> $n=5$ · $\bar{x}=6$ · $\bar{y}=60$
>
> **ขั้นที่ 2: หา $b_1$**
> $$b_1=\frac{1958-\frac{(30)(300)}{5}}{220-\frac{30^2}{5}}=\frac{1958-1800}{220-180}=\frac{158}{40}=\mathbf{3.95}$$
>
> **ขั้นที่ 3: หา $b_0$**
> $$b_0=60-3.95(6)=60-23.7=\mathbf{36.3}$$
> $$\boxed{\hat{y}=36.3+3.95x}$$
>
> **ขั้นที่ 4: residuals และ R²**
>
> | $x$ | $y$ | $\hat{y}$ | $y-\hat{y}$ | $(y-\hat{y})^2$ | $(y-\bar{y})^2$ |
> |---|---|---|---|---|---|
> | 2 | 45 | 44.20 | +0.80 | 0.64 | 225 |
> | 4 | 51 | 52.10 | −1.10 | 1.21 | 81 |
> | 6 | 61 | 60.00 | +1.00 | 1.00 | 1 |
> | 8 | 66 | 67.90 | −1.90 | 3.61 | 36 |
> | 10 | 77 | 75.80 | +1.20 | 1.44 | 289 |
> | | | | **Σ = 0** ✓ | **SSE = 7.90** | **SST = 632** |
>
> $$R^{2}=1-\frac{7.90}{632}=1-0.0125=\mathbf{0.9875}$$
>
> **ขั้นที่ 5: ตีความ**
> - **$b_1 = 3.95$** → **อ่านหนังสือเพิ่ม 1 ชั่วโมง คะแนนสอบเพิ่มขึ้นเฉลี่ย 3.95 คะแนน**
> - **$b_0 = 36.3$** → ถ้าไม่อ่านเลย ($x=0$) คาดว่าได้ **36.3 คะแนน**
> - **$R^2 = 0.9875$** → **98.75% ของความแปรผันในคะแนนสอบ อธิบายได้ด้วยจำนวนชั่วโมงที่อ่าน**
> → [[09 Regression Analysis#9.4 The Least Square Method (OLS) ⭐⭐⭐ (สูตรที่ต้องคำนวณเป็น)]]

> [!question]- B6. โมเดลทำนายราคาบ้าน (พันบาท) ได้ผลดังตาราง จงหา MAE, RMSE และ MAPE
> | จริง $y$ | 1000 | 2000 | 1500 | 2500 |
> |---|---|---|---|---|
> | ทำนาย $\hat{y}$ | 1100 | 1800 | 1550 | 2200 |
>
> **เฉลย:** errors $(y-\hat{y})$ = $-100, +200, -50, +300$
>
> $$\text{MAE}=\frac{100+200+50+300}{4}=\frac{650}{4}=\mathbf{162.5}$$
> $$\text{RMSE}=\sqrt{\frac{10000+40000+2500+90000}{4}}=\sqrt{\frac{142500}{4}}=\sqrt{35625}=\mathbf{188.75}$$
> $$\text{MAPE}=\frac{1}{4}\left(\frac{100}{1000}+\frac{200}{2000}+\frac{50}{1500}+\frac{300}{2500}\right)\times 100\%$$
> $$=\frac{0.10+0.10+0.0333+0.12}{4}\times 100\%=\frac{0.3533}{4}\times 100\%=\mathbf{8.83\%}$$
>
> **ตีความ:** **RMSE (188.75) > MAE (162.5)** เพราะ RMSE ยกกำลังสอง จึงลงโทษ error ก้อนใหญ่ (300) หนักกว่า
> → [[09 Regression Analysis#9.8 Prediction Errors ⭐⭐⭐ (guideline ข้อ 8.5 "Different types of prediction errors")]]

> [!question]- B7. โมเดล A มี R² = 0.85 ใช้ 3 predictors · โมเดล B มี R² = 0.87 ใช้ 12 predictors (n = 100) โมเดลไหนดีกว่า
> **เฉลย:** ต้องใช้ **Adjusted R²** เพราะจำนวน predictor ต่างกัน
> $$R^2_{\text{adj,A}}=1-\frac{(1-0.85)(99)}{100-3-1}=1-\frac{14.85}{96}=1-0.1547=\mathbf{0.845}$$
> $$R^2_{\text{adj,B}}=1-\frac{(1-0.87)(99)}{100-12-1}=1-\frac{12.87}{87}=1-0.1479=\mathbf{0.852}$$
> **→ โมเดล B ดีกว่าเล็กน้อย** (0.852 > 0.845)
>
> ⚠️ **แต่ต้องพิจารณาเพิ่ม:** ส่วนต่างน้อยมาก (0.007) แต่โมเดล B ใช้ตัวแปรมากกว่า **4 เท่า** — ตามหลัก **Parsimony** (*"More insight with few predictors"*) และเหตุผลเรื่อง missing values / ความยากในการเก็บข้อมูล **โมเดล A อาจเป็นตัวเลือกที่ดีกว่าในทางปฏิบัติ**
> → [[09 Regression Analysis#Adjusted R² ⭐⭐ (guideline ระบุตรง ๆ)]]

---

## Part C · ออกแบบ Star Schema และเขียน SQL

> [!question]- C1. ⭐ ออกแบบ Star Schema สำหรับร้านกาแฟ — เดินครบ 4 ขั้น
> **โจทย์:** ร้านกาแฟมี 15 สาขา ต้องการวิเคราะห์ยอดขาย เพื่อตอบคำถาม: สาขาไหนขายดีที่สุด · เมนูไหนขายดีในช่วงเวลาใด · โปรโมชั่นไหนได้ผล · ลูกค้าสมาชิกซื้อต่างจากลูกค้าทั่วไปอย่างไร
>
> ---
> **เฉลย**
>
> **Step 1 · Select the Business Process**
> → **การขายหน้าร้าน (POS retail sales)**
>
> **Step 2 · Declare the Grain** ⭐ *(ขั้นสำคัญที่สุด)*
> → **1 แถว = 1 บรรทัดสินค้าบนใบเสร็จ 1 ใบ** (individual line item on a POS transaction)
> *เหตุผล:* ละเอียดที่สุดเท่าที่ทำได้ → roll-up ขึ้นไปตอบทุกคำถามข้างบนได้ทั้งหมด
>
> **Step 3 · Choose the Dimensions**
> | Dimension | ตอบคำถาม | Attributes ตัวอย่าง |
> |---|---|---|
> | **Dim_Date** | When (วัน) | DateKey, FullDate, DayOfWeek, Month, Quarter, Year, IsWeekend, IsHoliday |
> | **Dim_Time** | When (ชั่วโมง) | TimeKey, Hour, TimeSlot (เช้า/บ่าย/เย็น) |
> | **Dim_Product** | What | ProductKey, SKU, ProductName, Category (กาแฟ/ชา/เบเกอรี่), Size, IsSeasonal |
> | **Dim_Store** | Where | StoreKey, StoreID, StoreName, District, Province, StoreType |
> | **Dim_Customer** | Who | CustomerKey, CustomerID, MemberTier, JoinDate, AgeGroup |
> | **Dim_Promotion** | Under what condition | PromotionKey, PromotionName, DiscountType, Channel |
>
> **Step 4 · Identify the Facts (Measures)**
> | Measure | Additivity |
> |---|---|
> | `QuantitySold` | **Additive** |
> | `SalesAmount` | **Additive** |
> | `DiscountAmount` | **Additive** |
> | `UnitPrice` | **Non-additive** (บวกไม่ได้ — เป็นราคาต่อหน่วย) |
> | `ProfitMargin (%)` | **Non-additive** → **ควรเก็บ `Profit` และ `Revenue` แยกกันแทน** |
>
> **+ Degenerate Dimension:** `ReceiptNumber` (เก็บใน fact table ตรง ๆ ไม่มี dimension table) — ใช้จัดกลุ่มสินค้าที่ซื้อพร้อมกันในใบเสร็จเดียว
>
> **DDL:**
> ```sql
> CREATE TABLE SalesFact (
>   DateKey       INT NOT NULL,
>   TimeKey       INT NOT NULL,
>   ProductKey    INT NOT NULL,
>   StoreKey      INT NOT NULL,
>   CustomerKey   INT NOT NULL,
>   PromotionKey  INT NOT NULL,
>   ReceiptNumber VARCHAR(20) NOT NULL,   -- ⭐ degenerate dimension
>   QuantitySold   INT NOT NULL,
>   SalesAmount    DECIMAL(10,2) NOT NULL,
>   DiscountAmount DECIMAL(10,2) NOT NULL,
>   PRIMARY KEY (DateKey, TimeKey, ProductKey, StoreKey,
>                CustomerKey, PromotionKey, ReceiptNumber),
>   FOREIGN KEY (DateKey)      REFERENCES Dim_Date(DateKey),
>   FOREIGN KEY (ProductKey)   REFERENCES Dim_Product(ProductKey)
>   -- … FK ที่เหลือ
> );
> ```
> → [[06 Multi-Dimensional Design#6.1 The 4-Step Dimensional Design Process ⭐⭐⭐]]

> [!question]- C2. จาก schema ข้อ C1 เขียน SQL: "ยอดขายรวมและจำนวนแก้ว ของแต่ละหมวดสินค้า ในแต่ละสาขา เฉพาะวันหยุดสุดสัปดาห์ของปี 2026"
> **เฉลย:**
> ```sql
> SELECT   s.StoreName,
>          p.Category,
>          SUM(f.SalesAmount)  AS TotalSales,
>          SUM(f.QuantitySold) AS TotalCups
> FROM     SalesFact f
> JOIN     Dim_Store   s ON f.StoreKey   = s.StoreKey
> JOIN     Dim_Product p ON f.ProductKey = p.ProductKey
> JOIN     Dim_Date    d ON f.DateKey    = d.DateKey
> WHERE    d.Year = 2026
>   AND    d.IsWeekend = TRUE
> GROUP BY s.StoreName, p.Category
> ORDER BY TotalSales DESC;
> ```
> **หลักคิด:** วัดอะไร → `SUM` จาก **fact** · มองมุมไหน → `StoreName`, `Category` จาก **dim** · กรองอะไร → `Year`, `IsWeekend` จาก **dim**
> ⭐ สังเกตว่า **`IsWeekend` มีอยู่แล้วใน Dim_Date** จึงไม่ต้องคำนวณตอน query — นี่คือประโยชน์ของการทำ Date Dimension ให้ robust
> → [[08 Reporting from Star Schema#8.1 แม่แบบของทุก Query บน Star Schema ⭐⭐⭐]]

> [!question]- C3. ธนาคารต้องการรู้ (ก) ยอดโอนแต่ละครั้ง (ข) ยอดคงเหลือทุกสิ้นเดือน (ค) ระยะเวลาอนุมัติสินเชื่อ — ต้องใช้ fact table กี่ตัว ชนิดอะไร
> **เฉลย: ต้องใช้ 3 fact tables** เพราะมี **grain ต่างกัน** และ **ชนิด measure ต่างกัน**
>
> | คำถาม | Fact Table | ชนิด | Grain | Measure เด่น |
> |---|---|---|---|---|
> | (ก) ยอดโอนแต่ละครั้ง | `Fact_Transfer` | **Transaction** | 1 แถว = 1 การโอน | `TransferAmount` (**Additive**) |
> | (ข) ยอดคงเหลือสิ้นเดือน | `Fact_Account_Monthly` | **Periodic Snapshot** | 1 แถว = 1 บัญชี × 1 เดือน | `Balance` (**Semi-additive** — บวกข้ามบัญชีได้ แต่ข้ามเดือนไม่ได้) |
> | (ค) ระยะเวลาอนุมัติสินเชื่อ | `Fact_Loan_Application` | **Accumulating Snapshot** | 1 แถว = 1 ใบสมัคร | `ApplyDate`, `ReviewDate`, `ApproveDate`, `DisburseDate` + `DaysToApprove` |
>
> **เหตุผลที่แยก (ตามสไลด์):** **Different Granularities** · **Different Measure Types** (transactional vs snapshot vs accumulated) · บางส่วนยังใช้ **dimension คนละชุด**
> **Dim_Date เป็น conformed dimension** ที่ทั้ง 3 fact tables ใช้ร่วมกัน
> → [[06 Multi-Dimensional Design#6.9 Different Types of Fact Tables ⭐⭐⭐ (guideline ข้อ 4.5 — ออกแน่)]]

> [!question]- C4. เขียน SQL โหลด `ProductDim` จาก OLTP ที่มี `Items(ItemID, ItemName, CategoryID, SupplierID, Price)` และ `Categories(CategoryID, CategoryName)` และ `Suppliers(SupplierID, SupplierName, Country)`
> **เฉลย:**
> ```sql
> INSERT INTO ProductDim (ProductID, ProductName, CategoryName,
>                         SupplierName, SupplierCountry, ProductPrice)
> SELECT i.ItemID,              -- natural key เก็บไว้ trace กลับต้นทาง
>        i.ItemName,
>        c.CategoryName,        -- ⭐ de-normalize: แปะชื่อลงมาเลย
>        s.SupplierName,        -- ⭐ de-normalize
>        s.Country,
>        i.Price
> FROM       AllElectronics.Items      i
> INNER JOIN AllElectronics.Categories c ON i.CategoryID = c.CategoryID
> INNER JOIN AllElectronics.Suppliers  s ON i.SupplierID = s.SupplierID;
> ```
> ⭐ **สังเกต 2 จุด:**
> 1. **ไม่ INSERT `ProductKey`** — เพราะเป็น `AUTO_INCREMENT` ฐานข้อมูลสร้าง surrogate key ให้เอง
> 2. **JOIN Categories และ Suppliers เพื่อ de-normalize** — ทำให้ตอน query ไม่ต้อง join 2 ตารางนี้อีก (ถ้าไม่ทำ จะกลายเป็น **snowflake schema**)
> → [[07 ETL#Step 3 — Populate Dimensions ⭐]]

---

## Part D · สถานการณ์ (ข้อยาว)

> [!question]- D1. ⭐ ข้อสอบรวมทุกบท: บริษัทประกันมีข้อมูลลูกค้า 50,000 ราย ต้องการทำนายเบี้ยประกัน จงวางแผนทั้งกระบวนการ
> **ข้อมูลที่มี:** `อายุ` (มี missing 3%) · `เพศ` (nominal) · `จังหวัด` (77 ค่า) · `รายได้ต่อปี` (skewness = 2.8, missing 12%) · `ระดับความเสี่ยง` (ต่ำ/กลาง/สูง) · `จำนวนเคลมย้อนหลัง` · `เบี้ยประกัน` ← target
>
> ---
> **เฉลย — เดินตาม Main Steps of Analytics**
>
> **① Business Understanding** — โจทย์: ทำนายเบี้ยประกัน (**ค่าต่อเนื่อง → Regression**) · success metric: **RMSE / MAPE บน test set**
>
> **② Data Acquisition** — ข้อมูลลูกค้า 50,000 ราย (**Primary data** ถ้าเก็บเอง)
>
> **③ EDA** ([[03 Exploratory Data Analysis (EDA)|บทที่ 3]])
> - **Phase 1 Overview:** `df.shape`, `df.dtypes`, `df.describe()`
> - **Phase 2 Quality:** `df.isnull().sum()` → พบ missing · `heatmap(df.isnull())` ดูรูปแบบ · boxplot หา outlier
> - **Phase 3 Univariate:** histogram ของ `รายได้` → ยืนยันว่า **skewed มาก** (2.8 ≥ 1)
> - **Phase 4 Bivariate:** **correlation heatmap** ระหว่าง predictors ทั้งหมด + scatter plot กับ target
>
> **④ Pre-processing** ([[04 Data Pre-processing|บทที่ 4]])
> | ปัญหา | วิธีแก้ | เหตุผล |
> |---|---|---|
> | `อายุ` missing 3% | **Median** (หรือลบแถวก็ได้เพราะ < 5%) | numerical |
> | `รายได้` missing 12%, **skew 2.8** | **Median** ⭐ | **> 5% จึงลบไม่ได้** และ **skewed มาก → Mean จะถูกหางลากไป** |
> | `เพศ` (nominal, 2 ค่า) | **One-Hot Encoding** | nominal ไม่มีลำดับ |
> | `จังหวัด` (77 ค่า) | **Combine categories** (ยุบเป็นภาค) **แล้วค่อย One-Hot** | **high cardinality (>50)** → one-hot ตรง ๆ จะได้ 77 คอลัมน์ = curse of dimensionality |
> | `ระดับความเสี่ยง` (ordinal) | **Label Encoding** (ต่ำ=1, กลาง=2, สูง=3) | **มีลำดับจริง** |
> | สเกลต่างกันมาก (อายุ 0–100 vs รายได้ 0–10M) | **Standardization** | *"Most of the time ⇒ Standardization is better"* — และถ้าจะใช้ k-NN/NN ต่อ **จำเป็น** |
> | outlier ในรายได้ | **วิเคราะห์ก่อน ห้ามลบอัตโนมัติ** | คนรวยจริงมีอยู่ — เป็น *"rare but real events"* |
>
> ⚠️ **ลำดับสำคัญ:** **split ก่อน → scale ทีหลัง** (fit scaler บน train เท่านั้น) มิฉะนั้นเกิด **data leakage**
>
> **⑤ Modeling** ([[09 Regression Analysis|บทที่ 9]])
> - **Hold-out:** train 80% / test 20%
> - **ตรวจสมมติฐาน:** (ก) **Linearity** — scatter ของแต่ละ $X_i$ กับ $Y$ (ข) **No Multicollinearity** — correlation heatmap ระหว่าง predictors ด้วยกัน
> - ถ้าพบ multicollinearity → **Remove / Combine / Regularization (Ridge, Lasso)**
> - **Feature selection:** Backward หรือ Forward Selection · เลือกโมเดลด้วย **Adjusted R²** *("Good model has: High adj-R²")*
>
> **⑥ Evaluation**
> - รายงาน **R²**, **Adjusted R²**, **RMSE**, **MAE**, **MAPE** — และรายงาน **ทั้ง training และ test**
> - ถ้า **Training RMSE ต่ำมากแต่ Test RMSE สูง → Overfitting** → ลดจำนวน predictors
> - **ตีความ coefficient:** "เมื่อ [ตัวแปร] เพิ่ม 1 หน่วย เบี้ยประกันเปลี่ยน [β] บาท **โดยที่ตัวแปรอื่นคงที่**"

> [!question]- D2. คุณได้ตาราง OLTP ของโรงพยาบาลมา 7 ระบบแยกกัน CEO อยากได้ dashboard เทียบรายได้ตามบริษัทประกันและเวลารอตามสาขา จงอธิบายว่าทำไมต้องสร้าง DW และวางแผนอย่างไร
> **เฉลย:**
>
> **① ทำไมต้องมี DW ไม่ merge Excel**
> - *"The problem is NOT Excel. The problem is business complexity"* — แผนกมากขึ้น ระบบมากขึ้น รายงานมากขึ้น ข้อมูลย้อนหลังมากขึ้น
> - การ merge เอง วนลูป Export → Merge → Clean → Analyze → Repeat ซึ่ง **Time-consuming, Error-prone, Inconsistent**
> - แต่ละระบบเป็น **OLTP** ที่ **normalized** และ **optimize เพื่อ write** → query วิเคราะห์ที่กินข้อมูลก้อนใหญ่จะช้าและ **รบกวนงานปฏิบัติการ**
> - DW ให้ **single source of truth** และ **"Doesn't interfere with local processing at sources"**
>
> **② สถาปัตยกรรม**
> `7 OLTP Sources → ETL → Data Warehouse → Data Marts → Cubes → Dashboard`
>
> **③ ออกแบบ (4-step)**
> - **Business Process:** การให้บริการผู้ป่วยและการเรียกเก็บเงิน (แยก 2 process → **2 fact tables**)
> - **Grain:**
>   - `Fact_Visit` = **Transaction** — 1 แถว = 1 การเข้ารับบริการ (มี `WaitingMinutes`)
>   - `Fact_Billing` = **Transaction** — 1 แถว = 1 รายการเรียกเก็บ (มี `Amount`)
> - **Dimensions (conformed):** `Dim_Date`, `Dim_Branch`, `Dim_Patient`, `Dim_Doctor`, `Dim_Department`, `Dim_Insurance`
> - **Facts:** `WaitingMinutes` (Additive), `ServiceMinutes` (Additive), `BillAmount` (Additive), `SatisfactionScore` (**Non-additive** — เป็นคะแนนเฉลี่ย ต้องเก็บ `ScoreSum` + `ResponseCount` แทน)
>
> **④ ปัญหา ETL ที่ต้องเจอ**
> - **Heterogeneous source systems** (7 ระบบ คนละเทคโนโลยี)
> - **Inconsistent:** รหัสบริษัทประกันไม่ตรงกันระหว่างระบบ · รูปแบบวันที่ต่างกัน → **แก้ด้วย surrogate key** ที่ *"allow the data warehouse team to integrate data from multiple operational source systems"*
> - ต้องสร้าง **Date Dimension** เองเป็น derived structure
>
> **⑤ Reporting** — SQL `GROUP BY Dim_Insurance.CompanyName` + `SUM(BillAmount)` และ `GROUP BY Dim_Branch.BranchName` + `AVG(WaitingMinutes)` → **นี่คือ Descriptive Analytics**
> → [[05 Data Warehouse Concepts]] · [[06 Multi-Dimensional Design]] · [[07 ETL]]

---

## 🎯 กับดักที่คนพลาดบ่อยที่สุด — อ่านซ้ำก่อนเข้าห้องสอบ

> [!warning] 12 ข้อที่ต้องระวัง
> 1. **"เป้าหมายของ analytics คือสร้างโมเดล"** → **ผิด** — *"The goal is not building models, it is making better decisions"*
> 2. **"เจอ outlier ให้ลบทิ้ง"** → **ผิด** — *"should not be removed automatically"* ต้องดู domain knowledge ก่อน
> 3. **"$r = 0$ แปลว่าไม่มีความสัมพันธ์"** → **ผิด** — $r$ วัดเฉพาะความสัมพันธ์ **เชิงเส้น**
> 4. **ใช้ Label Encoding กับ Nominal** → **ผิด** — ต้องใช้ **One-Hot**
> 5. **เติมค่าว่างของข้อมูล skewed ด้วย Mean** → **ผิด** — ต้องใช้ **Median**
> 6. **ตีความ coefficient โดยลืมวรรค "โดยที่ตัวแปรอื่นคงที่"** → **หักคะแนน**
> 7. **ใช้ $R^2$ เทียบโมเดลที่มีจำนวน predictor ต่างกัน** → **ผิด** — ต้องใช้ **Adjusted $R^2$**
> 8. **scale ก่อน split** → **data leakage** — ต้อง **split ก่อน แล้ว fit scaler บน train เท่านั้น**
> 9. **สับสน Encoding กับ Discretization** → เป็นทิศ **ตรงข้าม** กัน
> 10. **`Year` เป็น measure** → **ผิด** — เป็น **dimension attribute** (บวกกันไม่มีความหมาย)
> 11. **บวก Balance/Stock ข้ามเวลา** → **ผิด** — เป็น **semi-additive** ต้องใช้ AVG/LAST
> 12. **ประเมินโมเดลด้วย training data** → **ผิด** — ต้องใช้ **test/hold-out set** (Average Error บน training ≈ 0 เสมอโดยนิยามของ OLS)

---

**ลิงก์:** [[00 START HERE|หน้าหลัก]] · [[10 Formula Sheet]] · [[11 Glossary EN-TH]]
