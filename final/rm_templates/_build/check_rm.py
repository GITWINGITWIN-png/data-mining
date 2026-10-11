"""ตรวจ .rmp แบบ static (ไม่ต้องมี RapidMiner) — ใช้ตอนที่รัน batch ไม่ได้

ตรวจ:
 1. XML อ่านได้ · ชื่อ operator ไม่ซ้ำทั้ง process
 2. operator class มีอยู่จริง: อยู่ใน OperatorsCore.xml ของ RapidMiner Studio source หรือเคยใช้ใน process ที่รันผ่านแล้ว
 3. parameter key มีอยู่จริง: เป็นค่า PARAMETER_* ใน source หรือเคยใช้กับ class เดียวกันใน process ที่รันผ่าน
 4. port ที่ต่อ: เคยใช้กับ class เดียวกันใน process ที่รันผ่าน หรือมี createPort("…") ใน source ของ class นั้น/แม่ของมัน
 5. output port ต่อออกได้เส้นเดียว · input port รับได้เส้นเดียว · port บังคับต่อครบ
 6. Log / Optimize Parameters อ้างชื่อ operator ที่มีอยู่จริง

ใช้:  python check_rm.py <rapidminer-studio source dir> file1.rmp …
      (source: git clone --depth 1 https://github.com/rapidminer/rapidminer-studio)
"""
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

SRC = Path(sys.argv[1])
FILES = [Path(f) for f in sys.argv[2:]]
REPO = Path(__file__).resolve().parents[2]
VALIDATED = list((REPO / "practice" / "rm").glob("*.rmp")) + list((REPO / "mock_lab" / "recipes").glob("*.rmp")) + \
    list((REPO / "mock_lab").glob("mock*/solution*.rmp"))

JAVA = SRC / "src" / "main" / "java"
core_xml = (SRC / "src/main/resources/com/rapidminer/resources/OperatorsCore.xml").read_text()
CORE = dict(re.findall(r"<key>([^<]+)</key>\s*<class>\s*([^<\s]+)\s*</class>", core_xml))
PARAM_LITERALS = set()
for f in JAVA.rglob("*.java"):
    PARAM_LITERALS.update(re.findall(r'PARAMETER_[A-Z0-9_]*\s*=\s*"([^"]+)"', f.read_text(errors="ignore")))

norm_port = lambda p: re.sub(r"\s\d+$", "", p)  # noqa: E731


def strip(cls):
    return cls


def walk_ops(proc_el, unit_ops):
    """yield (operator element, parent <process> element)"""
    for op in proc_el.findall("operator"):
        unit_ops.append((op, proc_el))
        for sub in op.findall("process"):
            walk_ops(sub, unit_ops)


# ── ความรู้จาก process ที่รันผ่านแล้ว ──
seen_params, seen_ports = defaultdict(set), defaultdict(set)
for f in VALIDATED:
    root = ET.parse(f).getroot()
    ops = []
    walk_ops(root, ops)
    for op, parent in ops:
        for p in op.findall("parameter") + op.findall("list") + op.findall("enumeration"):
            seen_params[op.get("class")].add(p.get("key"))
    allproc = [root.find("operator")] + [o for o, _ in ops]
    for op, _ in [(root.find("operator"), None)] + ops:
        for sub in op.findall("process"):
            names = {o.get("name"): o.get("class") for o in sub.findall("operator")}
            for c in sub.findall("connect"):
                if c.get("from_op"):
                    seen_ports[names[c.get("from_op")]].add(("out", norm_port(c.get("from_port"))))
                if c.get("to_op"):
                    seen_ports[names[c.get("to_op")]].add(("in", norm_port(c.get("to_port"))))


def java_ports(cls_key):
    """createPort("…") ของ class + superclass (เฉพาะ core)"""
    out = set()
    fq = CORE.get(cls_key)
    seen = set()
    while fq and fq not in seen:
        seen.add(fq)
        f = JAVA / (fq.replace(".", "/") + ".java")
        if not f.exists():
            break
        txt = f.read_text(errors="ignore")
        out.update(re.findall(r'createPort\("([^"]+)"', txt))
        for const in re.findall(r'createPort\(([A-Z_]+)', txt):
            m = re.search(const + r'\s*=\s*"([^"]+)"', txt)
            if m:
                out.add(m.group(1))
        m = re.search(r"class\s+\w+(?:<[^>]*>)?\s+extends\s+([\w.]+)", txt)
        if not m:
            break
        sup = m.group(1).split("<")[0]
        imp = re.search(r"import\s+([\w.]+\." + sup + r");", txt)
        fq = imp.group(1) if imp else fq.rsplit(".", 1)[0] + "." + sup
        # constants defined in superclass files
        sf = JAVA / (fq.replace(".", "/") + ".java")
        if sf.exists():
            st = sf.read_text(errors="ignore")
            for const in re.findall(r'createPort\(([A-Z_]+)', st):
                mm = re.search(const + r'\s*=\s*"([^"]+)"', st)
                if mm:
                    out.add(mm.group(1))
    return out


