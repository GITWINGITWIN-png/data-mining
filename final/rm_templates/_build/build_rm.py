"""สร้าง RapidMiner template R01–R11 (คู่กับ Python T01–T11) → final/rm_templates/*.rmp

แต่ละไฟล์ = process เดียว แบ่งเป็นแถว (§) ตามหัวข้อ · มีโน้ตสีบน canvas บอกว่าแก้ operator / parameter ไหน
ทุกแถวต่อผลออก port res → กด ▶ Run แล้วดูแท็บ Results ได้เลย (ไม่เขียนไฟล์ทิ้ง)

ทุก operator + ชื่อ parameter + ชื่อ port มาจาก (1) process เฉลยที่เคยรันผ่านจริง (mock_lab/recipes, practice/rm)
หรือ (2) ตรวจกับ source code ของ RapidMiner Studio (OperatorsCore.xml + class ของ operator) — ดู check_rm.py

รัน:  python final/rm_templates/_build/build_rm.py            (path ข้อมูล default = เครื่องผู้ใช้)
      RM_ROOT="/path/to/data mining" python …/build_rm.py      (เปลี่ยนโฟลเดอร์หลักของ repo)
ทดสอบในเครื่องที่มี RapidMiner:  bash final/mock_lab/run_rm.sh final/rm_templates/*.rmp
"""
import os
import sys
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
OUTDIR = HERE.parent
sys.path.insert(0, str(HERE.parents[1] / "mock_lab"))
from rm_builder import Op, Proc, save  # noqa: E402

ROOT = os.environ.get("RM_ROOT", "/home/panguin/Projects/data mining")
SEED = 1992


def P(*parts):
    return str(PurePosixPath(ROOT, *parts))


DATA = lambda f: P("final", "practice", "data", f)     # noqa: E731
NEW = lambda f: P("final", "rm_templates", "data", f)  # noqa: E731

# ════════════════════════════ ตัวช่วย ════════════════════════════


class T:
    """process หนึ่งไฟล์ + ตัวนับ port res"""

    def __init__(self):
        self.m = Proc()
        self.n = 0

    def add(self, op):
        return self.m.add(op)

    def wire(self, *a):
        self.m.wire(*a)

    def res(self, op, port):
        self.n += 1
        self.m.wire(op, port, None, f"result {self.n}")
        return self.n

    def note(self, *a, **k):
        self.m.note(*a, **k)


def OUT(op):
    """port ออกหลักของ operator (ExampleSet)"""
    if op.cls in ("read_csv", "read_excel"):
        return "output"
    if op.cls in ("append",):
        return "merged set"
    if op.cls in ("concurrency:join",):
        return "join"
    if op.cls in ("blending:pivot",):
        return "output"
    if op.cls in ("principal_component_analysis",):
        return "example set output"
    return "example set output"


def IN(op):
    if op.cls in ("blending:pivot", "multiply"):
        return "input"
    if op.cls in ("correlation_matrix", "weight_by_information_gain", "weight_by_information_gain_ratio",
                  "weight_by_gini_index", "weight_by_correlation", "agglomerative_clustering",
                  "concurrency:k_means", "concurrency:fp_growth", "split_data"):
        return "example set"
    return "example set input"


def chain(t, ops):
    for a, b in zip(ops, ops[1:]):
        t.wire(a, OUT(a), b, IN(b))
    return ops[-1]


def read_csv(name, path, x=45, y=85, sep=","):
    return Op("read_csv", name, {"csv_file": path, "column_separators": sep, "first_row_as_names": True,
                                 "parse_numbers": True, "decimal_character": ".", "encoding": "UTF-8"}, x=x, y=y)


def set_role(name, attr, role="label", x=180, y=85):
    return Op("set_role", name, {"attribute_name": attr, "target_role": role}, x=x, y=y)


def to_binominal(name, attr, x=180, y=85):
    """label ที่เป็นตัวเลข 0/1 → binominal (false/true) · RapidMiner ต้องการ label แบบ nominal สำหรับ classification"""
    return Op("numerical_to_binominal", name, {"attribute_filter_type": "single", "attribute": attr,
                                               "min": 0.0, "max": 0.0}, x=x, y=y)


def multiply(name, x, y=85):
    return Op("multiply", name, {}, x=x, y=y)


def norm(name="Normalize", method="Z-transformation", x=45, y=85):
    return Op("normalize", name, {"method": method}, x=x, y=y)


def binom_perf(name, positive=None, main="f_measure", x=180, y=85):
    p = {"main_criterion": main, "accuracy": True, "precision": True, "recall": True, "f_measure": True}
    if positive:
        p.update({"manually_set_positive_class": True, "positive_class": positive})
    return Op("performance_binominal_classification", name, p, x=x, y=y)


def multi_perf(name, x=180, y=85):
    return Op("performance_classification", name, {"main_criterion": "accuracy", "accuracy": True,
                                                   "kappa": True}, x=x, y=y)


def reg_perf(name, x=180, y=85):
    return Op("performance_regression", name, {
        "main_criterion": "root_mean_squared_error", "root_mean_squared_error": True,
        "absolute_error": True, "squared_error": True, "squared_correlation": True}, x=x, y=y)


def cross_validation(name, training, testing, folds=10, sampling="stratified sampling", x=45, y=85):
    return Op("concurrency:cross_validation", name, {
        "split_on_batch_attribute": False, "leave_one_out": False, "number_of_folds": folds,
        "sampling_type": sampling, "use_local_random_seed": True, "local_random_seed": SEED,
        "enable_parallel_execution": True}, subprocesses=[training, testing], x=x, y=y)


def testing(tag, perf):
    te = Proc()
    ap = te.add(Op("apply_model", f"Apply Model ({tag})", {}))
    perf.x = 180
    te.add(perf)
    te.wire(None, "model", ap, "model")
    te.wire(None, "test set", ap, "unlabelled data")
    te.wire(ap, "labelled data", perf, "labelled data")
    te.wire(perf, "performance", None, "performance 1")
    return te


PREP_MODEL = ("normalize", "replace_missing_values", "nominal_to_numerical", "principal_component_analysis")


def training(tag, learner, steps=()):
    """steps = preprocessing ใน Training pane (fit เฉพาะ training fold = ไม่ leak) → Group Models"""
    tr = Proc()
    prev, port = None, "training set"
    for i, op in enumerate(steps):
        op.name, op.x, op.y = f"{op.name} ({tag})", 45 + 135 * i, 85
        tr.add(op)
        tr.wire(prev, port, op, "exa" if op.cls == "operator_toolbox:smote" else "example set input")
        prev, port = op, ("ups" if op.cls == "operator_toolbox:smote" else "example set output")
    learner.name, learner.x, learner.y = f"{learner.name} ({tag})", 45 + 135 * len(steps), 85
    tr.add(learner)
    tr.wire(prev, port, learner, "training set")
    models = [op for op in steps if op.cls in PREP_MODEL]
    if models:
        grp = tr.add(Op("group_models", f"Group Models ({tag})", {}, x=learner.x + 135))
        for i, op in enumerate(models, start=1):
            tr.wire(op, "preprocessing model", grp, f"models in {i}")
        tr.wire(learner, "model", grp, f"models in {len(models) + 1}")
        tr.wire(grp, "model out", None, "model")
    else:
        tr.wire(learner, "model", None, "model")
    return tr


def cv(tag, learner, perf, steps=(), folds=10, sampling="stratified sampling", x=450, y=85):
    return cross_validation(f"CV {tag}", training(tag, learner, steps), testing(tag, perf),
                            folds=folds, sampling=sampling, x=x, y=y)


def optimize(t, src, src_port, inner_cv, grid, log_cols, tag, x, y):
    """Optimize Parameters (Grid) ครอบ CV + Log → Log to Data (ตารางผลทุกค่า) + parameter set ที่ดีที่สุด"""
    inner = Proc()
    inner.add(inner_cv)
    log = inner.add(Op("log", f"Log ({tag})", {"log": ("list", log_cols), "sorting_type": "none",
                                               "persistent": False}, x=180))
    inner.wire(None, "input 1", inner_cv, "example set")
    inner.wire(inner_cv, "performance 1", log, "through 1")
    inner.wire(log, "through 1", None, "performance")
    opt = t.add(Op("concurrency:optimize_parameters_grid", f"Optimize Parameters ({tag})", {
        "parameters": ("list", grid), "error_handling": "fail on error"}, subprocesses=[inner], x=x, y=y))
    t.wire(src, src_port, opt, "input 1")
    l2d = t.add(Op("log_to_data", f"Log to Data ({tag})", {"log_name": f"Log ({tag})"}, x=x + 135, y=y))
    t.res(l2d, "exampleSet")
    t.res(opt, "parameter set")
    return opt


def cv_value(cv_name):
    return f"operator.{cv_name}.value.performance main criterion"


def dt(name="Decision Tree", depth=10, criterion="gini_index"):
    return Op("concurrency:parallel_decision_tree", name, {"criterion": criterion, "maximal_depth": depth,
                                                           "apply_pruning": False, "apply_prepruning": False})


def rf(name="Random Forest", trees=100, depth=10):
    return Op("concurrency:parallel_random_forest", name, {
        "number_of_trees": trees, "criterion": "gini_index", "maximal_depth": depth, "guess_subset_ratio": True,
        "voting_strategy": "confidence vote", "use_local_random_seed": True, "local_random_seed": SEED})


def knn(name="k-NN", k=5):
    return Op("k_nn", name, {"k": k})


def logreg(name="Logistic Regression"):
    return Op("h2o:logistic_regression", name, {
        "solver": "AUTO", "reproducible": True, "use_regularization": False, "standardize": True,
        "compute_p-values": True, "remove_collinear_columns": True, "add_intercept": True})


def baseline(name="Default Model", method="mode"):
    return Op("default_model", name, {"method": method})


def lane_note(t, sec, text, y, x=45, w=900, h=56, color="yellow"):
    t.note(f"<b>{sec}</b><br>{text}", x, y, w, h, color)


def config_note(t, items, extra="", w=900, h=None):
    body = "<br>".join(f"{i}. {s}" for i, s in enumerate(items, 1))
    h = h or 40 + 17 * (len(items) + (1 if extra else 0))
    t.note(f"<b>⚙️ แก้ก่อน (CONFIG)</b><br>{body}" + (f"<br>{extra}" if extra else ""), 45, 10, w, h, "green")
    return 10 + h + 20


