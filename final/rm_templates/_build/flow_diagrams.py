"""วาดภาพ canvas แบบ RapidMiner (mermaid) จาก R01–R11 แล้วแทรกลงโน้ต FLOW 01–11

- อ่าน operator + เส้นเชื่อมจาก .rmp จริง (ไม่ได้วาดมือ) → ภาพตรงกับ template ที่เปิดใน RapidMiner
- กล่อง = operator (บรรทัดบน = ชื่อบน canvas · บรรทัดล่าง = ชนิด operator) · สีตามหมวดเหมือนแผง Operators
- ป้ายบนเส้น = ชื่อ port ย่อแบบบน canvas (exa / mod / per / pre / lab / tra / tes …) · ◯ res = port ผลลัพธ์ขอบขวา
- operator ที่มี subprocess (Cross Validation / Optimize) วาดข้างในเป็นภาพแยก: pane Training | Testing
- แทรกใต้แต่ละขั้นใน "## ทีละขั้น" เป็นกล่องพับได้ ระหว่าง <!-- RM-CANVAS … --> (รันซ้ำได้ แทนที่ของเดิม)

รัน: python final/rm_templates/_build/flow_diagrams.py
"""
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLOW = ROOT.parent / "obsidian" / "flow"

TYPE = {
    "read_csv": "Read CSV", "read_excel": "Read Excel", "append": "Append", "concurrency:join": "Join",
    "generate_attributes": "Generate Attributes", "multiply": "Multiply", "filter_examples": "Filter Examples",
    "aggregate": "Aggregate", "blending:pivot": "Pivot", "set_role": "Set Role", "select_attributes": "Select Attributes",
    "normalize": "Normalize", "principal_component_analysis": "PCA", "discretize_by_frequency": "Discretize by Frequency",
    "discretize_by_bins": "Discretize by Binning", "discretize_by_user_specification": "Discretize by User Spec.",
    "concurrency:cross_validation": "Cross Validation", "replace_missing_values": "Replace Missing Values",
    "nominal_to_numerical": "Nominal to Numerical", "nominal_to_binominal": "Nominal to Binominal",
    "numerical_to_binominal": "Numerical to Binominal", "k_nn": "k-NN", "group_models": "Group Models",
    "apply_model": "Apply Model", "performance_classification": "Performance (Classification)",
    "performance_binominal_classification": "Performance (Binominal)", "performance_regression": "Performance (Regression)",
    "default_model": "Default Model", "concurrency:parallel_decision_tree": "Decision Tree", "sample": "Sample",
    "sample_stratified": "Sample (Stratified)", "operator_toolbox:smote": "SMOTE Upsampling",
    "concurrency:optimize_parameters_grid": "Optimize Parameters (Grid)", "log": "Log", "log_to_data": "Log to Data",
    "declare_missing_value": "Declare Missing Value", "split_data": "Split Data",
    "h2o:logistic_regression": "Logistic Regression", "create_threshold": "Create Threshold",
    "apply_threshold": "Apply Threshold", "concurrency:parallel_random_forest": "Random Forest",
    "linear_regression": "Linear Regression", "concurrency:k_means": "k-Means",
    "cluster_distance_performance": "Cluster Distance Performance", "concurrency:fp_growth": "FP-Growth",
    "create_association_rules": "Create Association Rules", "cross_distances": "Cross Distances",
    "weight_by_information_gain": "Weight by Information Gain", "weight_by_information_gain_ratio": "Weight by Gain Ratio",
    "weight_by_gini_index": "Weight by Gini Index", "select_by_weights": "Select by Weights",
    "agglomerative_clustering": "Agglomerative Clustering", "flatten_clustering": "Flatten Clustering",
    "detect_outlier_distances": "Detect Outlier (Distances)", "correlation_matrix": "Correlation Matrix",
    "sort": "Sort",
}
# หมวด → สี (ใกล้กับสีหมวดในแผง Operators ของ RapidMiner)
CAT = {
    "data": ["read_csv", "read_excel"],
    "blend": ["append", "concurrency:join", "blending:pivot", "aggregate", "filter_examples", "select_attributes",
              "set_role", "generate_attributes", "sort", "sample", "sample_stratified", "split_data"],
    "clean": ["normalize", "replace_missing_values", "declare_missing_value", "nominal_to_numerical",
              "nominal_to_binominal", "numerical_to_binominal", "discretize_by_frequency", "discretize_by_bins",
              "discretize_by_user_specification", "principal_component_analysis", "operator_toolbox:smote",
              "detect_outlier_distances", "weight_by_information_gain", "weight_by_information_gain_ratio",
              "weight_by_gini_index", "select_by_weights"],
    "model": ["k_nn", "default_model", "concurrency:parallel_decision_tree", "concurrency:parallel_random_forest",
              "h2o:logistic_regression", "linear_regression", "concurrency:k_means", "agglomerative_clustering",
              "flatten_clustering", "concurrency:fp_growth", "create_association_rules", "group_models"],
    "score": ["apply_model", "create_threshold", "apply_threshold", "cross_distances"],
    "eval": ["performance_classification", "performance_binominal_classification", "performance_regression",
             "cluster_distance_performance", "concurrency:cross_validation", "concurrency:optimize_parameters_grid",
             "correlation_matrix"],
    "util": ["multiply", "log", "log_to_data"],
}
CATOF = {c: k for k, v in CAT.items() for c in v}
CLASSDEF = [
    "classDef data fill:#e8dcf5,stroke:#7b52ab,color:#000",
    "classDef blend fill:#dceefb,stroke:#3a7bbf,color:#000",
    "classDef clean fill:#d9f2e6,stroke:#2e8b57,color:#000",
    "classDef model fill:#ffe7c2,stroke:#d4860b,color:#000",
    "classDef score fill:#fff6b3,stroke:#b8a400,color:#000",
    "classDef eval fill:#fcd9d9,stroke:#c0392b,color:#000",
    "classDef util fill:#eeeeee,stroke:#777,color:#000",
    "classDef port fill:#ffffff,stroke:#999,stroke-dasharray:3 3,color:#555",
    "classDef res fill:#ffffff,stroke:#333,stroke-width:2px,color:#000",
]


