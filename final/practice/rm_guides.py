"""ไกด์ RapidMiner โจทย์ P1–P9: สร้าง process เฉลย → รันจริงด้วย batch runner → เขียนไกด์ที่มีผลจริง

รัน:  final/.venv/bin/python final/practice/rm_guides.py
ผล:   final/practice/rm/PXX_solution.rmp (import เปิดดูได้) · final/obsidian/practice/PR XX … (RapidMiner).md
"""
import subprocess
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "mock_lab"))
from rm_builder import Op, Proc, save, read_csv, write_csv, cross_validation  # noqa: E402

DATA = HERE / "data"
RM = HERE / "rm"
OUT = RM / "out"
OUT.mkdir(parents=True, exist_ok=True)
VAULT = HERE.parent / "obsidian" / "practice"
RUNNER = HERE.parent / "mock_lab" / "run_rm.sh"


# ── ตัวช่วยสร้าง process ─────────────────────────────────────────────────────────────────────
def ex(proc, a, b, a_port="example set output", b_port="example set input"):
    src = "output" if a.cls in ("read_csv", "read_excel") else a_port
    proc.wire(a, src, b, b_port)


def perf_csv(m, src, port, tag, res, x=900, y=85):
    p2d = m.add(Op("performance_to_data", f"Performance to Data ({tag})", {}, x=x, y=y))
    wr = m.add(write_csv(f"Write CSV ({tag})", OUT / f"{tag}.csv", x=x + 135, y=y))
    m.wire(src, port, p2d, "performance vector")
    m.wire(p2d, "example set", wr, "input")
    m.wire(p2d, "performance vector", None, f"result {res}")


def data_csv(m, src, port, tag, res, x=900, y=85):
    wr = m.add(write_csv(f"Write CSV ({tag})", OUT / f"{tag}.csv", x=x, y=y))
    m.wire(src, port, wr, "input")
    m.wire(wr, "through", None, f"result {res}")


def text_out(m, src, port, tag, res, x=900, y=85):
    wt = m.add(Op("write_as_text", f"Write as Text ({tag})", {"result_file": str(OUT / f"{tag}.txt")}, x=x, y=y))
    m.wire(src, port, wt, "input 1")
    m.wire(wt, "input 1", None, f"result {res}")


def binom_perf(tag, positive=None, main="f_measure"):
    p = {"main_criterion": main, "accuracy": True, "precision": True, "recall": True, "f_measure": True}
    if positive:
        p.update({"manually_set_positive_class": True, "positive_class": positive})
    return Op("performance_binominal_classification", f"Performance ({tag})", p, x=180)


def multi_perf(tag):
    return Op("performance_classification", f"Performance ({tag})", {
        "main_criterion": "accuracy", "accuracy": True, "kappa": True}, x=180)


def reg_perf(tag):
    return Op("performance_regression", f"Performance ({tag})", {
        "main_criterion": "root_mean_squared_error", "root_mean_squared_error": True,
        "absolute_error": True, "squared_correlation": True}, x=180)


def testing(tag, perf):
    te = Proc()
    ap = te.add(Op("apply_model", f"Apply Model ({tag})", {}))
    te.add(perf)
    te.wire(None, "model", ap, "model")
    te.wire(None, "test set", ap, "unlabelled data")
    te.wire(ap, "labelled data", perf, "labelled data")
    te.wire(perf, "performance", None, "performance 1")
    return te


def training(tag, learner, steps=(), learner_in="training set"):
    """steps = operator preprocessing ที่ต้องอยู่ใน Training pane (คืน preprocessing model) → Group Models"""
    tr = Proc()
    prev, port = None, "training set"
    for i, op in enumerate(steps):
        op.name, op.x = f"{op.name} ({tag})", 45 + 135 * i
        tr.add(op)
        in_port = "exa" if op.cls == "operator_toolbox:smote" else "example set input"
        tr.wire(prev, port, op, in_port)
        prev, port = op, ("ups" if op.cls == "operator_toolbox:smote" else "example set output")
    learner.name, learner.x = f"{learner.name} ({tag})", 45 + 135 * len(steps)
    tr.add(learner)
    tr.wire(prev, port, learner, learner_in)
    models = [op for op in steps if op.cls in ("normalize", "replace_missing_values", "nominal_to_numerical",
                                               "principal_component_analysis")]
    if models:
        grp = tr.add(Op("group_models", f"Group Models ({tag})", {}, x=learner.x + 135))
        for i, op in enumerate(models, start=1):
            tr.wire(op, "preprocessing model", grp, f"models in {i}")
        tr.wire(learner, "model", grp, f"models in {len(models) + 1}")
        tr.wire(grp, "model out", None, "model")
    else:
        tr.wire(learner, "model", None, "model")
    return tr


