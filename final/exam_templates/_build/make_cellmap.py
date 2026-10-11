"""Generate ../02_CELL_MAP.md from the built notebooks: every CONFIG variable and every ✏️ line per §.

usage: python make_cellmap.py   (run after the notebooks are rebuilt)
"""
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def esc(s):
    return s.replace("|", "\\|").strip()


def split_comment(line):
    """'NAME = value   # comment' → (code, comment) — ignores # inside quotes"""
    q = None
    for i, ch in enumerate(line):
        if ch in "\"'" and q is None:
            q = ch
        elif ch == q:
            q = None
        elif ch == "#" and q is None:
            return line[:i].rstrip(), line[i + 1:].strip()
    return line.rstrip(), ""


out = ["# 🗺️ CELL MAP: ทุกจุดที่ต้องแก้ ในทุกไฟล์",
       "",
       "> สร้างอัตโนมัติจาก notebook (`_build/make_cellmap.py`) ตรงกับโค้ดจริงเสมอ",
       "> **cell #** = ลำดับ cell นับจาก 0 (cell 0 = หัวเรื่อง · cell 1 = ⚙️ CONFIG · cell 2 = 🔧 helpers ห้ามแก้)",
       "> ทุกไฟล์: แก้ **CONFIG** ก่อนเสมอ → Run All → แล้วค่อยแก้บรรทัด ✏️ ใน § ที่โจทย์ถาม → รัน cell นั้นใหม่",
       "> วิธีใช้แบบละเอียด: [01_MANUAL.md](01_MANUAL.md) · หาไฟล์จากคำในโจทย์: [00_INDEX.md](00_INDEX.md)",
       ""]

for f in sorted(glob.glob(os.path.join(ROOT, "T*.ipynb"))):
    nb = json.load(open(f, encoding="utf-8"))
    cells = nb["cells"]
    title = "".join(cells[0]["source"]).strip().splitlines()[0].lstrip("# ").strip()
    name = os.path.basename(f)
    out += ["---", "", f"## {title}", "", f"ไฟล์ `{name}` · {len(cells)} cells", ""]

    out += ["### ⚙️ CONFIG (cell 1)", "", "| ตัวแปร | ค่าตัวอย่าง | ความหมาย / ตัวเลือก |", "|---|---|---|"]
    pending = None
    for raw in "".join(cells[1]["source"]).splitlines()[1:]:
        code, com = split_comment(raw)
        if not code.strip() and com:
            out.append(f"| | | {esc(com)} |")
            continue
        m = re.match(r"^([A-Za-z_][\w, ]*?)\s*=\s*(.+)$", code)
        if m:
            val = m.group(2)
            if len(val) > 60:
                val = val[:57] + "…"
            out.append(f"| `{esc(m.group(1))}` | `{esc(val)}` | {esc(com)} |")
        elif code.strip():          # continuation line of a multi-line value
            continue
    out.append("")

    out += ["### § ต่าง ๆ และบรรทัด ✏️ ที่แก้ได้", "", "| cell # | § | ✏️ แก้ในเซลล์ (ถ้าโจทย์ต้องการ) |", "|---|---|---|"]
    sec = None
    rows = {}
    order = []
    for i, c in enumerate(cells):
        src = "".join(c["source"])
        if i < 3:
            continue
        if c["cell_type"] == "markdown":
            h = [l for l in src.splitlines() if l.startswith("## ")]
            if h:
                sec = re.sub(r"\*\*", "", h[0][3:]).strip()
                order.append((i, sec))
                rows[sec] = []
            continue
        if sec is None:
            continue
        for l in src.splitlines():
            if "✏️" in l:
                code, com = split_comment(l.strip())
                com = com.replace("✏️", "").strip()
                txt = f"cell {i}: `{esc(code)[:70]}`" if code else f"cell {i}"
                if com:
                    txt += f" — {esc(com)}"
                rows[sec].append(txt)
    for i, s in order:
        edits = "<br>".join(rows[s]) if rows[s] else "— (ไม่ต้องแก้ ใช้ค่าจาก CONFIG)"
        out.append(f"| {i} | {esc(s)} | {edits} |")
    out.append("")

open(os.path.join(ROOT, "02_CELL_MAP.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("wrote 02_CELL_MAP.md", len(out), "lines")
