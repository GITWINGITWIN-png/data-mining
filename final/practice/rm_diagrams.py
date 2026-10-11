"""วาดภาพ canvas ของ RapidMiner (mermaid) หลังแต่ละขั้นของไกด์ — ดึงจาก process เฉลยที่รันจริง

ไม่ได้วาดมือ: อ่าน operator + เส้นเชื่อม (connect) จาก rm/P0X_solution.rmp แล้วกรองให้เหลือ
เฉพาะ operator ที่ "ควรมีบน canvas แล้ว" ณ ขั้นนั้น (กำหนดใน STEPS ด้วย pattern แบบ fnmatch)

- operator ที่เพิ่มในขั้นนั้น = สีเหลือง
- เส้นประไป res = port ที่ยังไม่มีปลายทาง (ต่อไป res ชั่วคราวเพื่อดูผลตามไกด์)
- Write CSV / Write as Text / Performance to Data มีไว้ให้ batch runner บันทึกผลเท่านั้น
  → ไม่วาด แต่เปลี่ยนเป็นเส้นไป res (ในโปรแกรมคุณต่อไป res ตรง ๆ)
- operator ที่มี subprocess (Cross Validation, Optimize Parameters) วาดข้างในแยกอีกภาพ
"""
from fnmatch import fnmatch
from pathlib import Path
import re
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent

HIDDEN = {"write_csv", "write_as_text", "performance_to_data"}

# ชื่อ operator ตามที่เห็นในแผง Operators (ใช้เป็นบรรทัดที่ 2 ของกล่อง ถ้าชื่อกล่องต่างจากนี้)
TYPE = {
    "read_csv": "Read CSV", "append": "Append", "concurrency:join": "Join",
    "generate_attributes": "Generate Attributes", "multiply": "Multiply",
    "filter_examples": "Filter Examples", "aggregate": "Aggregate", "blending:pivot": "Pivot",
    "set_role": "Set Role", "select_attributes": "Select Attributes", "normalize": "Normalize",
    "principal_component_analysis": "Principal Component Analysis",
    "discretize_by_frequency": "Discretize by Frequency",
    "concurrency:cross_validation": "Cross Validation",
    "replace_missing_values": "Replace Missing Values", "nominal_to_numerical": "Nominal to Numerical",
    "k_nn": "k-NN", "group_models": "Group Models", "apply_model": "Apply Model",
    "performance_classification": "Performance (Classification)",
    "performance_binominal_classification": "Performance (Binominal Classification)",
    "performance_regression": "Performance (Regression)", "default_model": "Default Model",
    "concurrency:parallel_decision_tree": "Decision Tree", "sample": "Sample",
    "operator_toolbox:smote": "SMOTE Upsampling",
    "concurrency:optimize_parameters_grid": "Optimize Parameters (Grid)", "log": "Log",
    "log_to_data": "Log to Data", "numerical_to_binominal": "Numerical to Binominal",
    "declare_missing_value": "Declare Missing Value", "split_data": "Split Data",
    "h2o:logistic_regression": "Logistic Regression", "create_threshold": "Create Threshold",
    "apply_threshold": "Apply Threshold", "concurrency:parallel_random_forest": "Random Forest",
    "linear_regression": "Linear Regression", "concurrency:k_means": "k-Means",
    "cluster_distance_performance": "Cluster Distance Performance",
    "concurrency:fp_growth": "FP-Growth", "create_association_rules": "Create Association Rules",
}
PANES = {"concurrency:cross_validation": ["Training", "Testing"]}

# ชื่อกล่องที่ไกด์ใช้ (ถ้าไม่ระบุ: ตัด "(p3_xxx)" ท้ายชื่อ · "CV p3_xxx" → "CV xxx")
LABELS = {
    2: {"CV p2_knn": "Cross Validation"},
    3: {"CV p3_rus": "CV RUS", "CV p3_smote": "CV SMOTE"},
    4: {"CV p4_knn_raw": "CV raw", "CV p4_knn_norm": "CV normalized",
        "CV p4_opt": "CV normalized (copy)"},
    5: {"Apply Model (impute test)": "Apply Model 1 (เติม test)",
        "Apply Model (logistic)": "Apply Model 2",
        "Performance (p5_default)": "Performance (threshold อัตโนมัติ)",
        "Performance (p5_t050)": "Performance (0.5)", "Performance (p5_t030)": "Performance (0.3)"},
    6: {"CV p6_tree_full": "CV tree full", "CV p6_tree_d3": "CV tree depth 3",
        "CV p6_rf": "CV Random Forest", "CV p6_opt": "CV tree (copy)"},
    7: {"CV p7_opt": "Cross Validation", "Apply Model (normalize test)": "Apply Model 1 (normalize test)",
        "Apply Model (knn)": "Apply Model 2"},
}

