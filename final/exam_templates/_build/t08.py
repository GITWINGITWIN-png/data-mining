from nbtools import md, code, build

TITLE = r"""
# T08 · Decision Tree & Random Forest (Gini/Entropy/Gain · Tree construction · Rules · Overfitting · Parameters · RF)

**ใช้เมื่อโจทย์ถาม:** คำนวณ Gini / Entropy / Information Gain / Gain Ratio เลือก root · สร้างต้นไม้ + วาด + เขียนกฎ IF-THEN ·
feature importance · overfitting (train vs test, ปรับ max_depth / min_samples_leaf) · criterion gini vs entropy ·
Random Forest (n_estimators, max_features) · tune + เทียบ DT vs RF vs baseline · ทำนายข้อมูลใหม่ + อธิบายเส้นทาง

| ขั้น | ทำอะไร |
|---|---|
| 1 | แก้ **⚙️ CONFIG** · Run All |
| 2 | §0 = คำนวณ impurity ด้วยมือ (ข้อมูลเล็ก เช่น weather) — config แยกในเซลล์ |

> Tree/RF **ไม่ต้อง scale** (แบ่งตาม threshold ไม่ใช่ระยะทาง) · RapidMiner Decision Tree default = **gain_ratio** + pruning · sklearn = **gini** ไม่ prune
"""

CONFIG = r'''# ════════ ⚙️ CONFIG — แก้ cell นี้ให้ตรงโจทย์ ════════
DATA_PATH = "../practice/data/p6_heart.csv"
TARGET    = "target"
POS_LABEL = 1
ID_COL    = None
DROP_COLS = []
CRITERION = "gini"          # "gini" | "entropy" (= information gain)
MAX_DEPTH = 3               # ความลึกที่โจทย์กำหนด (None = โตจนสุด)
MIN_LEAF  = 1               # min_samples_leaf
N_TREES   = 100             # Random Forest n_estimators
NEW_DATA  = None            # dict ข้อมูลใหม่ / path .csv · None = ใช้แถวแรกของ test เป็นตัวอย่าง
EVAL_MODE = "cv"
SCALE     = None            # tree ไม่ต้อง scale
TEST_SIZE, N_FOLDS, SEED = 0.2, 5, 42
MISSING_MARKERS, SHEET, CSV_SEP = ["?", "", " ", "NA"], 0, ","
'''

