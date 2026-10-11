"""ไกด์ Python โจทย์ P1–P5 (รัน: final/.venv/bin/python final/practice/py_guides_a.py)"""
from guidegen import Step, build


def header(no, topic, story, data, tasks, minutes, lab_link):
    return f"""---
title: PR {no:02d} · {topic} (Python)
tags: [final, lab, practice, python]
---

# PR {no:02d} · {topic} — ไกด์ Python ทีละขั้น

> [!abstract] โจทย์
> {story}
>
> **สิ่งที่ต้องทำ:**
{tasks}

**ข้อมูล:** {data}
**เวลาแนะนำ:** {minutes} นาที · **ลิงก์:** [[PR 00 START HERE|หน้ารวมโจทย์]] · ทำโจทย์เดียวกันใน RapidMiner: [[PR {no:02d} {topic} (RapidMiner)]] · ทฤษฎี/สูตร: {lab_link}

> [!tip] เตรียมตัว (ครั้งแรกครั้งเดียว)
> 1. VS Code → **File → Open Folder…** → เลือกโฟลเดอร์ `data mining/final/practice`
> 2. สร้างไฟล์ใหม่ `p{no:02d}_mywork.ipynb` ในโฟลเดอร์นั้น
> 3. มุมขวาบน **Select Kernel → Jupyter Kernel… → Python (dm-exam)**
> 4. ทำทีละขั้น: พิมพ์โค้ด (หรือ copy) ลง cell ใหม่ → `Shift+Enter` → **เทียบกับ "ผลที่ควรได้"** ถ้าไม่ตรง หยุดหาสาเหตุก่อนไปขั้นต่อไป
> 5. ลองทำแบบ closed-book: อ่านแค่หัวข้อขั้นกับคำอธิบาย แล้วเขียนโค้ดเอง ค่อยเปิดดูโค้ดในไกด์

---
"""