# STEPS[guide][step] = (pattern ของ operator ที่เพิ่มในขั้นนี้, subprocess ที่จะวาดข้างใน หรือ None = อัตโนมัติ)
STEPS = {
    1: {1: (["Read *"], None), 2: (["Append"], None), 3: (["Join"], None),
        4: (["Generate Attributes"], None), 5: (["Multiply"], None),
        6: (["Filter Examples", "*(p1_filter)"], None), 7: (["Aggregate", "*(p1_aggregate)"], None),
        8: (["Pivot", "*(p1_pivot)"], None), 9: (["*(p1_all)"], None)},
    2: {1: (["Read CSV"], None), 2: (["Filter Examples"], None), 3: (["Set Role", "Multiply"], None),
        4: (["Discretize by Frequency", "Aggregate", "*(p2_mass_bins)"], None),
        5: (["Select Attributes", "Normalize", "PCA", "*(p2_pca_*)"], None),
        6: (["CV p2_knn", "*(p2_knn)"], None)},
    3: {1: (["Read CSV", "Set Role", "Multiply"], None),
        2: (["CV p3_*", "Apply Model (*)", "Performance (*)", "Performance to Data (*)"], ["CV p3_baseline"]),
        3: (["Default Model*", "Decision Tree*", "Sample*", "SMOTE*"], None)},
    4: {1: (["Read CSV", "Set Role", "Multiply"], None),
        2: (["CV p4_baseline", "CV p4_knn_*", "*(p4_baseline)", "*(p4_knn_*)"], None),
        3: (["Optimize*", "CV p4_opt", "*(p4_opt)", "Log", "Log to Data*", "*(p4_opt_log)"], None)},
    5: {1: (["Read CSV", "Numerical to Binominal", "Set Role"], None), 2: (["Declare Missing Value"], None),
        3: (["Split Data"], None),
        4: (["Replace Missing Values", "Logistic Regression", "Apply Model (*)", "*(p5_model)"], None),
        5: (["Multiply", "*(p5_default)", "* 0.5", "*(p5_t050)", "* 0.3", "*(p5_t030)"], None)},
    6: {1: (["Read CSV", "Numerical to Binominal", "Set Role", "Multiply"], None),
        2: (["*(train acc)", "*(p6_train_full)"], None),
        3: (["CV p6_tree_*", "CV p6_rf", "*(p6_tree_*)", "*(p6_rf)"], None),
        4: (["Optimize*", "CV p6_opt", "*(p6_opt)", "Log", "Log to Data*", "*(p6_opt_log)"], None)},
    7: {1: (["Read CSV", "Set Role", "Nominal to Numerical"], None),
        2: (["Split Data", "Multiply (*)"], None),
        3: (["*(p7_baseline)", "*(p7_linreg)", "*(p7_linreg_model)"], None),
        4: (["Normalize", "k-NN (p7)", "Apply Model (normalize test)", "Apply Model (knn)", "*(p7_knn)"], None),
        5: (["Optimize*", "CV p7_opt", "*(p7_opt)", "Log", "Log to Data*", "*(p7_opt_log)"], None)},
    8: {1: (["Read CSV", "Set Role", "Normalize", "Multiply"], None),
        2: (["Optimize*", "*(opt)", "Log", "Log to Data", "*(p8_elbow)"], None),
        3: (["Clustering", "Cluster Distance Performance", "*(p8_k3_perf)", "*(p8_centroids)"], None),
        4: (["Aggregate", "*(p8_crosstab)"], None)},
    9: {1: (["Read CSV", "Set Role", "Numerical to Binominal"], None), 2: (["FP-Growth"], None),
        3: (["Create Association Rules", "*(p9_*)"], None)},
}


# เส้นประไป res: ปกติ = operator ใหม่ทุกตัวที่ยังไม่มีปลายทาง · ระบุเองเมื่อไกด์ให้ต่อแค่บางตัว
PEEK = {(1, 1): {"Read week1"}}

