"""บทที่ 13 — Star Schema เต็มรูปแบบของ "FoodGo" (เคสตัวอย่างที่เดินครบ 4 ขั้น)

วาดผลลัพธ์สุดท้ายของ workshop: 2 fact tables (Transaction + Accumulating
Snapshot) ที่ใช้ grain เดียวกัน (1 ออเดอร์) แต่วัดคนละเรื่อง, มี Dim_Date
เป็น role-playing dimension (เชื่อม 4 ครั้งเข้า Fact_Order_Lifecycle),
Dim_Restaurant/Dim_Rider เป็น conformed dimension (เชื่อมทั้ง 2 fact),
Dim_Customer/Dim_Promo เป็น dimension เฉพาะของ Fact_Order_Transaction
"""
from _style import apply, save, C
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

apply()

FACT1, FACT1_E = "#FDE9D9", C["orange"]   # Transaction fact
FACT2, FACT2_E = "#F3E1EE", C["purple"]   # Accumulating snapshot fact
DIM, DIM_E = "#DCEBF7", C["blue"]
DATE, DATE_E = "#E4F3E9", C["green"]


def table(ax, x, y, w, title, rows, fc, ec, fs=8.4, hi_rows=()):
    h = 0.32 + 0.225 * len(rows)
    ax.add_patch(FancyBboxPatch((x, y - h), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.05",
                                facecolor=fc, edgecolor=ec, linewidth=1.8, zorder=3))
    ax.add_patch(plt.Rectangle((x, y - 0.32), w, 0.32, facecolor=ec,
                               edgecolor="none", zorder=4))
    ax.text(x + w / 2, y - 0.16, title, ha="center", va="center",
            fontsize=fs + 1.3, fontweight="bold", color="white", zorder=5)
    for i, r in enumerate(rows):
        bold = r.endswith("(PK)") or r.endswith("(FK)") or i in hi_rows
        ry = y - 0.32 - 0.225 * (i + 0.55)
        if i in hi_rows:
            ax.add_patch(plt.Rectangle((x + 0.04, ry - 0.10), w - 0.08, 0.20,
                                       facecolor="#FFF3CF", edgecolor="none", zorder=4))
        ax.text(x + 0.09, ry, r, ha="left", va="center", fontsize=fs, zorder=5,
                fontweight="bold" if bold else "normal",
                color=C["ink"] if bold else "#414750")
    left = (x, y - h * 0.30)      # จุดต่อฝั่งซ้าย (สำหรับกล่องที่รับเส้นจากซ้าย)
    right = (x + w, y - h * 0.30)  # จุดต่อฝั่งขวา
    return left, right, (x, y, w, h)


def wire(ax, p1, p2, col=C["grey"], lw=1.5, rad=0.0, ls="-", alpha=0.85):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-", lw=lw, color=col,
                                 ls=ls, alpha=alpha, zorder=1,
                                 connectionstyle=f"arc3,rad={rad}"))


fig, ax = plt.subplots(figsize=(18.5, 11.0))

# ── DATE (ซ้ายสุด — role-playing hub) ──────────────────────────────────────
d_left, d_right, _ = table(ax, 0.2, 8.9, 2.55, "Dim_Date",
                           ["DateKey (PK)", "FullDate", "Day", "Month",
                            "Quarter", "Year", "DayOfWeek", "IsWeekend"],
                           DATE, DATE_E)

# ── FACT 1: Order Transaction (บน-กลาง) ────────────────────────────────────
f1_left, f1_right, _ = table(ax, 4.55, 10.35, 3.75, "Fact_Order_Transaction",
                             ["OrderDateKey (FK)", "CustomerKey (FK)",
                              "RestaurantKey (FK)", "RiderKey (FK)",
                              "PromoKey (FK)", "OrderNumber", "── measures ──",
                              "FoodAmount", "DeliveryFee", "DiscountAmount",
                              "ItemCount"], FACT1, FACT1_E, hi_rows={5})

# ── FACT 2: Order Lifecycle (ล่าง-กลาง) ────────────────────────────────────
f2_left, f2_right, _ = table(ax, 4.55, 4.55, 3.75, "Fact_Order_Lifecycle",
                             ["OrderNumber", "OrderPlacedDateKey (FK)",
                              "AcceptedDateKey (FK)", "PickedUpDateKey (FK)",
                              "CompletedDateKey (FK)", "RestaurantKey (FK)",
                              "RiderKey (FK)", "FinalStatus",
                              "── measures ──", "MinutesToAccept",
                              "MinutesToPickup", "MinutesToDeliver",
                              "TotalLifecycleMinutes"],
                             FACT2, FACT2_E, hi_rows={0})

