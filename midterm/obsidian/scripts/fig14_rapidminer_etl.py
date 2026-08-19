"""บทที่ 7 — จำลอง RapidMiner Process Canvas สำหรับ ETL เคส AllElectronics

จุดประสงค์: guideline ข้อ 6.3 บอกว่าต้องทำ "Practical implementation using
RapidMiner" แต่สไลด์แทบไม่มีภาพประกอบ (แค่ชื่ออยู่ในลิสต์เครื่องมือ) ภาพนี้จึง
จำลอง "หน้าตาจริง" ของ operator บน canvas ให้ตรงกับ SQL script ที่มีอยู่แล้วใน
07 ETL.md §7.6 — จัดเป็นกริดคอลัมน์คงที่ (Read ชิดซ้าย, Write ชิดขวาเสมอ)
เพื่อไม่ให้กล่อง/เส้นชนกัน ไม่ว่าแถวนั้นจะมี operator กี่ตัว
"""
from _style import apply, save, C
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

apply()

COL_E, FACE_E = C["blue"],   "#DCEBF7"
COL_T, FACE_T = C["green"],  "#E4F3E9"
COL_L, FACE_L = C["orange"], "#FDE9D9"

BOX_W, BOX_H = 3.35, 1.85
GAP_X, GAP_Y = 0.55, 0.85
HEAD_H = 0.62                     # สูงพอสำหรับหัวข้อ 2 บรรทัดเสมอ ไม่ต้องคิดเคสพิเศษ

# ตำแหน่งคอลัมน์คงที่ทั้งภาพ — Read เสมอที่ x=X[0], Write เสมอที่ x=X[4]
X = [i * (BOX_W + GAP_X) for i in range(5)]
ROW_H = BOX_H + GAP_Y


def operator(ax, col, row, name, sub, col_color, face, fs=10.2):
    """วาง operator ที่ grid (col, row) — row นับจาก 0 = แถวบนสุด"""
    x, y = X[col], (3 - row) * ROW_H
    box = FancyBboxPatch((x, y), BOX_W, BOX_H,
                         boxstyle="round,pad=0.03,rounding_size=0.09",
                         facecolor=face, edgecolor=col_color, linewidth=1.8, zorder=3)
    ax.add_patch(box)
    ax.add_patch(FancyBboxPatch((x, y + BOX_H - HEAD_H), BOX_W, HEAD_H,
                                boxstyle="round,pad=0,rounding_size=0.0",
                                facecolor=col_color, edgecolor="none", zorder=4))
    ax.text(x + BOX_W / 2, y + BOX_H - HEAD_H / 2, name, ha="center", va="center",
            fontsize=fs, fontweight="bold", color="white", zorder=5, linespacing=1.3)
    ax.text(x + BOX_W / 2, y + (BOX_H - HEAD_H) / 2, sub, ha="center", va="center",
            fontsize=fs - 1.6, color=C["ink"], zorder=5, linespacing=1.55)
    ax.add_patch(Circle((x, y + BOX_H / 2), 0.05, facecolor="white",
                        edgecolor=col_color, linewidth=1.6, zorder=6))
    ax.add_patch(Circle((x + BOX_W, y + BOX_H / 2), 0.05, facecolor=col_color,
                        edgecolor=col_color, linewidth=1.6, zorder=6))
    return (x, y + BOX_H / 2), (x + BOX_W, y + BOX_H / 2)


def wire(ax, p1, p2, col=C["grey"], rad=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=13,
                                 color=col, lw=1.7, zorder=2,
                                 connectionstyle=f"arc3,rad={rad}"))


fig, ax = plt.subplots(figsize=(19.5, 12.6))

TOP = 4 * ROW_H + 0.15
ax.add_patch(plt.Rectangle((-0.3, -0.3), X[1] - 0.25, TOP + 0.5, facecolor="#F7F9FB", edgecolor="none", zorder=0))
ax.add_patch(plt.Rectangle((X[1] - 0.15, -0.3), X[4] - X[1] - 0.10, TOP + 0.5, facecolor="#F8FBF8", edgecolor="none", zorder=0))
ax.add_patch(plt.Rectangle((X[4] - 0.15, -0.3), BOX_W + 0.45, TOP + 0.5, facecolor="#FDF9F4", edgecolor="none", zorder=0))
for xc, label, col in [(X[0] + BOX_W / 2, "① EXTRACT", COL_E),
                       ((X[1] + X[3] + BOX_W) / 2, "② TRANSFORM", COL_T),
                       (X[4] + BOX_W / 2, "③ LOAD", COL_L)]:
    ax.text(xc, TOP + 0.30, label, ha="center", fontsize=15.5, fontweight="bold", color=col)