# ─────────────────────────────────────────── อ่าน .rmp ───────────────────────────────────────────
class Proc:
    """หนึ่ง canvas (process หลัก หรือ pane หนึ่งของ subprocess)"""
    def __init__(self, el, owner=None, pane=None):
        self.owner, self.pane = owner, pane
        self.ops = {}       # name → (class, [Proc, ...])
        for op in el.findall("operator"):
            self.ops[op.get("name")] = (op.get("class"),
                                        [Proc(p, op.get("name"), i) for i, p in enumerate(op.findall("process"))])
        # from_op=None = port บนขอบซ้ายของ canvas นี้ · to_op=None = ขอบขวา (หรือ res ถ้าเป็น process หลัก)
        self.edges = [(c.get("from_op"), c.get("from_port"), c.get("to_op"), c.get("to_port"))
                      for c in el.findall("connect")]

    def all_names(self):
        for name, (_, subs) in self.ops.items():
            yield name
            for s in subs:
                yield from s.all_names()

    def find(self, name):
        """หา subprocess panes ของ operator ชื่อ name (ค้นทุกชั้น)"""
        for n, (_, subs) in self.ops.items():
            if n == name:
                return subs
            for s in subs:
                r = s.find(name)
                if r is not None:
                    return r
        return None

    def cls(self, name):
        for n, (c, subs) in self.ops.items():
            if n == name:
                return c
            for s in subs:
                r = s.cls(name)
                if r:
                    return r
        return None


def load(no):
    root = ET.parse(HERE / "rm" / f"P{no:02d}_solution.rmp").getroot()
    return Proc(root.find("operator/process"))


def short(port):
    """ชื่อ port แบบที่เห็นบน canvas: 3 ตัวแรก + เลขท้าย ('example set output' → 'exa', 'output 2' → 'out 2')"""
    if port in ("exa", "ups"):
        return port
    m = re.search(r"\s(\d+)$", port)
    return port[:3].lower() + (f" {m.group(1)}" if m else "")


def label(no, name, cls):
    lab = LABELS.get(no, {}).get(name)
    if lab is None:
        lab = re.sub(r"\s*\(p\d[^)]*\)$", "", name)
        lab = re.sub(r"^CV p\d_", "CV ", lab)
    typ = TYPE.get(cls, cls)
    if typ.startswith(lab):      # "Performance" → "Performance (Classification)"
        return typ
    if lab.startswith(typ):
        return lab
    return f"{lab}<br/><i>{typ}</i>"


# ─────────────────────────────────────────── วาด ─────────────────────────────────────────────────
CLASSDEF = ["classDef new fill:#ffe08a,stroke:#b8860b,color:#000",
            "classDef op fill:#eef3fb,stroke:#5b7db1,color:#000",
            "classDef sub fill:#e3ecf9,stroke:#2f5597,stroke-width:2px,color:#000",
            "classDef port fill:#f2f2f2,stroke:#888,color:#333"]


def draw_canvas(no, proc, visible, new, top=True, peek=None):
    """process หลัก หรือ subprocess (ทุก pane) → บรรทัด mermaid"""
    panes = [proc] if top else proc
    lines = ["flowchart LR"]
    ids, n = {}, [0]

    def nid(key):
        if key not in ids:
            n[0] += 1
            ids[key] = f"n{n[0]}"
        return ids[key]

    for pi, p in enumerate(panes):
        if not top:
            title = (PANES.get(proc_cls(no, p.owner)) or ["ข้างใน"])[pi]
            lines.append(f'  subgraph P{pi}["{title}"]')
            lines.append("    direction LR")
        ind = "  " if top else "    "
        # หา edge ที่วาดได้: ข้าม operator ที่ซ่อน (Write CSV ฯลฯ) → ปลายทาง = res
        out, has_out = [], set()
        for fo, fp, to, tp in p.edges:
            if fo is not None and fo not in visible:
                continue
            if fo is not None and p.ops[fo][0] in HIDDEN:
                continue          # ต่อจาก operator ที่ซ่อน (ปลายทางจัดการตอนเส้นที่เข้าไปแล้ว)
            if to is not None and p.ops[to][0] in HIDDEN:
                if to not in visible:
                    continue
                to, tp = None, "result"
            elif to is not None and to not in visible:
                continue
            out.append((fo, fp, to, tp))
            if fo is not None:
                has_out.add(fo)
        # กล่อง operator
        for name, (c, subs) in p.ops.items():
            if name not in visible or c in HIDDEN:
                continue
            shape = ('[["', '"]]') if subs else ('["', '"]')
            cl = "new" if name in new else ("sub" if subs else "op")
            mark = " ▣" if subs else ""
            lines.append(f'{ind}{nid((pi, name))}{shape[0]}{label(no, name, c)}{mark}{shape[1]}:::{cl}')
        # เส้น
        for fo, fp, to, tp in out:
            if fo is None:   # port ขอบซ้ายของ pane
                src = nid((pi, "in", fp))
                lines.append(f'{ind}{src}(["{short(fp)}"]):::port')
                if to is not None:
                    lines.append(f'{ind}{src} -->|"{short(tp)}"| {nid((pi, to))}')
                    continue
            else:
                src = nid((pi, fo))
            if to is None:
                if top:
                    dst = "res"
                    lines.append(f'{ind}{src} -->|"{short(fp)}"| res(("res"))')
                    continue
                dst = nid((pi, "out", tp))
                lines.append(f'{ind}{dst}(["{short(tp)}"]):::port')
                lines.append(f'{ind}{src} -->|"{short(fp)}"| {dst}')
                continue
            lines.append(f'{ind}{src} -->|"{short(fp)} → {short(tp)}"| {nid((pi, to))}')
        # เส้นประไป res: operator ใหม่ที่ยังไม่มีปลายทาง (ใน process หลักเท่านั้น)
        if top:
            for name, (c, subs) in p.ops.items():
                if name in (peek or new) and name in visible and c not in HIDDEN and name not in has_out:
                    port = next((fp for fo, fp, to, tp in p.edges if fo == name), None)
                    if port:
                        lines.append(f'{ind}{nid((pi, name))} -.->|"{short(port)}"| res(("res"))')
        if not top:
            lines.append("  end")
    # Cross Validation: โมเดลจาก Training ส่งข้ามไป Testing
    if not top and len(panes) == 2:
        a, b = ids.get((0, "out", "model")), ids.get((1, "in", "model"))
        if a and b:
            lines.append(f'  {a} -.->|"ส่งโมเดลไป test fold"| {b}')
    lines += ["  " + c for c in CLASSDEF]
    return lines


