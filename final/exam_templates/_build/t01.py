from nbtools import md, code, build

TITLE = r"""
# T01 · Data Handling & Visualization (Import · Inspect · Select · Filter · Set Role · Join · Concatenate · Pivot · Charts)

**ใช้เมื่อโจทย์ถาม:** อ่านไฟล์/ตรวจข้อมูล · สรุปสถิติ · เลือก/ตัดคอลัมน์ · กรองแถว · ตั้ง id/label · ต่อตาราง (append/concat) · join/merge ·
group by / aggregate · pivot table · สร้างคอลัมน์ใหม่ · วาดกราฟ (histogram, boxplot, bar, scatter, heatmap) + ตีความ

| ขั้น | ทำอะไร |
|---|---|
| 1 | แก้ **⚙️ CONFIG** (cell ถัดไป) — path ไฟล์ + ชื่อคอลัมน์ |
| 2 | **Run All** (หรือรันทีละ cell จากบนลงล่าง) |
| 3 | ไปเฉพาะ § ที่โจทย์ถาม → แก้บรรทัดที่มี `# ✏️` ใน cell นั้น → รันใหม่ |
| 4 | copy ประโยค `✍️` ที่พิมพ์ออกมา + เติมใน cell **คำตอบ** · ลบ § ที่ไม่ใช้ก่อนส่ง |

> ทุก § ใช้ตัวแปร `df` (ข้อมูลหลัก) ต่อกันเป็นทอด ๆ — ถ้าข้าม § ไหนก็ไม่เป็นไร ยกเว้น §1 ต้องรันเสมอ
"""

CONFIG = r'''# ════════ ⚙️ CONFIG — แก้ cell นี้ให้ตรงโจทย์ ════════
DATA_PATH   = "../practice/data/p1_bills_week1.csv"   # ไฟล์หลัก (.csv / .xlsx / .xls)
DATA_PATH_2 = "../practice/data/p1_bills_week2.csv"   # ไฟล์ที่จะ "ต่อแถว" (concatenate/append) — ไม่มีใส่ None
LOOKUP_PATH = "../practice/data/p1_day_info.csv"      # ไฟล์ที่จะ "join" เข้ามา — ไม่มีใส่ None
JOIN_KEY    = "day"          # คอลัมน์ที่ใช้จับคู่ (ชื่อต่างกัน 2 ฝั่ง → ใส่ tuple เช่น ("cust_id", "id"))
JOIN_HOW    = "left"         # "inner" = เฉพาะที่ตรงกัน · "left" = เก็บทุกแถวของไฟล์หลัก · "outer" = เก็บทั้งหมด
ID_COL      = "bill_id"      # คอลัมน์ id (ไม่มีใส่ None)
TARGET      = "tip"          # คอลัมน์ที่โจทย์สนใจ/label (ไม่มีใส่ None)
SHEET       = 0              # ชื่อ/ลำดับ sheet ถ้าเป็น Excel
CSV_SEP     = ","            # ตัวคั่น csv (บางไฟล์ใช้ ";")
MISSING_MARKERS = ["?", "", " ", "NA", "N/A", "null", "-"]   # ค่าที่แปลว่า "ว่าง" ในไฟล์นี้
SEED = 42
'''