def write(t, name):
    path = save(t.m, OUTDIR / name, random_seed=SEED)
    print("wrote", path.name, f"({len(t.m.ops)} operators, {t.n} results)")


LANE = 230     # ระยะห่างแนวตั้งระหว่างแถว (CV สูง ~165px + โน้ต 56px)
ROW2 = 210     # แถวที่ 2 ภายใน lane (ใต้ operator 3 port)
LANE2 = 350    # lane ที่มี 2 แถว


# ════════════════════════════ R01 · Data Handling ════════════════════════════
def r01():
    t = T()
    y0 = config_note(t, [
        "Read CSV (หลัก) → csv_file = ไฟล์โจทย์ (หรือใช้ Import Configuration Wizard)",
        "Read CSV (append) / Read CSV (lookup) → ไฟล์ที่ 2 / ตาราง lookup · ไม่ใช้ → ลบ operator + ลบ Append/Join แล้วต่อเส้นตรง",
        "Join → key_attributes (คู่คอลัมน์ key) + join_type (inner / left / right / outer)",
        "Set Role → attribute_name = คอลัมน์ id / label",
    ], extra="ดูสถิติ: Results → แท็บ Statistics · กราฟ: Results → Visualizations (Histogram / Boxplot / Bar / Scatter)")
    y = y0 + 60
    rd = t.add(read_csv("Read CSV (หลัก)", DATA("p1_bills_week1.csv"), y=y))
    rd2 = t.add(read_csv("Read CSV (append)", DATA("p1_bills_week2.csv"), y=y + 100))
    rl = t.add(read_csv("Read CSV (lookup)", DATA("p1_day_info.csv"), y=y + 200))
    app = t.add(Op("append", "Append", {"merge_type": "all"}, x=180, y=y + 50))
    t.wire(rd, "output", app, "example set 1")
    t.wire(rd2, "output", app, "example set 2")
    join = t.add(Op("concurrency:join", "Join", {
        "join_type": "left", "use_id_attribute_as_key": False,
        "key_attributes": ("list", [("day", "day")]), "remove_double_attributes": True}, x=315, y=y + 100))
    t.wire(app, "merged set", join, "left")
    t.wire(rl, "output", join, "right")
    mul = t.add(multiply("Multiply", 450, y + 100))
    t.wire(join, "join", mul, "input")
    lane_note(t, "§1 Import · §4 Append (ต่อแถว) · §5 Join (เพิ่มคอลัมน์ด้วย key) → res 1 = ข้อมูลหลังรวม",
              "คลิก res 1 → Statistics (missing / min / max / mean / ค่าที่พบบ่อย) · Visualizations วาดกราฟ", y0)
    t.res(mul, "output 1")

    x0, yy = 1000, y0
    lanes = []

    def lane(sec, text, ops, port_from=None):
        nonlocal yy
        lane_note(t, sec, text, yy, x=x0, w=760)
        for i, op in enumerate(ops):
            op.x, op.y = x0 + 135 * i, yy + 62
            t.add(op)
        t.wire(mul, f"output {len(lanes) + 2}", ops[0], IN(ops[0]))
        chain(t, ops)
        lanes.append(ops)
        yy += LANE
        return ops[-1]

    last = lane("§2 Select Attributes + Set Role", "Select Attributes → attributes (คั่นด้วย |) · invert_selection = true คือ 'ตัด' · Set Role → id / label",
                [Op("select_attributes", "Select Attributes", {"attribute_filter_type": "subset", "attributes": "size",
                                                               "invert_selection": True}),
                 set_role("Set Role (id)", "bill_id", "id"), set_role("Set Role (label)", "tip", "label")])
    t.res(last, "example set output")
    last = lane("§3 Filter Examples (กรองแถว)", "condition_class = custom_filters → Add Entry: คอลัมน์ · เงื่อนไข (equals / > / ≥ / is missing) · ค่า · filters_logic_and = AND/OR",
                [Op("filter_examples", "Filter Examples", {
                    "condition_class": "custom_filters", "filters_logic_and": True,
                    "filters_list": ("list", [("filters_entry_key", "time.equals.Dinner"),
                                              ("filters_entry_key", "size.ge.4")])})])
    t.res(last, "example set output")
    last = lane("§6 Aggregate (group by)", "group_by_attributes = คอลัมน์กลุ่ม · aggregation_attributes → Edit List: คอลัมน์ + ฟังก์ชัน (sum / average / count / maximum …)",
                [Op("aggregate", "Aggregate", {"use_default_aggregation": False, "group_by_attributes": "day",
                                               "aggregation_attributes": ("list", [("total_bill", "sum"), ("total_bill", "average"),
                                                                                   ("tip", "average"), ("bill_id", "count")])})])
    t.res(last, "example set output")
    last = lane("§7 Pivot", "group_by_attributes = แถว · column_grouping_attribute = คอลัมน์ · aggregation_attributes = ค่า + ฟังก์ชัน · สัดส่วนคลาส: Generate Attributes สร้าง 0/1 ก่อนแล้ว average",
                [Op("generate_attributes", "Generate Attributes (rate)", {
                    "function_descriptions": ("list", [("is_smoker", 'if(smoker=="Yes", 1, 0)')])}),
                 Op("blending:pivot", "Pivot", {"group_by_attributes": "day", "column_grouping_attribute": "time",
                                                "aggregation_attributes": ("list", [("tip", "average"), ("is_smoker", "average")])})])
    t.res(last, "output")
    last = lane("§8 Generate Attributes (สร้างคอลัมน์ใหม่)", "function_descriptions → Edit List: ชื่อใหม่ = สูตร เช่น tip / total_bill * 100 · if(x > 20, \"high\", \"low\")",
                [Op("generate_attributes", "Generate Attributes", {
                    "function_descriptions": ("list", [("tip_pct", "tip / total_bill * 100"),
                                                       ("big_bill", 'if(total_bill > 20, "Yes", "No")')])})])
    t.res(last, "example set output")
    last = lane("§9 Sort + Sample (ดูตัวอย่าง)", "Sort → attribute_name + sorting_direction · Sample → sample = absolute / relative",
                [Op("sort", "Sort", {"attribute_name": "total_bill", "sorting_direction": "decreasing"}),
                 Op("sample", "Sample (10 rows)", {"sample": "absolute", "sample_size": 10,
                                                   "use_local_random_seed": True, "local_random_seed": SEED})])
    t.res(last, "example set output")
    cm = Op("correlation_matrix", "Correlation Matrix", {})
    lane("§10 Correlation Matrix", "ใช้ได้กับคอลัมน์ตัวเลข · ผล = ตาราง r ทุกคู่ (Results → Correlation Matrix / Pairwise Table)", [cm])
    t.res(cm, "matrix")
    write(t, "R01_data_handling.rmp")


