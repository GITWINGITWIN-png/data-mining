---
title: Glossary EN–TH — อภิธานศัพท์
chapter: 11
tags: [midterm, glossary, vocabulary]
---

# 11 · Glossary EN–TH
### อภิธานศัพท์ — ศัพท์ทุกตัวที่โผล่ในสไลป์ พร้อมนิยามสั้น

> [!tip] วิธีใช้
> ข้อสอบมักใช้ **ศัพท์อังกฤษ** ตรงตามสไลด์ · หน้านี้ช่วยให้แปลได้เร็วและไม่สับสนกับศัพท์ที่คล้ายกัน
> ⭐ = ศัพท์ที่ guideline ระบุชื่อโดยตรง

**ลิงก์:** [[00 START HERE|หน้าหลัก]] · [[10 Formula Sheet]] · [[12 Exam Drills]]

---

## A — Analytics & Foundations

| English | ไทย | นิยามสั้น | บท |
|---|---|---|---|
| **Data Analytics** ⭐ | การวิเคราะห์ข้อมูล | กระบวนการตรวจสอบ แปลง และสรุปข้อมูล เพื่อสกัด insight ที่นำไปสู่การตัดสินใจ | [[01 Introduction to Data Analytics\|1]] |
| **Data** ⭐ | ข้อมูล | raw organized facts and observations | 1 |
| **Information** ⭐ | สารสนเทศ | **Data + Context** — ตอบ who/what/when/where | 1 |
| **Knowledge** ⭐ | ความรู้ | **Information + Experience** — ตอบ *What should we do?* | 1 |
| **Descriptive Analytics** ⭐ | การวิเคราะห์เชิงพรรณนา | *What happened?* | 1 |
| **Diagnostic Analytics** | การวิเคราะห์เชิงวินิจฉัย | *Why did it happen?* | 1 |
| **Predictive Analytics** ⭐ | การวิเคราะห์เชิงพยากรณ์ | *What will happen?* — ให้ความน่าจะเป็น ไม่ใช่ความแน่นอน | 1 |
| **Prescriptive Analytics** ⭐ | การวิเคราะห์เชิงแนะนำ | *What should we do?* | 1 |
| **Data Mining** | การทำเหมืองข้อมูล | **discovers patterns** — classification, clustering, association rules | 1 |
| **Machine Learning** | การเรียนรู้ของเครื่อง | **builds predictive models** | 1 |
| **Data Science** | วิทยาการข้อมูล | **solves problems using data** | 1 |
| **Artificial Intelligence** | ปัญญาประดิษฐ์ | **automates intelligent behavior** | 1 |
| **Data Drift / Concept Drift** | การเลื่อนของข้อมูล/แนวคิด | ข้อมูลหรือความสัมพันธ์เปลี่ยนไปหลัง deploy → ต้อง retrain | 1 |
| **Actionable Insight** | ข้อมูลเชิงลึกที่นำไปใช้ได้ | insight ที่นำไปสู่การกระทำจริง | 1 |

---

## B — Data & Attributes