def short(port):
    if port in ("exa", "ups", "ori"):
        return port
    m = re.search(r"\s(\d+)$", port)
    return port[:3].lower() + (f" {m.group(1)}" if m else "")


def esc(s):
    return s.replace('"', "'")


class Pane:
    def __init__(self, el):
        self.ops = {o.get("name"): o for o in el.findall("operator")}
        self.edges = [(c.get("from_op"), c.get("from_port"), c.get("to_op"), c.get("to_port")) for c in el.findall("connect")]


def load(rmp):
    root = ET.parse(ROOT / rmp).getroot()
    return root.find("operator/process")


def find_op(proc_el, name):
    for o in proc_el.iter("operator"):
        if o.get("name") == name:
            return o
    raise KeyError(name)


def box(nid, op, label=None, strip_tag=False):
    cls = op.get("class")
    typ = TYPE.get(cls, cls)
    name = label or op.get("name")
    if strip_tag:                                   # ข้างใน subprocess: "k-NN (kNN raw)" → "k-NN"
        base = re.sub(r"\s*\([^)]*\)$", "", name)
        if typ.startswith(base) or base.startswith(typ):
            name = typ
    text = typ if name == typ else f"{esc(name)}<br/><i>{typ}</i>"
    if op.findall("process"):
        text += "<br/>⧉"
    return f'{nid}["{text}"]:::{CATOF.get(cls, "util")}'