def norm():
    return Op("normalize", "Normalize", {"method": "Z-transformation"})


def cv(tag, learner, perf, steps=(), folds=10, seed=1992, sampling="stratified sampling", x=600, y=85):
    op = cross_validation(f"CV {tag}", training(tag, learner, steps), testing(tag, perf), folds=folds, seed=seed, x=x, y=y)
    op.params["sampling_type"] = sampling
    return op


def log_opt(m, src, src_port, inner_cv, param, grid, log_cols, tag, res, x=600, y=85):
    """Optimize Parameters (Grid) ครอบ CV + Log → Log to Data → CSV"""
    inner = Proc()
    inner.add(inner_cv)
    log = inner.add(Op("log", "Log", {"log": ("list", log_cols), "sorting_type": "none", "persistent": False}, x=180))
    inner.wire(None, "input 1", inner_cv, "example set")
    inner.wire(inner_cv, "performance 1", log, "through 1")
    inner.wire(log, "through 1", None, "performance")
    opt = m.add(Op("concurrency:optimize_parameters_grid", f"Optimize Parameters ({tag})", {
        "parameters": ("list", [(param, grid)])}, subprocesses=[inner], x=x, y=y))
    m.wire(src, src_port, opt, "input 1")
    l2d = m.add(Op("log_to_data", f"Log to Data ({tag})", {"log_name": "Log"}, x=x + 135, y=y))
    data_csv(m, l2d, "exampleSet", tag, res, x=x + 270, y=y)
    m.wire(opt, "performance", None, f"result {res + 1}")
    return opt


def cv_value(cv_name):
    return f"operator.{cv_name}.value.performance main criterion"


BUILDERS = {}


def builder(fn):
    BUILDERS[fn.__name__] = fn
    return fn


# ════════════════════════════════════ P1 · Data Handling ═══════════════════════════════════════
@builder
def p1():
    m = Proc()
    r1 = m.add(read_csv("Read week1", DATA / "p1_bills_week1.csv", y=34))
    r2 = m.add(read_csv("Read week2", DATA / "p1_bills_week2.csv", y=136))
    rd = m.add(read_csv("Read day_info", DATA / "p1_day_info.csv", y=238))
    app = m.add(Op("append", "Append", {"merge_type": "all"}, x=180, y=85))
    m.wire(r1, "output", app, "example set 1"); m.wire(r2, "output", app, "example set 2")
    join = m.add(Op("concurrency:join", "Join", {"join_type": "left", "use_id_attribute_as_key": False,
                                                 "key_attributes": ("list", [("day", "day")]),
                                                 "remove_double_attributes": True}, x=315, y=85))
    m.wire(app, "merged set", join, "left"); m.wire(rd, "output", join, "right")
    gen = m.add(Op("generate_attributes", "Generate Attributes", {
        "function_descriptions": ("list", [("tip_pct", "tip / total_bill * 100")])}, x=450, y=85))
    m.wire(join, "join", gen, "example set input")
    mul = m.add(Op("multiply", "Multiply", {}, x=585, y=85))
    m.wire(gen, "example set output", mul, "input")
    flt = m.add(Op("filter_examples", "Filter Examples", {
        "condition_class": "custom_filters", "filters_logic_and": True,
        "filters_list": ("list", [("filters_entry_key", "time.equals.Dinner"), ("filters_entry_key", "size.ge.4")])},
        x=720, y=34))
    m.wire(mul, "output 1", flt, "example set input")
    data_csv(m, flt, "example set output", "p1_filter", 1, x=855, y=34)
    agg = m.add(Op("aggregate", "Aggregate", {"use_default_aggregation": False, "group_by_attributes": "day",
                                              "aggregation_attributes": ("list", [("bill_id", "count"), ("total_bill", "average"),
                                                                                  ("tip_pct", "average")])}, x=720, y=136))
    m.wire(mul, "output 2", agg, "example set input")
    data_csv(m, agg, "example set output", "p1_aggregate", 2, x=855, y=136)
    piv = m.add(Op("blending:pivot", "Pivot", {"group_by_attributes": "day", "column_grouping_attribute": "time",
                                               "aggregation_attributes": ("list", [("tip_pct", "average")])}, x=720, y=238))
    m.wire(mul, "output 3", piv, "input")
    data_csv(m, piv, "output", "p1_pivot", 3, x=855, y=238)
    data_csv(m, mul, "output 4", "p1_all", 4, x=720, y=340)
    return save(m, RM / "P01_solution.rmp")