# ════════════════════════════ R02 · Preprocessing ════════════════════════════
def r02():
    t = T()
    y0 = config_note(t, [
        "Read CSV → csv_file · Declare Missing Value → ค่าที่แปลว่าว่าง เช่น ? (ไม่มี → ลบ operator)",
        "Set Role → attribute_name = label",
        "แต่ละแถว: แก้ attribute / attributes ให้ตรงคอลัมน์ของโจทย์ (ดูโน้ตเหลืองของแถวนั้น)",
    ], extra="§1–§7 = ทำกับทั้งตาราง (สาธิต) · §8 = วิธีถูกต้องตอนสร้างโมเดล (fit บน train / ใน CV เท่านั้น)")
    y = y0 + 60
    rd = t.add(read_csv("Read CSV", DATA("p2_penguins.csv"), y=y))
    dmv = t.add(Op("declare_missing_value", "Declare Missing Value", {
        "attribute_filter_type": "all", "mode": "nominal", "nominal_value": "?"}, x=180, y=y))
    role = t.add(set_role("Set Role", "species", x=315, y=y))
    mul = t.add(multiply("Multiply", 450, y))
    chain(t, [rd, dmv, role, mul])
    lane_note(t, "§0 ข้อมูลดิบ → res 1", "res 1 → Statistics: ดูจำนวน Missing ของแต่ละคอลัมน์ · ชนิด (nominal/numeric) · range", y0)
    t.res(mul, "output 1")
    x0, yy, k = 1000, y0, [2]

    def lane(sec, text, ops):
        nonlocal yy
        lane_note(t, sec, text, yy, x=x0, w=780)
        for i, op in enumerate(ops):
            op.x, op.y = x0 + 135 * i, yy + 62
            t.add(op)
        t.wire(mul, f"output {k[0]}", ops[0], IN(ops[0]))
        k[0] += 1
        chain(t, ops)
        yy += LANE
        return ops[-1]

    t.res(lane("§2 Missing: Replace Missing Values", "default = average / minimum / maximum / zero / value (replenishment_value) · ตัดแถวแทน: Filter Examples (attr.is_not_missing.)",
               [Op("replace_missing_values", "Replace Missing Values", {"default": "average"})]), "example set output")
    t.res(lane("§2b Missing: ตัดแถวที่ว่าง", "Filter Examples → filters_list: body_mass_g.is_not_missing. (แก้ชื่อคอลัมน์)",
               [Op("filter_examples", "Filter Examples (not missing)", {
                   "condition_class": "custom_filters",
                   "filters_list": ("list", [("filters_entry_key", "body_mass_g.is_not_missing.")])})]), "example set output")
    t.res(lane("§3 Outlier: Detect Outlier (Distances) → ตัดแถว outlier", "number_of_neighbors (k) · number_of_outliers (n แถวที่ไกลสุด) · ผลมีคอลัมน์ outlier = true/false → Filter Examples outlier.equals.false",
               [Op("select_attributes", "Select Attributes (numeric)", {"attribute_filter_type": "value_type", "value_type": "numeric",
                                                                        "include_special_attributes": False}),
                Op("replace_missing_values", "Replace Missing (outlier)", {"default": "average"}),
                Op("detect_outlier_distances", "Detect Outlier (Distances)", {
                    "number_of_neighbors": 10, "number_of_outliers": 10, "distance_function": "euclidian distance"}),
                Op("filter_examples", "Filter Examples (no outlier)", {
                    "condition_class": "custom_filters",
                    "filters_list": ("list", [("filters_entry_key", "outlier.equals.false")])})]), "example set output")
    t.res(lane("§4 Encoding: Nominal to Numerical (dummy = one-hot)", "coding_type = dummy coding (one-hot) / unique integers (label encoding) / effect coding · attribute_filter_type = all หรือ subset",
               [Op("nominal_to_numerical", "Nominal to Numerical", {"coding_type": "dummy coding"})]), "example set output")
    t.res(lane("§5a Standardization: Normalize (Z-transformation)", "method = Z-transformation → mean 0, std 1 (RapidMiner ใช้ n−1)",
               [norm("Normalize (Z)")]), "example set output")
    t.res(lane("§5b Normalization: Normalize (range transformation 0–1)", "method = range transformation · min = 0 · max = 1",
               [Op("normalize", "Normalize (0-1)", {"method": "range transformation", "min": 0.0, "max": 1.0})]), "example set output")
    t.res(lane("§6a Discretize by Binning (equal width)", "attribute = คอลัมน์ · number_of_bins · range_name_type = short (ชื่อ range1, range2 …)",
               [Op("discretize_by_bins", "Discretize by Binning", {"attribute_filter_type": "single", "attribute": "body_mass_g",
                                                                   "number_of_bins": 3, "range_name_type": "short"})]), "example set output")
    t.res(lane("§6b Discretize by Frequency (equal frequency)", "จำนวนต่อช่วงเท่ากัน · ทนข้อมูลเบ้",
               [Op("discretize_by_frequency", "Discretize by Frequency", {"attribute_filter_type": "single", "attribute": "body_mass_g",
                                                                          "number_of_bins": 3, "range_name_type": "short"})]), "example set output")
    t.res(lane("§6c Discretize by User Specification (ขอบกำหนดเอง)", "classes → Edit List: ชื่อช่วง + upper limit (ค่าบนสุดของช่วง · ช่วงสุดท้ายใส่ Infinity)",
               [Op("discretize_by_user_specification", "Discretize by User Specification", {
                   "attribute_filter_type": "single", "attribute": "body_mass_g",
                   "classes": ("list", [("Low", 3500), ("Mid", 4500), ("High", "Infinity")])})]), "example set output")
    t.res(lane("§7a Sample (สุ่ม 30%)", "sample = relative · sample_ratio = 0.3 · (absolute → sample_size)",
               [Op("sample", "Sample (relative)", {"sample": "relative", "sample_ratio": 0.3,
                                                   "use_local_random_seed": True, "local_random_seed": SEED})]), "example set output")
    t.res(lane("§7b Sample (Stratified) — รักษาสัดส่วนคลาส", "ต้องมี label · sample = relative · sample_ratio",
               [Op("sample_stratified", "Sample (Stratified)", {"sample": "relative", "sample_ratio": 0.3,
                                                                "use_local_random_seed": True, "local_random_seed": SEED})]), "example set output")

    # §8 split แบบไม่ leak: preprocessing fit บน train → ใช้ preprocessing model กับ test
    lane_note(t, "§8 ⭐ Split Data ไม่ให้ leak: Replace Missing + Normalize fit บน train → Apply Model (preprocessing model) กับ test",
              "res = train ที่ preprocess แล้ว + test ที่ใช้ค่า mean/std จาก train · Split Data → partitions (0.7 / 0.3) · sampling_type = stratified", yy, x=x0, w=780)
    sp = t.add(Op("split_data", "Split Data", {"partitions": ("enum", [0.7, 0.3], "ratio"), "sampling_type": "stratified sampling",
                                               "use_local_random_seed": True, "local_random_seed": SEED}, x=x0, y=yy + 62))
    t.wire(mul, f"output {k[0]}", sp, "example set"); k[0] += 1
    rmv = t.add(Op("replace_missing_values", "Replace Missing (train)", {"default": "average", "return_preprocessing_model": True},
                   x=x0 + 135, y=yy + 62))
    nm = t.add(norm("Normalize (train)", x=x0 + 270, y=yy + 62))
    t.wire(sp, "partition 1", rmv, "example set input"); chain(t, [rmv, nm])
    a1 = t.add(Op("apply_model", "Apply Model (missing → test)", {}, x=x0 + 135, y=yy + ROW2))
    a2 = t.add(Op("apply_model", "Apply Model (normalize → test)", {}, x=x0 + 270, y=yy + ROW2))
    t.wire(rmv, "preprocessing model", a1, "model"); t.wire(sp, "partition 2", a1, "unlabelled data")
    t.wire(nm, "preprocessing model", a2, "model"); t.wire(a1, "labelled data", a2, "unlabelled data")
    t.res(nm, "example set output"); t.res(a2, "labelled data")
    yy += LANE2

    # §8b เทียบก่อน/หลัง normalize ด้วย k-NN ใน CV (preprocessing อยู่ใน Training pane)
    lane_note(t, "§8b ⭐ เทียบก่อน/หลัง preprocessing: k-NN ไม่ normalize vs normalize (ทุกอย่างอยู่ใน Training pane ของ CV)",
              "ดับเบิลคลิก CV เพื่อดูข้างใน · เปรียบเทียบ accuracy ใน res · เปลี่ยน learner ได้ (ลาก operator ใหม่แทน k-NN)", yy, x=x0, w=780)
    mm = t.add(multiply("Multiply (compare)", x0, yy + 62))
    t.wire(mul, f"output {k[0]}", mm, "input"); k[0] += 1
    for i, (tag, steps) in enumerate([("raw", []), ("normalized", [norm()])]):
        st = [Op("replace_missing_values", "Replace Missing Values", {"default": "average", "return_preprocessing_model": True}),
              Op("nominal_to_numerical", "Nominal to Numerical", {"coding_type": "dummy coding", "return_preprocessing_model": True})] + steps
        c = t.add(cv(f"kNN {tag}", knn(), multi_perf(f"Performance (kNN {tag})"), steps=st, folds=5, x=x0 + 135 + 135 * i, y=yy + 62))
        t.wire(mm, f"output {i + 1}", c, "example set")
        t.res(c, "performance 1")
    yy += LANE

    # §9 feature selection
    lane_note(t, "§9 Feature selection: Weight by Information Gain → Select by Weights (top k)",
              "weight_relation = top k · k = จำนวน feature · เปลี่ยนเป็น Weight by Correlation / Gini Index ได้ · ⚠️ ใช้ใน CV ถ้าจะวัดผลโมเดล", yy, x=x0, w=780)
    w = t.add(Op("weight_by_information_gain", "Weight by Information Gain", {"normalize_weights": False, "sort_weights": True,
                                                                              "sort_direction": "descending"}, x=x0, y=yy + 62))
    sw = t.add(Op("select_by_weights", "Select by Weights", {"weight_relation": "top k", "k": 3}, x=x0 + 135, y=yy + 62))
    t.wire(mul, f"output {k[0]}", w, "example set"); k[0] += 1
    t.wire(w, "example set", sw, "example set input"); t.wire(w, "weights", sw, "weights")
    t.res(sw, "weights"); t.res(sw, "example set output")
    write(t, "R02_preprocessing.rmp")


# ════════════════════════════ R03 · PCA ════════════════════════════
def r03():
    t = T()
    y0 = config_note(t, [
        "Read CSV → csv_file · Set Role → label (ไว้ระบายสีกราฟ · ไม่มี label → ลบ Set Role)",
        "Select Attributes → ตัด id / คอลัมน์ที่ไม่ใช่ตัวเลข (PCA ใช้ตัวเลขเท่านั้น)",
        "PCA → dimensionality_reduction = keep variance (variance_threshold 0.8/0.9/0.95) หรือ fixed number (number_of_components)",
    ], extra="ผล PCA model (res) → แท็บ Eigenvalues (variance / cumulative) · Eigenvectors (loadings) · กราฟ 2D: res scores → Visualizations → Scatter pc_1 × pc_2 สีตาม label")
    y = y0 + 60
    rd = t.add(read_csv("Read CSV", DATA("p4_wine.csv"), y=y))
    role = t.add(set_role("Set Role", "cultivar", x=180, y=y))
    sel = t.add(Op("select_attributes", "Select Attributes", {"attribute_filter_type": "value_type", "value_type": "numeric",
                                                              "include_special_attributes": False}, x=315, y=y))
    mul = t.add(multiply("Multiply", 450, y))
    chain(t, [rd, role, sel, mul])
    lane_note(t, "§2–§3 Normalize → PCA (keep variance 0.95) → res: scores + model (eigenvalues / loadings)",
              "จำนวน PC ที่ต้องใช้ = ดู Cumulative Variance ใน Eigenvalues · loadings = Eigenvectors", y0, x=600, w=760)
    n1 = t.add(norm("Normalize (pca)", x=600, y=y0 + 62))
    p1 = t.add(Op("principal_component_analysis", "PCA (keep variance)", {"dimensionality_reduction": "keep variance",
                                                                         "variance_threshold": 0.95}, x=735, y=y0 + 62))
    t.wire(mul, "output 1", n1, "example set input"); chain(t, [n1, p1])
    t.res(p1, "example set output"); t.res(p1, "preprocessing model")
    y2 = y0 + LANE
    lane_note(t, "§4 PCA 2 components → scatter 2D", "number_of_components = 2 · res → Visualizations → Scatter: x = pc_1, y = pc_2, color = label", y2, x=600, w=760)
    n2 = t.add(norm("Normalize (2D)", x=600, y=y2 + 62))
    p2 = t.add(Op("principal_component_analysis", "PCA (2 components)", {"dimensionality_reduction": "fixed number",
                                                                        "number_of_components": 2}, x=735, y=y2 + 62))
    t.wire(mul, "output 2", n2, "example set input"); chain(t, [n2, p2])
    t.res(p2, "example set output")
    y3 = y2 + LANE
    lane_note(t, "§5 ⭐ เทียบโมเดลก่อน/หลัง PCA (Normalize + PCA อยู่ใน Training pane ของ CV = ไม่ leak)",
              "เปลี่ยนจำนวน PC: ดับเบิลคลิก CV kNN + PCA → PCA → number_of_components", y3, x=600, w=760)
    mm = t.add(multiply("Multiply (compare)", 600, y3 + 62))
    t.wire(mul, "output 3", mm, "input")
    for i, (tag, steps) in enumerate([("kNN", [norm()]),
                                      ("kNN + PCA", [norm(), Op("principal_component_analysis", "PCA", {
                                          "dimensionality_reduction": "fixed number", "number_of_components": 2})])]):
        c = t.add(cv(tag, knn(), multi_perf(f"Performance ({tag})"), steps=steps, folds=5, x=735 + 135 * i, y=y3 + 62))
        t.wire(mm, f"output {i + 1}", c, "example set")
        t.res(c, "performance 1")
    write(t, "R03_pca.rmp")


