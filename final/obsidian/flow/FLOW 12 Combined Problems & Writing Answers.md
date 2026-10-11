---
title: FLOW 12 · โจทย์หลายส่วน + วิธีเขียนคำตอบ + checklist ก่อนส่ง
tags: [final, flow, exam-strategy, writing]
---

# FLOW 12 · โจทย์หลายส่วน + วิธีเขียนคำตอบ
> กลับ [[FLOW 00 START HERE]]

## 1 · โจทย์ผสมที่พบบ่อย → ต่อ flow ยังไง

| โจทย์ | ต่อ flow | ทำไมเรียงแบบนี้ |
|---|---|---|
| "รวมไฟล์แล้วสร้างโมเดลทำนาย" | [[FLOW 01 Data Handling]] (append → join) → บันทึกไฟล์ → [[FLOW 09 Classification Workflow]] | โมเดลต้องเห็นข้อมูลครบทุกแถว/คอลัมน์ก่อน |
| "preprocess แล้วเทียบก่อน/หลัง" | [[FLOW 02 Preprocessing & Leakage]] §8 | ต้องคุมโมเดลและ folds ให้เหมือนกัน ต่างแค่ preprocessing |
| "ข้อมูลไม่สมดุล หาโมเดลที่ดีสุด" | [[FLOW 04 Imbalanced Classification]] (เลือกวิธี resample) → [[FLOW 09 Classification Workflow]] (SMOTE ใน pipeline, metric F1/recall) | เลือก metric ก่อนเทียบโมเดล |
| "PCA แล้วทำโมเดล / cluster" | [[FLOW 03 PCA]] → (scaler + PCA ใน pipeline) หรือ [[FLOW 10 Clustering]] บน PC | PCA ต้องอยู่หลัง scale และใน pipeline |
| "cluster แล้วหากฎ" | [[FLOW 10 Clustering]] → คอลัมน์ cluster → [[FLOW 11 Association Rules]] (cluster=… เป็น item) | หากฎที่อธิบายแต่ละกลุ่ม |
| "regression หลายโมเดล" | [[FLOW 06 Linear Regression]] + KNN/Tree regression (T06 §6) | baseline = ค่าเฉลี่ย · metric RMSE/R² |

## 2 · แบ่งเวลา 3 ชั่วโมง
| ช่วง | ทำ |
|---|---|
| 10 นาทีแรก | อ่านทุกข้อ · จับคู่แต่ละข้อกับ FLOW/template · ข้อไหนเครื่องมือไหน (Python/RapidMiner) |
| ระหว่างทำ | ทำข้อที่ได้คะแนนแน่นอนก่อน · แต่ละข้อ: CONFIG → รัน → ตรวจ §1 → § ที่ถาม → เขียนคำตอบทันที |
| 20 นาทีสุดท้าย | Restart & Run All / Run process ทุกไฟล์อีกรอบ · เติมคำตอบที่ขาด · ตรวจชื่อไฟล์ส่ง |

> [!tip] เขียนคำตอบทันทีหลังรันแต่ละ § — อย่ารอทำโค้ดครบแล้วค่อยเขียน (หมดเวลาแล้วมีแต่โค้ดไม่มีคำตอบ = คะแนนหาย)

## 3 · โครงคำตอบ 4 ขั้น (ใช้ได้ทุกข้อ)
1. **Process** — ทำอะไรตามลำดับ (อ่าน → ตัด … → preprocessing … → แบ่งข้อมูล … → โมเดล … → ประเมิน …)
2. **Settings + เหตุผล** — seed, k, depth, folds, threshold, min support, metric · **ทุกการตั้งค่าต้องมี "เพราะ"**
3. **Results** — ตัวเลขจากตาราง (metric + ค่า + เทียบ baseline/ก่อน-หลัง)
4. **Interpretation** — แปลว่าอะไรในบริบทของโจทย์ · ทำไมได้ผลแบบนี้ · ข้อจำกัด · ข้อเสนอ

### ประโยคเหตุผลที่ใช้บ่อย (copy ได้)
| ตัดสินใจ | เหตุผล |
|---|---|
| ตัด id | ไม่ซ้ำกันทุกแถว ไม่มีความหมายเชิงทำนาย ถ้าใช้จะทำให้โมเดลจำแถว |
| เติม median | ตัวแปรเบ้ขวา/มี outlier median ไม่ถูกค่าสุดขั้วดึง |
| one-hot | หมวดหมู่ไม่มีลำดับ ถ้าใช้ตัวเลข 1,2,3 โมเดลจะตีความว่ามีลำดับ |
| standardize | โมเดลใช้ระยะทาง ตัวแปรหน่วยใหญ่จะครอบงำ |
| ไม่ scale สำหรับ tree | tree แบ่งด้วย threshold ทีละตัวแปร ไม่ใช้ระยะทาง |
| stratified | รักษาสัดส่วนคลาสใน train/test/fold |
| fit บน train | กัน data leakage ค่าทางสถิติของ test ต้องไม่ถูกใช้ตอนเรียน |
| CV แทน hold-out | ข้อมูลน้อย ผล hold-out ขึ้นกับการสุ่มครั้งเดียว CV เสถียรกว่า |
| F1 แทน accuracy | คลาสไม่สมดุล baseline ได้ accuracy สูงแต่หาคลาสที่สนใจไม่เจอ |
| recall | การพลาดกรณีจริง (FN) มีต้นทุนสูงกว่าการเตือนผิด |
| tune ด้วย CV | เลือก parameter โดยไม่แตะ test เพื่อให้ผล test เป็นกลาง |
| จำกัด max_depth | ต้นไม้เต็ม overfit (train … vs CV …) |
| lift | confidence สูงอาจเพราะ consequent ขายดีอยู่แล้ว lift ตัดผลนั้นออก |
| เลือก k (cluster) | silhouette/elbow + ขนาดกลุ่มสมดุล + ตีความได้ |

## 4 · Checklist ก่อนส่ง
- [ ] ทุกข้อมี **ตัวเลข + เหตุผล + ตีความ** ไม่ใช่แค่โค้ด/ภาพ
- [ ] มี **baseline** และเทียบกับมัน (ข้อที่สร้างโมเดล)
- [ ] metric เหมาะกับโจทย์ (ไม่สมดุล → ไม่ใช้ accuracy อย่างเดียว)
- [ ] preprocessing fit บน train / อยู่ใน pipeline / Training pane
- [ ] seed / folds / ค่าที่โจทย์กำหนดถูกต้อง
- [ ] Python: **Restart & Run All** ไม่มี error · RapidMiner: Run แล้วได้ Results ครบ
- [ ] ลบส่วนที่ไม่ใช้ · ตั้งชื่อไฟล์ตามที่โจทย์กำหนด
- [ ] ภาพ/ตารางที่อ้างในคำตอบมีอยู่จริงในไฟล์ส่ง