S = [
md(r"""
## §0 คำนวณ impurity ด้วยมือ — เลือก attribute ที่ดีที่สุดเป็น root
- $Entropy = -\sum p_j \log_2 p_j$ · $Gini = 1-\sum p_j^2$
- **Information Gain** = Entropy(parent) − Σ (n_k/n)·Entropy(child_k)
- **Gain Ratio** = Gain / SplitInfo, $SplitInfo = -\sum \frac{n_k}{n}\log_2\frac{n_k}{n}$ (ลงโทษ attribute ที่มีหลายค่า)
- **Gini gain** = Gini(parent) − Σ (n_k/n)·Gini(child_k)
- attribute ตัวเลข → ลองทุกจุดตัด (ค่ากึ่งกลาง) แบบ binary `≤ t / > t`
"""),
code(r'''IMP_PATH   = "../data/weather.csv"      # ✏️ ข้อมูลเล็กที่โจทย์ให้คำนวณมือ (ใช้ DATA_PATH ก็ได้)
IMP_TARGET = "Class"                    # ✏️
IMP_DROP   = []                         # ✏️ เช่น ["Tid"]

def entropy(s):
    p = s.value_counts(normalize=True); return float(-(p * np.log2(p)).sum())
def gini(s):
    p = s.value_counts(normalize=True); return float(1 - (p ** 2).sum())

def split_scores(d, attr, target):
    n = len(d); parts = []
    if pd.api.types.is_numeric_dtype(d[attr]) and d[attr].nunique() > 4:
        vals = np.sort(d[attr].unique()); best = None
        for t in (vals[:-1] + vals[1:]) / 2:
            g = d[target].groupby(d[attr] <= t)
            w_gini = sum(len(s) / n * gini(s) for _, s in g)
            if best is None or w_gini < best[1]:
                best = (t, w_gini)
        t = best[0]; groups = {f"<= {t:g}": d[d[attr] <= t][target], f"> {t:g}": d[d[attr] > t][target]}
    else:
        groups = {str(k): s for k, s in d.groupby(attr)[target]}
    w_ent = sum(len(s) / n * entropy(s) for s in groups.values())
    w_gini = sum(len(s) / n * gini(s) for s in groups.values())
    split_info = -sum(len(s) / n * np.log2(len(s) / n) for s in groups.values())
    gain = entropy(d[target]) - w_ent
    detail = "; ".join(f"{k}: { {c: int(v) for c, v in s.value_counts().items()} } E={abs(entropy(s)):.3f} G={gini(s):.3f}" for k, s in groups.items())
    return {"attribute": attr, "weighted_entropy": w_ent, "info_gain": gain, "split_info": split_info,
            "gain_ratio": gain / split_info if split_info > 0 else 0, "weighted_gini": w_gini,
            "gini_gain": gini(d[target]) - w_gini, "children": detail}

imp = load_data(IMP_PATH).drop(columns=IMP_DROP, errors="ignore")
print(f"parent: { {c: int(v) for c, v in imp[IMP_TARGET].value_counts().items()} } → Entropy = {entropy(imp[IMP_TARGET]):.4f} · Gini = {gini(imp[IMP_TARGET]):.4f}")
imp_tab = pd.DataFrame([split_scores(imp, a, IMP_TARGET) for a in imp.columns if a != IMP_TARGET])
display(imp_tab.drop(columns="children").sort_values("info_gain", ascending=False))
for _, r in imp_tab.iterrows():
    print(f"  {r['attribute']}: {r['children']}")
print(f"✍️ root ตาม Information Gain = {imp_tab.loc[imp_tab.info_gain.idxmax(), 'attribute']} · "
      f"ตาม Gain Ratio = {imp_tab.loc[imp_tab.gain_ratio.idxmax(), 'attribute']} · ตาม Gini = {imp_tab.loc[imp_tab.gini_gain.idxmax(), 'attribute']}")'''),
md(r"""**✍️ คำตอบ §0:** Entropy(parent) = … · Gain(…) = … สูงสุด → เลือก … เป็น root · (Gain ratio / Gini ให้ผล … เหมือน/ต่าง เพราะ …)"""),

md(r"""## §1 โหลด + split"""),
code(r'''df = load_data(DATA_PATH)
check(df, TARGET)
X, y = make_xy(df)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, stratify=y, random_state=SEED)
cv = get_cv()
print(f"train {X_train.shape} | test {X_test.shape}")'''),

md(r"""## §2 Decision Tree (ตามที่โจทย์กำหนด) → วาดต้นไม้ + กฎ IF-THEN + feature importance"""),
code(r'''tree = make_pipe(DecisionTreeClassifier(criterion=CRITERION, max_depth=MAX_DEPTH, min_samples_leaf=MIN_LEAF, random_state=SEED), X_train, scale=None)
tree.fit(X_train, y_train)
fn = list(tree.named_steps["prep"].get_feature_names_out())
dt = tree.named_steps["model"]
cls_names = [str(c) for c in dt.classes_]
print(f"ความลึก = {dt.get_depth()} · จำนวนใบ = {dt.get_n_leaves()}")
print(f"train accuracy = {accuracy_score(y_train, tree.predict(X_train)):.4f} · test accuracy = {accuracy_score(y_test, tree.predict(X_test)):.4f}")
plt.figure(figsize=(min(24, 4 + 3 * 2 ** min(dt.get_depth(), 4)), 2.2 * dt.get_depth() + 2))
plot_tree(dt, feature_names=fn, class_names=cls_names, filled=True, rounded=True, fontsize=8, impurity=True, proportion=False)
plt.title(f"Decision Tree ({CRITERION}, max_depth={MAX_DEPTH})"); plt.show()
print(export_text(dt, feature_names=fn, show_weights=True))'''),
code(r'''# กฎ IF-THEN จากทุกใบ (path จาก root → leaf)
from sklearn.tree import _tree
def tree_rules(dt, fn):
    t = dt.tree_; rules = []
    def walk(node, conds):
        if t.feature[node] == _tree.TREE_UNDEFINED:
            v = t.value[node][0]; k = int(np.argmax(v))
            rules.append({"rule": "IF " + (" AND ".join(conds) or "TRUE") + f" THEN {dt.classes_[k]}",
                          "samples": int(t.n_node_samples[node]), "confidence": float(v[k] / v.sum())})
            return
        f, th = fn[t.feature[node]], t.threshold[node]
        walk(t.children_left[node], conds + [f"{f} <= {th:.3f}"]); walk(t.children_right[node], conds + [f"{f} > {th:.3f}"])
    walk(0, []); return pd.DataFrame(rules).sort_values("samples", ascending=False)
with pd.option_context("display.max_colwidth", 200):
    display(tree_rules(dt, fn))
fi = pd.Series(dt.feature_importances_, index=fn).sort_values(ascending=False)
display(fi[fi > 0].to_frame("importance"))
print(f"✍️ root node = {fn[dt.tree_.feature[0]]} (threshold {dt.tree_.threshold[0]:.3f}) · feature สำคัญสุด: {', '.join(fi.index[:3])}")'''),
md(r"""**✍️ คำตอบ §2:** root = … · กฎหลัก: IF … AND … THEN … (… ตัวอย่าง, confidence …) · feature สำคัญสุด …"""),

md(r"""
## §3 Overfitting — train vs CV accuracy ตาม max_depth
ต้นไม้ลึก → train ~100% แต่ CV ต่ำ = **overfit** (จำ noise) · แก้: จำกัด max_depth, เพิ่ม min_samples_leaf, pruning (ccp_alpha), ใช้ RF
"""),
code(r'''depths = list(range(1, 16))
dc = []
for d in depths:
    r = cross_validate(make_pipe(DecisionTreeClassifier(criterion=CRITERION, max_depth=d, random_state=SEED), X, scale=None),
                       X, y, cv=cv, scoring=cls_scoring(y), return_train_score=True)
    dc.append({"max_depth": d, "train_acc": r["train_accuracy"].mean(), "cv_acc": r["test_accuracy"].mean(), "cv_f1": r["test_f1"].mean()})
r = cross_validate(make_pipe(DecisionTreeClassifier(criterion=CRITERION, random_state=SEED), X, scale=None), X, y, cv=cv, scoring=cls_scoring(y), return_train_score=True)
dc.append({"max_depth": "None (full)", "train_acc": r["train_accuracy"].mean(), "cv_acc": r["test_accuracy"].mean(), "cv_f1": r["test_f1"].mean()})
dc = pd.DataFrame(dc); dc["gap"] = dc.train_acc - dc.cv_acc
display(dc.round(4))
plt.figure(figsize=(8, 3.6)); plt.plot(depths, dc.train_acc[:-1], "o-", label="train"); plt.plot(depths, dc.cv_acc[:-1], "o-", label="CV")
plt.xlabel("max_depth"); plt.ylabel("accuracy"); plt.title("Overfitting curve"); plt.legend(); plt.show()
bd = dc.iloc[:-1].loc[dc.iloc[:-1].cv_acc.idxmax()]
full = dc.iloc[-1]
print(f"✍️ ต้นไม้เต็ม: train {full.train_acc:.4f} vs CV {full.cv_acc:.4f} (gap {full.gap:.4f}) → overfit · ความลึกที่ดีสุด = {bd.max_depth} (CV acc {bd.cv_acc:.4f})")'''),

md(r"""## §4 Tune Decision Tree (GridSearchCV: max_depth × min_samples_leaf × criterion)"""),
code(r'''g_dt = GridSearchCV(make_pipe(DecisionTreeClassifier(random_state=SEED), X, scale=None),
                    {"model__max_depth": [2, 3, 4, 5, 6, 8, 10, None], "model__min_samples_leaf": [1, 2, 5, 10, 20],
                     "model__criterion": ["gini", "entropy"]}, cv=cv, scoring=cls_scoring(y), refit="f1", n_jobs=-1).fit(X, y)
print("best:", g_dt.best_params_, "| CV F1 =", round(g_dt.best_score_, 4)); display(top_k(g_dt, 8))'''),

md(r"""
## §5 Random Forest (bagging หลายต้น + สุ่ม feature ทุก split → variance ต่ำกว่า, overfit น้อยกว่า)
พารามิเตอร์: `n_estimators` (จำนวนต้น) · `max_features` (feature ที่สุ่มต่อ split: "sqrt") · `max_depth` · `min_samples_leaf`
"""),
code(r'''rf = make_pipe(RandomForestClassifier(n_estimators=N_TREES, random_state=SEED), X, scale=None)
g_rf = GridSearchCV(make_pipe(RandomForestClassifier(random_state=SEED), X, scale=None),
                    {"model__n_estimators": [100, 200], "model__max_depth": [None, 5, 10],
                     "model__min_samples_leaf": [1, 3, 5], "model__max_features": ["sqrt", None]},
                    cv=cv, scoring=cls_scoring(y), refit="f1", n_jobs=-1).fit(X, y)
print("RF best:", g_rf.best_params_, "| CV F1 =", round(g_rf.best_score_, 4)); display(top_k(g_rf, 5))
# ผลของจำนวนต้น
nt = []
for n in [1, 5, 10, 25, 50, 100, 200, 400]:
    r = cross_validate(make_pipe(RandomForestClassifier(n_estimators=n, random_state=SEED), X, scale=None), X, y, cv=cv, scoring="accuracy", n_jobs=-1)
    nt.append({"n_estimators": n, "cv_acc": r["test_score"].mean()})
nt = pd.DataFrame(nt); display(nt.T.round(4))
plt.figure(figsize=(6, 3)); plt.plot(nt.n_estimators, nt.cv_acc, "o-"); plt.xscale("log"); plt.xlabel("n_estimators"); plt.ylabel("CV acc"); plt.title("RF: number of trees"); plt.show()'''),

md(r"""## §6 เปรียบเทียบ baseline vs DT vs RF (ก่อน/หลัง optimize) ⭐"""),
code(r'''rows = [evaluate("Majority baseline", DummyClassifier(strategy="most_frequent"), X, y, cv, train=True),
        evaluate("Decision Tree (full)", make_pipe(DecisionTreeClassifier(criterion=CRITERION, random_state=SEED), X, scale=None), X, y, cv, "no limit", train=True),
        evaluate(f"Decision Tree (depth={MAX_DEPTH})", make_pipe(DecisionTreeClassifier(criterion=CRITERION, max_depth=MAX_DEPTH, min_samples_leaf=MIN_LEAF, random_state=SEED), X, scale=None), X, y, cv, "โจทย์กำหนด", train=True),
        evaluate("Decision Tree tuned", g_dt.best_estimator_, X, y, cv, str(g_dt.best_params_), train=True),
        evaluate(f"Random Forest ({N_TREES})", rf, X, y, cv, "default", train=True),
        evaluate("Random Forest tuned", g_rf.best_estimator_, X, y, cv, str(g_rf.best_params_), train=True)]
cmp_t = results_table(rows)
say_compare(cmp_t, "f1", "Majority baseline")
best_rf = g_rf.best_estimator_.fit(X_train, y_train)
fi_rf = pd.Series(best_rf.named_steps["model"].feature_importances_, index=best_rf.named_steps["prep"].get_feature_names_out()).sort_values(ascending=False)
fi_rf.head(15).plot(kind="barh", figsize=(6, 4), title="Random Forest feature importance"); plt.gca().invert_yaxis(); plt.show()
print("RF tuned บน test:"); show_cm(y_test, best_rf.predict(X_test), "RF tuned (test)")'''),
md(r"""**✍️ คำตอบ §6:** ต้นไม้เต็ม train … CV … → overfit · จำกัด depth = … ได้ CV F1 … · RF ได้ … ดีกว่า/ใกล้ DT เพราะเฉลี่ยหลายต้นลด variance · feature สำคัญ (RF) = …"""),

md(r"""## §7 ทำนายข้อมูลใหม่ + อธิบายเส้นทางในต้นไม้"""),
code(r'''nd = align_new(new_data(NEW_DATA), X) if NEW_DATA is not None else X_test.iloc[[0]]
out = nd.copy()
out["DT pred"] = tree.predict(nd); out["DT P(1)"] = tree.predict_proba(nd)[:, -1]
out["RF pred"] = best_rf.predict(nd); out["RF P(1)"] = best_rf.predict_proba(nd)[:, -1]
display(out)
xr = tree.named_steps["prep"].transform(nd.iloc[[0]])
path = dt.decision_path(xr).indices
steps = []
for node in path:
    if dt.tree_.children_left[node] == -1:
        v = dt.tree_.value[node][0]; steps.append(f"→ leaf: class {dt.classes_[np.argmax(v)]} ({v.max() / v.sum():.1%})")
    else:
        f, th = dt.tree_.feature[node], dt.tree_.threshold[node]
        steps.append(f"{fn[f]} = {xr[0, f]:g} {'<=' if xr[0, f] <= th else '>'} {th:.3f}")
print("✍️ เส้นทาง:", " | ".join(steps))'''),
]

if __name__ == "__main__":
    build("../T08_decision_tree_rf.ipynb", TITLE, CONFIG, S)