# ════════════════════════════ R04 · Imbalanced ════════════════════════════
def r04():
    t = T()
    y0 = config_note(t, [
        "Read CSV → csv_file · Set Role → label",
        "ทุก Performance (ในแต่ละ CV) → positive_class = คลาสส่วนน้อย/ที่สนใจ (ตอนนี้ = malignant)",
        "Sample (undersample) → sample_size_per_class: ใส่ชื่อคลาส + จำนวน (= จำนวนของคลาสส่วนน้อยใน training fold)",
        "SMOTE ต้องติดตั้ง Operator Toolbox (Extensions → Marketplace) · ไม่มี → ลบแถว SMOTE ทั้ง 2 แถว",
    ], extra="ดู res: recall / precision / F1 ของคลาสส่วนน้อย ไม่ใช่ accuracy อย่างเดียว · resample อยู่ใน Training pane = ไม่แตะ test fold")
    y = y0 + 60
    rd = t.add(read_csv("Read CSV", DATA("p3_breast_cancer_imbalanced.csv"), y=y))
    role = t.add(set_role("Set Role", "diagnosis", x=180, y=y))
    mul = t.add(multiply("Multiply", 315, y))
    chain(t, [rd, role, mul])
    lane_note(t, "§1 ดูความไม่สมดุล → res 1 (Statistics ของ label)", "", y0, x=45, w=300, h=40)
    t.res(mul, "output 1")
    pos = "malignant"
    variants = [
        ("§2 Baseline (Default Model = mode) → accuracy สูงแต่ recall = 0", "Baseline", baseline(), []),
        ("§4a ไม่ resample (Decision Tree)", "Tree", dt(depth=4), []),
        ("§4b Undersampling: Sample (balance_data) ใน Training pane", "Undersample", dt(depth=4),
         [Op("sample", "Sample (undersample)", {"sample": "absolute", "balance_data": True,
                                                 "sample_size_per_class": ("list", [("benign", 32), ("malignant", 32)]),
                                                 "use_local_random_seed": True, "local_random_seed": SEED})]),
        ("§4c SMOTE ใน Training pane (Operator Toolbox)", "SMOTE", dt(depth=4),
         [Op("operator_toolbox:smote", "SMOTE Upsampling", {
             "number_of_neighbours": 5, "normalize": True, "equalize_classes": True, "auto_detect_minority_class": True,
             "use_local_random_seed": True, "local_random_seed": SEED})]),
    ]
    yy = y0
    for i, (sec, tag, learner, steps) in enumerate(variants):
        lane_note(t, sec, "ดับเบิลคลิก CV → Training pane เห็น resampling + learner · Testing pane = Apply Model + Performance", yy, x=600, w=760)
        c = t.add(cv(tag, learner, binom_perf(f"Performance ({tag})", positive=pos), steps=steps, folds=5, x=600, y=yy + 62))
        t.wire(mul, f"output {i + 2}", c, "example set")
        t.res(c, "performance 1")
        yy += LANE
    lane_note(t, "§6 ❌ วิธีผิด: SMOTE ทั้งตารางก่อน CV (leak) → ผลดีเกินจริง (ไว้ตอบคำถาม 'ทำไมห้าม')",
              "เทียบ res กับ §4c · synthetic ที่สร้างจากจุดใน test fold รั่วเข้า training", yy, x=600, w=760, color="red")
    sm = t.add(Op("operator_toolbox:smote", "SMOTE (WRONG, before CV)", {
        "number_of_neighbours": 5, "normalize": True, "equalize_classes": True, "auto_detect_minority_class": True,
        "use_local_random_seed": True, "local_random_seed": SEED}, x=600, y=yy + 62))
    t.wire(mul, f"output {len(variants) + 2}", sm, "exa")
    c = t.add(cv("WRONG", dt(depth=4), binom_perf("Performance (WRONG)", positive=pos), folds=5, x=735, y=yy + 62))
    t.wire(sm, "ups", c, "example set")
    t.res(c, "performance 1")
    write(t, "R04_imbalanced_smote.rmp")


# ════════════════════════════ R05 · KNN ════════════════════════════
def r05():
    t = T()
    y0 = config_note(t, [
        "Read CSV → csv_file · Set Role → label · (label เป็น 0/1 → เพิ่ม Numerical to Binominal ก่อน Set Role)",
        "Read CSV (new point) → ไฟล์ข้อมูลใหม่ (คอลัมน์เดียวกัน ไม่ต้องมี label) — สร้างใน Excel/Notepad 1 แถว",
        "k-NN → k · measure_types = NumericalMeasures · numerical_measure = EuclideanDistance / ManhattanDistance",
        "Performance → positive_class = คลาสที่สนใจ (ตอนนี้ = Owner)",
    ])
    y = y0 + 60
    rd = t.add(read_csv("Read CSV", P("final", "data", "riding_mowers.csv"), y=y))
    role = t.add(set_role("Set Role", "Ownership", x=180, y=y))
    mul = t.add(multiply("Multiply", 315, y))
    chain(t, [rd, role, mul])
    rn = t.add(read_csv("Read CSV (new point)", NEW("new_mower.csv"), y=y + 120))
    mn = t.add(multiply("Multiply (new)", 180, y + 120))
    t.wire(rn, "output", mn, "input")
    yy = y0
    # §2 distances by hand
    lane_note(t, "§2 ระยะจากจุดใหม่ถึงทุกจุด (Cross Distances) → k จุดใกล้สุด",
              "only_top_k = true · k = 3 · ไม่ normalize ตามตำรา (ถ้าโจทย์ให้ normalize ต้อง Normalize ทั้งสองฝั่งด้วยค่าจากข้อมูล train)", yy, x=600, w=820)
    cd = t.add(Op("cross_distances", "Cross Distances", {"measure_types": "NumericalMeasures", "numerical_measure": "EuclideanDistance",
                                                         "only_top_k": True, "k": 3, "search_for": "nearest"}, x=600, y=yy + 62))
    t.wire(mn, "output 1", cd, "request set"); t.wire(mul, "output 1", cd, "reference set")
    t.res(cd, "result set")
    yy += LANE
    # §3 hold-out
    lane_note(t, "§3 Hold-out: Split Data 70/30 → Normalize (fit train) → k-NN → Apply กับ test → Performance",
              "partitions = 0.7 / 0.3 · ไม่ normalize → ลบ Normalize + Apply Model (normalize) แล้วต่อเส้นตรง", yy, x=600, w=820)
    sp = t.add(Op("split_data", "Split Data", {"partitions": ("enum", [0.7, 0.3], "ratio"), "sampling_type": "stratified sampling",
                                               "use_local_random_seed": True, "local_random_seed": SEED}, x=600, y=yy + 62))
    t.wire(mul, "output 2", sp, "example set")
    nm = t.add(norm("Normalize (hold-out)", x=735, y=yy + 62))
    kn = t.add(knn("k-NN (hold-out)", 3)); kn.x, kn.y = 870, yy + 62
    t.wire(sp, "partition 1", nm, "example set input"); t.wire(nm, "example set output", kn, "training set")
    a1 = t.add(Op("apply_model", "Apply Model (normalize test)", {}, x=870, y=yy + ROW2))
    a2 = t.add(Op("apply_model", "Apply Model (kNN test)", {}, x=1005, y=yy + ROW2))
    t.wire(nm, "preprocessing model", a1, "model"); t.wire(sp, "partition 2", a1, "unlabelled data")
    t.wire(kn, "model", a2, "model"); t.wire(a1, "labelled data", a2, "unlabelled data")
    pf = t.add(binom_perf("Performance (hold-out)", positive="Owner", x=1140, y=yy + ROW2))
    t.wire(a2, "labelled data", pf, "labelled data")
    t.res(pf, "performance"); t.res(pf, "example set")
    yy += LANE2
    # §4 CV compare
    lane_note(t, "§4 ⭐ CV: baseline vs k-NN ไม่ normalize vs k-NN + normalize (เทียบก่อน/หลัง preprocessing)",
              "number_of_folds ใน CV แต่ละตัว · k ใน k-NN ข้างใน CV", yy, x=600, w=820)
    mm = t.add(multiply("Multiply (compare)", 600, yy + 62))
    t.wire(mul, "output 3", mm, "input")
    for i, (tag, lr, steps) in enumerate([("Baseline", baseline(), []), ("kNN raw", knn(k=3), []), ("kNN normalized", knn(k=3), [norm()])]):
        c = t.add(cv(tag, lr, binom_perf(f"Performance ({tag})", positive="Owner"), steps=steps, folds=5, x=735 + 135 * i, y=yy + 62))
        t.wire(mm, f"output {i + 1}", c, "example set")
        t.res(c, "performance 1")
    yy += LANE
    # §5 optimize k
    lane_note(t, "§5 ⭐ Optimize Parameters (Grid): k = 1…15 + Log → ตาราง k vs F1 · parameter set = k ที่ดีที่สุด",
              "แก้ช่วง: Optimize Parameters → Edit Parameter Settings (k-NN (opt).k: min, max, steps) · กราฟ: Log to Data → Visualizations → Line", yy, x=600, w=820)
    inner = cv("opt", knn("k-NN"), binom_perf("Performance (opt)", positive="Owner"), steps=[norm()], folds=5)
    optimize(t, mul, "output 4", inner, [("k-NN (opt).k", "[1.0;15.0;14;linear]")],
             [("k", "operator.k-NN (opt).parameter.k"), ("f_measure", cv_value("CV opt"))], "k", 600, yy + 62)
    yy += LANE
    # §6 final model → new point
    lane_note(t, "§6 โมเดลสุดท้าย (ทั้งชุด) → ทำนายจุดใหม่ (prediction + confidence = สัดส่วน vote)",
              "k ของ k-NN (final) = ค่าที่ดีที่สุดจาก §5 หรือค่าที่โจทย์กำหนด", yy, x=600, w=820)
    nf = t.add(norm("Normalize (final)", x=600, y=yy + 62))
    kf = t.add(knn("k-NN (final)", 3)); kf.x, kf.y = 735, yy + 62
    t.wire(mul, "output 5", nf, "example set input"); t.wire(nf, "example set output", kf, "training set")
    b1 = t.add(Op("apply_model", "Apply Model (normalize new)", {}, x=735, y=yy + ROW2))
    b2 = t.add(Op("apply_model", "Apply Model (kNN new)", {}, x=870, y=yy + ROW2))
    t.wire(nf, "preprocessing model", b1, "model"); t.wire(mn, "output 2", b1, "unlabelled data")
    t.wire(kf, "model", b2, "model"); t.wire(b1, "labelled data", b2, "unlabelled data")
    t.res(b2, "labelled data")
    yy += LANE2
    # §7 KNN regression
    lane_note(t, "§7 KNN Regression (label ตัวเลข) → Performance (Regression): RMSE / MAE / R²",
              "Read CSV (regression) → ไฟล์ · Set Role (regression) → label ตัวเลข · k ใน k-NN", yy, x=45, w=900)
    rr = t.add(read_csv("Read CSV (regression)", P("final", "mock_lab", "mock2_regression_pca", "data", "housing.csv"), x=45, y=yy + 62))
    sr = t.add(set_role("Set Role (regression)", "medv", x=180, y=yy + 62))
    chain(t, [rr, sr])
    c = t.add(cv("kNN regression", knn(k=5), reg_perf("Performance (kNN regression)"), steps=[norm()], folds=10,
                 sampling="shuffled sampling", x=315, y=yy + 62))
    t.wire(sr, "example set output", c, "example set")
    t.res(c, "performance 1")
    write(t, "R05_knn.rmp")