# ════════════════════════════════════════════════════════════════════════════════════════════
P1 = [
Step("Import และตรวจข้อมูลทั้ง 3 ไฟล์",
"""อ่านไฟล์ทั้งหมดแล้วดูขนาด ชนิดข้อมูล และค่าว่าง — **ตรวจก่อนทำอะไรเสมอ**""",
"""
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
""",
"""สัปดาห์ 1 มี **{len(w1)}** บิล สัปดาห์ 2 มี **{len(w2)}** บิล · คอลัมน์เหมือนกัน 8 ตัว · ไม่มีค่าว่าง
`day_info` มี 4 วัน (Thur–Sun) พร้อม `is_weekend` และ `open_hours` → ต้อง **join** ด้วยคอลัมน์ `day`"""),
Step("Concatenate (Append) สองสัปดาห์",
"""ต่อ **แถว** ของสองไฟล์เป็นตารางเดียว — เช็กก่อนว่าคอลัมน์ตรงกัน""",
"""
print("คอลัมน์ต่างกัน:", set(w1.columns) ^ set(w2.columns))
bills = pd.concat([w1, w2], ignore_index=True)
print(bills.shape)
print("bill_id ซ้ำ:", bills["bill_id"].duplicated().sum())
""",
"""คอลัมน์ต่างกัน = `set()` (ตรงกันหมด) → ต่อแล้วได้ **{bills.shape[0]} แถว** ({len(w1)} + {len(w2)}) · bill_id ไม่ซ้ำ"""),
Step("Join กับตาราง day_info",
"""ใช้ **left join** — เก็บบิลทุกใบ แล้วเติมข้อมูลวันให้ (`validate="many_to_one"` เช็กว่าฝั่ง days ไม่มี key ซ้ำ)""",
"""
df = pd.merge(bills, days, on="day", how="left", validate="many_to_one")
print(df.shape)
print(df[["bill_id", "day", "is_weekend", "open_hours"]].head())
print("บิลที่ join ไม่เจอวัน:", df["is_weekend"].isna().sum())
""",
"""ได้ {df.shape[0]} แถว × {df.shape[1]} คอลัมน์ (เพิ่ม `is_weekend`, `open_hours`) · join ไม่เจอ = 0 → ทุกวันในบิลมีในตาราง days"""),
Step("สร้างคอลัมน์ใหม่: tip เป็น % ของบิล",
"""tip เป็นดอลลาร์เทียบกันไม่ได้ (บิลใหญ่ tip ก็ใหญ่) → ใช้ **tip_pct = tip / total_bill × 100**""",
"""
df["tip_pct"] = df["tip"] / df["total_bill"] * 100
print(df["tip_pct"].describe().round(2))
""",
"""tip เฉลี่ย **{df.tip_pct.mean():.2f}%** · median {df.tip_pct.median():.2f}% · max {df.tip_pct.max():.2f}% (สูงผิดปกติ — น่าจะเป็น outlier)"""),
Step("Select attributes + Filter examples",
"""เลือกคอลัมน์ที่สนใจ แล้วกรองเฉพาะ **มื้อเย็น โต๊ะ ≥ 4 คน**""",
"""
cols = ["bill_id", "day", "time", "size", "total_bill", "tip_pct", "is_weekend"]
big_dinner = df.loc[(df["time"] == "Dinner") & (df["size"] >= 4), cols]
print(len(big_dinner))
print(big_dinner.sort_values("total_bill", ascending=False).head(3))
""",
"""มีโต๊ะใหญ่มื้อเย็น **{len(big_dinner)}** บิล · ใช้ `&` และวงเล็บครอบแต่ละเงื่อนไขเสมอ"""),
Step("Aggregate: สรุปตามวัน",
"""groupby แล้วสรุปหลายค่าพร้อมกัน""",
"""
by_day = (df.groupby("day")
            .agg(n_bills=("bill_id", "count"), avg_bill=("total_bill", "mean"),
                 avg_tip_pct=("tip_pct", "mean"))
            .round(2).sort_values("avg_tip_pct", ascending=False))
print(by_day)
""",
"""วันที่ tip% สูงสุดคือ **{by_day.index[0]}** ({by_day.avg_tip_pct.iloc[0]:.2f}%) · วันที่บิลมากที่สุดคือ {by_day.n_bills.idxmax()} ({by_day.n_bills.max()} บิล)"""),
Step("Pivot: tip% เฉลี่ย ตามวัน × มื้อ",
"""แถว = day · คอลัมน์ = time · ค่า = mean ของ tip_pct · `margins=True` เพิ่มแถว/คอลัมน์รวม""",
"""
pv = pd.pivot_table(df, index="day", columns="time", values="tip_pct", aggfunc="mean", margins=True).round(2)
print(pv)
cnt = pd.crosstab(df["day"], df["time"])
print(cnt)
""",
"""มื้อกลางวันมีเฉพาะ Thur/Fri (Sat/Sun เป็น NaN) — crosstab ยืนยันว่า Sat/Sun ไม่มีมื้อกลางวันเลย · **ค่า NaN ใน pivot = ไม่มีข้อมูล ไม่ใช่ 0**"""),
Step("กราฟ 4 แบบ",
"""histogram (การกระจาย) · boxplot (เทียบกลุ่ม + outlier) · scatter (ความสัมพันธ์ 2 ตัวเลข) · bar (เทียบค่าเฉลี่ย)""",
"""
fig, ax = plt.subplots(2, 2, figsize=(11, 8))
sns.histplot(df, x="tip_pct", bins=25, ax=ax[0, 0]); ax[0, 0].set_title("tip % distribution")
sns.boxplot(df, x="day", y="tip_pct", order=["Thur", "Fri", "Sat", "Sun"], ax=ax[0, 1]); ax[0, 1].set_title("tip % by day")
sns.scatterplot(df, x="total_bill", y="tip", hue="time", ax=ax[1, 0]); ax[1, 0].set_title("tip vs total bill")
sns.barplot(df, x="is_weekend", y="tip_pct", errorbar=None, ax=ax[1, 1]); ax[1, 1].set_title("mean tip % weekend?")
plt.tight_layout()
""",
"""- histogram: ส่วนใหญ่ 10–20% · หางขวามีค่าสูงผิดปกติ (outlier)
- boxplot: median ของ 4 วันใกล้กัน · มี outlier ด้านบน
- scatter: tip เพิ่มตาม total_bill (ความสัมพันธ์บวก)
- bar: weekend vs weekday tip% ต่างกันไม่มาก"""),
Step("Correlation + outlier",
"""หา r ระหว่างตัวเลข แล้วหา outlier ของ tip_pct ด้วยกฎ IQR""",
"""
print(df[["total_bill", "tip", "size", "tip_pct"]].corr().round(3))
q1, q3 = df["tip_pct"].quantile([0.25, 0.75])
iqr = q3 - q1
upper = q3 + 1.5 * iqr
print(f"Q1={q1:.2f} Q3={q3:.2f} IQR={iqr:.2f} upper fence={upper:.2f}")
print(df.loc[df["tip_pct"] > upper, ["bill_id", "total_bill", "tip", "tip_pct"]].round(2))
""",
"""r(total_bill, tip) = **{df[['total_bill','tip']].corr().iloc[0,1]:.3f}** (บวกค่อนข้างสูง) · แต่ r(total_bill, tip_pct) = {df[['total_bill','tip_pct']].corr().iloc[0,1]:.3f} (ลบ) → บิลใหญ่ให้ tip เป็น **%** น้อยลง
outlier (> {upper:.2f}%): {int((df.tip_pct > upper).sum())} บิล — ต้องตรวจว่าเป็นค่าจริงหรือบันทึกผิดก่อนตัด"""),
]
P1_OUT = """
## ✅ สรุปคำตอบ (เทียบกับของคุณ)
| คำถาม | คำตอบ |
|---|---|
| รวมกี่บิล | {len(df)} บิล ({len(w1)} + {len(w2)}) |
| tip% เฉลี่ย | {df.tip_pct.mean():.2f}% |
| วันที่ tip% สูงสุด | {by_day.index[0]} ({by_day.avg_tip_pct.iloc[0]:.2f}%) |
| โต๊ะใหญ่มื้อเย็น | {len(big_dinner)} บิล |
| r(total_bill, tip) | {df[['total_bill','tip']].corr().iloc[0,1]:.3f} |

> [!question]- ลองเองต่อ (ไม่มีเฉลยโค้ด)
> 1. pivot ค่าเฉลี่ย total_bill ตาม `sex` × `smoker` แล้วตีความ 1 ประโยค
> 2. join แบบ inner กับตาราง days ที่ลบแถว Thur ออก → จำนวนแถวเหลือเท่าไร ทำไม
> 3. วาด boxplot tip_pct แยกตาม size แล้วบอกว่าโต๊ะขนาดไหนให้ tip% สูงสุด
"""