REQUIRED_IN = {
    "apply_model": {"model", "unlabelled data"}, "concurrency:cross_validation": {"example set"},
    "k_nn": {"training set"}, "linear_regression": {"training set"}, "h2o:logistic_regression": {"training set"},
    "concurrency:parallel_decision_tree": {"training set"}, "concurrency:parallel_random_forest": {"training set"},
    "default_model": {"training set"}, "performance_binominal_classification": {"labelled data"},
    "performance_classification": {"labelled data"}, "performance_regression": {"labelled data"},
    "concurrency:join": {"left", "right"}, "append": {"example set"}, "flatten_clustering": {"hierarchical", "example set"},
    "cross_distances": {"request set", "reference set"}, "apply_threshold": {"example set", "threshold"},
    "select_by_weights": {"example set input", "weights"}, "cluster_distance_performance": {"example set", "cluster model"},
    "concurrency:fp_growth": {"example set"}, "create_association_rules": {"item sets"}, "multiply": {"input"},
    "concurrency:k_means": {"example set"}, "agglomerative_clustering": {"example set"},
}

bad = 0
for f in FILES:
    errs = []
    root = ET.parse(f).getroot()
    ops = []
    walk_ops(root, ops)
    names = Counter(o.get("name") for o, _ in ops)
    errs += [f"ชื่อซ้ำ: {n}" for n, c in names.items() if c > 1]
    allnames = set(names)
    for op, parent in ops:
        cls = op.get("class")
        if cls not in CORE and cls not in seen_params:
            errs.append(f"{op.get('name')}: class {cls} ไม่รู้จัก")
        for p in op.findall("parameter") + op.findall("list") + op.findall("enumeration"):
            k = p.get("key")
            if k not in PARAM_LITERALS and k not in seen_params.get(cls, ()):
                errs.append(f"{op.get('name')} ({cls}): parameter '{k}' ไม่พบใน source / process ที่รันผ่าน")
        # Log / Optimize references
        for p in op.iter("parameter"):
            v = p.get("value") or ""
            for ref in re.findall(r"operator\.([^.]+)\.(?:parameter|value)\.", v):
                if ref not in allnames:
                    errs.append(f"{op.get('name')}: อ้าง operator '{ref}' ที่ไม่มี")
        if cls == "concurrency:optimize_parameters_grid":
            for p in op.find("list[@key='parameters']"):
                if p.get("key").rsplit(".", 1)[0] not in allnames:
                    errs.append(f"{op.get('name')}: optimize อ้าง '{p.get('key')}' ไม่มี operator นี้")
    # connections per execution unit
    units = [o for o, _ in ops]
    for u in units:
        for sub in u.findall("process"):
            local = {o.get("name"): o.get("class") for o in sub.findall("operator")}
            outs, ins = Counter(), Counter()
            connected_in = defaultdict(set)
            for c in sub.findall("connect"):
                fo, fp, to, tp = c.get("from_op"), c.get("from_port"), c.get("to_op"), c.get("to_port")
                if fo and fo not in local:
                    errs.append(f"connect จาก '{fo}' ไม่มีใน pane นี้")
                    continue
                if to and to not in local:
                    errs.append(f"connect ไป '{to}' ไม่มีใน pane นี้")
                    continue
                outs[(fo, fp)] += 1
                ins[(to, tp)] += 1
                for side, op_name, port in (("out", fo, fp), ("in", to, tp)):
                    if not op_name:
                        continue
                    cls = local[op_name]
                    if side == "in":
                        connected_in[op_name].add(norm_port(port))
                    okp = (side, norm_port(port)) in seen_ports.get(cls, set()) or norm_port(port) in java_ports(cls) \
                        or port in java_ports(cls)
                    if not okp:
                        errs.append(f"{op_name} ({cls}): port '{port}' ({side}) ไม่พบ")
            errs += [f"output port ต่อซ้ำ: {k}" for k, v in outs.items() if v > 1]
            errs += [f"input port ต่อซ้ำ: {k}" for k, v in ins.items() if v > 1]
            for name, cls in local.items():
                need = REQUIRED_IN.get(cls, set())
                have = connected_in.get(name, set())
                miss = {n for n in need if n not in have and not any(h.startswith(n) for h in have)}
                if miss:
                    errs.append(f"{name} ({cls}): ยังไม่ได้ต่อ input {sorted(miss)}")
    print(("✗ " if errs else "✓ ") + f.name + (f"  ({len(ops)} operators)" if not errs else ""))
    for e in errs:
        print("    ", e)
    bad += bool(errs)
print("validated reference processes:", len(VALIDATED))
sys.exit(1 if bad else 0)