# ════════════════════════════ R06 · Linear Regression ════════════════════════════
def r06():
    t = T()
    y0 = config_note(t, [
        "Read CSV → csv_file · Set Role → label (ตัวเลขที่จะทำนาย)",
        "Nominal to Numerical → comparison_groups: คอลัมน์หมวดหมู่ + ค่าอ้างอิง (reference) · ไม่มีคอลัมน์หมวดหมู่ → ลบ",
        "Select Attributes (simple) → x ตัวเดียว + label",
        "Read CSV (new) → ข้อมูลใหม่ (คอลัมน์เดียวกัน)",
    ], extra="สมการ: res model → แท็บ Description/Data: Coefficient · p-value · y = intercept + Σ coef × x")
    y = y0 + 60
    rd = t.add(read_csv("Read CSV", DATA("p7_insurance.csv"), y=y))
    role = t.add(set_role("Set Role", "charges", x=180, y=y))
    n2n = t.add(Op("nominal_to_numerical", "Nominal to Numerical", {
        "coding_type": "dummy coding", "use_comparison_groups": True, "return_preprocessing_model": True,
        "comparison_groups": ("list", [("sex", "female"), ("smoker", "no"), ("region", "northeast")])}, x=315, y=y))
    mul = t.add(multiply("Multiply", 450, y))
    chain(t, [rd, role, n2n, mul])
    yy = y0
    lane_note(t, "§3 Simple linear regression (x ตัวเดียว) บนข้อมูลทั้งหมด → สมการ y = b0 + b1·x",
              "Select Attributes → attributes = age|charges (x|label)", yy, x=600, w=820)
    s = t.add(Op("select_attributes", "Select Attributes (simple)", {"attribute_filter_type": "subset", "attributes": "age|charges",
                                                                    "include_special_attributes": False}, x=600, y=yy + 62))
    l1 = t.add(Op("linear_regression", "Linear Regression (simple)", {"feature_selection": "none", "eliminate_colinear_features": True,
                                                                      "use_bias": True}, x=735, y=yy + 62))
    t.wire(mul, "output 1", s, "example set input"); t.wire(s, "example set output", l1, "training set")
    t.res(l1, "model")
    yy += LANE
    lane_note(t, "§4–§5 ⭐ Multiple LR + baseline (mean) บน hold-out 80/20 → MAE / RMSE / R² (squared_correlation)",
              "Split Data → partitions · Linear Regression → feature_selection = none (ใช้ทุกตัว) / M5 prime · model = สมการเต็ม", yy, x=600, w=820)
    sp = t.add(Op("split_data", "Split Data", {"partitions": ("enum", [0.8, 0.2], "ratio"), "sampling_type": "shuffled sampling",
                                               "use_local_random_seed": True, "local_random_seed": SEED}, x=600, y=yy + 62))
    t.wire(mul, "output 2", sp, "example set")
    mtr = t.add(multiply("Multiply (train)", 735, yy + 62)); mte = t.add(multiply("Multiply (test)", 735, yy + ROW2))
    t.wire(sp, "partition 1", mtr, "input"); t.wire(sp, "partition 2", mte, "input")
    for i, (tag, lr) in enumerate([("Baseline mean", baseline("Default Model (mean)", "average")),
                                   ("Linear Regression", Op("linear_regression", "Linear Regression", {
                                       "feature_selection": "none", "eliminate_colinear_features": True, "use_bias": True}))]):
        lr.x, lr.y = 870, yy + 62 + (ROW2 - 62) * i
        t.add(lr)
        t.wire(mtr, f"output {i + 1}", lr, "training set")
        ap = t.add(Op("apply_model", f"Apply Model ({tag})", {}, x=1005, y=yy + 62 + (ROW2 - 62) * i))
        t.wire(lr, "model", ap, "model"); t.wire(mte, f"output {i + 1}", ap, "unlabelled data")
        pf = t.add(reg_perf(f"Performance ({tag})", x=1140, y=yy + 62 + (ROW2 - 62) * i))
        t.wire(ap, "labelled data", pf, "labelled data")
        t.res(pf, "performance")
        if tag == "Linear Regression":
            t.res(ap, "model")
    yy += LANE2
    lane_note(t, "§6 เทียบใน CV: LR vs k-NN regression vs Decision Tree regression",
              "ดู RMSE ต่ำสุด / R² สูงสุด", yy, x=600, w=820)
    mm = t.add(multiply("Multiply (compare)", 600, yy + 62))
    t.wire(mul, "output 3", mm, "input")
    for i, (tag, lr, steps) in enumerate([("LR", Op("linear_regression", "Linear Regression", {"feature_selection": "none"}), []),
                                          ("kNN reg", knn(k=10), [norm()]),
                                          ("Tree reg", dt(depth=5), [])]):
        c = t.add(cv(tag, lr, reg_perf(f"Performance (CV {tag})"), steps=steps, folds=5, sampling="shuffled sampling",
                     x=735 + 135 * i, y=yy + 62))
        t.wire(mm, f"output {i + 1}", c, "example set")
        t.res(c, "performance 1")
    yy += LANE
    lane_note(t, "§7 ทำนายข้อมูลใหม่: dummy coding เดิม (preprocessing model) → Linear Regression (ทั้งชุด)", "", yy, x=600, w=820, h=40)
    lf = t.add(Op("linear_regression", "Linear Regression (final)", {"feature_selection": "none"}, x=600, y=yy + 62))
    t.wire(mul, "output 4", lf, "training set")
    rn = t.add(read_csv("Read CSV (new)", NEW("new_insurance.csv"), x=600, y=yy + ROW2))
    b1 = t.add(Op("apply_model", "Apply Model (dummy new)", {}, x=735, y=yy + ROW2))
    b2 = t.add(Op("apply_model", "Apply Model (LR new)", {}, x=870, y=yy + ROW2))
    t.wire(n2n, "preprocessing model", b1, "model"); t.wire(rn, "output", b1, "unlabelled data")
    t.wire(lf, "model", b2, "model"); t.wire(b1, "labelled data", b2, "unlabelled data")
    t.res(b2, "labelled data")
    write(t, "R06_linear_regression.rmp")


