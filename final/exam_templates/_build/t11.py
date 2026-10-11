from nbtools import md, code, build

TITLE = r"""
# T11 · Association Rules (Transaction data · Frequent itemsets · Apriori / FP-Growth · Rules · Support / Confidence / Lift)

**ใช้เมื่อโจทย์ถาม:** market basket / "สินค้าอะไรถูกซื้อด้วยกัน" · เตรียมข้อมูล transaction (ตะกร้า → ตาราง True/False) ·
discretize ตัวเลขก่อนหากฎ · frequent itemsets (min support) · Apriori ทีละขั้น (C1 → L1 → C2 → L2 …) · สร้างกฎ (min confidence) ·
ตีความ support / confidence / lift · กฎที่ทำนาย item เป้าหมาย (เช่น `pep=YES`) · ผลของการเปลี่ยน min support / min confidence

| ขั้น | ทำอะไร |
|---|---|
| 1 | แก้ **⚙️ CONFIG** — `DATA_PATH`, `FORMAT`, `ID_COL`, `MIN_SUPPORT`, `MIN_CONFIDENCE` (+ `BINS` ถ้าเป็นตารางที่มีตัวเลข) |
| 2 | Run All → §2 สินค้าขายดี · §3 frequent itemsets · §4 กฎ + ประโยคตีความ · §6 ผลของ min support |
| 3 | โจทย์ให้คำนวณมือ (ข้อมูล 5–10 ตะกร้า) → §7 แก้ `SMALL_TRANSACTIONS` |

**รูปแบบข้อมูลที่รองรับ (`FORMAT`)**
| FORMAT | หน้าตาไฟล์ | ตัวอย่าง |
|---|---|---|
| `"basket"` | 1 บรรทัด = 1 ตะกร้า คั่นด้วย comma (จำนวนไม่เท่ากัน, ไม่มีหัวตาราง) | `milk,bread,eggs` |
| `"onehot"` | 1 แถว = 1 ตะกร้า · 1 คอลัมน์ = 1 สินค้า ค่า 0/1, T/F, Y/N | BeautyCo (`Trans.` = id) |
| `"long"` | 2 คอลัมน์: รหัสตะกร้า + สินค้า (1 แถว = 1 สินค้าในตะกร้า) | `tid,item` |
| `"table"` | ตาราง attribute ทั่วไป (หมวดหมู่ + ตัวเลข) → แปลงเป็น item `attr=value` | bank-data (`pep=YES`) |
| `"auto"` | เดาให้ (basket / onehot / table) — `long` ต้องระบุเอง | |

> สูตร: **support(A→B)** = P(A∪B) · **confidence** = support(A∪B) / support(A) = P(B|A) · **lift** = confidence / support(B)
> lift > 1 = ซื้อด้วยกันบ่อยกว่าบังเอิญ (สัมพันธ์บวก) · = 1 อิสระกัน · < 1 สัมพันธ์ลบ (ทดแทนกัน)
"""

CONFIG = r'''# ════════ ⚙️ CONFIG — แก้ cell นี้ให้ตรงโจทย์ ════════
DATA_PATH = "../practice/data/p9_groceries_baskets.csv"
#   ตัวอย่างอื่น: "../../W10/BeautyCo_68.xls" (FORMAT="onehot", ID_COL="Trans.")
#               "../mock_lab/mock3_cluster_assoc/data/bank-data.csv" (FORMAT="table", ID_COL="id", BINS ด้านล่าง)
FORMAT    = "auto"           # "basket" | "onehot" | "long" | "table" | "auto"
ID_COL    = None             # คอลัมน์รหัสตะกร้า/ลูกค้า (ไม่ใช่สินค้า) เช่น "Trans." · None = ไม่มี
DROP_COLS = []               # คอลัมน์ที่ไม่เอามาหากฎ (เช่น region, sex ที่ไม่ให้ข้อมูล)
LONG_TID, LONG_ITEM = "tid", "item"   # ใช้เมื่อ FORMAT = "long"
BASKET_SEP = ","             # ตัวคั่นสินค้าในไฟล์ basket
# FORMAT = "table": คอลัมน์ตัวเลขต้อง discretize ก่อน
BINS       = {}              # {"age": 3, "income": 3} = แบ่ง 3 ช่วง · {"children": [-1, 0, 2, 10]} = กำหนดขอบเอง
BIN_METHOD = "frequency"     # "frequency" (equal frequency, เหมาะกับข้อมูลเบ้) | "width" (equal width)
BIN_LABELS = None            # เช่น ["LOW", "MID", "HIGH"] · None = ใช้ช่วงตัวเลข

ALGO           = "apriori"   # "apriori" | "fpgrowth" (ผลเหมือนกัน fpgrowth เร็วกว่า · RapidMiner ใช้ FP-Growth)
MIN_SUPPORT    = 0.02        # สัดส่วน (0.02 = 2% ของตะกร้า) · โจทย์ให้เป็น "จำนวนครั้ง" → หารด้วยจำนวนตะกร้า
MIN_CONFIDENCE = 0.30
MAX_LEN        = None        # ขนาด itemset สูงสุด (None = ไม่จำกัด)
TARGET_ITEM    = None        # สนใจกฎที่ "ทำนาย" item นี้ เช่น "pep=YES" / "whole milk" · None = ทุกกฎ
SORT_BY        = "lift"      # "lift" | "confidence" | "support"
TOP_N          = 10
RULE_TO_EXPLAIN = None       # (["root vegetables"], ["other vegetables"]) = คำนวณมือกฎนี้ · None = ใช้กฎอันดับ 1
SEED = 42
MISSING_MARKERS, SHEET, CSV_SEP = ["?", "", " ", "NA"], 0, ","
'''