| English | ไทย | นิยามสั้น | บท |
|---|---|---|---|
| **Dataset** | ชุดข้อมูล | collection ของ data objects ที่จัดระเบียบไว้ | [[02 Data and Dataset Types\|2]] |
| **Data object** | วัตถุข้อมูล | 1 แถวในตาราง (record, instance, sample) | 2 |
| **Attribute** | คุณลักษณะ | 1 คอลัมน์ — เรียกได้อีกว่า **column, dimension, feature, variable** | 2 |
| **Dimensionality** | มิติ | จำนวน attribute → มากเกินไปเกิด **curse of dimensionality** | 2 |
| **Sparsity** | ความเบาบาง | สัดส่วนค่าศูนย์/ว่าง — "only presence counts" | 2 |
| **Resolution** | ความละเอียด | ระดับรายละเอียด — *"patterns depend on the scale"* | 2 |
| **Nominal** ⭐ | นามบัญญัติ | หมวดหมู่ **ไม่มีลำดับ** (สี, สถานภาพสมรส, zip code) · ใช้ **mode** | 2 |
| **Ordinal** ⭐ | เรียงอันดับ | หมวดหมู่ **มีลำดับ** แต่ระยะห่างไม่แน่นอน (เกรด, S/M/L) · ใช้ **median** | 2 |
| **Interval** | อันตรภาค | ผลต่างมีความหมาย แต่ **ไม่มีศูนย์แท้** (°C, ปฏิทิน) · ใช้ **mean, SD** | 2 |
| **Ratio** | อัตราส่วน | **มีศูนย์แท้** ผลต่างและอัตราส่วนมีความหมาย (น้ำหนัก, อายุ, เงิน) | 2 |
| **Binary** | ทวิภาค | 2 สถานะ (0/1) | 2 |
| **Symmetric binary** | ทวิภาคสมมาตร | 2 ผลลัพธ์สำคัญเท่ากัน (เพศ) — **นับ $t$ (0,0)** | 2 |
| **Asymmetric binary** | ทวิภาคอสมมาตร | สำคัญไม่เท่ากัน (ผลตรวจโรค) — **ไม่นับ $t$** | 2 |
| **Discrete** | ไม่ต่อเนื่อง | ค่าจำกัด นับได้ (integer) | 2 |
| **Continuous** | ต่อเนื่อง | จำนวนจริง วัดได้ (float) | 2 |
| **Target / Response / Dependent / Label** | ตัวแปรตาม | สิ่งที่ต้องการทำนาย ($Y$) | 2, 9 |
| **Predictor / Independent / Feature** | ตัวแปรอิสระ | สิ่งที่ใช้ทำนาย ($X$) | 2, 9 |
| **Primary Data** | ข้อมูลปฐมภูมิ | เก็บเอง — แม่นยำ ตรงความต้องการ แต่แพงและช้า | 2 |
| **Secondary Data** | ข้อมูลทุติยภูมิ | ได้จากแหล่งที่มีอยู่ — เร็ว ประหยัด แต่อาจไม่ตรงความต้องการ | 2 |
| **Similarity** | ความคล้าย | สูง = เหมือนกันมาก · มักอยู่ในช่วง [0,1] | 2 |
| **Dissimilarity** | ความต่าง | สูง = ต่างกันมาก · ต่ำสุดมักเป็น 0 | 2 |
| **Proximity** | ความใกล้เคียง | **คำรวม** ของ similarity และ dissimilarity | 2 |
| **Euclidean Distance** | ระยะทางแบบยุคลิด | เส้นตรง (Minkowski $h=2$, L2 norm) | 2 |
| **Manhattan Distance** | ระยะทางแบบแมนฮัตตัน | เดินตามตาราง (Minkowski $h=1$, L1 norm) | 2 |
| **Jaccard coefficient** | สัมประสิทธิ์แจ็คการ์ด | similarity สำหรับ asymmetric binary = $q/(q+r+s)$ | 2 |
| **Cosine Similarity** | ความคล้ายโคไซน์ | วัด **มุม** ไม่ใช่ขนาด — เหมาะกับข้อมูล sparse เช่นเอกสาร | 2 |

---

## C — EDA & Visualization

