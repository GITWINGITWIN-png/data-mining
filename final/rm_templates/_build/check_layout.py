"""ตรวจ layout ของ .rmp: operator ทับกัน / ทับโน้ต (ใช้สูตรความสูงเดียวกับ RapidMiner Studio)

ProcessDrawUtils.calcHeighForOperator: h = max(68, 40 + 21 * max(#in, #out))
กล่อง = (x, y) ถึง (x+90, y+18+h) · 18 = แถบชื่อ (HEADER_HEIGHT)
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

W, HEAD = 90, 18
PORTS = {  # จำนวน port สูงสุด (in/out) โดยประมาณ · ตัวที่เป็น dynamic นับจากเส้นที่ต่อ
    "read_csv": 1, "read_excel": 1, "create_threshold": 1,
    "apply_model": 2, "set_role": 2, "select_attributes": 2, "performance_regression": 2,
    "performance_binominal_classification": 2, "performance_classification": 2, "default_model": 2,
    "log_to_data": 2, "sample": 2, "sample_stratified": 2, "generate_attributes": 2, "declare_missing_value": 2,
    "concurrency:k_means": 2, "apply_threshold": 2, "aggregate": 2, "sort": 2, "flatten_clustering": 2,
    "detect_outlier_distances": 2, "concurrency:join": 2, "blending:pivot": 2, "agglomerative_clustering": 2,
    "create_association_rules": 2, "concurrency:fp_growth": 2,
    "concurrency:cross_validation": 5, "concurrency:optimize_parameters_grid": 4,
}
DYN = {"multiply", "group_models", "append", "log", "split_data"}


def ports(op):
    cls = op.get("class")
    if cls in DYN:
        return None
    return PORTS.get(cls, 3)


def check(path):
    root = ET.parse(path).getroot()
    bad = []

    def walk(proc, where):
        ops = proc.findall("operator")
        conns = proc.findall("connect")
        rects = []
        for op in ops:
            n = ports(op)
            if n is None:
                name = op.get("name")
                outs = sum(1 for c in conns if c.get("from_op") == name)
                ins = sum(1 for c in conns if c.get("to_op") == name)
                n = max(outs, ins) + 1
            h = max(68, 40 + 21 * n)
            x, y = float(op.get("x", 0)), float(op.get("y", 0))
            rects.append((f"op '{op.get('name')}'", x, y, x + W, y + HEAD + h))
            for sub in op.findall("process"):
                walk(sub, f"{where} > {op.get('name')}")
        for d in proc.findall("description"):
            x, y, w, h = (float(d.get(k)) for k in ("x", "y", "width", "height"))
            rects.append((f"note '{re.sub('<[^>]+>', '', d.text or '')[:40]}'", x, y, x + w, y + h))
        for i, a in enumerate(rects):
            for b in rects[i + 1:]:
                if a[0].startswith("note") and b[0].startswith("note"):
                    continue
                if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    bad.append(f"{where}: {a[0]} ⟂ {b[0]}")

    walk(root.find("operator/process"), "Main")
    return bad


if __name__ == "__main__":
    total = 0
    for p in sys.argv[1:]:
        b = check(p)
        total += len(b)
        print(f"{'OK ' if not b else 'BAD'} {Path(p).name} ({len(b)})")
        for s in b:
            print("    ", s)
    sys.exit(1 if total else 0)
