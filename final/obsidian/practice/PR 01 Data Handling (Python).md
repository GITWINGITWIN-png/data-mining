---
title: PR 01 · Data Handling (Python)
tags: [final, lab, practice, python]
---

# PR 01 · Data Handling — ไกด์ Python ทีละขั้น

> [!abstract] โจทย์
> ร้านอาหารส่งบิล 2 สัปดาห์มาเป็น 2 ไฟล์ และตารางข้อมูลวันทำการแยกอีกไฟล์ ผู้จัดการอยากรู้ว่า **tip เป็น % ของบิล** ต่างกันตามวันและมื้อหรือไม่
>
> **สิ่งที่ต้องทำ:**
> 1. import + ตรวจ 3 ไฟล์ 2. **append** สองสัปดาห์ 3. **join** กับ day_info 4. สร้าง tip_pct 5. **select + filter** โต๊ะใหญ่มื้อเย็น 6. **aggregate** ตามวัน 7. **pivot** วัน × มื้อ 8. กราฟ 4 แบบ + ตีความ 9. correlation + outlier

**ข้อมูล:** `data/p1_bills_week1.csv`, `data/p1_bills_week2.csv` (บิล), `data/p1_day_info.csv` (ข้อมูลวัน) — ข้อมูล tips ของ seaborn
**เวลาแนะนำ:** 45 นาที · **ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · ทำโจทย์เดียวกันใน RapidMiner: [[PR 01 Data Handling (RapidMiner)]] · ทฤษฎี/สูตร: [[LAB 02 Data Handling & Visualization]]

> [!tip] เตรียมตัว (ครั้งแรกครั้งเดียว)
> 1. VS Code → **File → Open Folder…** → เลือกโฟลเดอร์ `data mining/final/practice`
> 2. สร้างไฟล์ใหม่ `p01_mywork.ipynb` ในโฟลเดอร์นั้น
> 3. มุมขวาบน **Select Kernel → Jupyter Kernel… → Python (dm-exam)**
> 4. ทำทีละขั้น: พิมพ์โค้ด (หรือ copy) ลง cell ใหม่ → `Shift+Enter` → **เทียบกับ "ผลที่ควรได้"** ถ้าไม่ตรง หยุดหาสาเหตุก่อนไปขั้นต่อไป
> 5. ลองทำแบบ closed-book: อ่านแค่หัวข้อขั้นกับคำอธิบาย แล้วเขียนโค้ดเอง ค่อยเปิดดูโค้ดในไกด์

---

## ขั้นที่ 1 · Import และตรวจข้อมูลทั้ง 3 ไฟล์

อ่านไฟล์ทั้งหมดแล้วดูขนาด ชนิดข้อมูล และค่าว่าง — **ตรวจก่อนทำอะไรเสมอ**

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

w1 = pd.read_csv("data/p1_bills_week1.csv")
w2 = pd.read_csv("data/p1_bills_week2.csv")
days = pd.read_csv("data/p1_day_info.csv")
print(w1.shape, w2.shape, days.shape)
print(w1.head(3))
print(w1.dtypes)
print("missing:", w1.isna().sum().sum(), w2.isna().sum().sum())
print(days)
```

**ผลที่ควรได้:**

```text
(130, 8) (114, 8) (4, 3)
   bill_id  total_bill   tip   sex smoker  day    time  size
0        2       10.34  1.66  Male     No  Sun  Dinner     3
1        3       21.01  3.50  Male     No  Sun  Dinner     3
2        6       25.29  4.71  Male     No  Sun  Dinner     4
bill_id         int64
total_bill    float64
tip           float64
sex               str
smoker            str
day               str
time              str
size            int64
dtype: object
missing: 0 0
    day is_weekend  open_hours
0  Thur         No          10
1   Fri         No          12
2   Sat        Yes          14
3   Sun        Yes          12
```

> [!check] อ่านผล
> สัปดาห์ 1 มี **130** บิล สัปดาห์ 2 มี **114** บิล · คอลัมน์เหมือนกัน 8 ตัว · ไม่มีค่าว่าง
> `day_info` มี 4 วัน (Thur–Sun) พร้อม `is_weekend` และ `open_hours` → ต้อง **join** ด้วยคอลัมน์ `day`

---

## ขั้นที่ 2 · Concatenate (Append) สองสัปดาห์

ต่อ **แถว** ของสองไฟล์เป็นตารางเดียว — เช็กก่อนว่าคอลัมน์ตรงกัน

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
print("คอลัมน์ต่างกัน:", set(w1.columns) ^ set(w2.columns))
bills = pd.concat([w1, w2], ignore_index=True)
print(bills.shape)
print("bill_id ซ้ำ:", bills["bill_id"].duplicated().sum())
```

**ผลที่ควรได้:**

