---
title: Formula Sheet — สูตรทั้งหมดในหน้าเดียว
chapter: 10
tags: [midterm, formula, cheatsheet]
---

# 10 · Formula Sheet
### สูตรทั้งหมดที่อาจต้องคำนวณในห้องสอบ — หน้าเดียวจบ

> [!tip] วิธีใช้หน้านี้
> อ่านบทเต็มให้เข้าใจก่อน แล้วใช้หน้านี้ **ทวนรอบสุดท้ายก่อนเข้าห้องสอบ** · ทุกสูตรมีลิงก์กลับไปยังบทที่อธิบายที่มา

**ลิงก์:** [[00 START HERE|หน้าหลัก]] · [[11 Glossary EN-TH]] · [[12 Exam Drills]]

---

## 📊 สถิติพื้นฐาน — [[03 Exploratory Data Analysis (EDA)]]

### Central Tendency

| ค่า | สูตร | ใช้กับ |
|---|---|---|
| **Mean** | $\bar{x}=\dfrac{1}{n}\sum_{i=1}^{n}x_i$ | numerical **สมมาตร** |
| **Median** | ค่าตำแหน่งกลางเมื่อเรียงแล้ว (เปอร์เซ็นไทล์ที่ 50) | numerical **เบ้ (skewed)** |
| **Mode** | ค่าที่พบบ่อยที่สุด | **categorical** |

### Dispersion

$$\text{Range}=x_{\max}-x_{\min}
\qquad
\sigma^{2}=\frac{1}{n}\sum(x_i-\bar{x})^{2}
\qquad
\sigma=\sqrt{\sigma^{2}}
\qquad
CV=\frac{\sigma}{\bar{x}}$$

### Quartiles & Outliers ⭐ ออกสอบแน่

$$\text{IQR}=Q_3-Q_1$$

> [!important] กฎ 1.5 × IQR
> $$x < Q_1-1.5\,(\text{IQR}) \quad\text{หรือ}\quad x > Q_3+1.5\,(\text{IQR}) \;\Rightarrow\; \textbf{Outlier}$$

> [!important] Z-Score
> $$z=\frac{x-\mu}{\sigma}\qquad \lvert z\rvert>3 \Rightarrow \text{Outlier (เกณฑ์ที่นิยม)}$$

### เกณฑ์ Skewness

| $\lvert\text{Skew}\rvert$ | ความหมาย | ความสัมพันธ์ |
|---|---|---|
| $< 0.5$ | เบ้เล็กน้อย (Nearly symmetric) | Mean ≈ Median |
| $0.5 \le \cdot < 1$ | เบ้ปานกลาง (Moderately skewed) | — |
| $\ge 1$ | เบ้มาก (Highly skewed) | — |

**Skew บวก (ขวา):** **Mean > Median > Mode** · **Skew ลบ (ซ้าย):** **Mean < Median < Mode**

### Pearson Correlation ⭐

$$r=\frac{\text{Cov}(X,Y)}{\sqrt{\text{Var}(X)\cdot\text{Var}(Y)}}
\qquad
\text{Cov}(X,Y)=\frac{\sum(x_i-\bar{x})(y_i-\bar{y})}{n-1}$$

| ค่า | ความหมาย | | ช่วง | ความแรง |
|---|---|---|---|---|
| $r=+1$ | perfect positive linear | | $\lvert r\rvert > 0.7$ | **Strong** |
| $r=0$ | no (linear) correlation | | $0.3<\lvert r\rvert<0.7$ | **Moderate** |
| $r=-1$ | perfect negative linear | | $\lvert r\rvert < 0.3$ | **Weak** |

### เกณฑ์ตัวเลขอื่น ๆ ที่ต้องจำ

| เรื่อง | เกณฑ์ |
|---|---|
| **Missing > 50%** | พิจารณาลบทั้งคอลัมน์ |
| **Missing < 5%** | ลบแถวได้ |
| **Cardinality < 10** | Low (OK) |
| **Cardinality > 50** | High (quite high) |

---

