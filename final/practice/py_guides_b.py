"""ไกด์ Python โจทย์ P6–P9 (รัน: final/.venv/bin/python final/practice/py_guides_b.py)"""
from guidegen import Step, build
from py_guides_a import header

# ════════════════════════════════════════════════════════════════════════════════════════════
P6 = [
Step("Import + ดูข้อมูล",
"""ผู้ป่วย 303 คน · `target` = 1 เป็นโรคหัวใจ · หลายคอลัมน์เป็น **รหัสหมวด** (cp, restecg, slope, ca, thal) แม้เก็บเป็นตัวเลข""",
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, recall_score, f1_score

heart = pd.read_csv("data/p6_heart.csv")
print(heart.shape, "| missing:", heart.isna().sum().sum())
print(heart["target"].value_counts().to_dict())
print(heart.nunique().sort_values().head(8).to_dict())
X = heart.drop(columns="target"); y = heart["target"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=1992)
print(len(X_train), len(X_test))
""",
"""ไม่มีค่าว่าง · เป็นโรค {y.sum()} / ไม่เป็น {(y==0).sum()} (ค่อนข้างสมดุล) · tree **ไม่ต้อง scale และไม่ต้อง one-hot** รหัสหมวดก็ได้ (แต่ต้องรู้ว่ามันเป็นหมวด)"""),
Step("Tree โตเต็ม: train vs test",
"""""",
"""
full = DecisionTreeClassifier(random_state=1992).fit(X_train, y_train)
print("depth:", full.get_depth(), "| leaves:", full.get_n_leaves())
print("train acc:", round(full.score(X_train, y_train), 4), "| test acc:", round(full.score(X_test, y_test), 4))
""",
"""train **{full.score(X_train, y_train):.4f}** (จำได้หมด) แต่ test **{full.score(X_test, y_test):.4f}** → **overfitting** · tree ลึก {full.get_depth()} ชั้น มี {full.get_n_leaves()} ใบ"""),
Step("กราฟความลึก vs train/CV accuracy",
"""""",
"""
cv = StratifiedKFold(10, shuffle=True, random_state=1992)
rows = []
for d in range(1, 13):
    r = cross_validate(DecisionTreeClassifier(max_depth=d, random_state=1992), X_train, y_train, cv=cv, return_train_score=True)
    rows.append({"depth": d, "train": r["train_score"].mean(), "cv": r["test_score"].mean()})
dt = pd.DataFrame(rows).round(4)
print(dt.to_string(index=False))
plt.figure(figsize=(7, 3.5))
plt.plot(dt.depth, dt.train, "o-", label="train"); plt.plot(dt.depth, dt.cv, "s-", label="CV")
plt.xlabel("max_depth"); plt.ylabel("accuracy"); plt.legend(); plt.title("Tree depth vs accuracy")
best_d = int(dt.loc[dt.cv.idxmax(), "depth"])
""",
"""CV สูงสุดที่ depth **{best_d}** ({dt.cv.max():.4f}) · train เพิ่มเรื่อย ๆ จนใกล้ 1 แต่ CV ไม่เพิ่ม → ช่องว่าง = overfitting"""),
Step("Optimize tree (criterion × depth × min leaf)",
"""""",
"""
grid = GridSearchCV(DecisionTreeClassifier(random_state=1992),
                    {"criterion": ["gini", "entropy"], "max_depth": [2, 3, 4, 5, 6], "min_samples_leaf": [1, 5, 10, 20]},
                    cv=cv, scoring="accuracy").fit(X_train, y_train)
print(grid.best_params_, round(grid.best_score_, 4))
tree = grid.best_estimator_
print("test acc:", round(tree.score(X_test, y_test), 4))
print(export_text(tree, feature_names=list(X.columns), max_depth=3))
""",
"""best: **{grid.best_params_}** · CV {grid.best_score_:.4f} · test {tree.score(X_test, y_test):.4f}
root split = feature ที่ลด impurity มากที่สุด (บรรทัดแรกของ export_text)"""),
Step("วาด tree",
"""""",
"""
plt.figure(figsize=(14, 6))
plot_tree(tree, feature_names=list(X.columns), class_names=["healthy", "disease"], filled=True, max_depth=3, fontsize=8)
""",
"""แต่ละกล่อง: เงื่อนไข · impurity · samples · value (จำนวนแต่ละคลาส) · class ที่ทาย · สีเข้ม = บริสุทธิ์มาก"""),
Step("Random Forest default และ tuned",
"""""",
"""
rf = RandomForestClassifier(n_estimators=300, random_state=1992, n_jobs=-1)
rf_cv = cross_validate(rf, X_train, y_train, cv=cv)["test_score"].mean()
rf_grid = GridSearchCV(RandomForestClassifier(n_estimators=300, random_state=1992, n_jobs=-1),
                       {"max_features": ["sqrt", 0.5], "min_samples_leaf": [1, 3, 5]}, cv=cv, scoring="accuracy").fit(X_train, y_train)
print("RF default CV:", round(rf_cv, 4))
print("RF tuned:", rf_grid.best_params_, round(rf_grid.best_score_, 4))
rf_best = rf_grid.best_estimator_
print("RF test acc:", round(rf_best.score(X_test, y_test), 4))
""",
"""RF default CV {rf_cv:.4f} · tuned {rf_grid.best_score_:.4f} · test **{rf_best.score(X_test, y_test):.4f}**"""),
Step("Feature importance + ตารางเปรียบเทียบ",
"""""",
"""
imp = pd.Series(rf_best.feature_importances_, index=X.columns).sort_values(ascending=False).round(3)
print(imp.head(5))
base = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
comp = pd.DataFrame([
    {"model": "Majority baseline", "test acc": base.score(X_test, y_test), "recall": recall_score(y_test, base.predict(X_test))},
    {"model": "Tree (full)", "test acc": full.score(X_test, y_test), "recall": recall_score(y_test, full.predict(X_test))},
    {"model": "Tree (tuned)", "test acc": tree.score(X_test, y_test), "recall": recall_score(y_test, tree.predict(X_test))},
    {"model": "RF (tuned)", "test acc": rf_best.score(X_test, y_test), "recall": recall_score(y_test, rf_best.predict(X_test))},
]).round(4)
print(comp.to_string(index=False))
""",
"""feature สำคัญอันดับ 1–3: **{imp.index[0]}, {imp.index[1]}, {imp.index[2]}** · importance ไม่บอกทิศทาง (เพิ่มหรือลดความเสี่ยง)
⚠️ baseline ได้ recall **1.0** เพราะคลาสส่วนมากของข้อมูลนี้คือ "เป็นโรค" (target = 1) → ทายเป็นโรคทุกคน — accuracy {comp.iloc[0, 1]:.4f} · recall สูงจากการทายเหมาเป็นกับดัก ต้องดู precision/accuracy ประกอบ"""),
]
P6_OUT = """
## ✅ สรุปคำตอบ
{md_table(comp)}

**ตีความ:** tree โตเต็มจำ train ได้ {full.score(X_train, y_train):.0%} แต่ test {full.score(X_test, y_test):.4f} = overfitting · tree ที่ tune (depth {tree.get_depth()}, {tree.get_n_leaves()} ใบ) ได้ test **เท่ากัน** แต่ CV ดีกว่ามาก ({grid.best_score_:.4f} vs {dt.cv.iloc[7]:.4f} ที่ depth 8) และง่ายกว่ามาก → เลือกตัวที่ง่ายกว่า (parsimony) · RF รวม 300 ต้นที่ต่างกัน (bootstrap + สุ่ม feature) จึงเสถียรกว่า · ข้อมูล test แค่ {len(y_test)} คน — ต่างกัน 1–2 คนก็เปลี่ยน accuracy ~1–3% ระวังการสรุป

> [!question]- ลองเองต่อ
> 1. ใช้ `ccp_alpha` (post-pruning) หา tree ที่ดีที่สุด
> 2. ทำนายผู้ป่วย age 60, sex 1, cp 0, trestbps 140, chol 260, fbs 0, restecg 1, thalach 130, exang 1, oldpeak 2.0, slope 1, ca 2, thal 3 ด้วย tree และ RF แล้วเทียบ predict_proba
"""

# ════════════════════════════════════════════════════════════════════════════════════════════
P7 = [
Step("Import + EDA ของ target",
"""ค่ารักษาพยาบาลรายปี (`charges`) ของผู้ถือกรมธรรม์ 1,338 คน""",
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, KFold, cross_validate, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error, r2_score

ins = pd.read_csv("data/p7_insurance.csv")
print(ins.shape, "| missing:", ins.isna().sum().sum())
print(ins["charges"].describe().round(0))
print("skew:", round(ins["charges"].skew(), 3))
print(ins.groupby("smoker")["charges"].mean().round(0))
fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
sns.histplot(ins, x="charges", bins=40, ax=ax[0]); ax[0].set_title("charges")
sns.scatterplot(ins, x="age", y="charges", hue="smoker", s=12, ax=ax[1]); ax[1].set_title("age vs charges")
""",
"""charges เบ้ขวา (skew {ins.charges.skew():.2f}, mean > median) · คนสูบบุหรี่จ่ายเฉลี่ย {ins[ins.smoker=='yes'].charges.mean():,.0f} vs ไม่สูบ {ins[ins.smoker=='no'].charges.mean():,.0f} (~{ins[ins.smoker=='yes'].charges.mean()/ins[ins.smoker=='no'].charges.mean():.1f} เท่า) · scatter เห็น 3 แถบตามอายุ (smoker แยกเป็นแถบบน)"""),
Step("Encode categorical (drop_first) + split",
"""linear regression ใช้ dummy แบบ **k−1** (`drop_first=True`) กัน dummy variable trap""",
"""
X = pd.get_dummies(ins.drop(columns="charges"), columns=["sex", "smoker", "region"], drop_first=True, dtype=int)
y = ins["charges"]
print(list(X.columns))
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1992)
print(len(X_train), len(X_test))
""",
"""baseline ของแต่ละ dummy: sex = female · smoker = no · region = northeast (ตัวที่ถูกตัด)"""),
Step("Mean baseline vs Linear Regression",
"""""",
"""
def metrics(name, model):
    p = model.fit(X_train, y_train).predict(X_test)
    return {"model": name, "MAE": mean_absolute_error(y_test, p), "RMSE": root_mean_squared_error(y_test, p),
            "R2": r2_score(y_test, p)}
lin = LinearRegression()
rows = [metrics("Mean baseline", DummyRegressor(strategy="mean")), metrics("Linear Regression", lin)]
print(pd.DataFrame(rows).round(3).to_string(index=False))
""",
"""Linear Regression: MAE **{rows[1]['MAE']:,.0f}** · RMSE {rows[1]['RMSE']:,.0f} · R² **{rows[1]['R2']:.3f}** — ดีกว่า baseline (R² {rows[0]['R2']:.3f}) มาก"""),
Step("ตีความ coefficient",
"""""",
"""
coef = pd.Series(lin.coef_, index=X.columns).round(1)
print("intercept:", round(lin.intercept_, 1))
print(coef.sort_values(ascending=False))
""",
"""- **smoker_yes = {coef['smoker_yes']:,.0f}** → คนสูบบุหรี่ค่ารักษาสูงกว่าคนไม่สูบ ~{coef['smoker_yes']:,.0f} ต่อปี **โดยตัวแปรอื่นคงที่**
- **age = {coef['age']:,.1f}** → อายุ +1 ปี ค่ารักษา +{coef['age']:,.0f}
- **bmi = {coef['bmi']:,.1f}** → BMI +1 ค่ารักษา +{coef['bmi']:,.0f}
- region_* ติดลบ = ถูกกว่า northeast (baseline)"""),
Step("KNN regressor: ก่อน/หลัง scale + optimize k (CV บน train)",
"""""",
"""
kcv = KFold(5, shuffle=True, random_state=1992)
def cv_rmse(model):
    return -cross_validate(model, X_train, y_train, cv=kcv, scoring="neg_root_mean_squared_error")["test_score"].mean()
print("KNN raw k=5   :", round(cv_rmse(KNeighborsRegressor(5)), 0))
print("KNN scaled k=5:", round(cv_rmse(Pipeline([("sc", StandardScaler()), ("knn", KNeighborsRegressor(5))])), 0))
print("Linear        :", round(cv_rmse(LinearRegression()), 0))
g = GridSearchCV(Pipeline([("sc", StandardScaler()), ("knn", KNeighborsRegressor())]),
                 {"knn__n_neighbors": range(1, 31), "knn__weights": ["uniform", "distance"]},
                 cv=kcv, scoring="neg_root_mean_squared_error").fit(X_train, y_train)
print("best:", g.best_params_, "CV RMSE", round(-g.best_score_, 0))
rows.append(metrics(f"KNN tuned k={g.best_params_['knn__n_neighbors']}", g.best_estimator_))
print(pd.DataFrame(rows).round(3).to_string(index=False))
""",
"""KNN tuned test RMSE {rows[2]['RMSE']:,.0f} · R² {rows[2]['R2']:.3f} เทียบ Linear {rows[1]['RMSE']:,.0f} / {rows[1]['R2']:.3f}"""),
Step("ทำนายลูกค้าใหม่",
"""""",
"""
new = pd.DataFrame([{"age": 40, "bmi": 30.0, "children": 2, "sex_male": 1, "smoker_yes": 1,
                     "region_northwest": 0, "region_southeast": 1, "region_southwest": 0}])[X.columns]
print("Linear:", round(lin.predict(new)[0], 0), "| KNN:", round(g.best_estimator_.predict(new)[0], 0))
new_ns = new.assign(smoker_yes=0)
print("ถ้าไม่สูบ — Linear:", round(lin.predict(new_ns)[0], 0))
""",
"""ต่างกันระหว่างสูบ/ไม่สูบใน Linear = coefficient ของ smoker_yes พอดี ({coef['smoker_yes']:,.0f}) — เพราะเป็นโมเดลเชิงเส้น"""),
]
P7_OUT = """
## ✅ สรุปคำตอบ
{md_table(pd.DataFrame(rows).round(3))}

**ตีความ:** smoker เป็นปัจจัยใหญ่สุด · Linear ตีความง่าย · KNN ต้อง scale (ไม่ scale RMSE แย่มาก) · เลือกโมเดลตาม RMSE บน test + ความต้องการอธิบายผล

> [!question]- ลองเองต่อ
> 1. เพิ่ม feature `smoker_yes × bmi` (สูบ + อ้วน) ใน Linear แล้วดู R² (ความสัมพันธ์แบบ interaction)
> 2. ทำนาย log(charges) แทน charges แล้วเทียบ RMSE (หลังแปลงกลับ)
"""

