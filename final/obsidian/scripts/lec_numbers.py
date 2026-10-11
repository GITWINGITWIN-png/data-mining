"""คำนวณยืนยัน "ตัวเลขทุกตัว" ที่ใช้ในโน้ต Lecture (LEC 03–13) — รันแล้วเทียบกับข้อความในโน้ต

ทำไมต้องมี: ตัวอย่างในสไลด์บางหน้าคำนวณผิด (เช่น Tree p.41) และบางค่าไม่ได้เขียนไว้ (lift, gain ratio)
สคริปต์นี้คำนวณใหม่ทั้งหมดจากข้อมูลดิบ ให้ตรวจได้ว่าเฉลยในโน้ตถูก

รัน:  final/.venv/bin/python final/obsidian/scripts/lec_numbers.py
"""
from itertools import combinations
from math import log2, sqrt, exp, log
import numpy as np
import pandas as pd

from _style import DATA


def H(counts):
    n = sum(counts)
    return -sum(c / n * log2(c / n) for c in counts if c)


def gini(counts):
    n = sum(counts)
    return 1 - sum((c / n) ** 2 for c in counts)


def section(t):
    print(f"\n{'═' * 8} {t} {'═' * (70 - len(t))}")


# ── LEC 05 · evaluation ─────────────────────────────────────────────────────────
section("Riding Mowers threshold (KNN p.70–72)")
pr = pd.read_csv(DATA / "riding_mowers_probs.csv")
for c in (0.25, 0.5, 0.75, 0.8):
    pred = pr.Prob_Owner >= c
    tp = (pred & (pr.Actual == "Owner")).sum(); fp = (pred & (pr.Actual == "Nonowner")).sum()
    fn = (~pred & (pr.Actual == "Owner")).sum(); tn = (~pred & (pr.Actual == "Nonowner")).sum()
    p, r = tp / (tp + fp), tp / (tp + fn)
    print(f"cutoff {c}: TP{tp} FN{fn} FP{fp} TN{tn}  acc {(tp+tn)/24:.4f}  P {p:.3f} R {r:.3f} F1 {2*p*r/(p+r):.3f}  #pred owner {pred.sum()}")

section("5-fold CV (Tree p.74)")
f = np.array([0.80, 0.88, 0.85, 0.78, 0.84]); print("mean", f.mean().round(4), "std(ddof=1)", f.std(ddof=1).round(4), "std(ddof=0)", f.std().round(4))

section("Multi-class CM drugs (KNN p.66; rows=predicted, cols=actual)")
cm = np.array([[22, 0, 0, 0, 3], [1, 16, 0, 0, 1], [0, 0, 16, 0, 4], [0, 0, 0, 54, 2], [0, 0, 0, 0, 81]])
print("N", cm.sum(), "acc", np.trace(cm) / cm.sum())
for i, d in enumerate("ABCXY"):
    print(f"drug{d}: precision {cm[i,i]/cm[i].sum():.3f}  recall {cm[i,i]/cm[:,i].sum():.3f}")

section("Fraud CM (Imbalanced p.11)")
tn, fp, fn, tp = 950, 30, 15, 5
P, R = tp / (tp + fp), tp / (tp + fn)
print("acc", (tp + tn) / 1000, "P1", round(P, 4), "R1", R, "F1", round(2 * P * R / (P + R), 4),
      "P0", round(tn / (tn + fn), 4), "R0", round(tn / (tn + fp), 4), "majority acc", 980 / 1000)

section("Regression metrics drill")
y = np.array([3, 5, 2.5, 7]); yh = np.array([2.5, 5, 4, 8])
e = y - yh
print("MAE", np.abs(e).mean(), "MSE", (e**2).mean(), "RMSE", round(sqrt((e**2).mean()), 4),
      "R2", round(1 - (e**2).sum() / ((y - y.mean())**2).sum(), 4))