# ════════════════════════════════════════════════════════════════════════════════════════════
P2 = [
Step("Import + หาค่าว่าง",
"""Penguins 3 สายพันธุ์ · เป้าหมายสุดท้าย: เตรียมข้อมูลให้ KNN ทำนาย `species` โดย **ไม่ leak**""",
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder, KBinsDiscretizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier

peng = pd.read_csv("data/p2_penguins.csv")
print(peng.shape)
print(peng.isna().sum())
print(peng[peng.isna().any(axis=1)].head(6))
""",
"""ค่าว่าง: ตัวเลข 4 คอลัมน์ว่างคอลัมน์ละ 2 แถว (**แถวเดียวกัน** — ไม่มีการวัดเลย) · `sex` ว่าง {peng.sex.isna().sum()} แถว"""),
Step("ตัดแถวที่ไม่มีการวัดเลย",
"""แถวที่ทุกตัวเลขว่าง ไม่มีข้อมูลให้ใช้ → ตัดทิ้ง (เป็นการ clean ที่ไม่ได้ "เรียนค่า" จากข้อมูล จึงทำก่อน split ได้)""",
"""
num_cols = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
peng = peng.dropna(subset=num_cols, how="all").reset_index(drop=True)
print(peng.shape, "| sex ยังว่าง:", peng["sex"].isna().sum())
print(peng["species"].value_counts())
""",
"""เหลือ {len(peng)} แถว · sex ยังว่าง {peng.sex.isna().sum()} แถว (จะเติมด้วย mode จาก train) · คลาสไม่สมดุลเล็กน้อย (Adelie มากสุด)"""),
Step("ดูสเกลของแต่ละตัวแปร (ทำไมต้อง scale)",
"""""",
"""
print(peng[num_cols].describe().loc[["mean", "std", "min", "max"]].round(1))
""",
"""body_mass_g หลักพัน (std {peng.body_mass_g.std():.0f}) แต่ bill_depth_mm หลักสิบ (std {peng.bill_depth_mm.std():.1f}) → ถ้าไม่ scale KNN/PCA จะเห็นแค่ body_mass"""),
Step("Split ก่อน preprocessing (กัน leakage)",
"""แบ่ง 80/20 แบบ **stratify** — ล็อก test ไว้ ห้ามใช้คำนวณ mean/mode ใด ๆ""",
"""
X = peng.drop(columns="species")
y = peng["species"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=1992)
print(len(X_train), len(X_test))
print(y_train.value_counts(normalize=True).round(3))
""",
"""train {len(X_train)} / test {len(X_test)} · สัดส่วนคลาสใน train เท่ากับข้อมูลเดิม (stratify)"""),
Step("Impute: เติม sex ด้วย mode ของ train",
"""fit imputer บน train → transform ทั้ง train และ test""",
"""
sex_imp = SimpleImputer(strategy="most_frequent").fit(X_train[["sex"]])
print("mode ที่เรียนจาก train:", sex_imp.statistics_)
X_train_sex = sex_imp.transform(X_train[["sex"]])
X_test_sex = sex_imp.transform(X_test[["sex"]])
print("ค่าว่างหลังเติม:", pd.isna(X_train_sex).sum(), pd.isna(X_test_sex).sum())
""",
"""mode = **{sex_imp.statistics_[0]}** · เติมแล้วไม่มีค่าว่าง"""),
Step("Encode: one-hot ของ island และ sex",
"""nominal ไม่มีลำดับ → one-hot · `handle_unknown="ignore"` กัน test เจอค่าที่ train ไม่มี""",
"""
ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
ohe.fit(X_train[["island"]].assign(sex=X_train_sex.ravel()))
print(ohe.get_feature_names_out())
""",
"""ได้ {len(ohe.get_feature_names_out())} คอลัมน์ใหม่ (island 3 + sex 2)"""),
Step("Scale: standardize vs normalize",
"""เทียบสองวิธีบน train (fit บน train เท่านั้น)""",
"""
std = StandardScaler().fit(X_train[num_cols])
mm = MinMaxScaler().fit(X_train[num_cols])
z = pd.DataFrame(std.transform(X_test[num_cols]), columns=num_cols)
m = pd.DataFrame(mm.transform(X_test[num_cols]), columns=num_cols)
print("z-score test (mean, std):"); print(z.agg(["mean", "std"]).round(2))
print("min-max test (min, max):"); print(m.agg(["min", "max"]).round(2))
""",
"""z-score ของ **test** มี mean ไม่เป็น 0 เป๊ะ — **ถูกต้องแล้ว** เพราะใช้ mean/std ของ train · min-max ของ test อาจเกิน [0, 1] เล็กน้อยด้วยเหตุผลเดียวกัน"""),
Step("Discretize: body_mass เป็น 3 ช่วงจำนวนเท่ากัน",
"""equal frequency (quantile) — ขอบช่วงเรียนจาก train""",
"""
kb = KBinsDiscretizer(n_bins=3, encode="ordinal", strategy="quantile").fit(X_train[["body_mass_g"]])
print("ขอบช่วง:", kb.bin_edges_[0].round(0))
bins = kb.transform(X_train[["body_mass_g"]]).ravel()
print(pd.crosstab(pd.Series(bins, name="mass_bin", index=X_train.index), y_train))
""",
"""ขอบช่วง ≈ {kb.bin_edges_[0][1]:.0f} และ {kb.bin_edges_[0][2]:.0f} g · ช่วงหนักสุด (2) แทบเป็น Gentoo ทั้งหมด → body mass แยก Gentoo ได้ดี"""),
Step("PCA บนตัวเลข 4 ตัว (standardize ก่อน)",
"""explained variance + loadings · ใช้เพื่อ **ดูภาพ** จึง fit กับข้อมูลทั้งชุดได้ (descriptive)""",
"""
Z = StandardScaler().fit_transform(peng[num_cols])
pca = PCA().fit(Z)
print("explained:", pca.explained_variance_ratio_.round(4))
print("cumulative:", pca.explained_variance_ratio_.cumsum().round(4))
load = pd.DataFrame(pca.components_[:2].T, index=num_cols, columns=["PC1", "PC2"]).round(3)
print(load)
""",
"""PC1 {pca.explained_variance_ratio_[0]:.1%} · PC2 {pca.explained_variance_ratio_[1]:.1%} · รวม **{pca.explained_variance_ratio_[:2].sum():.1%}** → 2 มิติเก็บข้อมูลได้เกือบหมด
PC1: flipper, body_mass, bill_length (+) vs bill_depth (−) → "ขนาดตัว" · PC2 ขับด้วย bill_depth / bill_length → "รูปทรงปาก\""""),
Step("กราฟ PC1 × PC2 ระบายสีตาม species",
"""""",
"""
P = pca.transform(Z)[:, :2]
fig, ax = plt.subplots(figsize=(6, 5))
for sp in peng["species"].unique():
    mk = (peng["species"] == sp).to_numpy()
    ax.scatter(P[mk, 0], P[mk, 1], s=15, label=sp)
ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.0%})"); ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.0%})")
ax.legend(); ax.set_title("Penguins PCA")
""",
"""Gentoo แยกออกชัดตาม PC1 (ตัวใหญ่) · Adelie กับ Chinstrap แยกกันตาม PC2 (รูปปาก)"""),
Step("รวมทุกอย่างใน Pipeline + KNN (แบบที่ใช้ในข้อสอบจริง)",
"""ทุกขั้นที่เรียนค่าจากข้อมูลอยู่ใน Pipeline → CV จะ fit ใหม่ในทุก fold = **ไม่ leak**""",
"""
prep = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), num_cols),
    ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                      ("oh", OneHotEncoder(handle_unknown="ignore"))]), ["island", "sex"]),
])
model = Pipeline([("prep", prep), ("knn", KNeighborsClassifier(n_neighbors=5))])
cv = StratifiedKFold(5, shuffle=True, random_state=1992)
acc = cross_val_score(model, X_train, y_train, cv=cv)
model.fit(X_train, y_train)
test_acc = model.score(X_test, y_test)
raw = cross_val_score(KNeighborsClassifier(5), X_train[num_cols].fillna(X_train[num_cols].median()), y_train, cv=cv)
print("CV acc (pipeline):", acc.round(3), "mean", acc.mean().round(4))
print("test acc:", round(test_acc, 4))
print("CV acc ถ้าไม่ scale:", raw.mean().round(4))
""",
"""CV accuracy **{acc.mean():.4f}** · test **{test_acc:.4f}** · ถ้าไม่ scale เหลือ {raw.mean():.4f} → scaling ช่วยมาก"""),
]
P2_OUT = """
## ✅ สรุปคำตอบ
| คำถาม | คำตอบ |
|---|---|
| ค่าว่าง | ตัวเลขว่าง 2 แถว (ตัดทิ้ง) · sex ว่าง 11 → mode ของ train = {sex_imp.statistics_[0]} |
| PC1 + PC2 | {pca.explained_variance_ratio_[:2].sum():.1%} |
| CV / test accuracy (KNN k=5 + pipeline) | {acc.mean():.4f} / {test_acc:.4f} |
| ไม่ scale | {raw.mean():.4f} |

> [!question]- ลองเองต่อ
> 1. เปลี่ยน StandardScaler เป็น MinMaxScaler ใน pipeline แล้วเทียบ CV accuracy
> 2. ทำ PCA โดย **ไม่** standardize แล้วดูว่า PC1 อธิบายได้กี่ % และ loading ของ body_mass เท่าไร (ทำไม?)
> 3. เพิ่ม PCA(n_components=2) เข้าไปใน pipeline ก่อน KNN แล้วเทียบผล
"""

