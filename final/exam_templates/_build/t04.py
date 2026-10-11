from nbtools import md, code, build

TITLE = r"""
# T04 · Imbalanced Classification (Undersampling · Oversampling · SMOTE · Cost-sensitive · Threshold)

**ใช้เมื่อโจทย์ถาม:** คลาสไม่สมดุล · ทำไม accuracy หลอก · random under/oversampling · **SMOTE** · SMOTE ต้องทำเฉพาะ training ·
เทียบก่อน/หลัง resampling · class_weight / cost-sensitive · เลือก metric (recall / precision / F1 / PR-AUC) · ปรับ threshold

| ขั้น | ทำอะไร |
|---|---|
| 1 | แก้ **⚙️ CONFIG** — สำคัญที่สุด: `TARGET`, `POS_LABEL` (= คลาสส่วนน้อยที่สนใจ) |
| 2 | Run All · ตารางหลักอยู่ §4 · ตาราง threshold อยู่ §7 |

> 🔑 กฎทอง: **resample เฉพาะ training (ใน fold) — ห้ามแตะ test** → ใช้ `imblearn.pipeline.Pipeline` แล้ว CV
"""

CONFIG = r'''# ════════ ⚙️ CONFIG — แก้ cell นี้ให้ตรงโจทย์ ════════
DATA_PATH = "../practice/data/p3_breast_cancer_imbalanced.csv"
TARGET    = "diagnosis"
POS_LABEL = "malignant"     # คลาสส่วนน้อย/คลาสที่สนใจ (= 1)
ID_COL    = None
DROP_COLS = []
SCALE     = "standard"
MODEL_NAME = "LogReg"       # โมเดลหลักที่จะลอง resampling: "LogReg" | "KNN" | "Tree" | "RF"
PRIMARY_METRIC = "f1"       # metric ที่ใช้เลือก: "f1" | "recall" | "precision"
SMOTE_K   = 5               # k_neighbors ของ SMOTE
EVAL_MODE = "cv"            # "cv" = stratified k-fold · "holdout" = แบ่ง train/test
N_FOLDS, TEST_SIZE, SEED = 5, 0.2, 42
MISSING_MARKERS, SHEET, CSV_SEP = ["?", "", " ", "NA"], 0, ","
'''

