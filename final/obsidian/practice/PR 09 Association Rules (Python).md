---
title: PR 09 · Association Rules (Python)
tags: [final, lab, practice, python]
---

# PR 09 · Association Rules — ไกด์ Python ทีละขั้น

> [!abstract] โจทย์
> ซูเปอร์มาร์เก็ตมีใบเสร็จ 9,835 ใบ จงหาสินค้าที่ขายดี frequent itemsets และกฎความสัมพันธ์ ตีความ support / confidence / lift ของกฎที่ดีที่สุด และศึกษาผลของ min support
>
> **สิ่งที่ต้องทำ:**
> 1. อ่าน + one-hot 2. สินค้าขายดี 3. Apriori minsup 2% 4. rules + lift 5. ตีความ + lift < 1 6. ผลของ min support

**ข้อมูล:** `data/p9_groceries_baskets.csv` (Groceries — 1 บรรทัด = 1 ตะกร้า)
**เวลาแนะนำ:** 30 นาที · **ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · ทำโจทย์เดียวกันใน RapidMiner: [[PR 09 Association Rules (RapidMiner)]] · ทฤษฎี/สูตร: [[LAB 06 Clustering & Association#6.3 Association Rules ⭐⭐⭐]] · [[LEC 10 Association Rules]]

> [!tip] เตรียมตัว (ครั้งแรกครั้งเดียว)
> 1. VS Code → **File → Open Folder…** → เลือกโฟลเดอร์ `data mining/final/practice`
> 2. สร้างไฟล์ใหม่ `p09_mywork.ipynb` ในโฟลเดอร์นั้น
> 3. มุมขวาบน **Select Kernel → Jupyter Kernel… → Python (dm-exam)**
> 4. ทำทีละขั้น: พิมพ์โค้ด (หรือ copy) ลง cell ใหม่ → `Shift+Enter` → **เทียบกับ "ผลที่ควรได้"** ถ้าไม่ตรง หยุดหาสาเหตุก่อนไปขั้นต่อไป
> 5. ลองทำแบบ closed-book: อ่านแค่หัวข้อขั้นกับคำอธิบาย แล้วเขียนโค้ดเอง ค่อยเปิดดูโค้ดในไกด์

---

## ขั้นที่ 1 · อ่านตะกร้าและแปลงเป็นตาราง True/False

ไฟล์เป็น "1 บรรทัด = 1 ตะกร้า" รายการคั่นด้วย comma (จำนวนไม่เท่ากัน) → อ่านเป็น list แล้วใช้ TransactionEncoder

**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
import pandas as pd
import matplotlib.pyplot as plt
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules

baskets = [line.strip().split(",") for line in open("data/p9_groceries_baskets.csv") if line.strip()]
print(len(baskets), "ตะกร้า | ตัวอย่าง:", baskets[:2])
te = TransactionEncoder()
items = pd.DataFrame(te.fit(baskets).transform(baskets), columns=te.columns_)
print(items.shape)
print("จำนวนสินค้าต่อตะกร้าเฉลี่ย:", round(items.sum(axis=1).mean(), 2))
```

**ผลที่ควรได้:**

```text
9835 ตะกร้า | ตัวอย่าง: [['citrus fruit', 'margarine', 'ready soups', 'semi-finished bread'], ['coffee', 'tropical fruit', 'yogurt']]
(9835, 169)
จำนวนสินค้าต่อตะกร้าเฉลี่ย: 4.41
```

> [!check] อ่านผล
> 9,835 ตะกร้า · 169 สินค้า · เฉลี่ย 4.41 ชิ้นต่อตะกร้า

---

## ขั้นที่ 2 · สินค้าขายดี (support ของ 1 item)



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
top = items.mean().sort_values(ascending=False).head(10).round(4)
print(top)
top.plot.barh(figsize=(6, 4), title="Top 10 items (support)").invert_yaxis()
```

**ผลที่ควรได้:**

```text
whole milk          0.2555
other vegetables    0.1935
rolls/buns          0.1839
soda                0.1744
yogurt              0.1395
bottled water       0.1105
root vegetables     0.1090
tropical fruit      0.1049
shopping bags       0.0985
sausage             0.0940
dtype: float64
```

**กราฟที่ควรได้:**

![[pr_p9_2.png]]

> [!check] อ่านผล
> whole milk อยู่ใน **25.6%** ของตะกร้า · ระวัง: สินค้าขายดีจะโผล่เป็น consequent ของกฎจำนวนมาก (confidence สูงเพราะฐานสูง)

---

## ขั้นที่ 3 · Frequent itemsets (Apriori, min support 2%)



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
freq = apriori(items, min_support=0.02, use_colnames=True)
freq["size"] = freq["itemsets"].apply(len)
print("frequent itemsets:", len(freq), "| แยกตามขนาด:", freq["size"].value_counts().sort_index().to_dict())
print(freq[freq["size"] == 2].sort_values("support", ascending=False).head(5))
```

**ผลที่ควรได้:**

```text
frequent itemsets: 122 | แยกตามขนาด: {1: 59, 2: 61, 3: 2}
      support                                        itemsets  size
91   0.074835       frozenset({whole milk, other vegetables})     2
103  0.056634             frozenset({whole milk, rolls/buns})     2
119  0.056024                 frozenset({whole milk, yogurt})     2
106  0.048907        frozenset({whole milk, root vegetables})     2
85   0.047382  frozenset({root vegetables, other vegetables})     2
```

> [!check] อ่านผล
> ได้ 122 itemsets · คู่ที่พบบ่อยที่สุดมี whole milk เกือบทั้งหมด

---

## ขั้นที่ 4 · สร้างกฎ (min confidence 30%) แล้วเรียงด้วย lift



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
rules = association_rules(freq, metric="confidence", min_threshold=0.3)
rules = rules.sort_values("lift", ascending=False)
show = rules[["antecedents", "consequents", "support", "confidence", "lift"]].round(3)
print(len(rules), "rules")
print(show.head(8).to_string(index=False))
r1 = rules.iloc[0]
```

**ผลที่ควรได้:**

```text
37 rules
                              antecedents                   consequents  support  confidence  lift
frozenset({whole milk, other vegetables})  frozenset({root vegetables})    0.023       0.310 2.842
 frozenset({whole milk, root vegetables}) frozenset({other vegetables})    0.023       0.474 2.450
             frozenset({root vegetables}) frozenset({other vegetables})    0.047       0.435 2.247
          frozenset({whipped/sour cream}) frozenset({other vegetables})    0.029       0.403 2.082
          frozenset({whole milk, yogurt}) frozenset({other vegetables})    0.022       0.397 2.054
    frozenset({yogurt, other vegetables})       frozenset({whole milk})    0.022       0.513 2.007
                      frozenset({butter})       frozenset({whole milk})    0.028       0.497 1.946
                        frozenset({pork}) frozenset({other vegetables})    0.022       0.376 1.941
```

> [!check] อ่านผล
> กฎ lift สูงสุด: **{'whole milk', 'other vegetables'} → {'root vegetables'}** · support 0.023 · confidence 0.310 · lift **2.84**

---

## ขั้นที่ 5 · ตีความกฎ + หากฎที่ lift < 1



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
print(f"support {r1.support:.1%} | confidence {r1.confidence:.1%} | lift {r1.lift:.2f}")
print("กฎ conf>=30% ที่ lift < 1:", int((rules["lift"] < 1).sum()))
loose = association_rules(freq, metric="confidence", min_threshold=0.1)       # ลด conf เพื่อหาตัวอย่าง
low = loose[loose["lift"] < 1].sort_values("lift")[["antecedents", "consequents", "confidence", "lift"]].round(3)
print("กฎ conf>=10% ที่ lift < 1:", len(low))
print(low.head().to_string(index=False))
```

**ผลที่ควรได้:**

```text
support 2.3% | confidence 31.0% | lift 2.84
กฎ conf>=30% ที่ lift < 1: 0
กฎ conf>=10% ที่ lift < 1: 6
                  antecedents                   consequents  confidence  lift
      frozenset({whole milk})             frozenset({soda})       0.157 0.899
            frozenset({soda})       frozenset({whole milk})       0.230 0.899
            frozenset({soda}) frozenset({other vegetables})       0.188 0.970
frozenset({other vegetables})             frozenset({soda})       0.169 0.970
   frozenset({shopping bags})       frozenset({whole milk})       0.249 0.973
```

> [!check] อ่านผล
> **อ่านกฎอันดับ 1:** 2.3% ของทุกตะกร้ามีสินค้าทั้งสองฝั่ง · ในตะกร้าที่มี {'whole milk', 'other vegetables'} มี 31.0% ที่มี {'root vegetables'} ด้วย · มากกว่าโอกาสทั่วไป 2.84 เท่า → วางใกล้กัน/จัดโปร
> ที่ conf ≥ 30% ไม่มีกฎ lift < 1 · พอลด conf เหลือ 10% เจอ **6 กฎ** ที่ lift < 1 เช่น {'whole milk'} → {'soda'} (conf 15.7%, lift 0.90) = ซื้อด้วยกัน **น้อยกว่า** บังเอิญ — ห้ามใช้ทำโปร

---

## ขั้นที่ 6 · ผลของ min support (FP-Growth เร็วกว่า ผลเหมือนกัน)



**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**

```python
comp = []
for ms in [0.01, 0.02, 0.05]:
    f = fpgrowth(items, min_support=ms, use_colnames=True)
    r = association_rules(f, metric="confidence", min_threshold=0.3) if len(f) else []
    comp.append({"min_support": ms, "itemsets": len(f), "rules": len(r)})
cmp = pd.DataFrame(comp)
print(cmp.to_string(index=False))
```

**ผลที่ควรได้:**

```text
 min_support  itemsets  rules
        0.01       333    125
        0.02       122     37
        0.05        31      3
```

> [!check] อ่านผล
> min support ↑ → itemsets และกฎ ↓ อย่างรวดเร็ว · 0.05 แทบไม่เหลือกฎ · 0.01 ได้กฎเยอะแต่บางกฎมาจากไม่กี่ร้อยตะกร้า

---

## ✅ สรุปคำตอบ
| คำถาม | คำตอบ |
|---|---|
| สินค้าขายดีสุด | whole milk (25.6%) |
| frequent itemsets (minsup 2%) | 122 |
| กฎ (conf ≥ 30%) | 37 กฎ (lift < 1: 0 กฎ · ถ้า conf ≥ 10% มี lift < 1 อยู่ 6 กฎ) |
| กฎ lift สูงสุด | {'whole milk', 'other vegetables'} → {'root vegetables'} (s 0.023, c 0.310, lift 2.84) |

| min_support | itemsets | rules |
|---|---|---|
| 0.01 | 333 | 125 |
| 0.02 | 122 | 37 |
| 0.05 | 31 | 3 |

> [!question]- ลองเองต่อ
> 1. เลือกเฉพาะกฎที่ consequent = {'whole milk'} แล้วเรียงด้วย lift — กฎไหนน่าทำโปรมากสุด
> 2. ตั้ง min_confidence = 0.5 แล้วดูว่าเหลือกี่กฎ
