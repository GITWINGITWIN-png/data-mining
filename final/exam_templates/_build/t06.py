from nbtools import md, code, build

TITLE = r"""
# T06 · Linear Regression (Equation · Coefficients · Prediction · MAE/MSE/RMSE/R² · Baseline · เทียบโมเดล regression)

**ใช้เมื่อโจทย์ถาม:** ทำนาย "ตัวเลข" (ราคา, ยอดขาย, ค่าใช้จ่าย) · เขียนสมการ · ตีความ coefficient · R² ·
เทียบกับ mean baseline · simple vs multiple regression · residual plot · ทำนายข้อมูลใหม่ · เทียบ KNN/Tree regressor · optimize

| ขั้น | ทำอะไร |
|---|---|
| 1 | แก้ **⚙️ CONFIG** — `TARGET` (ตัวเลข), `SIMPLE_X` (ตัวแปรเดียว ถ้าโจทย์ให้ simple regression), `NEW_DATA` |
| 2 | Run All · สมการอยู่ §3–§4 · ตาราง metric อยู่ §5 |
"""

CONFIG = r'''# ════════ ⚙️ CONFIG — แก้ cell นี้ให้ตรงโจทย์ ════════
DATA_PATH = "../practice/data/p7_insurance.csv"
TARGET    = "charges"        # ตัวเลขที่จะทำนาย
ID_COL    = None
DROP_COLS = []
FEATURES  = None             # list feature ที่โจทย์ให้ใช้ · None = ทุกคอลัมน์ที่เหลือ
SIMPLE_X  = "age"            # ตัวแปรเดียวสำหรับ simple linear regression (None = ข้าม §3)
DROP_FIRST = True            # one-hot ตัด dummy ตัวแรก (reference category) → ตีความ coef ง่าย ไม่ซ้ำซ้อน
NEW_DATA  = {"age": 40, "sex": "male", "bmi": 30.0, "children": 2, "smoker": "no", "region": "northeast"}   # None = ข้าม
EVAL_MODE = "holdout"        # "holdout" (train/test) | "cv"
TEST_SIZE, N_FOLDS, SEED = 0.2, 5, 42
MISSING_MARKERS, SHEET, CSV_SEP = ["?", "", " ", "NA"], 0, ","
'''

