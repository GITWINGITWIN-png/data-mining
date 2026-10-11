"""สร้าง RapidMiner process เฉลยของ mock lab (รันทดสอบแล้วด้วย run_rm.sh)

- mock1_classification/solution_partC.rmp    — Append + Join + เตรียมข้อมูล + CV 3 โมเดล (baseline / k-NN / RF)
- mock2_regression_pca/solution_rapidminer.rmp — Linear Regression hold-out + k-NN regression CV + PCA
- mock3_cluster_assoc/solution_rapidminer.rmp  — k-Means (Utilities) + FP-Growth (bank-data)

รัน:  final/.venv/bin/python final/mock_lab/build_mock_rmp.py
"""
from pathlib import Path
from rm_builder import Op, Proc, save, read_csv, write_csv, cross_validation

HERE = Path(__file__).resolve().parent


def perf_csv(m, src, port, name, path, x, y, res):
    """PerformanceVector → res + Write CSV (ไว้ตรวจผลจาก batch)"""
    p2d = m.add(Op("performance_to_data", f"Performance to Data ({name})", {}, x=x, y=y))
    wr = m.add(write_csv(f"Write CSV ({name})", path, x=x + 135, y=y))
    m.wire(src, port, p2d, "performance vector")
    m.wire(p2d, "example set", wr, "input")
    m.wire(p2d, "performance vector", None, f"result {res}")


def testing(tag, kind="binominal", positive=None):
    te = Proc()
    ap = te.add(Op("apply_model", f"Apply Model ({tag})", {}))
    if kind == "binominal":
        pf = te.add(Op("performance_binominal_classification", f"Performance ({tag})", {
            "main_criterion": "f_measure", "accuracy": True, "precision": True, "recall": True,
            "f_measure": True}, x=180))
        if positive:   # กำหนด positive class เอง (ไม่งั้น RapidMiner ใช้ค่าที่ 2 ของ mapping ซึ่งอาจเป็นอีกคลาส)
            pf.params.update({"manually_set_positive_class": True, "positive_class": positive})
    else:
        pf = te.add(Op("performance_regression", f"Performance ({tag})", {
            "main_criterion": "root_mean_squared_error", "root_mean_squared_error": True,
            "absolute_error": True, "squared_correlation": True}, x=180))
    te.wire(None, "model", ap, "model")
    te.wire(None, "test set", ap, "unlabelled data")
    te.wire(ap, "labelled data", pf, "labelled data")
    te.wire(pf, "performance", None, "performance 1")
    return te


def training(tag, learner, steps):
    """Training pane: preprocessing ทุกตัวที่ "เรียนค่า" → learner → Group Models (กัน leakage)"""
    tr = Proc()
    prev, port = None, "training set"
    pre_models = []
    for i, op in enumerate(steps):
        op.name = f"{op.name} ({tag})"
        op.x = 45 + 135 * i
        tr.add(op)
        tr.wire(prev, port, op, "example set input")
        prev, port = op, "example set output"
        pre_models.append(op)
    learner.name = f"{learner.name} ({tag})"
    learner.x = 45 + 135 * len(steps)
    tr.add(learner)
    tr.wire(prev, port, learner, "training set")
    grp = tr.add(Op("group_models", f"Group Models ({tag})", {}, x=learner.x + 135))
    for i, op in enumerate(pre_models, start=1):
        tr.wire(op, "preprocessing model", grp, f"models in {i}")
    tr.wire(learner, "model", grp, f"models in {len(pre_models) + 1}")
    tr.wire(grp, "model out", None, "model")
    return tr


def replace_missing():
    return Op("replace_missing_values", "Replace Missing Values", {"default": "average",
                                                                  "return_preprocessing_model": True})


def dummy_coding():
    return Op("nominal_to_numerical", "Nominal to Numerical", {"coding_type": "dummy coding",
                                                              "return_preprocessing_model": True})


def normalize():
    return Op("normalize", "Normalize", {"method": "Z-transformation"})


# ── Mock 1 · Part C ───────────────────────────────────────────────────────────────────────────
D1 = HERE / "mock1_classification" / "data"
OUT1 = HERE / "mock1_classification" / "rm_out"
OUT1.mkdir(exist_ok=True)
m = Proc()
rp = m.add(read_csv("Read people", D1 / "people.csv", y=34))
r1 = m.add(read_csv("Read work H1", D1 / "work_2025H1.csv", y=136))
r2 = m.add(read_csv("Read work H2", D1 / "work_2025H2.csv", y=238))
app = m.add(Op("append", "Append", {"merge_type": "all"}, x=180, y=187))
m.wire(r1, "output", app, "example set 1")
m.wire(r2, "output", app, "example set 2")
join = m.add(Op("concurrency:join", "Join", {"join_type": "inner", "use_id_attribute_as_key": False,
                                             "key_attributes": ("list", [("person_id", "person_id")]),
                                             "remove_double_attributes": True}, x=315, y=85))