# ── LEC 06 · KNN ────────────────────────────────────────────────────────────────
section("Data p.21 distance matrix")
pts = {"x1": (1, 2), "x2": (3, 5), "x3": (2, 0), "x4": (4, 5)}
for a, b in combinations(pts, 2):
    (x1, y1), (x2, y2) = pts[a], pts[b]
    print(f"d({a},{b}) Euclid {sqrt((x1-x2)**2+(y1-y2)**2):.2f}  Manhattan {abs(x1-x2)+abs(y1-y2)}  Chebyshev {max(abs(x1-x2), abs(y1-y2))}")

section("KNN hand drill (raw vs scaled)")
train = pd.DataFrame({"age": [25, 35, 45, 20, 35, 52, 23, 40, 60, 48],
                      "income": [40, 60, 80, 20, 120, 18, 95, 62, 100, 220],
                      "y": ["N", "N", "N", "N", "N", "N", "Y", "Y", "Y", "Y"]})
q = (48, 142)
d = np.sqrt((train.age - q[0])**2 + (train.income - q[1])**2)
print(train.assign(d=d.round(2)).sort_values("d").head(3).to_string())
mm = train[["age", "income"]]
z = (mm - mm.min()) / (mm.max() - mm.min())
qz = ((q[0] - mm.age.min()) / (mm.age.max() - mm.age.min()), (q[1] - mm.income.min()) / (mm.income.max() - mm.income.min()))
dz = np.sqrt((z.age - qz[0])**2 + (z.income - qz[1])**2)
print("query scaled", np.round(qz, 3)); print(train.assign(dz=dz.round(3)).sort_values("dz").head(3).to_string())

section("Riding Mowers new household (Income 60, Lot 20) k=1,3,5 (raw)")
rm = pd.read_csv(DATA / "riding_mowers.csv")
dd = np.sqrt((rm.Income - 60)**2 + (rm.Lot_Size - 20)**2)
print(rm.assign(d=dd.round(3)).sort_values("d").head(5).to_string())

# ── LEC 07 · logistic ───────────────────────────────────────────────────────────
section("Sigmoid from Age 35→0.42, 45→0.81 (KNN p.16–17)")
l35, l45 = log(0.42 / 0.58), log(0.81 / 0.19)
b1 = (l45 - l35) / 10; b0 = l35 - 35 * b1
print(f"logit(0.42)={l35:.4f} logit(0.81)={l45:.4f} → b1={b1:.4f} b0={b0:.4f}  odds ratio/yr={exp(b1):.4f}  p(50%) at age {-b0/b1:.2f}")
for a in (30, 40, 50):
    print(f"  p(age={a}) = {1/(1+exp(-(b0+b1*a))):.4f}")
section("Likelihood (KNN p.20)")
L = 0.03 * 0.54 * 0.92 * 0.95 * 0.98 * (1 - 0.01) * (1 - 0.04) * (1 - 0.10) * (1 - 0.58) * (1 - 0.96)
print("L =", round(L, 8), " log-likelihood =", round(log(L), 4))
section("LogReg drill z→p")
z_ = -3.84078827 + 5.11087515e-04 * 1500 + 2.55647725e-01 * 1.5 + 6.77689408e-01 * 4
print("veh: weight 1500kg h 1.5m wheels 4 → z", round(z_, 4), "P(other)", round(1 / (1 + exp(-z_)), 4))
z2 = -4 + 0.05 * 60 + 0.8 * 1
print("drill: b0=-4, b_income=0.05 (60), b_married=0.8 (1) → z", z2, "p", round(1 / (1 + exp(-z2)), 4), "OR income", round(exp(0.05), 4), "OR married", round(exp(0.8), 4))