# ════════════════════════════════════════════════════════════════════════════════════════════
P3 = [
Step("Import + Imbalance Ratio",
"""ผลตรวจชิ้นเนื้อ 397 ราย · target = `diagnosis` (malignant = มะเร็ง = **positive**)""",
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

bc = pd.read_csv("data/p3_breast_cancer_imbalanced.csv")
X = bc.drop(columns="diagnosis")
y = (bc["diagnosis"] == "malignant").astype(int)
counts = y.value_counts()
IR = counts[0] / counts[1]
print(counts.to_dict(), "IR =", round(IR, 2))
""",
"""benign {counts[0]} : malignant {counts[1]} → **IR = {IR:.2f}** (mild, < 10) แต่คลาสที่สนใจมีแค่ {counts[1]/len(y):.1%}"""),
Step("Baseline: ทาย benign ทุกคน",
"""""",
"""
cv = StratifiedKFold(5, shuffle=True, random_state=1992)
scoring = ["accuracy", "precision", "recall", "f1"]
def run(name, model):
    r = cross_validate(model, X, y, cv=cv, scoring=scoring)
    return {"model": name, **{m: round(float(r[f"test_{m}"].mean()), 4) for m in scoring}}
import warnings; warnings.filterwarnings("ignore")
rows = [run("Majority baseline", DummyClassifier(strategy="most_frequent"))]
print(rows[0])
""",
"""accuracy **{rows[0]['accuracy']:.4f}** โดยหามะเร็งไม่เจอเลย (recall 0) → **ห้ามใช้ accuracy ตัดสิน**"""),
Step("E0: Decision Tree ไม่ทำอะไรกับ imbalance",
"""""",
"""
tree = DecisionTreeClassifier(max_depth=4, random_state=1992)
rows.append(run("E0 tree (no sampling)", Pipeline([("sc", StandardScaler()), ("tree", tree)])))
print(rows[-1])
""",
"""recall = {rows[1]['recall']:.4f} · F1 = {rows[1]['f1']:.4f}"""),
Step("E1–E3: RUS / ROS / SMOTE — ใส่ใน imblearn Pipeline",
"""sampler อยู่ **ใน** Pipeline → ทำเฉพาะ training fold · validation fold เป็นข้อมูลจริง""",
"""
for name, sampler in [("E1 RUS", RandomUnderSampler(random_state=1992)),
                      ("E2 ROS", RandomOverSampler(random_state=1992)),
                      ("E3 SMOTE", SMOTE(k_neighbors=5, random_state=1992))]:
    rows.append(run(name, Pipeline([("sc", StandardScaler()), ("sample", sampler), ("tree", tree)])))
table = pd.DataFrame(rows)
print(table.to_string(index=False))
""",
"""ดูคอลัมน์ **recall และ F1** ไม่ใช่ accuracy:
- **E0 (ไม่ resample) ได้ F1 สูงสุด {table.f1.iloc[1]:.4f}** แต่ recall {table.recall.iloc[1]:.3f} (พลาดมะเร็ง {1-table.recall.iloc[1]:.0%})
- **RUS ได้ recall สูงสุด {table.recall.iloc[2]:.3f}** แต่ precision ตกเหลือ {table.precision.iloc[2]:.3f}
- SMOTE: recall {table.recall.iloc[4]:.3f} · precision {table.precision.iloc[4]:.3f} · F1 {table.f1.iloc[4]:.4f} (ดีกว่า RUS/ROS ด้าน F1)
→ **resampling เพิ่ม recall แลกกับ precision** — จะเลือกตัวไหนขึ้นกับเป้าหมาย"""),
Step("SMOTE ทำอะไรกับจำนวนแถว (ใน training fold เดียว)",
"""ดูผลของ SMOTE บน train ของ fold แรก""",
"""
tr_idx, va_idx = next(cv.split(X, y))
Xs, ys = SMOTE(random_state=1992).fit_resample(StandardScaler().fit_transform(X.iloc[tr_idx]), y.iloc[tr_idx])
print("ก่อน:", y.iloc[tr_idx].value_counts().to_dict(), "→ หลัง:", pd.Series(ys).value_counts().to_dict())
print("validation fold (ไม่ถูกแตะ):", y.iloc[va_idx].value_counts().to_dict())
""",
"""SMOTE สร้าง malignant สังเคราะห์จนเท่า benign · validation fold ยังเป็นสัดส่วนจริง"""),
Step("วิธีที่ผิด: SMOTE ก่อน CV (ดูว่าผลดีเกินจริงแค่ไหน)",
"""**ห้ามทำในข้อสอบ** — ทำเพื่อเห็นผลของ leakage""",
"""
X_bad, y_bad = SMOTE(random_state=1992).fit_resample(StandardScaler().fit_transform(X), y)
bad = cross_val_score(tree, X_bad, y_bad, cv=cv, scoring="f1").mean()
print("F1 แบบผิด (SMOTE ก่อน CV):", round(bad, 4), "| แบบถูก:", table.f1.iloc[4])
""",
"""แบบผิดได้ F1 **{bad:.4f}** สูงกว่าแบบถูก ({table.f1.iloc[4]:.4f}) — เพราะ validation มีจุดสังเคราะห์ที่เกือบซ้ำกับ train และสัดส่วนไม่ใช่โลกจริง (สไลด์ Imbalanced p.22)"""),
]
P3_OUT = """
## ✅ สรุปคำตอบ
{md_table(table)}

**เลือกอย่างไร (ตัวอย่างคำตอบ):** งานคัดกรองมะเร็ง การพลาดผู้ป่วย (FN) อันตรายกว่าการส่งตรวจซ้ำ (FP) → ให้น้ำหนัก **recall** → เลือก **SMOTE** (recall {table.recall.iloc[4]:.3f} และ F1 ดีกว่า RUS) หรือ RUS ถ้าต้องการ recall สูงสุด · ถ้าโจทย์ให้ใช้ **F1** เป็นเกณฑ์ → E0 ({table.f1.iloc[1]:.4f}) ชนะ · baseline accuracy {rows[0]['accuracy']:.4f} แต่ recall 0 → accuracy ใช้ตัดสินไม่ได้
**SMOTE ก่อน CV** ให้ F1 {bad:.4f} (ดีเกินจริง) — ผิดหลัก "sampling เฉพาะ training data"

> [!question]- ลองเองต่อ
> 1. ใช้ `class_weight="balanced"` ใน DecisionTreeClassifier (ไม่ resample) แล้วเทียบ F1
> 2. เปลี่ยนโมเดลเป็น RandomForest แล้วดูว่ายังต้องใช้ SMOTE ไหม
"""

# ════════════════════════════════════════════════════════════════════════════════════════════
P4 = [
Step("Import + ดูสเกล",
"""ไวน์ 178 ตัวอย่าง จากองุ่น 3 สายพันธุ์ · ทำนาย `cultivar` ด้วย KNN""",
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold, cross_validate, GridSearchCV, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import confusion_matrix, classification_report

wine = pd.read_csv("data/p4_wine.csv")
X = wine.drop(columns="cultivar")
y = wine["cultivar"]
print(wine.shape)
print(y.value_counts())
print(X.agg(["min", "max"]).T.sort_values("max", ascending=False).head(4))
""",
"""13 feature · proline ช่วงหลักร้อย–พัน ขณะที่ตัวอื่นหลักหน่วย → **KNN ต้อง scale**"""),
Step("Baseline + KNN ไม่ scale + KNN scale (folds เดียวกัน)",
"""""",
"""
cv = StratifiedKFold(10, shuffle=True, random_state=1992)
def run(name, model):
    r = cross_validate(model, X, y, cv=cv, scoring=["accuracy", "f1_macro"])
    return {"model": name, "accuracy": round(r["test_accuracy"].mean(), 4), "f1_macro": round(r["test_f1_macro"].mean(), 4)}
rows = [run("Majority baseline", DummyClassifier(strategy="most_frequent")),
        run("KNN k=5 (raw)", KNeighborsClassifier(n_neighbors=5)),
        run("KNN k=5 (scaled)", Pipeline([("sc", StandardScaler()), ("knn", KNeighborsClassifier(n_neighbors=5))]))]
print(pd.DataFrame(rows).to_string(index=False))
""",
"""baseline {rows[0]['accuracy']:.4f} · KNN ไม่ scale {rows[1]['accuracy']:.4f} · **scale แล้ว {rows[2]['accuracy']:.4f}** (เพิ่ม {rows[2]['accuracy']-rows[1]['accuracy']:.3f})
multi-class → ใช้ **f1_macro** (เฉลี่ย F1 ของทุกคลาส)"""),
Step("Optimize k และ weights ด้วย GridSearchCV",
"""ใช้ **cv เดิม** · เลือกด้วย accuracy""",
"""
pipe = Pipeline([("sc", StandardScaler()), ("knn", KNeighborsClassifier())])
grid = GridSearchCV(pipe, {"knn__n_neighbors": list(range(1, 31, 2)), "knn__weights": ["uniform", "distance"]},
                    cv=cv, scoring="accuracy").fit(X, y)
res = pd.DataFrame(grid.cv_results_)
top5 = res.sort_values(["mean_test_score", "param_knn__n_neighbors"], ascending=[False, True])[
    ["param_knn__n_neighbors", "param_knn__weights", "mean_test_score", "std_test_score"]].head(5).round(4)
print(grid.best_params_, round(grid.best_score_, 4))
print(top5.to_string(index=False))
""",
"""best = **k {grid.best_params_['knn__n_neighbors']}, {grid.best_params_['knn__weights']}** accuracy {grid.best_score_:.4f} · หลายค่า k ได้ผลใกล้กัน"""),
Step("กราฟ accuracy vs k",
"""""",
"""
u = res[res["param_knn__weights"] == "uniform"]
plt.figure(figsize=(7, 3.5))
plt.errorbar(u["param_knn__n_neighbors"], u["mean_test_score"], yerr=u["std_test_score"], marker="o", capsize=3)
plt.xlabel("k"); plt.ylabel("CV accuracy"); plt.title("Choosing k (uniform)")
""",
"""k = 1 ได้ {u[u.param_knn__n_neighbors == 1].mean_test_score.iloc[0]:.4f} · k = 5 ได้ {u[u.param_knn__n_neighbors == 5].mean_test_score.iloc[0]:.4f} · k = 29 ได้ {u[u.param_knn__n_neighbors == 29].mean_test_score.iloc[0]:.4f} · error bar = std ข้าม fold (ช่วง k กว้างให้ผลใกล้กัน → เลือก k ที่ดีสุดตัวเล็กที่สุด)"""),
Step("Confusion matrix + classification report จาก CV",
"""""",
"""
best = grid.best_estimator_
pred = cross_val_predict(best, X, y, cv=cv)
labels = sorted(y.unique())
print(pd.DataFrame(confusion_matrix(y, pred, labels=labels), index=labels, columns=labels))
print(classification_report(y, pred, digits=3))
""",
"""แถว = actual · คอลัมน์ = predicted · ผิดพลาดน้อยมาก ส่วนใหญ่สับสนระหว่าง cultivar_1 กับคลาสอื่น"""),
Step("ทำนายไวน์ใหม่",
"""ไวน์ใหม่ 1 ขวด (ใช้ค่าเฉลี่ยของ cultivar_0 ปัดเศษ) → pipeline scale ให้เองด้วยค่าจาก train""",
"""
new = X[y == "cultivar_0"].mean().round(2).to_frame().T
best.fit(X, y)
print(best.predict(new), best.predict_proba(new).round(3))
""",
"""ทายเป็น **{best.predict(new)[0]}** · `predict_proba` = สัดส่วนโหวตของเพื่อนบ้าน"""),
]
P4_OUT = """
## ✅ สรุปคำตอบ
{md_table(pd.DataFrame(rows + [dict(model='KNN tuned k=' + str(grid.best_params_['knn__n_neighbors']) + ' ' + grid.best_params_['knn__weights'], accuracy=round(grid.best_score_, 4), f1_macro='—')]))}

**ตีความ:** scaling เป็นตัวเปลี่ยนผลมากที่สุด · tune k ช่วยเพิ่มอีกเล็กน้อย/เท่าเดิม · ทุกโมเดลชนะ baseline มาก

> [!question]- ลองเองต่อ
> 1. ใช้ `metric="manhattan"` แล้วเทียบ
> 2. ใช้ hold-out 70/30 แทน CV แล้วรันหลาย random_state — ผลแกว่งแค่ไหน (เหตุผลที่ CV ดีกว่า)
"""

