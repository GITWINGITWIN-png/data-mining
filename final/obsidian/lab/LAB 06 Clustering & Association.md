---
title: LAB 06 · Clustering & Association Rules
exam: Lab — จ. 12 ต.ค. 2569 09:00–12:00
guideline: "Lab › Model Construction ข้อ 5 (Clustering, Association Rules) + อ่านผลจากกราฟ/ตาราง"
tags: [final, lab, kmeans, elbow, silhouette, apriori, fp-growth, rapidminer]
---

# LAB 06 · Clustering & Association Rules
### Unsupervised 2 งาน: จัดกลุ่ม (K-Means) และหากฎ "ซื้อด้วยกัน" (Apriori / FP-Growth)

> [!abstract] สิ่งที่ข้อสอบ Lab น่าจะถาม (อิงสไลด์ + W10/W11/HW8/HW9)
> **Clustering:** preprocess (เลือก attribute + normalize) → K-Means หลายค่า k → **เลือก k** (elbow / silhouette / Davies–Bouldin) → **ตีความ centroid** (กลุ่มไหนเป็นแบบไหน) → ทำนายกลุ่มของจุดใหม่ → (PCA plot)
> **Association:** เตรียม transaction (one-hot/binominal, discretize ตัวเลข) → frequent itemsets (min support) → rules (min confidence) → **อ่าน support / confidence / lift** → คำแนะนำเชิงธุรกิจ

**ลิงก์:** [[LAB 00 START HERE|หน้าหลัก Lab]] · ก่อนหน้า [[LAB 05 Supervised Models]] · ถัดไป [[LAB 07 Reading & Explaining Results]] · ทฤษฎี: [[LEC 09 Clustering]] · [[LEC 10 Association Rules]]

> [!warning] 🕳️ Gap ของคุณในบทนี้
> - **RapidMiner: ไม่เคยทำ k-Means, Cluster Distance Performance, FP-Growth, Create Association Rules** (W10 sheet แนะนำ RapidMiner แต่คุณทำ Python)
> - silhouette เคยใช้แค่ใน HW9 · ไม่เคยวาด cluster บน PCA 2D

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.decomposition import PCA
```

---

## 6.1 Preprocessing สำหรับ Clustering ⭐⭐

> [!important] 3 เรื่องที่ต้องทำ (สไลด์ clustering p.21–22)
> 1. **เลือก attribute** — เอาเฉพาะตัวที่เกี่ยวกับ "ความเหมือน" ที่อยากได้ · ตัด ID / ชื่อ (ใน RapidMiner ตั้ง role = **id** ไม่ต้องลบ) · ตัด label ถ้ามี (clustering ไม่ใช้ label — ถ้าใส่ไปเท่ากับโกง)
> 2. **Normalize** — *"Raw distance measures are highly influenced by scale of measurements → normalize (standardize) the data first"* (p.21) · Sales (หลักพัน) จะกลบ Fixed_charge (หลักหน่วย)
> 3. **จัดการ outlier** — K-Means *"too sensitive to outliers"* (p.39) · post-processing: กลุ่มเล็กมาก 1–2 สมาชิกอาจเป็น outlier
>
> K-Means ใช้ได้กับ **ตัวเลขเท่านั้น** (p.17) → categorical ต้อง one-hot ก่อน (หรือใช้ K-Prototypes/Gower — นอกขอบเขต)

```python
util = pd.read_csv("final/data/utilities.csv").set_index("Company")   # 22 บริษัท × 8 ตัวแปร (สไลด์ clustering p.10)
print(util.describe().loc[["mean", "std", "min", "max"]].round(2))      # Sales หลักหมื่น vs Fixed_charge ~1 → ต้อง normalize