# ── LEC 08 · trees ──────────────────────────────────────────────────────────────
section("Weather (Tree p.8–39)")
w = pd.read_csv(DATA / "weather.csv")
Hs = H(w.Class.value_counts().tolist())
print("H(S)", round(Hs, 4), "Gini(S)", round(gini(w.Class.value_counts().tolist()), 4))
for a in ["Outlook", "Temperature", "Humidity", "Windy"]:
    parts = [g.Class.value_counts().tolist() for _, g in w.groupby(a)]
    sizes = [sum(p) for p in parts]
    child = sum(s / 14 * H(p) for s, p in zip(sizes, parts))
    gchild = sum(s / 14 * gini(p) for s, p in zip(sizes, parts))
    si = H(sizes)
    print(f"{a:12s} E_child {child:.4f}  IG {Hs-child:.4f}  SplitInfo {si:.4f}  GR {(Hs-child)/si:.4f}  Gini_split {gchild:.4f}  Gini gain {gini(w.Class.value_counts().tolist())-gchild:.4f}")
sunny = w[w.Outlook == "sunny"]; rain = w[w.Outlook == "rain"]
for nm, sub in [("sunny", sunny), ("rain", rain)]:
    for a in ["Temperature", "Humidity", "Windy"]:
        parts = [g.Class.value_counts().tolist() for _, g in sub.groupby(a)]
        child = sum(sum(p) / len(sub) * H(p) for p in parts)
        print(f"  {nm}: IG({a}) = {H(sub.Class.value_counts().tolist()) - child:.4f}")

section("Tree p.41 binary Gini (slide wrong)")
g1, g2 = gini([5, 2]), gini([1, 4]); print("Gini N1", round(g1, 4), "N2", round(g2, 4), "split", round(7/12*g1 + 5/12*g2, 4), "gain", round(0.5 - (7/12*g1 + 5/12*g2), 4))
print("slide values 0.194/0.528 → weighted", round(7/12*0.194 + 5/12*0.528, 4))

section("Own Car / Car Type / Student ID (Tree p.21, 43)")
for nm, parts in [("OwnCar", [[6, 4], [4, 6]]), ("CarType", [[1, 3], [8, 0], [1, 7]]), ("StudentID", [[1, 0]] * 10 + [[0, 1]] * 10)]:
    sizes = [sum(p) for p in parts]
    child = sum(s / 20 * H(p) for s, p in zip(sizes, parts)); si = H(sizes)
    gs = sum(s / 20 * gini(p) for s, p in zip(sizes, parts))
    print(f"{nm:10s} IG {1-child:.4f}  SplitInfo {si:.4f}  GR {(1-child)/si:.4f}  Gini_split {gs:.4f}")

section("Tid/Cheat (Tree p.47)")
t = pd.read_csv(DATA / "tid_cheat.csv")
Ht = H(t.Cheat.value_counts().tolist()); print("H", round(Ht, 4), "Gini", round(gini(t.Cheat.value_counts().tolist()), 4))
t["Inc>80"] = t.Taxable_Income_K > 80
for a in ["Refund", "Marital", "Inc>80"]:
    parts = [g.Cheat.value_counts().tolist() for _, g in t.groupby(a)]
    child = sum(sum(p) / 10 * H(p) for p in parts); gs = sum(sum(p) / 10 * gini(p) for p in parts)
    print(f"{a:8s} IG {Ht-child:.4f}  Gini_split {gs:.4f}  Gini gain {gini(t.Cheat.value_counts().tolist())-gs:.4f}")

# ── LEC 03 · PCA ────────────────────────────────────────────────────────────────
section("PCA cereals (PCA p.10–18)")
print("calories share", round(379.63 / (379.63 + 197.32), 4), " Z1 share", round(498.0244751 / (498.0244751 + 78.932724), 4))
eig = np.array([3.59530377, 3.16411042, 1.86585701, 1.09171081, 0.96962351, 0.72342771])
print("std eig/13", (eig / 13).round(4), "cum", (eig / 13).cumsum().round(4), "Kaiser>1:", (eig > 1).sum())
raw = np.array([7204.161133, 4833.050293, 498.4260864, 357.2174377, 72.47863007, 4.33980322])
print("raw cum%", (raw.cumsum() / raw.sum() * 0.9997 * 100).round(2))
section("PCA 2x2 hand drill")
Xp = np.array([[2, 0], [0, 2], [4, 4], [6, 2], [8, 6]], float)   # มีความสัมพันธ์บวก
Xc = Xp - Xp.mean(0); C = np.cov(Xc.T); ev, vec = np.linalg.eigh(C)
print("cov", C.round(3).tolist(), "eigvals", ev[::-1].round(4), "EVR", (ev[::-1] / ev.sum()).round(4), "PC1", vec[:, -1].round(4))

