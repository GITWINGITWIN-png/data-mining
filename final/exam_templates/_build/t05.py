from nbtools import md, code, build

TITLE = r"""
# T05 · K-Nearest Neighbors (Distance · Classification · Regression · เลือก k · Scale ก่อน/หลัง)

**ใช้เมื่อโจทย์ถาม:** คำนวณระยะ (Euclidean / Manhattan / Minkowski) จากจุดใหม่ · หา k เพื่อนบ้านใกล้สุด + vote ·
KNN classification / regression · ผลของการ scale (ก่อน vs หลัง normalize) · เลือก k ที่ดีที่สุด (CV / Optimize) · ทำนายข้อมูลใหม่

| ขั้น | ทำอะไร |
|---|---|
| 1 | แก้ **⚙️ CONFIG** — `NEW_POINT` = ข้อมูลใหม่ที่โจทย์ให้ทำนาย, `K`, `METRIC` |
| 2 | Run All · §2 = คำนวณมือ (แสดงระยะทุกแถว) · §5 = เลือก k · §7 = KNN regression (config แยกในเซลล์) |
"""

CONFIG = r'''# ════════ ⚙️ CONFIG — แก้ cell นี้ให้ตรงโจทย์ ════════
DATA_PATH = "../data/riding_mowers.csv"
TARGET    = "Ownership"
POS_LABEL = "Owner"
ID_COL    = None
DROP_COLS = []
NEW_POINT = {"Income": 60, "Lot_Size": 20}   # ข้อมูลใหม่ (dict / list ของ dict / path .csv) · None = ข้าม
K         = 3              # k ที่โจทย์กำหนด
METRIC    = "euclidean"    # "euclidean" | "manhattan" | "minkowski" (ใช้ P_MINKOWSKI)
P_MINKOWSKI = 3
WEIGHTS   = "uniform"      # "uniform" = vote เท่ากัน | "distance" = ใกล้กว่าเสียงดังกว่า (1/d)
SCALE     = "standard"     # "standard" | "minmax" | None  (KNN ควร scale เสมอ)
K_MAX     = 25             # ลอง k = 1..K_MAX ตอนหา k ที่ดีที่สุด
EVAL_MODE = "cv"           # "cv" | "holdout"
N_FOLDS, TEST_SIZE, SEED = 5, 0.2, 42
MISSING_MARKERS, SHEET, CSV_SEP = ["?", "", " ", "NA"], 0, ","
'''