scaler = StandardScaler().fit(util)
Z = pd.DataFrame(scaler.transform(util), index=util.index, columns=util.columns)
```

> ถ้าอยากได้ตัวเลขตรงกับ RapidMiner (สไลด์ p.30) ใช้ `(util - util.mean()) / util.std(ddof=1)` — RapidMiner ใช้ sample std ($n-1$) · ผลการจัดกลุ่มแทบไม่ต่าง (scale ทุกคอลัมน์ด้วยตัวคูณเดียวกัน)

---

## 6.2 K-Means + เลือกจำนวน cluster ⭐⭐⭐

**อัลกอริทึม (สไลด์ p.17):** (1) สุ่ม k centroid (2) ให้แต่ละจุดเข้ากลุ่ม centroid ที่ใกล้สุด (3) ย้าย centroid ไปที่ **ค่าเฉลี่ย** ของสมาชิก (4) วนข้อ 2–3 จนไม่มีใครย้ายกลุ่ม · ฝึกคำนวณมือ 9 จุด: [[LEC 09 Clustering]]

| พารามิเตอร์ | sklearn | RapidMiner `k-Means` | ความหมาย |
|---|---|---|---|
| จำนวนกลุ่ม | `n_clusters` | **k** | ต้องกำหนดเอง (ข้อเสียของ K-Means) |
| วิธีเลือกจุดเริ่ม | `init="k-means++"` (default) | ✅ **determine good start values** | K-Means++ กระจายจุดเริ่มให้ห่างกัน (สไลด์ p.24) |
| จำนวนรอบสุ่มใหม่ | `n_init` (`"auto"`) | **max runs** (10) | รันหลายรอบแล้วเก็บรอบที่ SSE ต่ำสุด → ลดปัญหา local optimum |
| รอบสูงสุดต่อการรัน | `max_iter` (300) | **max optimization steps** (100) | — |
| ระยะทาง | Euclidean เท่านั้น | **measure types** → numerical measure | — |

```python
rows = []
for k in range(2, 9):
    km = KMeans(n_clusters=k, n_init=50, random_state=42).fit(Z)
    rows.append({"k": k, "WCSS (inertia)": km.inertia_,
                 "silhouette": silhouette_score(Z, km.labels_),         # สูง = ดี (−1 ถึง 1)
                 "Davies-Bouldin": davies_bouldin_score(Z, km.labels_),  # ต่ำ = ดี
                 "sizes": np.bincount(km.labels_).tolist()})
choose_k = pd.DataFrame(rows).round(3)
print(choose_k.to_string(index=False))

fig, ax = plt.subplots(1, 2, figsize=(10, 3.5))
ax[0].plot(choose_k["k"], choose_k["WCSS (inertia)"], marker="o"); ax[0].set_title("Elbow (WCSS)")
ax[1].plot(choose_k["k"], choose_k["silhouette"], marker="o", color="#D55E00"); ax[1].set_title("Silhouette")
for a in ax: a.set_xlabel("k")
plt.tight_layout(); plt.savefig("/tmp/lab06_k.png", dpi=100)
```

> [!example] ผลจริง (Utilities, standardized, n_init = 50)
> | k | 2 | 3 | 4 | **5** | 6 | 7 | 8 |
> |---|---|---|---|---|---|---|---|
> | WCSS | 137.5 | 106.6 | 84.2 | 70.6 | 60.9 | 51.9 | 44.3 |
> | silhouette | 0.185 | 0.230 | 0.234 | **0.248** | 0.241 | 0.230 | 0.219 |
> | Davies–Bouldin | 1.621 | 1.367 | 1.177 | 1.000 | 0.904 | 0.871 | 0.835 |
>
> **อ่านผล:** WCSS ลดลงเรื่อย ๆ ไม่มี "ข้อศอก" ชัด (ข้อมูลแค่ 22 แถว 8 มิติ) · silhouette สูงสุดที่ **k = 5** · DB ลดตาม k เสมอ (ระวัง: k มากขึ้นมักดูดีขึ้นแต่กลุ่มเล็กเกินจนไม่มีประโยชน์) → **เลือก k = 4–5** แล้วตัดสินด้วย **interpretability** (กลุ่มอธิบายได้ไหม, มีกลุ่มสมาชิก 1 ตัวเยอะไหม)
> ⚠️ **WCSS ลดลงเสมอเมื่อ k เพิ่ม** (k = n → WCSS = 0) → ห้ามเลือก k ที่ WCSS ต่ำสุด · ต้องดู "จุดที่การลดเริ่มแบน" (สไลด์ p.28)

### ตีความ centroid — หัวใจของโจทย์ clustering ⭐⭐⭐

```python
km4 = KMeans(n_clusters=4, n_init=50, random_state=42).fit(Z)
util_c = util.assign(cluster=km4.labels_)

