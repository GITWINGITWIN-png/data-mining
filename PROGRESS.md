# PROGRESS — Data Mining course

---

# Final Study Vault (folder `final/obsidian/`, `final/mock_lab/`) — เตรียมสอบ Final

## Exams (จาก `final/69_1_Guideline.pdf`)
- **Lab:** จ. 12 ต.ค. 2569 09:00–12:00 E11-S603 · โน้ตบุ๊กตัวเอง · RapidMiner หรือ Python ตามโจทย์
- **Lecture:** จ. 19 ต.ค. 2569 16:00–19:00 E11-S603 · 6 หมวด

## Status
- ✅ **ชุด Lab เสร็จ (2026-10-07):** `final/obsidian/lab/LAB 00–09` (hub · setup · data handling · preprocessing ·
  workflow/baseline/eval · supervised · clustering/association · reading results · mock guide · cheat sheet)
- ✅ **โจทย์ฝึกทีละขั้น 9 ชุด (2026-10-10):** `final/obsidian/practice/PR 00–09` — ไกด์ Python 9 + RapidMiner 9
  ข้อมูลใหม่จากภายนอกใน `final/practice/data/` (tips, penguins, breast cancer, wine, pima, heart, insurance, groceries)
  ไกด์ Python สร้างโดยรันโค้ดจริง (`final/practice/guidegen.py`, `py_guides_a/b.py`) · ไกด์ RM จาก process เฉลยที่รัน batch จริง
  (`rm_guides.py` → `rm/P0X_solution.rmp` + `rm/out/` → `rm_guides_md.py`)
  + ภาพ canvas mermaid หลังทุกขั้น (60 ภาพ) จาก `.rmp` จริง ด้วย `rm_diagrams.py` (กำหนดว่าขั้นไหนเพิ่ม operator อะไรใน `STEPS`) · ตรวจ render ด้วย mermaid-cli ผ่านครบ
  Findings ใหม่: **H2O Logistic Regression ตัดที่ threshold F1-max ไม่ใช่ 0.5** · SMOTE Upsampling ports `exa`/`ups` ·
  Operator Toolbox ติดตั้งแล้ว (smote recipe ผ่าน) · Filter Examples list format `attr.equals.val` / `attr.ge.4` / `attr.is_not_missing.`
- ✅ Mock lab 3 ชุด `final/mock_lab/mock{1,2,3}_*` — question.ipynb / solution.ipynb (executed) / solution*.rmp (batch-run)
- ✅ RapidMiner recipes 12 ไฟล์ `final/mock_lab/recipes/` (11 batch-run ผ่าน · SMOTE ต้องมี Operator Toolbox)
- ✅ **ชุด Lecture เสร็จ (2026-10-07):** `final/obsidian/lecture/LEC 00–13` (hub · EDA · preprocessing+leakage · PCA ·
  imbalanced · evaluation · KNN · lin/logistic · tree/RF · clustering · association · formula · glossary · drills)
  ตัวเลขยืนยันด้วย `final/obsidian/scripts/lec_numbers.py` · ภาพ 12 ภาพจาก `figs_lecture.py` · ลิงก์ 0 เสีย (24 โน้ต)
- ⏳ ผู้ใช้ต้องติดตั้ง **Operator Toolbox** ใน AI Studio เอง (Marketplace) แล้วรัน smote recipe

## Decisions (ผู้ใช้เลือก 7 ต.ค.)
Lab notes ต้องใช้ได้ทั้ง open-file และ closed-book · Python = RapidMiner น้ำหนักเท่ากัน · มี mock notebook ·
Lecture ไม่รู้รูปแบบ → drill ทุกแบบ · 4–5 ชม./วัน · **ไม่ commit git** (ไฟล์ untracked; commit ลง main ทีหลัง)

## Toolchain
- Python env สอบ: `final/.venv` (uv, CPython 3.14, pandas 3.0.6, sklearn 1.9.1, imblearn 0.14.2, mlxtend 0.25) +
  kernel `dm-exam` · โค้ดในโน้ตทดสอบด้วย `final/obsidian/scripts/run_snippets.py [--show] <notes>`
