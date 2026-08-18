"""บทที่ 5 — Star Schema vs Snowflake Schema วางเทียบกัน

ใช้ตัวอย่าง Retail Sales เดียวกันทั้งสองฝั่ง เพื่อให้เห็นชัดว่า snowflake
คือ "star ที่เอา dimension มา normalize ต่อ" ไม่ใช่โครงสร้างคนละเรื่อง
"""
from _style import apply, save, C
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

apply()

FACT = "#FDE9D9"      # ส้มอ่อน = fact
FACT_E = C["orange"]
DIM = "#DCEBF7"       # ฟ้าอ่อน = dimension
DIM_E = C["blue"]
SUB = "#E4F3E9"       # เขียวอ่อน = dimension ลูก (เฉพาะ snowflake)
SUB_E = C["green"]


def table(ax, x, y, w, title, rows, fc, ec, fs=8.0):
    """วาดกล่องตาราง 1 ใบ: หัวตาราง + รายการคอลัมน์ คืนค่าจุดกึ่งกลาง"""
    h = 0.30 + 0.208 * len(rows)
    ax.add_patch(FancyBboxPatch((x, y - h), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor=fc, edgecolor=ec, linewidth=1.7,
                                zorder=3))
    ax.add_patch(plt.Rectangle((x, y - 0.30), w, 0.30, facecolor=ec,
                               edgecolor="none", zorder=4))
    ax.text(x + w / 2, y - 0.15, title, ha="center", va="center",
            fontsize=fs + 1.0, fontweight="bold", color="white", zorder=5)
    for i, r in enumerate(rows):
        bold = r.endswith("(PK)") or r.endswith("(FK)")
        ax.text(x + 0.09, y - 0.30 - 0.208 * (i + 0.55), r, ha="left",
                va="center", fontsize=fs, zorder=5,
                fontweight="bold" if bold else "normal",
                color=C["ink"] if bold else "#414750")
    return (x + w / 2, y - h / 2), (x, y, w, h)


def link(ax, a, b, col=C["grey"], lw=1.6, ls="-"):
    ax.plot([a[0], b[0]], [a[1], b[1]], color=col, lw=lw, ls=ls, zorder=1)


fig, axes = plt.subplots(1, 2, figsize=(15.0, 9.4))

fact_rows = ["DateKey (FK)", "ProductKey (FK)", "StoreKey (FK)",
             "── measures ──", "QuantitySold", "DollarSalesAmount"]

# ══════════ ซ้าย: STAR ══════════
ax = axes[0]
cF, _ = table(ax, 3.45, 5.35, 2.6, "Sales Fact", fact_rows, FACT, FACT_E)
cD, _ = table(ax, 0.25, 7.85, 2.5, "Dim_Date",
              ["DateKey (PK)", "FullDate", "DayOfWeek", "Month",
               "Quarter", "Year", "HolidayFlag"], DIM, DIM_E)
cP, _ = table(ax, 6.75, 7.85, 2.5, "Dim_Product",
              ["ProductKey (PK)", "SKU", "Description", "Brand",
               "Category", "Department"], DIM, DIM_E)
cS, _ = table(ax, 3.45, 2.15, 2.6, "Dim_Store",
              ["StoreKey (PK)", "StoreName", "Address", "City",
               "District", "State"], DIM, DIM_E)
for c in (cD, cP, cS):
    link(ax, cF, c)
ax.set_title("STAR SCHEMA — dimension แบน ไม่ normalize", fontsize=13.5, pad=12)
ax.text(4.75, -0.35,
        "✓ join น้อย → query เร็ว\n"
        "✓ เข้าใจง่าย ผู้ใช้ธุรกิจอ่านออก\n"
        "✗ ข้อมูลซ้ำซ้อน (redundancy) กินพื้นที่มากกว่า",
        ha="center", va="top", fontsize=10.2, linespacing=1.8,
        color=C["ink"],
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#F6FAFD",
                  edgecolor=DIM_E, linewidth=1.2))

# ══════════ ขวา: SNOWFLAKE ══════════
ax = axes[1]
cF2, _ = table(ax, 3.45, 5.35, 2.6, "Sales Fact", fact_rows, FACT, FACT_E)
cD2, _ = table(ax, 0.55, 7.85, 2.3, "Dim_Date",
               ["DateKey (PK)", "FullDate", "MonthKey (FK)"], DIM, DIM_E)
cP2, _ = table(ax, 6.55, 7.20, 2.3, "Dim_Product",
               ["ProductKey (PK)", "SKU", "Description",
                "BrandKey (FK)"], DIM, DIM_E)
cS2, _ = table(ax, 3.45, 2.55, 2.6, "Dim_Store",
               ["StoreKey (PK)", "StoreName", "CityKey (FK)"], DIM, DIM_E)
# ตารางลูกที่แตกออกมาจากการ normalize
cM, _ = table(ax, 0.10, 9.85, 2.3, "Dim_Month",
              ["MonthKey (PK)", "Month", "Quarter", "Year"], SUB, SUB_E)
cB, _ = table(ax, 7.05, 9.85, 2.3, "Dim_Brand",
              ["BrandKey (PK)", "Brand", "CategoryKey (FK)"], SUB, SUB_E)
cC, _ = table(ax, 4.10, 1.15, 2.4, "Dim_City",
              ["CityKey (PK)", "City", "District", "State"], SUB, SUB_E)
for c in (cD2, cP2, cS2):
    link(ax, cF2, c)
link(ax, cD2, cM, SUB_E, 1.6, "--")
link(ax, cP2, cB, SUB_E, 1.6, "--")
link(ax, cS2, cC, SUB_E, 1.6, "--")
ax.set_title("SNOWFLAKE SCHEMA — dimension ถูก normalize แตกเป็นตารางลูก",
             fontsize=13.5, pad=12)
ax.text(4.75, -0.35,
        "✓ ลดความซ้ำซ้อน ประหยัดพื้นที่\n"
        "✓ ดูแลข้อมูลที่เปลี่ยนบ่อยง่ายกว่า\n"
        "✗ ต้อง join หลายชั้น → query ช้าลงและซับซ้อนขึ้น",
        ha="center", va="top", fontsize=10.2, linespacing=1.8,
        color=C["ink"],
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#F4FBF6",
                  edgecolor=SUB_E, linewidth=1.2))

for ax in axes:
    ax.set_xlim(-0.15, 9.6)
    ax.set_ylim(-2.75, 10.3)
    ax.axis("off")
    ax.grid(False)

fig.suptitle("Star Schema vs Snowflake Schema — "
             "\"Snowflake schemas are normalized star-schemas\"",
             fontsize=15, fontweight="bold", y=0.985)
fig.tight_layout(rect=[0, 0, 1, 0.95])
save(fig, "dw_star_vs_snowflake.png")