# ── แถว 0–2: Customer / Product / Date Dim — Read → 1 Transform → Write ──
dims = [
    (0, "Read Database", "AllElectronics\n.Customers",
        "Replace Missing\nValues", "Age, Income →\naverage / median", "→ CustomerDim"),
    (1, "Read Database", "AllElectronics\n.Items + .Suppliers",
        "Join", "Items × Suppliers\non SupplierID", "→ ProductDim"),
    (2, "Read Database", "AllElectronics\n.Purchases",
        "Generate\nAttributes", "DAY/MONTH/QUARTER\n(Purchases.Date)", "→ DateDim"),
]
t_out_pts = []
for row, rn, rs, tn, ts, wn in dims:
    _, r_out = operator(ax, 0, row, rn, rs, COL_E, FACE_E)
    t_in, t_out = operator(ax, 1, row, tn, ts, COL_T, FACE_T)
    wire(ax, r_out, t_in)
    w_in, _ = operator(ax, 4, row, "Write Database", wn, COL_L, FACE_L)
    wire(ax, t_out, w_in)          # ลากยาวข้ามเลนที่ว่าง — ไม่ชนอะไรเพราะ col 2,3 แถวนี้ไม่ได้ใช้
    t_out_pts.append(t_out)

# ── แถว 3: ElectFact — ใช้ครบ 5 คอลัมน์ (สายที่ซับซ้อนสุด) ──
row = 3
r_in, r_out = operator(ax, 0, row, "Read Database", "Item_sold + Purchases\n+ Items", COL_E, FACE_E)
j_in, j_out = operator(ax, 1, row, "Join (×3)", "รวม 3 ตาราง OLTP\nด้วย TransID, ItemID", COL_T, FACE_T)
wire(ax, r_out, j_in)
a_in, a_out = operator(ax, 2, row, "Aggregate", "GROUP BY product/customer/date\nSUM(qty), SUM(price×qty)", COL_T, FACE_T)
wire(ax, j_out, a_in)
lk_in, lk_out = operator(ax, 3, row, "Surrogate Lookup", "Join ×3 บน natural key\n→ Product/Customer/DateKey", COL_T, FACE_T)
wire(ax, a_out, lk_in)
w_in, _ = operator(ax, 4, row, "Write Database", "→ ElectFact", COL_L, FACE_L)
wire(ax, lk_out, w_in)

# เส้นแสดงว่า Lookup ต้องพึ่งพา Dim ทั้ง 3 ที่โหลดไปแล้ว (เส้นประ = "ใช้เป็นตารางอ้างอิง")
for p in t_out_pts:
    ax.add_patch(FancyArrowPatch(p, (X[3] + BOX_W / 2, (3 - row) * ROW_H + BOX_H),
                                 arrowstyle="-|>", mutation_scale=10, color=C["grey"],
                                 lw=1.1, ls=(0, (4, 3)), alpha=0.55, zorder=1,
                                 connectionstyle="arc3,rad=0.05"))

ax.text(X[1] + 0.15, (3 - 1) * ROW_H + BOX_H + 0.30,
        "Supplier ถูก de-normalize เข้า ProductDim ตรงนี้ (join ครั้งเดียว ไม่ต้อง join อีกตอน query)",
        ha="left", va="bottom", fontsize=9.6, color=COL_T, fontweight="bold")

ax.text((X[0] + X[4] + BOX_W) / 2, -0.75,
        "แต่ละแถว ↔ SQL ใน §7.6:  แถว 1–3 = INSERT…SELECT (populate Dim)   ·   แถวล่าง = INSERT…SELECT…JOIN (populate Fact, เส้นประ = surrogate-key lookup)",
        ha="center", fontsize=10.6, color=C["ink"], fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#F3F5F8", edgecolor=C["grey"], linewidth=1.0))

ax.set_xlim(-0.5, X[4] + BOX_W + 0.35)
ax.set_ylim(-1.35, TOP + 0.65)
ax.axis("off")
ax.grid(False)
fig.suptitle("RapidMiner Process Canvas — ETL เคส AllElectronics (1 แถว = 1 ตารางปลายทาง)",
             fontsize=16.5, fontweight="bold", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.955])
save(fig, "etl_rapidminer_canvas.png")
