"""ตรวจลิงก์ในโน้ต Obsidian — wikilink, #heading anchor และภาพฝัง ต้องชี้ไปที่ที่มีอยู่จริง

Obsidian หาไฟล์จาก "ชื่อไฟล์" ทั้ง vault (vault = โฟลเดอร์ data mining/) จึงตรวจแบบเดียวกัน:
- [[Note]] / [[Note#Heading]] / [[Note|alias]] / [[Note\\|alias]] (escape ในตาราง)
- ![[image.png]]
- ลิงก์ markdown ไปไฟล์จริง เช่น [W13](../../../W13/x.ipynb)

ใช้:  final/.venv/bin/python final/obsidian/scripts/check_links.py
"""
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]
VAULT_NOTES = {p.stem: p for p in ROOT.rglob("*.md")
               if ".venv" not in p.parts and ".git" not in p.parts}
VAULT_FILES = {p.name for p in ROOT.rglob("*") if p.is_file() and ".venv" not in p.parts}
WIKI = re.compile(r"(!?)\[\[([^\]]+?)\]\]")
MDLINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")


def slug(text: str) -> str:
    """Obsidian เทียบ heading แบบตรงตัว (ไม่สนช่องว่างหัวท้าย) — ตัด markdown ** และ ` ออก"""
    text = re.sub(r"[*`]", "", text).strip()
    return unicodedata.normalize("NFC", text)


def headings(md: Path) -> set:
    out = set()
    in_code = False
    for line in md.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
        if not in_code and re.match(r"^#{1,6} ", line):
            out.add(slug(line.lstrip("#")))
    return out


def check(md: Path) -> list[str]:
    errors = []
    text = md.read_text(encoding="utf-8")
    text_no_code = re.sub(r"```.*?```", "", text, flags=re.S)
    text_no_code = re.sub(r"`[^`\n]+`", "", text_no_code)   # inline code ไม่ใช่ลิงก์
    for bang, target in WIKI.findall(text_no_code):
        target = target.replace("\\|", "|").split("|")[0].strip()
        if bang:
            if target not in VAULT_FILES:
                errors.append(f"ภาพไม่พบ: {target}")
            continue
        name, _, anchor = target.partition("#")
        note = VAULT_NOTES.get(name) if name else md
        if note is None:
            errors.append(f"โน้ตไม่พบ: [[{target}]]")
        elif anchor and slug(anchor) not in headings(note):
            errors.append(f"heading ไม่พบ: [[{target}]]")
    for href in MDLINK.findall(text_no_code):
        if href.startswith(("http://", "https://", "#", "mailto:")):
            continue
        path = (md.parent / unquote(href.split("#")[0])).resolve()
        if not path.exists():
            errors.append(f"ไฟล์ไม่พบ: {href}")
    return errors


if __name__ == "__main__":
    targets = sorted((ROOT / "final" / "obsidian").rglob("*.md"))
    total = 0
    for md in targets:
        errs = check(md)
        total += len(errs)
        mark = "✓" if not errs else "✗"
        print(f"  {mark} {md.relative_to(ROOT)}" + (f" — {len(errs)} ปัญหา" if errs else ""))
        for e in errs:
            print(f"      {e}")
    print(f"\nรวม {total} ลิงก์เสีย ใน {len(targets)} โน้ต")
    sys.exit(1 if total else 0)
