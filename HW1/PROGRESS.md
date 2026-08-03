# PROGRESS — HW#2: Titanic Data Quality Assessment & EDA

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