# ════════════════════════════════════ P2 · Preprocessing & PCA ═════════════════════════════════
@builder
def p2():
    m = Proc()
    rd = m.add(read_csv("Read CSV", DATA / "p2_penguins.csv"))
    flt = m.add(Op("filter_examples", "Filter Examples", {
        "condition_class": "custom_filters", "filters_list": ("list", [("filters_entry_key", "body_mass_g.is_not_missing.")])}, x=180))
    role = m.add(Op("set_role", "Set Role", {"attribute_name": "species", "target_role": "label"}, x=315))
    ex(m, rd, flt); ex(m, flt, role)
    mul = m.add(Op("multiply", "Multiply", {}, x=450))
    m.wire(role, "example set output", mul, "input")
    # (ก) PCA เพื่อ visualization: Replace Missing → Select ตัวเลข → Normalize → PCA 2 PC
    sel = m.add(Op("select_attributes", "Select Attributes", {"attribute_filter_type": "value_type", "value_type": "numeric"}, x=585, y=34))
    nm = m.add(norm()); nm.x, nm.y = 720, 34
    pca = m.add(Op("principal_component_analysis", "PCA", {"dimensionality_reduction": "fixed number",
                                                           "number_of_components": 2}, x=855, y=34))
    m.wire(mul, "output 1", sel, "example set input"); ex(m, sel, nm); ex(m, nm, pca)
    data_csv(m, pca, "example set output", "p2_pca_scores", 1, x=990, y=34)
    text_out(m, pca, "preprocessing model", "p2_pca_model", 2, x=990, y=136)
    # (ข) Discretize body mass 3 ช่วงจำนวนเท่ากัน
    dfq = m.add(Op("discretize_by_frequency", "Discretize by Frequency", {
        "attribute_filter_type": "single", "attribute": "body_mass_g", "number_of_bins": 3, "range_name_type": "short"}, x=585, y=238))
    m.wire(mul, "output 2", dfq, "example set input")
    agg = m.add(Op("aggregate", "Aggregate", {"use_default_aggregation": False, "group_by_attributes": "body_mass_g|species",
                                              "aggregation_attributes": ("list", [("island", "count")])}, x=720, y=238))
    ex(m, dfq, agg)
    data_csv(m, agg, "example set output", "p2_mass_bins", 3, x=855, y=238)
    # (ค) KNN ใน CV: Replace Missing + Nominal to Numerical + Normalize อยู่ใน Training pane
    c = m.add(cv("p2_knn", Op("k_nn", "k-NN", {"k": 5}), multi_perf("p2_knn"),
                 steps=[Op("replace_missing_values", "Replace Missing Values", {"default": "average", "return_preprocessing_model": True}),
                        Op("nominal_to_numerical", "Nominal to Numerical", {"coding_type": "dummy coding", "return_preprocessing_model": True}),
                        norm()], folds=5, x=585, y=340))
    m.wire(mul, "output 3", c, "example set")
    perf_csv(m, c, "performance 1", "p2_knn", 4, x=720, y=340)
    c2 = m.add(cv("p2_knn_raw", Op("k_nn", "k-NN", {"k": 5}), multi_perf("p2_knn_raw"),
                  steps=[Op("replace_missing_values", "Replace Missing Values", {"default": "average", "return_preprocessing_model": True}),
                         Op("nominal_to_numerical", "Nominal to Numerical", {"coding_type": "dummy coding", "return_preprocessing_model": True})],
                  folds=5, x=585, y=442))
    m.wire(mul, "output 4", c2, "example set")
    perf_csv(m, c2, "performance 1", "p2_knn_raw", 5, x=720, y=442)
    return save(m, RM / "P02_solution.rmp")


