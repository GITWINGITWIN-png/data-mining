from nbtools import md, code, build

TITLE = r"""
# T07 · Logistic Regression (Probability · Threshold · Coefficients / Odds ratio · Evaluation · ROC)

**ใช้เมื่อโจทย์ถาม:** ทำนายความน่าจะเป็น (predict_proba) · เปลี่ยน threshold (0.5 → 0.3) · confusion matrix แต่ละ threshold ·
สมการ logit / sigmoid · ตีความ coefficient / **odds ratio** $e^{b}$ · คำนวณ p ด้วยมือ · ROC/AUC · เทียบ baseline · tune C

| ขั้น | ทำอะไร |
|---|---|
| 1 | แก้ **⚙️ CONFIG** — `TARGET`, `POS_LABEL`, `THRESHOLD`, `NEW_DATA` |
| 2 | Run All · coefficient §3 · ตาราง threshold §5 |
"""

CONFIG = r'''# ════════ ⚙️ CONFIG — แก้ cell นี้ให้ตรงโจทย์ ════════
DATA_PATH = "../practice/data/p5_pima_diabetes.csv"
TARGET    = "diabetes"
POS_LABEL = 1                # คลาสที่สนใจ (= 1)
ID_COL    = None
DROP_COLS = []
FEATURES  = None             # list feature ที่โจทย์ให้ใช้ · None = ทั้งหมด
ZERO_AS_MISSING = ["glucose", "blood_pressure", "skin_thickness", "insulin", "bmi"]   # ข้อมูลอื่นใส่ []
THRESHOLD = 0.3              # threshold ที่โจทย์ให้ลอง (เทียบกับ 0.5)
THRESHOLDS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
NEW_DATA  = {"pregnancies": 2, "glucose": 150, "blood_pressure": 70, "skin_thickness": 30,
             "insulin": 100, "bmi": 32.0, "pedigree": 0.5, "age": 45}   # None = ข้าม
SCALE     = "standard"
TEST_SIZE, N_FOLDS, SEED = 0.2, 5, 42
MISSING_MARKERS, SHEET, CSV_SEP = ["?", "", " ", "NA"], 0, ","
'''