def draw(pane, names, ind="  ", prefix="n", res_label="res", left_ports=None, right_ports=None, strip_tag=False):
    """วาด operator ใน names ของ pane หนึ่ง · คืน (บรรทัด, ids)"""
    lines, ids = [], {}
    for i, n in enumerate(names):
        ids[n] = f"{prefix}{i}"
        lines.append(ind + box(ids[n], pane.ops[n], strip_tag=strip_tag))
    used_res, used_lp, used_rp = set(), set(), set()
    for fo, fp, to, tp in pane.edges:
        if fo is not None and fo not in ids:
            continue
        if to is not None and to not in ids:
            continue
        if fo is None:                                 # port ขอบซ้ายของ pane
            if left_ports is None:
                continue
            pid = f"{prefix}L{len(used_lp)}"
            used_lp.add(pid)
            lines.append(f'{ind}{pid}(["{short(fp)}"]):::port')
            src = pid
        else:
            src = ids[fo]
        if to is None:                                 # port ขอบขวา (res ของ process หลัก)
            if right_ports is None and fo is not None and pane.ops[fo].get("class") == "multiply" and any(
                    e[0] == fo and e[2] in ids for e in pane.edges):
                continue                               # Multiply ที่ส่งต่อให้ขั้นนี้อยู่แล้ว → ไม่วาดเส้นไป res ของ § อื่น
            if right_ports is None:
                rid = f"{prefix}R{len(used_res)}"
                used_res.add(rid)
                lines.append(f'{ind}{rid}(("{res_label}")):::res')
            else:
                rid = f"{prefix}P{len(used_rp)}"
                used_rp.add(rid)
                lines.append(f'{ind}{rid}(["{short(tp)}"]):::port')
            lines.append(f'{ind}{src} -->|"{short(fp) if fo else ""}"| {rid}')
        else:
            if fo is None:                             # จาก port ขอบ pane: ชื่อ port อยู่ในกล่องแล้ว
                lines.append(f'{ind}{src} --> {ids[to]}')
            else:
                lines.append(f'{ind}{src} -->|"{short(fp)}"| {ids[to]}')
    return lines


def main_view(rmp, names):
    pane = Pane(load(rmp))
    missing = [n for n in names if n not in pane.ops]
    assert not missing, (rmp, missing)
    return "\n".join(["flowchart LR"] + draw(pane, names) + ["  " + c for c in CLASSDEF])


def sub_view(rmp, op_name):
    """ข้างใน operator ที่มี subprocess: แต่ละ pane เป็น subgraph"""
    op = find_op(load(rmp), op_name)
    panes = op.findall("process")
    titles = ["Training", "Testing"] if op.get("class") == "concurrency:cross_validation" else ["ข้างใน"]
    lines = ["flowchart LR", f'  subgraph S["{esc(op_name)} · {TYPE.get(op.get("class"))}"]', "    direction LR"]
    for i, pel in enumerate(panes):
        pane = Pane(pel)
        lines.append(f'    subgraph P{i}["{titles[i] if i < len(titles) else "pane"}"]')
        lines.append("      direction LR")
        lines += draw(pane, list(pane.ops), ind="      ", prefix=f"p{i}x", left_ports=True, right_ports=True, strip_tag=True)
        lines.append("    end")
    if len(panes) > 1:                                 # Training ซ้าย · Testing ขวา (เหมือนใน RapidMiner)
        lines.append("    P0 ~~~ P1")
    lines.append("  end")
    return "\n".join(lines + ["  " + c for c in CLASSDEF])