S = [
md(r"""
## §0 เครื่องมือ association (mlxtend ถ้ามี · ถ้าไม่มีใช้ Apriori ที่เขียนเองด้านล่าง — ผลเหมือนกัน)
ไม่ต้องแก้ cell นี้ · ติดตั้ง mlxtend: `pip install mlxtend`
"""),
code(r'''from itertools import combinations
try:
    from mlxtend.frequent_patterns import apriori as _mx_apriori, fpgrowth as _mx_fpgrowth, association_rules as _mx_rules
    HAS_MLXTEND = True
except ImportError:
    HAS_MLXTEND = False
print("mlxtend:", "✅ มี" if HAS_MLXTEND else "❌ ไม่มี → ใช้ Apriori ที่เขียนเอง (ผลเหมือนกัน)")


def my_apriori(items, min_support, max_len=None, verbose=False):
    """Apriori แบบตำรา: Ck (join L(k-1) + prune ด้วย subset) → นับ support → Lk"""
    M = items.values.astype(bool); n = len(M); cols = list(items.columns)
    sup = M.mean(axis=0)
    L = {(i,): s for i, s in enumerate(sup) if s >= min_support}
    out, k = dict(L), 1
    if verbose:
        print(f"C1: {len(cols)} candidates → L1: {len(L)} frequent")
    while L and (max_len is None or k < max_len):
        k += 1
        prev = sorted(L)
        prev_set = set(prev)
        cands = []
        for a in range(len(prev)):
            for b in range(a + 1, len(prev)):
                if prev[a][:-1] != prev[b][:-1]:
                    break
                c = prev[a] + (prev[b][-1],)
                if all(s in prev_set for s in combinations(c, k - 1)):     # prune: ทุก subset ต้อง frequent
                    cands.append(c)
        L = {}
        for c in cands:
            s = M[:, list(c)].all(axis=1).mean()
            if s >= min_support:
                L[c] = s
        if verbose:
            print(f"C{k}: {len(cands)} candidates (หลัง prune) → L{k}: {len(L)} frequent")
        out.update(L)
    return pd.DataFrame({"support": list(out.values()),
                         "itemsets": [frozenset(cols[i] for i in c) for c in out]})


def my_rules(freq, min_confidence):
    sup = {s: v for s, v in zip(freq["itemsets"], freq["support"])}
    rows = []
    for iset, s in sup.items():
        if len(iset) < 2:
            continue
        for r in range(1, len(iset)):
            for ante in combinations(sorted(iset), r):
                A = frozenset(ante); C = iset - A
                conf = s / sup[A]
                if conf >= min_confidence:
                    rows.append({"antecedents": A, "consequents": C, "antecedent support": sup[A],
                                 "consequent support": sup[C], "support": s, "confidence": conf,
                                 "lift": conf / sup[C], "leverage": s - sup[A] * sup[C],
                                 "conviction": np.inf if conf == 1 else (1 - sup[C]) / (1 - conf)})
    return pd.DataFrame(rows)


def frequent_itemsets(items, min_support, algo=None, max_len=None):
    algo = ALGO if algo is None else algo
    if HAS_MLXTEND:
        f = (_mx_fpgrowth if algo == "fpgrowth" else _mx_apriori)(items.astype(bool), min_support=min_support,
                                                                   use_colnames=True, max_len=max_len)
    else:
        f = my_apriori(items, min_support, max_len)
    f["size"] = f["itemsets"].apply(len)
    return f.sort_values(["size", "support"], ascending=[True, False]).reset_index(drop=True)


def make_rules(freq, min_confidence, n_trans):
    if len(freq) == 0 or freq["size"].max() < 2:
        return pd.DataFrame(columns=["antecedents", "consequents", "support", "confidence", "lift"])
    if HAS_MLXTEND:
        try:
            r = _mx_rules(freq.drop(columns="size"), num_itemsets=n_trans, metric="confidence", min_threshold=min_confidence)
        except TypeError:                     # mlxtend รุ่นเก่าไม่มี num_itemsets
            r = _mx_rules(freq.drop(columns="size"), metric="confidence", min_threshold=min_confidence)
    else:
        r = my_rules(freq, min_confidence)
    if len(r) == 0:
        return r
    return r.sort_values([SORT_BY, "confidence"], ascending=False).reset_index(drop=True)


def iset_str(s):
    return "{" + ", ".join(sorted(map(str, s))) + "}"


def pretty(rules, n=None):
    """ตารางกฎอ่านง่าย: A → B"""
    t = rules.copy()
    t.insert(0, "rule", [f"{iset_str(a)} → {iset_str(c)}" for a, c in zip(t["antecedents"], t["consequents"])])
    keep = ["rule", "antecedent support", "consequent support", "support", "confidence", "lift"] + \
           [c for c in ["leverage", "conviction"] if c in t]
    t = t[[c for c in keep if c in t]]
    return t.head(n) if n else t


def explain_rule(A, C, items):
    """นับมือจากตาราง item → support / confidence / lift ของกฎ A → C + ประโยคตีความ"""
    A, C = list(A), list(C)
    n = len(items)
    nA = int(items[A].all(axis=1).sum()); nC = int(items[C].all(axis=1).sum()); nAC = int(items[A + C].all(axis=1).sum())
    sup, conf = nAC / n, (nAC / nA if nA else float("nan"))
    lift = conf / (nC / n)
    print(f"กฎ {iset_str(A)} → {iset_str(C)}  (จำนวนตะกร้าทั้งหมด N = {n})")
    print(f"  count(A) = {nA} · count(C) = {nC} · count(A∪C) = {nAC}")
    print(f"  support    = count(A∪C)/N        = {nAC}/{n} = {sup:.4f}")
    print(f"  confidence = count(A∪C)/count(A) = {nAC}/{nA} = {conf:.4f}")
    print(f"  lift       = confidence/support(C) = {conf:.4f}/{nC / n:.4f} = {lift:.4f}")
    kind = ("สัมพันธ์เชิงบวก (ซื้อด้วยกันบ่อยกว่าบังเอิญ)" if lift > 1.05 else
            "สัมพันธ์เชิงลบ (ซื้อด้วยกันน้อยกว่าบังเอิญ / ทดแทนกัน)" if lift < 0.95 else "เกือบอิสระกัน")
    print(f"✍️ ตะกร้าที่มี {iset_str(A)} และ {iset_str(C)} พร้อมกันมี {sup:.1%} ของทั้งหมด (support) · "
          f"ในตะกร้าที่มี {iset_str(A)} มี {iset_str(C)} ด้วย {conf:.1%} (confidence) · "
          f"ซึ่งเป็น {lift:.2f} เท่าของโอกาสปกติที่ {nC / n:.1%} (lift) → {kind}")
    return {"support": sup, "confidence": conf, "lift": lift}'''),

md(r"""
## §1 โหลด + แปลงเป็นตาราง transaction (True/False)
ผลลัพธ์ = `items` : 1 แถว = 1 ตะกร้า · 1 คอลัมน์ = 1 item · ค่า True = มีในตะกร้า
"""),
code(r'''def _is_basket_file(path, sep=BASKET_SEP):
    if str(path).lower().endswith((".xls", ".xlsx")):
        return False
    lines = [l for l in open(path, encoding="utf-8-sig").read().splitlines()[:200] if l.strip()]
    return len({l.count(sep) for l in lines}) > 1           # จำนวนช่องไม่เท่ากัน = basket


_TRUE = {"1", "1.0", "true", "t", "y", "yes"}
_FALSE = {"0", "0.0", "false", "f", "n", "no", "nan", ""}


def _is_onehot(df):
    vals = set()
    for c in df.columns:
        vals |= set(df[c].astype(str).str.strip().str.lower().unique())
    return vals <= (_TRUE | _FALSE)


fmt = FORMAT
if fmt == "auto":
    fmt = "basket" if _is_basket_file(DATA_PATH) else None
if fmt == "basket":
    baskets = [[i.strip() for i in l.split(BASKET_SEP) if i.strip()]
               for l in open(DATA_PATH, encoding="utf-8-sig").read().splitlines() if l.strip()]
    all_items = sorted({i for b in baskets for i in b})
    items = pd.DataFrame([[i in set(b) for i in all_items] for b in baskets], columns=all_items)
    print(f"basket: {len(baskets)} ตะกร้า | ตัวอย่าง: {baskets[:2]}")
else:
    raw = load_data(DATA_PATH)
    raw = raw.drop(columns=[c for c in list(DROP_COLS) + [ID_COL] if c and c in raw.columns and (fmt != "long" or c not in (LONG_TID, LONG_ITEM))])
    if fmt is None:
        fmt = "onehot" if _is_onehot(raw) else "table"
    if fmt == "long":
        items = pd.crosstab(raw[LONG_TID], raw[LONG_ITEM]).gt(0)
        items.columns = [str(c) for c in items.columns]
    elif fmt == "onehot":
        items = raw.apply(lambda s: s.astype(str).str.strip().str.lower().isin(_TRUE))
    else:   # table → discretize ตัวเลข → item "attr=value"
        tab = raw.copy()
        for c, b in BINS.items():
            if isinstance(b, int) and BIN_METHOD == "frequency":
                tab[c] = pd.qcut(tab[c], b, labels=BIN_LABELS, duplicates="drop")
            else:
                tab[c] = pd.cut(tab[c], b, labels=BIN_LABELS, include_lowest=True)
            print(f"discretize {c} ({BIN_METHOD if isinstance(b, int) else 'กำหนดขอบเอง'}):", tab[c].value_counts().sort_index().to_dict())
        left_num = [c for c in num_cols(tab) if tab[c].nunique() > 10]
        if left_num:
            print("⚠️ ยังเป็นตัวเลขต่อเนื่อง (ควรใส่ใน BINS):", left_num)
        items = pd.get_dummies(tab.astype(str).replace("nan", np.nan), prefix_sep="=").astype(bool)
print(f"FORMAT = {fmt} → items: {items.shape[0]} transactions × {items.shape[1]} items")
display(items.head())'''),
md(r"""**✍️ คำตอบ §1:** ข้อมูลเป็น transaction … ตะกร้า × … item · ตัด `…` (id ไม่ซ้ำ → ไม่มีทาง frequent / attribute ที่เกือบคงที่หรือ 50:50 ไม่ให้ข้อมูล) · discretize `…` แบบ equal frequency เพราะ … (ข้อมูลเบ้)"""),

md(r"""## §2 สำรวจ: จำนวน item ต่อตะกร้า + item ที่พบบ่อย (support ของ 1-itemset)"""),
code(r'''size = items.sum(axis=1)
item_sup = items.mean().sort_values(ascending=False)
print(f"ตะกร้า {len(items)} · item {items.shape[1]} · item ต่อตะกร้า: เฉลี่ย {size.mean():.2f} · median {size.median():.0f} · max {size.max()}")
top = item_sup.head(TOP_N).to_frame("support"); top["count"] = items[top.index].sum().values
display(top.round(4))
print(f"item ที่ support < MIN_SUPPORT ({MIN_SUPPORT}): {(item_sup < MIN_SUPPORT).sum()} จาก {len(item_sup)} → ถูกตัดตั้งแต่รอบแรกของ Apriori")
fig, ax = plt.subplots(1, 2, figsize=(13, 4))
item_sup.head(TOP_N)[::-1].plot.barh(ax=ax[0], title=f"Top {TOP_N} items (support)")
ax[0].axvline(MIN_SUPPORT, color="r", ls="--", label=f"min support {MIN_SUPPORT}"); ax[0].legend()
size.value_counts().sort_index().plot.bar(ax=ax[1], title="Items per transaction"); plt.tight_layout(); plt.show()
print(f"✍️ item ที่พบบ่อยสุดคือ {item_sup.index[0]} (support = {item_sup.iloc[0]:.4f} = {int(items[item_sup.index[0]].sum())} ตะกร้า)")'''),

md(r"""
## §3 Frequent itemsets (Apriori / FP-Growth, min support)
**Apriori principle:** ถ้า itemset ไม่ frequent → superset ทุกตัวก็ไม่ frequent → ตัดทิ้งได้ (anti-monotone ของ support)
"""),
code(r'''freq = frequent_itemsets(items, MIN_SUPPORT, ALGO, MAX_LEN)
print(f"{ALGO} min_support = {MIN_SUPPORT} (≥ {int(np.ceil(MIN_SUPPORT * len(items)))} ตะกร้า) → frequent itemsets {len(freq)} ชุด")
print("แยกตามขนาด:", freq["size"].value_counts().sort_index().to_dict())
show_f = freq.assign(itemset=freq["itemsets"].apply(iset_str), count=(freq["support"] * len(items)).round().astype(int))
for k in sorted(freq["size"].unique()):
    print(f"── {k}-itemsets (top {TOP_N}):")
    display(show_f[show_f["size"] == k].sort_values("support", ascending=False)[["itemset", "support", "count"]].head(TOP_N))
# maximal = ไม่มี superset ที่ frequent · closed = ไม่มี superset ที่ support เท่ากัน
sets = list(zip(freq["itemsets"], freq["support"]))
maximal = sum(1 for s, _ in sets if not any(s < t for t, _ in sets))
closed = sum(1 for s, v in sets if not any(s < t and abs(v - w) < 1e-12 for t, w in sets))
print(f"maximal frequent itemsets = {maximal} · closed frequent itemsets = {closed}")'''),
md(r"""**✍️ คำตอบ §3:** min support … ได้ frequent itemset … ชุด (1-item … · 2-item … · 3-item …) · คู่ที่พบบ่อยสุดคือ {…} support … (… ตะกร้า)"""),

md(r"""
## §4 สร้างกฎ (min confidence) → เรียงตาม lift ⭐
กฎ A → B สร้างจาก frequent itemset ที่มี ≥ 2 item: แบ่งเป็น A (antecedent / LHS) กับ B (consequent / RHS) แล้วเก็บเฉพาะ confidence ≥ min
"""),
code(r'''rules = make_rules(freq, MIN_CONFIDENCE, len(items))
print(f"min_confidence = {MIN_CONFIDENCE} → {len(rules)} rules (เรียงตาม {SORT_BY})")
if len(rules):
    display(pretty(rules, TOP_N).round(4))
    r1 = rules.iloc[0]
    print(f"✍️ กฎอันดับ 1: {iset_str(r1.antecedents)} → {iset_str(r1.consequents)} · support {r1.support:.4f} · "
          f"confidence {r1.confidence:.4f} · lift {r1.lift:.4f}")
    print(f"   = ตะกร้า {r1.support:.1%} มีทั้งสองอย่าง · คนที่ซื้อ {iset_str(r1.antecedents)} ซื้อ {iset_str(r1.consequents)} ด้วย {r1.confidence:.1%} "
          f"· มากกว่าปกติ ({r1['consequent support']:.1%}) {r1.lift:.2f} เท่า → เสนอ: จัดวางใกล้กัน / ทำโปรโมชันคู่ / แนะนำสินค้า (cross-sell)")
    neg = rules[rules["lift"] < 1]
    print(f"กฎที่ lift < 1 (confidence ผ่านแต่สัมพันธ์ลบ — มักเพราะ consequent เป็นของขายดี): {len(neg)} กฎ")
    if len(neg):
        display(pretty(neg.sort_values("lift"), 5).round(4))
else:
    print("⚠️ ไม่มีกฎผ่านเกณฑ์ → ลด MIN_SUPPORT หรือ MIN_CONFIDENCE")'''),
code(r'''# กฎที่ "ทำนาย" item เป้าหมาย (consequent = TARGET_ITEM) — เช่นหาโปรไฟล์ลูกค้าที่ซื้อ pep=YES
if TARGET_ITEM is not None and len(rules):
    tr = rules[rules["consequents"] == frozenset({TARGET_ITEM})].sort_values("lift", ascending=False)
    base = items[TARGET_ITEM].mean() if TARGET_ITEM in items else float("nan")
    print(f"P({TARGET_ITEM}) ทั้งหมด = {base:.4f} · กฎที่ทำนาย {TARGET_ITEM}: {len(tr)} กฎ")
    display(pretty(tr, TOP_N).round(4))
    # กฎที่มี TARGET_ITEM อยู่ฝั่งไหนก็ได้
    anyside = rules[rules.apply(lambda r: TARGET_ITEM in r.antecedents or TARGET_ITEM in r.consequents, axis=1)]
    print(f"กฎที่มี {TARGET_ITEM} อยู่ฝั่งใดฝั่งหนึ่ง: {len(anyside)} กฎ")
else:
    print("TARGET_ITEM = None → ข้าม (ตัวอย่าง TARGET_ITEM = 'pep=YES' หรือ 'whole milk')")'''),
md(r"""
**✍️ คำตอบ §4 (ตีความกฎ 1 ข้อให้ครบ 3 ค่า):** กฎ {…} → {…}
- **support = …** → ตะกร้า …% มีทั้ง … และ … (กฎนี้เกิดบ่อยแค่ไหน / สำคัญแค่ไหนต่อยอดขาย)
- **confidence = …** → ลูกค้าที่ซื้อ … มี …% ที่ซื้อ … ด้วย (ความน่าเชื่อถือของกฎ = P(B|A))
- **lift = …** → มากกว่าโอกาสปกติ … เท่า (> 1 = สัมพันธ์จริง ไม่ใช่เพราะ … ขายดีอยู่แล้ว)
- **ข้อเสนอ:** วางสินค้าใกล้กัน / bundle / แนะนำ … ให้คนที่ซื้อ …
- confidence สูงแต่ lift ≤ 1 = กฎหลอก (consequent ขายดีอยู่แล้ว) → ใช้ lift ประกอบเสมอ
"""),

md(r"""## §5 คำนวณกฎด้วยมือ (นับจากตาราง) — ตรวจสูตร / ตอบโจทย์ "แสดงวิธีคำนวณ" """),
code(r'''if RULE_TO_EXPLAIN is not None:
    A, C = RULE_TO_EXPLAIN
elif len(rules):
    A, C = sorted(rules.iloc[0].antecedents), sorted(rules.iloc[0].consequents)
else:
    A = C = None
if A is not None:
    explain_rule(A, C, items)'''),

md(r"""
## §6 ผลของการเปลี่ยน min support / min confidence
- min support ↑ → itemset/กฎ **น้อยลง** (เหลือแต่ของขายดี) · ↓ → กฎเยอะ ช้าขึ้น และมีกฎจาก item ที่หายาก
- min confidence ↑ → กฎน้อยลงแต่น่าเชื่อถือขึ้น (ไม่ได้รับประกันว่า lift สูง)
"""),
code(r'''SUP_GRID  = [MIN_SUPPORT / 2, MIN_SUPPORT, MIN_SUPPORT * 2, MIN_SUPPORT * 5]   # ✏️ ค่า min support ที่ลอง
CONF_GRID = [0.2, 0.3, 0.5, 0.7, 0.9]                                            # ✏️ ค่า min confidence ที่ลอง
grid_rows = []
for s in SUP_GRID:
    f = frequent_itemsets(items, s, ALGO, MAX_LEN)
    row = {"min_support": s, "frequent itemsets": len(f), "max size": int(f["size"].max()) if len(f) else 0}
    for c in CONF_GRID:
        row[f"rules (conf≥{c})"] = len(make_rules(f, c, len(items)))
    grid_rows.append(row)
sens = pd.DataFrame(grid_rows); display(sens)
print(f"✍️ เพิ่ม min support จาก {SUP_GRID[0]:g} เป็น {SUP_GRID[-1]:g} → itemset ลดจาก {sens.iloc[0, 1]} เหลือ {sens.iloc[-1, 1]} "
      f"· เพิ่ม min confidence → จำนวนกฎลดลง (ดูแต่ละแถว)")'''),

md(r"""
## §7 Apriori ทีละขั้นบนข้อมูลเล็ก (ตอบโจทย์คำนวณมือ: C1 → L1 → C2 → L2 → …)
✏️ ใส่ตะกร้าจากโจทย์ใน `SMALL_TRANSACTIONS` และ `SMALL_MINSUP` (เป็น **จำนวนครั้ง** หรือสัดส่วนก็ได้)
"""),
code(r'''SMALL_TRANSACTIONS = [            # ✏️ ตัวอย่างในตำรา (Tan et al.) — แทนด้วยข้อมูลโจทย์
    ["Bread", "Milk"],
    ["Bread", "Diaper", "Beer", "Eggs"],
    ["Milk", "Diaper", "Beer", "Coke"],
    ["Bread", "Milk", "Diaper", "Beer"],
    ["Bread", "Milk", "Diaper", "Coke"],
]
SMALL_MINSUP  = 3                 # ✏️ min support count (≥ 1 = จำนวนครั้ง · < 1 = สัดส่วน)
SMALL_MINCONF = 0.6               # ✏️

n_s = len(SMALL_TRANSACTIONS)
minc = SMALL_MINSUP if SMALL_MINSUP >= 1 else int(np.ceil(SMALL_MINSUP * n_s))
tsets = [set(t) for t in SMALL_TRANSACTIONS]
cnt = lambda c: sum(1 for t in tsets if set(c) <= t)
items_all = sorted({i for t in tsets for i in t})
print(f"N = {n_s} ตะกร้า · min support count = {minc} (= {minc / n_s:.2f})\n")
Lk = [(i,) for i in items_all]; k = 1; small_freq = {}
while Lk:
    if k == 1:
        Ck = Lk
    else:  # join + prune
        prev = sorted(Lk); ps = set(prev)
        joined = sorted({tuple(sorted(set(a) | set(b))) for a in prev for b in prev if len(set(a) | set(b)) == k})
        Ck = [c for c in joined if all(s in ps for s in combinations(c, k - 1))]
        pruned = [c for c in joined if c not in Ck]
        if pruned:
            print(f"   prune C{k} (มี subset ที่ไม่ frequent): {[', '.join(c) for c in pruned]}")
    if not Ck:
        break
    tab = pd.DataFrame({"itemset": ["{" + ", ".join(c) + "}" for c in Ck], "count": [cnt(c) for c in Ck]})
    tab["support"] = tab["count"] / n_s; tab["frequent?"] = np.where(tab["count"] >= minc, "✔", "✘")
    print(f"C{k} → L{k}:"); display(tab)
    Lk = [c for c in Ck if cnt(c) >= minc]
    small_freq.update({c: cnt(c) for c in Lk}); k += 1
print("frequent itemsets ทั้งหมด:", {"{" + ", ".join(c) + "}": v for c, v in small_freq.items()})

srows = []
for c, v in small_freq.items():
    for r in range(1, len(c)):
        for a in combinations(c, r):
            b = tuple(x for x in c if x not in a)
            conf = v / cnt(a)
            srows.append({"rule": "{" + ", ".join(a) + "} → {" + ", ".join(b) + "}", "support": v / n_s,
                          "confidence": f"{v}/{cnt(a)} = {conf:.3f}", "lift": conf / (cnt(b) / n_s),
                          "pass conf?": "✔" if conf >= SMALL_MINCONF else "✘"})
print(f"\nกฎทั้งหมดจาก frequent itemsets (min confidence = {SMALL_MINCONF}):")
display(pd.DataFrame(srows).sort_values(["pass conf?", "lift"], ascending=[True, False]).round(4) if srows else "ไม่มี itemset ขนาด ≥ 2")'''),

md(r"""## §8 กราฟ support × confidence (สี = lift) + บันทึกกฎ"""),
code(r'''if len(rules):
    plt.figure(figsize=(7, 4.5))
    sc = plt.scatter(rules["support"], rules["confidence"], c=rules["lift"], cmap="viridis", s=40, alpha=.8)
    plt.colorbar(sc, label="lift"); plt.xlabel("support"); plt.ylabel("confidence")
    plt.title(f"{len(rules)} rules (min sup {MIN_SUPPORT}, min conf {MIN_CONFIDENCE})"); plt.show()
    out = pretty(rules)
    out.to_csv("t11_rules.csv", index=False); print("saved t11_rules.csv", out.shape)'''),
]

if __name__ == "__main__":
    build("../T11_association_rules.ipynb", TITLE, CONFIG, S)