profile = util_c.groupby("cluster").mean().round(2)        # centroid ในหน่วยเดิม (อ่านง่ายกว่า z-score)
profile.insert(0, "n", util_c["cluster"].value_counts().sort_index())
print(profile.to_string())
print(util_c.groupby("cluster").apply(lambda g: ", ".join(g.index), include_groups=False))

# เทียบกับค่าเฉลี่ยทั้งหมด (สไลด์ p.41: "cluster mean vs population mean")
z_profile = pd.DataFrame(km4.cluster_centers_, columns=util.columns).round(2)  # z-score: + = สูงกว่าเฉลี่ย
print(z_profile.to_string())
```

> [!important] ⭐ วิธีเขียนตีความแต่ละกลุ่ม (ใช้ z-score ของ centroid: |z| > ~0.8 = โดดเด่น)
> | กลุ่ม | สมาชิก | ลักษณะเด่น (เทียบค่าเฉลี่ย) | ตั้งชื่อ |
> |---|---|---|---|
> | Idaho, Nevada, Puget | 3 | **Sales สูงมาก (z = +1.90)** · Cost สูง (+1.37) · Demand_growth สูง (+1.02) · Fuel_Cost ต่ำ (−0.99) · ไม่มี Nuclear | "ขายมาก โตเร็ว เชื้อเพลิงถูก" |
> | Boston, NY, Hawaiian, New England, Pacific, San Diego, United | 7 | **Fuel_Cost สูง (+1.28)** · Load_factor สูง (+0.82) · Sales ต่ำ (−0.88) | "เชื้อเพลิงแพง ขายน้อย" |
> | Commonwealth, Madison, Northern, Wisconsin, Virginia | 5 | **Nuclear สูง (+1.60 · เฉลี่ย 38% vs ทั้งหมด 12%)** · Fuel_Cost ต่ำ (−0.61) | "พึ่งพานิวเคลียร์" |
> | Arizona, Central, Florida, Kentucky, Oklahoma, Southern, Texas | 7 | **Cost ต่ำ (−1.01) · RoR สูง (+0.80)** · Fixed_charge ค่อนข้างสูง (+0.52) | "ต้นทุนต่ำ ผลตอบแทนดี" |
>
> โครงประโยค: *"กลุ่ม [n] ประกอบด้วย [สมาชิก] มี [ตัวแปร] **สูง/ต่ำกว่า**ค่าเฉลี่ยมาก ([ค่า] vs [ค่าเฉลี่ย]) → [ความหมายเชิงธุรกิจ]"*
> สอดคล้องกับข้อสังเกตในสไลด์ p.11 (scatter Sales × Fuel Cost เห็น 3 กลุ่ม: fuel แพง+ขายน้อย / fuel ถูก+ขายมาก / fuel ถูก+ขายน้อย)

### ทำนายกลุ่มของจุดใหม่ + วาดบน PCA 2D

```python
# บริษัทใหม่ → ต้อง transform ด้วย scaler ตัวเดิม (เหมือน W11) แล้ว predict
new_util = pd.DataFrame([[1.10, 11.0, 160, 56.0, 3.0, 14000, 0.0, 0.70]], columns=util.columns)
print("cluster ของบริษัทใหม่:", km4.predict(pd.DataFrame(scaler.transform(new_util), columns=util.columns)))