S = [
md(r"""## §1 โหลด + เตรียม X / y + split"""),
code(r'''df = load_data(DATA_PATH)
for c in ZERO_AS_MISSING:
    if c in df:
        print(f"{c}: 0 → NaN {int((df[c] == 0).sum())} ค่า"); df[c] = df[c].replace(0, np.nan)
check(df, TARGET)
X, y = make_xy(df)
if FEATURES:
    X = X[FEATURES]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, stratify=y, random_state=SEED)
print(f"train {X_train.shape} | test {X_test.shape} | สัดส่วน 1 ใน train {y_train.mean():.3f}")'''),

md(r"""
## §2 Fit + baseline (hold-out และ CV)
$p = P(y=1) = \dfrac{1}{1+e^{-(b_0+b_1x_1+\dots)}}$ · `predict()` = ทาย 1 ถ้า $p \ge 0.5$
"""),
code(r'''logit = make_pipe(LogisticRegression(max_iter=5000), X_train)
logit.fit(X_train, y_train)
rows = [evaluate_holdout("Majority baseline", DummyClassifier(strategy="most_frequent"), X_train, y_train, X_test, y_test),
        evaluate_holdout("Logistic Regression (t=0.5)", logit, X_train, y_train, X_test, y_test, settings=f"scale={SCALE}")]
print("── hold-out (test) ──"); ht = results_table(rows)
cv = get_cv()
print("── 5-fold CV ──")
ct = results_table([evaluate("Majority baseline", DummyClassifier(strategy="most_frequent"), X, y, cv),
                    evaluate("Logistic Regression", make_pipe(LogisticRegression(max_iter=5000), X), X, y, cv)])
say_compare(ct, "f1", "Majority baseline")
show_cm(y_test, logit.predict(X_test), "Logistic t=0.5 (test)")'''),

md(r"""
## §3 Coefficients → Odds ratio (ตีความ)
- $b > 0$ → x เพิ่ม โอกาสเป็นคลาส 1 เพิ่ม · $b < 0$ → ลด
- **odds ratio** $= e^{b}$: x เพิ่ม 1 หน่วย odds ของคลาส 1 **คูณด้วย** $e^b$ (เช่น 1.04 = เพิ่ม 4%)
- ตาราง 1 = หน่วยเดิม (ไม่ scale, ไม่ regularize) → ตีความต่อ "1 หน่วย" · ตาราง 2 = standardized → เทียบความสำคัญ (ต่อ 1 SD)
"""),
code(r'''raw = Pipeline([("prep", build_prep(X_train, scale=None)), ("model", LogisticRegression(C=1e6, max_iter=20000))]).fit(X_train, y_train)
names = raw.named_steps["prep"].get_feature_names_out()
b_raw = raw.named_steps["model"].coef_[0]
std = Pipeline([("prep", build_prep(X_train, scale="standard")), ("model", LogisticRegression(C=1e6, max_iter=20000))]).fit(X_train, y_train)
b_std = std.named_steps["model"].coef_[0]
coef = pd.DataFrame({"coef (หน่วยเดิม)": b_raw, "odds ratio e^b": np.exp(b_raw),
                     "% เปลี่ยนของ odds ต่อ 1 หน่วย": (np.exp(b_raw) - 1) * 100,
                     "coef (standardized)": b_std, "odds ratio ต่อ 1 SD": np.exp(b_std)}, index=names)
coef = coef.reindex(coef["coef (standardized)"].abs().sort_values(ascending=False).index)
display(coef)
b0 = raw.named_steps["model"].intercept_[0]
print("logit(p) = ln(p/(1-p)) = " + f"{b0:.4f} " + " ".join(f"{'+' if v >= 0 else '-'} {abs(v):.4f}×{k}" for k, v in zip(names, b_raw)))
for k in coef.index[:3]:
    r = coef.loc[k]
    print(f"✍️ {k}: เพิ่ม 1 หน่วย → odds ของ {TARGET}={POS_LABEL} คูณ {r['odds ratio e^b']:.4f} ({r['% เปลี่ยนของ odds ต่อ 1 หน่วย']:+.2f}%) โดยตัวแปรอื่นคงที่")
coef["coef (standardized)"].plot(kind="barh", figsize=(6, 0.35 * len(coef) + 1), title="standardized coefficients"); plt.gca().invert_yaxis(); plt.show()'''),
md(r"""**✍️ คำตอบ §3:** ตัวแปรที่มีผลมากสุดคือ … (coef มาตรฐาน …) · `…` เพิ่ม 1 หน่วย odds ของคลาส 1 เพิ่มขึ้น … เท่า (…%) · `…` มี coef ลบ → ลดโอกาส"""),

md(r"""## §4 คำนวณความน่าจะเป็นด้วยมือ (แถวแรกของ test) — ตรวจกับ predict_proba"""),
code(r'''x0 = raw.named_steps["prep"].transform(X_test.iloc[[0]])[0]
z = b0 + float(np.dot(b_raw, x0))
p = 1 / (1 + np.exp(-z))
print("ค่าแถวแรก:", {n: round(float(v), 3) for n, v in zip(names, x0)})
print(f"z = b0 + Σ b·x = {z:.4f}  →  p = 1/(1+e^(-z)) = {p:.4f}")
print(f"predict_proba = {raw.predict_proba(X_test.iloc[[0]])[0, 1]:.4f} → ทาย {int(p >= 0.5)} ที่ t=0.5 / {int(p >= THRESHOLD)} ที่ t={THRESHOLD} | ค่าจริง {y_test.iloc[0]}")
proba_test = logit.predict_proba(X_test)[:, 1]
display(pd.DataFrame({"actual": y_test.values[:10], "P(1)": proba_test[:10], "pred t=0.5": (proba_test[:10] >= .5).astype(int),
                      f"pred t={THRESHOLD}": (proba_test[:10] >= THRESHOLD).astype(int)}))
plt.figure(figsize=(6, 3.2)); sns.histplot(x=proba_test, hue=y_test.values, bins=20, element="step"); plt.axvline(.5, color="k", ls="--"); plt.axvline(THRESHOLD, color="r", ls=":")
plt.xlabel("P(class 1)"); plt.title("predicted probability by actual class (test)"); plt.show()'''),

md(r"""
## §5 Threshold — ตาราง confusion matrix + metrics ทุก threshold ⭐
ลด threshold → ทาย 1 ง่ายขึ้น → **recall ↑ precision ↓** (FN ↓ FP ↑)
"""),
code(r'''# ใช้ความน่าจะเป็นจาก CV (ทุกแถวถูกทำนายตอนอยู่ใน validation) → เสถียรกว่า test ชุดเดียว · เปลี่ยนเป็น proba_test/y_test ได้ถ้าโจทย์ใช้ hold-out
SOURCE = "holdout"     # ✏️ "holdout" = ใช้ test set · "cv" = cross_val_predict ทั้งชุด
if SOURCE == "cv":
    yy, pp = y, cross_val_predict(make_pipe(LogisticRegression(max_iter=5000), X), X, y, cv=cv, method="predict_proba")[:, 1]
else:
    yy, pp = y_test, proba_test
trows = []
for t in sorted(set(THRESHOLDS + [THRESHOLD, 0.5])):
    pr = (pp >= t).astype(int); tn, fp, fn, tp = confusion_matrix(yy, pr, labels=[0, 1]).ravel()
    trows.append({"threshold": t, "TP": tp, "FP": fp, "FN": fn, "TN": tn, "accuracy": accuracy_score(yy, pr),
                  "precision": precision_score(yy, pr, zero_division=0), "recall": recall_score(yy, pr), "f1": f1_score(yy, pr)})
tt = results_table(trows)
a, b = tt.set_index("threshold").loc[0.5], tt.set_index("threshold").loc[THRESHOLD]
print(f"✍️ ลด threshold 0.5 → {THRESHOLD}: recall {a.recall:.4f} → {b.recall:.4f} · precision {a.precision:.4f} → {b.precision:.4f} · "
      f"F1 {a.f1:.4f} → {b.f1:.4f} · FN {int(a.FN)} → {int(b.FN)} · FP {int(a.FP)} → {int(b.FP)}")
best = tt.loc[tt.f1.idxmax()]; print(f"✍️ threshold ที่ F1 สูงสุด = {best.threshold} (F1 {best.f1:.4f})")
for t in [0.5, THRESHOLD]:
    print(f"===== threshold {t} ====="); show_cm(yy, (pp >= t).astype(int), f"threshold = {t}")'''),
code(r'''fpr, tpr, thr_roc = roc_curve(yy, pp)
prec, rec, _ = precision_recall_curve(yy, pp)
fig, ax = plt.subplots(1, 3, figsize=(15, 3.8))
ax[0].plot(tt.threshold, tt.precision, "o-", label="precision"); ax[0].plot(tt.threshold, tt.recall, "o-", label="recall")
ax[0].plot(tt.threshold, tt.f1, "o-", label="F1"); ax[0].plot(tt.threshold, tt.accuracy, "o--", label="accuracy"); ax[0].legend(); ax[0].set(xlabel="threshold", title="metrics vs threshold")
ax[1].plot(fpr, tpr); ax[1].plot([0, 1], [0, 1], "k--"); ax[1].set(xlabel="FPR (1 - specificity)", ylabel="TPR (recall)", title=f"ROC (AUC = {roc_auc_score(yy, pp):.3f})")
ax[2].plot(rec, prec); ax[2].set(xlabel="recall", ylabel="precision", title=f"PR curve (AP = {average_precision_score(yy, pp):.3f})")
plt.tight_layout(); plt.show()
print(f"✍️ AUC = {roc_auc_score(yy, pp):.4f} → โอกาสที่โมเดลให้คะแนนตัวอย่างคลาส 1 สูงกว่าคลาส 0 ที่สุ่มมา = {roc_auc_score(yy, pp):.1%} (0.5 = เดาสุ่ม)")'''),
md(r"""**✍️ คำตอบ §5:** ที่ threshold 0.5 recall … precision … · ลดเป็น … recall เพิ่มเป็น … precision ลดเป็น … · ถ้าการพลาดผู้ป่วยจริง (FN) แพงกว่า → เลือก threshold ต่ำ"""),

md(r"""## §6 Tune C (regularization) + เทียบก่อน/หลัง (CV)"""),
code(r'''grid = GridSearchCV(make_pipe(LogisticRegression(max_iter=5000), X),
                    {"model__C": [0.001, 0.01, 0.1, 1, 10, 100], "model__class_weight": [None, "balanced"]},
                    cv=cv, scoring=cls_scoring(y), refit="f1").fit(X, y)
display(top_k(grid, 6))
results_table([evaluate("Majority baseline", DummyClassifier(), X, y, cv),
               evaluate("Logistic default (C=1)", make_pipe(LogisticRegression(max_iter=5000), X), X, y, cv),
               evaluate("Logistic tuned", grid.best_estimator_, X, y, cv, str(grid.best_params_))])
print("✍️ C เล็ก = regularize แรง (coef หดเข้า 0) · class_weight='balanced' = ให้น้ำหนักคลาสส่วนน้อย → recall ↑")'''),

md(r"""## §7 ทำนายข้อมูลใหม่ (probability + คำตัดสินที่ threshold 0.5 และ THRESHOLD)"""),
code(r'''if NEW_DATA is not None:
    nd = align_new(new_data(NEW_DATA), X)
    pn = logit.predict_proba(nd)[:, 1]
    out = nd.copy(); out["P(1)"] = pn; out["pred t=0.5"] = (pn >= .5).astype(int); out[f"pred t={THRESHOLD}"] = (pn >= THRESHOLD).astype(int)
    display(out)
    print(f"✍️ ข้อมูลใหม่มีความน่าจะเป็นเป็น {TARGET}={POS_LABEL} = {pn[0]:.4f} → ที่ threshold 0.5 ทาย {int(pn[0] >= .5)}, ที่ {THRESHOLD} ทาย {int(pn[0] >= THRESHOLD)}")'''),
]

if __name__ == "__main__":
    build("../T07_logistic_regression.ipynb", TITLE, CONFIG, S)
