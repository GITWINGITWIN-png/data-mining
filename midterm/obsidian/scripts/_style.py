"""สไตล์กลางสำหรับภาพประกอบทุกภาพในโน้ตมิดเทอม

เหตุผลที่แยกไฟล์นี้ออกมา: ทุกภาพจะได้ใช้จานสี ขนาดฟอนต์ และ DPI ชุดเดียวกัน
เวลาเปิดใน Obsidian เรียงกันจะดูเป็นระบบเดียว ไม่ใช่ภาพมั่ว ๆ คนละสไตล์
"""
import matplotlib
matplotlib.use("Agg")          # ไม่มีจอ → ต้อง backend แบบเขียนไฟล์อย่างเดียว
import matplotlib.pyplot as plt
from matplotlib import font_manager
from pathlib import Path
import glob

# --- ฟอนต์ไทย -------------------------------------------------------------
# DejaVu Sans (ดีฟอลต์ของ matplotlib) ไม่มีอักขระไทย → ข้อความไทยจะกลายเป็นสี่เหลี่ยม
# แก้โดยลงทะเบียนฟอนต์ TLWG (มากับ Linux) แล้วตั้ง font.family เป็น "ลิสต์"
# matplotlib จะไล่หาทีละฟอนต์ต่อ 1 อักขระ (font fallback) → ไทยได้ Garuda, สูตร/สัญลักษณ์ได้ DejaVu
for _f in glob.glob("/usr/share/fonts/opentype/tlwg/Garuda*.otf"):
    font_manager.fontManager.addfont(_f)

THAI_STACK = ["Garuda", "DejaVu Sans"]

# จานสี Okabe–Ito — ปลอดภัยกับตาบอดสี (color-blind safe) และพิมพ์ขาวดำยังแยกออก
C = {
    "blue":   "#0072B2",   # ใช้กับ "ข้อมูล / ปกติ"
    "orange": "#E69F00",   # ใช้กับ "คำเตือน / ค่าที่ถูกแปลง"
    "green":  "#009E73",   # ใช้กับ "ถูกต้อง / ผลลัพธ์ดี"
    "red":    "#D55E00",   # ใช้กับ "ผิด / outlier / error"
    "purple": "#CC79A7",
    "sky":    "#56B4E9",
    "yellow": "#F0E442",
    "grey":   "#6E6E6E",
    "ink":    "#22252A",   # สีตัวอักษรหลัก
    "paper":  "#FFFFFF",
}

ASSETS = Path(__file__).resolve().parent.parent / "assets"
ASSETS.mkdir(exist_ok=True)


def apply():
    """ตั้งค่า rcParams ครั้งเดียวต่อสคริปต์"""
    plt.rcParams.update({
        "figure.dpi": 150,
        "axes.unicode_minus": False,   # Garuda ไม่มี U+2212 → ใช้ hyphen ธรรมดาแทน           # คมพอสำหรับจอ retina ใน Obsidian
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
        "savefig.facecolor": C["paper"],
        "font.size": 11,
        "font.family": THAI_STACK,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "axes.edgecolor": C["grey"],
        "axes.linewidth": 0.9,
        "axes.spines.top": False,    # เอากรอบบน/ขวาออก ให้กราฟดูโปร่ง
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linewidth": 0.7,
        "legend.frameon": False,
        "text.color": C["ink"],
        "axes.labelcolor": C["ink"],
        "xtick.color": C["ink"],
        "ytick.color": C["ink"],
    })


def save(fig, name):
    """เซฟลง assets/ แล้วพิมพ์ path เพื่อให้เห็นว่าไฟล์ไหนถูกสร้าง"""
    out = ASSETS / name
    fig.savefig(out)
    plt.close(fig)
    print(f"  ✓ {name}")
    return out