pcs = PCA(n_components=2).fit(Z)
P = pcs.transform(Z)
fig, ax = plt.subplots(figsize=(6, 5))
sc = ax.scatter(P[:, 0], P[:, 1], c=km4.labels_, cmap="tab10", s=60)
for name, (a, b) in zip(util.index, P):
    ax.annotate(name, (a, b), fontsize=7, xytext=(3, 3), textcoords="offset points")
ax.set_xlabel(f"PC1 ({pcs.explained_variance_ratio_[0]:.0%})"); ax.set_ylabel(f"PC2 ({pcs.explained_variance_ratio_[1]:.0%})")
ax.set_title("K-Means (k=4) on PCA 2D")
plt.savefig("/tmp/lab06_pca.png", dpi=100)
```

> [!warning] ผลไม่ตรงกับ RapidMiner/เพื่อน = ปกติ (สไลด์ p.24 *"Result can vary significantly depending on initial choice of seeds"*)
> ทดลองจริง (z-score แบบ RapidMiner, $n-1$): สไลด์ p.30 (RapidMiner k = 6, max runs 50) ได้ SSE **59.10** · sklearn (`n_init=50`) ได้ SSE **58.15** — Kentucky กับ Boston อยู่คนละกลุ่มกัน · ทั้งคู่เป็น local optimum → เลขกลุ่ม (cluster_0, cluster_1) ก็สลับได้ ให้เทียบที่ "สมาชิก" ไม่ใช่ "เลขกลุ่ม"

### ⚙️ RapidMiner — k-Means (สร้างตามสไลด์ clustering p.26)

```
Retrieve Utilities → Set Role (Company = id) → Normalize (Z-transformation)
   → Clustering (k-Means) ─clu─→ Multiply ─→ Cluster Model Visualizer
                          ─mod─→ Multiply ─→ Performance (Cluster Distance Performance) ─per─→ res
