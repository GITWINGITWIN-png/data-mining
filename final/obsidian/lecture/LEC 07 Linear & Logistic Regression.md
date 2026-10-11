---
title: LEC 07 · Linear & Logistic Regression
exam: Lecture — จ. 19 ต.ค. 2569 16:00–19:00
guideline: "Lecture ข้อ 4.2 Linear Regression (equation, coefficients, prediction, evaluation) · 4.3 Logistic Regression (probability, threshold, coefficients, evaluation)"
source: midterm 69_1_Regression_Analysis.pdf · 69_1_Kitsana_KNN.pdf p.14–24, 68–72
tags: [final, lecture, linear-regression, logistic-regression, odds, threshold]
---

# LEC 07 · Linear & Logistic Regression
### ทำนาย "ตัวเลข" กับทำนาย "ความน่าจะเป็นของคลาส" ด้วยสมการเชิงเส้น

> [!abstract] guideline ข้อ 4.2 + 4.3
> **Linear:** equation · coefficients · prediction · model evaluation → [[#7.1 Linear Regression — สรุปทวน ⭐⭐⭐]]
> **Logistic:** probability · classification threshold · coefficients · model evaluation → [[#7.2 Logistic Regression แนวคิด ⭐⭐⭐]] ถึง [[#7.6 Evaluation ของ Logistic Regression ⭐⭐]]

**ลิงก์:** [[LEC 00 START HERE|หน้าหลัก Lecture]] · [[LEC 05 Model Construction & Evaluation]] · ละเอียดเต็มของ Linear: [[09 Regression Analysis]] (มิดเทอม) · ฝั่ง Lab: [[LAB 05 Supervised Models#5.3 Logistic Regression ⭐⭐⭐⭐ (gap ใหญ่)]]

---

## 7.1 Linear Regression — สรุปทวน ⭐⭐⭐

> [!important] ⭐ ทุกอย่างที่ต้องรู้ในกล่องเดียว (ละเอียด + ตัวอย่างคำนวณมือ: [[09 Regression Analysis#9.4 The Least Square Method (OLS) ⭐⭐⭐ (สูตรที่ต้องคำนวณเป็น)]])
> **สมการ:** $\hat y=b_0+b_1x_1+\dots+b_kx_k$ · หา $b$ ด้วย **OLS** = minimize $\sum(y_i-\hat y_i)^2$
> **simple:** $b_1=\dfrac{\sum xy-\frac{(\sum x)(\sum y)}{n}}{\sum x^2-\frac{(\sum x)^2}{n}}$ · $b_0=\bar y-b_1\bar x$
> **ตีความ coefficient:** *"x เพิ่ม 1 หน่วย y เปลี่ยน b หน่วย **โดยที่ตัวแปรอื่นคงที่**"* · intercept = ค่า ŷ เมื่อทุก x = 0
> **prediction:** แทนค่า x ใหม่ลงสมการ
> **evaluation:** R² · Adjusted R² · MAE · MSE · RMSE บน **test set** ([[LEC 05 Model Construction & Evaluation#5.8 Regression Metrics ⭐⭐⭐]])
> **assumption:** linearity (x แต่ละตัวกับ y) · **no multicollinearity** (x ไม่สัมพันธ์กันเอง)

> [!example] ตัวอย่างจริงจาก Lab (Boston, test 20%)
> **medv = −3.841 − 0.633·lstat + 5.465·rm** · test RMSE **5.59** · R² **0.574**
> *"lstat เพิ่ม 1 จุด % ราคาบ้านลด 0.633 พันดอลลาร์ โดยที่จำนวนห้องคงที่"* · *"ห้องเพิ่ม 1 ห้อง ราคาเพิ่ม 5.465 พันดอลลาร์ โดยที่ lstat คงที่"*
> ทำนาย: lstat = 10, rm = 6 → −3.841 − 6.325 + 32.791 = **22.62** พันดอลลาร์

> [!warning] ขนาด coefficient ≠ ความสำคัญ
> coefficient ขึ้นกับ **หน่วย** ของ x (เช่น nox มี SD 0.12 → coef −16.4 ดูใหญ่แต่ไม่ได้แปลว่าสำคัญที่สุด) → เทียบความสำคัญด้วย **standardized coefficient** หรือ p-value

---

## 7.2 Logistic Regression แนวคิด ⭐⭐⭐

> [!quote] สไลด์ KNN p.14–15 (bullet ซ้ำทุกหน้า)
> - **"Logistic Regression is used to predict a CATEGORICAL dependent variable from a number of independent variables"**
> - **"Binary-classification technique used to predict the PROBABILITY that an instance belongs to a given class"**
> - **"User function similar to SIGMOID function to predict outcome"**
> - **"Uses MAXIMUM LIKELIHOOD to find the best line"**

> [!important] ⭐⭐ ทำไมใช้ linear regression ทำ classification ตรง ๆ ไม่ได้
> เส้นตรงให้ค่าได้ตั้งแต่ −∞ ถึง +∞ แต่ความน่าจะเป็นต้องอยู่ใน [0, 1] → แปลงสมการเชิงเส้นผ่าน **logit / sigmoid**
> $$\underbrace{\ln\frac{p}{1-p}}_{\text{logit = log-odds}}=b_0+b_1x_1+\dots+b_kx_k=z\qquad\Longleftrightarrow\qquad p=\frac{1}{1+e^{-z}}$$
> - ฝั่งซ้าย (สไลด์ p.16–18) = **log ของ odds** · odds = $\frac{p}{1-p}$ (เช่น p = 0.8 → odds = 4 "โอกาสเกิด 4 ต่อ 1")
> - 📚 ฝั่งขวา = **sigmoid** (สไลด์แสดงเป็นกราฟ S ไม่ได้เขียนสูตร) — รับ z ใดก็ได้ ให้ p ในช่วง (0, 1)
> - multiple (p.18): $\ln\frac{p}{1-p}=b_0+b_1\text{Age}+b_2\text{Income}+b_3\text{Education}+b_4\text{Family}$

![[lec_sigmoid.png]]

---

## 7.3 Probability + Threshold ⭐⭐⭐

> [!example] ⭐ ตัวอย่างสไลด์ p.16–17: ทำนายว่าจะรับข้อเสนอประกันสุขภาพไหม จากอายุ
> **Age 35 → p = 42% → < 50% → NO** · **Age 45 → p = 81% → ≥ 50% → YES** · cut line = **0.50**
> 📚 *(derived — ฟิตจาก 2 จุดนี้)* logit(0.42) = −0.323 · logit(0.81) = 1.450 → **b₁ = (1.450 + 0.323)/10 = 0.177** · **b₀ = −0.323 − 35(0.177) = −6.53**
> → p(30) = 0.230 · p(40) = 0.637 · p(50) = 0.912 · จุดที่ p = 0.5 คือ age = −b₀/b₁ = **36.8 ปี**

> [!important] ⭐ Threshold (สไลด์ p.68–72)
> - default **0.5**: p ≥ 0.5 → คลาส 1
> - **ลด** threshold (เช่น 0.25) → ทายคลาส 1 ง่ายขึ้น → **recall ↑, precision ↓**
> - **เพิ่ม** threshold (เช่น 0.75) → **precision ↑, recall ↓**
> - Riding Mowers: cutoff 0.25 / 0.5 / 0.75 → accuracy 0.792 / **0.875** / 0.750 · recall 0.917 / 0.917 / 0.583 ([[LEC 05 Model Construction & Evaluation#5.7 Threshold (Cutoff) ⭐⭐⭐]])
> - **เลือก threshold ตามต้นทุนผิดพลาด** ไม่จำเป็นต้อง 0.5 เสมอ · RapidMiner: `Create Threshold` + `Apply Threshold` (p.69)

---

## 7.4 Maximum Likelihood ⭐⭐

> [!quote] สไลด์ p.19–21
> หา b₀, b₁ ที่ทำให้ **likelihood** (ความน่าจะเป็นที่จะเห็นข้อมูลจริงชุดนี้) สูงสุด:
> $$L=\prod_{\text{y=yes}}p_i\times\prod_{\text{y=no}}(1-p_i)$$
> ตัวอย่าง p.20: $L = 0.03 \times 0.54 \times 0.92 \times 0.95 \times 0.98 \times (1-0.01)(1-0.04)(1-0.10)(1-0.58)(1-0.96)$ = **0.00019939** ✓ (คำนวณยืนยันแล้ว)
> ลองเส้นโค้ง 4 แบบ ได้ L = 0.00007418 · 0.00012845 · 0.00016553 · **0.00019939** → **เลือกเส้นที่ L สูงสุด**

> [!tip] ทำไมไม่ใช้ least squares แบบ linear
> y เป็น 0/1 → ใช้ likelihood เหมาะกว่า · ในทางปฏิบัติ maximize **log-likelihood** ($\ln L$ = −8.52 ในตัวอย่างนี้) เพราะคูณเลขเล็ก ๆ หลายตัวแล้วใกล้ 0 จนคำนวณยาก

---

## 7.5 Coefficients → Odds Ratio ⭐⭐⭐

> [!important] ⭐⭐ การตีความ coefficient ของ logistic (📚 ISLR §4.3 / Shmueli DMBA ch.10 — สไลด์ไม่ได้อธิบาย)
> 1. **เครื่องหมาย:** b > 0 → x เพิ่ม **โอกาสเป็นคลาส 1 เพิ่ม** · b < 0 → ลด · b ≈ 0 → ไม่มีผล
> 2. **b = การเปลี่ยนของ log-odds** ต่อ x เพิ่ม 1 หน่วย (ตัวอื่นคงที่)
> 3. **odds ratio = $e^{b}$** → *"x เพิ่ม 1 หน่วย **odds** คูณด้วย $e^b$"*
>    - $e^b = 1.25$ → odds เพิ่ม 25% · $e^b = 0.80$ → odds ลด 20% · $e^b = 1$ → ไม่มีผล
> 4. ⚠️ **ไม่ใช่** "ความน่าจะเป็นเพิ่ม b" — ผลต่อ p ขึ้นกับว่าตอนนี้อยู่ตรงไหนของ sigmoid

> [!example] ⭐ ตัวอย่างการตีความ
> - ตัวอย่างประกัน (derived): b₁ = 0.177 → $e^{0.177}$ = **1.194** → *"อายุเพิ่ม 1 ปี odds ที่จะรับประกันเพิ่มขึ้น 19.4%"*
> - Lab (Social Network Ads, standardized): Age coef 2.197 → OR **9.0** ต่อ 1 SD
> - sklearn output สไลด์ p.22 (`simple-veh-class.csv`): `classes ['car' 'other']` · `coef [[0.000511, 0.2556, 0.6777]]` (weight_kg, height_m, n_wheels) · `intercept [-3.8408]`
>   → coef เป็นของ **classes_[1] = 'other'** · ล้อเพิ่ม 1 ล้อ → odds ของการเป็น 'other' คูณ $e^{0.678}$ = 1.97 เท่า
>   → รถหนัก 1500 kg สูง 1.5 m 4 ล้อ: z = −3.841 + 0.767 + 0.383 + 2.711 = **0.020** → p(other) = **0.505**

> [!example]- 🧮 Drill: z → p
> $\ln\frac{p}{1-p}=-4+0.05\,\text{Income}+0.8\,\text{Married}$ · Income = 60 (พัน), Married = 1
> z = −4 + 3 + 0.8 = **−0.2** → p = 1/(1 + e^{0.2}) = **0.450** → threshold 0.5 → ทาย **คลาส 0**
> OR(Income) = e^{0.05} = **1.051** (รายได้ +1 พัน → odds +5.1%) · OR(Married) = e^{0.8} = **2.23** (แต่งงาน → odds 2.23 เท่าของโสด)

---

## 7.6 Evaluation ของ Logistic Regression ⭐⭐

- ใช้ metric ของ classification ทั้งหมด: **confusion matrix · accuracy · precision · recall · F1** (ที่ threshold ที่เลือก) + 📚 **AUC** (ไม่ขึ้นกับ threshold)
- RapidMiner `Logistic Regression` (p.23): solver AUTO · reproducible · use regularization ❌ · **standardize ✅** · add intercept ✅ · **compute p-values ✅** · remove collinear columns ✅ → ผลให้ coefficient + **p-value** (p < 0.05 = ตัวแปรมีนัยสำคัญ)
- Process (p.23): Retrieve → Data Preprocessing → **Split Data** → Logistic Regression → **Apply Model** → **Performance**

> [!quote] Pros / Cons (p.24)
> | ✅ Pros | ❌ Cons |
> |---|---|
> | **Interpretability** (coefficient/odds) | **Assumption of linearity** (เชิงเส้นใน log-odds) |
> | Simplicity | **Limited to binary** (มี extension multi-class) |
> | ทำงานดีเมื่อ **linearly separable** | **Prone to overfitting with high-dimensional features** |

| | **Linear Regression** | **Logistic Regression** |
|---|---|---|
| target | ตัวเลขต่อเนื่อง | คลาส (binary) |
| output | ŷ (ไม่จำกัดช่วง) | p ∈ (0, 1) → threshold → คลาส |
| สมการ | y = b₀ + Σbx | ln(p/(1−p)) = b₀ + Σbx |
| หาค่า b | least squares (OLS) | maximum likelihood |
| ตีความ b | y เปลี่ยน b หน่วย | log-odds เปลี่ยน b · odds × e^b |
| ประเมิน | R², RMSE, MAE | confusion matrix, F1, AUC |

---

## ✅ Self-Test — LEC 07

> [!question]- Q1. p = 0.75 odds และ log-odds เท่าไร
> odds = 0.75/0.25 = **3** · log-odds = ln 3 = **1.099**

> [!question]- Q2. logistic ได้ z = 1.5 ความน่าจะเป็นเท่าไร ทายคลาสอะไรที่ threshold 0.5 และ 0.85
> p = 1/(1+e^{−1.5}) = 1/(1+0.223) = **0.818** → threshold 0.5 → **คลาส 1** · threshold 0.85 → **คลาส 0**

> [!question]- Q3. coefficient ของ "Smoker" = 0.69 ตีความ
> e^{0.69} ≈ **2.0** → *"ผู้สูบบุหรี่มี odds ของการเป็นโรคเป็น 2 เท่าของผู้ไม่สูบ โดยตัวแปรอื่นคงที่"*

> [!question]- Q4. ทำไม logistic ใช้ maximum likelihood ไม่ใช้ least squares
> y เป็น 0/1 และ output เป็นความน่าจะเป็นผ่าน sigmoid (ไม่เป็นเชิงเส้น) → MLE หา b ที่ทำให้ข้อมูลที่เห็นมีโอกาสเกิดสูงสุด (สไลด์ p.19: *"uses Maximum Likelihood to find the best line"*)

> [!question]- Q5. linear regression ได้ medv = 30 − 0.9·lstat ทายบ้าน lstat = 12 และตีความ −0.9
> ŷ = 30 − 10.8 = **19.2** · lstat เพิ่ม 1 จุด % ราคาลดเฉลี่ย 0.9 หน่วย

> [!question]- Q6. ธนาคารไม่อยากพลาดลูกค้าที่จะผิดนัด (default) ควรตั้ง threshold สูงหรือต่ำ
> **ต่ำ** — ทำให้ทาย "จะผิดนัด" ง่ายขึ้น → recall ของคลาสผิดนัดสูงขึ้น (FN ลด) แลกกับ FP ที่มากขึ้น

---

**กลับหน้าหลัก →** [[LEC 00 START HERE]] · **ถัดไป →** [[LEC 08 Decision Trees & Random Forest]]