# ───────────── ภาพใต้แต่ละขั้น: STEPS[flow] = [(เลขขั้น ①…, หัวข้อ, คำอธิบาย, spec), …] ─────────────
# spec = ("main", ไฟล์ R, [ชื่อ operator บน canvas หลัก])  หรือ  ("sub", ไฟล์ R, ชื่อ operator ที่จะวาดข้างใน)
R = {i: f for i, f in enumerate(sorted(p.name for p in ROOT.glob("R*.rmp")), start=1)}
M, S = "main", "sub"
STEPS = {
    1: [("③", "Append (exa 1 + exa 2) → Join (lef + rig) → Multiply แตกสำเนาให้แต่ละ §", "", (M, R[1], [
            "Read CSV (หลัก)", "Read CSV (append)", "Read CSV (lookup)", "Append", "Join", "Multiply"])),
        ("⑤", "Select Attributes → Set Role (id) → Set Role (label)", "", (M, R[1], [
            "Multiply", "Select Attributes", "Set Role (id)", "Set Role (label)"])),
        ("⑥", "Filter Examples · Generate Attributes (แต่ละตัวรับสำเนาจาก Multiply)", "", (M, R[1], [
            "Multiply", "Filter Examples", "Generate Attributes"])),
        ("⑧", "Aggregate · Generate (คอลัมน์ 0/1) → Pivot (average = สัดส่วน)", "", (M, R[1], [
            "Multiply", "Aggregate", "Generate Attributes (rate)", "Pivot"])),
        ("⑨", "กราฟ = Results → Visualizations ของ res ข้อมูล · Correlation Matrix → mat", "", (M, R[1], [
            "Multiply", "Correlation Matrix"]))],
    2: [("①", "Read CSV → Declare Missing Value (? → ว่าง) → Set Role → Multiply", "", (M, R[2], [
            "Read CSV", "Declare Missing Value", "Set Role", "Multiply"])),
        ("②", "เติมค่าว่าง หรือ ตัดแถวที่ว่าง", "", (M, R[2], [
            "Multiply", "Replace Missing Values", "Filter Examples (not missing)"])),
        ("③", "Detect Outlier ใช้ระยะทาง → เลือกเฉพาะตัวเลข + เติมค่าว่างก่อน → กรอง outlier = false", "", (M, R[2], [
            "Multiply", "Select Attributes (numeric)", "Replace Missing (outlier)", "Detect Outlier (Distances)",
            "Filter Examples (no outlier)"])),
        ("④", "Nominal to Numerical (dummy coding = one-hot)", "", (M, R[2], ["Multiply", "Nominal to Numerical"])),
        ("⑤", "Normalize: Z-transformation vs range transformation", "", (M, R[2], [
            "Multiply", "Normalize (Z)", "Normalize (0-1)"])),
        ("⑥", "Discretize 3 แบบ", "", (M, R[2], [
            "Multiply", "Discretize by Binning", "Discretize by Frequency", "Discretize by User Specification"])),
        ("⑦", "Sample · Sample (Stratified)", "", (M, R[2], ["Multiply", "Sample (relative)", "Sample (Stratified)"])),
        ("⑧", "Hold-out ไม่ leak: fit บน train → เส้น pre ส่ง 'ค่าที่เรียนจาก train' ไปใช้กับ test ผ่าน Apply Model", "", (M, R[2], [
            "Multiply", "Split Data", "Replace Missing (train)", "Normalize (train)", "Apply Model (missing → test)",
            "Apply Model (normalize → test)"])),
        ("⑧", "ข้างใน Cross Validation: preprocessing อยู่ใน Training → Group Models มัดรวมกับโมเดล → Testing ใช้กับ test fold",
         "ทุก fold fit ค่าใหม่จาก training fold ของตัวเอง = ไม่ leak", (S, R[2], "CV kNN normalized")),
        ("⑨", "Weight by Information Gain → Select by Weights (top k)", "", (M, R[2], [
            "Multiply", "Weight by Information Gain", "Select by Weights"]))],
    3: [("①", "เลือกเฉพาะตัวเลข (label ตั้ง role ไว้ → ไม่ถูกใช้ใน PCA)", "", (M, R[3], [
            "Read CSV", "Set Role", "Select Attributes", "Multiply"])),
        ("②", "Normalize → PCA · pre = PCA model (Eigenvalues = §③ · Eigenvectors = §④)", "", (M, R[3], [
            "Multiply", "Normalize (pca)", "PCA (keep variance)"])),
        ("⑤", "PCA 2 components → Visualizations: Scatter pc_1 × pc_2 สีตาม label", "", (M, R[3], [
            "Multiply", "Normalize (2D)", "PCA (2 components)"])),
        ("⑥", "เทียบ kNN ก่อน/หลัง PCA ด้วย CV เดียวกัน", "", (M, R[3], ["Multiply", "Multiply (compare)", "CV kNN",
                                                                        "CV kNN + PCA"])),
        ("⑥", "ข้างใน CV kNN + PCA: Normalize + PCA อยู่ใน Training", "", (S, R[3], "CV kNN + PCA"))],
    4: [("①", "ดูสัดส่วน (res ของ Multiply → Statistics) · baseline ใน CV", "", (M, R[4], [
            "Read CSV", "Set Role", "Multiply", "CV Baseline"])),
        ("④", "ข้างใน CV SMOTE: SMOTE อยู่ใน Training (exa → ups) · test fold ใน Testing ไม่ถูกแตะ", "", (S, R[4], "CV SMOTE")),
        ("④", "❌ วิธีผิด: SMOTE ก่อน CV = สร้างจุดก่อนแบ่ง fold → leak", "", (M, R[4], [
            "Multiply", "SMOTE (WRONG, before CV)", "CV WRONG"])),
        ("⑤", "เทียบทุกวิธีด้วย CV ชุดเดียวกัน", "", (M, R[4], [
            "Multiply", "CV Baseline", "CV Tree", "CV Undersample", "CV SMOTE"])),
        ("⑤", "ข้างใน CV Undersample: Sample (balance_data) ใน Training", "", (S, R[4], "CV Undersample")),
        ("⑦", "Threshold (จาก R07): Create Threshold (thr) + Apply Threshold → Performance", "", (M, R[7], [
            "Multiply (scored test)", "Create Threshold 0.3", "Apply Threshold 0.3", "Performance (t=0.3)"]))],
    5: [("②", "เทียบไม่ normalize vs normalize ด้วย CV เดียวกัน", "", (M, R[5], [
            "Multiply", "Multiply (compare)", "CV Baseline", "CV kNN raw", "CV kNN normalized"])),
        ("②", "ข้างใน CV kNN normalized: Normalize ใน Training → Group Models", "", (S, R[5], "CV kNN normalized")),
        ("②", "Hold-out: Split → Normalize (train) → k-NN → Apply (pre) กับ test → Apply (mod) → Performance", "", (M, R[5], [
            "Multiply", "Split Data", "Normalize (hold-out)", "k-NN (hold-out)", "Apply Model (normalize test)",
            "Apply Model (kNN test)", "Performance (hold-out)"])),
        ("③", "Cross Distances: req = จุดใหม่ · ref = ข้อมูล → ระยะ + k จุดใกล้สุด", "", (M, R[5], [
            "Read CSV", "Set Role", "Multiply", "Read CSV (new point)", "Multiply (new)", "Cross Distances"])),
        ("④", "Optimize Parameters ครอบ CV + Log → Log to Data = ตาราง k vs F1", "", (S, R[5], "Optimize Parameters (k)")),
        ("④", "ข้างใน CV opt", "", (S, R[5], "CV opt")),
        ("⑤", "จุดใหม่: Normalize ด้วย pre ของ train → Apply Model (k-NN)", "", (M, R[5], [
            "Multiply", "Multiply (new)", "Normalize (final)", "k-NN (final)", "Apply Model (normalize new)",
            "Apply Model (kNN new)"])),
        ("⑥", "KNN regression: label ตัวเลข → Performance (Regression)", "", (M, R[5], [
            "Read CSV (regression)", "Set Role (regression)", "CV kNN regression"]))],
    6: [("②", "Nominal to Numerical (comparison_groups = reference) · pre ใช้ซ้ำกับข้อมูลใหม่", "", (M, R[6], [
            "Read CSV", "Set Role", "Nominal to Numerical", "Multiply"])),
        ("③", "Split Data → Multiply (train)/(test) ให้ทุกโมเดลใช้ชุดเดียวกัน", "", (M, R[6], [
            "Multiply", "Split Data", "Multiply (train)", "Multiply (test)"])),
        ("④", "Simple LR: Select Attributes (x + label) → Linear Regression → res mod = สมการ", "", (M, R[6], [
            "Multiply", "Select Attributes (simple)", "Linear Regression (simple)"])),
        ("⑤", "baseline (mean) vs Linear Regression บน train/test เดียวกัน", "", (M, R[6], [
            "Multiply (train)", "Multiply (test)", "Default Model (mean)", "Linear Regression", "Apply Model (Baseline mean)",
            "Apply Model (Linear Regression)", "Performance (Baseline mean)", "Performance (Linear Regression)"])),
        ("⑥", "เทียบ LR / kNN / Tree regression ด้วย CV", "", (M, R[6], [
            "Multiply", "Multiply (compare)", "CV LR", "CV kNN reg", "CV Tree reg"])),
        ("⑦", "ข้อมูลใหม่: dummy เดิม (pre) → Linear Regression (final)", "", (M, R[6], [
            "Nominal to Numerical", "Multiply", "Linear Regression (final)", "Read CSV (new)", "Apply Model (dummy new)",
            "Apply Model (LR new)"]))],
    7: [("①", "label 0/1 → Numerical to Binominal (false/true) → Set Role", "", (M, R[7], [
            "Read CSV", "Numerical to Binominal", "Set Role"])),
        ("②", "Declare Missing Value: 0 ใน glucose/bmi/… → ว่าง", "", (M, R[7], [
            "Set Role", "Declare Missing Value", "Multiply"])),
        ("③", "Split → Replace Missing (train) → Logistic → Apply กับ test (pre ก่อน แล้ว mod)", "", (M, R[7], [
            "Multiply", "Split Data", "Replace Missing Values", "Logistic Regression", "Apply Model (impute test)",
            "Apply Model (logistic)", "Multiply (model)", "Multiply (scored test)"])),
        ("⑤", "threshold: H2O default vs 0.5 vs 0.3", "", (M, R[7], [
            "Multiply (scored test)", "Performance (H2O default)", "Create Threshold 0.5", "Apply Threshold 0.5",
            "Performance (t=0.5)", "Create Threshold 0.3", "Apply Threshold 0.3", "Performance (t=0.3)"])),
        ("⑦", "baseline vs Logistic ใน CV", "", (M, R[7], ["Multiply", "Multiply (CV)", "CV Baseline", "CV LogReg"])),
        ("⑦", "ทำนายข้อมูลใหม่: impute ด้วยค่าเดิม → logistic", "", (M, R[7], [
            "Apply Model (impute test)", "Multiply (model)", "Read CSV (new)", "Apply Model (impute new)",
            "Apply Model (logistic new)"]))],
    8: [("①", "Weight by Information Gain / Gain Ratio / Gini → wei = ค่าของแต่ละ attribute", "", (M, R[8], [
            "Read CSV (hand)", "Set Role (hand)", "Multiply (hand)", "Weight By Information Gain",
            "Weight By Information Gain Ratio", "Weight By Gini Index"])),
        ("②", "Decision Tree บนข้อมูลทั้งหมด → res mod = Graph / Description (กฎ)", "", (M, R[8], [
            "Read CSV", "Numerical to Binominal", "Set Role", "Multiply", "Decision Tree (show)"])),
        ("③", "train acc ของต้นไม้เต็ม: train แล้ว Apply กับข้อมูลเดิม", "", (M, R[8], [
            "Multiply", "Decision Tree (full)", "Apply Model (train acc)", "Performance (train acc)"])),
        ("④", "Optimize maximal_depth: ข้างใน Optimize = CV + Log", "", (S, R[8], "Optimize Parameters (depth)")),
        ("⑤", "Random Forest → ทำนายข้อมูลใหม่", "", (M, R[8], [
            "Multiply", "Random Forest (final)", "Read CSV (new)", "Apply Model (new)"])),
        ("⑥", "เทียบ baseline / tree เต็ม / depth 3 / RF ด้วย CV เดียวกัน", "", (M, R[8], [
            "Multiply", "Multiply (compare)", "CV Baseline", "CV Tree full", "CV Tree d3", "CV Random Forest"]))],
    9: [("②", "Select Attributes ตัด id → Set Role → Multiply", "", (M, R[9], [
            "Read CSV", "Select Attributes", "Set Role", "Multiply"])),
        ("④", "ข้างใน CV kNN: Replace Missing → Nominal to Numerical → Normalize → k-NN → Group Models", "", (S, R[9], "CV kNN")),
        ("⑥", "baseline + 4 โมเดล ด้วย CV ชุดเดียวกัน (seed เดียวกัน)", "", (M, R[9], [
            "Multiply", "Multiply (default)", "CV Baseline", "CV kNN", "CV LogReg", "CV Tree", "CV RF"])),
        ("⑦", "Optimize kNN / Tree → Log to Data (ตาราง) + par (ค่าที่ดีที่สุด)", "", (M, R[9], [
            "Multiply", "Optimize Parameters (kNN)", "Log to Data (kNN)", "Optimize Parameters (Tree)", "Log to Data (Tree)"])),
        ("⑦", "ข้างใน Optimize Tree", "", (S, R[9], "Optimize Parameters (Tree)")),
        ("⑪", "โมเดลสุดท้าย (fit ทั้งชุด) → ทำนายข้อมูลใหม่", "", (M, R[9], [
            "Multiply", "Decision Tree (final)", "Read CSV (new)", "Apply Model (new)"]))],
    10: [("②", "Set Role (id) → Normalize → Multiply", "", (M, R[10], ["Read CSV", "Set Role", "Normalize", "Multiply"])),
         ("③", "เลือก k: Optimize Parameters (k) → Log to Data", "", (M, R[10], [
             "Multiply", "Optimize Parameters (k)", "Log to Data (k)"])),
         ("③", "ข้างใน Optimize: k-Means → Cluster Distance Performance → Log", "", (S, R[10], "Optimize Parameters (k)")),
         ("④", "k-Means → Cluster Distance Performance · clu = clustered set · mod = cluster model (centroid)", "", (M, R[10], [
             "Multiply", "Clustering", "Cluster Distance Performance", "Multiply (clustered)", "Multiply (cluster model)"])),
         ("⑤", "profile: Aggregate average ตาม cluster", "", (M, R[10], ["Multiply (clustered)", "Aggregate (profile)"])),
         ("⑦", "จุดใหม่: Normalize ด้วย pre เดิม → Apply cluster model", "", (M, R[10], [
             "Normalize", "Multiply (cluster model)", "Read CSV (new)", "Set Role (new)", "Apply Model (normalize new)",
             "Apply Model (cluster new)"])),
         ("⑧", "PCA 2D ของ clustered set · Hierarchical → Flatten", "", (M, R[10], [
             "Multiply (clustered)", "PCA (2D)", "Multiply", "Clustering (Agglomerative)", "Flatten Clustering"]))],
    11: [("①", "ตาราง 0/1 (A): Read Excel → Set Role id → Numerical to Binominal", "", (M, R[11], [
             "Read Excel (A)", "Set Role (A)", "Numerical to Binominal (A)"])),
         ("②", "ตารางลูกค้า (B): ตัด id/คอลัมน์ไม่ให้ข้อมูล → Discretize → Nominal to Binominal", "", (M, R[11], [
             "Read CSV (B)", "Select Attributes (B)", "Discretize by Frequency (B)", "Discretize by User Specification (B)",
             "Nominal to Binominal (B)"])),
         ("④", "FP-Growth (min support) → fre = frequent itemsets", "", (M, R[11], [
             "Numerical to Binominal (A)", "FP-Growth (A)"])),
         ("⑤", "Create Association Rules (min confidence) → rul = rules (Support · Confidence · Lift)", "", (M, R[11], [
             "FP-Growth (A)", "Create Association Rules (A)"]))],
}