## 🔧 Pre-processing — [[04 Data Pre-processing]]

### Feature Scaling ⭐⭐

> [!important] Standardization (Z-score normalization)
> $$x_{i,\text{new}}=\frac{x_i-\text{mean}(x)}{\text{stdev}(x)}=\frac{x_i-\mu}{\sigma}$$
> ผลลัพธ์: **mean = 0, SD = 1** · ช่วงค่าไม่จำกัด

> [!important] Normalization (Min-Max Scaling)
> **ช่วง [0, 1]:**
> $$x_{i,\text{new}}=\frac{x_i-\min(x)}{\max(x)-\min(x)}$$
> **ช่วง [−1, 1]:**
> $$x_{i,\text{new}}=\frac{x_i-\min(x)}{\max(x)-\min(x)}\times 2-1$$

**เลือกอันไหน:** *"Most of the time ⇒ Standardization is better"* · แต่ **Min-Max เร็วกว่าสำหรับ Neural Network และ Linear regression**

### Discretization — จำนวนช่วง (Rule of Thumb)

$$\text{จำนวนช่วง}=\frac{M}{3C}
\qquad
\begin{cases}M=\text{number of training examples}\\ C=\text{number of classes}\end{cases}$$

### Impurity Measures

$$\text{GINI}(t)=1-\sum_{j}\left[p(j\mid t)\right]^{2}
\qquad
\text{Entropy}(t)=-\sum_{j}p(j\mid t)\log_{2}p(j\mid t)$$

| การกระจาย | GINI | Entropy |
|---|---|---|
| บริสุทธิ์ (class เดียว) | **0** (ต่ำสุด) | **0** (ต่ำสุด) |
| กระจายเท่ากันทุก class | $1-\dfrac{1}{N}$ (สูงสุด) | $\log_2 n_c$ (สูงสุด) |

**Information Gain** $= \text{Entropy}(\text{parent}) - \sum_{v}\dfrac{n_v}{n}\text{Entropy}(v)$ → **เลือก attribute ที่ Gain สูงสุด**

---

## 📐 Distance & Similarity — [[02 Data and Dataset Types]]

### Minkowski (สูตรแม่)

$$d(i,j)=\left(\sum_{k=1}^{p}\lvert x_{ik}-x_{jk}\rvert^{h}\right)^{1/h}$$

| $h$ | ชื่อ | สูตร |
|---|---|---|
| **1** | **Manhattan** (L1) | $d=\sum\lvert x_{ik}-x_{jk}\rvert$ |
| **2** | **Euclidean** (L2) | $d=\sqrt{\sum(x_{ik}-x_{jk})^{2}}$ |

**คุณสมบัติ metric:** 1) Positive definiteness $d(i,j)>0$ เมื่อ $i\ne j$, $d(i,i)=0$ · 2) Symmetry $d(i,j)=d(j,i)$ · 3) Triangle inequality $d(i,j)\le d(i,k)+d(k,j)$

### Nominal

$$d(i,j)=\frac{p-m}{p} \qquad \begin{cases}m=\text{จำนวนที่ตรงกัน}\\p=\text{จำนวน attribute ทั้งหมด}\end{cases}$$

### Binary — contingency table $q$ (1,1), $r$ (1,0), $s$ (0,1), $t$ (0,0)

$$d_{\text{symmetric}}=\frac{r+s}{q+r+s+t}
\qquad
d_{\text{asymmetric}}=\frac{r+s}{q+r+s}
\qquad
\text{Jaccard}=\frac{q}{q+r+s}=1-d_{\text{asym}}$$

> [!tip] จำง่าย ๆ: **symmetric นับ $t$ · asymmetric ตัด $t$ ทิ้ง**

### Cosine Similarity

$$\cos(d_1,d_2)=\frac{d_1\cdot d_2}{\lVert d_1\rVert\,\lVert d_2\rVert}
\qquad \lVert d\rVert=\sqrt{\textstyle\sum d_k^{2}}$$

---

## 📈 Regression — [[09 Regression Analysis]]

### สมการ