```text
คอลัมน์ต่างกัน: set()
(244, 8)
bill_id ซ้ำ: 0
```

> [!check] อ่านผล
> คอลัมน์ต่างกัน = `set()` (ตรงกันหมด) → ต่อแล้วได้ **244 แถว** (130 + 114) · bill_id ไม่ซ้ำ

---

## ขั้นที่ 3 · Join กับตาราง day_info

ใช้ **left join** — เก็บบิลทุกใบ แล้วเติมข้อมูลวันให้ (`validate="many_to_one"` เช็กว่าฝั่ง days ไม่มี key ซ้ำ)

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
df = pd.merge(bills, days, on="day", how="left", validate="many_to_one")
print(df.shape)
print(df[["bill_id", "day", "is_weekend", "open_hours"]].head())
print("บิลที่ join ไม่เจอวัน:", df["is_weekend"].isna().sum())
```

**ผลที่ควรได้:**

```text
(244, 10)
   bill_id  day is_weekend  open_hours
0        2  Sun        Yes          12
1        3  Sun        Yes          12
2        6  Sun        Yes          12
3        9  Sun        Yes          12
4       10  Sun        Yes          12
บิลที่ join ไม่เจอวัน: 0
```

> [!check] อ่านผล
> ได้ 244 แถว × 10 คอลัมน์ (เพิ่ม `is_weekend`, `open_hours`) · join ไม่เจอ = 0 → ทุกวันในบิลมีในตาราง days

---

## ขั้นที่ 4 · สร้างคอลัมน์ใหม่: tip เป็น % ของบิล

tip เป็นดอลลาร์เทียบกันไม่ได้ (บิลใหญ่ tip ก็ใหญ่) → ใช้ **tip_pct = tip / total_bill × 100**

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
df["tip_pct"] = df["tip"] / df["total_bill"] * 100
print(df["tip_pct"].describe().round(2))
```

**ผลที่ควรได้:**

```text
count    244.00
mean      16.08
std        6.11
min        3.56
25%       12.91
50%       15.48
75%       19.15
max       71.03
Name: tip_pct, dtype: float64
```

> [!check] อ่านผล
> tip เฉลี่ย **16.08%** · median 15.48% · max 71.03% (สูงผิดปกติ — น่าจะเป็น outlier)

---

## ขั้นที่ 5 · Select attributes + Filter examples

เลือกคอลัมน์ที่สนใจ แล้วกรองเฉพาะ **มื้อเย็น โต๊ะ ≥ 4 คน**

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
cols = ["bill_id", "day", "time", "size", "total_bill", "tip_pct", "is_weekend"]
big_dinner = df.loc[(df["time"] == "Dinner") & (df["size"] >= 4), cols]
print(len(big_dinner))
print(big_dinner.sort_values("total_bill", ascending=False).head(3))
```

**ผลที่ควรได้:**

```text
37
     bill_id  day    time  size  total_bill    tip_pct is_weekend
109      213  Sat  Dinner     4       48.33  18.621974        Yes
33        60  Sat  Dinner     4       48.27  13.942407        Yes
81       157  Sun  Dinner     6       48.17  10.379905        Yes
```

> [!check] อ่านผล
> มีโต๊ะใหญ่มื้อเย็น **37** บิล · ใช้ `&` และวงเล็บครอบแต่ละเงื่อนไขเสมอ

---

## ขั้นที่ 6 · Aggregate: สรุปตามวัน

groupby แล้วสรุปหลายค่าพร้อมกัน

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
by_day = (df.groupby("day")
            .agg(n_bills=("bill_id", "count"), avg_bill=("total_bill", "mean"),
                 avg_tip_pct=("tip_pct", "mean"))
            .round(2).sort_values("avg_tip_pct", ascending=False))
print(by_day)
```

**ผลที่ควรได้:**

```text
      n_bills  avg_bill  avg_tip_pct
day                                 
Fri        19     17.15        16.99
Sun        76     21.41        16.69
Thur       62     17.68        16.13
Sat        87     20.44        15.32
```

> [!check] อ่านผล
> วันที่ tip% สูงสุดคือ **Fri** (16.99%) · วันที่บิลมากที่สุดคือ Sat (87 บิล)

---

## ขั้นที่ 7 · Pivot: tip% เฉลี่ย ตามวัน × มื้อ