# ════════════════════════════════════════════════════════════════════════════════════════════
P5 = [
Step("Import + หาค่าว่างแฝง (0 ที่เป็นไปไม่ได้)",
"""Pima 768 คน · target `diabetes` (1 = เป็นเบาหวาน) · glucose/BP/BMI = 0 เป็นไปไม่ได้ทางการแพทย์""",
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score, roc_auc_score

pima = pd.read_csv("data/p5_pima_diabetes.csv")
zero_cols = ["glucose", "blood_pressure", "skin_thickness", "insulin", "bmi"]
print((pima[zero_cols] == 0).sum())
print(pima["diabetes"].value_counts(normalize=True).round(3))
""",
"""insulin เป็น 0 ถึง {(pima.insulin==0).sum()} แถว · skin {(pima.skin_thickness==0).sum()} · เป็นเบาหวาน {pima.diabetes.mean():.1%}"""),
Step("แปลง 0 → NaN แล้ว split",
"""""",
"""
pima[zero_cols] = pima[zero_cols].replace(0, np.nan)
X = pima.drop(columns="diabetes"); y = pima["diabetes"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=1992)
print(len(X_train), len(X_test), "| NaN ใน train:", X_train.isna().sum().sum())
""",
"""train {len(X_train)} / test {len(X_test)} · median ที่จะเติมต้องคำนวณจาก train (อยู่ใน pipeline ขั้นถัดไป)"""),
Step("Pipeline: impute median → scale → logistic",
"""""",
"""
logreg = Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler()),
                   ("lr", LogisticRegression(max_iter=1000))]).fit(X_train, y_train)