# ════════════════════════════ R07 · Logistic Regression ════════════════════════════
def r07():
    t = T()
    y0 = config_note(t, [
        "Read CSV → csv_file · Numerical to Binominal → label 0/1 (label เป็นคำอยู่แล้ว → ลบ) · Set Role → label",
        "Declare Missing Value → คอลัมน์ที่ค่า 0 เป็นไปไม่ได้ (ข้อมูลอื่น → ลบ operator)",
        "Create Threshold → threshold · first_class = คลาสลบ · second_class = คลาสบวก (ตอนนี้ false / true)",
        "Performance → positive_class = คลาสบวก (true)",
    ], extra="⚠️ H2O Logistic Regression ตัดสินที่ threshold ที่ทำให้ F1 สูงสุด (ไม่ใช่ 0.5) → อยากได้ 0.5 ต้องใช้ Create/Apply Threshold")
    y = y0 + 60
    rd = t.add(read_csv("Read CSV", DATA("p5_pima_diabetes.csv"), y=y))
    n2b = t.add(to_binominal("Numerical to Binominal", "diabetes", x=180, y=y))
    role = t.add(set_role("Set Role", "diabetes", x=315, y=y))
    dmv = t.add(Op("declare_missing_value", "Declare Missing Value", {
        "attribute_filter_type": "subset", "attributes": "glucose|blood_pressure|skin_thickness|insulin|bmi",
        "mode": "numeric", "numeric_value": 0.0}, x=450, y=y))
    mul0 = t.add(multiply("Multiply", 585, y))
    chain(t, [rd, n2b, role, dmv, mul0])
    sp = t.add(Op("split_data", "Split Data", {"partitions": ("enum", [0.75, 0.25], "ratio"), "sampling_type": "stratified sampling",
                                               "use_local_random_seed": True, "local_random_seed": SEED}, x=720, y=y0 + 62))
    t.wire(mul0, "output 1", sp, "example set")
    lane_note(t, "§1–§3 Split 75/25 → Replace Missing (fit train) → Logistic Regression → Apply กับ test",
              "res model = coefficients (+ p-value) · odds ratio = e^coef", y0, x=720, w=820)
    rmv = t.add(Op("replace_missing_values", "Replace Missing Values", {"default": "average", "return_preprocessing_model": True},
                   x=855, y=y0 + 62))
    lr = t.add(logreg()); lr.x, lr.y = 990, y0 + 62
    t.wire(sp, "partition 1", rmv, "example set input"); t.wire(rmv, "example set output", lr, "training set")
    a1 = t.add(Op("apply_model", "Apply Model (impute test)", {}, x=990, y=y0 + ROW2))
    a2 = t.add(Op("apply_model", "Apply Model (logistic)", {}, x=1125, y=y0 + ROW2))
    t.wire(rmv, "preprocessing model", a1, "model"); t.wire(sp, "partition 2", a1, "unlabelled data")
    t.wire(lr, "model", a2, "model"); t.wire(a1, "labelled data", a2, "unlabelled data")
    mmod = t.add(multiply("Multiply (model)", 1260, y0 + 62))
    t.wire(a2, "model", mmod, "input")
    t.res(mmod, "output 1")
    mul = t.add(multiply("Multiply (scored test)", 1260, y0 + ROW2))
    t.wire(a2, "labelled data", mul, "input")
    t.res(mul, "output 1")
    yy = y0 + LANE2 + 40   # Multiply (scored test) 5 port
    lane_note(t, "§5 ⭐ Threshold: default ของ H2O vs 0.5 vs 0.3 → confusion matrix + precision / recall / F1",
              "เพิ่ม threshold อื่น: copy Create Threshold + Apply Threshold + Performance แล้วต่อจาก Multiply (scored test) port ถัดไป",
              yy, x=720, w=820)
    pd_ = t.add(binom_perf("Performance (H2O default)", positive="true", x=1260, y=yy + 62))
    t.wire(mul, "output 2", pd_, "labelled data")
    t.res(pd_, "performance")
    for j, thv in enumerate([0.5, 0.3]):
        yj = yy + ROW2 + 150 * j
        thr = t.add(Op("create_threshold", f"Create Threshold {thv}", {"threshold": thv, "first_class": "false",
                                                                     "second_class": "true"}, x=990, y=yj))
        apt = t.add(Op("apply_threshold", f"Apply Threshold {thv}", {}, x=1125, y=yj))
        t.wire(mul, f"output {j + 3}", apt, "example set"); t.wire(thr, "output", apt, "threshold")
        pf = t.add(binom_perf(f"Performance (t={thv})", positive="true", x=1260, y=yj))
        t.wire(apt, "example set", pf, "labelled data")
        t.res(pf, "performance")
    yy += ROW2 + 150 + 140
    lane_note(t, "§2 / §6 Baseline vs Logistic ใน 10-fold CV (Replace Missing อยู่ใน Training pane)", "", yy, x=45, w=900, h=40)
    mm = t.add(multiply("Multiply (CV)", 45, yy + 62))
    t.wire(mul0, "output 2", mm, "input")
    for i, (tag, lrn, steps) in enumerate([("Baseline", baseline(), []),
                                           ("LogReg", logreg(), [Op("replace_missing_values", "Replace Missing Values", {
                                               "default": "average", "return_preprocessing_model": True})])]):
        c = t.add(cv(tag, lrn, binom_perf(f"Performance (CV {tag})", positive="true"), steps=steps, folds=10, x=180 + 135 * i, y=yy + 62))
        t.wire(mm, f"output {i + 1}", c, "example set")
        t.res(c, "performance 1")
    yy += LANE
    lane_note(t, "§7 ทำนายข้อมูลใหม่ → confidence(true) = ความน่าจะเป็น · prediction ตาม threshold ของ H2O",
              "Read CSV (new) → ไฟล์ข้อมูลใหม่ (ไม่ต้องมี label)", yy, x=45, w=900, h=50)
    rn = t.add(read_csv("Read CSV (new)", NEW("new_pima.csv"), x=45, y=yy + 62))
    b1 = t.add(Op("apply_model", "Apply Model (impute new)", {}, x=180, y=yy + 62))
    b2 = t.add(Op("apply_model", "Apply Model (logistic new)", {}, x=315, y=yy + 62))
    t.wire(a1, "model", b1, "model"); t.wire(rn, "output", b1, "unlabelled data")
    t.wire(mmod, "output 2", b2, "model"); t.wire(b1, "labelled data", b2, "unlabelled data")
    t.res(b2, "labelled data")
    write(t, "R07_logistic_regression.rmp")


# ════════════════════════════ R08 · Decision Tree & RF ════════════════════════════
def r08():
    t = T()
    y0 = config_note(t, [
        "Read CSV → csv_file · Numerical to Binominal → label 0/1 (label เป็นคำอยู่แล้ว → ลบ) · Set Role → label",
        "Decision Tree → criterion (gini_index / information_gain / gain_ratio) · maximal_depth · apply_pruning",
        "Read CSV (hand) + Set Role (hand) → ข้อมูลเล็กที่โจทย์ให้คำนวณ gain ด้วยมือ",
        "Performance → positive_class = true",
    ], extra="RapidMiner default = gain_ratio + pruning · ดูต้นไม้: res model → Graph / Description (กฎ IF-THEN)")
    y = y0 + 60
    rh = t.add(read_csv("Read CSV (hand)", P("final", "data", "weather.csv"), y=y))
    sh = t.add(set_role("Set Role (hand)", "Class", x=180, y=y))
    mh = t.add(multiply("Multiply (hand)", 315, y))
    chain(t, [rh, sh, mh])
    lane_note(t, "§0 คำนวณ impurity: Weight by Information Gain / Gain Ratio / Gini Index → ค่าสูงสุด = root",
              "normalize_weights = false (ค่าจริง) · ใช้กับ attribute หมวดหมู่ · ตรวจคำตอบที่คำนวณมือ", y0, x=450, w=760)
    for i, cls in enumerate(["weight_by_information_gain", "weight_by_information_gain_ratio", "weight_by_gini_index"]):
        w = t.add(Op(cls, cls.replace("weight_by_", "Weight by ").replace("_", " ").title(), {
            "normalize_weights": False, "sort_weights": True, "sort_direction": "descending"}, x=450 + 135 * i, y=y0 + 62))
        t.wire(mh, f"output {i + 1}", w, "example set")
        t.res(w, "weights")
    yy = y0 + LANE + 60
    rd = t.add(read_csv("Read CSV", DATA("p6_heart.csv"), y=yy))
    n2b = t.add(to_binominal("Numerical to Binominal", "target", x=180, y=yy))
    role = t.add(set_role("Set Role", "target", x=315, y=yy))
    mul = t.add(multiply("Multiply", 450, yy))
    chain(t, [rd, n2b, role, mul])
    yy -= 40
    lane_note(t, "§2 Decision Tree (depth 3) บนข้อมูลทั้งหมด → ต้นไม้ + กฎ + feature importance (Weight by Tree Importance)",
              "res model → Graph (ต้นไม้) / Description (กฎ IF-THEN)", yy, x=600, w=820)
    d0 = t.add(dt("Decision Tree (show)", 3)); d0.x, d0.y = 600, yy + 62
    t.wire(mul, "output 1", d0, "training set")
    t.res(d0, "model")
    yy += LANE
    lane_note(t, "§3 Overfitting: train accuracy ของต้นไม้เต็ม (Apply กับข้อมูลเดิม) — เทียบกับ CV ใน §6",
              "", yy, x=600, w=820, h=40)
    df = t.add(dt("Decision Tree (full)", 30)); df.x, df.y = 600, yy + 62
    t.wire(mul, "output 2", df, "training set")
    ap = t.add(Op("apply_model", "Apply Model (train acc)", {}, x=735, y=yy + 62))
    t.wire(df, "model", ap, "model"); t.wire(mul, "output 3", ap, "unlabelled data")
    pf = t.add(binom_perf("Performance (train acc)", positive="true", main="accuracy", x=870, y=yy + 62))
    t.wire(ap, "labelled data", pf, "labelled data")
    t.res(pf, "performance")
    yy += LANE
    lane_note(t, "§6 ⭐ CV: baseline vs Tree เต็ม vs Tree depth 3 vs Random Forest", "", yy, x=600, w=820, h=40)
    mm = t.add(multiply("Multiply (compare)", 600, yy + 62))
    t.wire(mul, "output 4", mm, "input")
    for i, (tag, lrn) in enumerate([("Baseline", baseline()), ("Tree full", dt(depth=30)), ("Tree d3", dt(depth=3)),
                                    ("Random Forest", rf(trees=100))]):
        c = t.add(cv(tag, lrn, binom_perf(f"Performance ({tag})", positive="true", main="accuracy"), folds=10,
                     x=735 + 135 * i, y=yy + 62))
        t.wire(mm, f"output {i + 1}", c, "example set")
        t.res(c, "performance 1")
    yy += LANE
    lane_note(t, "§4 ⭐ Optimize maximal_depth 1…12 (+ Log) → ตาราง depth vs accuracy (หาจุด overfit)",
              "เพิ่ม parameter: Edit Parameter Settings → criterion / minimal_leaf_size", yy, x=600, w=820)
    inner = cv("opt", dt("Decision Tree", 3), binom_perf("Performance (opt)", positive="true", main="accuracy"))
    optimize(t, mul, "output 5", inner, [("Decision Tree (opt).maximal_depth", "[1.0;12.0;11;linear]")],
             [("depth", "operator.Decision Tree (opt).parameter.maximal_depth"), ("accuracy", cv_value("CV opt"))], "depth", 600, yy + 62)
    yy += LANE
    lane_note(t, "§5 Random Forest บนข้อมูลทั้งหมด → ทำนายข้อมูลใหม่", "Read CSV (new) → ไฟล์ข้อมูลใหม่ · number_of_trees", yy, x=600, w=820, h=50)
    rff = t.add(rf("Random Forest (final)", trees=100)); rff.x, rff.y = 600, yy + 62
    t.wire(mul, "output 6", rff, "training set")
    rn = t.add(read_csv("Read CSV (new)", NEW("new_heart.csv"), x=600, y=yy + ROW2))
    b = t.add(Op("apply_model", "Apply Model (new)", {}, x=735, y=yy + 136))
    t.wire(rff, "model", b, "model"); t.wire(rn, "output", b, "unlabelled data")
    t.res(b, "labelled data")
    write(t, "R08_decision_tree_rf.rmp")