LEGEND = ("> [!info]- 🖥️ วิธีอ่านภาพ RapidMiner ใต้แต่ละขั้น (สร้างจาก `{rmp}` จริง)\n"
          "> กล่อง = operator (บน: ชื่อบน canvas · ล่าง: ชนิด) · ⧉ = มี subprocess (ดับเบิลคลิกเข้าไป) · ป้ายบนเส้น = port ย่อ "
          "(exa = example set · mod = model · pre = preprocessing model · per = performance · lab = labelled data · "
          "tra = training set · tes = test set · out = output · par = partition ของ Split Data / parameter set ของ Optimize · thr = threshold · wei = weights · fre = frequent sets · rul = rules) · ◯ res = ต่อออกผลลัพธ์ · "
          "กล่องเส้นประ = port ขอบ pane · สี: 🟪 อ่านข้อมูล · 🟦 จัดการข้อมูล · 🟩 preprocessing · 🟧 โมเดล · 🟨 apply · "
          "🟥 ประเมิน/validation · ⬜ utility · มีเฉพาะ operator ของขั้นนั้น (ไฟล์จริงมี operator อื่นต่ออยู่ด้วย)")
OPEN, CLOSE = "<!-- RM-CANVAS -->", "<!-- /RM-CANVAS -->"


def block(title, desc, spec, rmp_main):
    kind, rmp, arg = spec
    code = main_view(rmp, arg) if kind == M else sub_view(rmp, arg)
    src = "" if rmp == rmp_main else f" (จาก `{rmp}`)"
    lines = [OPEN, "", f"> [!example]+ 🖥️ RapidMiner{src}: {title}"]
    if desc:
        lines.append(f"> {desc}")
    lines += ["> ```mermaid"] + [f"> {l}" for l in code.splitlines()] + ["> ```", "", CLOSE]
    return "\n".join(lines)