m.wire(rp, "output", join, "left")
m.wire(app, "merged set", join, "right")
dmv = m.add(Op("declare_missing_value", "Declare Missing Value", {
    "attribute_filter_type": "all", "mode": "nominal", "nominal_value": "?"}, x=450, y=85))
sel = m.add(Op("select_attributes", "Select Attributes", {
    "attribute_filter_type": "subset", "attributes": "fnlwgt|educational-num", "invert_selection": True},
    x=585, y=85))
role = m.add(Op("set_role", "Set Role", {"attribute_name": "income", "target_role": "label",
                                        "set_additional_roles": ("list", [("person_id", "id")])}, x=720, y=85))
m.wire(join, "join", dmv, "example set input")
for a, b in [(dmv, sel), (sel, role)]:
    m.wire(a, "example set output", b, "example set input")
mul = m.add(Op("multiply", "Multiply", {}, x=855, y=85))
m.wire(role, "example set output", mul, "input")
models = [
    ("Baseline", Op("default_model", "Default Model", {"method": "mode"}), []),
    ("k-NN", Op("k_nn", "k-NN", {"k": 25}), [replace_missing(), dummy_coding(), normalize()]),
    ("RF", Op("concurrency:parallel_random_forest", "Random Forest", {
        "number_of_trees": 100, "criterion": "gini_index", "maximal_depth": 20, "guess_subset_ratio": True,
        "use_local_random_seed": True, "local_random_seed": 1992}), [replace_missing()]),
]
for i, (tag, learner, steps) in enumerate(models):
    cv = m.add(cross_validation(f"CV {tag}", training(tag, learner, steps), testing(tag, positive=">50K"),
                                folds=5, seed=1992, x=1125, y=34 + 153 * i))
    m.wire(mul, f"output {i + 1}", cv, "example set")
    perf_csv(m, cv, "performance 1", tag, OUT1 / f"partC_{tag}.csv", x=1260, y=34 + 153 * i, res=i + 1)
save(m, HERE / "mock1_classification" / "solution_partC.rmp")

# ── Mock 2 ───────────────────────────────────────────────────────────────────────────────────
D2 = HERE / "mock2_regression_pca" / "data"
OUT2 = HERE / "mock2_regression_pca" / "rm_out"
OUT2.mkdir(exist_ok=True)
m = Proc()
rd = m.add(read_csv("Read housing", D2 / "housing.csv"))
role = m.add(Op("set_role", "Set Role", {"attribute_name": "medv", "target_role": "label"}, x=180))
m.wire(rd, "output", role, "example set input")
mul = m.add(Op("multiply", "Multiply", {}, x=315))
m.wire(role, "example set output", mul, "input")
# (B) Linear Regression hold-out 80/20
split = m.add(Op("split_data", "Split Data", {"partitions": ("enum", [0.8, 0.2], "ratio"),
                                              "sampling_type": "shuffled sampling",
                                              "use_local_random_seed": True, "local_random_seed": 1992},
                 x=450, y=34))
lin = m.add(Op("linear_regression", "Linear Regression", {"feature_selection": "none"}, x=585, y=34))
ap = m.add(Op("apply_model", "Apply Model (LinReg)", {}, x=720, y=34))
pr = m.add(Op("performance_regression", "Performance (LinReg)", {
    "root_mean_squared_error": True, "absolute_error": True, "squared_error": True,
    "squared_correlation": True}, x=855, y=34))
m.wire(mul, "output 1", split, "example set")
m.wire(split, "partition 1", lin, "training set")
m.wire(lin, "model", ap, "model")
m.wire(split, "partition 2", ap, "unlabelled data")
m.wire(ap, "labelled data", pr, "labelled data")
perf_csv(m, pr, "performance", "LinReg", OUT2 / "linreg_holdout.csv", x=990, y=34, res=1)
# (C) k-NN regression: ไม่ normalize vs normalize ใน 5-fold CV
cv_raw = m.add(cross_validation("CV k-NN raw", training("raw", Op("k_nn", "k-NN", {"k": 5}), []),
                                testing("raw", "regression"), folds=5, seed=1992, x=450, y=187))
cv_raw.params["sampling_type"] = "shuffled sampling"         # label ตัวเลข → stratified ใช้ไม่ได้
cv_sc = m.add(cross_validation("CV k-NN scaled", training("scaled", Op("k_nn", "k-NN", {"k": 5}), [normalize()]),
                               testing("scaled", "regression"), folds=5, seed=1992, x=450, y=340))