S = [
md(r"""
## §1 Import + ตรวจข้อมูล (Inspect) — **รันเสมอ**
โจทย์: *"import ข้อมูลและตรวจสอบ · มีกี่แถว/คอลัมน์ · ชนิดข้อมูล · ค่าว่าง · สรุปสถิติ"*
"""),
code(r'''df = load_data(DATA_PATH)
display(df.head())
check(df, TARGET)'''),
code(r'''# สรุปสถิติ: ตัวเลข (mean, std, min, quartiles, max) และหมวดหมู่ (count, unique, top, freq)
display(df.describe().T)
if cat_cols(df):
    display(df[cat_cols(df)].describe().T)
# ค่าที่ต่างจากปกติ: skew > 1 = เบ้ขวามาก (mean > median)
skew = df[num_cols(df)].skew().sort_values(ascending=False)
print("skewness:\n", skew.round(3).to_string())'''),
md(r"""
**✍️ คำตอบ §1:** ข้อมูลมี … แถว … คอลัมน์ (ตัวเลข … / หมวดหมู่ …) · ค่าว่างอยู่ที่ … (…%) · `…` มี mean … median … → เบ้ขวา/สมมาตร ·
target มีสัดส่วน … → สมดุล/ไม่สมดุล
"""),

md(r"""
## §2 Select Attributes (เลือก/ตัดคอลัมน์) + Set Role
- **Select** = เลือกเฉพาะคอลัมน์ที่ใช้ · **ตัด** = id, คอลัมน์ที่เป็นคำตอบล่วงหน้า (leak), คอลัมน์ซ้ำซ้อน, ค่าว่างเยอะ
- **Set Role** ใน Python = ตั้ง `id` เป็น index และแยก `X` (attributes) กับ `y` (label)
"""),
code(r'''KEEP_COLS = None                 # ✏️ list ของคอลัมน์ที่ "เก็บ" เช่น ["total_bill", "tip", "day"] · None = เก็บทั้งหมด
DROP_THESE = []                  # ✏️ list ของคอลัมน์ที่ "ตัด" เช่น ["size"]
BY_TYPE = None                   # ✏️ "number" = เก็บเฉพาะตัวเลข · "category" = เฉพาะหมวดหมู่ · None = ไม่กรองตามชนิด

sel = df.copy()
if KEEP_COLS is not None:
    sel = sel[[c for c in KEEP_COLS if c in sel.columns] + [c for c in [ID_COL, TARGET] if c and c in sel and c not in KEEP_COLS]]
sel = sel.drop(columns=[c for c in DROP_THESE if c in sel.columns])
if BY_TYPE == "number":
    sel = sel[[c for c in sel.columns if c in num_cols(sel) or c in (ID_COL, TARGET)]]
elif BY_TYPE == "category":
    sel = sel[[c for c in sel.columns if c in cat_cols(sel) or c in (ID_COL, TARGET)]]
print("คอลัมน์ก่อน:", df.shape[1], "→ หลัง:", sel.shape[1])
print("เหลือ:", list(sel.columns))

# ---- Set Role ----
roled = sel.set_index(ID_COL) if ID_COL and ID_COL in sel else sel
if TARGET and TARGET in roled:
    X_role, y_role = roled.drop(columns=[TARGET]), roled[TARGET]
    print(f"id = {ID_COL} (index) | label = {TARGET} | attributes = {list(X_role.columns)}")
display(roled.head())'''),
md(r"""**✍️ คำตอบ §2:** ตัด `…` เพราะเป็นรหัส (id) ไม่มีความหมายเชิงทำนาย / เป็นข้อมูลที่รู้หลังเกิดผล (leakage) / ซ้ำกับ `…` · ตั้ง `…` เป็น label"""),

md(r"""
## §3 Filter Examples (กรองแถว)
เขียนเงื่อนไขแบบ pandas `query` · ตัวอย่าง:
`"total_bill > 20"` · `"smoker == 'Yes' and day in ['Sat','Sun']"` · `"tip >= 2 or size > 4"` · `"`ชื่อมีเว้นวรรค` > 5"` (ชื่อคอลัมน์มีช่องว่างใช้ backtick)
"""),
code(r'''FILTER = "total_bill > 20 and smoker == 'Yes'"     # ✏️ เงื่อนไข
DROP_MISSING_ROWS_IN = []                          # ✏️ ตัดแถวที่คอลัมน์เหล่านี้ว่าง (= Filter: is not missing)

flt = df.query(FILTER) if FILTER else df.copy()
if DROP_MISSING_ROWS_IN:
    flt = flt.dropna(subset=DROP_MISSING_ROWS_IN)
print(f"แถวก่อนกรอง {len(df)} → หลังกรอง {len(flt)} ({len(flt)/len(df):.1%})")
display(flt.head())
# ตัวอย่างเงื่อนไขแบบอื่น (ไม่ใช้ query):
#   df[df["day"].isin(["Sat", "Sun"])]          df[df["total_bill"].between(10, 20)]
#   df[df["name"].str.contains("abc", na=False)] df[df["col"].isna()]  /  .notna()'''),
md(r"""**✍️ คำตอบ §3:** กรองเงื่อนไข `…` เหลือ … แถวจาก … แถว (…%)"""),

md(r"""
## §4 Concatenate / Append (ต่อแถว — ไฟล์คอลัมน์เดียวกัน เช่นข้อมูลคนละช่วงเวลา)
ต่อ `df` (ไฟล์หลัก) + `DATA_PATH_2` · ตรวจว่าคอลัมน์ตรงกัน · ใส่คอลัมน์ `source` บอกว่ามาจากไฟล์ไหน
"""),
code(r'''if DATA_PATH_2:
    df2 = load_data(DATA_PATH_2)
    only1, only2 = set(df.columns) - set(df2.columns), set(df2.columns) - set(df.columns)
    print("คอลัมน์ที่มีแค่ไฟล์ 1:", only1 or "-", "| มีแค่ไฟล์ 2:", only2 or "-")
    both = pd.concat([df.assign(source="file1"), df2.assign(source="file2")], ignore_index=True)
    print(f"ต่อแถว: {len(df)} + {len(df2)} = {len(both)} แถว | คอลัมน์ {both.shape[1]}")
    dup_id = both[ID_COL].duplicated().sum() if ID_COL and ID_COL in both else both.duplicated().sum()
    print("id/แถวซ้ำหลังต่อ:", int(dup_id), "(ถ้า > 0 พิจารณา both.drop_duplicates(...))")
    display(both["source"].value_counts())
    df = both.drop(columns="source")          # ✏️ ใช้ข้อมูลที่ต่อแล้วเป็น df หลักต่อจากนี้ (ไม่ต้องการ → comment บรรทัดนี้)
else:
    print("ไม่มี DATA_PATH_2 → ข้าม §4")'''),
md(r"""**✍️ คำตอบ §4:** ใช้ concatenate (append) เพราะสองไฟล์มีคอลัมน์เดียวกัน เป็นข้อมูลคนละช่วง → ได้ … แถว"""),

md(r"""
## §5 Join / Merge (เพิ่มคอลัมน์จากอีกตารางด้วย key)
| how | ผล | ใช้เมื่อ |
|---|---|---|
| `inner` | เฉพาะ key ที่มีทั้งสองตาราง | ต้องการเฉพาะแถวที่ข้อมูลครบ |
| `left` | ทุกแถวของตารางหลัก (ไม่เจอคู่ → NaN) | ห้ามแถวหลักหาย (นิยมสุด) |
| `outer` | ทุกแถวทั้งสองฝั่ง | ดูว่าอะไรไม่จับคู่ |
"""),
code(r'''if LOOKUP_PATH:
    lk = load_data(LOOKUP_PATH)
    lkey, rkey = (JOIN_KEY if isinstance(JOIN_KEY, tuple) else (JOIN_KEY, JOIN_KEY))
    print(f"ก่อน join: หลัก {df.shape} | lookup {lk.shape} | key ซ้ำใน lookup: {int(lk[rkey].duplicated().sum())}")
    joined = df.merge(lk, left_on=lkey, right_on=rkey, how=JOIN_HOW, indicator=True,
                      suffixes=("", "_lookup"))
    display(joined["_merge"].value_counts().rename({"both": "จับคู่ได้", "left_only": "มีแค่ตารางหลัก",
                                                    "right_only": "มีแค่ lookup"}))
    joined = joined.drop(columns="_merge")
    if rkey != lkey and rkey in joined:
        joined = joined.drop(columns=rkey)
    print(f"หลัง join ({JOIN_HOW}): {joined.shape}")
    display(joined.head())
    df = joined                                # ✏️ ใช้ผล join เป็น df หลักต่อจากนี้
else:
    print("ไม่มี LOOKUP_PATH → ข้าม §5")'''),
md(r"""**✍️ คำตอบ §5:** join แบบ `…` ด้วย key `…` เพราะ … (ต้องเก็บทุกแถวของตารางหลัก / เอาเฉพาะที่ตรงกัน) · ก่อน … แถว × … คอลัมน์ → หลัง … × … · จับคู่ไม่ได้ … แถว"""),

md(r"""
## §6 Aggregate / Group by
สรุปตามกลุ่ม: count, mean, sum, min, max, median, std
"""),
code(r'''GROUP_BY = ["day"]                                    # ✏️ จัดกลุ่มตาม (1 หรือหลายคอลัมน์)
AGG = {"total_bill": ["count", "mean", "sum"], "tip": ["mean", "max"]}   # ✏️ คอลัมน์: [ฟังก์ชัน]

agg = df.groupby(GROUP_BY).agg(AGG)
agg.columns = ["_".join(c) for c in agg.columns]       # ชื่อคอลัมน์แบบชั้นเดียว เช่น total_bill_mean
agg = agg.reset_index().sort_values(agg.columns[1], ascending=False)
display(agg)'''),
md(r"""**✍️ คำตอบ §6:** กลุ่ม `…` มีค่าเฉลี่ย `…` สูงสุด (…) ต่ำสุดคือ … (…)"""),

md(r"""
## §7 Pivot table / Crosstab
- `pivot_table` = แถว × คอลัมน์ × ค่า (aggregate) · `crosstab` = นับจำนวน/สัดส่วน 2 ตัวแปรหมวดหมู่
- **สัดส่วนของคลาสหนึ่ง** (เช่น % income >50K ตาม education × gender) → สร้างคอลัมน์ 0/1 แล้ว pivot ด้วย `mean`
"""),
code(r'''PIV_INDEX, PIV_COLUMNS, PIV_VALUES, PIV_FUNC = "day", "time", "tip", "mean"   # ✏️ แถว, คอลัมน์, ค่า, ฟังก์ชัน (mean/sum/count/max)
RATE_OF = None                 # ✏️ หา "สัดส่วน" ของคลาส เช่น ("income", ">50K") → ใช้แทน PIV_VALUES · None = ไม่ใช้

data_p = df.copy()
values = PIV_VALUES
if RATE_OF:
    data_p["_rate"] = (data_p[RATE_OF[0]].astype(str) == str(RATE_OF[1])).astype(int)
    values, PIV_FUNC = "_rate", "mean"
pv = pd.pivot_table(data_p, index=PIV_INDEX, columns=PIV_COLUMNS, values=values, aggfunc=PIV_FUNC,
                    margins=True, margins_name="All")
display(pv.round(4))

# crosstab: จำนวน + สัดส่วนตามแถว (แต่ละแถวรวม = 1)
display(pd.crosstab(df[PIV_INDEX], df[PIV_COLUMNS], margins=True))
display(pd.crosstab(df[PIV_INDEX], df[PIV_COLUMNS], normalize="index").round(3))
# pivot กลับ (wide → long): pv.reset_index().melt(id_vars=PIV_INDEX)'''),
md(r"""**✍️ คำตอบ §7:** จาก pivot `…` × `…` ค่า `…` สูงสุดที่ … = … ต่ำสุดที่ … = … → แสดงว่า …"""),

md(r"""
## §8 Generate Attributes (สร้างคอลัมน์ใหม่) + แปลงชนิด
"""),
code(r'''# ✏️ แก้/เพิ่มสูตรตามโจทย์
df["tip_pct"] = df["tip"] / df["total_bill"] * 100                          # คำนวณจากคอลัมน์อื่น
df["big_bill"] = np.where(df["total_bill"] > df["total_bill"].median(), "Yes", "No")   # if-else
df["bill_level"] = pd.cut(df["total_bill"], bins=[0, 15, 30, np.inf], labels=["low", "mid", "high"])  # แบ่งช่วง
# df["date"] = pd.to_datetime(df["date"]); df["month"] = df["date"].dt.month   # วันที่
# df["col"] = df["col"].astype(float)  /  .astype(str)                       # แปลงชนิด
# df = df.rename(columns={"old": "new"})                                     # เปลี่ยนชื่อ
display(df.head())'''),

md(r"""
## §9 กราฟพื้นฐาน + ตีความ
| อยากดู | กราฟ |
|---|---|
| การกระจายของตัวเลข 1 ตัว | histogram (+KDE) / boxplot |
| ตัวเลข เทียบระหว่างกลุ่ม | boxplot แยกกลุ่ม / bar ค่าเฉลี่ย |
| จำนวนในแต่ละหมวด / สัดส่วนคลาส | bar (countplot) / stacked bar |
| ความสัมพันธ์ตัวเลข 2 ตัว | scatter (+สีตามคลาส) |
| ความสัมพันธ์หลายตัวพร้อมกัน | correlation heatmap / pairplot |
| แนวโน้มตามเวลา | line |
"""),
code(r'''NUM_COL = "total_bill"   # ✏️ ตัวเลขที่จะดูการกระจาย
CAT_COL = "day"          # ✏️ หมวดหมู่ที่จะแยกกลุ่ม
X_COL, Y_COL = "total_bill", "tip"   # ✏️ scatter
HUE = "smoker"           # ✏️ ระบายสีตาม (เช่น label) · None ได้

fig, ax = plt.subplots(2, 2, figsize=(12, 8))
sns.histplot(df[NUM_COL], kde=True, ax=ax[0, 0]); ax[0, 0].set_title(f"Histogram of {NUM_COL}")
ax[0, 0].axvline(df[NUM_COL].mean(), color="r", ls="--", label="mean"); ax[0, 0].axvline(df[NUM_COL].median(), color="g", ls=":", label="median"); ax[0, 0].legend()
sns.boxplot(data=df, x=CAT_COL, y=NUM_COL, ax=ax[0, 1]); ax[0, 1].set_title(f"{NUM_COL} by {CAT_COL}")
sns.countplot(data=df, x=CAT_COL, hue=HUE, ax=ax[1, 0]); ax[1, 0].set_title(f"Count of {CAT_COL}" + (f" by {HUE}" if HUE else ""))
sns.scatterplot(data=df, x=X_COL, y=Y_COL, hue=HUE, ax=ax[1, 1]); ax[1, 1].set_title(f"{Y_COL} vs {X_COL}")
plt.tight_layout(); plt.show()

q1, q3 = df[NUM_COL].quantile([.25, .75]); iqr = q3 - q1
n_out = int(((df[NUM_COL] < q1 - 1.5 * iqr) | (df[NUM_COL] > q3 + 1.5 * iqr)).sum())
print(f"✍️ {NUM_COL}: mean={df[NUM_COL].mean():.2f} median={df[NUM_COL].median():.2f} skew={df[NUM_COL].skew():.2f} "
      f"→ {'เบ้ขวา (หางยาวด้านค่ามาก)' if df[NUM_COL].skew() > 0.5 else 'เบ้ซ้าย' if df[NUM_COL].skew() < -0.5 else 'ค่อนข้างสมมาตร'} · outlier (IQR) {n_out} ค่า")
print("✍️ ค่ากลางตามกลุ่ม:", df.groupby(CAT_COL)[NUM_COL].median().round(2).to_dict())
print(f"✍️ correlation({X_COL}, {Y_COL}) = {df[X_COL].corr(df[Y_COL]):.3f}")'''),
code(r'''# สัดส่วนคลาสในแต่ละกลุ่ม (stacked bar 100%) — เหมาะกับ "สัดส่วน label ตามหมวด"
STACK_GROUP, STACK_CLASS = "day", "smoker"     # ✏️ กลุ่ม (แกน x), คลาสที่จะดูสัดส่วน
ct = pd.crosstab(df[STACK_GROUP], df[STACK_CLASS], normalize="index")
ct.plot(kind="bar", stacked=True, figsize=(7, 4), colormap="tab20c"); plt.ylabel("proportion")
plt.title(f"{STACK_CLASS} proportion by {STACK_GROUP}"); plt.legend(bbox_to_anchor=(1, 1)); plt.tight_layout(); plt.show()
display(ct.round(3))

# bar ค่าเฉลี่ยตามกลุ่ม (เรียงมาก → น้อย)
df.groupby(STACK_GROUP)[NUM_COL].mean().sort_values(ascending=False).plot(kind="bar", figsize=(6, 3.5), title=f"mean {NUM_COL} by {STACK_GROUP}")
plt.tight_layout(); plt.show()'''),
md(r"""
## §10 Correlation heatmap (+ คู่ที่สัมพันธ์สูง)
r ใกล้ ±1 = สัมพันธ์เชิงเส้นแรง · |r| < 0.3 อ่อน · **correlation ≠ causation** และวัดแค่เชิงเส้น · คู่ predictor ที่ |r| สูง = multicollinearity
"""),
code(r'''corr = df[[c for c in num_cols(df) if c != ID_COL]].corr()     # ไม่เอา id
plt.figure(figsize=(1 + 0.7 * len(corr), 0.6 * len(corr) + 1))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1); plt.title("Correlation matrix"); plt.show()

pairs = corr.where(np.triu(np.ones(corr.shape, dtype=bool), k=1)).stack().rename("r").reset_index()
pairs.columns = ["var1", "var2", "r"]
pairs["|r|"] = pairs["r"].abs()
print("คู่ที่สัมพันธ์กันมากที่สุด:"); display(pairs.sort_values("|r|", ascending=False).head(8))
if TARGET in corr:
    tc = corr[TARGET].drop(TARGET).sort_values(key=abs, ascending=False)
    print(f"✍️ ตัวแปรที่สัมพันธ์กับ {TARGET} มากสุด: " + ", ".join(f"{k} (r={v:.3f})" for k, v in tc.head(3).items()))
# pairplot (ช้าถ้าคอลัมน์เยอะ): sns.pairplot(df, vars=num_cols(df)[:4], hue=HUE); plt.show()'''),
md(r"""**✍️ คำตอบ §9–10:** กราฟ … แสดงว่า … (บอกรูปร่าง/ค่ากลาง/การกระจาย/outlier หรือความต่างระหว่างกลุ่ม) · ตัวแปร … สัมพันธ์กับ … มากสุด (r = …) เชิงบวก/ลบ แต่ไม่ได้แปลว่าเป็นสาเหตุ"""),

md(r"""## §11 Save ผลลัพธ์ (ถ้าโจทย์ให้ส่งไฟล์)"""),
code(r'''OUT_PATH = "t01_result.csv"     # ✏️ ชื่อไฟล์ผลลัพธ์
df.to_csv(OUT_PATH, index=False)
print("saved", OUT_PATH, df.shape)'''),
]

if __name__ == "__main__":
    build("../T01_data_handling_viz.ipynb", TITLE, CONFIG, S)
