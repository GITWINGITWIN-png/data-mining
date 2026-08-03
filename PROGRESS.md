# PROGRESS — Data Mining course

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
