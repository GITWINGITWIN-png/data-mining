---
title: Star Schema Design Workshop — เดินครบทุกขั้นตอน
chapter: 13
tags: [midterm, star-schema, workshop, practice, worked-example]
---

# 13 · Star Schema Design Workshop
### เดินให้ครบทุกขั้นตอน ตั้งแต่ตั้งคำถามจนได้ผลลัพธ์

> [!info] จุดประสงค์ของบทนี้
> [[06 Multi-Dimensional Design]] สอนหลักการ (4-Step Process, Grain, Additivity, Keys) ไว้ครบแล้ว แต่หลักการอย่างเดียวไม่พอ — ต้อง **ลงมือทำจริงจนครบวงจร** ถึงจะมั่นใจ
>
> บทนี้มี 2 ส่วน:
> - **ส่วนที่ 1** — ผมเดินให้ดูครบทุกขั้นตอน บนโจทย์ที่ **ซับซ้อนพอสมควร** (มี 2 fact tables, role-playing dimension, conformed dimension, degenerate dimension — เกือบทุกคอนเซ็ปต์ของบทที่ 6 มารวมอยู่ในเคสเดียว)
> - **ส่วนที่ 2** — โจทย์ให้คุณลองทำเอง (เอามาจากเคสเปิดเรื่องใน [[05 Data Warehouse Concepts]] ที่ยังไม่เคยแก้ในวิชานี้!) พร้อม**เฉลยทีละขั้นแบบกดดูได้** ให้ลองทำก่อนแล้วค่อยเปิดเช็ค

**ลิงก์:** [[00 START HERE|หน้าหลัก]] · พื้นฐาน [[06 Multi-Dimensional Design]] · เชื่อมต่อ [[07 ETL]] · [[08 Reporting from Star Schema]]

---

# ส่วนที่ 1 — ตัวอย่างที่เดินครบ: "FoodGo" แอปสั่งอาหารเดลิเวอรี่

## 🎬 สถานการณ์ตั้งต้น

> [!quote] อีเมลจาก Head of Operations
> "ทีมงาน ตอนนี้ FoodGo โตจาก 5 ร้านค้าเป็น 500 ร้านค้าใน 50 จังหวัดแล้ว บอร์ดบริหารอยากเห็นแดชบอร์ดที่ตอบคำถามพวกนี้ได้:
>
> 1. **แต่ละร้านอาหารทำรายได้ให้เราเท่าไหร่ในแต่ละเดือน?**
> 2. **ไรเดอร์คนไหนส่งของช้าเป็นประจำ — และช้าตรงขั้นตอนไหน (รอร้านรับออเดอร์ หรือหาที่ส่งไม่เจอ)?**
> 3. **ออเดอร์ที่ถูกยกเลิก เกิดขึ้นบ่อยที่สุดตรงขั้นตอนไหนของกระบวนการ?**
> 4. **ลูกค้าคนไหนสั่งบ่อยและใช้โค้ดส่วนลดคุ้มค่าที่สุด?**
>
> ช่วยออกแบบฐานข้อมูลที่ตอบคำถามพวกนี้ได้หน่อย"