```
| operator | ตั้งค่า |
|---|---|
| **Clustering (k-Means)** | ✅ add cluster attribute · **k = 4** · **max runs = 50** · ✅ determine good start values · measure types = NumericalMeasures · EuclideanDistance · max optimization steps 100 |
| **Cluster Distance Performance** | ต่อ **exa** (ข้อมูลที่มีคอลัมน์ cluster) + **clu** (cluster model) · **main criterion** = `Avg. within centroid distance` หรือ `Davies Bouldin` |

**ผลที่ได้ (Results):** ExampleSet มีคอลัมน์ `cluster` (cluster_0…) · **Cluster Model** → Description (จำนวนสมาชิก) · **Folder View** (ใครอยู่กลุ่มไหน) · **Centroid Table** (z-score ของ centroid) · **Centroid Chart** · **Heat Map** (ใน Cluster Model Visualizer)

**วาด elbow ใน RapidMiner (สไลด์ p.31):** ครอบ `k-Means` + `Cluster Distance Performance` ด้วย **`Optimize Parameters (Grid)`** → Edit Parameter Settings: **Clustering.k** = 2…10 → ใส่ **`Log`** ต่อจาก Cluster Distance Performance แล้ว **log → Edit List**: คอลัมน์ `k` = operator *Clustering* → parameter *k* · คอลัมน์ `avg_within` = operator *Cluster Distance Performance* → value **avg_within_distance** → นอก Optimize ใส่ `Log to Data` (log name = Log) → Visualizations แบบ Lines → หาข้อศอก (ไฟล์ที่รันทดสอบแล้ว: `final/mock_lab/recipes/elbow_kmeans.rmp`)

> [!example] ผลจริงจาก RapidMiner (Utilities, Z-transformation, max runs 50)
> | k | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
> |---|---|---|---|---|---|---|---|---|---|
> | avg within centroid distance | 6.27 | 4.65 | 3.67 | 3.09 | 2.62 | 2.23 | 1.91 | 1.67 | 1.45 |
>
> ลดลงทุกครั้งที่เพิ่ม k (เหมือน WCSS) · ลดมากช่วง k = 2→4 แล้วค่อย ๆ แบน → ข้อศอกประมาณ **k = 4**

> [!warning] ⚠️ เครื่องหมายของตัวเลข clustering ใน RapidMiner (ยืนยันด้วยการรันจริง)
> - ใน **PerformanceVector** ทั้ง **Avg. within centroid distance (−3.654)** และ **Davies Bouldin (−1.177)** ถูกแสดงเป็น **ค่าติดลบ** เพราะ RapidMiner ถือว่า "ยิ่งมากยิ่งดี" จึงคูณ −1 ให้ตัวที่ "ยิ่งน้อยยิ่งดี" → อ่านเป็นค่าสัมบูรณ์ · ทั้งสองค่า **ต่ำ = ดี**
> - ค่าใน `Log` (value `avg_within_distance`) เป็น **ค่าบวก**
> - **Avg. within centroid distance = WCSS ÷ จำนวนแถว** (ค่าเฉลี่ยของระยะทาง*กำลังสอง*ถึง centroid) → k = 4 ได้ 80.38 / 22 = 3.654 ตรงกับ sklearn `inertia_ / n`

---

## 6.3 Association Rules ⭐⭐⭐

**นิยาม (สไลด์ Apriori p.12–13, 25):**
$$\text{support}(X\to Y)=\frac{\sigma(X\cup Y)}{N}\quad\text{confidence}(X\to Y)=\frac{\sigma(X\cup Y)}{\sigma(X)}\quad\text{lift}(X\to Y)=\frac{\text{confidence}(X\to Y)}{\text{support}(Y)}$$
lift **> 1** = ซื้อด้วยกันบ่อยกว่าบังเอิญ (positive correlation) · **= 1** = อิสระกัน · **< 1** = ซื้อด้วยกันน้อยกว่าบังเอิญ · การคำนวณมือ + Apriori ทีละรอบ: [[LEC 10 Association Rules]]

### ข้อมูล 2 รูปแบบที่ต้องแปลงให้เป็น

```python
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules

# แบบ ① "ตะกร้า" (list ของรายการ) — สไลด์ Apriori p.3 (Bread/Milk)
baskets = [["Bread", "Milk"], ["Bread", "Diaper", "Beer", "Eggs"], ["Milk", "Diaper", "Beer", "Coke"],
           ["Bread", "Milk", "Diaper", "Beer"], ["Bread", "Milk", "Diaper", "Coke"]]
te = TransactionEncoder()
onehot = pd.DataFrame(te.fit(baskets).transform(baskets), columns=te.columns_)   # → ตาราง True/False (p.28)
print(onehot.astype(int))

freq = apriori(onehot, min_support=0.4, use_colnames=True)          # minsup 40% = อย่างน้อย 2 ใน 5 ตะกร้า
rules = association_rules(freq, metric="confidence", min_threshold=0.6)
print(rules[["antecedents", "consequents", "support", "confidence", "lift"]].round(2).to_string())
```

```python
# แบบ ② ตาราง 0/1 ต่อสินค้า (BeautyCo — สไลด์ Apriori p.35–41 และ W10 ของคุณ)
beauty = pd.read_excel("W10/BeautyCo_68.xls")
beauty.columns = beauty.columns.str.strip()             # ⚠️ ชื่อคอลัมน์จริงคือ "Trans. " (มีช่องว่างท้าย)
items = beauty.drop(columns="Trans.").astype(bool)       # mlxtend ต้องการ True/False