# ════════════════════════════════════════════════════════════════════════════════════════════
P8 = [
Step("Import + เตรียมข้อมูล (ไม่ใช้ label)",
"""จัดกลุ่มไวน์ 178 ขวดจากเคมี 13 ค่า · **ตัด `cultivar` ออก** (เก็บไว้ตรวจทีหลังเท่านั้น)""",
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.decomposition import PCA

wine = pd.read_csv("data/p8_wine_unlabeled.csv")
truth = wine.pop("cultivar")
scaler = StandardScaler().fit(wine)
Z = scaler.transform(wine)
print(wine.shape, "| scaled mean≈0:", Z.mean(axis=0).round(2)[:4], "std≈1:", Z.std(axis=0).round(2)[:4])
""",
"""13 feature standardize แล้ว · ถ้าไม่ scale proline (หลักพัน) จะครองระยะทาง"""),
Step("K-Means k = 2…8: WCSS, silhouette, Davies–Bouldin",
"""""",
"""
rows = []
for k in range(2, 9):
    km = KMeans(n_clusters=k, n_init=20, random_state=1992).fit(Z)
    rows.append({"k": k, "WCSS": round(km.inertia_, 1), "silhouette": round(silhouette_score(Z, km.labels_), 4),
                 "DB": round(davies_bouldin_score(Z, km.labels_), 4)})
ks = pd.DataFrame(rows)
print(ks.to_string(index=False))
fig, ax = plt.subplots(1, 2, figsize=(10, 3.5))
ax[0].plot(ks.k, ks.WCSS, "o-"); ax[0].set_title("Elbow (WCSS)"); ax[0].set_xlabel("k")
ax[1].plot(ks.k, ks.silhouette, "o-", color="tab:red"); ax[1].set_title("Silhouette"); ax[1].set_xlabel("k")
best_k = int(ks.loc[ks.silhouette.idxmax(), "k"])
""",
"""silhouette สูงสุดที่ **k = {best_k}** ({ks.silhouette.max():.4f}) · elbow เห็นการหักชัดที่ k = 3 · DB ต่ำสุดที่ k = {int(ks.loc[ks.DB.idxmin(),'k'])}"""),
Step("K-Means k = 3 + profile ของกลุ่ม",
"""ดูค่าเฉลี่ยของแต่ละกลุ่มในหน่วยเดิม + z-score ของ centroid""",
"""
km3 = KMeans(n_clusters=3, n_init=20, random_state=1992).fit(Z)
lab = km3.labels_
print("ขนาดกลุ่ม:", np.bincount(lab))
prof = wine.groupby(lab)[["alcohol", "flavanoids", "color_intensity", "proline", "malic_acid", "hue"]].mean().round(2)
print(prof)
zc = pd.DataFrame(km3.cluster_centers_, columns=wine.columns)[["alcohol", "flavanoids", "color_intensity", "proline", "hue"]].round(2)
print(zc)
""",
"""ตั้งชื่อกลุ่มจาก z-score ที่โดดเด่น (|z| > ~0.8):
- **กลุ่ม 2** ({np.bincount(lab)[2]} ขวด): proline z = {zc.proline[2]:+.2f} · alcohol {zc.alcohol[2]:+.2f} · flavanoids {zc.flavanoids[2]:+.2f} → **"เข้มข้น แอลกอฮอล์สูง proline สูง"**
- **กลุ่ม 1** ({np.bincount(lab)[1]} ขวด): flavanoids {zc.flavanoids[1]:+.2f} · hue {zc.hue[1]:+.2f} · color {zc.color_intensity[1]:+.2f} → **"สีเข้ม flavanoids ต่ำ"**
- **กลุ่ม 0** ({np.bincount(lab)[0]} ขวด): alcohol {zc.alcohol[0]:+.2f} · color {zc.color_intensity[0]:+.2f} · proline {zc.proline[0]:+.2f} → **"เบา สีอ่อน แอลกอฮอล์ต่ำ"**"""),
Step("ดูภาพบน PCA 2D",
"""""",
"""
pca = PCA(n_components=2).fit(Z)
P = pca.transform(Z)
plt.figure(figsize=(6, 5))
plt.scatter(P[:, 0], P[:, 1], c=lab, cmap="viridis", s=18)
C2 = pca.transform(km3.cluster_centers_)
plt.scatter(C2[:, 0], C2[:, 1], marker="X", s=200, c="red")
plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.0%})"); plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.0%})")
plt.title("K-Means k=3 on PCA")
""",
"""PC1+PC2 = {pca.explained_variance_ratio_.sum():.1%} · 3 กลุ่มแยกกันชัดในภาพ (separation ดี)"""),
Step("ตรวจกับ label จริง (เฉพาะเพื่อเช็ก — ในงานจริงไม่มี label)",
"""""",
"""
print(pd.crosstab(pd.Series(lab, name="cluster"), truth))
match = pd.crosstab(lab, truth).max(axis=1).sum() / len(truth)
print("สัดส่วนที่ตรงกับสายพันธุ์จริง:", round(match, 4))
""",
"""แต่ละ cluster ตรงกับ cultivar หนึ่งเกือบทั้งหมด → **{match:.1%}** ตรง · แปลว่าเคมีของไวน์แบ่งตามสายพันธุ์ได้เองโดยไม่ต้องบอก label"""),
Step("จัดกลุ่มไวน์ขวดใหม่",
"""ต้อง transform ด้วย **scaler ตัวเดิม** ก่อน predict""",
"""
new = wine.iloc[[0]].copy()
new["alcohol"] = 13.0; new["proline"] = 600
print(new[["alcohol", "proline", "flavanoids"]])
print("cluster:", km3.predict(scaler.transform(new))[0])
""",
"""ได้ cluster **{km3.predict(scaler.transform(new))[0]}**"""),
]
P8_OUT = """
## ✅ สรุปคำตอบ
{md_table(ks)}