# ── LEC 04 · imbalanced ─────────────────────────────────────────────────────────
section("IR")
print("10000/100", 10000 / 100, " churn 5174/1869", round(5174 / 1869, 3), " Active/Claim", round(63679 / 30239, 2),
      "Active/Overdue", round(63679 / 14718, 2), "Active/Other", round(63679 / 8686, 2), " dept 799/162", round(799 / 162, 2))
section("SMOTE point")
xi, xn, lam = np.array([2.0, 3.0]), np.array([4.0, 7.0]), 0.25
print("x_new =", xi + lam * (xn - xi))

# ── LEC 09 · clustering ─────────────────────────────────────────────────────────
section("K-Means 9 points (HW9) seeds A1,A4,A7")
P9 = {"A1": (3, 8), "A2": (9, 4), "A3": (4, 9), "A4": (2, 2), "A5": (10, 5), "A6": (2, 4), "A7": (6, 8), "A8": (4, 3), "A9": (4, 7)}
names = list(P9); Xk = np.array(list(P9.values()), float); cen = Xk[[0, 3, 6]].copy()
for it in range(1, 6):
    d2 = ((Xk[:, None, :] - cen[None]) ** 2).sum(2); lab = d2.argmin(1)
    new = np.array([Xk[lab == k].mean(0) for k in range(3)])
    sse = sum(((Xk[lab == k] - new[k]) ** 2).sum() for k in range(3))
    print(f"iter {it}: " + " | ".join(f"C{k+1}={[n for n, l in zip(names, lab) if l == k]} → {tuple(new[k].round(3))}" for k in range(3)), f"SSE={sse:.3f}")
    if np.allclose(new, cen): break
    cen = new
section("Utilities p.56 weighted avg")
print(round((12 * 1748.348058 + 3 * 907.6919822 + 7 * 3625.242085) / 22, 3))
section("mean vs median (clustering p.32)")
print(np.mean([1, 3, 5, 7, 1009]), np.median([1, 3, 5, 7, 1009]))
section("silhouette drill (1-D)")
pts1 = {"a": 1, "b": 2, "c": 3, "d": 8, "e": 9}; cl = {"a": 0, "b": 0, "c": 0, "d": 1, "e": 1}
for p in pts1:
    same = [abs(pts1[p] - pts1[q]) for q in pts1 if q != p and cl[q] == cl[p]]
    other = [abs(pts1[p] - pts1[q]) for q in pts1 if cl[q] != cl[p]]
    a, b = np.mean(same), np.mean(other); print(f"{p}: a={a:.3f} b={b:.3f} s={(b-a)/max(a,b):.3f}")

# ── LEC 10 · association ────────────────────────────────────────────────────────
def apriori_trace(T, minsup_count, label):
    section(f"Apriori trace: {label} (minsup count {minsup_count})")
    items = sorted({i for t in T for i in t})
    sup = lambda s: sum(set(s) <= set(t) for t in T)
    L = [frozenset([i]) for i in items if sup([i]) >= minsup_count]
    print("C1:", {i: sup([i]) for i in items}); print("L1:", sorted("".join(sorted(s)) for s in L))
    k, allL = 2, list(L)
    while L:
        prev = sorted(tuple(sorted(s)) for s in L)
        joined = {tuple(sorted(set(a) | set(b))) for a, b in combinations(prev, 2) if a[:-1] == b[:-1]}
        pruned = [c for c in joined if all(frozenset(s) in set(L) for s in combinations(c, k - 1))]
        print(f"C{k} join: {sorted(''.join(c) for c in joined)}  after prune: {sorted(''.join(c) for c in pruned)}")
        cnt = {"".join(c): sup(c) for c in sorted(pruned)}
        L = [frozenset(c) for c in pruned if sup(c) >= minsup_count]
        print(f"   counts {cnt} → L{k}: {sorted(''.join(sorted(s)) for s in L)}")
        allL += L; k += 1
    return sup, allL