# ════════════════════════════════════ P3 · Imbalanced ══════════════════════════════════════════
@builder
def p3():
    m = Proc()
    rd = m.add(read_csv("Read CSV", DATA / "p3_breast_cancer_imbalanced.csv"))
    role = m.add(Op("set_role", "Set Role", {"attribute_name": "diagnosis", "target_role": "label"}, x=180))
    ex(m, rd, role)
    mul = m.add(Op("multiply", "Multiply", {}, x=315))
    m.wire(role, "example set output", mul, "input")
    tree = lambda: Op("concurrency:parallel_decision_tree", "Decision Tree", {
        "criterion": "gini_index", "maximal_depth": 4, "apply_pruning": False, "apply_prepruning": False})
    variants = [
        ("p3_baseline", Op("default_model", "Default Model", {"method": "mode"}), []),
        ("p3_tree", tree(), []),
        ("p3_rus", tree(), [Op("sample", "Sample", {"sample": "absolute", "balance_data": True,
                                                    "sample_size_per_class": ("list", [("benign", 32), ("malignant", 32)]),
                                                    "use_local_random_seed": True, "local_random_seed": 1992})]),
        ("p3_smote", tree(), [Op("operator_toolbox:smote", "SMOTE Upsampling", {
            "number_of_neighbours": 5, "normalize": True, "equalize_classes": True, "auto_detect_minority_class": True,
            "use_local_random_seed": True, "local_random_seed": 1992})]),
    ]
    for i, (tag, learner, steps) in enumerate(variants):
        c = m.add(cv(tag, learner, binom_perf(tag, positive="malignant"), steps=steps, folds=5, x=450, y=34 + 102 * i))
        m.wire(mul, f"output {i + 1}", c, "example set")
        perf_csv(m, c, "performance 1", tag, i + 1, x=585, y=34 + 102 * i)
    return save(m, RM / "P03_solution.rmp")


# ════════════════════════════════════ P4 · KNN ═════════════════════════════════════════════════
@builder
def p4():
    m = Proc()
    rd = m.add(read_csv("Read CSV", DATA / "p4_wine.csv"))
    role = m.add(Op("set_role", "Set Role", {"attribute_name": "cultivar", "target_role": "label"}, x=180))
    ex(m, rd, role)
    mul = m.add(Op("multiply", "Multiply", {}, x=315))
    m.wire(role, "example set output", mul, "input")
    for i, (tag, learner, steps) in enumerate([
            ("p4_baseline", Op("default_model", "Default Model", {"method": "mode"}), []),
            ("p4_knn_raw", Op("k_nn", "k-NN", {"k": 5}), []),
            ("p4_knn_norm", Op("k_nn", "k-NN", {"k": 5}), [norm()])]):
        c = m.add(cv(tag, learner, multi_perf(tag), steps=steps, x=450, y=34 + 102 * i))
        m.wire(mul, f"output {i + 1}", c, "example set")
        perf_csv(m, c, "performance 1", tag, i + 1, x=585, y=34 + 102 * i)
    inner = cv("p4_opt", Op("k_nn", "k-NN", {"k": 5}), multi_perf("p4_opt"), steps=[norm()])
    log_opt(m, mul, "output 4", inner, "k-NN (p4_opt).k", "[1.0;30.0;29;linear]",
            [("k", "operator.k-NN (p4_opt).parameter.k"), ("accuracy", cv_value("CV p4_opt"))], "p4_opt_log", 4, x=450, y=340)
    return save(m, RM / "P04_solution.rmp")