$$Y=f(X)+\varepsilon
\qquad
y=\beta_0+\beta_1x
\qquad
y=\beta_0+\beta_1x_1+\dots+\beta_kx_k+\varepsilon$$

### OLS — Least Squares ⭐⭐⭐

$$\min Z=\sum_{i=1}^{n}(y_i-b_0-b_1x_i)^{2}$$

> [!important] สูตรที่ต้องคำนวณได้
> $$b_1=\frac{\sum xy-\dfrac{\left(\sum x\right)\left(\sum y\right)}{n}}{\sum x^{2}-\dfrac{\left(\sum x\right)^{2}}{n}}
> \qquad
> b_0=\bar{y}-b_1\bar{x}$$
>
> **ทำ $b_1$ ก่อนเสมอ แล้วค่อยแทนหา $b_0$**

### R² และ Adjusted R² ⭐⭐⭐

$$\text{SSE}=\sum(y_i-\hat{y}_i)^{2}
\qquad
\text{SST}=\sum(y_i-\bar{y})^{2}
\qquad
\text{SSR}=\text{SST}-\text{SSE}$$

$$\boxed{R^{2}=1-\frac{\text{SSE}}{\text{SST}}}
\qquad
R^{2}_{\text{adj}}=1-\frac{(1-R^{2})(n-1)}{n-k-1}$$

**ตีความ:** *"$R^2$ tells you what percentage of the variation in the target can be explained by the predictors"* · $0\le R^2\le 1$

### Prediction Errors ⭐⭐⭐

| | สูตร | หน่วย | จุดเด่น |
|---|---|---|---|
| **MAE** | $\dfrac{1}{n}\sum\lvert y_i-\hat{y}_i\rvert$ | เดียวกับ $y$ | ไม่สนทิศทาง error |
| **MAPE** | $\dfrac{1}{n}\sum\left\lvert\dfrac{y_i-\hat{y}_i}{y_i}\right\rvert\times 100\%$ | **%** | เทียบข้ามสเกลได้ · ⚠️ ใช้ไม่ได้ถ้า $y_i=0$ |
| **RMSE** | $\sqrt{\dfrac{1}{n}\sum(y_i-\hat{y}_i)^{2}}$ | เดียวกับ $y$ | **ลงโทษ error ใหญ่หนักกว่า** |

> [!important] $\text{RMSE} \ge \text{MAE}$ เสมอ — ยิ่งต่างมาก แปลว่ายิ่งมี error ก้อนใหญ่

### การตีความ coefficient ⭐

> **"เมื่อ $x_j$ เพิ่มขึ้น 1 หน่วย $y$ จะเปลี่ยนไป $\beta_j$ หน่วย โดยที่ตัวแปรอื่นคงที่"**

---

## 🏢 Data Warehouse — [[05 Data Warehouse Concepts]] · [[06 Multi-Dimensional Design]]

### 4 คุณลักษณะของ DW — "SITN"

**S**ubject-Oriented · **I**ntegrated · **T**ime-Variant · **N**on-Volatile

### 4-Step Dimensional Design Process ⭐⭐

| ขั้น | ชื่อ | คำถาม |
|---|---|---|
| 1 | Select the Business Process | *What business activity are we analyzing?* |
| 2 | **Declare the Grain** | *What does each row in the fact table represent?* |
| 3 | Choose the Dimensions | *How do we want to analyze the facts?* |
| 4 | Identify the Facts | *What are we measuring?* |

### Measure Additivity

| ชนิด | บวกข้าม dimension | บวกข้ามเวลา | ตัวอย่าง |
|---|---|---|---|
| **Additive** | ✓ | ✓ | sales amount, quantity |
| **Semi-additive** | ✓ | ✗ | **account balance, stock level, headcount** |
| **Non-additive** | ✗ | ✗ | **ratios, percentages** |

### 3 ชนิดของ Fact Table

