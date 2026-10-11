"""เตรียมข้อมูลของโจทย์ฝึก 9 ชุด (final/practice/data/) — reproducible, seed คงที่

แหล่งข้อมูล (ดาวน์โหลด 2026-10-10 เก็บไว้ใน data/raw/):
  tips.csv, penguins.csv  ← github.com/mwaskom/seaborn-data
  groceries.csv, insurance.csv ← github.com/stedy/Machine-Learning-with-R-datasets
  pima-indians-diabetes.data.csv ← github.com/jbrownlee/Datasets
  dataset.csv (heart disease, UCI Cleveland) ← github.com/kb22/Heart-Disease-Prediction
  wine, breast cancer ← มากับ scikit-learn (UCI)

รัน:  final/.venv/bin/python -I final/practice/make_practice_data.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.datasets import load_wine, load_breast_cancer

HERE = Path(__file__).resolve().parent
RAW, OUT = HERE / "data" / "raw", HERE / "data"
SEED = 1992


def save(name, df):
    df.to_csv(OUT / name, index=False)
    print(f"  ✓ {name:<34} {df.shape}")


# P1 · Data Handling — ร้านอาหาร: บิล 2 สัปดาห์แยกไฟล์ + ตารางข้อมูลวัน (ต้อง Append แล้ว Join)
tips = pd.read_csv(RAW / "tips.csv")
tips.insert(0, "bill_id", range(1, len(tips) + 1))
order = np.random.default_rng(SEED).permutation(len(tips))
week1, week2 = tips.iloc[np.sort(order[:130])], tips.iloc[np.sort(order[130:])]
save("p1_bills_week1.csv", week1)
save("p1_bills_week2.csv", week2)
save("p1_day_info.csv", pd.DataFrame({"day": ["Thur", "Fri", "Sat", "Sun"],
                                       "is_weekend": ["No", "No", "Yes", "Yes"],
                                       "open_hours": [10, 12, 14, 12]}))

# P2 · Preprocessing + PCA — penguins (มีค่าว่าง, categorical, หน่วยต่างกัน)
save("p2_penguins.csv", pd.read_csv(RAW / "penguins.csv"))

# P3 · Imbalanced — breast cancer: เก็บ benign ทั้งหมด + สุ่ม malignant 40 ราย → IR ≈ 8.9
bc = load_breast_cancer(as_frame=True)
cols = [c for c in bc.data.columns if c.startswith("mean ")]          # 10 feature กลุ่ม mean
df = bc.data[cols].copy()
df.columns = [c.replace("mean ", "").replace(" ", "_") for c in cols]
df["diagnosis"] = np.where(bc.target == 0, "malignant", "benign")
mal = df[df.diagnosis == "malignant"].sample(40, random_state=SEED)
imb = pd.concat([df[df.diagnosis == "benign"], mal]).sample(frac=1, random_state=SEED).reset_index(drop=True)
save("p3_breast_cancer_imbalanced.csv", imb)

# P4 · KNN — wine 3 สายพันธุ์องุ่น (หน่วยต่างกันมาก: proline หลักพัน)
w = load_wine(as_frame=True)
wine = w.data.copy()
wine.columns = [c.replace("/", "_") for c in wine.columns]
wine["cultivar"] = "cultivar_" + w.target.astype(str)
save("p4_wine.csv", wine)

# P5 · Logistic — Pima diabetes (ไม่มี header; 0 ใน glucose/BP/skin/insulin/BMI = ค่าว่างแฝง)
pima = pd.read_csv(RAW / "pima-indians-diabetes.data.csv", header=None,
                   names=["pregnancies", "glucose", "blood_pressure", "skin_thickness", "insulin",
                          "bmi", "pedigree", "age", "diabetes"])
save("p5_pima_diabetes.csv", pima)

# P6 · Tree vs RF — heart disease (target 1 = เป็นโรค)
heart = pd.read_csv(RAW / "dataset.csv", encoding="utf-8-sig")
save("p6_heart.csv", heart)

# P7 · Regression — ค่ารักษาพยาบาล (insurance)
save("p7_insurance.csv", pd.read_csv(RAW / "insurance.csv"))

# P8 · Clustering — wine แบบไม่บอก label (ใช้ไฟล์เดียวกับ P4 แต่ห้ามใช้ cultivar ตอนจัดกลุ่ม)
save("p8_wine_unlabeled.csv", wine)

# P9 · Association — groceries 9,835 ตะกร้า
lines = (RAW / "groceries.csv").read_text().strip().splitlines()
baskets = [sorted(set(x.strip() for x in ln.split(",") if x.strip())) for ln in lines]
items = sorted({i for b in baskets for i in b})
onehot = pd.DataFrame([[int(i in set(b)) for i in items] for b in baskets], columns=items)
onehot.insert(0, "basket_id", range(1, len(baskets) + 1))
save("p9_groceries_onehot.csv", onehot)                    # สำหรับ RapidMiner (0/1 ต่อสินค้า)
(OUT / "p9_groceries_baskets.csv").write_text("\n".join(",".join(b) for b in baskets) + "\n")
print(f"  ✓ p9_groceries_baskets.csv           ({len(baskets)} baskets, {len(items)} items)")