# ════════════════════════════ R09 · Classification Workflow ════════════════════════════
def r09():
    t = T()
    y0 = config_note(t, [
        "Read CSV → csv_file · Select Attributes → ตัด id / คอลัมน์ leak (invert_selection = true)",
        "Set Role → label · (label 0/1 → เพิ่ม Numerical to Binominal ก่อน)",
        "ทุก Performance → positive_class (ตอนนี้ = YES) · main_criterion (f_measure / accuracy / recall)",
        "ไม่ใช้โมเดลไหน → ลบ CV ของโมเดลนั้น · hold-out แทน CV → ดู R05 §3",
    ], extra="ผล: res ของแต่ละ CV = performance (เทียบกันในตารางคำตอบ) · ดับเบิลคลิก CV เพื่อแก้พารามิเตอร์ของโมเดล")
    y = y0 + 60
    rd = t.add(read_csv("Read CSV", P("final", "mock_lab", "mock3_cluster_assoc", "data", "bank-data.csv"), y=y))
    sel = t.add(Op("select_attributes", "Select Attributes", {"attribute_filter_type": "subset", "attributes": "id",
                                                              "invert_selection": True}, x=180, y=y))
    role = t.add(set_role("Set Role", "pep", x=315, y=y))
    mul = t.add(multiply("Multiply", 450, y))
    chain(t, [rd, sel, role, mul])
    pos = "YES"
    prep = lambda: [Op("replace_missing_values", "Replace Missing Values", {"default": "average", "return_preprocessing_model": True}),  # noqa: E731
                    Op("nominal_to_numerical", "Nominal to Numerical", {"coding_type": "dummy coding", "return_preprocessing_model": True}),
                    norm()]
    yy = y0
    lane_note(t, "§4 ⭐ Baseline vs โมเดล default (10-fold CV) — preprocessing ทั้งหมดอยู่ใน Training pane",
              "KNN / Logistic: Replace Missing + dummy + Normalize · Tree / RF: ไม่ต้อง normalize", yy, x=600, w=900)
    mm = t.add(multiply("Multiply (default)", 600, yy + 62))
    t.wire(mul, "output 1", mm, "input")
    for i, (tag, lrn, steps) in enumerate([("Baseline", baseline(), []), ("kNN", knn(k=5), prep()),
                                           ("LogReg", logreg(), prep()[:2]), ("Tree", dt(depth=10), []),
                                           ("RF", rf(trees=100), [])]):
        c = t.add(cv(tag, lrn, binom_perf(f"Performance ({tag})", positive=pos), steps=steps, folds=10, x=735 + 135 * i, y=yy + 62))
        t.wire(mm, f"output {i + 1}", c, "example set")
        t.res(c, "performance 1")
    yy += LANE + 40   # Multiply 6 port สูงกว่า CV
    lane_note(t, "§5 ⭐ Optimize k-NN: k = 1…31 (+ Log)", "Edit Parameter Settings เพื่อเปลี่ยนช่วง", yy, x=600, w=900, h=50)
    inner = cv("opt kNN", knn("k-NN"), binom_perf("Performance (opt kNN)", positive=pos), steps=prep())
    optimize(t, mul, "output 2", inner, [("k-NN (opt kNN).k", "[1.0;31.0;15;linear]")],
             [("k", "operator.k-NN (opt kNN).parameter.k"), ("f_measure", cv_value("CV opt kNN"))], "kNN", 600, yy + 62)
    yy += LANE
    lane_note(t, "§5 ⭐ Optimize Decision Tree: maximal_depth 2…12 × criterion (+ Log)", "", yy, x=600, w=900, h=40)
    inner = cv("opt Tree", dt("Decision Tree", 5), binom_perf("Performance (opt Tree)", positive=pos))
    optimize(t, mul, "output 3", inner, [("Decision Tree (opt Tree).maximal_depth", "[2.0;12.0;10;linear]"),
                                         ("Decision Tree (opt Tree).criterion", "gini_index,information_gain,gain_ratio")],
             [("depth", "operator.Decision Tree (opt Tree).parameter.maximal_depth"),
              ("criterion", "operator.Decision Tree (opt Tree).parameter.criterion"),
              ("f_measure", cv_value("CV opt Tree"))], "Tree", 600, yy + 62)
    yy += LANE
    lane_note(t, "§6–§8 โมเดลสุดท้าย (ใส่ค่าที่ดีที่สุดจาก §5 เอง) → ทำนายข้อมูลใหม่",
              "Decision Tree (final) → maximal_depth / criterion ตามผล optimize · Read CSV (new) → ไฟล์ใหม่", yy, x=600, w=900)
    fin = t.add(dt("Decision Tree (final)", 6)); fin.x, fin.y = 600, yy + 62
    t.wire(mul, "output 4", fin, "training set")
    rn = t.add(read_csv("Read CSV (new)", NEW("new_bank.csv"), x=600, y=yy + ROW2))
    b = t.add(Op("apply_model", "Apply Model (new)", {}, x=735, y=yy + 136))
    t.wire(fin, "model", b, "model"); t.wire(rn, "output", b, "unlabelled data")
    t.res(b, "labelled data"); t.res(b, "model")
    write(t, "R09_classification_workflow.rmp")


# ════════════════════════════ R10 · Clustering ════════════════════════════
def r10():
    t = T()
    y0 = config_note(t, [
        "Read CSV → csv_file · Set Role → id = ชื่อ/รหัสแถว (ไม่ใช้คำนวณ) · มี label จริง → Set Role (label) หรือ Select Attributes ตัดออก",
        "Clustering (k-Means) → k · max_runs · measure_types = NumericalMeasures / EuclideanDistance",
        "Read CSV (new) → จุดใหม่ (คอลัมน์ feature เดียวกัน)",
    ], extra="centroid: res cluster model → Centroid Table (ค่า normalize แล้ว: + สูงกว่าค่าเฉลี่ย, − ต่ำกว่า) · กราฟ: Visualizations / Centroid Chart")
    y = y0 + 60
    rd = t.add(read_csv("Read CSV", P("final", "data", "utilities.csv"), y=y))
    role = t.add(set_role("Set Role", "Company", "id", x=180, y=y))
    nm = t.add(norm("Normalize", x=315, y=y))
    mul = t.add(multiply("Multiply", 450, y))
    chain(t, [rd, role, nm, mul])
    yy = y0
    lane_note(t, "§3 ⭐ k-Means (k = 4) → Cluster Distance Performance (avg within centroid distance + Davies–Bouldin)",
              "res: clustered set (คอลัมน์ cluster) · cluster model (centroid) · performance (cohesion) · main_criterion เปลี่ยนได้", yy, x=600, w=820)
    km = t.add(Op("concurrency:k_means", "Clustering", {
        "add_cluster_attribute": True, "k": 4, "max_runs": 50, "determine_good_start_values": True,
        "measure_types": "NumericalMeasures", "numerical_measure": "EuclideanDistance",
        "max_optimization_steps": 100, "use_local_random_seed": True, "local_random_seed": SEED}, x=600, y=yy + 62))
    t.wire(mul, "output 1", km, "example set")
    cdp = t.add(Op("cluster_distance_performance", "Cluster Distance Performance", {
        "main_criterion": "Avg. within centroid distance", "main_criterion_only": False}, x=735, y=yy + 62))
    t.wire(km, "clustered set", cdp, "example set"); t.wire(km, "cluster model", cdp, "cluster model")
    mc = t.add(multiply("Multiply (clustered)", 870, yy + 62))
    t.wire(cdp, "example set", mc, "input")
    mcm = t.add(multiply("Multiply (cluster model)", 870, yy + ROW2))
    t.wire(cdp, "cluster model", mcm, "input")
    t.res(cdp, "performance"); t.res(mc, "output 1"); t.res(mcm, "output 1")
    yy += LANE2
    lane_note(t, "§3b Profile แต่ละกลุ่มในหน่วยเดิม: Aggregate average ตาม cluster",
              "group_by = cluster · ค่าเฉลี่ยของ feature (เป็นค่า normalize — อยากได้หน่วยเดิม Join กลับกับข้อมูลดิบด้วย id)", yy, x=600, w=820)
    agg = t.add(Op("aggregate", "Aggregate (profile)", {"use_default_aggregation": True, "default_aggregation_function": "average",
                                                        "group_by_attributes": "cluster"}, x=600, y=yy + 62))
    t.wire(mc, "output 2", agg, "example set input")
    t.res(agg, "example set output")
    yy += LANE
    lane_note(t, "§2 ⭐ เลือก k: Optimize Parameters k = 2…10 + Log (avg within centroid distance → หา elbow)",
              "Log to Data → Visualizations → Line (x = k) · Davies–Bouldin ของ k ที่เลือก ดูใน performance ของ §3 (RapidMiner แสดงค่าติดลบ: ใกล้ 0 = ดี)", yy, x=600, w=820)
    inner = Proc()
    k2 = inner.add(Op("concurrency:k_means", "Clustering (opt)", {"add_cluster_attribute": True, "k": 2, "max_runs": 50,
                                                                 "determine_good_start_values": True,
                                                                 "use_local_random_seed": True, "local_random_seed": SEED}))
    c2 = inner.add(Op("cluster_distance_performance", "Cluster Distance Performance (opt)", {
        "main_criterion": "Avg. within centroid distance", "main_criterion_only": False}, x=180))
    log = inner.add(Op("log", "Log (k)", {"log": ("list", [
        ("k", "operator.Clustering (opt).parameter.k"),
        ("avg_within", "operator.Cluster Distance Performance (opt).value.avg_within_distance")]),
        "sorting_type": "none", "persistent": False}, x=315))
    inner.wire(None, "input 1", k2, "example set")
    inner.wire(k2, "clustered set", c2, "example set"); inner.wire(k2, "cluster model", c2, "cluster model")
    inner.wire(c2, "performance", log, "through 1"); inner.wire(log, "through 1", None, "performance")
    opt = t.add(Op("concurrency:optimize_parameters_grid", "Optimize Parameters (k)", {
        "parameters": ("list", [("Clustering (opt).k", "[2.0;10.0;8;linear]")])}, subprocesses=[inner], x=600, y=yy + 62))
    t.wire(mul, "output 2", opt, "input 1")
    l2d = t.add(Op("log_to_data", "Log to Data (k)", {"log_name": "Log (k)"}, x=735, y=yy + 62))
    t.res(l2d, "exampleSet")
    yy += LANE
    lane_note(t, "§4 จุดใหม่อยู่ cluster ไหน: Normalize ด้วยค่าเดิม (preprocessing model) → Apply cluster model", "", yy, x=600, w=820, h=40)
    rn = t.add(read_csv("Read CSV (new)", NEW("new_utility.csv"), x=600, y=yy + 62))
    rnr = t.add(set_role("Set Role (new)", "Company", "id", x=735, y=yy + 62))
    t.wire(rn, "output", rnr, "example set input")
    b1 = t.add(Op("apply_model", "Apply Model (normalize new)", {}, x=870, y=yy + 62))
    b2 = t.add(Op("apply_model", "Apply Model (cluster new)", {}, x=1005, y=yy + 62))
    t.wire(nm, "preprocessing model", b1, "model"); t.wire(rnr, "example set output", b1, "unlabelled data")
    t.wire(mcm, "output 2", b2, "model"); t.wire(b1, "labelled data", b2, "unlabelled data")
    t.res(b2, "labelled data")
    yy += LANE
    lane_note(t, "§6 ภาพ cluster บน PCA 2D → Visualizations → Scatter pc_1 × pc_2 color = cluster", "", yy, x=600, w=820, h=40)
    pca = t.add(Op("principal_component_analysis", "PCA (2D)", {"dimensionality_reduction": "fixed number",
                                                               "number_of_components": 2}, x=600, y=yy + 62))
    t.wire(mc, "output 3", pca, "example set input")
    t.res(pca, "example set output")
    yy += LANE
    lane_note(t, "§7 Hierarchical (Agglomerative) → dendrogram (res: Dendrogram) → Flatten Clustering = ตัดเป็น k กลุ่ม",
              "mode = SingleLink / CompleteLink / AverageLink · number_of_clusters", yy, x=600, w=820)
    ag = t.add(Op("agglomerative_clustering", "Clustering (Agglomerative)", {"mode": "CompleteLink", "measure_types": "NumericalMeasures",
                                                                            "numerical_measure": "EuclideanDistance"}, x=600, y=yy + 62))
    fl = t.add(Op("flatten_clustering", "Flatten Clustering", {"number_of_clusters": 4}, x=735, y=yy + 62))
    t.wire(mul, "output 3", ag, "example set")
    t.wire(ag, "cluster model", fl, "hierarchical"); t.wire(ag, "example set", fl, "example set")
    t.res(fl, "example set"); t.res(fl, "flat")
    write(t, "R10_clustering.rmp")