print(items.mean().sort_values(ascending=False).head(3).round(3))     # Base_Makeup 0.536 · Glossy_Lips 0.490 · Eye_Liner 0.457
freq_b = fpgrowth(items, min_support=0.2, use_colnames=True)          # FP-Growth = ผลเหมือน Apriori แต่เร็วกว่า
print("frequent itemsets:", len(freq_b))                               # 23 (ตรงกับสไลด์ p.39)
rules_b = association_rules(freq_b, metric="confidence", min_threshold=0.7)
rules_b = rules_b.sort_values("lift", ascending=False)
print(rules_b[["antecedents", "consequents", "support", "confidence", "lift"]].round(3).to_string(index=False))
```

> [!example] ผลจริง = สไลด์ Apriori p.39 ทุกตัว
> | Premises → Conclusion | support | confidence | lift |
> |---|---|---|---|
> | Eye_Palette → Eye_Enhancer | 0.321 | 0.843 | 2.360 |
> | **Eye_Enhancer → Eye_Palette** | 0.321 | **0.899** | 2.360 |
> | Glossy_Lips → Base_Makeup | 0.356 | 0.727 | 1.355 |

> [!important] ⭐ ประโยคตีความกฎ (ใช้กับทุกกฎ — ครบ 3 ค่า)
> **Eye_Enhancer → Eye_Palette** (s = 0.321, c = 0.899, lift = 2.36):
> - **support:** *"ลูกค้า **32.1% ของทุก transaction** ซื้อทั้ง Eye Enhancer และ Eye Palette"*
> - **confidence:** *"ในบรรดาคนที่ซื้อ Eye Enhancer **89.9%** ซื้อ Eye Palette ด้วย"*
> - **lift:** *"โอกาสซื้อ Eye Palette เมื่อซื้อ Eye Enhancer สูงกว่าโอกาสทั่วไป **2.36 เท่า** → ความสัมพันธ์จริง ไม่ใช่บังเอิญ (lift > 1)"*
> - **ข้อเสนอ:** bundle "2 Styles Glam Eye Look" / วางสินค้าใกล้กัน / แนะนำ Eye Palette ตอนลูกค้าหยิบ Eye Enhancer (สไลด์ p.40)
> ⚠️ **confidence สูงอย่างเดียวไม่พอ** — ถ้า Y ขายดีอยู่แล้ว confidence ก็สูงได้เอง → ต้องดู lift (สไลด์ p.25 tea → coffee: confidence 80% แต่ lift 0.89 < 1)

### ข้อมูลที่มีตัวเลข/หลายค่า → ต้อง discretize + one-hot ก่อน (HW8)

```python
bankd = pd.read_csv("HW8/bank-data.csv")
basket = pd.DataFrame({
    "age": pd.qcut(bankd["age"], 3, labels=["YOUNG", "MIDDLE", "SENIOR"]),      # equal frequency
    "income": pd.qcut(bankd["income"], 3, labels=["LOW", "MID", "HIGH"]),
    "children": pd.cut(bankd["children"], [-1, 0, 2, 10], labels=["0", "1-2", "3+"]),
    "married": bankd["married"], "car": bankd["car"], "mortgage": bankd["mortgage"], "pep": bankd["pep"],
})
items_bank = pd.get_dummies(basket, prefix_sep="=").astype(bool)       # 1 item = 1 คู่ attribute=value (สไลด์ p.33)
rules_pep = association_rules(apriori(items_bank, min_support=0.1, use_colnames=True),
                              metric="confidence", min_threshold=0.7)
rules_pep = rules_pep[rules_pep["consequents"] == frozenset({"pep=YES"})]   # เฉพาะกฎที่ทำนาย pep=YES
print(rules_pep.sort_values("lift", ascending=False)[["antecedents", "support", "confidence", "lift"]].head(3).round(3))
```

### ⚙️ RapidMiner — FP-Growth + Create Association Rules (ตาม W10 sheet และสไลด์ p.39)

```
Read Excel (BeautyCo) → Set Role (Trans. = id) → Numerical to Binominal (all, min 0, max 0)
   → FP-Growth ─fre─→ Create Association Rules ─rul─→ res
