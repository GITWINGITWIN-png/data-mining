"""ตัวสร้างไกด์ฝึก (Python) — รันโค้ดทุกขั้นจริง แล้วเขียน .md ที่มี "ผลที่ควรได้" จาก output จริง

แต่ละขั้น (Step) มี:  before (คำอธิบายก่อนพิมพ์) · code (โค้ดที่ให้พิมพ์) · after (อธิบายผล)
- after เป็น template: ใส่ {ชื่อตัวแปร:.3f} ได้ → ดึงค่าจริงจากตัวแปรในโค้ด → ตัวเลขในคำอธิบายตรงกับผลเสมอ
- ถ้าโค้ดวาดกราฟ ภาพจะถูกบันทึกเป็น assets/pr_<id>_<n>.png แล้วฝังในไกด์
"""
from __future__ import annotations

import contextlib
import io
import os
import string
from dataclasses import dataclass
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
VAULT = HERE.parent / "obsidian"
ASSETS = VAULT / "assets"
OUTDIR = VAULT / "practice"


@dataclass
class Step:
    title: str
    before: str
    code: str
    after: str = ""
    max_lines: int = 40          # ตัด output ยาว ๆ


class _NS(dict):
    """format_map แบบไม่พังถ้าอ้างตัวแปรไม่มี (ช่วยตอนเขียนไกด์)"""
    def __missing__(self, key):
        raise KeyError(f"ตัวแปร '{key}' ไม่มีใน namespace ของไกด์")


class _Fmt(string.Formatter):
    def get_field(self, field_name, args, kwargs):
        return eval(field_name, {}, kwargs), field_name   # ให้เขียน {res['f1'].mean():.3f} ได้


def md_table(df) -> str:
    """DataFrame → ตาราง markdown (ไม่ต้องพึ่ง tabulate)"""
    cols = list(df.columns)
    rows = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    rows += ["| " + " | ".join(str(v) for v in r) + " |" for r in df.itertuples(index=False)]
    return "\n".join(rows)


def build(gid: str, title: str, intro: str, steps: list[Step], outro: str, filename: str):
    pd.set_option("display.width", 120)
    pd.set_option("display.max_columns", 20)
    os.chdir(HERE)                                     # path ในโค้ดเป็น "data/xxx.csv"
    ns: dict = {"md_table": md_table}
    md = [intro.strip(), ""]
    for n, st in enumerate(steps, start=1):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec(compile(st.code, f"{gid}-step{n}", "exec"), ns)
        out = buf.getvalue().rstrip()
        lines = out.splitlines()
        if len(lines) > st.max_lines:
            lines = lines[: st.max_lines] + [f"... (อีก {len(lines) - st.max_lines} บรรทัด)"]
        md += [f"## ขั้นที่ {n} · {st.title}", "", st.before.strip(), "",
               "**พิมพ์ลงใน cell ใหม่ แล้วกด `Shift+Enter`:**", "", "```python", st.code.strip(), "```", ""]
        if lines:
            md += ["**ผลที่ควรได้:**", "", "```text", *lines, "```", ""]
        figs = plt.get_fignums()
        for k, num in enumerate(figs, start=1):
            name = f"pr_{gid}_{n}{'' if len(figs) == 1 else '_' + str(k)}.png"
            plt.figure(num).savefig(ASSETS / name, dpi=110, bbox_inches="tight")
            md += [f"**กราฟที่ควรได้:**", "", f"![[{name}]]", ""]
        plt.close("all")
        if st.after.strip():
            text = _Fmt().vformat(st.after.strip(), (), _NS(ns))
            md += ["> [!check] อ่านผล", *("> " + ln for ln in text.splitlines()), ""]
        md += ["---", ""]
    md.append(_Fmt().vformat(outro.strip(), (), _NS(ns)))
    OUTDIR.mkdir(parents=True, exist_ok=True)
    (OUTDIR / filename).write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"  ✓ {filename}  ({len(steps)} ขั้น)")
    return ns