**k ที่เลือก = 3** (silhouette สูงสุด + elbow + ตีความได้) · ตรงกับสายพันธุ์ {match:.1%}
**cohesion:** WCSS ที่ k = 3 = {ks.WCSS[1]} · **separation:** กลุ่มแยกกันใน PCA plot · **interpretability:** profile ต่างกันชัด

> [!question]- ลองเองต่อ
> 1. รัน K-Means **โดยไม่ scale** แล้วดู crosstab กับ cultivar — แย่ลงเท่าไร เพราะอะไร
> 2. ใช้ `init="random", n_init=1` หลาย random_state แล้วดูว่า WCSS เปลี่ยนไหม (local optimum)
"""

# ════════════════════════════════════════════════════════════════════════════════════════════
P9 = [
Step("อ่านตะกร้าและแปลงเป็นตาราง True/False",
"""ไฟล์เป็น "1 บรรทัด = 1 ตะกร้า" รายการคั่นด้วย comma (จำนวนไม่เท่ากัน) → อ่านเป็น list แล้วใช้ TransactionEncoder""",
"""
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
""",
"""{len(baskets):,} ตะกร้า · {items.shape[1]} สินค้า · เฉลี่ย {items.sum(axis=1).mean():.2f} ชิ้นต่อตะกร้า"""),
Step("สินค้าขายดี (support ของ 1 item)",
"""""",
"""
top = items.mean().sort_values(ascending=False).head(10).round(4)
print(top)
top.plot.barh(figsize=(6, 4), title="Top 10 items (support)").invert_yaxis()
""",
"""whole milk อยู่ใน **{top.iloc[0]:.1%}** ของตะกร้า · ระวัง: สินค้าขายดีจะโผล่เป็น consequent ของกฎจำนวนมาก (confidence สูงเพราะฐานสูง)"""),
Step("Frequent itemsets (Apriori, min support 2%)",
"""""",
"""
freq = apriori(items, min_support=0.02, use_colnames=True)
freq["size"] = freq["itemsets"].apply(len)
print("frequent itemsets:", len(freq), "| แยกตามขนาด:", freq["size"].value_counts().sort_index().to_dict())
print(freq[freq["size"] == 2].sort_values("support", ascending=False).head(5))
""",
"""ได้ {len(freq)} itemsets · คู่ที่พบบ่อยที่สุดมี whole milk เกือบทั้งหมด"""),
Step("สร้างกฎ (min confidence 30%) แล้วเรียงด้วย lift",
"""""",
"""
rules = association_rules(freq, metric="confidence", min_threshold=0.3)
rules = rules.sort_values("lift", ascending=False)
show = rules[["antecedents", "consequents", "support", "confidence", "lift"]].round(3)
print(len(rules), "rules")
print(show.head(8).to_string(index=False))
r1 = rules.iloc[0]
""",
"""กฎ lift สูงสุด: **{set(r1.antecedents)} → {set(r1.consequents)}** · support {r1.support:.3f} · confidence {r1.confidence:.3f} · lift **{r1.lift:.2f}**"""),
Step("ตีความกฎ + หากฎที่ lift < 1",
"""""",
"""
print(f"support {r1.support:.1%} | confidence {r1.confidence:.1%} | lift {r1.lift:.2f}")
print("กฎ conf>=30% ที่ lift < 1:", int((rules["lift"] < 1).sum()))
loose = association_rules(freq, metric="confidence", min_threshold=0.1)       # ลด conf เพื่อหาตัวอย่าง
low = loose[loose["lift"] < 1].sort_values("lift")[["antecedents", "consequents", "confidence", "lift"]].round(3)
print("กฎ conf>=10% ที่ lift < 1:", len(low))
print(low.head().to_string(index=False))
""",
"""**อ่านกฎอันดับ 1:** {r1.support:.1%} ของทุกตะกร้ามีสินค้าทั้งสองฝั่ง · ในตะกร้าที่มี {set(r1.antecedents)} มี {r1.confidence:.1%} ที่มี {set(r1.consequents)} ด้วย · มากกว่าโอกาสทั่วไป {r1.lift:.2f} เท่า → วางใกล้กัน/จัดโปร
ที่ conf ≥ 30% ไม่มีกฎ lift < 1 · พอลด conf เหลือ 10% เจอ **{len(low)} กฎ** ที่ lift < 1 เช่น {set(low.iloc[0].antecedents)} → {set(low.iloc[0].consequents)} (conf {low.iloc[0].confidence:.1%}, lift {low.iloc[0].lift:.2f}) = ซื้อด้วยกัน **น้อยกว่า** บังเอิญ — ห้ามใช้ทำโปร"""),
Step("ผลของ min support (FP-Growth เร็วกว่า ผลเหมือนกัน)",
"""""",
"""
comp = []
for ms in [0.01, 0.02, 0.05]:
    f = fpgrowth(items, min_support=ms, use_colnames=True)
    r = association_rules(f, metric="confidence", min_threshold=0.3) if len(f) else []
    comp.append({"min_support": ms, "itemsets": len(f), "rules": len(r)})