cv_sc.params["sampling_type"] = "shuffled sampling"
m.wire(mul, "output 2", cv_raw, "example set")
m.wire(mul, "output 3", cv_sc, "example set")
perf_csv(m, cv_raw, "performance 1", "kNN raw", OUT2 / "knn_raw_cv.csv", x=585, y=187, res=2)
perf_csv(m, cv_sc, "performance 1", "kNN scaled", OUT2 / "knn_scaled_cv.csv", x=585, y=340, res=3)
# (D) PCA บน feature ที่ normalize แล้ว (label ไม่ถูกแตะ เพราะเป็น special attribute)
norm = m.add(Op("normalize", "Normalize (PCA)", {"method": "Z-transformation"}, x=450, y=493))
pca = m.add(Op("principal_component_analysis", "PCA", {"dimensionality_reduction": "keep variance",
                                                     "variance_threshold": 0.8}, x=585, y=493))
m.wire(mul, "output 4", norm, "example set input")
m.wire(norm, "example set output", pca, "example set input")
wt = m.add(Op("write_as_text", "Write PCA as Text", {"result_file": str(OUT2 / "pca_model.txt")}, x=720, y=493))
m.wire(pca, "preprocessing model", wt, "input 1")
m.wire(wt, "input 1", None, "result 4")
m.wire(pca, "example set output", None, "result 5")
save(m, HERE / "mock2_regression_pca" / "solution_rapidminer.rmp")

# ── Mock 3 ───────────────────────────────────────────────────────────────────────────────────
D3 = HERE / "mock3_cluster_assoc" / "data"
OUT3 = HERE / "mock3_cluster_assoc" / "rm_out"
OUT3.mkdir(exist_ok=True)
m = Proc()
# (A) k-Means
ru = m.add(read_csv("Read utilities", D3 / "utilities.csv", y=34))
role = m.add(Op("set_role", "Set Role", {"attribute_name": "Company", "target_role": "id"}, x=180, y=34))
norm = m.add(Op("normalize", "Normalize", {"method": "Z-transformation"}, x=315, y=34))
km = m.add(Op("concurrency:k_means", "Clustering", {"add_cluster_attribute": True, "k": 4, "max_runs": 50,
                                                   "determine_good_start_values": True,
                                                   "use_local_random_seed": True, "local_random_seed": 1992},
              x=450, y=34))
cdp = m.add(Op("cluster_distance_performance", "Cluster Distance Performance", {
    "main_criterion": "Davies Bouldin"}, x=585, y=34))
m.wire(ru, "output", role, "example set input")
m.wire(role, "example set output", norm, "example set input")
m.wire(norm, "example set output", km, "example set")
m.wire(km, "clustered set", cdp, "example set")
m.wire(km, "cluster model", cdp, "cluster model")
perf_csv(m, cdp, "performance", "Cluster", OUT3 / "kmeans_perf.csv", x=720, y=34, res=1)
wr = m.add(write_csv("Write CSV (clusters)", OUT3 / "kmeans_clusters.csv", x=720, y=136))
m.wire(cdp, "example set", wr, "input")
m.wire(wr, "through", None, "result 2")
# (B) FP-Growth บน bank-data
rb = m.add(read_csv("Read bank", D3 / "bank-data.csv", y=289))
sel = m.add(Op("select_attributes", "Select Attributes", {
    "attribute_filter_type": "subset", "attributes": "id|region|sex|current_act", "invert_selection": True},
    x=180, y=289))
dfq = m.add(Op("discretize_by_frequency", "Discretize by Frequency", {
    "attribute_filter_type": "subset", "attributes": "age|income", "number_of_bins": 3,
    "range_name_type": "short"}, x=315, y=289))
dus = m.add(Op("discretize_by_user_specification", "Discretize by User Specification", {
    "attribute_filter_type": "single", "attribute": "children",
    "classes": ("list", [("0", 0.5), ("1-2", 2.5), ("3+", "Infinity")])}, x=450, y=289))
n2b = m.add(Op("nominal_to_binominal", "Nominal to Binominal", {"attribute_filter_type": "all",
                                                               "transform_binominal": True}, x=585, y=289))
fp = m.add(Op("concurrency:fp_growth", "FP-Growth", {
    "input_format": "items in dummy coded columns", "positive_value": "true", "min_requirement": "support",
    "min_support": 0.1, "find_min_number_of_itemsets": False}, x=720, y=289))
car = m.add(Op("create_association_rules", "Create Association Rules", {
    "criterion": "confidence", "min_confidence": 0.7}, x=855, y=289))
m.wire(rb, "output", sel, "example set input")
for a, b in [(sel, dfq), (dfq, dus), (dus, n2b)]:
    m.wire(a, "example set output", b, "example set input")
m.wire(n2b, "example set output", fp, "example set")
m.wire(fp, "frequent sets", car, "item sets")
wt = m.add(Op("write_as_text", "Write Rules as Text", {"result_file": str(OUT3 / "bank_rules.txt")}, x=990, y=289))
m.wire(car, "rules", wt, "input 1")
m.wire(wt, "input 1", None, "result 3")
save(m, HERE / "mock3_cluster_assoc" / "solution_rapidminer.rmp")

print("✓ mock solution processes built")