| English | ไทย | นิยามสั้น | บท |
|---|---|---|---|
| **EDA (Exploratory Data Analysis)** ⭐ | การวิเคราะห์ข้อมูลเชิงสำรวจ | สำรวจและสรุปคุณลักษณะสำคัญของข้อมูลด้วยสถิติและ visualization | [[03 Exploratory Data Analysis (EDA)\|3]] |
| **Univariate Analysis** ⭐ | การวิเคราะห์ตัวแปรเดียว | ดูทีละตัวแปร — histogram, boxplot, bar plot | 3 |
| **Bivariate Analysis** ⭐ | การวิเคราะห์สองตัวแปร | ดูความสัมพันธ์ 2 ตัว — scatter, heatmap, contingency table | 3 |
| **Multivariate Analysis** ⭐ | การวิเคราะห์หลายตัวแปร | 3 ตัวแปรขึ้นไป — bubble chart, PCA, correlation matrix | 3 |
| **Histogram** ⭐ | ฮิสโทแกรม | การกระจายของตัวแปรต่อเนื่อง แบ่งเป็น **bins** | 3 |
| **Boxplot** ⭐ | แผนภาพกล่อง | แสดง min, Q1, median, Q3, max และ **outliers** | 3 |
| **Scatter Plot** ⭐ | แผนภาพกระจาย | ความสัมพันธ์ระหว่าง 2 ตัวแปร numerical · **ไม่บอกความแรง** | 3 |
| **Heatmap** ⭐ | แผนภาพความร้อน | ใช้ **ความเข้มของสี** แทนค่า — ใช้กับ **correlation table** และ **missing values** | 3 |
| **Line Plot** | กราฟเส้น | แนวโน้มตามเวลา — *"used primarily for showing time series"* | 3 |
| **Pairplot** | แผนภาพคู่ | scatter ทุกคู่ + histogram บนแนวทแยง | 3 |
| **Violin Plot** | ไวโอลินพล็อต | **Boxplot + Density curve** | 3 |
| **Contingency Table** | ตารางแจกแจงร่วม | นับ observation ในแต่ละ combination ของ 2 categorical | 3 |
| **Chi-Square Test of Independence** | การทดสอบไคสแควร์ | ทดสอบว่า 2 categorical สัมพันธ์กันอย่างมีนัยสำคัญหรือไม่ | 3 |
| **t-test** | การทดสอบที | เทียบ **2 กลุ่ม** | 3 |
| **ANOVA** | การวิเคราะห์ความแปรปรวน | เทียบ **3 กลุ่มขึ้นไป** | 3 |
| **Skewness** ⭐ | ความเบ้ | ความไม่สมมาตรของการแจกแจง | 3 |
| **Kurtosis** | ความโด่ง | ความแหลม/แบนของยอดการแจกแจง | 3 |
| **Cardinality** | ภาวะเชิงการนับ | จำนวนค่าที่ไม่ซ้ำ — **<10 OK · >50 สูง** | 3 |
| **IQR (Interquartile Range)** ⭐ | พิสัยควอไทล์ | $Q_3-Q_1$ | 3 |
| **Correlation ≠ Causation** | สหสัมพันธ์ ≠ เหตุเป็นผล | สหสัมพันธ์บอกความแรงและทิศทาง **ไม่บอกเหตุ-ผล** | 3, 4 |

---

## D — Pre-processing