coef = pd.DataFrame({"coef (per 1 SD)": logreg["lr"].coef_[0], "odds ratio": np.exp(logreg["lr"].coef_[0])},
                    index=X.columns).sort_values("coef (per 1 SD)", ascending=False).round(3)
print("intercept:", logreg["lr"].intercept_.round(3))
print(coef)
""",
"""glucose มีผลมากที่สุด: odds ratio **{coef.loc['glucose','odds ratio']:.2f}** → glucose เพิ่ม 1 SD odds ของเบาหวานคูณ {coef.loc['glucose','odds ratio']:.2f} (ตัวอื่นคงที่) · ตัวที่ OR ≈ 1 แทบไม่มีผล"""),
Step("ความน่าจะเป็น → threshold 0.5",
"""""",
"""
proba = logreg.predict_proba(X_test)[:, 1]
print("5 คนแรก P(diabetes):", proba[:5].round(3))
pred = (proba >= 0.5).astype(int)
tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()
print(f"TN={tn} FP={fp} FN={fn} TP={tp}")
print("acc", round(accuracy_score(y_test, pred), 3), "precision", round(precision_score(y_test, pred), 3),
      "recall", round(recall_score(y_test, pred), 3), "F1", round(f1_score(y_test, pred), 3))
print("AUC", round(roc_auc_score(y_test, proba), 3))
""",
"""ที่ 0.5: recall **{recall_score(y_test, pred):.3f}** → พลาดผู้ป่วยไป {fn} คน (FN) — สำหรับการคัดกรองถือว่ามากเกินไป"""),
Step("เทียบหลาย threshold",
"""""",
"""
rows = []
for t in [0.2, 0.3, 0.4, 0.5, 0.6]:
    p = (proba >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, p).ravel()
    rows.append({"threshold": t, "TP": tp, "FN": fn, "FP": fp, "TN": tn,
                 "precision": round(precision_score(y_test, p), 3), "recall": round(recall_score(y_test, p), 3),
                 "F1": round(f1_score(y_test, p), 3)})