T_acd = [set("ACD"), set("BCE"), set("ABCE"), set("BE"), set("ABCE")]
sup, _ = apriori_trace(T_acd, 3, "ACD DB (Apriori p.15)")
for X_, Y_ in [("BC", "E"), ("BE", "C"), ("CE", "B"), ("B", "CE"), ("C", "BE"), ("E", "BC"), ("A", "C"), ("C", "A"), ("B", "E")]:
    s = sup(X_ + Y_) / 5; c = sup(X_ + Y_) / sup(X_); l = c / (sup(Y_) / 5)
    print(f"  {X_}->{Y_}: s {s:.2f} c {c:.3f} lift {l:.3f}")
T9 = [set("ABE"), set("BD"), set("BC"), set("ABCD"), set("AC"), set("BC"), set("AC"), set("ABCE"), set("ABC")]
sup9, _ = apriori_trace(T9, 2, "9 transactions (Apriori p.18)")
for X_, Y_ in [("AB", "E"), ("AE", "B"), ("BE", "A"), ("E", "AB"), ("A", "BE"), ("B", "AE")]:
    c = sup9(X_ + Y_) / sup9(X_); print(f"  {X_}->{Y_}: conf {sup9(X_+Y_)}/{sup9(X_)} = {c:.3f}  lift {c/(sup9(Y_)/9):.3f}")
T_ag = [{1, 3, 4}, {2, 3, 5}, {1, 2, 3, 5}, {2, 5}]
T_ag = [set(map(str, t)) for t in T_ag]
apriori_trace(T_ag, 2, "Agrawal Fig.3")
T_bm = [{"Bread", "Milk"}, {"Bread", "Diaper", "Beer", "Eggs"}, {"Milk", "Diaper", "Beer", "Coke"},
        {"Bread", "Milk", "Diaper", "Beer"}, {"Bread", "Milk", "Diaper", "Coke"}]
sbm = lambda s: sum(set(s) <= t for t in T_bm)
section("Bread/Milk rules from {Milk,Diaper,Beer}")
for X_, Y_ in [({"Milk", "Diaper"}, {"Beer"}), ({"Milk", "Beer"}, {"Diaper"}), ({"Diaper", "Beer"}, {"Milk"}),
               ({"Beer"}, {"Milk", "Diaper"}), ({"Diaper"}, {"Milk", "Beer"}), ({"Milk"}, {"Diaper", "Beer"})]:
    c = sbm(X_ | Y_) / sbm(X_); print(f"  {sorted(X_)}->{sorted(Y_)}: s {sbm(X_|Y_)/5} c {c:.3f} lift {c/(sbm(Y_)/5):.3f}")
section("tea/coffee + A=>B + Juice/Coke")
print("tea→coffee conf", 0.20 / 0.25, "lift", round(0.20 / 0.25 / 0.90, 4))
TA = [{"A"}, {"A", "B"}, {"A", "B"}, {"A", "B"}, {"B"}]
print("A→B s", 3 / 5, "c", 3 / 4, "lift", round(0.75 / 0.8, 4))
print("Juice→Coke lift", round(0.75 / (4 / 6), 4), " Coke→Beer", round(0.75 / 0.5, 4), " Beer→Coke", round(1.0 / (4 / 6), 4))