# ════════════════════════════════════ P5 · Logistic ════════════════════════════════════════════
@builder
def p5():
    m = Proc()
    rd = m.add(read_csv("Read CSV", DATA / "p5_pima_diabetes.csv"))
    n2b = m.add(Op("numerical_to_binominal", "Numerical to Binominal", {"attribute_filter_type": "single",
                                                                        "attribute": "diabetes", "min": 0.0, "max": 0.0}, x=180))
    role = m.add(Op("set_role", "Set Role", {"attribute_name": "diabetes", "target_role": "label"}, x=315))
    dmv = m.add(Op("declare_missing_value", "Declare Missing Value", {
        "attribute_filter_type": "subset", "attributes": "glucose|blood_pressure|skin_thickness|insulin|bmi",
        "mode": "numeric", "numeric_value": 0.0}, x=450))
    ex(m, rd, n2b); ex(m, n2b, role); ex(m, role, dmv)
    split = m.add(Op("split_data", "Split Data", {"partitions": ("enum", [0.75, 0.25], "ratio"),
                                                  "sampling_type": "stratified sampling",
                                                  "use_local_random_seed": True, "local_random_seed": 1992}, x=585))
    m.wire(dmv, "example set output", split, "example set")
    rmv = m.add(Op("replace_missing_values", "Replace Missing Values", {"default": "average",
                                                                        "return_preprocessing_model": True}, x=720, y=34))
    lr = m.add(Op("h2o:logistic_regression", "Logistic Regression", {
        "solver": "AUTO", "reproducible": True, "use_regularization": False, "standardize": True,
        "compute_p-values": True, "remove_collinear_columns": True}, x=855, y=34))
    m.wire(split, "partition 1", rmv, "example set input")
    m.wire(rmv, "example set output", lr, "training set")
    ap1 = m.add(Op("apply_model", "Apply Model (impute test)", {}, x=720, y=187))
    m.wire(rmv, "preprocessing model", ap1, "model"); m.wire(split, "partition 2", ap1, "unlabelled data")
    ap2 = m.add(Op("apply_model", "Apply Model (logistic)", {}, x=855, y=187))
    m.wire(lr, "model", ap2, "model"); m.wire(ap1, "labelled data", ap2, "unlabelled data")
    mul = m.add(Op("multiply", "Multiply", {}, x=990, y=187))
    m.wire(ap2, "labelled data", mul, "input")
    # ⚠️ prediction ของ H2O Logistic Regression ใช้ threshold ที่ทำให้ F1 สูงสุด (ไม่ใช่ 0.5)
    #    → ต้อง Create Threshold + Apply Threshold เองทุกครั้งที่โจทย์กำหนด threshold
    pfd = m.add(binom_perf("p5_default", positive="true")); pfd.x, pfd.y = 1125, 85
    m.wire(mul, "output 1", pfd, "labelled data")
    perf_csv(m, pfd, "performance", "p5_default", 1, x=1260, y=85)
    for j, t in enumerate([0.5, 0.3], start=2):
        tag = f"p5_t{int(t * 100):03d}"
        thr = m.add(Op("create_threshold", f"Create Threshold {t}", {"threshold": t, "first_class": "false", "second_class": "true"}, x=990, y=136 + 153 * j))
        apt = m.add(Op("apply_threshold", f"Apply Threshold {t}", {}, x=1125, y=187 + 153 * j))
        m.wire(mul, f"output {j}", apt, "example set"); m.wire(thr, "output", apt, "threshold")
        pf = m.add(binom_perf(tag, positive="true")); pf.x, pf.y = 1260, 187 + 153 * j
        m.wire(apt, "example set", pf, "labelled data")
        perf_csv(m, pf, "performance", tag, j, x=1395, y=187 + 153 * j)
    text_out(m, ap2, "model", "p5_model", 4, x=990, y=34)         # Apply Model ส่ง model ต่อออกมาให้ (port model ของ learner ต่อได้เส้นเดียว)
    return save(m, RM / "P05_solution.rmp")