| English | ไทย | นิยามสั้น | บท |
|---|---|---|---|
| **GIGO (Garbage In, Garbage Out)** ⭐ | ขยะเข้า ขยะออก | คุณภาพ input กำหนดคุณภาพ output | [[04 Data Pre-processing\|4]] |
| **Incomplete data** | ข้อมูลไม่สมบูรณ์ | ขาดค่า → เกิด **statistical bias** และอัลกอริทึมส่วนใหญ่ประมวลผล null ไม่ได้ | 4 |
| **Inconsistent data** | ข้อมูลไม่สอดคล้อง | รูปแบบ/ชื่อต่างกัน ("BKK" vs "Bangkok") → **จัดกลุ่มและรวมยอดไม่ได้** | 4 |
| **Imputation** ⭐ | การเติมค่าที่หายไป | แทนค่าว่างด้วย **Mean / Median / Mode** หรือวิธีขั้นสูง | 4 |
| **Model-Based Imputation** | การเติมค่าด้วยโมเดล | ถือ attribute ที่หายเป็น target แล้วใช้ regression/ML ทำนาย | 4 |
| **Noise** ⭐ | สัญญาณรบกวน | **การเบี่ยงเบนเล็ก ๆ แบบสุ่ม** จากสัญญาณจริง → แก้ด้วย **smoothing** | 4 |
| **Outlier** ⭐ | ค่าผิดปกติ | จุดที่ **เบี่ยงเบนอย่างมีนัยสำคัญ** จากข้อมูลส่วนใหญ่ → **ห้ามลบอัตโนมัติ** | 4 |
| **Smoothing** ⭐ | การทำให้เรียบ | ลด noise — **Binning, Regression, Clustering** | 4 |
| **Binning** ⭐ | การแบ่งช่วง | เรียงข้อมูล แบ่ง bin แล้วแทนด้วย **mean / median / boundaries** | 4 |
| **Encoding** ⭐ | การเข้ารหัส | **Categorical → Numerical** | 4 |
| **One-Hot Encoding** ⭐ | การเข้ารหัสแบบวันฮอต | **Nominal → binary vector** (1 คอลัมน์ต่อ 1 category) · เสี่ยง curse of dimensionality | 4 |
| **Label Encoding** ⭐ | การเข้ารหัสแบบป้าย | **Ordinal → integer** (Small=1, Medium=2, Large=3) | 4 |
| **Discretization** ⭐ | การแบ่งเป็นช่วง | **Numerical → Categorical (Ordinal)** | 4 |
| **Equal Width** ⭐ | ความกว้างเท่ากัน | แบ่งช่วงกว้างเท่ากัน — **ไวต่อ outlier มาก** | 4 |
| **Equal Frequency** ⭐ | ความถี่เท่ากัน | แต่ละช่วงมีจำนวนจุดเท่ากัน | 4 |
| **Feature Scaling** ⭐ | การปรับสเกลลักษณะ | ทำให้ทุก feature อยู่บนสเกลเดียวกัน | 4 |
| **Standardization / Z-score** ⭐ | การทำให้เป็นมาตรฐาน | $(x-\mu)/\sigma$ → mean 0, SD 1 | 4 |
| **Normalization / Min-Max** ⭐ | การทำให้เป็นบรรทัดฐาน | $(x-\min)/(\max-\min)$ → ช่วง [0,1] | 4 |
| **Curse of dimensionality** | คำสาปแห่งมิติ | ปัญหาเมื่อ attribute เยอะเกินไป | 2, 4 |
| **Sampling** | การสุ่มตัวอย่าง | ใช้ตัวอย่างแทนทั้งชุด — ต้อง **representative** | 4 |
| **Stratified sampling** | การสุ่มแบบแบ่งชั้น | แบ่ง partition แล้วสุ่มจากแต่ละ partition ตามสัดส่วน | 4 |
| **SMOTE** | — | Over-sampling ด้วย **การสร้างข้อมูลสังเคราะห์** | 4 |
| **RUS** | — | Random Under-Sampling | 4 |
| **PCA** | การวิเคราะห์องค์ประกอบหลัก | **Feature extraction** — project ไปยัง space มิติต่ำกว่า | 4 |
| **Redundant feature** | ลักษณะซ้ำซ้อน | ข้อมูลซ้ำกับ attribute อื่น (**Variance = 0 ต้องลบ**) | 4 |
| **Irrelevant feature** | ลักษณะไม่เกี่ยวข้อง | ไม่มีข้อมูลที่เป็นประโยชน์ (student ID → ทำนาย GPA) | 4 |
| **Filter approach** | วิธีแบบกรอง | คัดด้วยสถิติ (correlation, Gini, entropy) — เร็ว | 4 |
| **Wrapper approach** | วิธีแบบห่อหุ้ม | ใช้ **โมเดลจริง** ประเมินคุณภาพ subset — ช้าแต่แม่นกว่า | 4 |
| **Gini Index / Entropy** | — | วัด **impurity** — สูงสุดเมื่อกระจายเท่ากัน ต่ำสุด (=0) เมื่อบริสุทธิ์ | 4 |
| **Hold-out** ⭐ | การกันข้อมูลไว้ | แบ่งเป็น **Training Set** (สร้างโมเดล) และ **Test Set** (วัดผล) | 4, 9 |
| **Data leakage** | การรั่วของข้อมูล | ข้อมูล test แอบเข้าไปในการเทรน (เช่น `fit` scaler บนทั้งชุด) | 4 |