แถว = day · คอลัมน์ = time · ค่า = mean ของ tip_pct · `margins=True` เพิ่มแถว/คอลัมน์รวม

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
pv = pd.pivot_table(df, index="day", columns="time", values="tip_pct", aggfunc="mean", margins=True).round(2)
print(pv)
cnt = pd.crosstab(df["day"], df["time"])
print(cnt)
```

**ผลที่ควรได้:**

```text
time  Dinner  Lunch    All
day                       
Fri    15.89  18.88  16.99
Sat    15.32    NaN  15.32
Sun    16.69    NaN  16.69
Thur   15.97  16.13  16.13
All    15.95  16.41  16.08
time  Dinner  Lunch
day                
Fri       12      7
Sat       87      0
Sun       76      0
Thur       1     61
```

> [!check] อ่านผล
> มื้อกลางวันมีเฉพาะ Thur/Fri (Sat/Sun เป็น NaN) — crosstab ยืนยันว่า Sat/Sun ไม่มีมื้อกลางวันเลย · **ค่า NaN ใน pivot = ไม่มีข้อมูล ไม่ใช่ 0**

---

## ขั้นที่ 8 · กราฟ 4 แบบ

histogram (การกระจาย) · boxplot (เทียบกลุ่ม + outlier) · scatter (ความสัมพันธ์ 2 ตัวเลข) · bar (เทียบค่าเฉลี่ย)

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
fig, ax = plt.subplots(2, 2, figsize=(11, 8))
sns.histplot(df, x="tip_pct", bins=25, ax=ax[0, 0]); ax[0, 0].set_title("tip % distribution")
sns.boxplot(df, x="day", y="tip_pct", order=["Thur", "Fri", "Sat", "Sun"], ax=ax[0, 1]); ax[0, 1].set_title("tip % by day")
sns.scatterplot(df, x="total_bill", y="tip", hue="time", ax=ax[1, 0]); ax[1, 0].set_title("tip vs total bill")
sns.barplot(df, x="is_weekend", y="tip_pct", errorbar=None, ax=ax[1, 1]); ax[1, 1].set_title("mean tip % weekend?")
plt.tight_layout()
```

**กราฟที่ควรได้:**

![[pr_p1_8.png]]

> [!check] อ่านผล
> - histogram: ส่วนใหญ่ 10–20% · หางขวามีค่าสูงผิดปกติ (outlier)
> - boxplot: median ของ 4 วันใกล้กัน · มี outlier ด้านบน
> - scatter: tip เพิ่มตาม total_bill (ความสัมพันธ์บวก)
> - bar: weekend vs weekday tip% ต่างกันไม่มาก

---

## ขั้นที่ 9 · Correlation + outlier

หา r ระหว่างตัวเลข แล้วหา outlier ของ tip_pct ด้วยกฎ IQR

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
print(df[["total_bill", "tip", "size", "tip_pct"]].corr().round(3))
q1, q3 = df["tip_pct"].quantile([0.25, 0.75])
iqr = q3 - q1
upper = q3 + 1.5 * iqr
print(f"Q1={q1:.2f} Q3={q3:.2f} IQR={iqr:.2f} upper fence={upper:.2f}")
print(df.loc[df["tip_pct"] > upper, ["bill_id", "total_bill", "tip", "tip_pct"]].round(2))
```

**ผลที่ควรได้:**

```text
            total_bill    tip   size  tip_pct
total_bill       1.000  0.676  0.598   -0.339
tip              0.676  1.000  0.489    0.342
size             0.598  0.489  1.000   -0.143
tip_pct         -0.339  0.342 -0.143    1.000
Q1=12.91 Q3=19.15 IQR=6.23 upper fence=28.50
     bill_id  total_bill   tip  tip_pct
38        68        3.07  1.00    32.57
88       173        7.25  5.15    71.03
92       179        9.60  4.00    41.67
123      233       11.61  3.39    29.20
```

> [!check] อ่านผล
> r(total_bill, tip) = **0.676** (บวกค่อนข้างสูง) · แต่ r(total_bill, tip_pct) = -0.339 (ลบ) → บิลใหญ่ให้ tip เป็น **%** น้อยลง
> outlier (> 28.50%): 4 บิล — ต้องตรวจว่าเป็นค่าจริงหรือบันทึกผิดก่อนตัด

---

## ✅ สรุปคำตอบ (เทียบกับของคุณ)
| คำถาม | คำตอบ |
|---|---|
| รวมกี่บิล | 244 บิล (130 + 114) |
| tip% เฉลี่ย | 16.08% |
| วันที่ tip% สูงสุด | Fri (16.99%) |
| โต๊ะใหญ่มื้อเย็น | 37 บิล |
| r(total_bill, tip) | 0.676 |

> [!question]- ลองเองต่อ (ไม่มีเฉลยโค้ด)
> 1. pivot ค่าเฉลี่ย total_bill ตาม `sex` × `smoker` แล้วตีความ 1 ประโยค
> 2. join แบบ inner กับตาราง days ที่ลบแถว Thur ออก → จำนวนแถวเหลือเท่าไร ทำไม
> 3. วาด boxplot tip_pct แยกตาม size แล้วบอกว่าโต๊ะขนาดไหนให้ tip% สูงสุด