# ════════════════════════════════════ P6 · Tree vs RF ══════════════════════════════════════════
@builder
def p6():
    m = Proc()
    rd = m.add(read_csv("Read CSV", DATA / "p6_heart.csv"))
    n2b = m.add(Op("numerical_to_binominal", "Numerical to Binominal", {"attribute_filter_type": "single",
                                                                        "attribute": "target", "min": 0.0, "max": 0.0}, x=180))
    role = m.add(Op("set_role", "Set Role", {"attribute_name": "target", "target_role": "label"}, x=315))
    ex(m, rd, n2b); ex(m, n2b, role)
    mul = m.add(Op("multiply", "Multiply", {}, x=450))
    m.wire(role, "example set output", mul, "input")
    full = lambda: Op("concurrency:parallel_decision_tree", "Decision Tree", {
        "criterion": "gini_index", "maximal_depth": 30, "apply_pruning": False, "apply_prepruning": False})
    d3 = lambda: Op("concurrency:parallel_decision_tree", "Decision Tree", {
        "criterion": "gini_index", "maximal_depth": 3, "apply_pruning": False, "apply_prepruning": False})
    rf = Op("concurrency:parallel_random_forest", "Random Forest", {
        "number_of_trees": 300, "criterion": "gini_index", "maximal_depth": 10, "guess_subset_ratio": True,
        "use_local_random_seed": True, "local_random_seed": 1992})
    for i, (tag, learner) in enumerate([("p6_tree_full", full()), ("p6_tree_d3", d3()), ("p6_rf", rf)]):
        c = m.add(cv(tag, learner, binom_perf(tag, positive="true", main="accuracy"), x=585, y=34 + 102 * i))
        m.wire(mul, f"output {i + 1}", c, "example set")
        perf_csv(m, c, "performance 1", tag, i + 1, x=720, y=34 + 102 * i)
    # train accuracy ของ tree โตเต็ม: train บนข้อมูลทั้งหมดแล้ววัดบนข้อมูลเดิม
    mt = m.add(full()); mt.name, mt.x, mt.y = "Decision Tree (train acc)", 585, 340
    m.wire(mul, "output 4", mt, "training set")
    ap = m.add(Op("apply_model", "Apply Model (train acc)", {}, x=720, y=340))
    m.wire(mt, "model", ap, "model"); m.wire(mul, "output 6", ap, "unlabelled data")
    pf = m.add(binom_perf("p6_train_full", positive="true", main="accuracy")); pf.x, pf.y = 855, 340
    m.wire(ap, "labelled data", pf, "labelled data")
    perf_csv(m, pf, "performance", "p6_train_full", 4, x=990, y=340)
    inner = cv("p6_opt", d3(), binom_perf("p6_opt", positive="true", main="accuracy"))
    log_opt(m, mul, "output 5", inner, "Decision Tree (p6_opt).maximal_depth", "[1.0;12.0;11;linear]",
            [("depth", "operator.Decision Tree (p6_opt).parameter.maximal_depth"), ("accuracy", cv_value("CV p6_opt"))],
            "p6_opt_log", 5, x=585, y=442)
    return save(m, RM / "P06_solution.rmp")


