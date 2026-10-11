"""รันโค้ด Python ทุกบล็อกในโน้ต เพื่อพิสูจน์ว่า "copy ไปใช้ในห้องสอบได้จริง"

หลักการ: บล็อก ```python ในโน้ตเดียวกันถือเป็น cell ของ notebook เดียว รันต่อกันตามลำดับ
(ตัวแปรจากบล็อกก่อนหน้าใช้ต่อได้) โดยรันจากโฟลเดอร์ `data mining/` — path ในโน้ตจึงเขียนแบบ
relative เช่น "W12/Social_Network_Ads_2.csv"

บล็อกที่ไม่ได้ตั้งใจให้รัน (template ที่มีช่องว่างให้เติม) ให้ขึ้นบรรทัดแรกด้วย `# skip-test`

ใช้:  final/.venv/bin/python final/obsidian/scripts/run_snippets.py [--show] final/obsidian/lab/*.md
"""
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FENCE = re.compile(r"^(?P<indent>[ \t>]*)```python[ \t]*\n(?P<body>.*?)^(?P=indent)```", re.S | re.M)


def blocks_of(md: Path):
    text = md.read_text(encoding="utf-8")
    for m in FENCE.finditer(text):
        indent = m.group("indent")
        body = m.group("body")
        if indent:  # บล็อกที่อยู่ใน callout (> ) ต้องตัด prefix ออกทุกบรรทัด
            body = "\n".join(line[len(indent):] if line.startswith(indent) else line.lstrip("> ")
                             for line in body.splitlines())
        line_no = text[:m.start()].count("\n") + 1
        if body.lstrip().startswith("# skip-test"):
            continue
        yield line_no, body


def run_note(md: Path, show: bool = False) -> bool:
    blocks = list(blocks_of(md))
    if not blocks:
        print(f"  –  {md.name}: ไม่มีบล็อก python")
        return True
    # ใส่ marker ก่อนแต่ละบล็อก เพื่อบอกได้ว่า error มาจากบล็อกไหน (บรรทัดที่เท่าไรในโน้ต)
    script = ["import matplotlib; matplotlib.use('Agg')",
              "import warnings; warnings.filterwarnings('error', category=FutureWarning)"]
    for line_no, body in blocks:
        script.append(f"print('@@BLOCK {line_no}', flush=True)")
        script.append(body)
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write("\n".join(script))
        tmp = f.name
    t0 = time.time()
    proc = subprocess.run([sys.executable, tmp], cwd=ROOT, capture_output=True, text=True,
                          timeout=900, env={**os.environ, "MPLBACKEND": "Agg"})
    os.unlink(tmp)
    ok = proc.returncode == 0
    last = [ln for ln in proc.stdout.splitlines() if ln.startswith("@@BLOCK")]
    where = last[-1].split()[1] if last else "?"
    status = "✓" if ok else "✗"
    print(f"  {status}  {md.name}: {len(blocks)} บล็อก ({time.time() - t0:.0f}s)"
          + ("" if ok else f" — พังที่บล็อกบรรทัด {where}"))
    if show:
        print(proc.stdout)
    if not ok:
        print("\n".join("      " + ln for ln in proc.stderr.strip().splitlines()[-12:]))
    return ok


if __name__ == "__main__":
    show = "--show" in sys.argv  # พิมพ์ output ของโค้ดด้วย (ใช้ตรวจตัวเลขที่อ้างในโน้ต)
    notes = [Path(p) for p in sys.argv[1:] if p != "--show"]
    results = [run_note(n, show) for n in notes]
    print(f"\n{sum(results)}/{len(results)} โน้ตผ่าน")
    sys.exit(0 if all(results) else 1)
