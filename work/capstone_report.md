# Capstone Research Report — Lane 2: Refresh / Content Opportunity Scoring

- **Author:** Applied Search Intelligence Intern
- **Lane:** Lane 2 — Refresh / Content Opportunity Scoring
- **Repo:** [https://github.com/meer140/flyrank-ml-internship-project](https://github.com/meer140/flyrank-ml-internship-project)
- **Date:** September 2026

---

## 0. Abstract

Managing multi-client web portfolios requires allocating limited editorial resources to published pages facing search traffic decay. We evaluated 30,000 pseudonymized content items across 32 client portfolios using observed Search Console and GA4 metrics to predict 30-day impression decay. We constructed a transparent baseline rule and trained three machine learning classifiers (Logistic Regression, Decision Tree, and Random Forest) using a client-holdout grouped validation split. The Random Forest model achieved a Precision@50 of **0.740** (a 3.08x lift over the 0.240 baseline precision), an ROC-AUC of **0.750**, and an Average Precision of **0.618**. The resulting opportunity scoring engine powers a public-safe ranked action playbook that isolates high-upside refresh candidates and snippet optimization targets for human editorial review.

---

## 1. Problem framing

### Unit of Analysis & Decision Supported
- **Unit of Analysis:** One pseudonymized content item / page (`content_id` grain per `client_id`) evaluated over a trailing 90-day performance window.
- **Decision Supported:** Deciding how to allocate finite editorial review capacity (e.g., 20–50 pages per month) across thousands of published assets — replacing ad-hoc manual checks with a evidence-backed candidate queue.
- **Actor & Action:** A Content Editor or SEO Lead inspects the top-ranked review queue, reviews transparent reason codes (`model_decline_risk`, `ctr_review_candidate`, `stale_visible_page`, `thin_visible_page`), and executes targeted editorial updates (content refreshes, structural depth expansion, or title/meta snippet rewrites).

### Cost of a Wrong Call
- **False Positive (Flagging a healthy page for refresh):** Wastes 2–4 hours of expert editorial time per page updating content that was performing well or experiencing temporary seasonal fluctuations. Unnecessary edits may also disrupt established search ranking signals.
- **False Negative (Missing a high-demand page in active decay):** Results in compounding loss of organic search impressions, uncaptured user demand, and long-term SERP position decay before manual detection occurs.

### Why Machine Learning Beats a Fixed Rule
A static threshold rule (such as `if impressions_90d >= 500 and trend == 'down'`) flags **9,961 pages** simultaneously in our dataset without ranking them by opportunity or urgency. Editorial teams cannot check 10,000 pages. Machine Learning models combine non-linear interactions across position tier, CTR deficit, freshness risk, content age, word count, and engagement signals into a smooth, calibrated probability that orders candidates by true upside.

---

## 2. Data safety

### Dataset Scope & Release Provenance
- **Dataset Used:** FlyRank Anonymized Starter Dataset (`data/raw/content_refresh_anonymized.csv`), containing 30,000 content items across 32 pseudonymized clients, anchored to the FlyRank Pseudonymized Warehouse Release (`flyrank_pseudonymized_warehouse_release_v20260703` on Hugging Face).
- **Date Windows:** 90-day trailing performance window (`impressions_90d`, `clicks_90d`, `sessions_90d`), comparing 30-day prior signals (`impressions_prev_30d`) against target window outcomes (`impressions_last_30d`).

### Field Classification & Privacy Safeguards

| Bucket | Fields Included | Rationale / Timing |
|---|---|---|
| **Features** | `impressions_90d`, `clicks_90d`, `sessions_90d`, `avg_position`, `ctr`, `word_count`, `content_age_days`, `days_since_last_update`, `engagement_rate`, `scroll_rate`, `search_volume`, `cpc`, plus categorical tiers | Knowable strictly BEFORE the prediction/decision moment. |
| **Label** | `is_declining_label` (`trend_direction == 'down'`) | Target proxy identifying >20% traffic drop. |
| **Context** | `client_id`, `content_id`, `content_type` | Used strictly for grouping, joining, and client-holdout validation splits. |
| **Excluded** | `trend_direction`, `trend_pct`, `impressions_last_30d`, `clicks_last_30d`, `health_score`, product decision flags | Target-derived or future-window metrics that introduce feature leakage. |

### Privacy & Leakage Audit
- All client names, domain names, URLs, article titles, and search query strings were pseudonymized or stripped before release.
- In `work/notebooks/w03_feature_leakage_check.ipynb`, a deliberate trap experiment proved that injecting outcome period metrics (`impressions_last_30d`) produces an artificially inflated accuracy (~97.8%), whereas our honest feature vector achieves an authentic 0.750 ROC-AUC without future leakage.

---

## 3. Baseline

### Hand-Written Rule Formula
Our Week-4 baseline score combines four observable signals into a transparent hand-written priority score between 0 and 100:

$$\text{Baseline Score} = 0.40 \\cdot \\text{Visibility} + 0.30 \\cdot \\text{Freshness Risk} + 0.25 \\cdot \\text{Position Opportunity} + 0.05 \\cdot \\text{Depth Gap}$$

Where:
- $\\text{Visibility} = \\text{PercentileRank}(\\log(1 + \\text{impressions\\_90d}))$
- $\\text{Freshness Risk} = \\text{PercentileRank}(\\text{days\\_since\\_last\\_update})$
- $\\text{Position Opportunity} = (1 - \\text{Normalize}(\\text{avg\\_position})) \\cdot \\text{Visibility}$
- $\\text{Depth Gap} = (1 - \\text{PercentileRank}(\\text{word\\_count})) \\cdot \\text{Visibility}$

### Baseline Performance on Client-Holdout Test Split
- **Precision@20:** 0.250
- **Precision@50:** 0.240
- **Precision@100:** 0.360
- **ROC-AUC:** 0.627 / 0.648
- **Average Precision:** 0.468

---

## 4. Model / analysis

### Machine Learning Pipeline
We evaluated three supervised models built on our 30-feature vector (numeric signals + one-hot encoded categorical tiers):
1. **Logistic Regression:** Linear pipeline with `StandardScaler` and balanced class weighting.
2. **Decision Tree:** Shallow interpretable tree (`max_depth=5`, `min_samples_leaf=50`).
3. **Random Forest:** Ensemble of 100 decision trees (`max_depth=10`, `min_samples_leaf=25`, `class_weight='balanced_subsample'`).

### Target Definition
$$\\text{is\\_declining\\_label} = \\begin{cases} 1 & \\text{if } \\text{trend\\_direction} = \\text{'down'} \\\\ 0 & \\text{otherwise} \\end{cases}$$

---

## 5. Evaluation

### Client-Holdout Validation Design
To prevent domain-signature leakage (where pages from the same client domain land in both train and test sets), we split the 30,000 dataset by holding out **6 entire client portfolios (20% of clients / 2,325 pages)** for testing, training on the remaining 26 clients (27,675 pages).

### Model vs Baseline Comparison Table (Evaluated on Holdout Test Split)

| Method / Model | Base Rate | Precision@20 | Precision@50 | Precision@100 | ROC-AUC | PR-AUC | Accuracy | F1 Score |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Week-4 Baseline Rule** | 39.1% | 0.250 | 0.240 | 0.360 | 0.648 | 0.480 | 0.622 | 0.528 |
| **Logistic Regression** | 39.1% | 0.350 | 0.400 | 0.440 | 0.700 | 0.522 | 0.661 | 0.566 |
| **Decision Tree** | 39.1% | 0.550 | 0.620 | 0.600 | 0.742 | 0.575 | 0.677 | 0.634 |
| **Random Forest (Best)** | **39.1%** | **0.750** | **0.740** | **0.750** | **0.750** | **0.618** | **0.671** | **0.636** |

### Key Result
The **Random Forest** classifier outperforms the baseline rule on every metric, delivering a **3.08x lift in Precision@50 (0.740 vs 0.240)**. Out of the top 50 pages recommended by the Random Forest model, 37 are true decay candidates, compared to only 12 for the baseline rule.

---

## 6. Interpretation

### Top Feature Importances (Random Forest)
1. **`days_with_impressions` (13.7%):** Measures historical SERP consistency.
2. **`log_impressions_90d` (12.4%):** Captures total search demand volume.
3. **`avg_position` (11.3%):** Identifies striking-distance vs deep SERP placement.
4. **`content_age_days` (9.3%):** Indicates content staleness risk.
5. **`log_clicks_90d` (3.9%):** Measures historical organic click throughput.

### Signal Audit Insights & Nuanced Findings
- **Content Performance Curve:** Content performance peaks at 61–90 days (mean health score 33.1) and hits a decay cliff at 271–365 days (health score 14).
- **The Freshness Multiplier:** Updating mature pages (>365 days old) yields a 3.2x health boost and up to 57x impression lift compared to unrevised stale pages.
- **Search Volume Myth Debunked:** Stored keyword search volume correlates weakly with actual page impressions ($r = 0.0083$). 82.9% of active pages outpace their nominal keyword benchmark.

---

## 7. Recommendation

### Final Action Playbook Queue Formula
$$\\text{Final Refresh Score} = 100 \\cdot \\left(0.70 \\cdot \\text{Prob}_{\\text{RandomForest}} + 0.30 \\cdot \\text{Score}_{\\text{Baseline}}\\right)$$

### Action Categorization & Reason Codes

| Reason Code | Trigger Condition | Recommended Editorial Action |
|---|---|---|
| `model_decline_risk` | Model Prob $\\ge 0.65$ | Full content audit, update stale statistics, add missing subtopics. |
| `ctr_review_candidate` | Imp $\\ge 500$, Pos 1–20, CTR $< 0.5\\%$ | Rewrite page title & meta description to match SERP search intent. |
| `stale_visible_page` | Days Since Update $\\ge 180$, Imp $\\ge 500$ | Recency update: refresh facts, dates, links, and re-submit for indexing. |
| `thin_visible_page` | Word Count $< 1200$, Imp $\\ge 250$ | Expand content coverage with missing subtopics and structural depth. |

### Human Review Protocol & No-Go Rules
- **Human Protocol:** Editors must manually inspect SERP intent, check for keyword cannibalization, and verify topical accuracy before publishing updates.
- **No-Go List:** NEVER rewrite top-performing Page 1 assets (pos 1–3) with stable traffic. NEVER pad thin pages with low-quality AI text without expanding genuine user value.

---

## 8. Reproducibility

### Environment & Execution Instructions
To re-run the entire pipeline and generate all artifacts from a fresh clone:

```bash
git clone https://github.com/meer140/flyrank-ml-internship-project.git
cd flyrank-ml-internship-project
pip install -r requirements.txt
$env:PYTHONIOENCODING="utf-8"; python scripts/run_all.py
```

- **Random Seed:** `42` fixed across all splits and model training.
- **Dependencies:** Python 3.13+, `pandas`, `numpy`, `scikit-learn`, `duckdb`, `pypdf`.

---

## 9. Acknowledgments & data credit

Built on the FlyRank ML Internship dataset — [https://flyrank.ai](https://flyrank.ai/). Crediting our data source is standard research practice; special thanks to Mirza Ašćerić and the FlyRank engineering team for providing the pseudonymized search warehouse release.