thr = pd.DataFrame(rows)
print(thr.to_string(index=False))
""",
"""threshold ↓ → recall ↑ precision ↓ · ที่ 0.3: recall {thr.recall[1]:.3f} (FN {thr.FN[1]}) F1 {thr.F1[1]:.3f}"""),
Step("ทำนายผู้ป่วยใหม่",
"""""",
"""
patient = pd.DataFrame([{"pregnancies": 2, "glucose": 150, "blood_pressure": 70, "skin_thickness": np.nan,
                         "insulin": np.nan, "bmi": 33.5, "pedigree": 0.5, "age": 45}])
p_new = logreg.predict_proba(patient)[0, 1]
print("P(diabetes) =", round(p_new, 3), "→ threshold 0.3:", int(p_new >= 0.3), "| threshold 0.5:", int(p_new >= 0.5))
""",
"""P = **{p_new:.3f}** · ค่าว่าง (skin, insulin) ถูกเติมด้วย median ของ train ให้อัตโนมัติ"""),
]
P5_OUT = """
## ✅ สรุปคำตอบ
| คำถาม | คำตอบ |
|---|---|
| ค่าว่างแฝง | 0 ใน 5 คอลัมน์ → NaN → median (จาก train) |
| ตัวแปรสำคัญสุด | glucose (OR {coef.loc['glucose','odds ratio']:.2f} ต่อ 1 SD) |
| AUC | {roc_auc_score(y_test, proba):.3f} |
| threshold สำหรับคัดกรอง | ต่ำกว่า 0.5 (เช่น 0.3: recall {thr.recall[1]:.3f}) เพราะพลาดผู้ป่วยแพงกว่าตรวจซ้ำ |

{md_table(thr)}

