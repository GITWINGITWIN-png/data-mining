"""สร้างไฟล์ CSV จาก "ข้อมูลตัวอย่างในสไลด์ของอาจารย์" — ใช้ร่วมกันทั้งโน้ต Lab / Lecture / Mock

ทำไมต้องมีไฟล์นี้: ตัวเลขในสไลด์เป็นเฉลยอยู่แล้ว (เช่น Gain(Outlook)=0.246, accuracy ที่ cutoff 0.5 = 87.5%)
ถ้าเราใช้ข้อมูลชุดเดียวกันฝึก จะ "ตรวจคำตอบตัวเองกับสไลด์" ได้ทันที

รัน:  final/.venv/bin/python final/data/make_slide_datasets.py
"""
from pathlib import Path
import csv

HERE = Path(__file__).resolve().parent


def write(name, header, rows, source):
    path = HERE / name
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"  ✓ {name:<28} {len(rows):>3} rows   ← {source}")


# 69_1_basic_clustering.pdf p.10 (ซ้ำที่ p.51) — 22 Public Utilities
write("utilities.csv",
      ["Company", "Fixed_charge", "RoR", "Cost", "Load_factor", "Demand_growth",
       "Sales", "Nuclear", "Fuel_Cost"],
      [["Arizona", 1.06, 9.2, 151, 54.4, 1.6, 9077, 0, 0.628],
       ["Boston", 0.89, 10.3, 202, 57.9, 2.2, 5088, 25.3, 1.555],
       ["Central", 1.43, 15.4, 113, 53, 3.4, 9212, 0, 1.058],
       ["Commonwealth", 1.02, 11.2, 168, 56, 0.3, 6423, 34.3, 0.7],
       ["NY", 1.49, 8.8, 192, 51.2, 1, 3300, 15.6, 2.044],          # สไลด์ p.10 เขียน "Con Ed NY"
       ["Florida", 1.32, 13.5, 111, 60, -2.2, 11127, 22.5, 1.241],
       ["Hawaiian", 1.22, 12.2, 175, 67.6, 2.2, 7642, 0, 1.652],
       ["Idaho", 1.1, 9.2, 245, 57, 3.3, 13082, 0, 0.309],
       ["Kentucky", 1.34, 13, 168, 60.4, 7.2, 8406, 0, 0.862],
       ["Madison", 1.12, 12.4, 197, 53, 2.7, 6455, 39.2, 0.623],
       ["Nevada", 0.75, 7.5, 173, 51.5, 6.5, 17441, 0, 0.768],
       ["New England", 1.13, 10.9, 178, 62, 3.7, 6154, 0, 1.897],
       ["Northern", 1.15, 12.7, 199, 53.7, 6.4, 7179, 50.2, 0.527],
       ["Oklahoma", 1.09, 12, 96, 49.8, 1.4, 9673, 0, 0.588],
       ["Pacific", 0.96, 7.6, 164, 62.2, -0.1, 6468, 0.9, 1.4],
       ["Puget", 1.16, 9.9, 252, 56, 9.2, 15991, 0, 0.62],
       ["San Diego", 0.76, 6.4, 136, 61.9, 9, 5714, 8.3, 1.92],
       ["Southern", 1.05, 12.6, 150, 56.7, 2.7, 10140, 0, 1.108],
       ["Texas", 1.16, 11.7, 104, 54, -2.1, 13507, 0, 0.636],
       ["Wisconsin", 1.2, 11.8, 148, 59.9, 3.5, 7287, 41.1, 0.702],
       ["United", 1.04, 8.6, 204, 61, 3.5, 6650, 0, 2.116],
       ["Virginia", 1.07, 9.3, 174, 54.3, 5.9, 10093, 26.6, 1.306]],
      "clustering p.10")

# 69_1_Kitsana_KNN.pdf p.40–41 (และ Tree p.16–19) — Riding Mowers
owners = [(60.0, 18.4), (85.5, 16.8), (64.8, 21.6), (61.5, 20.8), (87.0, 23.6), (110.1, 19.2),
          (108.0, 17.6), (82.8, 22.4), (69.0, 20.0), (93.0, 20.8), (51.0, 22.0), (81.0, 20.0)]
nonowners = [(75.0, 19.6), (52.8, 20.8), (64.8, 17.2), (43.2, 20.4), (84.0, 17.6), (49.2, 17.6),
             (59.4, 16.0), (66.0, 18.4), (47.4, 16.4), (33.0, 18.8), (51.0, 14.0), (63.0, 14.8)]
write("riding_mowers.csv", ["Income", "Lot_Size", "Ownership"],
      [[i, l, "Owner"] for i, l in owners] + [[i, l, "Nonowner"] for i, l in nonowners],
      "KNN p.40–41")

# 69_1_Kitsana_KNN.pdf p.70–71 — ความน่าจะเป็นที่โมเดลทำนายว่าเป็น owner (ใช้ฝึก threshold)
probs = [("Owner", .9959), ("Owner", .9875), ("Owner", .9844), ("Owner", .9804),
         ("Owner", .9481), ("Owner", .8892), ("Owner", .8476), ("Nonowner", .7628),
         ("Owner", .7069), ("Owner", .6807), ("Owner", .6563), ("Nonowner", .6224),
         ("Owner", .5055), ("Nonowner", .4713), ("Nonowner", .3371), ("Owner", .2179),
         ("Nonowner", .1992), ("Nonowner", .1494), ("Nonowner", .0479), ("Nonowner", .0383),
         ("Nonowner", .0248), ("Nonowner", .0218), ("Nonowner", .0161), ("Nonowner", .0031)]
write("riding_mowers_probs.csv", ["Actual", "Prob_Owner"], probs, "KNN p.70–71")

# 69_1_Tree.pdf p.8 — Weather / Play (14 records)
write("weather.csv", ["Outlook", "Temperature", "Humidity", "Windy", "Class"],
      [["sunny", "hot", "high", "false", "N"], ["sunny", "hot", "high", "true", "N"],
       ["overcast", "hot", "high", "false", "P"], ["rain", "mild", "high", "false", "P"],
       ["rain", "cool", "normal", "false", "P"], ["rain", "cool", "normal", "true", "N"],
       ["overcast", "cool", "normal", "true", "P"], ["sunny", "mild", "high", "false", "N"],
       ["sunny", "cool", "normal", "false", "P"], ["rain", "mild", "normal", "false", "P"],
       ["sunny", "mild", "normal", "true", "P"], ["overcast", "mild", "high", "true", "P"],
       ["overcast", "hot", "normal", "false", "P"], ["rain", "mild", "high", "true", "N"]],
      "Tree p.8")

# 69_1_Tree.pdf p.7, 47 — Refund / Marital / Taxable Income / Cheat (10 records)
write("tid_cheat.csv", ["Tid", "Refund", "Marital", "Taxable_Income_K", "Cheat"],
      [[1, "Yes", "Single", 125, "No"], [2, "No", "Married", 100, "No"],
       [3, "No", "Single", 70, "No"], [4, "Yes", "Married", 120, "No"],
       [5, "No", "Divorced", 95, "Yes"], [6, "No", "Married", 60, "No"],
       [7, "Yes", "Divorced", 220, "No"], [8, "No", "Single", 85, "Yes"],
       [9, "No", "Married", 75, "No"], [10, "No", "Single", 90, "Yes"]],
      "Tree p.47")
