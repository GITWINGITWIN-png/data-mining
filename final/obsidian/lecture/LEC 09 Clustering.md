---
title: LEC 09 · Clustering (K-Means)
exam: Lecture — จ. 19 ต.ค. 2569 16:00–19:00
guideline: "Lecture ข้อ 5 — unsupervised learning · preprocessing สำหรับ clustering · K-Means และ parameters · เลือกจำนวน clusters · ประเมินด้วย interpretability, cohesion, separation"
source: 69_1_basic_clustering.pdf (59 pp) · HW9 · W11
tags: [final, lecture, clustering, kmeans, elbow, silhouette, cohesion, separation]
---

# LEC 09 · Clustering — K-Means
### หากลุ่มของข้อมูลโดยไม่มี label: "อะไรอยู่ด้วยกัน"

> [!abstract] guideline ข้อ 5 (5 หัวข้อ)
> 1. **Unsupervised learning และ data clustering** → [[#9.1 Unsupervised Learning & Clustering ⭐⭐]]
> 2. **Data preprocessing สำหรับ clustering** → [[#9.2 Preprocessing สำหรับ Clustering ⭐⭐⭐]]
> 3. **K-Means algorithm และ parameters** → [[#9.3 K-Means Algorithm ⭐⭐⭐⭐]] · [[#9.4 Parameters & ข้อจำกัด ⭐⭐⭐]]
> 4. **การเลือกจำนวน clusters** → [[#9.5 เลือกจำนวน Cluster ⭐⭐⭐⭐]]
> 5. **การประเมินผลด้วย interpretability, cohesion และ separation** → [[#9.6 ประเมินผล — Cohesion · Separation · Interpretability ⭐⭐⭐⭐]]

**ลิงก์:** [[LEC 00 START HERE|หน้าหลัก Lecture]] · [[LEC 03 PCA]] · [[LEC 10 Association Rules]] · Lab: [[LAB 06 Clustering & Association#6.2 K-Means + เลือกจำนวน cluster ⭐⭐⭐]] · งานของคุณ: HW9, W11

---

## 9.1 Unsupervised Learning & Clustering ⭐⭐

> [!quote] สไลด์ p.4–8
> - Clustering = **unsupervised** — *"no target (outcome) variable, no given classes"* ต่างจาก classification (supervised มี label)
> - **"Association Rules: what happens together? · Clustering: what belongs together?"**
> - เป้าหมาย: **"Intra-cluster distances are MINIMIZED · Inter-cluster distances are MAXIMIZED"** (ในกลุ่มใกล้กัน · ระหว่างกลุ่มห่างกัน)
> - การใช้: แบ่งกลุ่มลูกค้า (market segmentation), จัดกลุ่มบริษัท (Utilities), ตรวจจับความผิดปกติ, ย่อข้อมูล

**ชนิดของ clustering (p.12–15):** **Partitional** (K-Means — แบ่งเป็น k กลุ่มไม่ซ้อนกัน) · **Hierarchical** (dendrogram — กลุ่มซ้อนกันเป็นชั้น) · **Density-based** (กลุ่มตามความหนาแน่น) · p.15: *"Notion of a cluster can be AMBIGUOUS"* — ข้อมูลชุดเดียวมองเป็น 2, 4 หรือ 6 กลุ่มก็ได้

---

## 9.2 Preprocessing สำหรับ Clustering ⭐⭐⭐

> [!important] ⭐ สไลด์ p.21–22
> **Pre-processing:** (1) **Normalize the data** (2) **Dimension reduction** (3) **Eliminate outliers**
> **Post-processing:** ตัดกลุ่มเล็กที่อาจเป็น outlier · **split** กลุ่มที่ 'หลวม' · **merge** กลุ่มที่ 'ใกล้กัน'
>
> **ทำไมต้อง normalize (p.21):** *"Raw distance measures are highly influenced by scale of measurements → normalize (standardize) the data first: subtract mean, divide by std. deviation — also called z-scores"*
> Utilities: Sales 3,300–17,441 vs Fixed_charge 0.75–1.49 → ไม่ normalize = จัดกลุ่มตาม Sales อย่างเดียว

**เพิ่มเติม:** เลือกเฉพาะ attribute ที่เกี่ยวกับ "ความเหมือน" ที่ต้องการ · ตัด ID/ชื่อ (RapidMiner: role = id) · categorical → one-hot (K-Means ใช้กับตัวเลขเท่านั้น — p.17) · ระยะทางอื่น (p.21): correlation, **Jaccard** (categorical), **Gower** (ผสม), angle/cosine (ข้อความ), DTW (time series)

---

## 9.3 K-Means Algorithm ⭐⭐⭐⭐

> [!important] ⭐⭐ ขั้นตอน (p.17)
> 1. **เลือก K** centroid เริ่มต้น (สุ่ม หรือ K-Means++)
> 2. **Assign:** ให้แต่ละจุดเข้ากลุ่มของ centroid ที่ **ใกล้ที่สุด** (Euclidean)
> 3. **Update:** ย้าย centroid ไปที่ **ค่าเฉลี่ย (mean)** ของสมาชิก
> 4. **ทำซ้ำ** 2–3 จนไม่มีจุดย้ายกลุ่ม (converge) หรือการเปลี่ยนแปลงต่ำกว่า threshold
>
> **Objective (p.16):** minimize **SSE (WCSS)** $=\sum_{i=1}^{k}\sum_{p\in C_i}\lVert p-m_i\rVert^2$ (m_i = centroid ของ C_i)
> **Complexity (p.39):** $O(tkn)$ — n = จำนวนจุด, k = จำนวนกลุ่ม, t = จำนวนรอบ (k, t ≪ n) → **เร็ว**
> p.20: ระหว่างรอบ สิ่งที่เปลี่ยนคือ **boundary, centroid, สมาชิก** — ตัวข้อมูลไม่เปลี่ยน

![[lec_kmeans_iter.png]]

> [!example] ⭐⭐ K-Means ด้วยมือ 9 จุด (HW9 ของคุณ) — คำนวณยืนยันแล้ว
> A1 (3,8) · A2 (9,4) · A3 (4,9) · A4 (2,2) · A5 (10,5) · A6 (2,4) · A7 (6,8) · A8 (4,3) · A9 (4,7) · **seed = A1, A4, A7** · k = 3
> **รอบ 1** (centroid = A1, A4, A7): C1 = {A1, A3, A9} → (3.67, 8) · C2 = {A4, A6, A8} → (2.67, 3) · C3 = {A2, A5, A7} → (8.33, 5.67) · SSE = 24.67
> **รอบ 2:** A7 ย้ายไป C1 (ใกล้ (3.67, 8) กว่า (8.33, 5.67)) → C1 = {A1, A3, A7, A9} → **(4.25, 8)** · C2 = {A4, A6, A8} → **(2.67, 3)** · C3 = {A2, A5} → **(9.5, 4.5)** · SSE = **12.42**
> **รอบ 3:** ไม่มีจุดย้าย → **converge** (ต้องรัน 3 รอบ โดยรอบ 3 ยืนยันว่าไม่เปลี่ยน)
> ⚠️ ตารางระยะทางในโจทย์ HW9 เป็น **ระยะทางยกกำลังสอง** (A1–A2 = 6² + 4² = 52) — ใช้เปรียบเทียบได้เลยเพราะลำดับเท่าเดิม (ไม่ต้องถอดราก)

> [!tip] วิธีทำมือในห้องสอบ
> ทำตาราง: แถว = จุด · คอลัมน์ = ระยะ² ถึงแต่ละ centroid · วงค่าต่ำสุด → สมาชิก → เฉลี่ย x และ y ของสมาชิกแต่ละกลุ่ม = centroid ใหม่ · ทำจนสมาชิกไม่เปลี่ยน

---

## 9.4 Parameters & ข้อจำกัด ⭐⭐⭐

| parameter | ความหมาย | sklearn `KMeans` | RapidMiner `k-Means` |
|---|---|---|---|
| **k** | จำนวนกลุ่ม (ต้องกำหนดเอง) | `n_clusters` | k |
| **การเลือก seed** | สุ่ม / **K-Means++** (p.24 *"[Arthur & Vassilvitskii 2007] to determine good start seeds"*) | `init="k-means++"` | determine good start values ✅ |
| 📚 **จำนวนครั้งที่สุ่มใหม่** | รันหลายรอบเก็บ SSE ต่ำสุด | `n_init` ("auto") | max runs (10) |
| 📚 **รอบสูงสุด** | — | `max_iter` (300) | max optimization steps (100) |
| ระยะทาง | Euclidean | Euclidean | measure types / numerical measure |

> [!important] ⭐ ข้อจำกัดของ K-Means (p.24, 32–39)
> - **ต้องกำหนด k ล่วงหน้า**
> - **ไวต่อ seed เริ่มต้น** — *"Result can vary significantly depending on initial choice of seeds"* → local optimum (ทดลอง: RapidMiner SSE 59.10 vs sklearn 58.15 บน Utilities k = 6)
> - **ไวต่อ outlier** — centroid = mean ถูก outlier ดึง (p.32: mean ของ 1, 3, 5, 7, 1009 = **205** แต่ median = **5**) → ทางแก้: **K-Medoids** (ใช้จุดจริงเป็นศูนย์กลาง)
> - ทุกจุดถูกบังคับให้อยู่ในกลุ่มใดกลุ่มหนึ่ง
> - ไม่เหมาะกับกลุ่มที่ **ขนาดต่างกันมาก · ความหนาแน่นต่างกัน · รูปร่างไม่กลม (non-globular)** (p.33–35) → ทางแก้: ใช้ k มาก ๆ แล้วรวมทีหลัง (p.36)

---

## 9.5 เลือกจำนวน Cluster ⭐⭐⭐⭐

![[lec_elbow_silhouette.png]]

> [!important] ⭐ Elbow method (p.28–31)
> **"First, draw relationship between the number of clusters and Within Cluster Sum of Squares (WCSS), then select the number of clusters where the change in WCSS begins to LEVEL OFF."**
> WCSS = ผลรวมระยะทาง² จากสมาชิกถึง centroid ของกลุ่มตัวเอง (p.53) · **WCSS ลดลงเสมอเมื่อ k เพิ่ม** (k = n → 0) → ห้ามเลือก k ที่ WCSS ต่ำสุด · ตัวอย่าง p.28: WCSS 8000 → 3000 → **1000** → 800 → 600… → elbow ที่ **k = 3**
> RapidMiner (p.31): `Optimize Parameters (Grid)` ครอบ k-Means → วาด **Avg. within centroid distance** vs k

> [!important] 📚 Silhouette (Rousseeuw 1987 — สไลด์ไม่ได้สอน แต่ใช้ใน HW9)
> สำหรับจุด i: **a(i)** = ระยะเฉลี่ยถึงจุดอื่นใน **กลุ่มเดียวกัน** (cohesion) · **b(i)** = ระยะเฉลี่ยถึงจุดใน **กลุ่มอื่นที่ใกล้ที่สุด** (separation)
> $$s(i)=\frac{b(i)-a(i)}{\max\{a(i),b(i)\}}\in[-1,1]$$
> ใกล้ 1 = อยู่ถูกกลุ่ม แยกชัด · ≈ 0 = อยู่ตรงขอบ · < 0 = น่าจะอยู่ผิดกลุ่ม · **silhouette ของทั้งชุด = ค่าเฉลี่ย** → เลือก k ที่ค่าเฉลี่ยสูงสุด

> [!example]- 🧮 Silhouette ด้วยมือ (1 มิติ): จุด 1, 2, 3 (กลุ่ม A) และ 8, 9 (กลุ่ม B)
> จุด 1: a = (1 + 2)/2 = 1.5 · b = (7 + 8)/2 = 7.5 → s = (7.5 − 1.5)/7.5 = **0.80**
> จุด 3: a = (2 + 1)/2 = 1.5 · b = (5 + 6)/2 = 5.5 → s = 4/5.5 = **0.727**
> จุด 8: a = 1 · b = (7 + 6 + 5)/3 = 6 → s = 5/6 = **0.833**
> เฉลี่ยทั้ง 5 จุด (0.800, 0.846, 0.727, 0.833, 0.857) = **0.813** → แยกกลุ่มได้ดีมาก

> [!example] Utilities (standardized, n_init = 50)
> silhouette: k = 2 → 0.185 · 3 → 0.230 · 4 → 0.234 · **5 → 0.248** · 6 → 0.241 · 7 → 0.230 · 8 → 0.219 → เลือก **k = 4–5** + ดูการตีความ · สไลด์ p.56: ที่ k = 3 *"clusters 1 & 2 well defined, not so for cluster 3. Next step: try again with k = 2 or k = 4"*

---

## 9.6 ประเมินผล — Cohesion · Separation · Interpretability ⭐⭐⭐⭐

> [!important] ⭐⭐ 3 เกณฑ์ของ guideline
> | เกณฑ์ | วัดอะไร | ตัวชี้วัด | อยากได้ |
> |---|---|---|---|
> | **Cohesion** (ความแน่นในกลุ่ม) | สมาชิกใกล้ centroid / ใกล้กันแค่ไหน | **WCSS** · **average within-centroid distance** (p.54) · a(i) ของ silhouette | **ต่ำ** |
> | **Separation** (ความห่างระหว่างกลุ่ม) | กลุ่มต่าง ๆ ห่างกันแค่ไหน | **distance between centroids** (p.57) · *"ratio of between-cluster variation to within-cluster variation"* (p.51) · b(i) | **สูง** |
> | ผสมทั้งสอง | — | **Davies–Bouldin** (p.55: *"low intra- and high inter-cluster distance → low DBI · smallest DBI is the best"*) · 📚 silhouette | DBI ต่ำ · silhouette สูง |
> | **Interpretability** (อธิบายได้) | กลุ่มมีความหมายเชิงธุรกิจไหม | **centroid / summary stat ต่อกลุ่ม** · เทียบ cluster mean กับ population mean · กราฟ (p.41–48) | ตั้งชื่อกลุ่มได้ นำไปใช้ได้ |

> [!example] ⭐ Utilities k = 3 (สไลด์ p.52–57)
> **Cohesion — average distance ภายในกลุ่ม (p.56):** C1 (12 บริษัท) 1748.3 · C2 (3) 907.7 · C3 (7) **3625.2** · overall = (12·1748.3 + 3·907.7 + 7·3625.2)/22 = **2230.9**
> → *"Clusters 1 & 2 well defined, not so for cluster 3"* (C3 กระจายกว้างที่สุด)
> **Separation — distance between clusters (p.57):** d(1,2) = **5.03** · d(1,3) = 3.17 · d(2,3) = 3.77 → *"1 and 2 well-separated, cluster 3 not as much"*

> [!quote] Interpretability (p.40–48)
> **"Finding clusters is not often an end in itself"** → ต้องอธิบายได้ว่าแต่ละกลุ่มคืออะไร:
> - **summary statistics ต่อกลุ่ม** (centroid table) · **เทียบ cluster mean กับ population mean**
> - **visualization:** 2D scatter, PCA plot (N-D), pie chart (categorical — วงในกลุ่ม/วงนอกประชากร p.47), histogram เทียบกลุ่มกับทั้งหมด (p.48)
> - RapidMiner: Centroid Table, Centroid Chart, Heat map, Cluster Model Visualizer (p.44–45)

> [!example] ตีความ Utilities k = 4 (จาก Lab)
> ขายมาก + เชื้อเพลิงถูก (Idaho, Nevada, Puget) · เชื้อเพลิงแพง ขายน้อย (Boston, NY, Hawaiian, …) · พึ่งพานิวเคลียร์ (Commonwealth, Madison, Northern, Wisconsin, Virginia) · ต้นทุนต่ำ ผลตอบแทนดี (Arizona, Central, Florida, …) — ตรงกับข้อสังเกตในสไลด์ p.11 (Sales × Fuel Cost)

**Accuracy (p.58):** ถ้ามี label จริงอยู่แล้ว (ใช้ทดสอบ) เทียบกลุ่มกับ label ด้วย precision/recall ได้ — แต่ปกติ clustering ไม่มี label

---

## ✅ Self-Test — LEC 09

> [!question]- Q1. จุด (1,1), (2,1), (4,3), (5,4) · k = 2 · seed = (1,1), (5,4) รัน K-Means 1 รอบ
> ระยะ² ถึง (1,1) / (5,4): (1,1) 0 / 25 → C1 · (2,1) 1 / 18 → C1 · (4,3) 13 / 2 → C2 · (5,4) 25 / 0 → C2
> centroid ใหม่: C1 = (1.5, 1) · C2 = (4.5, 3.5) · รอบถัดไปสมาชิกไม่เปลี่ยน → converge · SSE = 0.25 + 0.25 + 0.5 + 0.5 = **1.5**

> [!question]- Q2. ทำไมต้อง normalize ก่อน K-Means
> K-Means ใช้ Euclidean distance · ตัวแปรสเกลใหญ่ครองระยะทาง → กลุ่มที่ได้สะท้อนตัวแปรนั้นตัวเดียว (สไลด์ p.21)

> [!question]- Q3. elbow ไม่ชัด ควรทำอย่างไร
> ใช้ **silhouette** / Davies–Bouldin ช่วย + พิจารณา **interpretability** (กลุ่มอธิบายได้ ขนาดสมเหตุสมผล ไม่มีกลุ่ม 1 สมาชิกเยอะ) + เป้าหมายธุรกิจ (เช่น ทีมการตลาดดูแลได้ 4 กลุ่ม)

> [!question]- Q4. cohesion กับ separation ต่างกันอย่างไร ตัวชี้วัดละ 1 ตัว
> cohesion = ความแน่นภายในกลุ่ม (WCSS / avg within-centroid distance — ต่ำดี) · separation = ความห่างระหว่างกลุ่ม (ระยะระหว่าง centroid — สูงดี)

> [!question]- Q5. รัน K-Means 2 ครั้งได้ผลต่างกัน ผิดหรือไม่ แก้อย่างไร
> ไม่ผิด — K-Means ติด **local optimum** ขึ้นกับ seed · แก้: ใช้ **K-Means++** + รันหลายครั้ง (`n_init` / max runs) เก็บผล SSE ต่ำสุด · ตั้ง random seed เพื่อให้ทำซ้ำได้

> [!question]- Q6. ข้อมูลมี outlier มาก ควรใช้อะไรแทน K-Means
> **K-Medoids** — ใช้จุดจริง (medoid) เป็นศูนย์กลาง ไม่ถูก outlier ดึงเหมือน mean (สไลด์ p.32) หรือกำจัด outlier ก่อน (preprocessing)

---

**กลับหน้าหลัก →** [[LEC 00 START HERE]] · **ถัดไป →** [[LEC 10 Association Rules]]