# ════════════════════════════════════ P7 · Regression ══════════════════════════════════════════
@builder
def p7():
    m = Proc()
    rd = m.add(read_csv("Read CSV", DATA / "p7_insurance.csv"))
    role = m.add(Op("set_role", "Set Role", {"attribute_name": "charges", "target_role": "label"}, x=180))
    n2n = m.add(Op("nominal_to_numerical", "Nominal to Numerical", {"coding_type": "dummy coding",
                                                                    "use_comparison_groups": True,
                                                                    "comparison_groups": ("list", [("sex", "female"), ("smoker", "no"), ("region", "northeast")])}, x=315))
    ex(m, rd, role); ex(m, role, n2n)
    split = m.add(Op("split_data", "Split Data", {"partitions": ("enum", [0.8, 0.2], "ratio"), "sampling_type": "shuffled sampling",
                                                  "use_local_random_seed": True, "local_random_seed": 1992}, x=450))
    m.wire(n2n, "example set output", split, "example set")
    mtr = m.add(Op("multiply", "Multiply (train)", {}, x=585, y=34))
    mte = m.add(Op("multiply", "Multiply (test)", {}, x=585, y=238))
    m.wire(split, "partition 1", mtr, "input"); m.wire(split, "partition 2", mte, "input")
    for i, (tag, learner) in enumerate([("p7_baseline", Op("default_model", "Default Model", {"method": "average"})),
                                        ("p7_linreg", Op("linear_regression", "Linear Regression", {"feature_selection": "none"}))]):
        learner.name = f"{learner.name} ({tag})"; learner.x, learner.y = 720, 34 + 153 * i
        m.add(learner)
        m.wire(mtr, f"output {i + 1}", learner, "training set")
        ap = m.add(Op("apply_model", f"Apply Model ({tag})", {}, x=855, y=34 + 153 * i))
        m.wire(learner, "model", ap, "model"); m.wire(mte, f"output {i + 1}", ap, "unlabelled data")
        pf = m.add(reg_perf(tag)); pf.x, pf.y = 990, 34 + 153 * i
        m.wire(ap, "labelled data", pf, "labelled data")
        perf_csv(m, pf, "performance", tag, i + 1, x=1125, y=34 + 153 * i)
        if tag == "p7_linreg":
            text_out(m, ap, "model", "p7_linreg_model", 3, x=990, y=289)
    # KNN regression: Normalize → k-NN บน train, ใช้ model เดียวกันกับ test
    nm = m.add(norm()); nm.x, nm.y = 720, 340
    knn = m.add(Op("k_nn", "k-NN (p7)", {"k": 10, "weighted_vote": True}, x=855, y=340))
    m.wire(mtr, "output 3", nm, "example set input"); m.wire(nm, "example set output", knn, "training set")
    a1 = m.add(Op("apply_model", "Apply Model (normalize test)", {}, x=855, y=442))
    m.wire(nm, "preprocessing model", a1, "model"); m.wire(mte, "output 3", a1, "unlabelled data")
    a2 = m.add(Op("apply_model", "Apply Model (knn)", {}, x=990, y=442))
    m.wire(knn, "model", a2, "model"); m.wire(a1, "labelled data", a2, "unlabelled data")
    pf = m.add(reg_perf("p7_knn")); pf.x, pf.y = 1125, 442
    m.wire(a2, "labelled data", pf, "labelled data")
    perf_csv(m, pf, "performance", "p7_knn", 4, x=1260, y=442)
    inner = cv("p7_opt", Op("k_nn", "k-NN", {"k": 5, "weighted_vote": True}), reg_perf("p7_opt"), steps=[norm()],
               folds=5, sampling="shuffled sampling")
    log_opt(m, mtr, "output 4", inner, "k-NN (p7_opt).k", "[1.0;30.0;29;linear]",
            [("k", "operator.k-NN (p7_opt).parameter.k"), ("rmse", cv_value("CV p7_opt"))], "p7_opt_log", 5, x=720, y=544)
    return save(m, RM / "P07_solution.rmp")