---

## E — Data Warehouse

| English | ไทย | นิยามสั้น | บท |
|---|---|---|---|
| **Data Warehouse (DW)** ⭐ | คลังข้อมูล | **subject-oriented, integrated, time-variant, non-volatile** collection สนับสนุนการตัดสินใจ | [[05 Data Warehouse Concepts\|5]] |
| **Subject-Oriented** ⭐ | เน้นหัวข้อ | จัดตามหัวข้อธุรกิจ ไม่ใช่ตาม application | 5 |
| **Integrated** ⭐ | บูรณาการ | รวมข้อมูลหลายแหล่งอย่างสอดคล้อง | 5 |
| **Time-Variant** ⭐ | แปรตามเวลา | เก็บย้อนหลังพร้อม time stamp | 5 |
| **Non-Volatile** ⭐ | ไม่ผันผวน | ข้อมูลนิ่ง อัปเดตไม่บ่อย อาจ append-only | 5 |
| **Single source of truth** | แหล่งความจริงหนึ่งเดียว | ข้อมูลชุดเดียวที่ทุกคนอ้างอิงตรงกัน | 5 |
| **OLTP** ⭐ | ระบบประมวลผลธุรกรรม | **Updates เป็นหลัก · Normalized · transaction เล็กจำนวนมาก** | 5 |
| **OLAP** ⭐ | ระบบวิเคราะห์ออนไลน์ | **Reads เป็นหลัก · De-normalized · Ad-hoc queries ยาวและซับซ้อน** | 5 |
| **Cube** | ลูกบาศก์ข้อมูล | **"set of pre-computed data at specific periods of time"** | 5 |
| **Data Mart** | ตลาดข้อมูล | ส่วนย่อยของ DW สำหรับแผนกหนึ่ง | 5 |
| **Ad-hoc query** | คิวรีเฉพาะกิจ | query ที่ผู้ใช้คิดขึ้นเอง ไม่ได้กำหนดไว้ล่วงหน้า | 5 |
| **Drill-down** | เจาะลึก | จากหยาบ → ละเอียด (Year → Month) | 5, 8 |
| **Roll-up** | ม้วนขึ้น | จากละเอียด → หยาบ (City → State → Country) | 5, 8 |
| **Slice / Dice** | หั่น / เจาะ | กรอง 1 มิติ / หลายมิติ | 8 |
| **Pivot** | หมุนแกน | สลับแกนการมอง | 8 |
| **De-normalization** ⭐ | การลดรูปปกติ | ยอมให้ข้อมูลซ้ำซ้อนเพื่อ **ลด join และเร่ง query** | 5 |

---

## F — Dimensional Modeling