> [!question]- ลองเองต่อ
> 1. ทำ 5-fold CV ด้วย `cross_val_predict(method="predict_proba")` แล้วหา threshold ที่ F1 สูงสุด
> 2. ลองไม่แปลง 0 → NaN แล้วดูว่า coefficient ของ insulin เปลี่ยนอย่างไร
"""

if __name__ == "__main__":
    build("p1", "Data Handling", header(1, "Data Handling", "ร้านอาหารส่งบิล 2 สัปดาห์มาเป็น 2 ไฟล์ และตารางข้อมูลวันทำการแยกอีกไฟล์ ผู้จัดการอยากรู้ว่า **tip เป็น % ของบิล** ต่างกันตามวันและมื้อหรือไม่",
          "`data/p1_bills_week1.csv`, `data/p1_bills_week2.csv` (บิล), `data/p1_day_info.csv` (ข้อมูลวัน) — ข้อมูล tips ของ seaborn",
          "> 1. import + ตรวจ 3 ไฟล์ 2. **append** สองสัปดาห์ 3. **join** กับ day_info 4. สร้าง tip_pct 5. **select + filter** โต๊ะใหญ่มื้อเย็น 6. **aggregate** ตามวัน 7. **pivot** วัน × มื้อ 8. กราฟ 4 แบบ + ตีความ 9. correlation + outlier",
          45, "[[LAB 02 Data Handling & Visualization]]"), P1, P1_OUT, "PR 01 Data Handling (Python).md")
    build("p2", "Preprocessing & PCA", header(2, "Preprocessing & PCA", "นักชีววิทยาวัดนกเพนกวิน 344 ตัว 3 สายพันธุ์ ข้อมูลมีค่าว่างและหน่วยต่างกัน จงเตรียมข้อมูลสำหรับ KNN ทำนายสายพันธุ์ **โดยไม่เกิด data leakage** และใช้ PCA ดูภาพ 2 มิติ",
          "`data/p2_penguins.csv` (Palmer Penguins)", "> 1. หาค่าว่าง 2. ตัดแถวที่ไม่มีการวัด 3. ดูสเกล 4. **split ก่อน** 5. impute mode 6. one-hot 7. standardize vs normalize 8. discretize 9. PCA + loadings 10. PCA plot 11. Pipeline + KNN + CV",
          50, "[[LAB 03 Preprocessing Recipes]]"), P2, P2_OUT, "PR 02 Preprocessing & PCA (Python).md")
    build("p3", "Imbalanced & SMOTE", header(3, "Imbalanced & SMOTE", "โรงพยาบาลมีผลตรวจชิ้นเนื้อ 397 ราย มีมะเร็ง (malignant) เพียง 40 ราย จงสร้างโมเดลที่หามะเร็งได้ดี และเปรียบเทียบการไม่ resample / RUS / ROS / SMOTE โดยทำ resampling **เฉพาะ training fold**",
          "`data/p3_breast_cancer_imbalanced.csv` (UCI Breast Cancer Wisconsin, 10 feature กลุ่ม mean)", "> 1. IR 2. majority baseline 3. tree ไม่ resample 4. RUS/ROS/SMOTE ใน pipeline 5. ดูผล SMOTE ต่อจำนวนแถว 6. เทียบกับวิธีผิด (SMOTE ก่อน CV)",
          35, "[[LEC 04 Imbalanced Classification]] · [[LAB 03 Preprocessing Recipes#3.5 Sampling & SMOTE ⭐⭐⭐]]"), P3, P3_OUT, "PR 03 Imbalanced & SMOTE (Python).md")
    build("p4", "KNN Baseline CV Optimize", header(4, "KNN Baseline CV Optimize", "โรงบ่มไวน์ต้องการระบุสายพันธุ์องุ่นจากผลวิเคราะห์ทางเคมี 13 ค่า จงสร้าง baseline, KNN ก่อน/หลัง scale, optimize k ด้วย CV, แสดง top-5, confusion matrix และทำนายไวน์ใหม่",
          "`data/p4_wine.csv` (UCI Wine, 178 ตัวอย่าง 3 คลาส)", "> 1. ดูสเกล 2. baseline + KNN raw + KNN scaled 3. grid search k × weights 4. กราฟ k 5. confusion matrix 6. ทำนายไวน์ใหม่",
          40, "[[LAB 04 Workflow, Baseline & Evaluation]] · [[LAB 05 Supervised Models#5.1 K-Nearest Neighbors ⭐⭐⭐]]"), P4, P4_OUT, "PR 04 KNN Baseline CV Optimize (Python).md")
    build("p5", "Logistic Regression & Threshold", header(5, "Logistic Regression & Threshold", "คลินิกต้องการคัดกรองผู้ป่วยเบาหวานจากผลตรวจ 8 ค่า จงจัดการค่าว่างแฝง สร้าง Logistic Regression ตีความ odds ratio และเลือก threshold ที่เหมาะกับการคัดกรอง",
          "`data/p5_pima_diabetes.csv` (Pima Indians Diabetes, 768 คน)", "> 1. หา 0 ที่เป็นค่าว่าง 2. 0 → NaN + split 3. pipeline + coefficient/odds 4. predict_proba + threshold 0.5 5. เทียบหลาย threshold 6. ทำนายผู้ป่วยใหม่",
          40, "[[LAB 05 Supervised Models#5.3 Logistic Regression ⭐⭐⭐⭐ (gap ใหญ่)]] · [[LEC 07 Linear & Logistic Regression]]"), P5, P5_OUT, "PR 05 Logistic Regression & Threshold (Python).md")
