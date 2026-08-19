"""บทที่ 8 — คำถามธุรกิจเดียวกัน ตอบด้วย 3 เครื่องมือ (guideline ข้อ 7.2)

โจทย์: "ยอดขายรวมของแต่ละหมวดสินค้า" จาก Sales-Fact + Product-Dim (เคส ETL
บทที่ 7) — แสดงให้เห็นว่า SQL / RapidMiner / Python ตอบคำถามเดียวกันได้
ด้วยแนวคิดเดียวกัน (join แล้ว aggregate) เพียงแค่ไวยากรณ์ต่างกัน แล้วจบด้วย
ผลลัพธ์ตารางเดียวกันทั้ง 3 ทาง (คำนวณจากข้อมูลจริงในสไลด์ ETL)
"""
from _style import apply, save, C
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
from collections import OrderedDict

apply()

# ── ข้อมูลจริงจากตัวอย่างสไลด์ ETL (Sales-Fact ที่สร้างเสร็จแล้ว + Product-Dim) ──
product = {  # pcode -> (name, brand, category)
    "K21": ("Power_Clean", "Cleaners", "house_goods"),
    "Q33": ("Coke_Classic", "Cola", "soft_drink"),
    "Q34": ("Coke_Diet", "Cola", "soft_drink"),
    "P67": ("Sprite", "Coolers", "soft_drink"),
}
sales_fact = [   # time_k, product_k, store_k, customer_k, amount, cost
    ("T01", "Q33", "A01", "9901", 50, 25), ("T01", "K21", "B01", "9902", 60, 40),
    ("T01", "Q33", "A03", "9903", 10, 5),  ("T02", "K21", "A02", "9903", 50, 20),
    ("T02", "Q33", "A01", "9902", 100, 50), ("T02", "K21", "A03", "9901", 5, 3),
    ("T02", "K21", "B02", "9904", 20, 15), ("T04", "K21", "A02", "9901", 3, 1),
    ("T05", "P67", "A01", "9905", 4, 3),  ("T05", "K21", "A02", "9905", 10, 3),
]

report = OrderedDict()
for t, pid, s, c, amt, cst in sales_fact:
    cat = product[pid][2]
    report[cat] = report.get(cat, 0) + amt
report = OrderedDict(sorted(report.items(), key=lambda kv: -kv[1]))
print("ผลลัพธ์ที่ทั้ง 3 ทางต้องได้ตรงกัน:", dict(report))


def panel_frame(ax, title, col, face):
    ax.add_patch(FancyBboxPatch((0.01, 0.01), 0.98, 0.98,
                                boxstyle="round,pad=0.01,rounding_size=0.02",
                                facecolor=face, edgecolor=col, linewidth=2.2, zorder=1))
    ax.add_patch(FancyBboxPatch((0.01, 0.90), 0.98, 0.09,
                                boxstyle="round,pad=0,rounding_size=0.0",
                                facecolor=col, edgecolor="none", zorder=2))
    ax.text(0.5, 0.945, title, ha="center", va="center", fontsize=14,
            fontweight="bold", color="white", zorder=3)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off"); ax.grid(False)


def result_table(ax, x0, y0, w):
    """วาดตารางผลลัพธ์ย่อ (เหมือนกันทั้ง 3 แผง เพื่อยืนยันว่าตอบตรงกัน)"""
    rows = list(report.items())
    rh = 0.052
    ax.add_patch(plt.Rectangle((x0, y0 - rh), w, rh, facecolor=C["ink"],
                               edgecolor="none", zorder=4))
    ax.text(x0 + w * 0.32, y0 - rh / 2, "category", ha="center", va="center",
            fontsize=9.5, color="white", fontweight="bold", zorder=5)
    ax.text(x0 + w * 0.78, y0 - rh / 2, "SUM(amount)", ha="center", va="center",
            fontsize=9.5, color="white", fontweight="bold", zorder=5)
    for i, (cat, amt) in enumerate(rows):
        yy = y0 - rh * (i + 2)
        ax.add_patch(plt.Rectangle((x0, yy), w, rh,
                                   facecolor="#F2F4F6" if i % 2 else "white",
                                   edgecolor="#D9DEE4", linewidth=0.5, zorder=4))
        ax.text(x0 + w * 0.32, yy + rh / 2, cat, ha="center", va="center",
                fontsize=9.3, zorder=5)
        ax.text(x0 + w * 0.78, yy + rh / 2, str(amt), ha="center", va="center",
                fontsize=9.3, fontweight="bold", zorder=5)
    return y0 - rh * (len(rows) + 2)


fig = plt.figure(figsize=(19.5, 9.4))
gs = fig.add_gridspec(1, 3, wspace=0.045, left=0.012, right=0.988, top=0.90, bottom=0.10)

# ══════════════════════ แผง 1: SQL ══════════════════════
ax = fig.add_subplot(gs[0, 0])
panel_frame(ax, "① SQL", C["blue"], "#F5FAFF")
sql = (
    "SELECT   Product.category,\n"
    "         SUM(Sales.amount) AS total\n"
    "FROM     Sales\n"
    "JOIN     Product\n"
    "  ON     Sales.product_k =\n"
    "         Product.product_k\n"
    "GROUP BY Product.category\n"
    "ORDER BY total DESC;"
)
ax.text(0.07, 0.855, sql, ha="left", va="top", fontsize=11.3,
        family="DejaVu Sans Mono", linespacing=1.75, color=C["ink"])
