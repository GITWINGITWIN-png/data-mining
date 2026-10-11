---
title: LEC 10 · Association Rules (Apriori)
exam: Lecture — จ. 19 ต.ค. 2569 16:00–19:00
guideline: "Lecture ข้อ 6 — Transaction data และ data preparation · Frequent itemsets และ Apriori · Rule generation · Support, Confidence และ Lift พร้อมการตีความ"
source: 69_1_apriori_basic_eng.pdf (41 pp) · Agrawal & Srikant 1994 (Agrawal_94.pdf) · HW8 · W10
tags: [final, lecture, association-rules, apriori, support, confidence, lift]
---

# LEC 10 · Association Rules — Apriori
### "อะไรเกิดขึ้นด้วยกัน" — Market Basket Analysis

> [!abstract] guideline ข้อ 6 (4 หัวข้อ)
> 1. **Transaction data และ data preparation** → [[#10.1 Transaction Data & Data Preparation ⭐⭐⭐]]
> 2. **Frequent itemsets และ Apriori** → [[#10.3 Frequent Itemsets & Apriori ⭐⭐⭐⭐]]
> 3. **Rule generation** → [[#10.4 Rule Generation ⭐⭐⭐]]
> 4. **Support, Confidence, Lift พร้อมการตีความ** → [[#10.2 Support · Confidence · Lift ⭐⭐⭐⭐]] · [[#10.5 การตีความ + กับดัก ⭐⭐⭐⭐]]

**ลิงก์:** [[LEC 00 START HERE|หน้าหลัก Lecture]] · [[LEC 09 Clustering]] · Lab: [[LAB 06 Clustering & Association#6.3 Association Rules ⭐⭐⭐]] · งานของคุณ: HW8 (Apriori มือ + bank-data), W10 (BeautyCo)

---

## 10.1 Transaction Data & Data Preparation ⭐⭐⭐

> [!quote] นิยาม (Apriori p.3–9, 12; Agrawal p.1)
> - **Itemset** = เซตของสินค้า เช่น {Milk, Bread, Diaper} · **k-itemset** = มี k items
> - **Transaction** T ⊆ I มี TID · **T contains X** ถ้า X ⊆ T
> - **Rule** X → Y โดย X ∩ Y = ∅ (X = antecedent/premise, Y = consequent/conclusion)
> - **Support count σ(X)** = จำนวน transaction ที่มี X · **frequent itemset** = support ≥ **minsup**

> [!important] ⭐ การเตรียมข้อมูล 3 แบบ (p.28–34)
> | ข้อมูลดิบ | แปลงเป็น | วิธี |
> |---|---|---|
> | list ของตะกร้า (T1: Bread, Milk) | **ตาราง binary 0/1** ต่อ item | p.28: *"Most existing libraries work with BINARY format"* · mlxtend `TransactionEncoder` |
> | **categorical** (Weather = Good/Bad) | **one-hot** — *"introduce a new 'item' for each distinct attribute-value pair"* (p.33–34) | Weather=Good, Weather=Bad, … |
> | **quantitative** (age, income) | **discretize** เป็นช่วง → แล้ว one-hot (p.30–32) | equal width / frequency / domain |
> ⚠️ p.32: discretize ไม่ดี = *"may be useless"* (ทุก weight ตกช่วง 60–80 → item นี้มีทุกแถว ไม่ได้ข้อมูลอะไร)
> 📌 ตัด attribute ที่เป็น **ID** (ไม่ซ้ำ → ไม่มีวัน frequent) และ **เกือบคงที่** (โผล่ทุกกฎโดยไม่มีความหมาย) — HW8: ตัด id, sex (50/50), current_act (75.8%)

> [!example] Multi-dimensional rules (p.29) — รูปแบบ [support, confidence]
> nationality = French ⇒ income = high [50%, 100%] · income = high ⇒ nationality = French [50%, 75%] · age = 50 ⇒ nationality = Italian [33%, 100%]

---

## 10.2 Support · Confidence · Lift ⭐⭐⭐⭐

> [!important] ⭐⭐⭐ สูตร (p.13, 25–27)
> $$\text{support}(X\to Y)=\frac{\sigma(X\cup Y)}{N}\qquad\text{confidence}(X\to Y)=\frac{\sigma(X\cup Y)}{\sigma(X)}=P(Y\mid X)$$
> $$\text{lift}(X\to Y)=\frac{\text{confidence}(X\to Y)}{\text{support}(Y)}=\frac{\text{confidence}}{\text{expected confidence}}=\frac{P(X\cup Y)}{P(X)P(Y)}$$
> | lift | ความหมาย (p.25) |
> |---|---|
> | **> 1** | positive correlation — X ทำให้ Y เกิด **บ่อยขึ้น** กว่าปกติ (*"genuine relationship"*) |
> | **= 1** | **independent** — X ไม่มีผลต่อ Y |
> | **< 1** | negative correlation — X ทำให้ Y เกิด **น้อยลง** |

> [!example] ⭐ Bread/Milk 5 transactions (p.3, 12–17)
> T1 {Bread, Milk} · T2 {Bread, Diaper, Beer, Eggs} · T3 {Milk, Diaper, Beer, Coke} · T4 {Bread, Milk, Diaper, Beer} · T5 {Bread, Milk, Diaper, Coke}
> σ({Milk, Bread, Diaper}) = 2 (T4, T5) → support = 2/5 = **40%**
> **{Milk, Diaper} → {Beer}:** σ(Milk, Diaper, Beer) = 2 · σ(Milk, Diaper) = 3 → s = **0.4** · c = 2/3 = **0.67** · s(Beer) = 3/5 → lift = 0.67/0.6 = **1.11**
> 6 กฎจาก {Milk, Diaper, Beer} (p.16–17) — **support เท่ากันทุกกฎ (0.4)** เพราะมาจาก itemset เดียวกัน แต่ confidence/lift ต่างกัน:
> | rule | conf | lift |
> |---|---|---|
> | {Milk, Diaper} → {Beer} | 0.67 | 1.11 |
> | {Milk, Beer} → {Diaper} | **1.00** | 1.25 |
> | {Diaper, Beer} → {Milk} | 0.67 | **0.83** |
> | {Beer} → {Milk, Diaper} | 0.67 | 1.11 |
> | {Diaper} → {Milk, Beer} | 0.50 | 1.25 |
> | {Milk} → {Diaper, Beer} | 0.50 | **0.83** |

> [!example]- 🧮 ตัวอย่างคำพูด (p.14, p.26–27)
> - 100 transactions มี {Diaper, Beer} 30 ครั้ง → **support 30%** · 50 คนซื้อ Diaper ในนั้น 40 คนซื้อ Beer → **confidence 80%**
> - p.26: T1 {A} · T2–T4 {A, B} · T5 {B} → A ⇒ B: s = 3/5 = 0.6 · c = 3/4 = 0.75 · expected conf = s(B) = 0.8 → **lift = 0.94** → *"The fact that A already bought does not increase the probability of buying B"*
> - p.27: Juice ⇒ Coke: c 75%, expected 67% → lift **1.1** · Coke ⇒ Beer: c 75%, expected 50% → **1.5** · Beer ⇒ Coke: c 100%, expected 67% → **1.5**

---

## 10.3 Frequent Itemsets & Apriori ⭐⭐⭐⭐

> [!important] ⭐⭐ แนวทาง 2 ขั้น (p.21, 23; Agrawal p.2)
> 1. **Frequent itemset generation** — หา itemset ทั้งหมดที่ support ≥ minsup (*"still computationally expensive"*)
> 2. **Rule generation** — จากแต่ละ frequent itemset สร้างกฎที่ confidence ≥ minconf (*"each rule is a binary partitioning of a frequent itemset"*)
> อัลกอริทึม: **Apriori** · **FP-Growth** (RapidMiner ใช้ตัวนี้ — ผลเหมือน Apriori แต่เร็วกว่า ไม่ต้องสร้าง candidate) · Eclat

> [!important] ⭐⭐⭐ Apriori principle (Agrawal p.3)
> **"Any subset of a large (frequent) itemset must be large"** ⟺ **ถ้า itemset ใดไม่ frequent ทุก superset ของมันก็ไม่ frequent** (anti-monotone)
> → ไม่ต้องนับ candidate ที่มี subset ไม่ frequent = **prune** → ประหยัดมหาศาล (lattice 5 items มี 31 itemsets)

> [!important] ⭐ อัลกอริทึม Apriori (Agrawal Fig. 1) + apriori-gen
> ```
> L1 = {frequent 1-itemsets}
> for (k = 2; L(k-1) ≠ ∅; k++):
>     Ck = apriori-gen(L(k-1))        # สร้าง candidate
>     นับ support ของทุก c ใน Ck (สแกน DB 1 รอบ)
>     Lk = {c ∈ Ck | count ≥ minsup}
> Answer = ∪ Lk
> ```
> **apriori-gen = Join + Prune**
> - **Join:** รวม 2 itemsets ใน L(k−1) ที่ **k−2 ตัวแรกเหมือนกัน** (เรียงตามตัวอักษร)
> - **Prune:** ลบ candidate ที่มี **(k−1)-subset ใดไม่อยู่ใน L(k−1)**
> ตัวอย่าง (Agrawal p.4): L3 = {123, 124, 134, 135, 234} → join ได้ {1234, 1345} → prune 1345 (เพราะ 145 ∉ L3) → **C4 = {1234}**

![[lec_apriori_lattice.png]]

> [!example] ⭐⭐ Trace เต็ม: 5 transactions (p.15) minsup = 60% (count ≥ 3) — คำนวณยืนยันแล้ว
> DB: 1 {A, C, D} · 2 {B, C, E} · 3 {A, B, C, E} · 4 {B, E} · 5 {A, B, C, E}
> **C1:** A 3 · B 4 · C 4 · **D 1** · E 4 → **L1 = {A, B, C, E}**
> **C2 (join L1):** AB 2 · AC 3 · AE 2 · BC 3 · BE 4 · CE 3 → **L2 = {AC, BC, BE, CE}**
> **C3:** join (BC, BE) → BCE · (AC กับตัวอื่น prefix ไม่ตรง) · prune: BC, BE, CE ∈ L2 ✓ → BCE count = 3 → **L3 = {BCE}**
> **C4 = ∅** → จบ · frequent itemsets ทั้งหมด: A, B, C, E, AC, BC, BE, CE, BCE (ตรงกับ p.22)

> [!example]- 🧮 Trace: 9 transactions (p.18) minsup count = 2
> DB: ABE · BD · BC · ABCD · AC · BC · AC · ABCE · ABC
> **C1:** A 6 · B 7 · C 7 · D 2 · E 2 → L1 = ทุกตัว
> **C2:** AB 4 · AC 5 · AD 1 · AE 2 · BC 5 · BD 2 · BE 2 · CD 1 · CE 1 · DE 0 → **L2 = {AB, AC, AE, BC, BD, BE}**
> **C3 join:** ABC, ABE, ACE, BCD, BCE, BDE → **prune:** ACE (CE ∉ L2), BCD (CD), BCE (CE), BDE (DE) → **C3 = {ABC, ABE}** → ABC 3, ABE 2 → **L3 = {ABC, ABE}**
> **C4:** join ABC + ABE → ABCE → prune (ACE ∉ L3) → **∅**

> [!example]- 🧮 Trace: Agrawal Fig. 3 (minsup = 2)
> 100 {1,3,4} · 200 {2,3,5} · 300 {1,2,3,5} · 400 {2,5}
> L1 = {1}:2 {2}:3 {3}:3 {5}:3 ({4}:1 ตัด) · C2: 12 1 · 13 2 · 15 1 · 23 2 · 25 3 · 35 2 → L2 = {13, 23, 25, 35} · C3 = {235} (2) → **L3 = {235}** · C4 = ∅

---

## 10.4 Rule Generation ⭐⭐⭐

> [!important] ⭐ วิธี (Agrawal p.2)
> **"For every large itemset l, find all non-empty subsets of l. For every such subset a, output a rule a ⇒ (l − a) if support(l)/support(a) ≥ minconf."**
> itemset ขนาด k สร้างกฎได้ $2^k-2$ กฎ (k = 3 → 6 กฎ) · **ทุกกฎจาก itemset เดียวกันมี support เท่ากัน** ต่างกันแค่ confidence

> [!example] ⭐ จาก {B, C, E} (p.22) minconf 75%
> s(BCE) = 3 · s(BC) = 3 · s(BE) = 4 · s(CE) = 3 · s(B) = s(C) = s(E) = 4
> | rule | conf | ผ่าน 75%? | lift (derived) |
> |---|---|---|---|
> | BC ⇒ E | 3/3 = 100% | ✓ | 1.25 |
> | BE ⇒ C | 3/4 = 75% | ✓ | **0.94** |
> | CE ⇒ B | 3/3 = 100% | ✓ | 1.25 |
> | B ⇒ CE | 3/4 = 75% | ✓ | 1.25 |
> | C ⇒ BE | 3/4 = 75% | ✓ | **0.94** |
> | E ⇒ BC | 3/4 = 75% | ✓ | 1.25 |
> ⚠️ **BE ⇒ C และ C ⇒ BE ผ่าน confidence แต่ lift < 1** → ไม่ใช่ความสัมพันธ์เชิงบวกจริง

> [!example]- 🧮 กฎจาก {A, B, E} (9 transactions, p.19) minconf 50%
> AB ⇒ E: 2/4 = **50%** ✓ · AE ⇒ B: 2/2 = **100%** ✓ · BE ⇒ A: 2/2 = **100%** ✓ · E ⇒ AB: 2/2 = **100%** ✓ · A ⇒ BE: 2/6 = 33% ✗ · B ⇒ AE: 2/7 = 28% ✗

> [!note] กฎไม่มีคุณสมบัติ monotone / transitive (Agrawal p.2)
> X ⇒ A ไม่ได้แปลว่า X + Y ⇒ A (support อาจไม่ถึง) · X ⇒ Y และ Y ⇒ Z ไม่ได้แปลว่า X ⇒ Z (confidence อาจไม่ถึง)

---

## 10.5 การตีความ + กับดัก ⭐⭐⭐⭐

> [!important] ⭐⭐ ประโยคตีความ 3 ค่า (สไลด์ p.39–41 BeautyCo)
> **Eye_Palette → Eye_Enhancer** (s = 0.321, c = 0.843, lift = 2.36):
> - **support:** *"32.1% ของทุก transaction มีทั้ง Eye Palette และ Eye Enhancer"* (กฎนี้ครอบคลุมลูกค้ามากแค่ไหน)
> - **confidence:** *"ในทุก transaction ที่มี Eye_Palette มีโอกาส 84.3% ที่ Eye_Enhancer จะอยู่ในตะกร้าเดียวกัน"* (p.39)
> - **lift:** *"มากกว่าโอกาสทั่วไป 2.36 เท่า → relationship stronger than random chance"* (p.40)
> - **การนำไปใช้:** bundle "2 Styles Glam Eye Look" · รีวิว influencer (p.40) · วางสินค้าใกล้กัน · แนะนำสินค้า
> สไลด์ p.41 Q&A: *"Confidence 80% = of 100 transactions with X, 80 also include Y" · "Support 70% = 70% of all transactions contain the rule's items" · "Lift > 1 = not random chance"*

> [!warning] ⭐⭐ กับดัก: confidence สูงแต่ lift < 1 (tea/coffee, p.25)
> 90% ซื้อ coffee · 25% ซื้อ tea · 20% ซื้อทั้งคู่
> tea ⇒ coffee: support = **20%** · confidence = 0.20/0.25 = **80%** (ดูดี!) · lift = 0.80/0.90 = **0.89 < 1**
> → *"high support and confidence, but NOT correlated"* — คนซื้อ tea ซื้อ coffee **น้อยกว่า** คนทั่วไป (80% vs 90%) → confidence สูงเพียงเพราะ coffee ขายดีอยู่แล้ว

> [!tip] ⭐ ผลของการตั้งค่า
> | ตั้ง | ผล |
> |---|---|
> | **minsup สูงเกิน** | ได้ itemset น้อย พลาดกฎของกลุ่มเฉพาะที่น่าสนใจ (Mock 3: minsup 0.2 → 0 กฎทำนาย pep = YES) |
> | **minsup ต่ำเกิน** | itemset/กฎ ระเบิด คำนวณช้า กฎจาก transaction ไม่กี่อันไม่น่าเชื่อถือ |
> | **minconf สูง** | กฎน้อยแต่แม่น · ยังต้องเช็ก lift |
> | เรียงกฎ | ด้วย **lift** (ความสัมพันธ์) ประกอบ support (ครอบคลุม) |
> BeautyCo (FP-Growth minsup 0.2, Create Association Rules minconf 0.7): **23 frequent itemsets · 3 กฎ** (p.39) · คู่ "ไม่คาดคิด" Base_Makeup + Glossy_Lips (support 0.356) ข้ามหมวดสินค้า → *"trend / bundle opportunity"* (p.38)

> 📚 นอกสไลด์ (mlxtend docs): **leverage** = s(X∪Y) − s(X)s(Y) (> 0 = บวก) · **conviction** = (1 − s(Y))/(1 − conf) (∞ ถ้า conf = 1) — RapidMiner ก็ให้ค่าเหล่านี้ในตาราง rules

---

## ✅ Self-Test — LEC 10

> [!question]- Q1. 1,000 transactions: X 200 · Y 300 · X∪Y 120 หา support, confidence, lift ของ X → Y และ Y → X
> X→Y: s = 0.12 · c = 120/200 = **0.60** · lift = 0.60/0.30 = **2.0**
> Y→X: s = 0.12 · c = 120/300 = **0.40** · lift = 0.40/0.20 = **2.0** (lift เท่ากันทั้งสองทิศเสมอ)

> [!question]- Q2. L2 = {AB, AC, AD, BC, BD} หา C3 หลัง join และ prune
> join (prefix A): ABC, ABD, ACD · (prefix B): BCD → prune: ACD (CD ∉ L2) ✗ · BCD (CD ∉ L2) ✗ · ABC (AB, AC, BC ✓) · ABD (AB, AD, BD ✓) → **C3 = {ABC, ABD}**

> [!question]- Q3. ทำไม Apriori principle ช่วยลดการคำนวณ
> ถ้า itemset X ไม่ frequent ทุก superset ของ X ไม่ frequent แน่นอน → ไม่ต้องสร้าง/นับ candidate พวกนั้น (prune) → ตัด lattice ออกได้มาก

> [!question]- Q4. กฎ A → B confidence 90% lift 0.95 ควรใช้ทำโปรโมชันไหม
> **ไม่ควร** — lift < 1 แปลว่าการซื้อ A ไม่ได้เพิ่มโอกาสซื้อ B (B ขายดีอยู่แล้ว ~95%) · confidence สูงเพราะ B ฐานสูง

> [!question]- Q5. ข้อมูลลูกค้ามี age (ตัวเลข), married (Yes/No) ต้องเตรียมอย่างไรก่อน Apriori
> discretize age เป็นช่วง (เช่น equal frequency 3 ช่วง) → one-hot ทุก attribute=value เป็น item (age=YOUNG, married=YES, married=NO …) → ตาราง True/False

---

**กลับหน้าหลัก →** [[LEC 00 START HERE]] · **ถัดไป →** [[LEC 11 Formula Sheet]]