| English | ไทย | นิยามสั้น | บท |
|---|---|---|---|
| **Fact Table** ⭐ | ตารางข้อเท็จจริง | เก็บ **numeric measurements** · **ตารางใหญ่ที่สุด** · คอลัมน์น้อย (FK + measures) | [[06 Multi-Dimensional Design\|6]] |
| **Dimension Table** ⭐ | ตารางมิติ | เก็บ **textual descriptors** · ข้อมูลน้อยและนิ่ง · **คอลัมน์เยอะ** | 6 |
| **Fact / Measure** ⭐ | ข้อเท็จจริง / ตัววัด | ค่าที่วัดได้และรวมยอดได้ (sales amount, quantity) | 6 |
| **Star Schema** ⭐ | สคีมาดาว | fact กลาง + dimension แผ่ออก **ไม่ normalize** · join น้อย เร็ว เข้าใจง่าย | 5, 6 |
| **Snowflake Schema** ⭐ | สคีมาเกล็ดหิมะ | **"normalized star-schema"** — dimension แตกเป็นตารางลูก | 5, 6 |
| **Grain / Granularity** ⭐ | ระดับความละเอียด | **"What does each row in the fact table represent?"** — ต้องนิยามก่อนออกแบบ | 6 |
| **Additive** ⭐ | บวกรวมได้ | รวมได้ทุกมิติ (sales amount) | 6 |
| **Semi-additive** ⭐ | บวกรวมได้บางมิติ | รวมข้ามมิติได้ **แต่ข้ามเวลาไม่ได้** (balance, stock level) | 6 |
| **Non-additive** ⭐ | บวกรวมไม่ได้ | ratios, percentages | 6 |
| **Primary Key (PK)** ⭐ | คีย์หลัก | ระบุแถวไม่ซ้ำ · ใน fact = **composite ของ FK ทั้งหมด** | 6 |
| **Foreign Key (FK)** ⭐ | คีย์นอก | ชี้ไปยัง PK ของอีกตาราง | 6 |
| **Surrogate Key** ⭐ | คีย์แทน | **meaningless integer** ที่ DW สร้างเอง — *"every join should be based on"* | 6 |
| **Natural Key** | คีย์ธรรมชาติ | รหัสจากระบบต้นทาง (SKU, StoreID) — **เก็บเป็น attribute ไม่ใช้ join** | 6 |
| **Degenerate Dimension** ⭐ | มิติเสื่อม | **dimension key ที่ไม่มี dimension table** (Transaction/Order/Invoice Number) | 6 |
| **Role-Playing Dimension** ⭐ | มิติหลายบทบาท | **1 physical table** ถูกอ้างถึงหลายครั้ง (Dim_Date → OrderDate, ShipDate) · แก้ด้วย **VIEW** | 6 |
| **Factless Fact Table** ⭐ | ตารางข้อเท็จจริงไร้ค่าวัด | fact table ที่ **ไม่มี measure** — บันทึกเหตุการณ์ · ใช้ `COUNT(*)` | 6 |
| **Transaction Fact** ⭐ | — | **1 แถว = 1 เหตุการณ์** · granularity สูงสุด | 6 |
| **Periodic Snapshot Fact** ⭐ | — | **1 แถว = 1 เอนทิตี × 1 งวด** (สิ้นเดือน, ทุกวันจันทร์) | 6 |
| **Accumulating Snapshot Fact** ⭐ | — | **1 แถว = 1 กระบวนการ** ที่ถูก **UPDATE** เมื่อคืบหน้า · มี **milestone dates** | 6 |
| **Conformed Dimension** | มิติร่วม | dimension ที่ fact table หลายตัวใช้ร่วมกัน (มัก = Dim_Date) | 6 |

---

## G — ETL & Reporting

| English | ไทย | นิยามสั้น | บท |
|---|---|---|---|
| **ETL** ⭐ | สกัด-แปลง-โหลด | อ่านจากแหล่ง → แปลงให้เข้ากับปลายทาง → โหลดเข้า DW · **กิน 70–80% ของเวลาโครงการ** | [[07 ETL\|7]] |
| **Extract** ⭐ | สกัด | ดึงข้อมูลจาก source systems ต่าง ๆ | 7 |
| **Transform** ⭐ | แปลง | แปลงรูปแบบและโครงสร้างให้พร้อมวิเคราะห์ | 7 |
| **Load** ⭐ | โหลด | นำเข้า target data warehouse | 7 |
| **Data Cleansing** ⭐ | การล้างข้อมูล | ทำให้ข้อมูลชัดเจน มีความหมาย และถูกต้อง | 7 |
| **Data Integration** | การบูรณาการข้อมูล | รวมและ map ข้อมูลจากทุกแหล่งเข้าสู่รูปแบบวิเคราะห์ | 7 |
| **Metadata Management** | การจัดการเมทาดาทา | อัปเดต metadata ที่ใช้ทำ ETL mappings และ rules | 7 |
| **Incremental Loading** | การโหลดเพิ่มทีละส่วน | โหลดเฉพาะส่วนที่เปลี่ยน ไม่ทำใหม่ทั้งหมด | 7 |
| **Date Dimension** ⭐ | มิติวันที่ | dimension ที่ **แทบทุก DW ต้องมี** · เป็น **derived structure** ต้องคำนวณเอง | 6, 7 |
| **Surrogate Key Lookup** ⭐ | การค้นหาคีย์แทน | แปลง natural key → surrogate key ตอนโหลด fact table | 7 |

