"""บทที่ 7 — การสร้าง Sales-Fact Table 3 ขั้น (ใช้ข้อมูลจริงจากสไลด์ ETL p.12–14)

สคริปต์นี้ "ทำ ETL จริง" ด้วย Python stdlib แล้ววาดผลออกมา — ไม่ได้ก๊อปตัวเลข
จากสไลด์มาแปะ ดังนั้นถ้าตัวเลขตรงกับสไลด์ ก็แปลว่าเข้าใจขั้นตอนถูกต้องจริง
"""
from _style import apply, save, C
import matplotlib.pyplot as plt
from collections import OrderedDict

apply()

# ── ข้อมูลต้นทางจากสไลด์ (สังเกต price = -30 คือข้อมูลสกปรกที่ต้องล้าง) ──────
sales_log = [
    ("T01", "Q33", "A01", "9901", 10, 2), ("T01", "Q33", "A01", "9901", 10, 3),
    ("T01", "K21", "B01", "9902", -30, 2),          # ⚠️ ราคาติดลบ!
    ("T01", "Q33", "A03", "9903", 10, 1),
    ("T01", "K21", "A02", "9903", 5, 2), ("T01", "K21", "A02", "9903", 5, 3),
    ("T01", "K21", "A02", "9903", 5, 4), ("T01", "K21", "A02", "9903", 5, 1),
    ("T02", "Q33", "A01", "9902", 20, 5), ("T02", "K21", "A03", "9901", 5, 1),
    ("T02", "K21", "B02", "9904", 20, 1), ("T04", "K21", "A02", "9901", 3, 1),
    ("T05", "P67", "A01", "9905", 4, 1),  ("T05", "K21", "A02", "9905", 10, 1),
]
cost_tbl = {("T01", "Q33", "A01"): 5,  ("T01", "K21", "B01"): 20,
            ("T01", "Q33", "A03"): 5,  ("T01", "K21", "A02"): 2,
            ("T02", "Q33", "A01"): 10, ("T02", "K21", "A03"): 3,
            ("T02", "K21", "B02"): 15, ("T04", "K21", "A02"): 1,
            ("T05", "P67", "A01"): 3,  ("T05", "K21", "A02"): 3}

# ── ขั้นที่ 1: CLEAN + JOIN บน (time_tag, pid, sid) ────────────────────────
joined = []
for t, p, s, c, price, qty in sales_log:
    price = abs(price)                       # ล้าง: ราคาติดลบ -> ค่าสัมบูรณ์
    joined.append((t, p, s, c, price, qty, cost_tbl[(t, p, s)]))

# ── ขั้นที่ 2: COMPUTE amount = price*qty, cost = unit_cost*qty ────────────
computed = [(t, p, s, c, price * qty, uc * qty)
            for t, p, s, c, price, qty, uc in joined]

# ── ขั้นที่ 3: GROUP BY (time,pid,sid,cid) + AGGREGATE ────────────────────
agg = OrderedDict()
for t, p, s, c, amt, cst in computed:
    k = (t, p, s, c)
    a, b = agg.get(k, (0, 0))
    agg[k] = (a + amt, b + cst)
fact = [(*k, v[0], v[1]) for k, v in agg.items()]

print(f"source rows = {len(sales_log)}  ->  fact rows = {len(fact)}  "
      f"(ยุบไป {len(sales_log)-len(fact)} แถวจากการ aggregate)")
print(f"ยอดขายรวมทั้งหมด = {sum(r[4] for r in fact)}   ต้นทุนรวม = {sum(r[5] for r in fact)}")


def draw(ax, title, cols, rows, color, face, hi_rows=(), hi_note=None, fs=7.4):
    n = len(rows)
    rh = 0.9 / (n + 2)
    cw = 1.0 / len(cols)
    ax.add_patch(plt.Rectangle((0, 0.90 - rh), 1.0, rh, facecolor=color,
                               edgecolor="none", zorder=2))
    for j, cname in enumerate(cols):
        ax.text((j + 0.5) * cw, 0.90 - rh / 2, cname, ha="center", va="center",
                fontsize=fs, fontweight="bold", color="white", zorder=3)
    for i, row in enumerate(rows):
        y = 0.90 - rh * (i + 2)
        hi = i in hi_rows
        ax.add_patch(plt.Rectangle((0, y), 1.0, rh,
                                   facecolor="#FFE7DB" if hi else
                                   (face if i % 2 == 0 else "white"),
                                   edgecolor="#DDE2E7", linewidth=0.5, zorder=1))
        for j, v in enumerate(row):
            ax.text((j + 0.5) * cw, y + rh / 2, str(v), ha="center", va="center",
                    fontsize=fs, zorder=3,
                    color=C["red"] if hi else C["ink"],
                    fontweight="bold" if hi else "normal")
    ax.add_patch(plt.Rectangle((0, 0.90 - rh * (n + 1)), 1.0, rh * (n + 1),
                               facecolor="none", edgecolor=color, linewidth=1.6,
                               zorder=4))
    ax.text(0.5, 0.96, title, ha="center", fontsize=11, fontweight="bold",
            color=color)
    if hi_note:
        ax.text(0.5, 0.90 - rh * (n + 1) - 0.035, hi_note, ha="center", va="top",
                fontsize=8.6, color=C["red"], fontweight="bold")
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.06, 1.0)
    ax.axis("off"); ax.grid(False)


fig, axes = plt.subplots(1, 4, figsize=(17.5, 6.6))

draw(axes[0], "① EXTRACT — Sales_log (ดิบ)",
     ["time", "pid", "sid", "cid", "price", "qty"],
     [(t, p, s, c, price, q) for t, p, s, c, price, q in sales_log],
     C["grey"], "#F2F4F6", hi_rows={2},
     hi_note="⚠️ price = -30 → ข้อมูลสกปรก")

draw(axes[1], "② TRANSFORM-1 — Clean + Join กับ Cost",
     ["time", "pid", "sid", "cid", "price", "qty", "u_cost"],
     joined, C["blue"], "#DCEBF7", hi_rows={2},
     hi_note="✓ -30 ถูกล้างเป็น 30 · u_cost มาจากการ join")

draw(axes[2], "③ TRANSFORM-2 — Compute measures",
     ["time", "pid", "sid", "cid", "amount", "cost"],
     computed, C["green"], "#E4F3E9",
     hi_note="amount = price × qty   ·   cost = u_cost × qty")

draw(axes[3], f"④ LOAD — Sales-Fact ({len(fact)} แถว)",
     ["time_k", "prod_k", "store_k", "cust_k", "amount", "cost"],
     fact, C["orange"], "#FDE9D9",
     hi_note=f"GROUP BY 4 คีย์ + SUM → {len(sales_log)} แถว ยุบเหลือ {len(fact)} แถว")

fig.suptitle("ETL ในทางปฏิบัติ — จาก Sales_log ดิบ สู่ Sales-Fact Table "
             "(ตัวเลขคำนวณจริงจากข้อมูลในสไลด์)",
             fontsize=14.5, fontweight="bold", y=0.985)
fig.tight_layout(rect=[0, 0, 1, 0.94])
save(fig, "etl_fact_build.png")
