---
title: LEC 11 · Formula Sheet
exam: Lecture — จ. 19 ต.ค. 2569 16:00–19:00
tags: [final, lecture, formulas]
---

# LEC 11 · Formula Sheet
### สูตรทั้งหมดของ Final ในหน้าเดียว — อ่านรอบสุดท้ายก่อนเข้าห้อง

**ลิงก์:** [[LEC 00 START HERE|หน้าหลัก Lecture]] · ฝึกใช้: [[LEC 13 Exam Drills]] · สูตรมิดเทอม (สถิติ, distance, regression): [[10 Formula Sheet]]

---

## 📊 EDA — [[LEC 01 EDA Review]]
| | สูตร |
|---|---|
| mean · variance · SD | $\bar x=\frac{1}{n}\sum x_i$ · $s^2=\frac{1}{n-1}\sum(x_i-\bar x)^2$ · $s=\sqrt{s^2}$ |
| IQR · outlier fence | $IQR=Q_3-Q_1$ · $[Q_1-1.5IQR,\ Q_3+1.5IQR]$ |
| CV | $s/\bar x$ |
| Pearson r | $r=\dfrac{\sum(x-\bar x)(y-\bar y)}{\sqrt{\sum(x-\bar x)^2\sum(y-\bar y)^2}}$ · strong > 0.7 · moderate 0.3–0.7 · weak < 0.3 |
| skew | mean > median → ขวา · \|s\| < 0.5 เกือบสมมาตร · ≥ 1 เบ้มาก |

## 🔧 Preprocessing — [[LEC 02 Preprocessing, Feature Selection & Leakage]]
| | สูตร |
|---|---|
| z-score | $z=\frac{x-\mu}{\sigma}$ (sklearn หาร n · RapidMiner หาร n−1) |
| min-max | $x'=\frac{x-\min}{\max-\min}$ · ไป [a, b]: $a+(b-a)x'$ |
| new point | ใช้ μ, σ, min, max **ของ training** |

## 🧭 PCA — [[LEC 03 PCA]]
| | สูตร |
|---|---|
| PC | $Z_i=a_{i1}X_1+\dots+a_{ip}X_p$ (a = loadings = eigenvector) |
| eigen | $\Sigma v=\lambda v$ · Var($Z_i$) = $\lambda_i$ · $\sum\lambda_i=\sum\text{Var}(X_j)$ |
| explained variance | $\text{EVR}_i=\lambda_i/\sum_j\lambda_j$ · standardized: $\lambda_i/p$ |
| เลือกจำนวน | cumulative ≥ 80–90% · Kaiser: λ > 1 (standardized) · scree elbow |
| 2×2 eigenvalue | $\lambda=\frac{(a+d)\pm\sqrt{(a+d)^2-4(ad-b^2)}}{2}$ สำหรับ $\begin{bmatrix}a&b\\b&d\end{bmatrix}$ |

## ⚖️ Imbalanced — [[LEC 04 Imbalanced Classification]]
| | สูตร |
|---|---|
| IR | majority / minority · mild < 10 · moderate 10–100 · severe > 100 · extreme > 1000 |
| SMOTE | $X_{new}=X_i+\lambda(\bar X_i-X_i)$, $\lambda\sim U(0,1)$, $\bar X_i$ ∈ kNN (minority) ของ $X_i$ |

## ✅ Evaluation — [[LEC 05 Model Construction & Evaluation]]
| | สูตร |
|---|---|
| accuracy | $\frac{TP+TN}{N}$ · error = 1 − accuracy |
| precision | $\frac{TP}{TP+FP}$ |
| recall (TPR, sensitivity) | $\frac{TP}{TP+FN}$ |
| specificity (TNR) | $\frac{TN}{TN+FP}$ · FPR = 1 − specificity |
| F1 | $\frac{2PR}{P+R}=\frac{2TP}{2TP+FP+FN}$ |
| k-fold | final = เฉลี่ย k รอบ · LOOCV: k = n |
| MAE · MSE · RMSE | $\frac1n\sum\lvert e\rvert$ · $\frac1n\sum e^2$ · $\sqrt{MSE}$ (e = y − ŷ) |
| R² · adj R² | $1-\frac{SSE}{SST}$ · $1-\frac{(1-R^2)(n-1)}{n-k-1}$ |
| baseline | classification: accuracy = สัดส่วนคลาสใหญ่ · regression: ทาย ȳ → R² = 0 |