_PROCS = {}


def proc_cls(no, name):
    return _PROCS[no].cls(name)


def step_blocks(no, step):
    """คืน markdown (callout + mermaid) ของขั้น step หรือ '' ถ้าไม่มี"""
    if no not in STEPS or step not in STEPS[no]:
        return ""
    proc = _PROCS.setdefault(no, load(no))
    names = list(proc.all_names())

    def match(pats):
        return {n for n in names if any(fnmatch(n, p) for p in pats)}

    visible = set()
    for s in sorted(STEPS[no]):
        if s > step:
            break
        visible |= match(STEPS[no][s][0])
    pats, inner = STEPS[no][step]
    new = match(pats)

    blocks = []
    top_new = {n for n in new if n in proc.ops and proc.ops[n][0] not in HIDDEN}
    if top_new or any(n in proc.ops for n in new):
        blocks.append(("Process หลัก", draw_canvas(no, proc, visible, new, peek=PEEK.get((no, step)))))
    # subprocess ที่จะวาดข้างใน
    if inner is None:
        inner = []
        for n in names:
            subs = proc.find(n)
            if subs and n in visible and any(m in new for s in subs for m in s.ops):
                inner.append(n)
    for n in inner:
        subs = proc.find(n)
        lab = label(no, n, proc.cls(n)).replace("<br/>", " · ").replace("<i>", "").replace("</i>", "")
        blocks.append((f"ข้างใน {lab} (ดับเบิลคลิก)", draw_canvas(no, subs, visible, new, top=False)))

    if not blocks:
        return ""
    out = ["> [!example]+ 🔌 Canvas หลังขั้นนี้ (จาก process เฉลยที่รันจริง)",
           "> 🟨 = เพิ่มในขั้นนี้ · ▣ = มี subprocess · ป้ายบนเส้น = port ต้นทาง → ปลายทาง · เส้นประไป **res** = ต่อชั่วคราวเพื่อดูผล"]
    for title, lines in blocks:
        out += [">", f"> **{title}**", "> ```mermaid"] + [f"> {l}" for l in lines] + ["> ```"]
    return "\n".join(out)


def inject(no, text):
    """ใส่ภาพลงท้าย (หรือก่อน 'ผลที่ควรเห็น') ของทุกส่วน '## ขั้นที่ N'"""
    parts = re.split(r"(?m)^(?=## )", text)
    for i, part in enumerate(parts):
        m = re.match(r"## ขั้นที่ (\d+)", part)
        if not m:
            continue
        block = step_blocks(no, int(m.group(1)))
        if not block:
            continue
        body, sep, rest = part.partition("\n---\n")
        lines = body.rstrip("\n").split("\n")
        pos = next((k for k, l in enumerate(lines) if l.startswith("**ผลที่ควรเห็น")), None)
        if pos is None:   # ไม่มี: ใส่ท้ายส่วน แต่ก่อน callout ท้าย (> [!warning] ...)
            pos = len(lines)
            while pos > 0 and (lines[pos - 1].startswith(">") or lines[pos - 1] == ""):
                pos -= 1
        lines[pos:pos] = ["", block, ""]
        parts[i] = "\n".join(lines).replace("\n\n\n", "\n\n") + "\n" + sep + rest
    return "".join(parts)


if __name__ == "__main__":   # ทดสอบ: พิมพ์ภาพทุกขั้นของไกด์ที่ระบุ
    import sys
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    for s in STEPS[g]:
        print(f"===== P{g} step {s}\n{step_blocks(g, s)}\n")
