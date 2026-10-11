"""สร้าง ../02_OPERATOR_MAP.md จากไฟล์ .rmp: โน้ตบน canvas (§) + operator ทุกตัวพร้อม parameter หลักที่ตั้งไว้"""
import html
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"compatibility", "expanded", "logverbosity", "random_seed", "first_row_as_names", "parse_numbers",
        "decimal_character", "encoding", "column_separators", "split_on_batch_attribute", "leave_one_out",
        "use_local_random_seed", "local_random_seed", "enable_parallel_execution", "persistent", "sorting_type",
        "accuracy", "precision", "recall", "f_measure", "kappa", "AUC", "root_mean_squared_error", "absolute_error",
        "squared_error", "squared_correlation", "error_handling", "add_intercept", "solver", "reproducible",
        "compute_p-values", "remove_collinear_columns", "standardize", "use_regularization"}


def txt(s):
    s = re.sub(r"<br>", " · ", s or "")
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).replace("|", "\\|").strip()


def params(op):
    out = []
    for p in op:
        k = p.get("key")
        if k in SKIP or p.tag not in ("parameter", "list", "enumeration"):
            continue
        if p.tag == "parameter":
            v = p.get("value")
            if k == "csv_file" or k == "excel_file":
                v = "…/" + v.split("/")[-1]
            out.append(f"`{k}`={v}")
        else:
            vals = ", ".join(f"{c.get('key')}:{c.get('value')}" if p.tag == "list" else c.get("value") for c in p)
            out.append(f"`{k}`=[{vals}]")
    return " · ".join(out).replace("|", "\\|")


lines = ["# 🗺️ OPERATOR MAP: ทุก operator / parameter ในทุกไฟล์ R01–R11", "",
         "> สร้างอัตโนมัติจากไฟล์ .rmp (`_build/make_opmap.py`) ตรงกับไฟล์จริงเสมอ",
         "> วิธีใช้: [01_MANUAL.md](01_MANUAL.md) · หาไฟล์จากคำในโจทย์: [00_INDEX.md](00_INDEX.md)",
         "> แถว **in CV** = operator ที่อยู่ข้างใน Cross Validation / Optimize (ดับเบิลคลิกเพื่อเข้าไปแก้)", ""]
for f in sorted(ROOT.glob("R*.rmp")):
    root = ET.parse(f).getroot()
    main = root.find("operator/process")
    lines += ["---", "", f"## {f.stem}", ""]
    notes = main.findall("description")
    lines += ["**โน้ตบน canvas:**", ""]
    for d in notes:
        lines.append(f"- {txt(d.text)}")
    lines += ["", "| operator | class | parameter ที่ตั้งไว้ (แก้ตามโจทย์) |", "|---|---|---|"]

    def walk(proc, depth):
        for op in proc.findall("operator"):
            name = ("↳ " * depth) + op.get("name")
            lines.append(f"| {name.replace('|', '/')} | `{op.get('class')}` | {params(op)} |")
            for sub in op.findall("process"):
                walk(sub, depth + 1)
    walk(main, 0)
    lines.append("")
(ROOT / "02_OPERATOR_MAP.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("wrote 02_OPERATOR_MAP.md", len(lines), "lines")