---

## H — Regression

| English | ไทย | นิยามสั้น | บท |
|---|---|---|---|
| **Supervised learning** | การเรียนรู้แบบมีผู้สอน | มีทั้ง INPUT และ OUTPUT — **Labeled Data** | [[09 Regression Analysis\|9]] |
| **Un-supervised learning** | การเรียนรู้แบบไม่มีผู้สอน | มีแค่ INPUT — **Un-Labeled Data** · หา hidden patterns | 9 |
| **Reinforcement learning** | การเรียนรู้แบบเสริมกำลัง | มี GOAL และ ACTION · **Trial and Error** + **Reward** | 9 |
| **Regression** ⭐ | การถดถอย | supervised learning ที่ **outcome เป็นค่าต่อเนื่อง** | 9 |
| **Simple Linear Regression** ⭐ | การถดถอยเชิงเส้นอย่างง่าย | $y=\beta_0+\beta_1x$ — 1 predictor | 9 |
| **Multiple Linear Regression** ⭐ | การถดถอยเชิงเส้นพหุคูณ | หลาย predictors | 9 |
| **Polynomial Regression** | การถดถอยพหุนาม | มีพจน์ $x^2, x^3, \dots$ — **ยังเป็น linear in parameters** | 9 |
| **Intercept ($\beta_0$)** ⭐ | จุดตัดแกน y | ค่า $y$ เมื่อ $x = 0$ | 9 |
| **Slope ($\beta_1$)** ⭐ | ความชัน | **"direction and strength of relationship"** | 9 |
| **OLS (Ordinary Least Squares)** ⭐ | วิธีกำลังสองน้อยที่สุด | หา $b_0, b_1$ ที่ทำให้ $\sum(y-\hat{y})^2$ น้อยที่สุด | 9 |
| **Residual** ⭐ | เศษเหลือ | $y_i-\hat{y}_i$ — **"the error in using $\hat{y}_i$ to estimate $y_i$"** | 9 |
| **SSE** ⭐ | ผลรวมกำลังสองของความคลาดเคลื่อน | $\sum(y_i-\hat{y}_i)^2$ | 9 |
| **SST** ⭐ | ผลรวมกำลังสองทั้งหมด | $\sum(y_i-\bar{y})^2$ | 9 |
| **R² (Coefficient of Determination)** ⭐ | สัมประสิทธิ์การตัดสินใจ | **Goodness of Fit** — % ของความแปรผันที่อธิบายได้ | 9 |
| **Adjusted R²** ⭐ | R² ปรับแก้ | มี penalty ตามจำนวน predictor — **ใช้เทียบโมเดลคนละขนาด** | 9 |
| **Linearity** ⭐ | ความเป็นเชิงเส้น | ต้องมีความสัมพันธ์เชิงเส้นระหว่าง $Y$ กับ **แต่ละ** $X_i$ | 9 |
| **Multicollinearity** ⭐ | สหสัมพันธ์พหุ | **predictors สัมพันธ์กันเองสูง** — อุดมคติคือสัมพันธ์กับ $Y$ แต่ไม่สัมพันธ์กันเอง | 9 |
| **Ridge / Lasso (Regularization)** | การทำให้เป็นระเบียบ | ลดผลของ multicollinearity **โดยเก็บทุกตัวแปรไว้** | 9 |
| **MAE** ⭐ | ความคลาดเคลื่อนสัมบูรณ์เฉลี่ย | $\frac{1}{n}\sum\lvert y-\hat{y}\rvert$ — ไม่สนทิศทาง | 9 |
| **MAPE** ⭐ | ความคลาดเคลื่อนเปอร์เซ็นต์ | error เป็น **%** ของค่าจริง — เทียบข้ามสเกลได้ | 9 |
| **RMSE** ⭐ | รากที่สองของค่าเฉลี่ยกำลังสอง | $\sqrt{\frac{1}{n}\sum(y-\hat{y})^2}$ — **ลงโทษ error ใหญ่หนักกว่า** | 9 |
| **Overfitting** ⭐ | การเรียนรู้เกินพอดี | **"memorizes the training data too well"** → ดีบน train แย่บน test | 9 |
| **Parsimony Model** ⭐ | โมเดลประหยัด | **"More insight with few predictors"** — โมเดลง่ายที่ทำงานได้ดีพอ | 9 |
| **Backward Selection** ⭐ | การเลือกแบบถอยหลัง | เริ่มจาก **ทุก predictor** แล้ว **ลบทีละตัว** | 9 |
| **Forward Selection** ⭐ | การเลือกแบบเดินหน้า | เริ่มจาก **ไม่มี predictor** แล้ว **เพิ่มทีละตัว** | 9 |
| **p-value** | ค่าพี | ต่ำ (≈0) = **มีนัยสำคัญ** · สูง = **ไม่มีนัยสำคัญ อาจตัดทิ้ง** | 9 |