> [!tip] สังเกตอะไรได้จากอีเมลนี้ก่อนเริ่ม
> เหมือนเคสโรงพยาบาลที่เปิดเรื่องใน [[05 Data Warehouse Concepts#5.1 ทำไมต้องมี Data Warehouse — เคสโรงพยาบาล]] — **คำถามจาก CEO/ผู้บริหารมักมาแบบ "ยุ่งเหยิง" ไม่ได้บอก grain, ไม่ได้บอก dimension มาให้** งานของเราคือ**แปล**คำถามธุรกิจแบบนี้ให้เป็นภาษาการออกแบบ ผ่าน 4-Step Process

---

## Step 1 — Select the Business Process ⭐

> [!question] คำถามหลัก: **"What business activity are we analyzing?"**

ลองไล่คำถามทั้ง 4 ข้อดูว่าพูดถึง **กิจกรรมทางธุรกิจ** อะไรบ้าง:

| คำถาม | พูดถึงอะไร |
|---|---|
| Q1 รายได้ต่อร้าน | **เงิน** — ยอดขาย, ค่าส่ง, ส่วนลด |
| Q2 ไรเดอร์ช้าตรงขั้นไหน | **เวลา/กระบวนการ** — แต่ละขั้นตอนใช้เวลาเท่าไหร่ |
| Q3 ยกเลิกตรงขั้นไหน | **เวลา/กระบวนการ** — เหมือน Q2 |
| Q4 ลูกค้า + ส่วนลด | **เงิน** — เหมือน Q1 |

> [!important] ⭐ จุดตัดสินใจสำคัญที่สุดของขั้นนี้
> คำถามทั้ง 4 ข้อ **แบ่งเป็น 2 กลุ่มธรรมชาติ** ที่มีลักษณะต่างกันโดยพื้นฐาน:
> - **กลุ่ม "การเงิน" (Q1, Q4):** สนใจ **ยอดเงิน** ที่เกิดขึ้น ณ ตอนออเดอร์เสร็จ — ตัวเลขนิ่ง ไม่เปลี่ยนอีกหลังจากนั้น
> - **กลุ่ม "กระบวนการ" (Q2, Q3):** สนใจ **ระยะเวลาระหว่างขั้นตอน** ของออเดอร์เดียวกัน ตั้งแต่สั่งจนถึงส่งเสร็จ(หรือยกเลิก) — ข้อมูลนี้**ทยอยรู้ทีละขั้น** ไม่ได้มาพร้อมกันทั้งหมดตั้งแต่แรก
>
> นี่ตรงกับเหตุผลใน [[06 Multi-Dimensional Design#6.8 Multiple Fact Tables — เมื่อไหร่ต้องมีมากกว่า 1 ⭐]] ข้อ **"Different Measure Types"**: *transactional measures (additive events)* ≠ *accumulated measures (track progress through stages)*
>
> **✅ สรุป: เลือก 2 business process ไม่ใช่ 1**
> 1. **"Order Transaction"** — การเงินของออเดอร์ (ตอบ Q1, Q4)
> 2. **"Order Fulfillment Lifecycle"** — วงจรชีวิตของออเดอร์ (ตอบ Q2, Q3)

> [!warning] กับดักที่มือใหม่มักตกม้าตาย
> ถ้าพยายามยัดทุกอย่างลงตาราง fact เดียว จะเจอปัญหา: ตาราง fact ที่มีทั้ง `FoodAmount` (รู้ทันทีตอนสั่ง) และ `DeliveredTime` (รู้ทีหลังตอนส่งเสร็จ) ต้องเขียนทับแถวเดิมซ้ำ ๆ ระหว่างที่ order ยังไม่จบ — ผสมพฤติกรรมของ **Transaction Fact** (insert ครั้งเดียว) กับ **Accumulating Snapshot Fact** (update หลายครั้ง) เข้าด้วยกัน ทำให้ทั้งสอง pattern เสียหายทั้งคู่

---

## Step 2 — Declare the Grain ⭐⭐ (ขั้นสำคัญที่สุด)

> [!question] คำถามหลัก: **"What does each row in the fact table represent?"**

### ลองข้อเสนอที่ผิดก่อน (เพื่อเห็นว่าทำไมผิด)

> [!bug] ข้อเสนอที่ 1 (ผิด): **"1 แถว = ยอดขายรวมต่อร้านต่อวัน"**
> ฟังดูสมเหตุสมผลเพราะ Q1 ถามแค่ "รายได้ต่อร้านต่อเดือน" — แต่ **grain นี้หยาบเกินไปสำหรับ Q4** ("ลูกค้าคนไหนสั่งบ่อย") เพราะไม่มีข้อมูลระดับลูกค้า/ออเดอร์เหลืออยู่แล้ว (ถูกรวมทิ้งไปตอน aggregate)
>
> จำกฎจากบทที่ 6: **grain ที่ละเอียดกว่าเสมอสามารถ roll-up ขึ้นไปตอบคำถามหยาบได้ แต่ grain ที่หยาบแล้ว drill-down ลงไม่ได้อีกเลย** — ถ้าเลือกหยาบไปตั้งแต่แรก คำถามอย่าง Q4 จะตอบไม่ได้ตลอดกาล

**✅ Grain ที่ถูกต้อง สำหรับ Fact 1 (Order Transaction):**
> **"1 แถว = 1 ออเดอร์"**

**✅ Grain ที่ถูกต้อง สำหรับ Fact 2 (Order Fulfillment Lifecycle):**
> **"1 แถว = 1 ออเดอร์ ติดตามความคืบหน้าตลอดวงจรชีวิต"**

> [!tip] สังเกตอะไรได้: **grain ของ Fact ทั้งสองตัวเป็น "1 ออเดอร์" เหมือนกัน!**
> นี่คือตัวอย่างจริงของสิ่งที่ [[06 Multi-Dimensional Design#6.9 Different Types of Fact Tables ⭐⭐⭐ (guideline ข้อ 4.5 — ออกแน่)|บทที่ 6]] อธิบายไว้: **แม้ grain จะเท่ากัน แต่ "ชนิดของ fact table" ต่างกันได้** เพราะ **รูปแบบการเขียนข้อมูลต่างกัน**:
> - Fact 1 (Transaction): **INSERT ครั้งเดียว** ตอนออเดอร์เสร็จสมบูรณ์ ไม่แก้อีก
> - Fact 2 (Accumulating Snapshot): **INSERT ทันทีที่สั่ง (ค่าส่วนใหญ่เป็น NULL) แล้ว UPDATE ซ้ำ ๆ** ทุกครั้งที่ผ่านแต่ละขั้น (accepted → picked up → delivered/cancelled)

---

## Step 3 — Choose the Dimensions ⭐

> [!question] 3 คำถามช่วยคิด: ผู้ใช้จะ **filter** ด้วยอะไร / **group** ด้วยอะไร / อะไรให้ **context**

ใช้กรอบ **5W** จาก [[06 Multi-Dimensional Design#Step 3 · Choose the Dimensions]]:

| Dimension | ตอบคำถาม | เหตุผลที่ต้องมี |
|---|---|---|
| **Dim_Date** | When | ทุกคำถามมีมิติเวลา ("ในแต่ละเดือน") |
| **Dim_Customer** | Who (สั่ง) | Q4 ต้องรู้ว่าใครสั่ง |
| **Dim_Restaurant** | What/Where (แหล่งที่มา) | Q1 ต้อง group ตามร้าน |
| **Dim_Rider** | Who (ส่ง) | Q2 ต้อง group ตามไรเดอร์ |
| **Dim_Promo** | What (เงื่อนไข) | Q4 ต้องรู้ว่าใช้โค้ดไหน |

### ⭐ Dim_Date เป็น Role-Playing Dimension — จุดที่ซับซ้อนที่สุดของเคสนี้

> [!important] ทบทวนนิยามจาก [[06 Multi-Dimensional Design#6.6 Role-Playing Dimension ⭐⭐ (guideline ข้อ 4.6)]]
> **"A role-playing dimension is a dimension that has ONE physical representation but is referred to MORE THAN ONCE by the fact table."**

ใน **Fact 1 (Transaction)** ใช้ Dim_Date แค่ **1 บทบาท**: `OrderDateKey`

ใน **Fact 2 (Lifecycle)** ใช้ Dim_Date ถึง **4 บทบาท** — เพราะต้องรู้เวลาของทุกขั้นตอน (เพื่อตอบ Q2, Q3):

```sql
Fact_Order_Lifecycle
├── OrderPlacedDateKey (FK)  → Dim_Date  role 1: ลูกค้ากดสั่ง
├── AcceptedDateKey    (FK)  → Dim_Date  role 2: ร้านกดรับออเดอร์
├── PickedUpDateKey    (FK)  → Dim_Date  role 3: ไรเดอร์รับของจากร้าน
└── CompletedDateKey   (FK)  → Dim_Date  role 4: ส่งถึงลูกค้า (หรือถูกยกเลิก)
```

> [!tip] จำหลักการ: **"นักแสดงคนเดียว เล่นหลายบทในละครเรื่องเดียวกัน"**
> ตารางจริงมีแค่ `Dim_Date` เดียว แต่ตอน query ต้อง **สร้าง VIEW แยก 4 ตัว** (ตามที่ [[06 Multi-Dimensional Design#6.6 Role-Playing Dimension ⭐⭐ (guideline ข้อ 4.6)]] สอนไว้) เพื่อ join พร้อมกันได้โดยไม่ชนกัน:
> ```sql
> CREATE VIEW Dim_PlacedDate    AS SELECT * FROM Dim_Date;
> CREATE VIEW Dim_AcceptedDate  AS SELECT * FROM Dim_Date;
> CREATE VIEW Dim_PickedUpDate  AS SELECT * FROM Dim_Date;
> CREATE VIEW Dim_CompletedDate AS SELECT * FROM Dim_Date;
> ```

### ⭐ Dim_Restaurant / Dim_Rider เป็น Conformed Dimension

> [!important] ทบทวนนิยามจาก [[06 Multi-Dimensional Design#6.8 Multiple Fact Tables — เมื่อไหร่ต้องมีมากกว่า 1 ⭐]]
> **dimension ที่ fact table หลายตัวใช้ร่วมกัน**

`Dim_Restaurant` และ `Dim_Rider` ถูกใช้ **ทั้ง 2 fact table** — เพราะทั้งร้านอาหารและไรเดอร์เกี่ยวข้องกับทั้งมุมการเงิน (Q1) และมุมกระบวนการ (Q2) พร้อมกัน ส่วน `Dim_Customer` กับ `Dim_Promo` ใช้เฉพาะ **Fact 1** เท่านั้น (Q2, Q3 ไม่ได้ถามถึงลูกค้าหรือโปรโมชั่นเลย)

---

## Step 4 — Identify the Facts (Measures) ⭐⭐

> [!question] คำถามหลัก: **"What are we measuring?"**

### Fact 1 — Order Transaction

| Measure | Additivity | เหตุผล |
|---|---|---|
| `FoodAmount` | **Additive** | รวมข้ามร้าน/ลูกค้า/วันได้ทุกทาง — ตรงกับนิยาม *"can be summed across all dimensions"* |
| `DeliveryFee` | **Additive** | เหมือนกัน |
| `DiscountAmount` | **Additive** | เหมือนกัน |
| `ItemCount` | **Additive** | นับจำนวนชิ้น รวมกันได้ |

### Fact 2 — Order Fulfillment Lifecycle

| Measure | Additivity | เหตุผล |
|---|---|---|
| `MinutesToAccept` | **Additive** (แต่มักรายงานเป็น AVG) | ดูละเอียดด้านล่าง ⬇️ |
| `MinutesToPickup` | **Additive** | เหมือนกัน |
| `MinutesToDeliver` | **Additive** | เหมือนกัน |
| `TotalLifecycleMinutes` | **Additive** | เหมือนกัน |

> [!warning] ⭐ จุดที่ทำให้คนสับสนบ่อยที่สุด — "Additive" ไม่ได้แปลว่า "ควรรายงานด้วย SUM เสมอ"
> `MinutesToAccept` **บวกกันข้าม dimension ได้จริงและมีความหมาย** (SUM ของนาทีทั้งหมดที่ร้านใช้ตอบรับออเดอร์ในหนึ่งวัน = "ภาระงานรวม" ซึ่งมีประโยชน์กับฝ่ายปฏิบัติการ) → ผ่านนิยาม **Additive** ตามตำรา
>
> แต่ **ในทางปฏิบัติ ธุรกิจแทบไม่เคยอยากได้ SUM ของนาที** — สิ่งที่ Q2 ("ไรเดอร์คนไหนส่งช้า") ต้องการจริง ๆ คือ **AVG(MinutesToPickup) ต่อไรเดอร์** ไม่ใช่ผลรวม
>
> **บทเรียน:** Additive/Semi-additive/Non-additive เป็นเรื่อง **"บวกข้าม dimension แล้วความหมายยังอยู่หรือเปล่า"** ล้วน ๆ — ไม่ใช่เรื่อง **"สถิติที่ธุรกิจนิยมใช้ดู"** สองเรื่องนี้แยกกัน อย่าเอามาปนกัน

**ตัวอย่างที่ไม่ใช่ measure แต่หลายคนพยายามยัดเป็น measure:**

> [!bug] `FinalStatus` ('Delivered' / 'Cancelled_By_Restaurant' / 'Cancelled_By_Rider' / 'In_Progress') **ไม่ใช่ measure**
> เป็นค่าที่**บวกกันไม่ได้เลยในทุกความหมาย** (ไม่ใช่แม้แต่ non-additive measure) — มันคือ **attribute เชิงบรรยาย** ที่บอกสถานะ ไม่ใช่ตัวเลขที่วัด → เก็บเป็นคอลัมน์ธรรมดาในตาราง fact ได้ (ค่าจำกัดไม่กี่ค่า ไม่มี attribute ประกอบเพิ่มเติมพอที่จะทำเป็น dimension table แยก) นี่คือเหตุผลเดียวกับที่ [[06 Multi-Dimensional Design#6.5 Degenerate Dimension ⭐⭐ (guideline ข้อ 4.6)]] อธิบายไว้เรื่อง operational control numbers ที่ไม่คุ้มจะทำตารางแยก

---

## Step 5 — Keys: Surrogate, Natural, Degenerate ⭐⭐

### Surrogate Keys — ตามกฎเหล็กจาก [[06 Multi-Dimensional Design#6.4 Keys: Primary · Surrogate · Foreign ⭐⭐ (guideline ข้อ 5.4)]]

ทุก `XxxKey` ในภาพด้านล่างเป็น **surrogate key** (`INT AUTO_INCREMENT`) — ไม่ใช่รหัสจากระบบต้นทางโดยตรง

> [!important] ⭐ ใช้ประโยชน์ข้อ 3 ของ Surrogate Key: **"รองรับกรณีที่ไม่มีรหัสจากระบบ"**
> `Dim_Promo` มีแถวพิเศษ **`PromoKey = -1` แทน "No Promotion"** — ตรงกับที่บทที่ 6 สอนไว้ว่า surrogate key ใช้แทนกรณี **"Date to be Determined"** หรือ **"Not Applicable"** ได้
>
> **ทำไมสำคัญ:** ถ้าปล่อยให้ `PromoKey` เป็น `NULL` ตรง ๆ ในออเดอร์ที่ไม่ใช้โค้ดส่วนลด จะทำให้ `INNER JOIN` กับ `Dim_Promo` **หายไปทั้งแถว** (เพราะ NULL join ไม่ match) — Q4 ("ลูกค้าคนไหนใช้ส่วนลดคุ้มสุด") ก็จะนับยอดขายของลูกค้าที่ไม่ใช้โค้ดขาดหายไปด้วย ซึ่งผิด! การมีแถว "No Promo" แก้ปัญหานี้ตรง ๆ

### Degenerate Dimension: `OrderNumber` ⭐

> [!important] ทบทวนนิยามจาก [[06 Multi-Dimensional Design#6.5 Degenerate Dimension ⭐⭐ (guideline ข้อ 4.6)]]
> **"dimension keys without corresponding dimension tables"**

`OrderNumber` (เลขที่ออเดอร์ที่ลูกค้าเห็นในแอป เช่น `FG-20260818-00432`) ถูกเก็บไว้ **ในทั้ง 2 fact table** โดยไม่มี `Dim_Order` แยก เพราะไม่มี attribute อื่นให้บรรยายเพิ่ม (ทำตารางแยกจะได้ตารางที่มีคอลัมน์เดียวและแถวเท่ากับ fact table พอดี — ไร้ประโยชน์)

> [!tip] ⭐ ประโยชน์ที่เพิ่มขึ้นมาจากการมี 2 fact tables: **Drill-Across**
> เพราะ `OrderNumber` เดียวกันปรากฏใน **ทั้ง Fact_Order_Transaction และ Fact_Order_Lifecycle** เราสามารถ **เชื่อมสองมุมมองเข้าด้วยกัน** ได้ เช่น "ออเดอร์ที่ยกเลิก (จาก Fact 2) สูญเสียรายได้เท่าไหร่ (จาก Fact 1)":
> ```sql
> SELECT SUM(t.FoodAmount + t.DeliveryFee) AS lost_revenue
> FROM   Fact_Order_Transaction t
> JOIN   Fact_Order_Lifecycle   l ON t.OrderNumber = l.OrderNumber
> WHERE  l.FinalStatus LIKE 'Cancelled%';
> ```
> เทคนิคนี้เรียกว่า **drill-across** — การ join ข้าม fact table สองตัวผ่าน dimension (หรือในกรณีนี้คือ degenerate dimension) ที่ใช้ร่วมกัน

---

## 📐 ผลลัพธ์สุดท้าย

![[star_design_foodgo_schema.png]]

> [!important] อ่านภาพนี้อย่างไร
> - **เส้นเขียว** (จาก Dim_Date) — 1 เส้นไป Fact_Order_Transaction, **4 เส้นไป Fact_Order_Lifecycle** = role-playing dimension
> - **เส้นเทา** (จาก Dim_Restaurant, Dim_Rider) — เชื่อม **ทั้ง 2 fact table** = conformed dimension
> - **เส้นน้ำเงิน** (จาก Dim_Customer, Dim_Promo) — เชื่อมแค่ **Fact_Order_Transaction** = dimension เฉพาะ process
> - **แถวสีเหลือง `OrderNumber`** ในทั้ง 2 fact table = degenerate dimension ที่ใช้ทำ drill-across

---

## 🔧 แปลงเป็น SQL DDL (เชื่อมกับ [[07 ETL]])

```sql
-- ══════ Dimension Tables ══════
CREATE TABLE Dim_Date (
  DateKey    INT AUTO_INCREMENT NOT NULL,
  FullDate   DATE NOT NULL,
  Day        INT NOT NULL, Month INT NOT NULL,
  Quarter    INT NOT NULL, Year  INT NOT NULL,
  DayOfWeek  INT NOT NULL, IsWeekend BOOLEAN NOT NULL,
  PRIMARY KEY (DateKey)
);

CREATE TABLE Dim_Customer (
  CustomerKey  INT AUTO_INCREMENT NOT NULL,
  CustomerID   INT NOT NULL,          -- natural key
  CustomerName VARCHAR(100) NOT NULL,
  JoinDate     DATE NOT NULL,
  City         VARCHAR(50) NOT NULL,
  PRIMARY KEY (CustomerKey)
);

CREATE TABLE Dim_Promo (
  PromoKey       INT NOT NULL,        -- ไม่ auto-increment เพราะต้องกำหนด -1 เอง
  PromoCode      VARCHAR(20),
  PromoName      VARCHAR(100),
  DiscountType   VARCHAR(20),
  DiscountValue  DECIMAL(10,2),
  PRIMARY KEY (PromoKey)
);
INSERT INTO Dim_Promo VALUES (-1, NULL, 'No Promotion', NULL, 0);   -- ⭐ แถวพิเศษ

-- Dim_Restaurant, Dim_Rider โครงสร้างคล้ายกัน (ละไว้)

-- ══════ Fact 1: Transaction (grain = 1 order) ══════
CREATE TABLE Fact_Order_Transaction (
  OrderDateKey    INT NOT NULL,
  CustomerKey     INT NOT NULL,
  RestaurantKey   INT NOT NULL,
  RiderKey        INT NOT NULL,
  PromoKey        INT NOT NULL,       -- -1 แทน "ไม่มีโปร" แทนที่จะเป็น NULL
  OrderNumber     VARCHAR(20) NOT NULL,   -- degenerate dimension
  FoodAmount      DECIMAL(10,2) NOT NULL,
  DeliveryFee     DECIMAL(10,2) NOT NULL,
  DiscountAmount  DECIMAL(10,2) NOT NULL,
  ItemCount       INT NOT NULL,
  PRIMARY KEY (OrderNumber),
  FOREIGN KEY (OrderDateKey)  REFERENCES Dim_Date(DateKey),
  FOREIGN KEY (CustomerKey)   REFERENCES Dim_Customer(CustomerKey),
  FOREIGN KEY (RestaurantKey) REFERENCES Dim_Restaurant(RestaurantKey),
  FOREIGN KEY (RiderKey)      REFERENCES Dim_Rider(RiderKey),
  FOREIGN KEY (PromoKey)      REFERENCES Dim_Promo(PromoKey)
);

-- ══════ Fact 2: Accumulating Snapshot (grain = 1 order, UPDATE ซ้ำ) ══════
CREATE TABLE Fact_Order_Lifecycle (
  OrderNumber          VARCHAR(20) NOT NULL,   -- degenerate dimension (ตัวเชื่อม drill-across)
  OrderPlacedDateKey   INT NOT NULL,
  AcceptedDateKey      INT NULL,       -- ⭐ NULL ได้ตอนยังไม่ผ่านขั้นนี้
  PickedUpDateKey      INT NULL,
  CompletedDateKey     INT NULL,
  RestaurantKey        INT NOT NULL,
  RiderKey             INT NOT NULL,
  FinalStatus          VARCHAR(30) NOT NULL DEFAULT 'In_Progress',
  MinutesToAccept      INT NULL,
  MinutesToPickup      INT NULL,
  MinutesToDeliver     INT NULL,
  TotalLifecycleMinutes INT NULL,
  PRIMARY KEY (OrderNumber),
  FOREIGN KEY (OrderPlacedDateKey) REFERENCES Dim_Date(DateKey),
  FOREIGN KEY (RestaurantKey)      REFERENCES Dim_Restaurant(RestaurantKey),
  FOREIGN KEY (RiderKey)           REFERENCES Dim_Rider(RiderKey)
);

-- ตอน order วิ่งผ่านแต่ละขั้น ระบบจะ UPDATE แถวเดิม (ตามนิยาม Accumulating Snapshot):
UPDATE Fact_Order_Lifecycle
SET    AcceptedDateKey = 20567, MinutesToAccept = 3
WHERE  OrderNumber = 'FG-20260818-00432';
```

---

## 📊 ตอบคำถามต้นเรื่องด้วย SQL (เชื่อมกับ [[08 Reporting from Star Schema]])

> [!example] Q1 — รายได้แต่ละร้านในแต่ละเดือน
> ```sql
> SELECT   r.RestaurantName, d.Year, d.Month,
>          SUM(t.FoodAmount + t.DeliveryFee - t.DiscountAmount) AS NetRevenue
> FROM     Fact_Order_Transaction t
> JOIN     Dim_Restaurant r ON t.RestaurantKey = r.RestaurantKey
> JOIN     Dim_Date       d ON t.OrderDateKey  = d.DateKey
> GROUP BY r.RestaurantName, d.Year, d.Month
> ORDER BY d.Year, d.Month, NetRevenue DESC;
> ```

> [!example] Q2 — ไรเดอร์คนไหนช้า และช้าตรงขั้นไหน (ใช้ Fact 2 — สังเกตว่าไม่ join Date เลยเพราะไม่ต้องใช้บทบาทไหนในคำถามนี้)
> ```sql
> SELECT   rd.RiderName,
>          AVG(l.MinutesToAccept)  AS avg_wait_for_restaurant,
>          AVG(l.MinutesToPickup)  AS avg_wait_for_rider,
>          AVG(l.MinutesToDeliver) AS avg_delivery_time
> FROM     Fact_Order_Lifecycle l
> JOIN     Dim_Rider rd ON l.RiderKey = rd.RiderKey
> WHERE    l.FinalStatus = 'Delivered'
> GROUP BY rd.RiderName
> ORDER BY avg_delivery_time DESC;
> ```
> ⭐ สังเกต: ใช้ **`AVG`** ไม่ใช่ `SUM` — ตามที่อธิบายไว้ใน Step 4 ว่า additive ≠ ควรใช้ SUM เสมอ

> [!example] Q3 — ยกเลิกบ่อยตรงขั้นไหน (Drill-down บน dimension attribute `FinalStatus`)
> ```sql
> SELECT   FinalStatus, COUNT(*) AS cnt
> FROM     Fact_Order_Lifecycle
> WHERE    FinalStatus LIKE 'Cancelled%'
> GROUP BY FinalStatus
> ORDER BY cnt DESC;
> ```

> [!example] Q4 — ลูกค้าที่ใช้ส่วนลดคุ้มที่สุด (join Dim_Promo รวมแถว "No Promo" ด้วย)
> ```sql
> SELECT   c.CustomerName,
>          COUNT(*)               AS order_count,
>          SUM(t.DiscountAmount)  AS total_saved
> FROM     Fact_Order_Transaction t
> JOIN     Dim_Customer c ON t.CustomerKey = c.CustomerKey
> WHERE    t.PromoKey != -1        -- ตัด "No Promo" ออก
> GROUP BY c.CustomerName
> ORDER BY total_saved DESC;
> ```

---

# ส่วนที่ 2 — โจทย์ให้ลองทำเอง: เคสโรงพยาบาลจาก [[05 Data Warehouse Concepts]]

> [!info] ทำไมเป็นเคสนี้
> [[05 Data Warehouse Concepts#5.1 ทำไมต้องมี Data Warehouse — เคสโรงพยาบาล|บทที่ 5]] เปิดเรื่องด้วยเคสโรงพยาบาลที่ขยายจาก Excel ไฟล์เดียวเป็น 7 ระบบแยกกัน พร้อมคำถามจาก CEO **แต่ยังไม่เคยแก้จริงในวิชานี้เลย** — นี่คือโอกาสปิดปมนั้นด้วยมือคุณเอง

## 🎬 โจทย์

> [!quote] คำถามจาก CEO (จากบทที่ 5)
> 1. **Revenue by insurance company** (เทียบรายได้ระหว่างบริษัทประกัน)
> 2. **Waiting time by branch** (เทียบเวลารอของแต่ละสาขา)
> 3. **Doctor performance trend** (แนวโน้มผลงานของแพทย์)
> 4. **Patient satisfaction over five years** (ความพึงพอใจผู้ป่วยย้อนหลัง 5 ปี — KPI dashboard)

**ข้อมูลเพิ่มเติม (สมมติให้สมจริงขึ้น):** โรงพยาบาลมี 6 สาขา · การมาแต่ละครั้งของผู้ป่วยเรียกว่า **"visit"** โดย 1 visit มี **เวลาลงทะเบียน, เวลาเริ่มพบแพทย์, เวลาจบการตรวจ, เวลาชำระเงิน** เป็น 4 timestamp คนละเวลากัน · ทุก visit มี **แพทย์ 1 คน สาขา 1 แห่ง ผู้ป่วย 1 คน** และ**อาจมี**บริษัทประกันเป็นผู้จ่าย (หรือจ่ายเอง) · หลัง visit จบ ผู้ป่วย**อาจ**ให้คะแนนความพึงพอใจ 1–5 ดาว (ไม่บังคับ ทำให้บางแถวไม่มีคะแนน)

**ลองทำเองก่อนตามลำดับ 5 ขั้นแบบเดียวกับ FoodGo ด้านบน แล้วค่อยกดดูเฉลยทีละขั้น**

---

## ✏️ Step 1 — Select the Business Process

> [!question]- 💭 ลองคิดเอง: มีกี่ business process? อะไรบ้าง?
> ลองแยกคำถามทั้ง 4 ข้อออกเป็นกลุ่มตามธรรมชาติของมันดูก่อน เหมือนที่ทำกับ FoodGo (กลุ่ม "เงิน" vs กลุ่ม "เวลา/กระบวนการ")

> [!success]- ✅ เฉลย Step 1
> แยกคำถามได้ 2 กลุ่ม:
> | คำถาม | กลุ่ม |
> |---|---|
> | Q1 Revenue by insurance | **การเงิน** |
> | Q2 Waiting time by branch | **เวลา/กระบวนการ** |
> | Q3 Doctor performance trend | **เวลา/กระบวนการ** (แนวโน้มมักวัดจากเวลาตรวจ/จำนวนเคสต่อวัน) |
> | Q4 Patient satisfaction | **คุณภาพบริการ** — เป็นกลุ่มที่ 3 แยกต่างหาก! เพราะคะแนนดาวไม่ใช่เงินและไม่ใช่ duration |
>
> **✅ เลือก 2 business process** (ไม่ใช่ 3 — เหตุผลอยู่ด้านล่าง):
> 1. **"Patient Visit"** — ครอบคลุมทั้งเวลา (Q2, Q3) **และ** คะแนนความพึงพอใจ (Q4) เพราะทั้งสองเกิดขึ้น**ในบริบทเดียวกัน** คือ 1 การมาพบแพทย์ 1 ครั้ง — ไม่จำเป็นต้องแยกเป็น process ที่ 3 เพราะ **satisfaction score เป็นแค่ measure เพิ่มเติมของ visit เดียวกัน** ไม่ได้มี dimension หรือจังหวะการเก็บข้อมูลต่างไปจาก Q2/Q3 เลย
> 2. **"Billing"** — การเงิน (Q1)
>
> ⭐ **จุดที่ต่างจาก FoodGo:** FoodGo แยกเป็น 2 fact เพราะ **จังหวะการเขียนข้อมูลต่างกัน** (insert ครั้งเดียว vs update หลายครั้ง) ส่วนเคสนี้แยกเพราะ **มิติของข้อมูล (dimensional context) ต่างกัน** — การเงินโรงพยาบาลมักมีรายละเอียดที่ visit fact ไม่จำเป็นต้องรู้ (เช่น การผ่อนชำระ, การเคลมประกันหลายรอบ) ตรงกับเหตุผล **"Non-Shared Dimensions"** ใน [[06 Multi-Dimensional Design#6.8 Multiple Fact Tables — เมื่อไหร่ต้องมีมากกว่า 1 ⭐]]

---

## ✏️ Step 2 — Declare the Grain

> [!question]- 💭 ลองคิดเอง: แต่ละ fact table 1 แถวคืออะไร?
> ระวังกับดักเดียวกับ FoodGo — อย่าเลือก grain ที่หยาบเกินไปจนตอบคำถามละเอียดไม่ได้ ลองนึกดูว่า Q3 ("Doctor performance **trend**") ต้องการข้อมูลระดับไหนถึงจะดูแนวโน้มได้

> [!success]- ✅ เฉลย Step 2
> **Fact_Patient_Visit:** **"1 แถว = 1 visit (การมาพบแพทย์ 1 ครั้งของผู้ป่วย 1 คน)"**
> — grain ระดับนี้ทำให้ Q2 (waiting time by branch) และ Q3 (doctor trend) ทำได้ทั้งคู่ด้วยการ `GROUP BY` แล้ว roll-up ขึ้นไปเป็นรายเดือน/รายไตรมาสภายหลัง
>
> **Fact_Billing:** **"1 แถว = 1 รายการเรียกเก็บเงิน (1 billing line item) ของ 1 visit"**
> — สังเกตว่า **ไม่ใช่ "1 แถว = 1 visit"** เพราะ 1 visit อาจมีหลายรายการค่าใช้จ่าย (ค่าตรวจ, ค่ายา, ค่าห้องแล็บ) แต่ละรายการอาจถูกจ่ายโดยประกันคนละสัดส่วนกัน — ถ้าใช้ grain "1 visit" หยาบเกินไป จะตอบไม่ได้ว่า "รายได้จากประกันบริษัท X มาจากค่าใช้จ่ายประเภทไหนบ้าง"
>
> ⚠️ **ข้อผิดพลาดที่พบบ่อยในขั้นนี้:** เลือก grain ของ Fact_Billing เป็น "1 แถว = 1 visit" (เอาไปปนกับ grain ของ Fact_Patient_Visit) — ทำให้เสียรายละเอียดระดับรายการค่าใช้จ่าย ซึ่ง Q1 ("revenue by insurance company") ต้องการความละเอียดระดับนี้เพื่อกระทบยอด (reconcile) กับใบแจ้งหนี้จริงของบริษัทประกันได้

---

## ✏️ Step 3 — Choose the Dimensions

> [!question]- 💭 ลองคิดเอง: แต่ละ Fact ต้องมี dimension อะไรบ้าง และมี Role-Playing Dimension ไหม?
> ใช้กรอบ 5W เหมือนเดิม แล้วสังเกตให้ดีว่าโจทย์บอกว่า visit หนึ่งมี **4 timestamp**

> [!success]- ✅ เฉลย Step 3
> | Dimension | ใช้ใน Fact ไหน | หมายเหตุ |
> |---|---|---|
> | **Dim_Date** | ทั้งคู่ | **Role-Playing** ใน Fact_Patient_Visit (ดูด้านล่าง) |
> | **Dim_Patient** | ทั้งคู่ | **Conformed dimension** |
> | **Dim_Branch** | ทั้งคู่ | **Conformed dimension** — Q2 ต้อง group ตามสาขา |
> | **Dim_Doctor** | Fact_Patient_Visit เท่านั้น | Q3 ต้อง group ตามแพทย์ — billing ไม่จำเป็นต้องรู้ว่าใครตรวจ |
> | **Dim_InsuranceCompany** | Fact_Billing เท่านั้น | Q1 ต้อง group ตามบริษัทประกัน — visit fact ไม่ต้องรู้เรื่องเงิน |
> | **Dim_ChargeType** | Fact_Billing เท่านั้น | บอกว่าเป็นค่าตรวจ/ค่ายา/ค่าห้องแล็บ |
>
> **⭐ Dim_Date เป็น Role-Playing ใน Fact_Patient_Visit — 4 บทบาท:**
> ```
> Fact_Patient_Visit
> ├── CheckInDateKey    (FK) → Dim_Date   role 1: ลงทะเบียน
> ├── ConsultStartDateKey (FK) → Dim_Date role 2: เริ่มพบแพทย์
> ├── ConsultEndDateKey (FK) → Dim_Date   role 3: จบการตรวจ
> └── PaymentDateKey    (FK) → Dim_Date   role 4: ชำระเงิน
> ```
> เหมือน FoodGo เป๊ะ — ต่างกันแค่ชื่อ role (Placed/Accepted/PickedUp/Completed → CheckIn/ConsultStart/ConsultEnd/Payment) โครงสร้างแนวคิดเดียวกันทุกประการ
>
> ⚠️ **ถ้าคุณตอบว่ามี Dim_Date แค่ตัวเดียวไม่มี role-playing** — กลับไปดูว่าโจทย์บอกไว้ว่า visit มี **4 timestamp คนละเวลากัน** ถ้าใช้ FK เดียว จะเก็บได้แค่เวลาเดียว แล้ว **waiting time = ConsultStart − CheckIn จะคำนวณไม่ได้เลย** เพราะไม่มีทั้งสองค่าให้ลบกัน

---

## ✏️ Step 4 — Identify the Facts (Measures)

> [!question]- 💭 ลองคิดเอง: measure อะไรบ้าง และแต่ละตัวเป็น Additive/Semi-additive/Non-additive?
> คิดถึง **Waiting Time** ให้ดี ๆ — มันคำนวณมาจากการลบกันของ 2 timestamp ไม่ใช่ค่าที่มีอยู่ตรง ๆ

> [!success]- ✅ เฉลย Step 4
> **Fact_Patient_Visit:**
> | Measure | Additivity | เหตุผล |
> |---|---|---|
> | `WaitingMinutes` (= ConsultStart − CheckIn) | **Additive** (แต่รายงานด้วย AVG) | เหมือน `MinutesToAccept` ของ FoodGo เป๊ะ — บวกข้ามสาขา/วันได้ แต่ธุรกิจอยากดู **AVG ต่อสาขา** มากกว่า SUM |
> | `ConsultMinutes` (= ConsultEnd − ConsultStart) | **Additive** | เหมือนกัน |
> | `SatisfactionScore` (1–5 ดาว) | **Non-additive** ⭐ | บวกดาวข้ามผู้ป่วยไม่มีความหมาย ("ผู้ป่วย 3 คนรวมกันได้ 12 ดาว" ตีความไม่ได้) — ต้องรายงานด้วย **AVG** เท่านั้น และเพราะบางแถวไม่มีคะแนน (optional) ต้องนับ `ResponseCount` แยกไว้เป็นอีก measure เพื่อคำนวณ AVG ที่ถูกต้อง (ไม่ปนแถวที่ไม่ตอบเข้าไปในตัวหาร) |
>
> **Fact_Billing:**
> | Measure | Additivity | เหตุผล |
> |---|---|---|
> | `ChargeAmount` | **Additive** | ยอดเรียกเก็บ รวมได้ทุกทาง |
> | `InsuranceCoveredAmount` | **Additive** | ส่วนที่ประกันจ่าย รวมได้ |
> | `PatientPaidAmount` | **Additive** | ส่วนที่ผู้ป่วยจ่ายเอง รวมได้ (และ `ChargeAmount = InsuranceCoveredAmount + PatientPaidAmount` เป็น business rule ที่ตรวจสอบได้) |
>
> ⭐ **ทำไม `SatisfactionScore` non-additive แต่ `WaitingMinutes` เป็น additive ทั้งที่ทั้งคู่มักถูกรายงานด้วย AVG เหมือนกัน?**
> ตัวชี้ขาดคือ **"SUM ข้าม dimension มีความหมายทางธุรกิจไหม"** ไม่ใช่ "นิยมรายงานด้วยอะไร":
> - `WaitingMinutes` **SUM มีความหมาย** — ผลรวมนาทีที่คนไข้ทั้งหมดรอในสาขาหนึ่งวันหนึ่ง บอก "ภาระงานของสาขา" ได้จริง
> - `SatisfactionScore` **SUM ไม่มีความหมายเลยในทุกกรณี** — ไม่มีใครสนใจ "ผลรวมดาว" แม้แต่นิดเดียว มีแต่ค่าเฉลี่ยเท่านั้นที่สื่อความหมาย → นี่คือ **non-additive จริง ๆ** ไม่ใช่แค่ "additive แต่นิยมดู AVG" แบบ WaitingMinutes

---

## ✏️ Step 5 — Keys: Surrogate, Natural, Degenerate

> [!question]- 💭 ลองคิดเอง: มี degenerate dimension ไหม? มี edge case อะไรที่ surrogate key ช่วยแก้ได้?
> คิดถึงตอนที่โจทย์บอกว่า **"อาจมีบริษัทประกันเป็นผู้จ่าย (หรือจ่ายเอง)"**

> [!success]- ✅ เฉลย Step 5
> **Degenerate Dimension:** `VisitNumber` (เลขที่ visit ที่ใช้ตรวจสอบในระบบโรงพยาบาล) — เก็บในทั้ง 2 fact table เพื่อทำ **drill-across** เหมือน `OrderNumber` ของ FoodGo เป๊ะ (เช่น เชื่อม "visit ที่ waiting time นานผิดปกติ" กับ "รายได้จาก visit นั้น" เพื่อวิเคราะห์ว่าลูกค้ารอนานแล้วยกเลิกการรักษาไปเท่าไหร่)
>
> **Surrogate Key แก้ NULL:** `Dim_InsuranceCompany` ต้องมีแถวพิเศษ **`InsuranceKey = -1` แทน "Self-Pay / จ่ายเอง"** — เหตุผลเดียวกับ `PromoKey = -1` ของ FoodGo: ถ้าปล่อย NULL ตรง ๆ `INNER JOIN` จะทำให้ **visit ที่จ่ายเองหายไปทั้งหมดจาก Q1** (revenue by insurance company จะนับไม่ครบ เพราะรายได้จากคนไข้จ่ายเองไม่ถูกนับเป็น "บริษัทประกัน" ไหนเลย ทั้งที่มันคือรายได้จริงที่ควรอยู่ในรายงาน)
>
> ```sql
> CREATE TABLE Dim_InsuranceCompany (
>   InsuranceKey INT NOT NULL,
>   CompanyName  VARCHAR(100),
>   PRIMARY KEY (InsuranceKey)
> );
> INSERT INTO Dim_InsuranceCompany VALUES (-1, 'Self-Pay (จ่ายเอง)');
> ```

---

## 🏆 เฉลยฉบับเต็ม — โครงสร้างสุดท้าย

> [!success]- 📐 กดดูโครงสร้างเต็มทั้งหมด (เช็คคำตอบตัวเองที่นี่)
> ```
> Fact_Patient_Visit                       Fact_Billing
> ├── VisitNumber (degenerate)             ├── VisitNumber (degenerate) ← drill-across
> ├── CheckInDateKey (FK, role 1)          ├── ChargeDateKey (FK)
> ├── ConsultStartDateKey (FK, role 2)     ├── PatientKey (FK, conformed)
> ├── ConsultEndDateKey (FK, role 3)       ├── BranchKey (FK, conformed)
> ├── PaymentDateKey (FK, role 4)          ├── InsuranceKey (FK, -1 = self-pay)
> ├── PatientKey (FK, conformed)           ├── ChargeTypeKey (FK)
> ├── BranchKey (FK, conformed)            ├── ── measures ──
> ├── DoctorKey (FK)                       ├── ChargeAmount (Additive)
> ├── ── measures ──                       ├── InsuranceCoveredAmount (Additive)
> ├── WaitingMinutes (Additive, รายงาน AVG)└── PatientPaidAmount (Additive)
> ├── ConsultMinutes (Additive)
> ├── SatisfactionScore (Non-additive)
> └── ResponseCount (Additive — ใช้เป็นตัวหารคำนวณ AVG ที่ถูกต้อง)
> ```
>
> **Dimension ทั้งหมด:** Dim_Date (role-playing ×4 ใน Visit) · Dim_Patient (conformed) · Dim_Branch (conformed) · Dim_Doctor (เฉพาะ Visit) · Dim_InsuranceCompany (เฉพาะ Billing, มีแถว -1) · Dim_ChargeType (เฉพาะ Billing)
>
> **ลองตรวจตัวเอง:** ถ้าโครงสร้างที่คุณทำได้ตรงกับนี้เกิน 80% (โดยเฉพาะ 2 fact tables + role-playing Dim_Date + surrogate key แก้ NULL) ถือว่าเข้าใจแก่นของบทที่ 6 แล้ว 🎉

---

## ✅ Self-Check — ทบทวนหลักการที่ใช้ในทั้ง 2 เคส

> [!question]- ทั้ง FoodGo และโรงพยาบาล มีอะไรที่ "โครงสร้างเหมือนกันเป๊ะ" บ้าง สรุปเป็น pattern ที่เอาไปใช้ซ้ำได้
> 1. **แยก 2 fact tables** เมื่อคำถามธุรกิจแบ่งเป็น "กลุ่มเงิน" กับ "กลุ่มเวลา/กระบวนการ" อย่างชัดเจน
> 2. **กระบวนการที่มีหลายขั้นตอน (เช่น สั่ง→รับ→ส่ง หรือ ลงทะเบียน→ตรวจ→จ่ายเงิน) → ต้องมี Date dimension แบบ role-playing** เพราะแต่ละขั้นเกิดคนละเวลา
> 3. **Duration ที่คำนวณจากผลต่างของ 2 timestamp (waiting time, minutes to accept) → additive ในทางเทคนิค แต่รายงานด้วย AVG ในทางปฏิบัติ**
> 4. **คะแนนแบบให้เรตติ้ง (satisfaction, rating) → non-additive แท้ ๆ ต้องเก็บ sum+count แยกเพื่อคำนวณ AVG ให้ถูก**
> 5. **Dimension ที่มี "ทางเลือกไม่มีก็ได้" (ไม่ใช้โปร / จ่ายเอง) → ต้องมี surrogate key พิเศษ (เช่น -1) แทน NULL เพื่อไม่ให้ INNER JOIN ทำข้อมูลหาย**
> 6. **เลขอ้างอิงที่ผู้ใช้เห็น (order number, visit number) ที่ปรากฏในหลาย fact table → degenerate dimension ที่ใช้ทำ drill-across ได้**

---

**กลับหน้าหลัก →** [[00 START HERE]] · **ทบทวนหลักการ →** [[06 Multi-Dimensional Design]] · **ฝึกเพิ่ม →** [[12 Exam Drills]]