cmp = pd.DataFrame(comp)
print(cmp.to_string(index=False))
""",
"""min support ↑ → itemsets และกฎ ↓ อย่างรวดเร็ว · 0.05 แทบไม่เหลือกฎ · 0.01 ได้กฎเยอะแต่บางกฎมาจากไม่กี่ร้อยตะกร้า"""),
]
P9_OUT = """
## ✅ สรุปคำตอบ
| คำถาม | คำตอบ |
|---|---|
| สินค้าขายดีสุด | whole milk ({top.iloc[0]:.1%}) |
| frequent itemsets (minsup 2%) | {len(freq)} |
| กฎ (conf ≥ 30%) | {len(rules)} กฎ (lift < 1: 0 กฎ · ถ้า conf ≥ 10% มี lift < 1 อยู่ {len(low)} กฎ) |
| กฎ lift สูงสุด | {set(r1.antecedents)} → {set(r1.consequents)} (s {r1.support:.3f}, c {r1.confidence:.3f}, lift {r1.lift:.2f}) |

{md_table(cmp)}

> [!question]- ลองเองต่อ
> 1. เลือกเฉพาะกฎที่ consequent = {{'whole milk'}} แล้วเรียงด้วย lift — กฎไหนน่าทำโปรมากสุด
> 2. ตั้ง min_confidence = 0.5 แล้วดูว่าเหลือกี่กฎ
"""

if __name__ == "__main__":
    build("p6", "Decision Tree vs Random Forest", header(6, "Decision Tree vs Random Forest", "โรงพยาบาลต้องการทำนายโรคหัวใจจากผลตรวจ 13 ค่า จงแสดง overfitting ของ tree ที่โตเต็ม หาความลึกที่เหมาะด้วย CV เปรียบเทียบกับ Random Forest และบอก feature ที่สำคัญ",
          "`data/p6_heart.csv` (UCI Heart Disease Cleveland, 303 คน)", "> 1. ดูข้อมูล + split 2. tree โตเต็ม (overfit) 3. depth curve 4. grid search tree 5. วาด tree 6. RF default/tuned 7. importance + ตารางเทียบ",
          40, "[[LAB 05 Supervised Models#5.4 Decision Tree ⭐⭐⭐]] · [[LEC 08 Decision Trees & Random Forest]]"), P6, P6_OUT, "PR 06 Decision Tree vs Random Forest (Python).md")
    build("p7", "Regression", header(7, "Regression", "บริษัทประกันต้องการประมาณค่ารักษาพยาบาลรายปีของลูกค้า จงสร้าง mean baseline, Linear Regression (ตีความ coefficient) และ KNN regressor (ก่อน/หลัง scale, optimize k) แล้วรายงาน MAE / RMSE / R²",
          "`data/p7_insurance.csv` (Medical Cost Personal, 1,338 คน)", "> 1. EDA ของ charges 2. encode + split 3. baseline vs linear 4. ตีความ coefficient 5. KNN regressor + optimize 6. ทำนายลูกค้าใหม่",
          40, "[[LAB 05 Supervised Models#5.2 Linear Regression ⭐⭐⭐]] · [[LEC 05 Model Construction & Evaluation#5.8 Regression Metrics ⭐⭐⭐]]"), P7, P7_OUT, "PR 07 Regression (Python).md")
    build("p8", "K-Means Clustering", header(8, "K-Means Clustering", "โรงบ่มไวน์ได้ไวน์ 178 ขวดที่ไม่รู้สายพันธุ์ จงจัดกลุ่มด้วย K-Means เลือกจำนวนกลุ่มด้วย elbow/silhouette/DB อธิบายลักษณะแต่ละกลุ่ม แสดงบน PCA และจัดกลุ่มไวน์ขวดใหม่",
          "`data/p8_wine_unlabeled.csv` (UCI Wine — คอลัมน์ cultivar ใช้ตรวจคำตอบเท่านั้น)", "> 1. เตรียมข้อมูล + scale 2. k = 2…8 3. profile k = 3 4. PCA plot 5. เทียบสายพันธุ์จริง 6. ขวดใหม่",
          35, "[[LAB 06 Clustering & Association#6.2 K-Means + เลือกจำนวน cluster ⭐⭐⭐]] · [[LEC 09 Clustering]]"), P8, P8_OUT, "PR 08 K-Means Clustering (Python).md")
    build("p9", "Association Rules", header(9, "Association Rules", "ซูเปอร์มาร์เก็ตมีใบเสร็จ 9,835 ใบ จงหาสินค้าที่ขายดี frequent itemsets และกฎความสัมพันธ์ ตีความ support / confidence / lift ของกฎที่ดีที่สุด และศึกษาผลของ min support",
          "`data/p9_groceries_baskets.csv` (Groceries — 1 บรรทัด = 1 ตะกร้า)", "> 1. อ่าน + one-hot 2. สินค้าขายดี 3. Apriori minsup 2% 4. rules + lift 5. ตีความ + lift < 1 6. ผลของ min support",
          30, "[[LAB 06 Clustering & Association#6.3 Association Rules ⭐⭐⭐]] · [[LEC 10 Association Rules]]"), P9, P9_OUT, "PR 09 Association Rules (Python).md")