## 📍 KNN — [[LEC 06 KNN]]
| | สูตร |
|---|---|
| Euclidean | $\sqrt{\sum(x_k-y_k)^2}$ |
| Manhattan | $\sum\lvert x_k-y_k\rvert$ |
| Minkowski | $(\sum\lvert x_k-y_k\rvert^q)^{1/q}$ (q = 1, 2) |
| weighted vote / avg | $w=1/d$ (หรือ $1/d^2$) · $\hat y=\frac{\sum w_iy_i}{\sum w_i}$ |
| เลือก k | ต่ำสุดบน validation · เลขคี่ · k = n = naive rule |

## 📈 Linear & Logistic — [[LEC 07 Linear & Logistic Regression]]
| | สูตร |
|---|---|
| OLS | $b_1=\frac{\sum xy-\frac{\sum x\sum y}{n}}{\sum x^2-\frac{(\sum x)^2}{n}}$ · $b_0=\bar y-b_1\bar x$ |
| odds · logit | odds = $\frac{p}{1-p}$ · $\ln\frac{p}{1-p}=b_0+b_1x_1+\dots=z$ |
| sigmoid | $p=\frac{1}{1+e^{-z}}$ · z = 0 → p = 0.5 · ±1 → 0.73/0.27 · ±2 → 0.88/0.12 |
| odds ratio | $e^{b}$ — x +1 หน่วย odds × $e^b$ |
| likelihood | $L=\prod_{y=1}p_i\prod_{y=0}(1-p_i)$ → maximize |
| threshold | p ≥ t → 1 · t ↓ → recall ↑ precision ↓ |

## 🌳 Trees — [[LEC 08 Decision Trees & Random Forest]]
| | สูตร |
|---|---|
| Entropy | $-\sum p_j\log_2p_j$ · max $\log_2 n_c$ (2 คลาส = 1) |
| Gini | $1-\sum p_j^2$ · max $1-1/n_c$ (2 คลาส = 0.5) |
| Misclassification | $1-\max_j p_j$ |
| Information Gain | $H(parent)-\sum\frac{n_i}{n}H(i)$ |
| Gini split | $\sum\frac{n_i}{n}\text{Gini}(i)$ · gain = Gini(parent) − Gini split |
| Gain Ratio | $\frac{IG}{\text{SplitInfo}}$ · SplitInfo $=-\sum\frac{n_i}{n}\log_2\frac{n_i}{n}$ |
| ค่า H ที่ใช้บ่อย | (½,½) 1 · (⅓,⅔) 0.918 · (¼,¾) 0.811 · (⅕,⅘) 0.722 · (⅖,⅗) 0.971 · (9/14,5/14) 0.940 · (1/6, 5/6) 0.650 |
| log₂ | $\log_2x=\ln x/0.6931=\log_{10}x/0.3010$ |
| RF | bootstrap n แถว (≈ 63% ไม่ซ้ำ) · max_features ≈ √p · โหวต / เฉลี่ย |

## 🔵 Clustering — [[LEC 09 Clustering]]
| | สูตร |
|---|---|
| SSE / WCSS | $\sum_k\sum_{x\in C_k}\lVert x-m_k\rVert^2$ |
| centroid | $m_k=\frac{1}{\lvert C_k\rvert}\sum_{x\in C_k}x$ |
| silhouette | $s(i)=\frac{b(i)-a(i)}{\max(a,b)}$ · a = เฉลี่ยในกลุ่ม · b = เฉลี่ยกลุ่มอื่นที่ใกล้สุด |
| avg within-centroid distance | WCSS / n (RapidMiner) |
| Davies–Bouldin | ต่ำ = ดี (RapidMiner แสดงติดลบ) |
| complexity | O(tkn) |

## 🛒 Association — [[LEC 10 Association Rules]]
| | สูตร |
|---|---|
| support | $\frac{\sigma(X\cup Y)}{N}$ |
| confidence | $\frac{\sigma(X\cup Y)}{\sigma(X)}$ |
| lift | $\frac{conf}{s(Y)}=\frac{s(X\cup Y)}{s(X)s(Y)}$ · > 1 บวก · = 1 อิสระ · < 1 ลบ · สมมาตร (X→Y = Y→X) |
| leverage · conviction | $s(XY)-s(X)s(Y)$ · $\frac{1-s(Y)}{1-conf}$ |
| จำนวนกฎจาก k-itemset | $2^k-2$ |
| Apriori principle | subset ของ frequent ต้อง frequent · superset ของ infrequent ไม่ frequent |
| apriori-gen | join (prefix k−2 ตัวเหมือน) → prune (มี (k−1)-subset ไม่อยู่ใน L(k−1)) |

---

**กลับหน้าหลัก →** [[LEC 00 START HERE]]
