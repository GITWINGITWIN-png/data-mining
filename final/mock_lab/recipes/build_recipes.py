"""สร้าง RapidMiner process "แม่แบบ" ของทุก recipe ในโน้ต LAB 02–06 (ไฟล์ .rmp)

ใช้ทำอะไร
- เปิดใน AI Studio (File → Import Process…) เพื่อดู "process ที่ถูกต้อง" ของแต่ละ task
  แล้วลองสร้างเองให้เหมือน · ทุกไฟล์ต่อผลไปที่ port res → กด ▶ แล้วดูแท็บ Results ได้เลย
- ทุกไฟล์ถูกรันทดสอบจริงด้วย batch runner (run_rm.sh) และเขียนผลลง out/ เพื่อเทียบกับ Python

รัน:  final/.venv/bin/python final/mock_lab/recipes/build_recipes.py
     bash final/mock_lab/run_rm.sh final/mock_lab/recipes/*.rmp
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from rm_builder import Op, Proc, save, read_csv, write_csv, cross_validation  # noqa: E402

ROOT = HERE.parents[2]                      # …/data mining
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
ADS = ROOT / "W12" / "Social_Network_Ads_2.csv"
BOSTON = ROOT / "W8" / "boston_r.csv"
BANK = ROOT / "W9" / "bank_dataset.csv"
CHURN = ROOT / "W14" / "customer_churn_69_1(in).csv"
UTIL = ROOT / "final" / "data" / "utilities.csv"
BEAUTY = ROOT / "W10" / "BeautyCo_68.xls"


def chain(proc, ops, out_port="example set output", in_port="example set input"):
    """ต่อ operator เรียงกันด้วย port มาตรฐาน (ExampleSet → ExampleSet)"""
    for a, b in zip(ops, ops[1:]):
        src = "output" if a.cls in ("read_csv", "read_excel") else out_port
        proc.wire(a, src, b, in_port)


def ads_prep(m, x0=45):
    """Social Network Ads: อ่าน → ตัด User ID → label 0/1 → binominal → Set Role → Gender เป็น dummy"""
    rd = m.add(read_csv("Read CSV", ADS, x=x0))
    sel = m.add(Op("select_attributes", "Select Attributes", {
        "attribute_filter_type": "subset", "attributes": "User ID", "invert_selection": True}, x=x0 + 135))
    n2b = m.add(Op("numerical_to_binominal", "Numerical to Binominal", {
        "attribute_filter_type": "single", "attribute": "Purchased", "min": 0.0, "max": 0.0}, x=x0 + 270))
    role = m.add(Op("set_role", "Set Role", {"attribute_name": "Purchased", "target_role": "label"}, x=x0 + 405))
    n2n = m.add(Op("nominal_to_numerical", "Nominal to Numerical", {
        "attribute_filter_type": "single", "attribute": "Gender", "coding_type": "dummy coding"}, x=x0 + 540))
    chain(m, [rd, sel, n2b, role, n2n])
    return n2n


def perf_binominal(name="Performance", main="f_measure"):
    return Op("performance_binominal_classification", name, {
        "main_criterion": main, "accuracy": True, "precision": True, "recall": True,
        "f_measure": True, "AUC": True}, x=180)


def testing_pane(perf, tag=""):
    """Testing pane: Apply Model → Performance  (tag = ต่อท้ายชื่อ เพราะชื่อ operator ห้ามซ้ำทั้ง process)"""
    te = Proc()
    ap = te.add(Op("apply_model", f"Apply Model{tag}", {}))
    te.add(perf)
    te.wire(None, "model", ap, "model")
    te.wire(None, "test set", ap, "unlabelled data")
    te.wire(ap, "labelled data", perf, "labelled data")
    te.wire(perf, "performance", None, "performance 1")
    return te


def training_normalize(learner, tag=""):
    """Training pane: Normalize → learner → Group Models (มัด preprocessing + โมเดล)"""
    tr = Proc()
    norm = tr.add(Op("normalize", f"Normalize{tag}", {"method": "Z-transformation"}))
    learner.x = 180
    tr.add(learner)
    grp = tr.add(Op("group_models", f"Group Models{tag}", {}, x=315))
    tr.wire(None, "training set", norm, "example set input")
    tr.wire(norm, "example set output", learner, "training set")
    tr.wire(norm, "preprocessing model", grp, "models in 1")
    tr.wire(learner, "model", grp, "models in 2")
    tr.wire(grp, "model out", None, "model")
    return tr


def training_plain(learner):
    tr = Proc()
    tr.add(learner)
    tr.wire(None, "training set", learner, "training set")
    tr.wire(learner, "model", None, "model")
    return tr


def perf_out(m, src, src_port, name, csv_name, x, y=85, res=0):
    """PerformanceVector → (res) + ตาราง CSV ใน out/"""
    p2d = m.add(Op("performance_to_data", f"Performance to Data {name}", {}, x=x, y=y))
    wr = m.add(write_csv(f"Write CSV {name}", OUT / csv_name, x=x + 135, y=y))
    m.wire(src, src_port, p2d, "performance vector")
    m.wire(p2d, "example set", wr, "input")
    m.wire(p2d, "performance vector", None, f"result {res + 1}")
    m.wire(wr, "through", None, f"result {res + 2}")


# ── 1. KNN ใน 10-fold CV โดย Normalize อยู่ใน Training pane (LAB 03 §3.7, LAB 04 §4.4) ──────────
m = Proc()
last = ads_prep(m)
cv = m.add(cross_validation("Cross Validation", training_normalize(Op("k_nn", "k-NN", {"k": 5})),
                            testing_pane(perf_binominal()), folds=10, seed=42, x=720))
m.wire(last, "example set output", cv, "example set")
perf_out(m, cv, "performance 1", "kNN", "knn_cv_normalize.csv", x=855)
save(m, HERE / "knn_cv_normalize.rmp")

# ── 2. Baseline (Default Model = mode) เทียบ k-NN ด้วย folds เดียวกัน (LAB 04 §4.3) ─────────────
m = Proc()
last = ads_prep(m)
mul = m.add(Op("multiply", "Multiply", {}, x=720))
m.wire(last, "example set output", mul, "input")
cv0 = m.add(cross_validation("CV Default Model", training_plain(Op("default_model", "Default Model", {"method": "mode"})),
                             testing_pane(perf_binominal("Performance (Baseline)"), " (Baseline)"),
                             folds=10, seed=42, x=855, y=34))
cv1 = m.add(cross_validation("CV k-NN", training_normalize(Op("k_nn", "k-NN", {"k": 5})),
                             testing_pane(perf_binominal("Performance (k-NN)"), " (k-NN)"),
                             folds=10, seed=42, x=855, y=187))
m.wire(mul, "output 1", cv0, "example set")
m.wire(mul, "output 2", cv1, "example set")
perf_out(m, cv0, "performance 1", "Baseline", "baseline_default_model.csv", x=990, y=34, res=0)
perf_out(m, cv1, "performance 1", "kNN", "baseline_knn.csv", x=990, y=187, res=2)
save(m, HERE / "baseline_vs_knn.rmp")

# ── 3. Optimize Parameters (Grid): k = 1..15 รอบ CV เดิม + Log ทุกรอบ (LAB 04 §4.5) ───────────────
m = Proc()
last = ads_prep(m)
inner = Proc()
cv = inner.add(cross_validation("Cross Validation", training_normalize(Op("k_nn", "k-NN", {"k": 5})),
                                testing_pane(perf_binominal(main="f_measure")), folds=10, seed=42))
log = inner.add(Op("log", "Log", {
    "log": ("list", [("k", "operator.k-NN.parameter.k"),
                     ("f_measure", "operator.Cross Validation.value.performance main criterion")]),
    "sorting_type": "none", "persistent": False}, x=180))
inner.wire(None, "input 1", cv, "example set")
inner.wire(cv, "performance 1", log, "through 1")
inner.wire(log, "through 1", None, "performance")
opt = m.add(Op("concurrency:optimize_parameters_grid", "Optimize Parameters (Grid)", {
    "parameters": ("list", [("k-NN.k", "[1.0;15.0;14;linear]")]),
    "error_handling": "fail on error"}, subprocesses=[inner], x=720))
m.wire(last, "example set output", opt, "input 1")
l2d = m.add(Op("log_to_data", "Log to Data", {"log_name": "Log"}, x=855, y=34))
wr = m.add(write_csv("Write CSV log", OUT / "optimize_knn_log.csv", x=990, y=34))
m.wire(opt, "performance", None, "result 1")
m.wire(opt, "parameter set", None, "result 2")
m.wire(l2d, "exampleSet", wr, "input")
m.wire(wr, "through", None, "result 3")
save(m, HERE / "optimize_knn_k.rmp")

# ── 4. Logistic Regression + Create/Apply Threshold บน hold-out 80/20 (LAB 05 §5.3) ───────────────
m = Proc()
last = ads_prep(m)
split = m.add(Op("split_data", "Split Data", {
    "partitions": ("enum", [0.8, 0.2], "ratio"), "sampling_type": "stratified sampling",
    "use_local_random_seed": True, "local_random_seed": 42}, x=720))
lr = m.add(Op("h2o:logistic_regression", "Logistic Regression", {
    "solver": "AUTO", "reproducible": True, "use_regularization": False, "standardize": True,
    "compute_p-values": True, "remove_collinear_columns": True, "add_intercept": True}, x=855, y=34))
ap = m.add(Op("apply_model", "Apply Model", {}, x=990, y=136))
thr = m.add(Op("create_threshold", "Create Threshold", {"threshold": 0.3, "first_class": "false",
                                                       "second_class": "true"}, x=990, y=34))
apt = m.add(Op("apply_threshold", "Apply Threshold", {}, x=1125, y=136))
pf = m.add(Op("performance_binominal_classification", "Performance (t=0.3)", {
    "main_criterion": "f_measure", "accuracy": True, "precision": True, "recall": True, "f_measure": True},
    x=1260, y=136))
m.wire(last, "example set output", split, "example set")
m.wire(split, "partition 1", lr, "training set")
m.wire(lr, "model", ap, "model")
m.wire(split, "partition 2", ap, "unlabelled data")
m.wire(ap, "labelled data", apt, "example set")
m.wire(thr, "output", apt, "threshold")
m.wire(apt, "example set", pf, "labelled data")
perf_out(m, pf, "performance", "LogReg", "logreg_threshold_0.3.csv", x=1395, y=136)
m.wire(ap, "model", None, "result 3")
save(m, HERE / "logreg_threshold.rmp")

# ── 5. Decision Tree vs Random Forest ใน 10-fold CV (LAB 05 §5.4–5.5) ─────────────────────────────
m = Proc()
last = ads_prep(m)
mul = m.add(Op("multiply", "Multiply", {}, x=720))
m.wire(last, "example set output", mul, "input")
tree = Op("concurrency:parallel_decision_tree", "Decision Tree", {
    "criterion": "gini_index", "maximal_depth": 3, "apply_pruning": False, "apply_prepruning": False})
rf = Op("concurrency:parallel_random_forest", "Random Forest", {
    "number_of_trees": 100, "criterion": "gini_index", "maximal_depth": 10, "guess_subset_ratio": True,
    "voting_strategy": "confidence vote", "use_local_random_seed": True, "local_random_seed": 42})
cvt = m.add(cross_validation("CV Decision Tree", training_plain(tree),
                             testing_pane(perf_binominal("Performance (Tree)"), " (Tree)"), folds=10, seed=42, x=855, y=34))
cvr = m.add(cross_validation("CV Random Forest", training_plain(rf),
                             testing_pane(perf_binominal("Performance (RF)"), " (RF)"), folds=10, seed=42, x=855, y=187))
m.wire(mul, "output 1", cvt, "example set")
m.wire(mul, "output 2", cvr, "example set")
perf_out(m, cvt, "performance 1", "Tree", "tree_cv.csv", x=990, y=34, res=0)
perf_out(m, cvr, "performance 1", "RF", "rf_cv.csv", x=990, y=187, res=2)
m.wire(cvt, "model", None, "result 5")
save(m, HERE / "tree_vs_rf.rmp")

# ── 6. Linear Regression (lstat, rm) hold-out 80/20 + Performance (Regression) (LAB 05 §5.2) ────────
m = Proc()
rd = m.add(read_csv("Read CSV", BOSTON))
sel = m.add(Op("select_attributes", "Select Attributes", {
    "attribute_filter_type": "subset", "attributes": "lstat|rm|medv"}, x=180))
role = m.add(Op("set_role", "Set Role", {"attribute_name": "medv", "target_role": "label"}, x=315))
chain(m, [rd, sel, role])
split = m.add(Op("split_data", "Split Data", {
    "partitions": ("enum", [0.8, 0.2], "ratio"), "sampling_type": "shuffled sampling",
    "use_local_random_seed": True, "local_random_seed": 42}, x=450))
lin = m.add(Op("linear_regression", "Linear Regression", {
    "feature_selection": "none", "eliminate_colinear_features": True, "use_bias": True}, x=585, y=34))
ap = m.add(Op("apply_model", "Apply Model", {}, x=720, y=136))
pr = m.add(Op("performance_regression", "Performance (Regression)", {
    "main_criterion": "root_mean_squared_error", "root_mean_squared_error": True, "absolute_error": True,
    "squared_error": True, "squared_correlation": True}, x=855, y=136))
m.wire(role, "example set output", split, "example set")
m.wire(split, "partition 1", lin, "training set")
m.wire(lin, "model", ap, "model")
m.wire(split, "partition 2", ap, "unlabelled data")
m.wire(ap, "labelled data", pr, "labelled data")
perf_out(m, pr, "performance", "LinReg", "linreg_boston.csv", x=990, y=136)
wt = m.add(Op("write_as_text", "Write Model as Text", {"result_file": str(OUT / "linreg_model.txt")}, x=855, y=34))
m.wire(ap, "model", wt, "input 1")
m.wire(wt, "input 1", None, "result 3")
save(m, HERE / "linreg_boston.rmp")

# ── 7. k-Means บน Utilities (k = 4) + Cluster Distance Performance (LAB 06 §6.2, สไลด์ clustering p.26) ──
m = Proc()
rd = m.add(read_csv("Read CSV", UTIL))
role = m.add(Op("set_role", "Set Role", {"attribute_name": "Company", "target_role": "id"}, x=180))
norm = m.add(Op("normalize", "Normalize", {"method": "Z-transformation"}, x=315))
chain(m, [rd, role, norm])
km = m.add(Op("concurrency:k_means", "Clustering", {
    "add_cluster_attribute": True, "k": 4, "max_runs": 50, "determine_good_start_values": True,
    "measure_types": "NumericalMeasures", "numerical_measure": "EuclideanDistance",
    "max_optimization_steps": 100, "use_local_random_seed": True, "local_random_seed": 42}, x=450))
cdp = m.add(Op("cluster_distance_performance", "Cluster Distance Performance", {
    "main_criterion": "Avg. within centroid distance", "main_criterion_only": False}, x=585))
m.wire(norm, "example set output", km, "example set")
m.wire(km, "clustered set", cdp, "example set")
m.wire(km, "cluster model", cdp, "cluster model")
perf_out(m, cdp, "performance", "Cluster", "kmeans_utilities_perf.csv", x=720)
wr = m.add(write_csv("Write CSV clustered", OUT / "kmeans_utilities_clusters.csv", x=720, y=200))
m.wire(cdp, "example set", wr, "input")
m.wire(wr, "through", None, "result 3")
m.wire(cdp, "cluster model", None, "result 4")
save(m, HERE / "kmeans_utilities.rmp")

# ── 8. Elbow ใน RapidMiner: Optimize Parameters (Grid) k = 2..10 + Log (สไลด์ clustering p.31) ────────
m = Proc()
rd = m.add(read_csv("Read CSV", UTIL))
role = m.add(Op("set_role", "Set Role", {"attribute_name": "Company", "target_role": "id"}, x=180))
norm = m.add(Op("normalize", "Normalize", {"method": "Z-transformation"}, x=315))
chain(m, [rd, role, norm])
inner = Proc()
km = inner.add(Op("concurrency:k_means", "Clustering", {
    "add_cluster_attribute": True, "k": 2, "max_runs": 50, "determine_good_start_values": True,
    "use_local_random_seed": True, "local_random_seed": 42}))
cdp = inner.add(Op("cluster_distance_performance", "Cluster Distance Performance", {
    "main_criterion": "Avg. within centroid distance"}, x=180))
log = inner.add(Op("log", "Log", {
    "log": ("list", [("k", "operator.Clustering.parameter.k"),
                     ("avg_within_centroid_distance",
                      "operator.Cluster Distance Performance.value.avg_within_distance")]),
    "sorting_type": "none", "persistent": False}, x=315))
inner.wire(None, "input 1", km, "example set")
inner.wire(km, "clustered set", cdp, "example set")
inner.wire(km, "cluster model", cdp, "cluster model")
inner.wire(cdp, "performance", log, "through 1")
inner.wire(log, "through 1", None, "performance")
opt = m.add(Op("concurrency:optimize_parameters_grid", "Optimize Parameters (Grid)", {
    "parameters": ("list", [("Clustering.k", "[2.0;10.0;8;linear]")])}, subprocesses=[inner], x=450))
m.wire(norm, "example set output", opt, "input 1")
l2d = m.add(Op("log_to_data", "Log to Data", {"log_name": "Log"}, x=585, y=34))
wr = m.add(write_csv("Write CSV log", OUT / "elbow_utilities_log.csv", x=720, y=34))
m.wire(l2d, "exampleSet", wr, "input")
m.wire(wr, "through", None, "result 1")
m.wire(opt, "parameter set", None, "result 2")
save(m, HERE / "elbow_kmeans.rmp")

# ── 9. FP-Growth + Create Association Rules บน BeautyCo (LAB 06 §6.3, สไลด์ Apriori p.39) ───────────
m = Proc()
rx = m.add(Op("read_excel", "Read Excel", {"excel_file": str(BEAUTY), "sheet_number": 1,
                                           "first_row_as_names": True}))
role = m.add(Op("set_role", "Set Role", {"attribute_name": "Trans.", "target_role": "id"}, x=180))
n2b = m.add(Op("numerical_to_binominal", "Numerical to Binominal", {
    "attribute_filter_type": "all", "min": 0.0, "max": 0.0}, x=315))
chain(m, [rx, role, n2b])
fp = m.add(Op("concurrency:fp_growth", "FP-Growth", {
    "input_format": "items in dummy coded columns", "positive_value": "true", "min_requirement": "support",
    "min_support": 0.2, "find_min_number_of_itemsets": False, "max_items_per_itemset": 0}, x=450))
car = m.add(Op("create_association_rules", "Create Association Rules", {
    "criterion": "confidence", "min_confidence": 0.7}, x=585))
m.wire(n2b, "example set output", fp, "example set")
m.wire(fp, "frequent sets", car, "item sets")
wt = m.add(Op("write_as_text", "Write Rules as Text", {"result_file": str(OUT / "beautyco_rules.txt")}, x=720))
m.wire(car, "rules", wt, "input 1")
m.wire(wt, "input 1", None, "result 1")
m.wire(car, "item sets", None, "result 2")
save(m, HERE / "fpgrowth_beautyco.rmp")

# ── 10. PCA 2 components สำหรับ visualization (LAB 03 §3.6, W13 Part IV) ───────────────────────────
m = Proc()
rd = m.add(read_csv("Read CSV", BANK))
sel = m.add(Op("select_attributes", "Select Attributes", {
    "attribute_filter_type": "subset", "attributes": "ID|ZIP Code", "invert_selection": True}, x=180))
n2b = m.add(Op("numerical_to_binominal", "Numerical to Binominal", {
    "attribute_filter_type": "single", "attribute": "Personal Loan", "min": 0.0, "max": 0.0}, x=315))
role = m.add(Op("set_role", "Set Role", {"attribute_name": "Personal Loan", "target_role": "label"}, x=450))
norm = m.add(Op("normalize", "Normalize", {"method": "Z-transformation"}, x=585))
pca = m.add(Op("principal_component_analysis", "PCA", {
    "dimensionality_reduction": "fixed number", "number_of_components": 2}, x=720))
chain(m, [rd, sel, n2b, role, norm, pca])
wr = m.add(write_csv("Write CSV pcs", OUT / "pca_bank_scores.csv", x=855))
m.wire(pca, "example set output", wr, "input")
m.wire(wr, "through", None, "result 1")
wt = m.add(Op("write_as_text", "Write PCA as Text", {"result_file": str(OUT / "pca_bank_model.txt")}, x=855, y=200))
m.wire(pca, "preprocessing model", wt, "input 1")
m.wire(wt, "input 1", None, "result 2")
save(m, HERE / "pca_bank.rmp")

# ── 11. Join (left) + Append + Pivot (LAB 02 §2.5–2.7) ────────────────────────────────────────────
DATA = HERE / "data"
DATA.mkdir(exist_ok=True)
(DATA / "customers.csv").write_text("cust_id,name,segment\n1,Ann,A\n2,Bo,B\n3,Cy,A\n4,Di,C\n")
(DATA / "orders.csv").write_text("cust_id,amount\n1,100\n1,250\n2,80\n5,40\n")
(DATA / "orders_q2.csv").write_text("cust_id,amount\n3,60\n4,90\n")
m = Proc()
rc = m.add(read_csv("Read customers", DATA / "customers.csv", y=34))
ro = m.add(read_csv("Read orders", DATA / "orders.csv", y=136))
rq = m.add(read_csv("Read orders Q2", DATA / "orders_q2.csv", y=238))
app = m.add(Op("append", "Append", {"merge_type": "all"}, x=180, y=187))
m.wire(ro, "output", app, "example set 1")
m.wire(rq, "output", app, "example set 2")
join = m.add(Op("concurrency:join", "Join", {
    "join_type": "left", "use_id_attribute_as_key": False,
    "key_attributes": ("list", [("cust_id", "cust_id")]), "remove_double_attributes": True}, x=315, y=85))
m.wire(rc, "output", join, "left")
m.wire(app, "merged set", join, "right")
rmv = m.add(Op("replace_missing_values", "Replace Missing Values", {
    "attribute_filter_type": "single", "attribute": "amount", "default": "zero"}, x=450, y=85))
m.wire(join, "join", rmv, "example set input")
agg = m.add(Op("aggregate", "Aggregate", {
    "use_default_aggregation": False, "group_by_attributes": "segment",
    "aggregation_attributes": ("list", [("amount", "sum"), ("cust_id", "count")])}, x=585, y=85))
m.wire(rmv, "example set output", agg, "example set input")
wr = m.add(write_csv("Write CSV agg", OUT / "join_append_aggregate.csv", x=720, y=85))
m.wire(agg, "example set output", wr, "input")
m.wire(wr, "through", None, "result 1")
# pivot: อัตรา churn ตาม Contract × InternetService
rch = m.add(read_csv("Read churn", CHURN, y=340))
gen = m.add(Op("generate_attributes", "Generate Attributes", {
    "function_descriptions": ("list", [("is_churn", 'if(Churn=="Yes", 1, 0)')])}, x=180, y=340))
piv = m.add(Op("blending:pivot", "Pivot", {
    "group_by_attributes": "Contract", "column_grouping_attribute": "InternetService",
    "aggregation_attributes": ("list", [("is_churn", "average")])}, x=315, y=340))
m.wire(rch, "output", gen, "example set input")
m.wire(gen, "example set output", piv, "input")
wr2 = m.add(write_csv("Write CSV pivot", OUT / "pivot_churn.csv", x=450, y=340))
m.wire(piv, "output", wr2, "input")
m.wire(wr2, "through", None, "result 2")
save(m, HERE / "join_append_pivot.rmp")

# ── 12. SMOTE ใน Training pane (ต้องติดตั้ง Operator Toolbox — ทดสอบแล้ว 2026-10-10) ────────────────
m = Proc()
rd = m.add(read_csv("Read CSV", CHURN))
sel = m.add(Op("select_attributes", "Select Attributes", {
    "attribute_filter_type": "subset", "attributes": "customerID", "invert_selection": True}, x=180))
rmv = m.add(Op("replace_missing_values", "Replace Missing Values", {"default": "zero"}, x=315))
role = m.add(Op("set_role", "Set Role", {"attribute_name": "Churn", "target_role": "label"}, x=450))
n2n = m.add(Op("nominal_to_numerical", "Nominal to Numerical", {"coding_type": "dummy coding"}, x=585))
chain(m, [rd, sel, rmv, role, n2n])
tr = Proc()
sm = tr.add(Op("operator_toolbox:smote", "SMOTE Upsampling", {
    "number_of_neighbours": 5, "normalize": True, "equalize_classes": True, "auto_detect_minority_class": True,
    "use_local_random_seed": True, "local_random_seed": 1992}))
dt = tr.add(Op("concurrency:parallel_decision_tree", "Decision Tree", {
    "criterion": "information_gain", "maximal_depth": 10, "apply_pruning": False}, x=180))
tr.wire(None, "training set", sm, "exa")          # port ของ SMOTE Upsampling: exa (เข้า) · ups (ออกหลัง upsample) · ori
tr.wire(sm, "ups", dt, "training set")
tr.wire(dt, "model", None, "model")
cv = m.add(cross_validation("Cross Validation", tr, testing_pane(perf_binominal()), folds=5, seed=1992, x=720))
m.wire(n2n, "example set output", cv, "example set")
m.wire(cv, "performance 1", None, "result 1")
save(m, HERE / "smote_cv_REQUIRES_OPERATOR_TOOLBOX.rmp")

print("✓ recipes:", ", ".join(sorted(p.name for p in HERE.glob("*.rmp"))))