ax.text(0.07, 0.47, "ผลลัพธ์:", fontsize=10.5, fontweight="bold", color=C["blue"])
result_table(ax, 0.07, 0.435, 0.86)
ax.text(0.5, 0.03, "แนวคิด: JOIN บน surrogate key → GROUP BY dim attribute → SUM(measure)",
        ha="center", fontsize=9.3, color=C["grey"], style="italic")

# ══════════════════════ แผง 2: RapidMiner ══════════════════════
ax = fig.add_subplot(gs[0, 1])
panel_frame(ax, "② RapidMiner", C["green"], "#F4FBF6")

ops = [("Read\nDatabase", "Sales-Fact", 0.10),
       ("Read\nDatabase", "Product-Dim", 0.10),
       ("Join", "on product_k", 0.36),
       ("Aggregate", "group=category\nSUM(amount)", 0.62)]
ys = [0.78, 0.63, 0.705, 0.705]
xs_map = {}
for (name, sub, xfrac), y in zip(ops, ys):
    w, h = 0.20, 0.115
    x = xfrac
    col_ = C["green"]
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.018",
                         facecolor="#DFF3E6", edgecolor=col_, linewidth=1.6, zorder=4)
    ax.add_patch(box)
    ax.add_patch(FancyBboxPatch((x, y + h - 0.040), w, 0.040,
                                boxstyle="round,pad=0,rounding_size=0.0",
                                facecolor=col_, edgecolor="none", zorder=5))
    ax.text(x + w / 2, y + h - 0.020, name.replace("\n", " "), ha="center", va="center",
            fontsize=8.4, fontweight="bold", color="white", zorder=6)
    ax.text(x + w / 2, y + (h - 0.040) / 2 - 0.006, sub, ha="center", va="center",
            fontsize=7.6, color=C["ink"], zorder=6, linespacing=1.4)
    ax.add_patch(Circle((x, y + h / 2), 0.008, facecolor="white", edgecolor=col_, linewidth=1.2, zorder=7))
    ax.add_patch(Circle((x + w, y + h / 2), 0.008, facecolor=col_, edgecolor=col_, linewidth=1.2, zorder=7))
    xs_map[name] = (x, y, w, h)

def rm_wire(a, b):
    xa, ya, wa, ha_ = xs_map[a]
    xb, yb, wb, hb = xs_map[b]
    ax.annotate("", xy=(xb, yb + hb / 2), xytext=(xa + wa, ya + ha_ / 2),
                arrowprops=dict(arrowstyle="-|>", color=C["grey"], lw=1.3,
                                connectionstyle="arc3,rad=0.12"))

rm_wire("Read\nDatabase", "Join")
ax.annotate("", xy=(0.36, 0.705 + 0.115 * 0.3), xytext=(0.10 + 0.20, 0.63 + 0.0575),
            arrowprops=dict(arrowstyle="-|>", color=C["grey"], lw=1.3,
                            connectionstyle="arc3,rad=-0.12"))
rm_wire("Join", "Aggregate")

ax.text(0.5, 0.545, "(ลาก operator ต่อกันบน canvas — ไม่ต้องพิมพ์โค้ด)",
        ha="center", fontsize=9.3, color=C["green"], fontweight="bold")
ax.text(0.07, 0.47, "ผลลัพธ์ (Results view):", fontsize=10.5, fontweight="bold", color=C["green"])
result_table(ax, 0.07, 0.435, 0.86)
ax.text(0.5, 0.03, "แนวคิดเดียวกับ SQL: Join operator = JOIN, Aggregate operator = GROUP BY + SUM",
        ha="center", fontsize=9.3, color=C["grey"], style="italic")

# ══════════════════════ แผง 3: Python / pandas ══════════════════════
ax = fig.add_subplot(gs[0, 2])
panel_frame(ax, "③ Python (pandas)", C["orange"], "#FFF8F0")
py = (
    "df = sales.merge(\n"
    "    product, on='product_k')\n"
    "\n"
    "report = (\n"
    "    df.groupby('category')\n"
    "      ['amount'].sum()\n"
    "      .sort_values(\n"
    "          ascending=False)\n"
    ")"
)
ax.text(0.07, 0.855, py, ha="left", va="top", fontsize=11.3,
        family="DejaVu Sans Mono", linespacing=1.75, color=C["ink"])
ax.text(0.07, 0.47, "ผลลัพธ์ (DataFrame):", fontsize=10.5, fontweight="bold", color=C["orange"])
result_table(ax, 0.07, 0.435, 0.86)
ax.text(0.5, 0.03, "แนวคิดเดียวกัน: merge() = JOIN, groupby()+sum() = GROUP BY + SUM",
        ha="center", fontsize=9.3, color=C["grey"], style="italic")

fig.suptitle('คำถามเดียวกัน "ยอดขายรวมของแต่ละหมวดสินค้า" — ตอบด้วย 3 เครื่องมือ ได้ผลลัพธ์เดียวกัน',
             fontsize=16, fontweight="bold", y=0.975)
save(fig, "reporting_three_tools.png")