# ════════════════════════════════════ P8 · K-Means ═════════════════════════════════════════════
@builder
def p8():
    m = Proc()
    rd = m.add(read_csv("Read CSV", DATA / "p8_wine_unlabeled.csv"))
    role = m.add(Op("set_role", "Set Role", {"attribute_name": "cultivar", "target_role": "label"}, x=180))
    nm = m.add(norm()); nm.x = 315
    ex(m, rd, role); ex(m, role, nm)
    mul = m.add(Op("multiply", "Multiply", {}, x=450))
    m.wire(nm, "example set output", mul, "input")
    km = m.add(Op("concurrency:k_means", "Clustering", {"add_cluster_attribute": True, "k": 3, "max_runs": 20,
                                                       "determine_good_start_values": True,
                                                       "use_local_random_seed": True, "local_random_seed": 1992}, x=585, y=34))
    m.wire(mul, "output 1", km, "example set")
    cdp = m.add(Op("cluster_distance_performance", "Cluster Distance Performance", {"main_criterion": "Davies Bouldin"}, x=720, y=34))
    m.wire(km, "clustered set", cdp, "example set"); m.wire(km, "cluster model", cdp, "cluster model")
    perf_csv(m, cdp, "performance", "p8_k3_perf", 1, x=855, y=34)
    agg = m.add(Op("aggregate", "Aggregate", {"use_default_aggregation": False, "group_by_attributes": "cluster|cultivar",
                                              "aggregation_attributes": ("list", [("alcohol", "count")])}, x=855, y=136))
    m.wire(cdp, "example set", agg, "example set input")
    data_csv(m, agg, "example set output", "p8_crosstab", 2, x=990, y=136)
    text_out(m, cdp, "cluster model", "p8_centroids", 3, x=855, y=238)
    inner = Proc()
    k2 = inner.add(Op("concurrency:k_means", "Clustering (opt)", {"add_cluster_attribute": True, "k": 2, "max_runs": 20,
                                                                 "determine_good_start_values": True,
                                                                 "use_local_random_seed": True, "local_random_seed": 1992}))
    c2 = inner.add(Op("cluster_distance_performance", "Cluster Distance Performance (opt)", {"main_criterion": "Avg. within centroid distance"}, x=180))
    log = inner.add(Op("log", "Log", {"log": ("list", [("k", "operator.Clustering (opt).parameter.k"),
                                                      ("avg_within", "operator.Cluster Distance Performance (opt).value.avg_within_distance")]),
                                      "sorting_type": "none", "persistent": False}, x=315))
    inner.wire(None, "input 1", k2, "example set")
    inner.wire(k2, "clustered set", c2, "example set"); inner.wire(k2, "cluster model", c2, "cluster model")
    inner.wire(c2, "performance", log, "through 1"); inner.wire(log, "through 1", None, "performance")
    opt = m.add(Op("concurrency:optimize_parameters_grid", "Optimize Parameters (k)", {
        "parameters": ("list", [("Clustering (opt).k", "[2.0;8.0;6;linear]")])}, subprocesses=[inner], x=585, y=340))
    m.wire(mul, "output 2", opt, "input 1")
    l2d = m.add(Op("log_to_data", "Log to Data", {"log_name": "Log"}, x=720, y=340))
    data_csv(m, l2d, "exampleSet", "p8_elbow", 4, x=855, y=340)
    return save(m, RM / "P08_solution.rmp")


# ════════════════════════════════════ P9 · Association ═════════════════════════════════════════
@builder
def p9():
    m = Proc()
    rd = m.add(read_csv("Read CSV", DATA / "p9_groceries_onehot.csv"))
    role = m.add(Op("set_role", "Set Role", {"attribute_name": "basket_id", "target_role": "id"}, x=180))
    n2b = m.add(Op("numerical_to_binominal", "Numerical to Binominal", {"attribute_filter_type": "all", "min": 0.0, "max": 0.0}, x=315))
    fp = m.add(Op("concurrency:fp_growth", "FP-Growth", {"input_format": "items in dummy coded columns", "positive_value": "true",
                                                         "min_requirement": "support", "min_support": 0.02,
                                                         "find_min_number_of_itemsets": False}, x=450))
    car = m.add(Op("create_association_rules", "Create Association Rules", {"criterion": "confidence", "min_confidence": 0.3}, x=585))
    ex(m, rd, role); ex(m, role, n2b)
    m.wire(n2b, "example set output", fp, "example set")
    m.wire(fp, "frequent sets", car, "item sets")
    text_out(m, car, "rules", "p9_rules", 1, x=720)
    text_out(m, car, "item sets", "p9_itemsets", 2, x=720, y=187)
    return save(m, RM / "P09_solution.rmp")


if __name__ == "__main__":
    only = sys.argv[1:] or list(BUILDERS)
    paths = [BUILDERS[k]() for k in only]
    print("built:", ", ".join(p.name for p in paths))
    subprocess.run(["bash", str(RUNNER), *map(str, paths)])