S = [
md(r"""## §1 โหลด + ภาพข้อมูล (2 feature แรก) + จุดใหม่"""),
code(r'''df = load_data(DATA_PATH)
check(df, TARGET)
X, y = make_xy(df)
new = align_new(new_data(NEW_POINT), X) if NEW_POINT is not None else None
nums = num_cols(X)
if len(nums) >= 2:
    fx, fy = nums[:2]                          # ✏️ เปลี่ยนคู่แกนที่จะวาดได้
    plt.figure(figsize=(6, 4.5))
    sns.scatterplot(x=X[fx], y=X[fy], hue=df.loc[X.index, TARGET], s=60)
    if new is not None:
        plt.scatter(new[fx], new[fy], marker="*", s=350, c="k", label="new point"); plt.legend()
    plt.title(f"{fy} vs {fx}"); plt.show()'''),

md(r"""
## §2 คำนวณระยะทางด้วยมือ → k เพื่อนบ้านใกล้สุด → vote
- Euclidean $d=\sqrt{\sum (x_i-q_i)^2}$ · Manhattan $d=\sum |x_i-q_i|$ · Minkowski $d=(\sum |x_i-q_i|^p)^{1/p}$
- ตารางแรก = **ไม่ scale** · ตารางที่สอง = **หลัง scale** (ใช้ค่า mean/std หรือ min/max จากข้อมูล train) → ดูว่าเพื่อนบ้านเปลี่ยนไหม
"""),
code(r'''def dist(A, q, metric=METRIC, p=P_MINKOWSKI):
    D = np.abs(A - q)
    if metric == "manhattan":
        return D.sum(axis=1)
    if metric == "minkowski":
        return (D ** p).sum(axis=1) ** (1 / p)
    return np.sqrt((D ** 2).sum(axis=1))

def neighbor_table(A, q, label, title):
    d = dist(A, q)
    t = pd.DataFrame(A, columns=feat_names, index=label.index).assign(**{TARGET: label.values, "distance": d})
    t = t.sort_values("distance"); t["rank"] = range(1, len(t) + 1)
    print(f"── {title} — {METRIC} ──"); display(t.head(max(K + 3, 6)).round(4))
    top = t.head(K)
    if WEIGHTS == "distance":
        w = 1 / top["distance"].replace(0, 1e-9); vote = w.groupby(top[TARGET]).sum().sort_values(ascending=False)
    else:
        vote = top[TARGET].value_counts()
    print(f"k = {K} เพื่อนบ้าน: {top[TARGET].tolist()} → vote { {k: round(float(v), 3) for k, v in vote.items()} } → ทำนาย = {vote.index[0]!r}")
    return t, vote.index[0]

if new is not None:
    prep_n = build_prep(X, scale=None).fit(X)                 # impute + one-hot (ไม่ scale)
    feat_names = list(prep_n.get_feature_names_out())
    A_raw, q_raw = prep_n.transform(X), prep_n.transform(new.iloc[[0]])[0]
    label = df.loc[X.index, TARGET]
    t_raw, pred_raw = neighbor_table(A_raw, q_raw, label, "ไม่ scale")

    prep_s = build_prep(X).fit(X)                             # impute + one-hot + scale ตาม SCALE
    A_s, q_s = prep_s.transform(X), prep_s.transform(new.iloc[[0]])[0]
    print("จุดใหม่หลัง scale:", {f: round(float(v), 4) for f, v in zip(feat_names, q_s)})
    t_s, pred_s = neighbor_table(A_s, q_s, label, f"scale = {SCALE}")
    print(f"✍️ จุดใหม่ {new.iloc[0].to_dict()} · k={K} · {METRIC}: ไม่ scale ทำนาย {pred_raw!r} / หลัง scale ทำนาย {pred_s!r}"
          + (" → เพื่อนบ้านเปลี่ยนเพราะตัวแปรหน่วยใหญ่ครอบงำระยะเมื่อไม่ scale" if pred_raw != pred_s else ""))'''),
md(r"""**✍️ คำตอบ §2:** ระยะจากจุดใหม่ถึงแถวที่ใกล้ที่สุด … คือ … · k = … เพื่อนบ้านเป็นคลาส … → ทำนาย … (vote …:…)"""),

md(r"""## §3 KNN แบบ hold-out (train/test) — scaler fit บน train เท่านั้น"""),
code(r'''X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, stratify=y, random_state=SEED)
knn = make_pipe(KNeighborsClassifier(n_neighbors=K, metric=METRIC, p=P_MINKOWSKI, weights=WEIGHTS), X)
row = evaluate_holdout(f"KNN k={K}", knn, X_train, y_train, X_test, y_test, settings=f"{METRIC}, {WEIGHTS}, {SCALE}")
results_table([evaluate_holdout("Majority baseline", DummyClassifier(), X_train, y_train, X_test, y_test), row])
show_cm(y_test, knn.predict(X_test), title=f"KNN k={K} (test)")'''),

md(r"""## §4 CV: baseline vs KNN ไม่ scale vs scale (เปรียบเทียบก่อน/หลัง preprocessing)"""),
code(r'''cv = get_cv()
def knn_model(k=K):
    return KNeighborsClassifier(n_neighbors=k, metric=METRIC, p=P_MINKOWSKI, weights=WEIGHTS)
rows = [evaluate("Majority baseline", DummyClassifier(strategy="most_frequent"), X, y, cv),
        evaluate(f"KNN k={K} ไม่ scale", make_pipe(knn_model(), X, scale=None), X, y, cv, "raw"),
        evaluate(f"KNN k={K} z-score", make_pipe(knn_model(), X, scale="standard"), X, y, cv, "standard"),
        evaluate(f"KNN k={K} min-max", make_pipe(knn_model(), X, scale="minmax"), X, y, cv, "minmax")]
t4 = results_table(rows)
say_compare(t4, "f1", "Majority baseline")'''),
md(r"""**✍️ คำตอบ §4:** KNN ไม่ scale ได้ … หลัง scale ได้ … → ดีขึ้นเพราะ KNN ใช้ระยะทาง ตัวแปรหน่วยใหญ่ไม่ครอบงำ · เหนือ baseline …"""),

md(r"""
## §5 เลือก k ที่ดีที่สุด (k-curve + GridSearchCV)
k เล็ก = เส้นแบ่งซับซ้อน → overfit (train สูง CV ต่ำ) · k ใหญ่ = เรียบเกิน → underfit · binary ควรใช้ k คี่ (กันเสมอ)
"""),
code(r'''ks = list(range(1, min(K_MAX, int(len(X) * (1 - 1 / N_FOLDS)) - 1) + 1))
curve = []
for k in ks:
    r = cross_validate(make_pipe(knn_model(k), X), X, y, cv=cv, scoring=cls_scoring(y), return_train_score=True)
    curve.append({"k": k, "train_acc": r["train_accuracy"].mean(), "cv_acc": r["test_accuracy"].mean(),
                  "cv_f1": r["test_f1"].mean(), "cv_recall": r["test_recall"].mean()})
curve = pd.DataFrame(curve)
best = curve.loc[curve["cv_f1"].idxmax()]
display(curve.round(4).style.highlight_max(subset=["cv_acc", "cv_f1"], color="#c8e6c9"))
plt.figure(figsize=(8, 3.8))
plt.plot(curve.k, curve.train_acc, "o-", label="train accuracy"); plt.plot(curve.k, curve.cv_acc, "o-", label="CV accuracy")
plt.plot(curve.k, curve.cv_f1, "s--", label="CV F1"); plt.axvline(best.k, color="gray", ls=":")
plt.xlabel("k"); plt.title("KNN: choosing k"); plt.legend(); plt.show()
print(f"✍️ k ที่ดีที่สุด (CV F1) = {int(best.k)} → F1 {best.cv_f1:.4f}, accuracy {best.cv_acc:.4f} · k=1 train acc {curve.train_acc.iloc[0]:.3f} vs CV {curve.cv_acc.iloc[0]:.3f} = overfit")

grid = GridSearchCV(make_pipe(KNeighborsClassifier(), X),
                    {"model__n_neighbors": ks, "model__weights": ["uniform", "distance"],
                     "model__metric": ["euclidean", "manhattan"]},
                    cv=cv, scoring=cls_scoring(y), refit="f1").fit(X, y)
print("GridSearch best:", grid.best_params_, "| CV F1 =", round(grid.best_score_, 4))
display(top_k(grid, 8))'''),
md(r"""**✍️ คำตอบ §5:** เลือก k = … (CV F1 …) · k น้อยเกินไป overfit (train … CV …) · k มากเกินไป underfit · ก่อน optimize (k=…) F1 … → หลัง … (+…)"""),

md(r"""## §6 โมเดลสุดท้าย → ทำนายข้อมูลใหม่ (probability = สัดส่วน vote)"""),
code(r'''final = grid.best_estimator_            # ✏️ หรือใช้ make_pipe(knn_model(K), X).fit(X, y) ถ้าโจทย์บังคับ k
final.fit(X, y)
results_table([evaluate("Majority baseline", DummyClassifier(), X, y, cv),
               evaluate(f"KNN k={K} (default)", make_pipe(knn_model(), X), X, y, cv),
               evaluate("KNN optimized", grid.best_estimator_, X, y, cv, str(grid.best_params_))])
if new is not None:
    proba = final.predict_proba(new)
    out = new.copy(); out["pred"] = final.predict(new)
    for i, c in enumerate(final.classes_):
        out[f"P(class={c})"] = proba[:, i]
    display(out)
    Aq = final.named_steps["prep"].transform(new.iloc[[0]])
    nn = NearestNeighbors(n_neighbors=final.named_steps["model"].n_neighbors,
                          metric=final.named_steps["model"].metric).fit(final.named_steps["prep"].transform(X))
    d_, idx = nn.kneighbors(Aq)
    print("เพื่อนบ้านของจุดใหม่ (แถวในข้อมูล):"); display(df.loc[X.index[idx[0]]].assign(distance=d_[0]))'''),
md(r"""**✍️ คำตอบ §6:** จุดใหม่ถูกทำนายเป็น … ความน่าจะเป็น … (เพื่อนบ้าน … จาก … เป็นคลาสนี้)"""),

md(r"""
## §7 KNN Regression (ทำนายตัวเลข = ค่าเฉลี่ยของ y ของ k เพื่อนบ้าน)
มี config แยกในเซลล์ — ใช้เมื่อโจทย์ให้ทำนายตัวเลขด้วย KNN · metric = MAE / RMSE / R² · เทียบกับ mean baseline
"""),
code(r'''REG_DATA_PATH = "../mock_lab/mock2_regression_pca/data/housing.csv"   # ✏️
REG_TARGET    = "medv"                                                # ✏️ target ตัวเลข
REG_DROP      = []                                                    # ✏️
REG_NEW       = None          # ✏️ dict ข้อมูลใหม่ · None = ข้าม
REG_K         = 5             # ✏️

rdf = load_data(REG_DATA_PATH)
Xr, yr = make_xy(rdf, target=REG_TARGET, drop=REG_DROP, task="regression")
cvr = get_cv("regression")
rrows = [evaluate_reg("Mean baseline", DummyRegressor(strategy="mean"), Xr, yr, cvr),
         evaluate_reg(f"KNN reg k={REG_K} ไม่ scale", make_pipe(KNeighborsRegressor(REG_K), Xr, scale=None), Xr, yr, cvr),
         evaluate_reg(f"KNN reg k={REG_K} z-score", make_pipe(KNeighborsRegressor(REG_K), Xr, scale="standard"), Xr, yr, cvr),
         evaluate_reg("Linear Regression", make_pipe(LinearRegression(), Xr), Xr, yr, cvr)]
rgrid = GridSearchCV(make_pipe(KNeighborsRegressor(), Xr), {"model__n_neighbors": range(1, 21), "model__weights": ["uniform", "distance"]},
                     cv=cvr, scoring="neg_root_mean_squared_error").fit(Xr, yr)
rrows.append(evaluate_reg("KNN reg optimized", rgrid.best_estimator_, Xr, yr, cvr, str(rgrid.best_params_)))
rt = results_table(rrows)
say_compare(rt, "RMSE", "Mean baseline", higher_is_better=False)
kc = pd.DataFrame(rgrid.cv_results_); kc = kc[kc.param_model__weights == "uniform"]
plt.figure(figsize=(7, 3.3)); plt.plot(kc.param_model__n_neighbors, -kc.mean_test_score, "o-"); plt.xlabel("k"); plt.ylabel("CV RMSE"); plt.title("KNN regression: RMSE vs k"); plt.show()
if REG_NEW is not None:
    print("ทำนาย:", rgrid.best_estimator_.predict(align_new(new_data(REG_NEW), Xr)))'''),
md(r"""**✍️ คำตอบ §7:** KNN regression (k = …) ได้ RMSE … R² … ดีกว่า mean baseline (RMSE …) · scale แล้ว RMSE ลดจาก … เป็น …"""),
]

if __name__ == "__main__":
    build("../T05_knn.ipynb", TITLE, CONFIG, S)