---

## ⚠️ คู่ศัพท์ที่สับสนบ่อยที่สุด

> [!warning] อ่านทวนก่อนเข้าห้องสอบ
> | คู่ที่สับสน | จำแบบนี้ |
> |---|---|
> | **Encoding** vs **Discretization** | Encoding: **Cat → Num** · Discretization: **Num → Cat** (**ทิศตรงข้าม**) |
> | **One-Hot** vs **Label Encoding** | One-Hot สำหรับ **Nominal** · Label สำหรับ **Ordinal** |
> | **Noise** vs **Outlier** | Noise = **เล็ก สุ่ม ทั่วไป** · Outlier = **ใหญ่ โดดเด่น ชัดเจน** |
> | **Standardization** vs **Normalization** | Standardization = **z-score (mean 0, SD 1)** · Normalization = **Min-Max [0,1]** |
> | **OLTP** vs **OLAP** | OLTP = **เขียน, normalized, ทีละ record** · OLAP = **อ่าน, de-normalized, หลายพันแถว** |
> | **Star** vs **Snowflake** | Snowflake = **star ที่ normalize dimension แล้ว** |
> | **PK** vs **Surrogate Key** vs **Natural Key** | Surrogate = **PK ที่ DW สร้างเอง ไร้ความหมาย** · Natural = **รหัสจากระบบต้นทาง** |
> | **Degenerate** vs **Factless** | Degenerate = **key ที่ไม่มีตาราง** · Factless = **ตารางที่ไม่มี measure** |
> | **t-test** vs **ANOVA** | t-test = **2 กลุ่ม** · ANOVA = **3 กลุ่มขึ้นไป** |
> | **MAE** vs **RMSE** | RMSE **ยกกำลังสอง → ลงโทษ error ใหญ่หนักกว่า** และ **RMSE ≥ MAE เสมอ** |
> | **R²** vs **Adjusted R²** | R² **เพิ่มเสมอ** เมื่อเพิ่มตัวแปร · Adjusted R² **ลดได้** ถ้าตัวแปรไร้ประโยชน์ |
> | **Backward** vs **Forward** | Back = **เริ่มเต็ม แล้วลบ** · Forward = **เริ่มศูนย์ แล้วเพิ่ม** |
> | **Filter** vs **Wrapper** | Filter = **สถิติ เร็ว** · Wrapper = **ใช้โมเดลจริง ช้า** |
> | **Additive** vs **Semi-additive** | Semi = **บวกข้ามเวลาไม่ได้** (balance, stock) |

---

**ลิงก์:** [[00 START HERE|หน้าหลัก]] · [[10 Formula Sheet]] · [[12 Exam Drills]]