S = [
md(r"""## §1 โหลด + ดูความไม่สมดุล"""),
code(r'''from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

df = load_data(DATA_PATH)
check(df, TARGET)
X, y = make_xy(df)
counts = y.value_counts()
ratio = counts.max() / counts.min()
print(f"✍️ คลาสส่วนน้อย (1 = {POS_LABEL}) มี {counts.get(1, 0)} แถว ({y.mean():.1%}) · คลาสส่วนใหญ่ {counts.get(0, 0)} แถว → imbalance ratio {ratio:.2f} : 1")
counts.rename({0: "0 (negative)", 1: f"1 ({POS_LABEL})"}).plot(kind="bar", figsize=(4, 3), title="class distribution", rot=0); plt.show()'''),

md(r"""
## §2 ทำไม accuracy หลอก — majority baseline
โมเดลที่ทายคลาสใหญ่ทุกแถวได้ accuracy = สัดส่วนคลาสใหญ่ แต่ **recall/F1 ของคลาสส่วนน้อย = 0**
"""),
code(r'''cv = get_cv()
base = evaluate("Majority baseline", DummyClassifier(strategy="most_frequent"), X, y, cv)
print(f"✍️ majority baseline ได้ accuracy {base['accuracy']:.4f} แต่ recall {base['recall']:.4f} และ F1 {base['f1']:.4f} → "
      "accuracy สูงแต่หาคลาสที่สนใจไม่เจอเลย จึงต้องใช้ recall / precision / F1 ของคลาสส่วนน้อย")'''),

md(r"""
## §3 Resampling บน training set (สาธิต: จำนวนก่อน/หลัง — test ไม่ถูกแตะ)
| วิธี | ทำอะไร | ข้อดี / ข้อเสีย |
|---|---|---|
| Random **Under**sampling | ลบคลาสใหญ่ให้เท่าคลาสเล็ก | เร็ว · ทิ้งข้อมูล |
| Random **Over**sampling | copy คลาสเล็กซ้ำ | ไม่เสียข้อมูล · overfit จุดซ้ำ |
| **SMOTE** | สร้างจุดใหม่บนเส้นระหว่างจุดคลาสเล็กกับ k เพื่อนบ้าน: $x_{new}=x+\lambda(x_{nn}-x)$ | ไม่ซ้ำ · อาจสร้าง noise ที่ขอบคลาส |
| class_weight="balanced" | ให้น้ำหนัก error คลาสเล็กมากขึ้น (cost-sensitive) | ไม่เปลี่ยนข้อมูล |
"""),
code(r'''X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, stratify=y, random_state=SEED)
prep = build_prep(X_train).fit(X_train)
Xtr = prep.transform(X_train)
show = {"original train": y_train.value_counts().sort_index()}
for name, s in [("RandomUnderSampler", RandomUnderSampler(random_state=SEED)),
                ("RandomOverSampler", RandomOverSampler(random_state=SEED)),
                ("SMOTE", SMOTE(k_neighbors=SMOTE_K, random_state=SEED))]:
    _, yr = s.fit_resample(Xtr, y_train)
    show[name] = pd.Series(yr).value_counts().sort_index()
show["test (ไม่แตะ)"] = y_test.value_counts().sort_index()
display(pd.DataFrame(show).T.rename(columns={0: "class 0", 1: f"class 1 ({POS_LABEL})"}))

# ภาพ SMOTE บน 2 feature แรก (หลัง scale)
Xs, ys = SMOTE(k_neighbors=SMOTE_K, random_state=SEED).fit_resample(Xtr[:, :2], y_train)
n0 = len(Xtr)
fig, ax = plt.subplots(1, 2, figsize=(11, 4), sharex=True, sharey=True)
ax[0].scatter(Xtr[:, 0], Xtr[:, 1], c=y_train, cmap="coolwarm", s=12, alpha=.7); ax[0].set_title("before SMOTE (train)")
ax[1].scatter(Xs[:n0, 0], Xs[:n0, 1], c=ys[:n0], cmap="coolwarm", s=12, alpha=.5)
ax[1].scatter(Xs[n0:, 0], Xs[n0:, 1], c="gold", edgecolor="k", s=18, label="synthetic"); ax[1].legend(); ax[1].set_title("after SMOTE")
for a in ax: a.set(xlabel=prep.get_feature_names_out()[0], ylabel=prep.get_feature_names_out()[1])
plt.tight_layout(); plt.show()'''),

md(r"""
## §4 เปรียบเทียบ: ไม่ทำอะไร vs Under vs Over vs SMOTE vs class_weight ⭐
resampler อยู่ **ใน** `ImbPipeline` → ใน CV จะ resample เฉพาะ training fold · validation fold เป็นข้อมูลจริงเสมอ
"""),
code(r'''def base_model(balanced=False):
    cw = "balanced" if balanced else None
    return {"LogReg": LogisticRegression(max_iter=5000, class_weight=cw),
            "KNN": KNeighborsClassifier(n_neighbors=5),
            "Tree": DecisionTreeClassifier(max_depth=5, random_state=SEED, class_weight=cw),
            "RF": RandomForestClassifier(n_estimators=200, random_state=SEED, class_weight=cw)}[MODEL_NAME]

def imb_pipe(sampler=None, balanced=False):
    steps = [("prep", build_prep(X))]
    if sampler is not None:
        steps.append(("sampler", sampler))
    steps.append(("model", base_model(balanced)))
    return ImbPipeline(steps)

variants = {"No resampling": imb_pipe(),
            "RandomUnderSampler": imb_pipe(RandomUnderSampler(random_state=SEED)),
            "RandomOverSampler": imb_pipe(RandomOverSampler(random_state=SEED)),
            "SMOTE": imb_pipe(SMOTE(k_neighbors=SMOTE_K, random_state=SEED))}
if MODEL_NAME != "KNN":
    variants["class_weight=balanced"] = imb_pipe(balanced=True)

rows = [base]
for name, pipe in variants.items():
    if EVAL_MODE == "cv":
        rows.append(evaluate(f"{MODEL_NAME} + {name}", pipe, X, y, cv))
    else:
        rows.append(evaluate_holdout(f"{MODEL_NAME} + {name}", pipe, X_train, y_train, X_test, y_test))
imb = results_table(rows)
say_compare(imb, PRIMARY_METRIC, "Majority baseline")
imb.set_index("model")[["precision", "recall", "f1"]].plot(kind="barh", figsize=(8, 4), title=f"{EVAL_MODE.upper()} — positive class = {POS_LABEL}")
plt.gca().invert_yaxis(); plt.tight_layout(); plt.show()'''),
md(r"""**✍️ คำตอบ §4:** ไม่ resample ได้ recall … F1 … · SMOTE ทำให้ recall เพิ่มเป็น … (precision เปลี่ยนเป็น …) เพราะโมเดลเห็นคลาสส่วนน้อยมากขึ้น · undersampling … · เลือก … เพราะ …"""),

md(r"""## §5 Confusion matrix: ไม่ resample vs SMOTE (cross_val_predict — ทุกแถวถูกทำนายตอนอยู่ใน validation fold)"""),
code(r'''for name in ["No resampling", "SMOTE"]:
    pred = cross_val_predict(variants[name], X, y, cv=cv)
    print(f"===== {MODEL_NAME} + {name} =====")
    show_cm(y, pred, title=f"{MODEL_NAME} + {name}")'''),
md(r"""**✍️ คำตอบ §5:** SMOTE ลด FN จาก … เหลือ … (หาคลาส {POS_LABEL} เจอเพิ่ม) แต่ FP เพิ่มจาก … เป็น … → trade-off recall ↑ precision ↓"""),

md(r"""
## §6 ❌ วิธีผิด: SMOTE ทั้งตารางก่อน CV (data leakage) — ไว้ตอบคำถาม "ทำไมห้าม"
จุดสังเคราะห์ถูกสร้างจากจุดที่อยู่ใน validation fold → validation ไม่ใช่ข้อมูลจริง → คะแนนสูงเกินจริง
"""),
code(r'''Xall = build_prep(X).fit_transform(X)
Xw, yw = SMOTE(k_neighbors=SMOTE_K, random_state=SEED).fit_resample(Xall, y)
wrong = evaluate("❌ SMOTE ก่อน CV (leak)", base_model(), Xw, yw, cv)
right = [r for r in rows if r["model"].endswith("+ SMOTE")][0]
results_table([right, wrong])
print(f"✍️ SMOTE ก่อน CV ได้ F1 {wrong['f1']:.4f} สูงกว่าวิธีถูก ({right['f1']:.4f}) เพราะ validation มีจุดสังเคราะห์ที่ลอกมาจาก training → ประเมินสูงเกินจริง")'''),

md(r"""
## §7 ปรับ threshold (อีกทางแก้ imbalance — ไม่ต้อง resample)
`predict()` ตัดที่ 0.5 · ลด threshold → recall ↑ precision ↓ · เลือก threshold ตามต้นทุน FN vs FP
"""),
code(r'''THRESHOLDS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]      # ✏️
proba = cross_val_predict(variants["No resampling"], X, y, cv=cv, method="predict_proba")[:, 1]
trows = []
for t in THRESHOLDS:
    p = (proba >= t).astype(int); tn, fp, fn, tp = confusion_matrix(y, p, labels=[0, 1]).ravel()
    trows.append({"threshold": t, "TP": tp, "FP": fp, "FN": fn, "TN": tn, "accuracy": accuracy_score(y, p),
                  "precision": precision_score(y, p, zero_division=0), "recall": recall_score(y, p), "f1": f1_score(y, p)})
tt = results_table(trows)
best_t = tt.loc[tt[PRIMARY_METRIC].idxmax()]
print(f"✍️ threshold ที่ {PRIMARY_METRIC} สูงสุด = {best_t['threshold']} ({PRIMARY_METRIC} {best_t[PRIMARY_METRIC]:.4f}, recall {best_t['recall']:.4f}, precision {best_t['precision']:.4f})")
prec, rec, thr = precision_recall_curve(y, proba)
fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
ax[0].plot(tt["threshold"], tt["precision"], "o-", label="precision"); ax[0].plot(tt["threshold"], tt["recall"], "o-", label="recall")
ax[0].plot(tt["threshold"], tt["f1"], "o-", label="F1"); ax[0].set(xlabel="threshold", title="metrics vs threshold"); ax[0].legend()
ax[1].plot(rec, prec); ax[1].set(xlabel="recall", ylabel="precision", title=f"PR curve (AP = {average_precision_score(y, proba):.3f})")
plt.tight_layout(); plt.show()
print(f"ROC-AUC = {roc_auc_score(y, proba):.4f} | PR-AUC (average precision) = {average_precision_score(y, proba):.4f}  ← PR-AUC เหมาะกับ imbalanced มากกว่า")'''),

md(r"""
## §8 เลือก metric ให้เหมาะกับปัญหา (copy ไปตอบ)
| สถานการณ์ | metric | เหตุผล |
|---|---|---|
| พลาดคลาสสนใจแพง (โรค, ฉ้อโกง, churn) | **recall** | ลด FN |
| เตือนผิดแพง (spam, ส่งโปรโมชันมีต้นทุน) | **precision** | ลด FP |
| ต้องสมดุลทั้งสอง | **F1** | harmonic mean ของ P และ R |
| ข้อมูลสมดุล ต้นทุนเท่ากัน | accuracy | — |
| เทียบโมเดลโดยไม่ผูก threshold (imbalanced) | PR-AUC | ไม่ถูกคลาสใหญ่ครอบงำเหมือน ROC-AUC |

**✍️ คำตอบ:** ข้อมูลนี้คลาส {POS_LABEL} มีแค่ …% · accuracy ของ baseline … จึงหลอก · เลือก … เพราะการพลาด … (FN/FP) เสียหายกว่า · โมเดลสุดท้าย = … ได้ … = …
"""),
]

if __name__ == "__main__":
    build("../T04_imbalanced_smote.ipynb", TITLE, CONFIG, S)