```
| operator | ตั้งค่า |
|---|---|
| **Numerical to Binominal** | attribute filter type = `all` · **min = 0, max = 0** → 0 = `false`, 1 = `true` |
| **FP-Growth** | input format = `items in dummy coded columns` · **positive value = `true`** · min requirement = `support` · **min support = 0.2** · (ถ้าผลน้อยเกิน ติ๊ก find min number of itemsets ออก) |
| **Create Association Rules** | criterion = `confidence` · **min confidence = 0.7** |

**ผล:** **Frequent Itemsets** (Size · Support · Item 1 · Item 2…) · **AssociationRules** ตาราง: No. · Premises · Conclusion · **Support · Confidence** · LaPlace · Gain · p-s · **Lift** · Conviction → คลิกหัวคอลัมน์ Lift เพื่อเรียง · มุมมอง Graph แสดงเป็นเครือข่าย
> ข้อมูล nominal (Yes/No หลายคอลัมน์ เช่น bank-data) → **`Nominal to Binominal`** แทน · ตัวเลข → **`Discretize by Frequency`** ก่อน แล้วค่อย Nominal to Binominal

---

## 🏋️ Drills (closed-book)

> [!question]- D1. elbow plot ของคุณ WCSS = 8000, 3000, 1000, 800, 600, 500 (k = 1…6) เลือก k เท่าไร เพราะอะไร
> **k = 3** — ลดลงมาก 5000 → 2000 แล้วหลัง k = 3 ลดลงทีละ 200 ซึ่งแบนลง (สไลด์ clustering p.28: *"select the number of clusters where the change in WCSS begins to level off"*)

> [!question]- D2. ทำไมต้อง normalize ก่อน K-Means และถ้าลืมจะเกิดอะไรกับข้อมูล Utilities
> K-Means ใช้ Euclidean distance · Sales (3,300–17,441) มีช่วงกว้างกว่า Fixed_charge (0.75–1.49) หลายพันเท่า → ระยะทางแทบจะเป็น "ผลต่างของ Sales" อย่างเดียว → กลุ่มที่ได้คือ "แบ่งตามยอดขาย" ไม่ได้ใช้ตัวแปรอื่นเลย

> [!question]- D3. กฎ {Milk} → {Diaper, Beer} จาก 5 ตะกร้า Bread/Milk หา support, confidence, lift
> σ(Milk, Diaper, Beer) = 2 (T3, T4) · σ(Milk) = 4 · σ(Diaper, Beer) = 3
> support = 2/5 = **0.4** · confidence = 2/4 = **0.5** · lift = 0.5 / (3/5) = **0.83** (< 1 → ไม่ควรใช้กฎนี้ทำโปรโมชัน)

> [!question]- D4. (RapidMiner) FP-Growth แจ้ง error ว่าข้อมูลต้องเป็น binominal ทั้งที่ CSV เป็น 0/1 แก้อย่างไร
> ใส่ **`Numerical to Binominal`** (min = max = 0) ก่อน FP-Growth แล้วตั้ง **positive value = true** · อย่าลืม Set Role คอลัมน์ Trans./ID เป็น **id** (ไม่งั้นมันกลายเป็น item)

> [!question]- D5. ถ้าตั้ง min support ต่ำมาก (0.01) จะเกิดอะไร
> ได้ frequent itemsets และกฎ **จำนวนมหาศาล** (ส่วนใหญ่เกิดจากไม่กี่ transaction → ไม่น่าเชื่อถือ) และคำนวณช้า (สไลด์: *"Frequent itemset generation is still computationally expensive"*) · ตั้งสูงเกิน → ไม่เจอกฎเลย

---

**ถัดไป →** [[LAB 07 Reading & Explaining Results]] · **กลับหน้าหลัก →** [[LAB 00 START HERE]]