- ลิงก์: `final/obsidian/scripts/check_links.py` (wikilink + #anchor + ภาพ ทั้ง vault)
- RapidMiner batch: `bash final/mock_lab/run_rm.sh <files>` — **ต้อง Java 17** (CommandLineLauncher เรียก
  setSecurityManager; Java 21 ห้าม, 25 ลบ) + copy ไป path ไม่มีช่องว่าง (สคริปต์ใช้ eval) · GUI ใช้ Java 25 ได้
- .rmp สร้างด้วย `final/mock_lab/rm_builder.py` · operator class: core / `concurrency:` (cross_validation,
  optimize_parameters_grid, parallel_decision_tree, parallel_random_forest, k_means, fp_growth, join) /
  `blending:pivot` / `h2o:logistic_regression` · ชื่อ operator ต้องไม่ซ้ำทั้ง process
- ข้อมูลจากสไลด์: `final/data/make_slide_datasets.py` (utilities, riding_mowers(+probs), weather, tid_cheat)

## Findings ที่ใช้ในโน้ต (ยืนยันด้วยการรันจริง)
- RapidMiner Normalize z ใช้ n−1 (ตรงกับสไลด์ clustering p.30) · sklearn ใช้ n
- Linear Regression default feature selection = M5 prime · Decision Tree default = gain_ratio
- Cluster Distance Performance: avg within centroid distance (= WCSS/n) และ Davies Bouldin แสดง **ติดลบ**;
  ค่าใน Log ใช้ value `avg_within_distance` (บวก)
- positive class: ใช้ `manually_set_positive_class` ใน Performance (Binominal) — `Set Positive Value` ไม่มีผล
- Nominal to Binominal ต้อง `transform_binominal` ก่อน FP-Growth · Excel column "Trans. " RapidMiner ตัดช่องว่างเอง
- write_as_text ของ AssociationRules ตัดผล ("... N other rules ...")
- sklearn 1.9: `LogisticRegression(penalty=)` deprecated · pandas 3: dtype `str`, ใช้ `select_dtypes(exclude="number")`,
  `.values` read-only
- สไลด์ผิด (ใช้เป็น drill "หาที่ผิด"): Tree p.41 Gini (ที่ถูก 0.408/0.320/0.371), KNN p.36 typo, KNN p.42 ลืม k=12,
  KNN p.70 "11 records", Imbalanced p.20–21 SMOTE ก่อน CV, KNN p.51/p.56 leakage, Data p.21 d(x1,x3)=2.24

---

# HW10 (folder `HW10/`): Tree-based Classification — hand exercises

## Status: ✅ Complete (2026-09-19) — minimum scope, `.docx`, matches original worksheet styling
| File | Content |
|---|---|
| `6710503739_HW#10.docx` | `65_2_Excercise_Eng.pdf` reproduced to match the source formatting exactly — Times New Roman, black text throughout, no colored headings, plain bordered tables (both data tables in full), underline preserved where the original had it — with **Answer:** blocks placed directly under each (a)/(b) part — Ex1 feature selection (Information Gain by hand for Gender/CarType/ShirtSize + why not Customer ID), Ex2 ID3 decision tree on the Buy-Computer data + prediction for the new example |

## Key results
- **Ex1(a):** CarType has by far the highest Information Gain (0.620 bits) vs. Gender (0.029) and
  ShirtSize (0.012) — best predictor of Class.
- **Ex1(b):** Customer ID gives 20 pure singleton branches (entropy 0, apparent max gain) but doesn't
  generalize — classic high-cardinality overfitting trap, must be excluded as a split candidate.
- **Ex2(a):** Root split = age (gain 0.246, highest vs. income 0.029/student 0.151/credit_rating 0.048).
  age≤30 branch splits perfectly on student; age>40 branch splits perfectly on credit_rating; age 31–40
  is a pure "yes" leaf.
- **Ex2(b):** New example (age≤30, income=medium, student=yes, credit_rating=fair) → follows
  age≤30 → student=yes → **buy = YES**.

## Toolchain note
Built directly with the `docx` npm package (Node/docx-js) rather than notebooks — no dataset/plots
needed, just worked calculations and text. `docx` isn't globally installed on this machine; installed
into the session scratchpad (`npm install docx`) rather than the repo. Verified by converting to PDF
via the skill's `soffice.py` + `pdftoppm` and visually checking both pages before copying into `HW10/`.

---

# HW9 (folder `HW9/`): K-Means — step-by-step exercise + Cereals lab

## Status: ✅ Complete and verified (2026-09-13) — minimum-requirement scope, answers only
| File | Content |
|---|---|
| `6710503739_HW#9_K-Mean.ipynb` / `.pdf` | Exercise I (`Excercise_K-Mean_60_2.pdf`): 9 points, seeds A1/A4/A7, members + centroid + plot per iteration (4 pp) |
| `6710503739_creal.ipynb` / `.pdf` | Cereals lab (`Cereals_Labsheet_66_2.pdf`), named per the sheet's `student_id_creal` (4 pp) |

## Key results
- **K-Mean:** converges after **3 iterations** (iteration 3 = no change).
  Final C1={A1,A3,A7,A9} (4.25, 8), C2={A4,A6,A8} (2.67, 3), C3={A2,A5} (9.5, 4.5).
- **Cereals:** this `.xls` has only 12 attributes (no mfr/type/weight/cups). `-1` in carbo/sugars
  means missing (Quaker_Oatmeal) → 3 cereals removed, 74 left. 9 nutrition attributes, Min-Max;
  dropped name, shelf, rating. **Best K = 6** (silhouette local peak 0.331, SSE elbow).
- **Healthy = clusters 3 (puffed/shredded wheat, 9) + 5 (bran, 3)** → 12 cereals; cluster 5 alone
  is too small for a different cereal every day. Cluster numbers are from `random_state=42`.
- **2026-09-13 (student edit):** the student trimmed `creal.ipynb` themselves (removed the SSE table,
  attribute-selection note, best-K note, `n` column and per-cluster stats from b). PDF was re-exported
  from their executed notebook **without re-running it**. Keep their wording and don't add prose back.

## Rebuild
Execute with `env -u VIRTUAL_ENV uv run --no-project --with pandas --with xlrd --with scikit-learn
--with matplotlib --with jupyter --with nbconvert --with ipykernel jupyter nbconvert --execute --inplace`;
PDF = copy to `nb.ipynb` (`#` in name), `--to latex`, inject `\newcounter{none}` after `\documentclass`,
xelatex x2 (pandoc from `pypandoc-binary`).

---

# HW#8 (folder `HW8/`): Association Rule Mining — 3 exercises

## Goal
Answer `HW8/HW#8.pdf` in full: (1) Apriori by hand on 6 transactions, (2) the same in Python,
(3) PEP customer-profiling case study on `HW8/bank-data.csv` (600 customers).

## Status: ✅ Complete and verified (2026-09-06)
| Deliverable | Content |
|---|---|
| `6710503739_HW#8_Exercise-1.ipynb` / `.pdf` | Hand calculation: C1→L1→C2→L2→C3→L3, C4 pruned. **11 frequent itemsets**, 3 strong rules with support/confidence/lift. |
| `6710503739_HW#8_Exercise-2.ipynb` / `.pdf` | mlxtend Apriori on the same 6 transactions — matches Ex1 exactly (11 itemsets, 12 strong rules). |
| `6710503739_HW#8_Exercise-3.ipynb` / `.pdf` | Full A1–A4 + B1–B4 case study, 15 pages. |

## Key results (all verified against executed output)
- **Ex1/Ex2:** every strong rule has **lift = 1.0** — G and J are in all 6 transactions, so the
  items are statistically independent. This is the correct finding, not a bug; don't "fix" it.
- **Ex3 preprocessing:** kept 8 attributes (age, income, married, children, car, save_act,
  mortgage, pep); dropped `id` (600 unique), `sex` (exactly 50/50), `region` (fragments support),
  `current_act` (75.8% YES, near-constant). Equal-frequency tertiles for age/income (income is
  right-skewed, so equal-width would empty the HIGH bin); domain bins for children (0 / 1-2 / 3+).
  → 19 binary items, 600 transactions.
- **Ex3 parameters:** min_support 0.10, min_confidence 0.70 → 413 itemsets, 215 rules,
  26 of them predicting pep. Base rate pep_YES = 0.4567.
- **Ex3 headline rules:**
  `children_1-2 & income_HIGH → pep_YES` (sup 0.1450, conf 0.9255, **lift 2.0267**) and
  `children_0 & married_YES → pep_NO` (sup 0.2350, conf 0.7833, lift 1.4417).

## Toolchain note (this repo's `.venv` is broken — `.venv/bin/python3` does not exist)
Everything ran through `uv`, never the venv:
```
env -u VIRTUAL_ENV uv run --no-project --with pandas --with mlxtend --with jupyter \
    --with nbconvert --with ipykernel jupyter nbconvert --to notebook --execute --inplace <nb>
```
**PDF export needs two workarounds** (see the helper used, reproduced below):
1. `pandoc` is not installed system-wide → get it from the `pypandoc-binary` wheel and put its
   directory on `PATH`.
2. nbconvert + pandoc 3.x emits `longtable` captions that need a `none` counter the template
   lacks → `! LaTeX Error: No counter 'none' defined.` Fix: convert `--to latex`, inject
   `\newcounter{none}` after `\documentclass`, then run `xelatex` twice.
3. XeLaTeX (Latin Modern) **silently drops** ✓ ✗ ✅ ⇒ ≥ ≤ ∉ ∅ ≈ — they vanish from the PDF with
   no error. Markdown cells use ASCII equivalents instead. `— – → ×` do render fine.
4. **Grid tables:** pandoc emits booktabs longtables (horizontal rules only, no vertical lines),
   which do not match the notebook's look. A `gridify.py` pass rewrites each longtable to
   `{|l|l|}` / `{|p{}|p{}|}` and `\hline` on every row. Two gotchas: subtract
   `n+1 \arrayrulewidth` from the `p{}` widths or wide tables overflow, and leave pandoc's
   `\bottomrule` in `\endlastfoot` rather than ruling the last row — longtable can break between
   the final row and its `\hline`, orphaning a stray rule at the top of the next page.

**2026-09-06 (2nd pass, on the student's instruction):** all `**bold**` / `*italic*` emphasis was
stripped from every markdown cell (84 + 0 + 72 markers) and the tables re-rendered as grids.
The student had already rewritten/trimmed the markdown themselves — wording and content are
theirs, deliberately kept as-is (including typos like "dept"). Do not re-add emphasis or prose.

---

# W10 (folder `W10/`): BeautyCo — Association Rules / Market Basket Analysis

## Goal
Lab sheet `69_1_Cosmetics_Lab_Sheet_Eng.pdf` on `BeautyCo_68.xls`: answer "which products are
most frequently purchased together?" via FP-Growth (min support 0.2) → association rules
(min confidence 0.7). Scope was deliberately **minimum requirement only**.

## Status: ✅ Complete and verified (2026-08-31)
Both required deliverables exist and are visually checked:
- `W10/Cosmetic_6710503739.ipynb` — coding, executed end-to-end, no errors
- `W10/Cosmetic_6710503739.pdf` — answers to questions 3-4-5 (2 pages, XeLaTeX)
- `W10/Cosmetic_6710503739.tex` — source for the PDF

**Deliberately minimal on the student's instruction:** the PDF carries the bare answers only
(no extended interpretation), and the notebook is program output plus one-line explanations,
**with no code comments**. Do not "improve" either by adding prose back.

## Data
1,000 transactions × 14 binary product columns, no missing values. `Trans.` is the ID
(header has a **trailing space** — must `.strip()` the columns or the drop fails).
Mean basket = 4.39 items.

## The answers (all recomputed from raw baskets and matched against mlxtend)
- **Q3 row meaning**: one customer's basket; 1,000 baskets over 14 products.
- **Q3 most-bought-together**: `Base_Makeup+Glossy_Lips` support 0.356 but lift only 1.36
  (both individually popular → co-occur by chance); `Eye_Enhancer+Eye_Palette` support 0.321
  with lift 2.36 is the genuinely related pair.
- **Q3 unexpected**: `Nail_Art+Makeup_Tools` lift **3.57** — strongest association in the data,
  but support 0.149 < 0.2 so FP-Growth never sees it. Also `Lip_Liner+Base_Makeup` lift 0.69
  (negative association).
- **Q4 frequent itemsets**: **23** (11 singletons + 12 pairs). Nothing of size ≥3 reaches 0.2,
  so only 1→1 rules are possible. Dropped below threshold: Makeup_Tools (.149),
  Travel_Pouch (.054), Brow_Definer (.042).
- **Q4 maximal**: **16 of 23** — all 12 pairs + 4 singletons that pair with nothing
  (Lip_Color, Nail_Art, Contouring, Lip_Liner → standalone products, not bundle candidates).
- **Q5 rules at conf ≥ 0.7**: only **3**. Highest confidence =
  `Eye_Enhancer → Eye_Palette`: **support 0.321, confidence 0.899, lift 2.36**
  (321/1000, 321/357, 0.899/0.381). Reverse rule also valid (conf 0.843) → bidirectional.
- **Q5 marketing**: "Eye Look Set" bundle; eye-look tutorials for TikTok/Shopee Live;
  cart cross-sell trigger; retarget the 36 mascara buyers who skipped the palette;
  trial the hidden `Nail_Art+Makeup_Tools` bundle.

## Environment (important)
`.venv` is still unusable — everything ran through:
`env -u VIRTUAL_ENV uv run --no-project --with pandas --with xlrd --with mlxtend ...`
`xlrd` is required to read the legacy `.xls`. FP-Growth via **mlxtend**
(`fpgrowth` + `association_rules`), which is the Python equivalent of the RapidMiner operators.

## Rebuild
```bash
cd W10
env -u VIRTUAL_ENV uv run --no-project --with pandas --with xlrd --with mlxtend \
  --with jupyter --with ipykernel --with nbconvert \
  jupyter nbconvert --to notebook --execute --inplace Cosmetic_6710503739.ipynb
xelatex -interaction=nonstopmode Cosmetic_6710503739.tex   # run in W10/, then rm *.aux *.log
```

## Not done (out of scope — "minimum requirement" only)
- No RapidMiner `.xml` process (the lab accepts *either* `.xml` **or** `.ipynb`; the notebook satisfies it).
- No support-bar chart / plots in the notebook (trimmed out; tables carry the answers).
- No extra sensitivity analysis at lower support thresholds, though the `Nail_Art+Makeup_Tools`
  finding suggests support 0.1 would be an interesting follow-up.

---

# Group Assignment #1: Mini DW & Dashboard — "ElderCare Insight" (นับเป็นงานกลุ่ม 3 คน)

## Goal
Answer `group project/69-1-Mini DW & Dashboard-1.pdf` — build a full pipeline from raw
data → ETL → star-schema DW → interactive dashboard, on a business case of our choice.
Chosen domain: **ธุรกิจสถานดูแลผู้สูงอายุ** using **CMS Nursing Homes** open data (US SNFs).
Deliverables per brief: PDF report 10–15 pages + 8–15 min video + a Google Drive folder
`GroupXX_ProjectName/{01_Raw_Data,02_ETL,03_Data_Warehouse,04_Dashboard,05_AI_Usage_Log}`.

## Status: 🟡 Design document complete — ETL/dashboard NOT started (2026-08-12)
User explicitly scoped this session to **planning only** ("แค่วางแผน จัดการ grain ตั้งคำถาม
วางแผนเรื่อง star schema เขียนลงใน latex file ก่อน"), then asked to rebuild it with the
`study-guide` skill and to spell out the data sources.

- **`group project/Group01_ElderCareDW/06_Report/eldercare_dw_design.tex`** → 33-page A4 PDF,
  XeLaTeX, **0 errors, 0 missing glyphs, 0 overfull >15pt**. All 6 TikZ figures visually
  verified via `pdftoppm`.
- Built with the **study-guide skill** conventions: Laksaman/Garuda dual-script fonts,
  4 semantic colours (src/etl/dw/dash, Okabe–Ito), 4 fixed callout boxes, `L{}` columns
  everywhere, bilingual glossary appendix, provenance footer.
- Rebuild: `cd "group project/Group01_ElderCareDW/06_Report" && latexmk -xelatex -outdir=build eldercare_dw_design.tex && cp build/eldercare_dw_design.pdf .`

## Spine (follows the data path, not theory order)
ภาค 1 ธุรกิจ+คำถาม → ภาค 2 แหล่งข้อมูล → ภาค 3 คุณภาพข้อมูล → ภาค 4 Grain+Star Schema
→ ภาค 5 ETL+Dashboard → ภาคผนวก (อภิธานศัพท์ / คอลัมน์ / คำสั่งตรวจสอบ / อ้างอิง)

## The design (the actual answer)
- **2 Fact tables** (brief gives bonus points; there is also a real reason):
  - `Fact_Facility_Monthly` — **periodic snapshot**, grain = 1 facility (CCN) × 1 CMS
    publication date. Measures: beds, avg residents/day, resident-days, nurse HPRD,
    turnover %, 4 star ratings, deficiency count, `is_suspect`.
  - `Fact_Penalty_Event` — **transaction**, grain = 1 penalty (one fine OR one payment
    denial) on 1 facility on 1 penalty date. Measures: fine_amount_usd,
    payment_denial_days, penalty_count.
  - **Why two:** ProviderInfo's `Total Amount of Fines in Dollars` is believed to be a
    ~3-year rolling total (⚠️ *unverified* — must check `NH_Data_Dictionary.pdf`), so it is
    semi-additive and cannot be summed across periods. BQ7 ("when do fines cluster") is
    unanswerable without a real transaction fact.
- **6 Dimensions** (5 conformed): `Dim_Date` (day grain, 1960–2027, role-playing),
  `Dim_Facility` (**SCD Type 2** — special_focus_status & abuse_icon flip over time),
  `Dim_Geography`, `Dim_Ownership`, `Dim_Chain`, `Dim_Penalty_Type`.
- **8 Business Questions**, **10 Measures** with additivity classified, **8 data-quality
  problem types** (brief needs 5 / 3 / 3).

## Data sources — verified by actually opening them
- **S1 CMS archived snapshots** (the "more complex than CSV" source): **88 monthly ZIPs,
  2019-01-17 → 2026-08-06**, ~38 MB each. Jun2026 ZIP = 20 files / 614 MB uncompressed.
  `NH_ProviderInfo` **14,695 × 99**, `NH_Penalties` **16,180 × 14**, `NH_SurveySummary`
  **43,952 × 41**, `NH_CitationDescriptions` 643 × 5, `NH_StateUSAverages` 54 × 51.
- **S2 CMS Provider Data API (JSON)** — the archived-data page is a JS SPA with no links in
  the HTML. The working endpoints (found by grepping the SPA bundle):
  - `…/api/1/archive/aggregate/theme/nursing-homes/relative` → all 96 archive entries
  - `…/api/1/metastore/schemas/dataset/items` → 234 datasets (11 nursing-home ones)
  - `…/api/1/datastore/query/4pq5-n9py/0?limit=1` → live rows, snake_case keys
- **S3 `FY_2026_SNF_VBP_Facility_Performance.csv`** — 13,900 × 49, different grain (fiscal
  year) → gives the incentive payment multiplier.
- **S4 Census ACS API** (pop 65+) — ⚠️ **first call returned empty, cause unknown**.
  Fallback for BQ1 is documented in the PDF.
- **S5** CMS lookup tables (citation descriptions, state averages).
- Test row for ETL: CCN `015009` = 57 beds / 51.6 residents → occupancy **90.5%**.

## Decisions taken (don't silently reverse)
- Download **quarterly**, not monthly (~28–31 snapshots vs 88) — ratings move slowly and
  88 × 38 MB ≈ 3.3 GB. Grain is declared "per snapshot", so adding more later needs no
  schema change.
- Only 6 of the 20 CSVs get extracted; `NH_HealthCitations` (165 MB) is left in the ZIP.
- Data-quality rule: **flag `is_suspect`, never delete rows** — becomes a dashboard filter.
- Planned stack: DuckDB (DW) + Streamlit/Plotly (dashboard). Neither installed yet.

## Toolchain notes (new, beyond earlier HW notes)
- `\\[2pt]` inside a `p{}`/`L{}` table cell **ends the row** — use `\newline` instead.
- `\caption*` needs the `caption` package or it prints a literal "Figure 1: *".
- `\mbox{}` around long identifiers causes overfull hboxes; the `underscore` package
  already gives break points at `_`, so let it break.
- TikZ `align=center` (the skill's `lbl`/`blk` styles) stretches Thai word gaps badly in
  wide nodes → use `align=flush left`.
- A 6-node ring diagram with a centre explanation box needs radius ≥ ~4.0 cm for 2.3 cm
  nodes, or the centre box overlaps the ±30° nodes.

## Remaining
- [ ] Verify the 3 open items the PDF lists: fine-total lookback period, 2019 schema drift,
      Census API failure, and whether `Fine ID` is unique across snapshots.
- [ ] Fill in group number + 3 member names on the cover page.
- [ ] Build ETL → DW → dashboard (nothing written yet).
- [ ] Condense ภาค 1–4 into the 10–15 page submitted report; record the 8–15 min video;
      keep an AI Usage Log (≥5 prompts) as the brief requires.

---

# HW7 (folder `HW7/`): KNN — car-theft prediction + KNN vs Logistic Regression on Titanic

Answers `HW7/KNN_Exercise_66_2.pdf`. Two notebooks + matching PDFs, named to the
submission scheme `Student_ID_HW#7_<n>.{ipynb,pdf}` (2026-08-30).

## Status: ✅ Complete — 4 deliverables, PDFs rendered and visually verified (2026-08-30)

| File | Content |
|---|---|
| `6710503739_HW#7_1.ipynb` / `.pdf` | Q1 — KNN on the 10-row car dataset (2 pp) |
| `6710503739_HW#7_2.ipynb` / `.pdf` | Q2 — KNN vs Logistic Regression on Titanic (4 pp) |

- **Q1** — Colour/Type/Origin one-hot encoded, KNN predicts **(Red, SUV, Domestic)**.
  **Answer: Stolen = No.**
  ⚠️ Key gotcha: **five** records tie at the minimum distance √2 (each differs by exactly
  one attribute — rows 0,1,2,7,8). `k=3` would return `Yes` purely because sklearn breaks
  the tie by row order and silently drops rows 7 and 8. The notebook uses **k=5** so all
  five equidistant neighbours vote → 3 No vs 2 Yes → **No**.
  On one-hot vectors Euclidean distance² = 2 × (mismatched attributes), so the only
  possible distances are √2 (1.414), 2.0 and √6 (2.449) — the tie is structural, not luck.
- **Q2** — uses the repo's existing `titanic_data.csv` (891 rows). Age→median,
  Embarked→mode, get_dummies(drop_first), 80/20 stratified split, StandardScaler fit on
  train only. **KNN (k=5) acc 0.82 / Survived-F1 0.74** vs **LogReg acc 0.80 / F1 0.72**.
  ~1pp on a 179-row test set ≈ 2 passengers, i.e. inside single-split noise.

### ⚠️ Known gap (user trimmed it, deliberately left alone)
The lab sheet's step 5 asks to *"Recommend the most suitable model"*. The current Q2
notebook ends at advantages/disadvantages — the recommendation paragraph was removed
during the bare-minimum trim. Add one line if marks depend on it.
(Also two typos in that section's markdown: "Adventages" / "Disaventage".)

## Rebuild
Notebooks are executed in Jupyter directly. PDFs are a straight nbconvert→XeLaTeX render
(no added content; only margins 2.2cm + paragraph spacing for legibility). `#` in the
filename is a LaTeX comment char, so the build copies to a temp name, compiles, renames:
`bash <scratchpad>/build_all.sh`  (pandoc comes from `--with pypandoc-binary`; no system pandoc)

---

# Midterm Study Vault (folder `midterm/obsidian/`) — คลังความรู้เตรียมสอบมิดเทอม

## Status: ✅ เสร็จสมบูรณ์ (2026-08-18)
Obsidian vault 13 โน้ต / ~39,600 คำ / 5,662 บรรทัด + ภาพประกอบ 13 ภาพ ครอบคลุม
สไลด์มิดเทอมทั้ง 8 ไฟล์ (443 หน้า) โดยยึด `midterm/guidline.txt` เป็น exam blueprint

## ⚠️ ข้อค้นพบสำคัญ: Syllabus ≠ guideline
Syllabus ระบุ Week 6–7 เป็น **Association Rule Mining** และ **Classification (Decision Trees, k-NN)**
แต่ `guidline.txt` **ไม่มีสองหัวข้อนี้เลย** — ใส่ **DW Design / Multi-Dim Design / ETL / Reporting /
Regression** แทน และในโฟลเดอร์ `midterm/` **ไม่มีสไลด์ Association Rules หรือ Decision Tree อยู่จริง**
→ ยืนยันว่าคอร์สปรับเนื้อหา จึง **ยึด guideline** ไม่ใช่ syllabus

## โครงสร้าง (`midterm/obsidian/`)
- `00 START HERE.md` — MOC: แผนที่เนื้อหา, หัวข้อ "ออกแน่" 3 ระดับ, แผนอ่าน 5 วัน, mermaid graph เชื่อมบท
- `01`–`09` — 9 บทตาม guideline 8 ข้อ (บท 02 Data Types เป็นบทฐานที่ guideline ไม่ระบุตรงแต่จำเป็น)
- `10 Formula Sheet.md` — สูตรทั้งหมดหน้าเดียว · `11 Glossary EN-TH.md` — ศัพท์ + 14 คู่ที่สับสนบ่อย
- `12 Exam Drills.md` — Part A ทฤษฎี / B คำนวณ / C ออกแบบ+SQL / D สถานการณ์ + 12 กับดัก
- `assets/` 13 PNG · `scripts/` 14 ไฟล์ Python (`_style.py` + fig01–fig13)

## ภาพประกอบ = reproducible ไม่ใช่ตกแต่ง
ทุกภาพสร้างจากสคริปต์ที่ **คำนวณตัวเลขจริง** แล้วเทียบกับสไลด์ ตัวอย่างผลที่ได้:
- `etl_fact_build.png` — ทำ ETL 4 ขั้นจาก `Sales_log` จริง → fact 10 แถว **ตัวเลขตรงสไลด์ทุกช่อง**
- `reg_ols_r2_overfit.png` — OLS ได้ b₁=8, b₀=21, SSE=10, SST=650, R²=0.9846 (ตัวเลขลงตัวสำหรับสอนคำนวณมือ)
- `prep_scaling.png` — พิสูจน์ว่า scaling **พลิกคำตอบ k-NN** ได้จริง (ค่าดิบตอบ C / หลัง scale ตอบ B)
- 🐛 **จับสไลด์พิมพ์ผิด:** `Data_69_1-3.pdf` p.21 พิมพ์ `d(x1,x3) = 5.1` แต่ที่ถูกคือ **2.24**
  (5.1 ถูกคัดลอกซ้ำมาจาก `d(x2,x3)`) — อีก 5 ช่องถูกต้องหมด บันทึกไว้ในบท 02 แล้ว

## รายละเอียดที่ต้องรู้เวลากลับมาแก้
- **ไม่มี matplotlib/numpy ในระบบ** และ `.venv` พัง → ต้องใช้ ephemeral env:
  ```bash
  cd "midterm/obsidian/scripts"
  env -u VIRTUAL_ENV uv run --quiet --no-project --with matplotlib --with numpy \
      --python 3.12 python fig01_analytics_types.py
  ```
  **`env -u VIRTUAL_ENV` จำเป็น** ไม่งั้น uv จะไปเจอ `.venv` ที่ symlink พังแล้ว error
- **ฟอนต์ไทยใน matplotlib:** DejaVu Sans ไม่มีอักขระไทย → `_style.py` ลงทะเบียน **Garuda**
  (`/usr/share/fonts/opentype/tlwg/`) แล้วตั้ง `font.family` เป็น **ลิสต์** `["Garuda","DejaVu Sans"]`
  เพื่อใช้ font fallback ต่ออักขระ + ตั้ง `axes.unicode_minus=False` (Garuda ไม่มี U+2212)
- **Wikilink ในตาราง markdown ต้อง escape เป็น `[[Note\|alias]]`** ไม่งั้นตารางแตก
- ตรวจลิงก์แล้ว: **wikilink 235 จุด + ภาพฝัง 13 จุด ชี้ถูกทุกอัน** (รวม anchor `#heading`)
- Mermaid 19 บล็อก — label ทุกตัวครอบ `"..."` เพื่อให้วงเล็บ/ไทยไม่ทำ parser พัง

---

# HW6 (folder `HW6/`): Tayko — Predicting software reselling profit (Spending)

## Goal
Answer `HW6/65_2_Tayko_Eng.pdf` using `HW6/Tayko.csv` (2000 × 28). Multiple linear regression
on **purchasers only** (`Purchase == 1` → 1000 rows), predicting `Spending`.
Scope per request: **minimum requirement only — answers, no exposition.**

## Status: ✅ Complete and verified (2026-08-16)
`HW6/6710503739_Tayko_Regression.ipynb` (+ `.pdf`) — **13 cells (6 code)**, executed
end-to-end, **0 errors**, 1 figure. Coefficients/p-values cross-checked against an
independent `statsmodels.OLS` fit (identical to 4 dp).

## PDF export
5 pages, 0 missing glyphs. `nbconvert --to pdf` needs two things this box lacks/breaks on:
pandoc (installed as `pypandoc_binary` into a scratch venv) and a fix for pandoc 3.9
markdown tables — they emit `\def\LTcaptype{none}`, and longtable then calls
`\refstepcounter{none}`, so **`\newcounter{none}` must be injected into the generated
`.tex`** before compiling (`\usepackage{caption}` does NOT fix it). Script kept at
`scratchpad/to_pdf.sh` (nbconvert --to latex → patch preamble → latexmk -xelatex).

## Environment (important)
Uses **only pandas / numpy / scipy / matplotlib** — deliberately: neither `.venv` nor
`HW5/.venv` has `statsmodels`, and the project `.venv` also lacks `sklearn`. OLS + p-values
come from a 10-line `ols()` helper (`np.linalg.lstsq` + `scipy.stats.t`) defined in the notebook.
Both venvs point at snap-confined interpreters (`/home/panguin/snap/code/{247,253}/…`) that are
**unrunnable outside VSCode**; this notebook was executed in a throwaway system-python venv,
then the kernelspec was restored to `.venv (3.14.4.final.0)`.

## The answers
- **Partition:** `t` = train (379 purchasers), `v` = test (377). `s` (244) is unused by the brief.
- **(a)** `Freq` vs Spending: positive, roughly linear, **r = 0.645** (variance widens with Freq).
  `last_update_days_ago`: weak negative, **r = −0.294** — barely linear.
- **(b2) Equation 1** `Spending = 39.34 + 92.65·Freq − 0.02511·last_update
  + 1.541·Web order + 4.305·Gender=male + 42.82·US − 92.83·Address_is_res` (train R² = 0.5042).
- **(b3)** High spenders = **frequent buyers, recently updated records, non-residential
  address**. Significant: Freq (p<0.001), last_update (p=0.003), Address_is_res (p<0.001).
  US is borderline (p=0.061).
- **(b4) Drop** `Web order` (p = 0.929) and `Gender=male` (p = 0.803); `US` next if needed.
- **(c1) Equation 2** (3 predictors) `Spending = 71.72 + 93.27·Freq − 0.02283·last_update
  − 92.36·Address_is_res` (train R² = 0.4993).
- **(c2)** First test record (seq 10): predicted **91.61**, actual **174** → error **+82.39**.
- **(c3) Test:** RMSE **162.33**, MAE **98.90**, ME **13.27**, R² **0.4564** —
  slightly better than model 1 (RMSE 164.50) with half the predictors.

## Remaining (student task)
- [ ] Export to PDF for submission if the course wants a PDF alongside the notebook.

---

# W8: Predicting MEDV — Multiple Linear Regression on the Boston dataset

## Goal
Answer `W8/69_1_Boston_Eng.pdf` using `W8/boston_r.csv` (506 × 14). Questions (a) EDA +
correlation heatmap, (b) two attributes most correlated with `medv`, (c) linear regression on
those two — 20 % hold-out, `StandardScaler`, regression equation, RMSE.
(d) is marked **[Extra-Points]** and was **deliberately skipped** — "minimum requirement only".

## Status: ✅ Complete and verified (2026-08-10)
`W8/6710503739_W8_Boston.ipynb` — **12 cells (7 code)**, runs end-to-end, **0 errors**,
1 figure. Every number quoted in the markdown was cross-checked against the executed output.

## Environment
Reuses **`HW5/.venv`** (the project-root `../.venv` is still broken — see the HW#6 notes).
Run: `cd W8 && env -u VIRTUAL_ENV PATH="../HW5/.venv/bin:/usr/bin:/bin" ../HW5/.venv/bin/python -m nbconvert --to notebook --execute --inplace 6710503739_W8_Boston.ipynb`

## The answers
- **(a)** Data is clean: 0 missing, 0 duplicates — no cleaning needed. 14×14 heatmap
  (`annot=True, fmt=".2f", cmap="coolwarm", center=0`).
- **(b)** **`lstat` (r = −0.7377)** and **`rm` (r = +0.6954)**. Next-best is `ptratio` at
  −0.5078, so the top two are well separated.
- **(c)** `random_state=42`, 404 train / 102 test. Scaler **fitted on train only**.
  - Standardised: `medv = 22.7965 − 4.4917·z_lstat + 3.8724·z_rm`
  - Original units: `medv = −3.8412 − 0.6325·lstat + 5.4651·rm`
  - **Test RMSE = 5.5896** (thousand $), R² = 0.5740. (Train RMSE 5.5129, R² 0.6502 —
    little gap, so the model is underfitting rather than overfitting.)

## If (d) Extra-Points is wanted later
Underfitting with only 2 features → the cheap wins are: all 13 features
(test RMSE ≈ 4.9), or polynomial/interaction terms on `lstat`+`rm` (`lstat` vs `medv` is
visibly curved), or a tree ensemble. Each needs the equation + RMSE reported the same way.

---

# HW#6: Pre-process the Adult Dataset (EDA + pre-processing for income prediction)

## Goal
Answer `HW5/Pre-process the Adult Dataset.pdf` + `HW5/Description.txt` on `HW5/adult.csv`
(48,842 × 15). Four phases: EDA → visual/outlier handling → imputation + encoding → scaling.
Deliver a notebook plus an English PDF report.

## Status: ✅ Complete — notebook trimmed to BARE MINIMUM on request (2026-08-09)
- `HW5/6710503739_hw#6_preprocess.ipynb` — **32 cells (16 code)**, down from 68 (34 code).
  **Runs end-to-end, 0 errors**, 2 figures. Output: `adult_preprocessed.csv`,
  **48,842 × 85**.
- `HW5/6710503739_hw#6_preprocess_answer.pdf` — **11 pages**, A4, XeLaTeX, 0 errors,
  0 font warnings. All 11 pages visually verified via `pdftoppm`. **Still the FULL version —
  not trimmed** (see the divergence warning below).
- Source: `HW5/hw6_preprocess_answer.tex` (safe name — `#` in a filename breaks the
  xelatex invocation, so only the *output* PDF carries the brief's literal `hw#6` name).
- `HW5/6710503739_hw6_preprocess.ipynb` (no `#`, 68 cells, outputs cleared) is a **user-made
  copy of the old full notebook** — left untouched.

## Bare-minimum trim (2026-08-09) — what was cut and what to restore first
Rule applied: a cell survives only if it answers a literal bullet of the brief.
**Cut:** duplicate detection + dedup · the capital-gain zoom figure · the missing-values bar
chart · per-label frequency proportions · the `>50K`-rate-by-capital-gain-band table · the
IQR outlier-count table · the "removal would cost 41.53 % of rows" calculation · the
missing-vs-present profile table (age / hours / %>50K) · `log1p` on capital-gain/loss · the
`capital-gain-topcoded` flag · the stratified train/test split · the Min-Max comparison ·
the scaling before/after figure · `report_stats.json` · the 3 CSV outputs (now one).

**Consequences of the trim (both are real, not bookkeeping):**
- No dedup → **48,842 rows** (52 duplicates retained); no top-code flag → **85 columns**.
  The full version produced 48,790 × 86.
- The outlier decision is now "KEEP" with justification only — no `log1p`, so
  `capital-gain` stays at skew 11.89 going into `StandardScaler`. The brief only asks to
  *state and justify* the decision, so this still answers it, but the pipeline is weaker.
- Scaler is now fitted on the whole dataset (no split) → would leak into a later test set.

**If marks come back short, restore in this order:** (1) `log1p` + the top-code flag,
(2) the train/test split before scaling, (3) the capital-gain band table (it is the evidence
that the outliers are real signal), (4) the IQR removal-cost calculation.

## ⚠️ Notebook and PDF now disagree — resolve before submitting
The PDF was **not** trimmed, so it describes work the notebook no longer does:
- PDF says **48,790 × 86**; notebook now yields **48,842 × 85**. *(direct contradiction)*
- PDF §2.3 / §4.1 describe `log1p` + the `capital-gain-topcoded` flag — both gone.
- PDF §4.2 describes a 39,032 / 9,758 stratified split — gone.
- PDF cites `adult_train_preprocessed.csv` etc.; the notebook now writes `adult_preprocessed.csv`.
- PDF Figures 2, 4, 5 (`hist_capgain_zoom`, `missing_bar`, `scaling_compare`) are no longer
  regenerated. **The PNGs are still on disk, so the PDF rebuilds fine** — but a clean
  `figures/` would break it.
- PDF phrases like "asserted in the notebook" / "the notebook checked whether…" no longer hold.

Either trim `hw6_preprocess_answer.tex` to match, or go back to the full version — a
complete copy survives as **`HW5/6710503739_hw6_preprocess.ipynb`** (no `#`, 68 cells,
outputs cleared); execute it to regenerate all 5 figures, `report_stats.json` and the 3 CSVs,
and the PDF is then accurate again.

## Environment (important — differs from earlier HWs)
- The project-root `../.venv` is **still broken** (snap-confined, dead `python3` symlink) and
  `VIRTUAL_ENV` is exported into every shell, which makes plain `uv run` fail. Workarounds:
  prefix commands with `env -u VIRTUAL_ENV`, and set an explicit `PATH` when calling nbconvert
  (otherwise it resolves `jupyter` from the broken root venv).
- Created a **dedicated `HW5/.venv`** (uv, Python 3.12.13) — pandas 3.0.5, numpy, matplotlib,
  seaborn, scikit-learn 1.9.0, jupyter. Non-destructive: the broken root venv was left alone.
- `HW5/.gitignore` excludes `.venv/` and LaTeX aux files.
- Re-run notebook:
  `env -u VIRTUAL_ENV PATH="$PWD/.venv/bin:/usr/bin:/bin" ./.venv/bin/python -m nbconvert --to notebook --execute --inplace "6710503739_hw#6_preprocess.ipynb"`
- Rebuild PDF: `cd HW5 && xelatex -interaction=nonstopmode hw6_preprocess_answer.tex` (twice).

## Reproducibility mechanism (reusable idea)
The notebook accumulates every headline number into a `stats` dict and writes
`HW5/report_stats.json`; the LaTeX report quotes only those values. This caught **five**
narrative claims that were wrong on the first pass (see below) — worth repeating on future HWs.

## Key findings / decisions (the actual answer)
- **Hidden missing values:** pandas reports 0 NaN because gaps are the literal `?`.
  Real counts: `occupation` 2,809 (5.75 %), `workclass` 2,799 (5.73 %), `native-country` 857
  (1.75 %); 3,620 rows (7.41 %) affected. 52 exact duplicate rows.
- **Missingness is structural, not random:** 2,799 of the 2,809 `occupation` gaps coincide
  with a missing `workclass`; the other 10 are all `Never-worked`. That group is older (40.2
  vs 38.6), works 31.8 vs 41.0 h/week, and earns >50K at 9.5 % vs 24.8 %.
  → **`workclass`/`occupation` imputed as an explicit `"Unknown"` category** (mode imputation
  would fabricate jobs for 2,795 retired/unemployed people and erase real signal);
  **`native-country` → mode** `United-States` (91.4 % of known values, no structural story).
- **`education` ⇄ `educational-num` is a verified perfect 1:1 mapping** → dropped `education`.
  Proven by rebuilding the ordinal code with `OrdinalEncoder` + explicit rank order; it
  reproduces `educational-num` on all 48,790 rows.
- **Outliers: KEEP, don't remove.** 1.5×IQR flags **41.53 % of the whole dataset** (20,284
  rows) across all numeric columns — `hours-per-week` alone flags 27.63 % because its IQR is
  5 hours. Removal would also delete nearly every high earner.
  - `capital-gain`: skew **+11.89**, 91.74 % zeros, **244 rows top-coded at exactly 99,999**
    (largest real value below it: 41,310). >50K rate by band: 20.5 % / 17.9 % / 88.7 % /
    92.7 % / **100 %** — non-monotonic at the bottom, then very strong.
  - Treatment: `log1p` + a new `capital-gain-topcoded` binary flag. `age` kept untransformed.
- **Encoding:** ordinal (`educational-num`), binary 0/1 (`gender`, `income`), one-hot with
  `drop_first=True` for 6 nominal columns → **15 → 86 columns**.
- **Scaling:** `StandardScaler`, fitted on the **train split only** (80/20 stratified) to avoid
  leakage. Dummies left as 0/1. Min-Max computed for comparison and rejected — `fnlwgt`'s max
  is ~6× its Q3, so Min-Max crushes its IQR into the 0.07–0.15 band.
- Outputs: `adult_train_preprocessed.csv` (39,032), `adult_test_preprocessed.csv` (9,758),
  `adult_encoded_unscaled.csv` (48,790 × 86).

## Honest caveats stated in both deliverables (don't "fix" these silently)
- `log1p` on **`capital-loss` barely helps** (skew 4.57 → 4.30): 95.33 % zeros, so the skew is
  zero-inflation, not scale, and no monotone transform removes a point mass. Accepted;
  the noted alternative is splitting it into `has-capital-loss` + log amount.
- `fnlwgt` is a survey weight, not a personal attribute — flagged as a poor predictor in §1.1
  but **kept** in the output (the brief didn't ask for feature selection).

## Toolchain gotchas hit this time (new, beyond the HW3.2/HW4.1 notes below)
- **`\begin{tabular}{[^}]*}` regexes fail** on preambles containing `p{3cm}` — the brace
  inside stops the match. Substitute on `p{...cm}` directly instead.
- **Latin Modern Mono has no bold face** → bold table headers emit a font warning. Used
  `DejaVu Sans Mono` at `Scale=0.80`. (`BoldFont={Latin Modern Mono Light Bold}` is *not* a
  resolvable fontspec name and hard-errors.)
- **`[h]` floats scattered tables away from the text that discusses them** in a
  table-dense report → `\usepackage{float}` and `[H]` on all 17 floats.
- Justified narrow `p{}` columns stretch word gaps badly → `\newcolumntype{L}` with
  `\raggedright\arraybackslash`.
- The `underscore` package will break `drop_first=True` across lines → wrap in `\mbox`.
- pandas 3.0 uses a **`str` dtype, not `object`** — `df[c].dtype == object` silently matches
  nothing, which initially made the `?` audit report zero missing values.
- Seaborn `barplot` of a Series prints `None` as the y-axis label → `ax.set_ylabel("")`.

## Remaining (student tasks)
- [ ] Submit `HW5/6710503739_hw#6_preprocess.ipynb` + `HW5/6710503739_hw#6_preprocess_answer.pdf`.
      Filenames follow `Description.txt` literally. If the upload form rejects `#`, rename both
      to `6710503739_hw6_preprocess.*`.
- [ ] The brief's attribute list says *education-num* / *sex*; this CSV ships
      `educational-num` / `gender`. Both deliverables note this — no action needed unless the
      grader expects the renamed columns.

---

# HW4: Data Warehouse Design & ETL — DAKDL Baby-sitting Service

## Goal
Answer `HW4/Baby_68_2_Eng_ETL.pdf` — build a **star-schema DWH + ETL** for a babysitting
service. Task 1 done via **Option 2 (SQL-based source)**. Deliver an English design-doc PDF
plus SQL scripts, ETL, and a populated sample dataset (single ZIP).

## Status: ✅ Complete — trimmed to BARE MINIMUM on request (2026-07-25)
Pipeline **executed end-to-end with Python stdlib `sqlite3`**: 10 fact rows,
**0 FK violations**, all 5 queries correct. Design PDF `HW4/6710503739_hw4_DAKDL_Babysitting.pdf`
— **2 pages** (Task 2 + Task 3 only), XeLaTeX, visually verified. ZIP has 21 files (72K).

**Bare-minimum decisions (vs. the first full version):** PDF cut to only the 4-step design +
star-schema diagram (dropped attribute dictionary, embedded DDL/ETL/sample-data/results sections).
**Pandas notebook removed** — SQL ETL (`04_etl_load.sql`) is the single ETL (brief accepts one).
Data cut to the "5–10 per table" minimum; working-hours simplified to a plain subtraction
(no overnight/midnight case), all jobs Completed (no cancelled row, no status filters), `job_count`
and some dim attributes dropped. If marks come back short, first restore: attribute dictionary in the
PDF, and the notebook.

## Design summary
- **Single-fact star:** `Fact_Babysitting_Job` (grain = one babysitting job) +
  `Dim_Date / Dim_Customer / Dim_Employee / Dim_Club / Dim_JobType`.
- **Measures:** `amount_paid`, `working_hours` (TimeEnd−TimeBegin). **Degenerate dims:** `job_number`, `status`.
- Data: 5 clubs / 5 customers / 5 employees / 5 job types / 10 jobs across 2025 quarters;
  jobs 1001 (New Year) & 1006 (Songkran) on holidays.

## Deliverables → tasks (in `HW4/`)
- `sql/01_create_oltp.sql` + `02_insert_oltp.sql` — Task 1 (OLTP DDL + data, PK/FK).
- PDF §1 (4-step design) = Task 2; §2 TikZ star schema = Task 3.
- `sql/03_create_star_schema.sql` — Task 4 (dims + fact DDL).
- `sql/04_etl_load.sql` — Task 5 (SQL ETL).
- `sql/05_validation_queries.sql` — 5 queries.
- `sample_data/*.csv` + `dakdl_dwh_dump.sql` — Dataset. `etl/build_and_verify.py` — stdlib runner.

## MySQL variant (for MySQL Workbench + RapidMiner, per `MySQL_RapidMiner_Setup_Guide.pdf`)
- `HW4/dakdl_mysql_setup.sql` — MySQL 8 dialect: `CREATE DATABASE dakdl_dwh` + OLTP + data +
  star schema + ETL. InnoDB (FK enforcement), `AUTO_INCREMENT` surrogate keys, `TIME` columns,
  `TIME_TO_SEC(TIMEDIFF())/3600` for working hours, `DATE_FORMAT/DAYNAME/MONTHNAME/QUARTER/WEEK`
  for the date dim. `dakdl_mysql_validation.sql` — the 5 queries.
- **Not executed here** (no MySQL installed); transform logic mirrors the verified SQLite build.
  RapidMiner connects via: host `localhost`, port `3306`, DB `dakdl_dwh`, driver class
  `com.mysql.cj.jdbc.Driver`, URL prefix `jdbc:mysql://`.
- SQLite files (`build.sql` etc.) are still the current ZIP; swap to MySQL only if that's the submit target.

## Remaining (student tasks)
- [ ] Task 3 brief suggests Draw.io/Lucidchart; the TikZ diagram satisfies it — redraw in Draw.io
      only if the grader specifically wants a `.drawio`/image file.

---

# HW 4.1: Data Warehouse Design — DAKDL Airways (Frequent Flyer Program)

## Goal
Answer `HW3/Homework_4_1_DAKDL_Airway.pdf` — dimensional modeling for an airline OLTP schema.
Deliver Thai-language PDF `HW3/6710503739_hw_4_1.pdf`: (1) Business Processes / Granularities /
Dimensions / Measures, (2) Star Schema diagram, (3) attribute tables (type + desc),
(4) sample data, (5) ≥6 Business Questions + SQL.

## Status: ✅ Complete and verified
`HW3/6710503739_hw_4_1.pdf` — 9 pages, A4 **all portrait** (rot: 0 on every page), compiles clean
(0 errors, 0 missing glyphs). All pages visually verified via PNG render.

**Trimmed to minimum scope** at the user's request: only the 5 deliverables the brief lists, 6 business
questions (brief says "อย่างน้อย 6"), and no extended commentary / result narration / design essay.

**Further cut on request (§1.3 Dimensions list + §1.4 Measures table removed).** ⚠️ The brief's
question 1 explicitly asks for "Dimensions ที่จำเป็น" and "Measures ที่จะใช้", so those sub-sections
were a direct answer to it. Coverage now survives only indirectly:
dimensions → the §2 diagram + §3.3–3.6 attribute tables; measures → §3.1–3.2 attribute tables.
**What is genuinely gone: the additive / semi-additive / non-additive classification of each measure**
(it lived only in §1.4; the sole trace left is one note under BQ4 about `load_factor`).
The §1 heading still reads "…, Dimensions, Measures" — left as-is on purpose so it maps to the
brief's question 1. If marks come back short on question 1, restore §1.4 first.

## Consistency pass (2026-07-18)
Made §2 diagram, §4 sample data and §5 BQs all agree with the **§3 attribute tables** (§3 treated as
the single source of truth — the `sample_data/*.csv` headers independently confirm it is the correct one):
- Diagram: dropped `flight_count`/`booking_count`; added `distance_km` to Fact 1,
  `is_weekend` to `Dim_Date`, `origin_country` + `route_name` to `Dim_Route`.
- §3.5 `Dim_Passenger` was missing `effective_date` / `is_current` — **added**, since the dim is
  declared SCD2 and cannot function without them. Fixed in this direction, not the other.
- §4 sample data: added `is_holiday` (4.1), `origin_country`/`dest_country` (4.2),
  `arrival_time`/`distance_km` (4.5).
- BQs 2–6: `SUM(flight_count)`/`SUM(booking_count)` → `COUNT(*)`. Those stored count columns are not
  in §3, and are redundant anyway (grain is already 1 row = 1 flight / 1 booking). **Result values are
  unchanged**, so the verified numbers below still hold.
- ⚠️ Left alone: `sample_data/fact_*.csv` still carry trailing `flight_count` / `booking_count`
  columns that no longer appear in the report. Harmless, but drop them if you want a clean match.

## Design summary (the actual answer)
- **Fact Constellation (galaxy schema)** — 2 facts, because the two processes have different grain:
  - `Fact_Flight_Operations` — 1 row = 1 flight leg flown on 1 date.
  - `Fact_Booking_Revenue` — 1 row = 1 seat booked (1 passenger × 1 flight × 1 class).
  - Keeping them in one table would double-count `delay_minutes` / `seat_capacity` per booking.
- **8 Dimensions**, 3 of them **conformed** (`Dim_Date`, `Dim_Route`, `Dim_Airline`) → enables the
  drill-across query in BQ8 (revenue vs. delay by route).
- `Dim_Passenger` is **SCD Type 2** (frequent_flyer_level changes over time).
- `Dim_Date` is **role-playing** in Fact 2: `booking_date_key` + `flight_date_key`.
- `Dim_Route` denormalizes OLTP `airports`+`routes` → true star, avoids snowflake + double airport join.
- Degenerate dims: `flight_number`, `booking_id`.
- Non-additive measures flagged: `load_factor` (must use SUM(pax)/SUM(seats), not AVG of the ratio),
  `days_before_departure`.

## Verification note (worth repeating on future HW)
All result numbers asserted in the PDF were **checked by actually running the queries** — loaded
`HW3/sample_data/*.csv` into in-memory sqlite via python3 and ran BQ1/2/3/5/7/8. Every figure matched
(on-time 50%, BKK-NRT avg delay 52.5 min, B737-800 LF 92.86%, Phone revenue 86,900,
Somchai 3 bookings/23,450, BKK-NRT revenue 139,400).

## Toolchain gotchas hit this time (beyond the HW 3.2 notes below)
- `tabularx` **cannot** be split across a custom `\newenvironment` begin/end — it scans the input
  stream for a literal `\end{tabularx}`. Used plain `tabular` with fixed widths for `atttable`.
- `tabularx` with **no X column** cannot stretch → overflows. Used `adjustbox{max width=\linewidth}`
  + `tabular` for the wide sample-data tables.
- `\underline{...}` for PK collides with the next line in tight TikZ nodes → add `\\[2.5pt]`.
- TikZ nodes hyphenate long labels (`Dim_Booking_Chan-nel`, `is_cur-rent`) → widen that one node
  via inline `text width=`, or split combined attribute lines with `\\`.
- **Portrait schema layout** (this is the reusable trick): a 2-fact constellation goes wide and
  needs landscape. Instead, stack the two facts vertically and put the *conformed* dimensions in a
  middle row between them, fact-specific dims flanking left/right. Taller than wide → fits portrait
  at full `\linewidth`, no `pdflscape`, no crossing edges.

## Remaining (student task)
- [ ] Submit `HW3/6710503739_hw_4_1.pdf` (must be .pdf — .docx is docked 20%).

---

# HW 3.2: Data Warehouse Star Schema — "Culture Passport" (หนังสือเดินทางวัฒนธรรม)

## Goal
Answer `HW2/Homework_3_2_rev01.pdf` — a **dimensional-modeling design** exercise (not coding/EDA).
Deliver a Thai-language PDF report `HW2/6710503739_hw_3_2.pdf` covering: (1) Business Process /
Granularity / Dimensions / Measures, (2) Star Schema diagram, (3) attribute tables (type + desc),
(4) sample data, (5) ≥5 Business Questions + SQL.

## Status: ✅ Complete and verified
`HW2/6710503739_hw_3_2.pdf` — 9 pages, A4, compiled clean (0 errors, 0 missing glyphs).
All 9 pages visually verified via PNG render (Thai text, TikZ diagram, tables, SQL all correct).

## Toolchain (important — venv is unreachable from shell)
- The project `../.venv` python is a **snap-confined symlink** → NOT runnable from a plain bash shell.
- PDF built with **XeLaTeX** (system TeX Live). Star schema drawn natively in **TikZ** (no draw.io).
- Fonts: main = **Waree** (TLWG dual-script: full Latin + Thai + bold/italic — Noto Sans Thai has
  NO Latin glyphs, do not use it as main). Mono = **Tlwg Typewriter** (Thai-capable, for SQL).
- Thai line-breaking: `\XeTeXlinebreaklocale "th"` (ICU dictionary) — required or Thai overflows margin.
- `underscore` package lets snake_case print literally in text/tables.
- Rebuild: `cd HW2 && xelatex -interaction=nonstopmode 6710503739_hw_3_2.tex` (run twice).
- Render to verify: `pdftoppm -png -r 105 6710503739_hw_3_2.pdf out` (poppler available).

## Design summary (the actual answer)
- **Business Process:** Member Activity Participation (การเข้าร่วมกิจกรรมของสมาชิก).
- **Grain:** 1 row = 1 member attending 1 activity event (atomic).
- **Fact:** `Fact_Participation` (measures: amount_paid, discount_amount, points_earned,
  review_score [non-additive→AVG], participant_count).
- **5 Dims:** Dim_Date, Dim_Member (SCD Type 2 for membership_level), Dim_Activity, Dim_Location, Dim_Team.
- Degenerate dim: `registration_id`. Surrogate keys throughout. Star (not snowflake).
- Sample data: `HW2/sample_data/*.csv` (6 files) — values cross-consistent so all 6 SQL queries
  return sensible answers (e.g. Isan-in-April revenue = 1,520; best 2567 team avg = TM-03 @ 4.75).

## Remaining (student task)
- [ ] Submit `HW2/6710503739_hw_3_2.pdf` (must be .pdf — .docx is docked 20%). Verify student ID
      `6710503739` is correct before submitting.

---

# HW#2: Titanic Data Quality Assessment & EDA

## Goal
Answer HW#2 (`HW#2_1_69_1.pdf`) Questions 2–6 on `titanic_data.csv` (891 passengers),
with charts + Thai-language interpretations. Work delivered in `HW_1.ipynb`.

## Status: ✅ Notebook complete and verified
`HW_1.ipynb` — 37 cells (19 code), runs end-to-end (Restart & Run All), 0 errors, 11 charts.
All explanations/interpretations written in **Thai**.

## Environment
- Uses parent `../.venv` (uv, Python 3.12): pandas 3.0, numpy, matplotlib, seaborn, missingno, scipy.
- Kernel name in notebook: `data mining`.
- Re-run: `../.venv/bin/jupyter nbconvert --to notebook --execute --inplace HW_1.ipynb`

## Coverage (per PDF)
- **Q2.1** Missing data: table + heatmap + missingno matrix/heatmap. Cabin 77.10%, Age 19.87%, Embarked 0.22%.
- **Q2.2** Outliers (IQR) on Age/Fare/SibSp + boxplots; all 6 sub-questions answered (IQR vs Z-score, bad-data, Fare removal, Isolation Forest, impact).
- **Q3.1** Histograms + boxplots (Age skew 0.39; Fare skew 4.79 heavy right-skew).
- **Q3.2** Categorical bar + pie (Survived 38.4%, Sex, Pclass, Embarked).
- **Q4.1** Pearson Age–Fare r=0.096 (very weak) + scatter.
- **Q5.1** Contingency Survived×Pclass; survival 1st 62.96% / 2nd 47.28% / 3rd 24.24%.
- **Q5.2** Chi-square: χ²=102.89, p≈4.55e-23, dof=2 → reject H₀.
- **Q6.1** Pairplot Age/Fare/SibSp by Survived.

## Remaining (student tasks)
- [ ] Rename/copy to submission name `6710503739_hw_2_1.ipynb` (student ID inferred from sibling `6710503739_Inclass#1.ipynb`).
- [ ] Export notebook to `6710503739_hw_2_1.pdf` for the report.

---

# W12: In-Class Decision Trees

## Status: ✅ Done (minimal submission)
- `W12/6710503739_Kawinphop_DecisionTree.ipynb`: steps 1–6 + short answers, executed.
- `W12/6710503739_Kawinphop_DecisionTree.pdf`: notebook export = answer document.
- Setup: features Gender(Male=1)/Age/EstimatedSalary; 10-fold StratifiedKFold shuffle seed 42.
- Baseline gini d=4 leaf=5 → 0.8775; entropy → 0.8825; grid best entropy d=2 (leaf 1–10 tied 0.9100) → pick leaf=10.
- Final tree train acc 0.915; new customer (F, 40, 100000) → Purchased=1, conf(0)=0.1591, conf(1)=0.8409.

## Remaining
- [ ] Submit the two files.

---

# W13: In-Class KNN + PCA (Personal Loan)

## Status: ✅ Done (minimal submission)
- `W13/6710503739_inclass13.ipynb`: Parts I–VI, executed with outputs; saves `pca_plot.png`.
- `W13/69_..._ANSWERED.pdf`: the original worksheet with every table/blank filled in.
  Built by stamping a transparent overlay onto the untouched source pages (Carlito ≈ the
  document's Aptos), so layout, rules and shading are unchanged. Script: scratchpad `fill.py`.
- Setup: drop ID/ZIP; 11 predictors; StratifiedKFold(5, shuffle, seed 42); Pipeline puts
  Normalize (and PCA) inside CV; grid criterion = F1 on class 1.
- Part I  KNN k=5 → acc 0.9608 / prec 0.9522 / rec 0.6229 / F1 0.7525; CM TN 4505 FP 15 FN 181 TP 299.
- Part II best k=1 → 0.9604 / 0.8675 / 0.6938 / 0.7706.
- Part III best components=8, k=1 → 0.9568 / 0.8270 / 0.6958 / 0.7552 (all top-5 rows use max 8 comps).
- Part IV PC1 0.1862, PC2 0.1688, cumulative 0.3550; PC1 = Age/Experience/Income, PC2 = Income/CCAvg/Experience.
- Decision: pick optimized KNN k=1; PCA did not help. Part VI customer → Personal Loan = 0.

## Known cosmetic issue
- The worksheet's `?` placeholders in Part V are covered by an opaque patch and overwritten,
  so the page renders correctly, but copying text still yields `=8?`. The source fonts are
  subsetted with no `?` code, so removing the glyph from the content stream is not safe.

## Remaining
- [ ] Submit the notebook + the ANSWERED PDF.

---

# W14: In-Class Imbalanced Classification (Telco Churn, E0/E1/E2)

## Status: ✅ Done (minimal submission)
- `W14/6710503739_Imbalanced_InClass.ipynb`: Parts A–D, executed with outputs.
- `W14/6710503739_Imbalanced_InClass_Report.pdf`: the notebook exported via nbconvert→LaTeX→XeLaTeX.
- Setup: target Churn, positive = Yes; No 5174 / Yes 1869 → IR 2.768; 11 blank TotalCharges
  (all tenure 0) → 0; customerID dropped; one-hot → 45 features; StratifiedKFold(5, shuffle, seed 1992).
- Same tree everywhere: entropy, max_depth 10, min_samples_leaf 2, seed 1992. imblearn Pipeline
  keeps sampling inside the training folds only.
- E0 acc 0.7647 / prec 0.5646 / rec 0.4976 / F1 0.5288; CM TN 4456 FP 718 FN 939 TP 930.
- E1 (RandomUnderSampler 300/300) 0.6947 / 0.4512 / 0.6977 / 0.5477; CM 3589 1585 565 1304.
- E2 (StandardScaler + SMOTE k=5, auto) 0.7375 / 0.5054 / 0.6977 / 0.5854; CM 3890 1284 565 1304.
- Decision: E2 SMOTE (best F1; same FN reduction as E1, −374, but +566 FP instead of +867).

## Remaining
- [ ] Submit the notebook + report PDF.