# ── Dimensions ฝั่งขวา ──────────────────────────────────────────────────────
cust_left, _, _ = table(ax, 10.0, 10.85, 2.95, "Dim_Customer",
                        ["CustomerKey (PK)", "CustomerID", "CustomerName",
                         "JoinDate", "City"], DIM, DIM_E)
promo_left, _, _ = table(ax, 10.0, 8.35, 2.95, "Dim_Promo",
                         ["PromoKey (PK)", "PromoCode", "PromoName",
                          "DiscountType", "DiscountValue",
                          "(-1 = No Promo)"], DIM, DIM_E, hi_rows={5})
rest_left, _, _ = table(ax, 10.0, 5.55, 2.95, "Dim_Restaurant",
                        ["RestaurantKey (PK)", "RestaurantID",
                         "RestaurantName", "CuisineType", "City", "Rating"],
                        DIM, DIM_E)
rider_left, _, _ = table(ax, 10.0, 2.55, 2.95, "Dim_Rider",
                         ["RiderKey (PK)", "RiderID", "RiderName",
                          "VehicleType", "City"], DIM, DIM_E)

# ── เส้นเชื่อม: Date -> Fact1 (1 role) + Date -> Fact2 (4 roles, สีเขียวเน้น) ──
wire(ax, d_right, f1_left, col=DATE_E, lw=1.8, rad=0.05)
ax.text(3.15, 9.55, "OrderDate", fontsize=8.2, color=DATE_E, fontweight="bold",
        rotation=8, ha="center")

roles = [("Placed", -0.42), ("Accepted", -0.20), ("PickedUp", 0.05), ("Completed", 0.30)]
for (label, rad), ty in zip(roles, [7.55, 7.05, 6.55, 6.05]):
    wire(ax, d_right, f2_left, col=DATE_E, lw=1.6, rad=rad, alpha=0.75)
ax.annotate("Dim_Date ถูกใช้ 4 บทบาท\nใน Fact เดียวกัน = Role-Playing Dimension",
            xy=(2.75, 6.9), fontsize=9.6, color=DATE_E, fontweight="bold",
            ha="left", linespacing=1.5,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                      edgecolor=DATE_E, linewidth=1.1, alpha=0.95))

# Customer / Promo -> Fact1 เท่านั้น (process-specific)
wire(ax, cust_left, f1_right, col=DIM_E, rad=-0.15)
wire(ax, promo_left, f1_right, col=DIM_E, rad=0.05)

# Restaurant / Rider -> ทั้ง Fact1 และ Fact2 (conformed dimension)
wire(ax, rest_left, f1_right, col=C["ink"], rad=0.25, alpha=0.55)
wire(ax, rest_left, f2_right, col=C["ink"], rad=-0.10, alpha=0.55)
wire(ax, rider_left, f2_right, col=C["ink"], rad=0.05, alpha=0.55)
wire(ax, rider_left, f1_right, col=C["ink"], rad=-0.30, alpha=0.55)

ax.annotate("Restaurant / Rider ใช้ร่วมกัน\nทั้ง 2 fact table = Conformed Dimension",
            xy=(9.3, 4.3), fontsize=9.6, color=C["ink"], fontweight="bold",
            ha="right", linespacing=1.5,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                      edgecolor=C["grey"], linewidth=1.0, alpha=0.95))

ax.annotate("OrderNumber: เก็บซ้ำในทั้ง 2 fact\nเพื่อ drill-across ข้าม fact ได้\n= Degenerate Dimension",
            xy=(4.58, 8.78), xytext=(0.35, 4.05), fontsize=9.3, color=FACT1_E,
            fontweight="bold", ha="left", linespacing=1.5,
            arrowprops=dict(arrowstyle="->", color=FACT1_E, lw=1.3,
                            connectionstyle="arc3,rad=-0.2"))

ax.set_xlim(-0.2, 13.3)
ax.set_ylim(0.5, 11.4)
ax.axis("off")
ax.grid(False)
fig.suptitle('FoodGo — Star Schema ผลลัพธ์สุดท้าย (2 Fact Tables, grain เดียวกัน คนละเรื่องที่วัด)',
             fontsize=16.5, fontweight="bold", y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.965])
save(fig, "star_design_foodgo_schema.png")
