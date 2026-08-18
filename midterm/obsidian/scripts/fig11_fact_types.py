"""บทที่ 6 — Fact Table 3 ชนิด แสดงด้วย "ข้อมูลตัวอย่างจริง"

จุดที่ต้องสื่อ: ทั้งสามชนิดต่างกันที่ "1 แถวหมายถึงอะไร" (grain) และ
"แถวถูกเขียนเมื่อไหร่" — Transaction เขียนครั้งเดียวตอนเกิดเหตุ,
Periodic เขียนทุกงวดตามปฏิทิน, Accumulating เขียนครั้งเดียวแล้ว UPDATE ซ้ำ ๆ
"""
from _style import apply, save, C
import matplotlib.pyplot as plt

apply()

PANELS = [
    {
        "title": "① TRANSACTION FACT",
        "sub": "1 แถว = 1 เหตุการณ์ที่เกิดขึ้น",
        "color": C["blue"], "face": "#DCEBF7",
        "cols": ["DateKey", "ProductKey", "StoreKey", "Qty", "Amount"],
        "rows": [["20260803", "P-101", "S-01", "2", "240"],
                 ["20260803", "P-207", "S-01", "1", "980"],
                 ["20260803", "P-101", "S-04", "5", "600"],
                 ["20260804", "P-350", "S-02", "3", "150"],
                 ["20260804", "P-101", "S-01", "1", "120"]],
        "note": "grain ละเอียดที่สุด (High granularity)\n"
                "แถวใหม่ถูก INSERT ทุกครั้งที่ขาย — ไม่มีการแก้แถวเก่า\n"
                "ใช้: retail sales, e-commerce, financial transactions",
        "q": "\"ยอดขายรวมของแต่ละออเดอร์ออนไลน์เดือนที่แล้วเท่าไร\"",
    },
    {
        "title": "② PERIODIC SNAPSHOT FACT",
        "sub": "1 แถว = 1 เอนทิตี × 1 งวดเวลา",
        "color": C["green"], "face": "#E4F3E9",
        "cols": ["MonthKey", "ProductKey", "StoreKey", "StockLevel", "InvValue"],
        "rows": [["2026-06", "P-101", "S-01", "100", "50,000"],
                 ["2026-06", "P-207", "S-01", "45", "44,100"],
                 ["2026-07", "P-101", "S-01", "82", "41,000"],
                 ["2026-07", "P-207", "S-01", "60", "58,800"],
                 ["2026-08", "P-101", "S-01", "95", "47,500"]],
        "note": "ถ่ายภาพนิ่งตามรอบปฏิทิน — ไม่เก็บรายละเอียดรายธุรกรรม\n"
                "แถวใหม่ถูกเพิ่มทุกงวด แม้ไม่มีอะไรเกิดขึ้นเลย\n"
                "ใช้: inventory, account balance, HR headcount",
        "q": "\"ยอดสต็อกของแต่ละสินค้า ณ สิ้นเดือน เป็นเท่าไร\"",
    },
    {
        "title": "③ ACCUMULATING SNAPSHOT FACT",
        "sub": "1 แถว = 1 กระบวนการ (อัปเดตเรื่อย ๆ)",
        "color": C["orange"], "face": "#FDE9D9",
        "cols": ["OrderID", "OrderDate", "ShipDate", "DeliverDate", "DaysToShip"],
        "rows": [["ORD-771", "2026-08-01", "2026-08-02", "2026-08-04", "1"],
                 ["ORD-772", "2026-08-02", "2026-08-05", "2026-08-09", "3"],
                 ["ORD-773", "2026-08-03", "2026-08-04", "— NULL —", "1"],
                 ["ORD-774", "2026-08-05", "— NULL —", "— NULL —", "— NULL —"],
                 ["ORD-775", "2026-08-06", "— NULL —", "— NULL —", "— NULL —"]],
        "note": "มี Date หลายคอลัมน์ = milestone ของแต่ละขั้น\n"
                "แถวเดิมถูก UPDATE เมื่อกระบวนการคืบหน้า (NULL → มีค่า)\n"
                "ใช้: order fulfillment, ใบสมัครงาน, อนุมัติสินเชื่อ",
        "q": "\"กี่ % ของคำสั่งซื้อที่จัดส่งได้ภายใน 3 วัน\"",
    },
]

fig, axes = plt.subplots(1, 3, figsize=(16.2, 7.4))

for ax, P in zip(axes, PANELS):
    ncol, nrow = len(P["cols"]), len(P["rows"])
    cw, rh = 1.0 / ncol, 0.072

    # หัวตาราง
    ax.add_patch(plt.Rectangle((0, 0.72), 1.0, rh, facecolor=P["color"],
                               edgecolor="none", zorder=2))
    for j, c in enumerate(P["cols"]):
        ax.text((j + 0.5) * cw, 0.72 + rh / 2, c, ha="center", va="center",
                fontsize=7.6, fontweight="bold", color="white", zorder=3)
    # แถวข้อมูล
    for i, row in enumerate(P["rows"]):
        y = 0.72 - rh * (i + 1)
        ax.add_patch(plt.Rectangle((0, y), 1.0, rh,
                                   facecolor=P["face"] if i % 2 == 0 else "white",
                                   edgecolor="#D9DEE4", linewidth=0.6, zorder=1))
        for j, v in enumerate(row):
            null = "NULL" in v
            ax.text((j + 0.5) * cw, y + rh / 2, v, ha="center", va="center",
                    fontsize=7.4, zorder=3,
                    color=C["red"] if null else C["ink"],
                    style="italic" if null else "normal")
    ax.add_patch(plt.Rectangle((0, 0.72 - rh * nrow), 1.0, rh * (nrow + 1),
                               facecolor="none", edgecolor=P["color"],
                               linewidth=1.8, zorder=4))

    ax.text(0.5, 0.955, P["title"], ha="center", fontsize=13,
            fontweight="bold", color=P["color"])
    ax.text(0.5, 0.885, P["sub"], ha="center", fontsize=10.5, color=C["ink"],
            fontweight="bold")
    ax.text(0.5, 0.30, P["note"], ha="center", va="top", fontsize=9.3,
            linespacing=1.8, color=C["ink"])
    ax.text(0.5, 0.045, "คำถามธุรกิจตัวอย่าง:\n" + P["q"], ha="center",
            va="top", fontsize=9.3, linespacing=1.7, color=P["color"],
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor=P["face"],
                      edgecolor=P["color"], linewidth=1.1))

    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.12, 1.02)
    ax.axis("off")
    ax.grid(False)

fig.suptitle("Different Types of Fact Tables — ต่างกันที่ \"1 แถวหมายถึงอะไร\" และ \"เขียนแถวเมื่อไหร่\"",
             fontsize=15, fontweight="bold", y=0.985)
fig.tight_layout(rect=[0, 0, 1, 0.94])
save(fig, "dw_fact_types.png")