def insert(no):
    f = next(FLOW.glob(f"FLOW {no:02d} *.md"))
    s = f.read_text(encoding="utf-8")
    # ลบของเดิมทั้งหมด (ทั้งแบบ section ใหญ่รุ่นก่อน และกล่องใต้ขั้น)
    s = re.sub(r"\n?<!-- RM-CANVAS:START.*?<!-- RM-CANVAS:END -->\n?", "\n", s, flags=re.S)
    s = re.sub(r"\n*" + re.escape(OPEN) + r".*?" + re.escape(CLOSE), "", s, flags=re.S)  # noqa
    lines = s.split("\n")
    by_step = {}
    for step, title, desc, spec in STEPS[no]:
        by_step.setdefault(step, []).append(block(title, desc, spec, R[no]))
    out, i, cur = [], 0, None
    for line in lines:
        is_head = line.startswith("## ") or line.startswith("### ")
        if is_head and cur is not None:              # จบขั้นก่อนหน้า → วางกล่องของขั้นนั้น
            while out and out[-1] == "":
                out.pop()
            out += [""] + ["\n\n".join(by_step.pop(cur))] + [""]
            cur = None
        out.append(line)
        if line.startswith("## ทีละขั้น"):
            out += ["", OPEN, "", LEGEND.format(rmp=R[no]), "", CLOSE]
        if line.startswith("### "):
            k = next((st for st in by_step if line.startswith(f"### {st}") or f" {st} " in line[:12] or line[4:].startswith(st)), None)
            cur = k
    if cur is not None:
        out += [""] + ["\n\n".join(by_step.pop(cur))]
    missing = list(by_step)
    s = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
    f.write_text(s, encoding="utf-8")
    return f.name, len(STEPS[no]), missing


if __name__ == "__main__":
    for no in STEPS:
        name, n, missing = insert(no)
        print("✓" if not missing else "✗", name, n, "ภาพ", f"(ไม่พบขั้น {missing})" if missing else "")
