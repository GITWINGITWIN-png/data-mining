"""ตัวช่วยสร้างไฟล์ RapidMiner process (.rmp) จาก Python

ทำไมไม่เขียน XML ด้วยมือ: process หนึ่งไฟล์มี operator ซ้อนกันหลายชั้น (เช่น Normalize อยู่ใน
training pane ของ Cross Validation ที่อยู่ใน Optimize Parameters อีกที) และต้องต่อ port ให้ถูกทุกเส้น
ถ้าพิมพ์เองพลาดง่ายมาก → เขียนเป็นโค้ดแล้วให้สคริปต์สร้าง XML ให้ จะได้โครงเดียวกันทุกไฟล์

ไฟล์ที่ได้ เปิดใน AI Studio ด้วย File → Import Process… (หรือลากไฟล์ใส่หน้าต่าง Process)
พารามิเตอร์ที่ไม่ได้ระบุ RapidMiner จะเติมค่า default ให้เองตอนโหลด

ชื่อ class ตรวจกับไฟล์ OperatorsCore.xml / OperatorsConcurrency.xml / OperatorsBlending.xml
ของ AI Studio 2026.1.1 ในเครื่องแล้ว
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

VERSION = "12.1.001"


@dataclass
class Op:
    """operator หนึ่งตัวบน canvas"""
    cls: str                      # class ใน XML เช่น "k_nn", "concurrency:cross_validation"
    name: str                     # ชื่อที่แสดงบน canvas (ต้องไม่ซ้ำใน process เดียวกัน)
    params: dict = field(default_factory=dict)
    subprocesses: list["Proc"] = field(default_factory=list)   # pane ข้างใน (เช่น Training/Testing)
    x: int = 45
    y: int = 85

    def xml(self, indent: int) -> str:
        pad = " " * indent
        out = [f'{pad}<operator activated="true" class={quoteattr(self.cls)} '
               f'compatibility="{VERSION}" expanded="true" name={quoteattr(self.name)} '
               f'width="90" x="{self.x}" y="{self.y}">']
        for key, value in self.params.items():
            out.append(_param_xml(key, value, indent + 2))
        for sub in self.subprocesses:
            out.append(sub.xml(indent + 2))
        out.append(f"{pad}</operator>")
        return "\n".join(out)


def _param_xml(key, value, indent):
    """แปลงพารามิเตอร์เป็น XML

    - ค่าเดี่ยว               → <parameter key=.. value=../>
    - ("list", [(k, v), ..])  → <list key=..> (เช่น parameters ของ Optimize Parameters)
    - ("enum", [v1, v2, ..])  → <enumeration key=..> (เช่น ratio ของ Split Data)
    """
    pad = " " * indent
    if isinstance(value, tuple) and value[0] == "list":
        rows = "".join(f'\n{pad}  <parameter key={quoteattr(str(k))} value={quoteattr(str(v))}/>'
                       for k, v in value[1])
        return f"{pad}<list key={quoteattr(key)}>{rows}\n{pad}</list>"
    if isinstance(value, tuple) and value[0] == "enum":
        rows = "".join(f'\n{pad}  <parameter key={quoteattr(value[2] if len(value) > 2 else key)} '
                       f'value={quoteattr(str(v))}/>' for v in value[1])
        return f"{pad}<enumeration key={quoteattr(key)}>{rows}\n{pad}</enumeration>"
    if isinstance(value, bool):
        value = "true" if value else "false"
    return f"{pad}<parameter key={quoteattr(key)} value={quoteattr(str(value))}/>"


@dataclass
class Proc:
    """pane หนึ่งช่อง (process หลัก หรือ subprocess ข้างใน operator)"""
    ops: list[Op] = field(default_factory=list)
    conns: list[tuple] = field(default_factory=list)
    notes: list[tuple] = field(default_factory=list)   # โน้ตสีบน canvas (workflow annotation)

    def add(self, op: Op) -> Op:
        self.ops.append(op)
        return op

    def wire(self, src, src_port, dst, dst_port):
        """ต่อเส้น — ใช้ None แทน 'ขอบของ pane' (port ซ้าย = source, port ขวา = sink)"""
        self.conns.append((src, src_port, dst, dst_port))

    def note(self, text, x, y, w=420, h=80, color="yellow"):
        """โน้ตบน canvas — text เป็น HTML สั้น ๆ (ขึ้นบรรทัดใหม่ด้วย <br>) · color: yellow/orange/red/purple/green/blue/gray"""
        self.notes.append((text, x, y, w, h, color))

    def xml(self, indent: int) -> str:
        pad = " " * indent
        out = [f'{pad}<process expanded="true">']
        out += [op.xml(indent + 2) for op in self.ops]
        for src, sp, dst, dp in self.conns:
            a = f'from_op={quoteattr(src.name)} ' if src is not None else ""
            b = f'to_op={quoteattr(dst.name)} ' if dst is not None else ""
            out.append(f'{pad}  <connect {a}from_port={quoteattr(sp)} {b}to_port={quoteattr(dp)}/>')
        for text, x, y, w, h, color in self.notes:
            out.append(f'{pad}  <description align="left" color="{color}" colored="true" height="{h}" '
                       f'resized="true" width="{w}" x="{x}" y="{y}">{escape(text)}</description>')
        out.append(f"{pad}</process>")
        return "\n".join(out)


def save(main: Proc, path: Path, random_seed: int = 1992) -> Path:
    """เขียน process หลักลงไฟล์ .rmp"""
    root = Op("process", "Process", {"logverbosity": "init", "random_seed": random_seed},
              subprocesses=[main])
    xml = (f'<?xml version="1.0" encoding="UTF-8"?><process version="{VERSION}">\n'
           "  <context>\n    <input/>\n    <output/>\n    <macros/>\n  </context>\n"
           f"{root.xml(2)}\n</process>\n")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(xml, encoding="utf-8")
    return path


# ── ตัวช่วยที่ใช้บ่อย ──────────────────────────────────────────────────────

def read_csv(name: str, csv_path: str | Path, x=45, y=85, sep=",") -> Op:
    """Read CSV — ใช้ path แบบเต็ม เพื่อให้ batch runner และ GUI หาไฟล์เจอเหมือนกัน"""
    return Op("read_csv", name, {
        "csv_file": str(Path(csv_path).resolve()),
        "column_separators": sep,
        "first_row_as_names": True,
        "parse_numbers": True,
        "decimal_character": ".",
        "encoding": "UTF-8",
    }, x=x, y=y)


def write_csv(name: str, csv_path: str | Path, x=45, y=85) -> Op:
    return Op("write_csv", name, {"csv_file": str(Path(csv_path).resolve()),
                                  "column_separator": ","}, x=x, y=y)


def cross_validation(name: str, training: Proc, testing: Proc, folds=5, seed=1992,
                     x=45, y=85) -> Op:
    """Cross Validation — pane ซ้าย (Training) และ pane ขวา (Testing)

    กฎกัน data leakage: ทุกอย่างที่ "เรียนรู้จากข้อมูล" (Normalize, PCA, SMOTE, Sample)
    ต้องอยู่ใน Training pane เท่านั้น แล้วส่ง preprocessing model ไปใช้กับ test fold
    """
    return Op("concurrency:cross_validation", name, {
        "split_on_batch_attribute": False,
        "leave_one_out": False,
        "number_of_folds": folds,
        "sampling_type": "stratified sampling",
        "use_local_random_seed": True,
        "local_random_seed": seed,
        "enable_parallel_execution": True,
    }, subprocesses=[training, testing], x=x, y=y)