# ════════════════════════════ R11 · Association Rules ════════════════════════════
def r11():
    t = T()
    y0 = config_note(t, [
        "เลือกแถวที่ตรงกับหน้าตาข้อมูล (A = ตาราง 0/1 ต่อสินค้า · B = ตารางลูกค้า/attribute) แล้วลบแถวที่ไม่ใช้",
        "Read Excel / Read CSV → ไฟล์ · Set Role → id = รหัสตะกร้า/ลูกค้า",
        "FP-Growth → min_support (สัดส่วน เช่น 0.2) · Create Association Rules → min_confidence",
        "ข้อมูลแบบ 'ตะกร้าคั่นด้วย comma ต่อบรรทัด' → แปลงด้วย Python T11 แล้วใช้แถว A",
    ], extra="ผล: res rules → Table (Premises → Conclusion · Support · Confidence · Lift) · เรียงตาม Lift ได้ · res itemsets = frequent itemsets")
    yy = y0
    lane_note(t, "A · ตาราง 0/1 (BeautyCo): Read Excel → Set Role id → Numerical to Binominal (0/1 → false/true) → FP-Growth → Rules",
              "min_support = 0.2 · min_confidence = 0.7 · ไฟล์ .csv ใช้ Read CSV แทน Read Excel", yy, x=45, w=1000)
    rx = t.add(Op("read_excel", "Read Excel (A)", {"excel_file": P("W10", "BeautyCo_68.xls"), "sheet_number": 1,
                                                    "first_row_as_names": True}, x=45, y=yy + 62))
    ra = t.add(set_role("Set Role (A)", "Trans.", "id", x=180, y=yy + 62))
    na = t.add(Op("numerical_to_binominal", "Numerical to Binominal (A)", {"attribute_filter_type": "all", "min": 0.0, "max": 0.0},
                  x=315, y=yy + 62))
    chain(t, [rx, ra, na])
    fa = t.add(Op("concurrency:fp_growth", "FP-Growth (A)", {
        "input_format": "items in dummy coded columns", "positive_value": "true", "min_requirement": "support",
        "min_support": 0.2, "find_min_number_of_itemsets": False, "max_items_per_itemset": 0}, x=450, y=yy + 62))
    ca = t.add(Op("create_association_rules", "Create Association Rules (A)", {"criterion": "confidence", "min_confidence": 0.7},
                  x=585, y=yy + 62))
    t.wire(na, "example set output", fa, "example set"); t.wire(fa, "frequent sets", ca, "item sets")
    t.res(ca, "rules"); t.res(ca, "item sets")
    yy += LANE + 20
    lane_note(t, "B · ตารางลูกค้า (bank): ตัด id/คอลัมน์ไม่ให้ข้อมูล → Discretize ตัวเลข → Nominal to Binominal → FP-Growth → Rules",
              "Discretize by Frequency → attributes (age|income) + number_of_bins · Discretize by User Specification → children · Nominal to Binominal → transform_binominal = true", yy, x=45, w=1000)
    rb = t.add(read_csv("Read CSV (B)", P("final", "mock_lab", "mock3_cluster_assoc", "data", "bank-data.csv"), x=45, y=yy + 62))
    sb = t.add(Op("select_attributes", "Select Attributes (B)", {"attribute_filter_type": "subset",
                                                                 "attributes": "id|region|sex|current_act", "invert_selection": True},
                  x=180, y=yy + 62))
    dfq = t.add(Op("discretize_by_frequency", "Discretize by Frequency (B)", {
        "attribute_filter_type": "subset", "attributes": "age|income", "number_of_bins": 3, "range_name_type": "short"}, x=315, y=yy + 62))
    dus = t.add(Op("discretize_by_user_specification", "Discretize by User Specification (B)", {
        "attribute_filter_type": "single", "attribute": "children",
        "classes": ("list", [("0", 0.5), ("1-2", 2.5), ("3+", "Infinity")])}, x=450, y=yy + 62))
    nb = t.add(Op("nominal_to_binominal", "Nominal to Binominal (B)", {"attribute_filter_type": "all", "transform_binominal": True},
                  x=585, y=yy + 62))
    chain(t, [rb, sb, dfq, dus, nb])
    fb = t.add(Op("concurrency:fp_growth", "FP-Growth (B)", {
        "input_format": "items in dummy coded columns", "positive_value": "true", "min_requirement": "support",
        "min_support": 0.1, "find_min_number_of_itemsets": False}, x=720, y=yy + 62))
    cb = t.add(Op("create_association_rules", "Create Association Rules (B)", {"criterion": "confidence", "min_confidence": 0.7},
                  x=855, y=yy + 62))
    t.wire(nb, "example set output", fb, "example set"); t.wire(fb, "frequent sets", cb, "item sets")
    t.res(cb, "rules"); t.res(cb, "item sets")
    yy += LANE + 20
    lane_note(t, "C · ตาราง 0/1 ขนาดใหญ่ (groceries 169 สินค้า) — เหมือน A แต่ Read CSV", "min_support = 0.02 · min_confidence = 0.3", yy, x=45, w=1000, h=50)
    rc = t.add(read_csv("Read CSV (C)", DATA("p9_groceries_onehot.csv"), x=45, y=yy + 62))
    rcr = t.add(set_role("Set Role (C)", "basket_id", "id", x=180, y=yy + 62))
    nc = t.add(Op("numerical_to_binominal", "Numerical to Binominal (C)", {"attribute_filter_type": "all", "min": 0.0, "max": 0.0},
                  x=315, y=yy + 62))
    chain(t, [rc, rcr, nc])
    fc = t.add(Op("concurrency:fp_growth", "FP-Growth (C)", {
        "input_format": "items in dummy coded columns", "positive_value": "true", "min_requirement": "support",
        "min_support": 0.02, "find_min_number_of_itemsets": False}, x=450, y=yy + 62))
    cc = t.add(Op("create_association_rules", "Create Association Rules (C)", {"criterion": "confidence", "min_confidence": 0.3},
                  x=585, y=yy + 62))
    t.wire(nc, "example set output", fc, "example set"); t.wire(fc, "frequent sets", cc, "item sets")
    t.res(cc, "rules")
    write(t, "R11_association_rules.rmp")


NEW_FILES = {
    "new_mower.csv": "Income,Lot_Size\n60,20\n",
    "new_insurance.csv": "age,sex,bmi,children,smoker,region\n40,male,30.0,2,no,northeast\n",
    "new_pima.csv": "pregnancies,glucose,blood_pressure,skin_thickness,insulin,bmi,pedigree,age\n2,150,70,30,100,32.0,0.5,45\n",
    "new_heart.csv": "age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal\n55,1,0,140,250,0,1,140,1,1.5,1,1,3\n",
    "new_bank.csv": "age,sex,region,income,married,children,car,save_act,current_act,mortgage\n"
                    "40,FEMALE,TOWN,30000.0,YES,1,NO,YES,YES,NO\n",
    "new_utility.csv": "Company,Fixed_charge,RoR,Cost,Load_factor,Demand_growth,Sales,Nuclear,Fuel_Cost\n"
                       "NewCo,1.10,11.0,160,56,3.0,14000,0,0.70\n",
}

if __name__ == "__main__":
    (OUTDIR / "data").mkdir(exist_ok=True)
    for f, txt in NEW_FILES.items():
        (OUTDIR / "data" / f).write_text(txt, encoding="utf-8")
    only = sys.argv[1:] or ["r01", "r02", "r03", "r04", "r05", "r06", "r07", "r08", "r09", "r10", "r11"]
    for fn in only:
        globals()[fn]()
    import runpy
    runpy.run_path(str(HERE / "make_opmap.py"))
