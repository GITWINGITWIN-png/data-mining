"""สร้างไฟล์ข้อมูลของ mock lab ทั้ง 3 ชุด จาก dataset ที่มีในเครื่อง (reproducible — seed คงที่)

Mock 1 (classification + imbalanced): HW5/adult.csv → สุ่มแบบรักษาสัดส่วน 6,000 แถว
    แล้ว "แตก" เป็น 3 ไฟล์ให้ต้อง Append + Join เอง (ตาม guideline: join, concatenate)
Mock 2 (regression + PCA):            W8/boston_r.csv → กันบ้าน 3 หลังไว้เป็น "บ้านใหม่" ให้ทำนาย
Mock 3 (clustering + association):    final/data/utilities.csv + HW8/bank-data.csv

รัน:  final/.venv/bin/python final/mock_lab/make_data.py
"""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SEED = 1992


def out(folder, name, df):
    path = HERE / folder / "data" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"  ✓ {folder}/data/{name:<22} {df.shape}")


# ── Mock 1 ────────────────────────────────────────────────────────────────────
adult = pd.read_csv(ROOT / "HW5" / "adult.csv")
sample = (adult.groupby("income", group_keys=False)
               .sample(frac=6000 / len(adult), random_state=SEED)       # รักษาสัดส่วน <=50K : >50K
               .sample(frac=1, random_state=SEED)                       # สลับแถว
               .reset_index(drop=True))
sample.insert(0, "person_id", range(10001, 10001 + len(sample)))
new_person = sample.iloc[[0]].drop(columns="income")                    # ใช้ถามข้อ "ทำนายคนใหม่"
sample = sample.iloc[1:]

people_cols = ["person_id", "age", "gender", "race", "native-country", "education",
               "educational-num", "marital-status", "relationship"]
work_cols = ["person_id", "workclass", "occupation", "hours-per-week", "capital-gain",
             "capital-loss", "fnlwgt", "income"]
people = sample[people_cols].sample(frac=1, random_state=SEED + 1)     # ลำดับแถวต่างกัน → ต้อง join ด้วย key
work = sample[work_cols]
out("mock1_classification", "people.csv", people)
out("mock1_classification", "work_2025H1.csv", work.iloc[:3500])
out("mock1_classification", "work_2025H2.csv", work.iloc[3500:])
out("mock1_classification", "new_person.csv", new_person)

# ── Mock 2 ────────────────────────────────────────────────────────────────────
boston = pd.read_csv(ROOT / "W8" / "boston_r.csv")
new_houses = boston.sample(3, random_state=SEED)
out("mock2_regression_pca", "housing.csv", boston.drop(index=new_houses.index))
out("mock2_regression_pca", "new_houses.csv", new_houses.drop(columns="medv"))
out("mock2_regression_pca", "new_houses_answer.csv", new_houses[["medv"]])   # เฉลยราคาจริง (อย่าเปิดก่อนทำ)

# ── Mock 3 ────────────────────────────────────────────────────────────────────
out("mock3_cluster_assoc", "utilities.csv", pd.read_csv(ROOT / "final" / "data" / "utilities.csv"))
out("mock3_cluster_assoc", "bank-data.csv", pd.read_csv(ROOT / "HW8" / "bank-data.csv"))