| ชนิด | 1 แถว = | คีย์เวิร์ดในโจทย์ |
|---|---|---|
| **Transaction** | 1 เหตุการณ์ | "แต่ละธุรกรรม" "ทุกครั้งที่ขาย" |
| **Periodic Snapshot** | 1 เอนทิตี × 1 งวด | **"ณ สิ้นเดือน" "ทุกวันจันทร์" "ยอดคงเหลือ"** |
| **Accumulating Snapshot** | 1 กระบวนการ (UPDATE) | **"ใช้เวลากี่วัน" "lifecycle" "milestone"** |

### 3 ศัพท์เฉพาะ

| ศัพท์ | นิยามสั้น |
|---|---|
| **Degenerate Dimension** | dimension key ที่**ไม่มี dimension table** (เช่น Transaction Number) |
| **Role-Playing Dimension** | **1 physical table** แต่ fact อ้างถึง **หลายบทบาท** (Dim_Date → OrderDate, ShipDate) · แก้ด้วย **VIEW** |
| **Factless Fact Table** | fact table ที่ **ไม่มี measure** — บันทึกเหตุการณ์ · วิเคราะห์ด้วย `COUNT(*)` |

---

## 🔄 SQL Template — [[07 ETL]] · [[08 Reporting from Star Schema]]

### Query แม่แบบบน Star Schema ⭐⭐⭐

```sql
SELECT      <dim attributes>, AGG(<measures>)   -- dim จาก DIM, measure จาก FACT
FROM        <fact> f
JOIN        <dim1> d1 ON f.<key> = d1.<key>     -- join ผ่าน surrogate key
WHERE       <filter บน dim attributes>
GROUP BY    <dim attributes>                     -- ต้องตรงกับ SELECT
ORDER BY    <measure> DESC;
```

### ลำดับการสร้าง DW (ห้ามสลับ)

**1. CREATE Dimensions → 2. CREATE Fact → 3. POPULATE Dimensions → 4. POPULATE Fact (lookup surrogate keys)**

### ไวยากรณ์ Surrogate Key

| | MySQL | SQL Server |
|---|---|---|
| Auto-increment | `INT AUTO_INCREMENT` | `int IDENTITY(1,1)` |
| ข้อความ | `VARCHAR(50)` | `nvarchar(50)` |
| เงิน | `DECIMAL(10,2)` | `money` |

### PK ของ Fact Table = composite ของ FK ทั้งหมด = **grain**

```sql
PRIMARY KEY (ProductKey, CustomerKey, TimeKey)   -- ต้องตรงกับ GROUP BY ตอน populate
```

---

## 🔢 ตัวเลข "%" ที่ต้องจำ

| เรื่อง | ตัวเลข | ที่มา |
|---|---|---|
| **Data preparation** | **60–80%** ของโครงการ analytics | [[01 Introduction to Data Analytics]] |
| **Data pre-processing** | **80%+** ของโครงการ Big Data | [[04 Data Pre-processing]] |
| **ETL process** | **70–80%** ของเวลาโครงการ DW | [[07 ETL]] |
| **Train/Test split** | **80/20** (Toyota Corolla ใช้ **60/40**) | [[04 Data Pre-processing]], [[09 Regression Analysis]] |
| **PCA cereals** | 2 components แรกเก็บ **93%** ของความแปรผัน | [[04 Data Pre-processing]] |

---

## 🎯 4 คำถามของ Analytics — [[01 Introduction to Data Analytics]]

| ระดับ | คำถาม | เทคนิค |
|---|---|---|
| **Descriptive** | *What happened?* | DW, queries, reports, dashboard, descriptive statistics |
| **Diagnostic** | *Why did it happen?* | drill-down, segmentation, correlation |
| **Predictive** | *What will happen?* | **Linear Regression**, time series, data mining |
| **Prescriptive** | *What should we do?* | recommendation, collaborative filtering, clustering |

$$\textbf{Information}=\textbf{Data}+\textbf{Context}
\qquad
\textbf{Knowledge}=\textbf{Information}+\textbf{Experience}$$

---

**ลิงก์:** [[00 START HERE|หน้าหลัก]] · [[11 Glossary EN-TH]] · [[12 Exam Drills]]