S = [
md(r"""## §1 โหลด + EDA ของ target + correlation กับ target"""),
code(r'''df = load_data(DATA_PATH)
check(df, TARGET)
X, y = make_xy(df, task="regression")
if FEATURES:
    X = X[FEATURES]
fig, ax = plt.subplots(1, 2, figsize=(11, 3.5))
sns.histplot(y, kde=True, ax=ax[0]); ax[0].set_title(f"{TARGET}: mean={y.mean():.2f}, median={y.median():.2f}, skew={y.skew():.2f}")
corr_t = pd.concat([X[num_cols(X)], y], axis=1).corr()[TARGET].drop(TARGET).sort_values(key=abs, ascending=False)
corr_t.plot(kind="barh", ax=ax[1], title=f"correlation with {TARGET}"); ax[1].invert_yaxis()
plt.tight_layout(); plt.show()
print("✍️ ตัวแปรตัวเลขที่สัมพันธ์กับ target มากสุด:", ", ".join(f"{k} (r={v:.3f})" for k, v in corr_t.head(3).items()))
for c in cat_cols(X):
    print(f"ค่าเฉลี่ย {TARGET} ตาม {c}:", df.groupby(c)[TARGET].mean().round(2).to_dict())'''),

md(r"""## §2 แบ่ง train/test (fit ทุกอย่างบน train)"""),
code(r'''X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=SEED)
print(f"train {X_train.shape} | test {X_test.shape}")'''),

md(r"""
## §3 Simple linear regression: $\hat y = b_0 + b_1 x$
$b_1$ = ความชัน (x เพิ่ม 1 หน่วย ŷ เปลี่ยน $b_1$) · $b_0$ = ค่า ŷ เมื่อ x = 0
"""),
code(r'''if SIMPLE_X:
    slr = LinearRegression().fit(X_train[[SIMPLE_X]], y_train)
    b0, b1 = slr.intercept_, slr.coef_[0]
    pred_s = slr.predict(X_test[[SIMPLE_X]])
    print(f"สมการ: {TARGET} = {b0:.4f} + ({b1:.4f}) × {SIMPLE_X}")
    print(f"✍️ {SIMPLE_X} เพิ่ม 1 หน่วย → {TARGET} เปลี่ยน {b1:+.4f} หน่วยโดยเฉลี่ย")
    print("test:", {k: round(v, 4) for k, v in reg_metrics(y_test, pred_s).items()})
    plt.figure(figsize=(6, 4)); plt.scatter(X_test[SIMPLE_X], y_test, s=12, alpha=.5, label="test")
    xs = np.linspace(X[SIMPLE_X].min(), X[SIMPLE_X].max(), 50); plt.plot(xs, b0 + b1 * xs, "r", label="fitted line")
    plt.xlabel(SIMPLE_X); plt.ylabel(TARGET); plt.legend(); plt.title("Simple linear regression"); plt.show()'''),

md(r"""
## §4 Multiple linear regression — สมการเต็ม + coefficient (หน่วยเดิม → ตีความได้)
- coefficient ตัวเลข: *x เพิ่ม 1 หน่วย ŷ เปลี่ยน b หน่วย **โดยตัวแปรอื่นคงที่***
- coefficient dummy (เช่น `smoker_yes`): *กลุ่มนี้มี ŷ ต่างจาก **กลุ่มอ้างอิง** (dummy ที่ถูกตัด) b หน่วย*
- **เทียบความสำคัญ** ด้วย coefficient หน่วยเดิมไม่ได้ (หน่วยต่างกัน) → ดู standardized coefficient
"""),
code(r'''prep_raw = build_prep(X_train, scale=None)
if DROP_FIRST:
    prep_raw.set_params(cat__encode=OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False))
lr = Pipeline([("prep", prep_raw), ("model", LinearRegression())]).fit(X_train, y_train)
names = lr.named_steps["prep"].get_feature_names_out()
coef = pd.DataFrame({"coefficient": lr.named_steps["model"].coef_}, index=names)

# standardized coefficient (z-score feature ตัวเลข; dummy คงเดิม) → ใช้จัดอันดับความสำคัญของตัวเลข = ผลต่อ y เมื่อ x เปลี่ยน 1 SD
prep_std = build_prep(X_train, scale="standard")
if DROP_FIRST:
    prep_std.set_params(cat__encode=OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False))
lr_std = Pipeline([("prep", prep_std), ("model", LinearRegression())]).fit(X_train, y_train)
std_coef = pd.Series(lr_std.named_steps["model"].coef_, index=lr_std.named_steps["prep"].get_feature_names_out())
coef["standardized_coef"] = std_coef.reindex(coef.index)
coef = coef.reindex(coef["coefficient"].abs().sort_values(ascending=False).index)
display(coef)
b0 = lr.named_steps["model"].intercept_
print("สมการ:\n  " + TARGET + f" = {b0:.4f} " + " ".join(f"{'+' if v >= 0 else '-'} {abs(v):.4f}×{k}" for k, v in coef["coefficient"].items()))
if DROP_FIRST and cat_cols(X):
    print("กลุ่มอ้างอิง (dummy ที่ถูกตัด):", {c: cats[0] for c, cats in zip(cat_cols(X_train), lr.named_steps["prep"].named_transformers_["cat"].named_steps["encode"].categories_)})
top = coef["standardized_coef"].abs().sort_values(ascending=False).index[0]
print(f"✍️ ตัวแปรที่มีผลมากสุด (standardized) = {top} · coefficient หน่วยเดิม {coef.loc[top, 'coefficient']:+.4f}")'''),
md(r"""**✍️ คำตอบ §4:** สมการ ŷ = … · `…` เพิ่ม 1 หน่วย ŷ เพิ่ม … โดยตัวแปรอื่นคงที่ · `smoker_yes` = … → คนสูบบุหรี่จ่ายมากกว่าคนไม่สูบ … หน่วย"""),

md(r"""
## §5 Evaluation: mean baseline vs simple vs multiple (MAE / MSE / RMSE / R²)
MAE = |error| เฉลี่ย (หน่วยเดียวกับ y) · RMSE = ลงโทษ error ใหญ่มากกว่า · R² = สัดส่วนความแปรปรวนของ y ที่อธิบายได้ (1 = สมบูรณ์, 0 = เท่ากับทายค่าเฉลี่ย, < 0 = แย่กว่าค่าเฉลี่ย)
"""),
code(r'''models = {"Mean baseline": DummyRegressor(strategy="mean"),
          "Linear Regression (all)": lr}
if SIMPLE_X:
    models[f"Linear Regression ({SIMPLE_X})"] = Pipeline([("sel", ColumnTransformer([("x", "passthrough", [SIMPLE_X])])), ("model", LinearRegression())])
rows = []
for name, m in models.items():
    if EVAL_MODE == "holdout":
        m.fit(X_train, y_train)
        r = {"model": name, **reg_metrics(y_test, m.predict(X_test)), "train_R2": r2_score(y_train, m.predict(X_train))}
    else:
        r = evaluate_reg(name, m, X, y)
    rows.append(r)
mt = results_table(rows)
say_compare(mt, "RMSE", "Mean baseline", higher_is_better=False)
best_r2 = mt.loc[mt["R2"].idxmax()]
print(f"✍️ R² = {best_r2['R2']:.4f} → โมเดลอธิบายความแปรปรวนของ {TARGET} ได้ {best_r2['R2']:.1%} · MAE {best_r2['MAE']:.2f} = ทายพลาดเฉลี่ย ±{best_r2['MAE']:.2f} หน่วย")'''),
code(r'''# ตรวจด้วยมือ: 5 แถวแรกของ test
pred = lr.predict(X_test)
chk = pd.DataFrame({"actual": y_test.values[:5], "predicted": pred[:5]}); chk["error"] = chk.actual - chk.predicted
chk["|error|"] = chk.error.abs(); chk["error²"] = chk.error ** 2
display(chk)
print(f"(5 แถวนี้) MAE = {chk['|error|'].mean():.4f} · MSE = {chk['error²'].mean():.4f} · RMSE = {np.sqrt(chk['error²'].mean()):.4f}")
# Residual plot + actual vs predicted
res = y_test - pred
fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
ax[0].scatter(pred, y_test, s=10, alpha=.5); lim = [min(pred.min(), y_test.min()), max(pred.max(), y_test.max())]
ax[0].plot(lim, lim, "r--"); ax[0].set(xlabel="predicted", ylabel="actual", title="actual vs predicted")
ax[1].scatter(pred, res, s=10, alpha=.5); ax[1].axhline(0, color="r", ls="--"); ax[1].set(xlabel="predicted", ylabel="residual", title="residual plot")
plt.tight_layout(); plt.show()
print("✍️ residual ควรกระจายสุ่มรอบ 0 · ถ้าเป็นรูปแบบ (โค้ง/กรวย/แยกกลุ่ม) แปลว่าความสัมพันธ์ไม่เป็นเชิงเส้นหรือขาดตัวแปร/interaction")'''),

md(r"""## §6 เทียบโมเดล regression อื่น + optimize (CV บน train)"""),
code(r'''cvr = get_cv("regression")
cands = {"Mean baseline": DummyRegressor(),
         "Linear Regression": make_pipe(LinearRegression(), X_train),
         "KNN regressor (k=5)": make_pipe(KNeighborsRegressor(5), X_train),
         "Decision Tree reg (depth=5)": make_pipe(DecisionTreeRegressor(max_depth=5, random_state=SEED), X_train, scale=None),
         "Random Forest reg": make_pipe(RandomForestRegressor(n_estimators=200, random_state=SEED), X_train, scale=None)}
rows = [evaluate_reg(n, m, X_train, y_train, cvr) for n, m in cands.items()]
g_knn = GridSearchCV(make_pipe(KNeighborsRegressor(), X_train), {"model__n_neighbors": range(1, 31), "model__weights": ["uniform", "distance"]},
                     cv=cvr, scoring="neg_root_mean_squared_error").fit(X_train, y_train)
g_tree = GridSearchCV(make_pipe(DecisionTreeRegressor(random_state=SEED), X_train, scale=None),
                      {"model__max_depth": [2, 3, 4, 5, 6, 8, 10, None], "model__min_samples_leaf": [1, 5, 10, 20]},
                      cv=cvr, scoring="neg_root_mean_squared_error").fit(X_train, y_train)
rows += [evaluate_reg("KNN optimized", g_knn.best_estimator_, X_train, y_train, cvr, str(g_knn.best_params_)),
         evaluate_reg("Tree optimized", g_tree.best_estimator_, X_train, y_train, cvr, str(g_tree.best_params_))]
ct = results_table(rows, sort_by="RMSE", ascending=True)
say_compare(ct, "RMSE", "Mean baseline", higher_is_better=False)

best_name = ct.iloc[0]["model"]
best_model = {**cands, "KNN optimized": g_knn.best_estimator_, "Tree optimized": g_tree.best_estimator_}[best_name]
best_model.fit(X_train, y_train)
print(f"โมเดลที่ดีที่สุด ({best_name}) บน test:", {k: round(v, 4) for k, v in reg_metrics(y_test, best_model.predict(X_test)).items()})'''),
md(r"""**✍️ คำตอบ §6:** โมเดลที่ดีที่สุดคือ … (CV RMSE …, R² …) ดีกว่า Linear Regression (RMSE …) เพราะ … (เช่น ความสัมพันธ์ไม่เชิงเส้น/มี interaction) · optimize แล้ว RMSE ลดจาก … เป็น …"""),

md(r"""## §7 ทำนายข้อมูลใหม่"""),
code(r'''if NEW_DATA is not None:
    nd = align_new(new_data(NEW_DATA), X)
    out = nd.copy()
    out["pred_LinearRegression"] = lr.predict(nd)
    out[f"pred_{best_name}"] = best_model.predict(nd)
    display(out)
    # ตรวจมือ: แทนค่าในสมการ
    row = lr.named_steps["prep"].transform(nd.iloc[[0]])[0]
    terms = " + ".join(f"({c:.3f}×{v:g})" for c, v in zip(lr.named_steps["model"].coef_, row))
    print(f"แทนค่า: {lr.named_steps['model'].intercept_:.3f} + {terms} = {lr.predict(nd.iloc[[0]])[0]:.4f}")'''),
md(r"""**✍️ คำตอบ §7:** ข้อมูลใหม่ทำนาย {TARGET} = … (Linear Regression) / … (…)"""),
]

if __name__ == "__main__":
    build("../T06_linear_regression.ipynb", TITLE, CONFIG, S)
