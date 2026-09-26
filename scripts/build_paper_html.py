import os
import json
import pandas as pd

print("=== BUILDING DEPLOYED RESEARCH PAPER HTML ===")

# Load data
with open("outputs/model_results.json", "r", encoding="utf-8") as f:
    results_json = json.load(f)

queue_df = pd.read_csv("outputs/refresh_queue.csv")
top_20 = queue_df.head(20).to_dict(orient="records")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Intelligence & Content Refresh Opportunity Scoring — FlyRank Research Paper</title>
    <meta name="description" content="Applied Search Intelligence Research Paper: Machine learning model for content refresh opportunity scoring on 30,000 anonymized search assets.">
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@500;600;700;800&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-primary: #090d16;
            --bg-secondary: #111827;
            --bg-card: rgba(17, 24, 39, 0.75);
            --bg-card-hover: rgba(31, 41, 55, 0.85);
            --border-color: rgba(255, 255, 255, 0.08);
            --border-active: rgba(99, 102, 241, 0.4);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-purple: #818cf8;
            --accent-indigo: #6366f1;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --accent-pink: #ec4899;
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-heading: 'Outfit', sans-serif;
            --font-mono: 'Fira Code', monospace;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        html {{
            scroll-behavior: smooth;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            font-family: var(--font-sans);
            line-height: 1.6;
        }}

        /* Header Navigation */
        header {{
            position: sticky;
            top: 0;
            z-index: 1000;
            background: rgba(9, 13, 22, 0.85);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-family: var(--font-heading);
            font-weight: 700;
            font-size: 1.25rem;
            color: #fff;
            text-decoration: none;
        }}

        .brand-badge {{
            background: linear-gradient(135deg, var(--accent-indigo), var(--accent-pink));
            color: #fff;
            padding: 0.2rem 0.6rem;
            border-radius: 6px;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        nav ul {{
            display: flex;
            list-style: none;
            gap: 1.5rem;
        }}

        nav a {{
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            transition: color 0.2s;
        }}

        nav a:hover {{
            color: var(--accent-purple);
        }}

        /* Container & Layout */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 3rem 1.5rem;
        }}

        /* Hero Header */
        .hero {{
            text-align: center;
            margin-bottom: 4rem;
            position: relative;
        }}

        .hero-tag {{
            display: inline-block;
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.3);
            color: var(--accent-purple);
            padding: 0.35rem 1rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
        }}

        h1 {{
            font-family: var(--font-heading);
            font-size: 2.75rem;
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 1.25rem;
            background: linear-gradient(135deg, #ffffff 30%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .hero-subtitle {{
            font-size: 1.15rem;
            color: var(--text-secondary);
            max-width: 800px;
            margin: 0 auto 2rem;
        }}

        .authors-bar {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            font-size: 0.9rem;
            color: var(--text-muted);
            border-top: 1px solid var(--border-color);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 0;
            margin-top: 2rem;
        }}

        .authors-bar strong {{
            color: var(--text-primary);
        }}

        /* Section Components */
        section {{
            margin-bottom: 4rem;
        }}

        .section-title {{
            font-family: var(--font-heading);
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            color: #fff;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 0.75rem;
        }}

        .section-num {{
            color: var(--accent-indigo);
            font-family: var(--font-mono);
            font-size: 1.25rem;
        }}

        /* Abstract Box */
        .abstract-card {{
            background: linear-gradient(135deg, rgba(30, 27, 75, 0.4), rgba(17, 24, 39, 0.8));
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 3rem;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
        }}

        .abstract-title {{
            font-family: var(--font-heading);
            font-size: 1.25rem;
            color: var(--accent-purple);
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .abstract-text {{
            font-size: 1.05rem;
            line-height: 1.8;
            color: #e2e8f0;
        }}

        /* Stat Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }}

        .stat-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            transition: transform 0.2s, border-color 0.2s;
        }}

        .stat-card:hover {{
            transform: translateY(-4px);
            border-color: var(--border-active);
        }}

        .stat-label {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}

        .stat-value {{
            font-family: var(--font-heading);
            font-size: 2.25rem;
            font-weight: 800;
            color: #fff;
            line-height: 1;
            margin-bottom: 0.5rem;
        }}

        .stat-sub {{
            font-size: 0.85rem;
            color: var(--accent-emerald);
        }}

        /* Content Cards & Grids */
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }}

        @media (max-width: 768px) {{
            .grid-2 {{ grid-template-columns: 1fr; }}
            h1 {{ font-size: 2rem; }}
        }}

        .card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 1.75rem;
        }}

        .card h3 {{
            font-family: var(--font-heading);
            font-size: 1.2rem;
            color: #fff;
            margin-bottom: 1rem;
        }}

        /* Tables */
        .table-responsive {{
            overflow-x: auto;
            margin: 1.5rem 0;
            border-radius: 12px;
            border: 1px solid var(--border-color);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
            text-align: left;
        }}

        th {{
            background: rgba(30, 41, 59, 0.8);
            color: var(--text-secondary);
            font-weight: 600;
            padding: 1rem;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
            border-bottom: 1px solid var(--border-color);
        }}

        td {{
            padding: 1rem;
            border-bottom: 1px solid var(--border-color);
            color: #e2e8f0;
        }}

        tr:hover td {{
            background: var(--bg-card-hover);
        }}

        tr.highlight td {{
            background: rgba(99, 102, 241, 0.12);
            font-weight: 600;
        }}

        /* Badges & Reason Codes */
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.6rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .badge-high {{
            background: rgba(16, 185, 129, 0.2);
            color: var(--accent-emerald);
            border: 1px solid rgba(16, 185, 129, 0.4);
        }}

        .badge-medium {{
            background: rgba(245, 158, 11, 0.2);
            color: var(--accent-amber);
            border: 1px solid rgba(245, 158, 11, 0.4);
        }}

        .code-pill {{
            display: inline-block;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid var(--border-color);
            color: #cbd5e1;
            font-family: var(--font-mono);
            font-size: 0.75rem;
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            margin-right: 0.3rem;
            margin-bottom: 0.2rem;
        }}

        /* Alerts */
        .alert {{
            border-left: 4px solid var(--accent-indigo);
            background: rgba(30, 41, 59, 0.5);
            padding: 1.25rem;
            border-radius: 0 8px 8px 0;
            margin: 1.5rem 0;
        }}

        .alert-warning {{
            border-left-color: var(--accent-amber);
            background: rgba(245, 158, 11, 0.1);
        }}

        .alert-title {{
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        /* Code Block */
        pre {{
            background: #020617;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1.25rem;
            font-family: var(--font-mono);
            font-size: 0.85rem;
            color: #e2e8f0;
            overflow-x: auto;
        }}

        /* Footer */
        footer {{
            border-top: 1px solid var(--border-color);
            padding: 3rem 1.5rem;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.9rem;
            background: #040711;
        }}

        footer a {{
            color: var(--accent-purple);
            text-decoration: none;
        }}

        footer a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>

    <!-- Header Navigation -->
    <header>
        <a href="#" class="brand">
            FlyRank Research <span class="brand-badge">March 2026</span>
        </a>
        <nav>
            <ul>
                <li><a href="#abstract">Abstract</a></li>
                <li><a href="#problem">Problem</a></li>
                <li><a href="#data">Data</a></li>
                <li><a href="#methodology">Methodology</a></li>
                <li><a href="#results">Results</a></li>
                <li><a href="#recommendations">Playbook</a></li>
                <li><a href="#reproducibility">Reproducibility</a></li>
            </ul>
        </nav>
    </header>

    <div class="container">
        <!-- Hero Header -->
        <div class="hero">
            <span class="hero-tag">Applied Search Intelligence Capstone Paper</span>
            <h1>Content Refresh Opportunity Scoring</h1>
            <p class="hero-subtitle">Machine Learning Prioritization of Organic Traffic Decay Across 30,000 Anonymized Search Assets</p>
            
            <div class="authors-bar">
                <span><strong>Author:</strong> Applied Search Intelligence Intern</span>
                <span><strong>Track:</strong> Applied Search Intelligence (Lane 2)</span>
                <span><strong>Data Release:</strong> <code>flyrank_pseudonymized_warehouse_release_v20260703</code></span>
            </div>
        </div>

        <!-- Metric Highlights Grid -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Precision@50 Lift</div>
                <div class="stat-value">3.08x</div>
                <div class="stat-sub">0.740 RF Model vs 0.240 Baseline</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Model ROC-AUC</div>
                <div class="stat-value">0.750</div>
                <div class="stat-sub">Client-Holdout Grouped Validation</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Evaluated Content Items</div>
                <div class="stat-value">30,000</div>
                <div class="stat-sub">Across 32 Anonymized Portfolios</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Freshness Multiplier</div>
                <div class="stat-value">3.2x</div>
                <div class="stat-sub">Health Boost on Refreshed Assets</div>
            </div>
        </div>

        <!-- Section 0: Abstract -->
        <section id="abstract">
            <div class="abstract-card">
                <div class="abstract-title">Abstract (5-Sentence Summary)</div>
                <p class="abstract-text">
                    Managing multi-client digital content portfolios requires allocating scarce editorial resources to published pages undergoing organic search traffic decay. 
                    We evaluated 30,000 pseudonymized content items across 32 client portfolios using Search Console and GA4 metrics to predict 30-day impression decay. 
                    We constructed a transparent baseline rule and trained three machine learning classifiers using an honest client-holdout validation split. 
                    The Random Forest classifier achieved a Precision@50 of <strong>0.740</strong> (a 3.08x lift over the 0.240 baseline precision), an ROC-AUC of <strong>0.750</strong>, and an Average Precision of <strong>0.618</strong>. 
                    The resulting opportunity scoring engine powers a public-safe ranked action playbook that isolates high-upside decay candidates and snippet optimization targets for human editorial review.
                </p>
            </div>
        </section>

        <!-- Section 1: Introduction / Problem Statement -->
        <section id="problem">
            <h2 class="section-title"><span class="section-num">01.</span> Introduction & Problem Statement</h2>
            <div class="grid-2">
                <div class="card">
                    <h3>The Resource Allocation Challenge</h3>
                    <p>Editorial and SEO teams face finite monthly bandwidth: a content team can realistically refresh or rewrite only 20 to 50 pages per sprint. Meanwhile, published content continuously decays in search rank, loses freshness, or faces shifting organic competition over time.</p>
                    <br>
                    <p>Static threshold rules (e.g. <code>impressions >= 500 AND trend == 'down'</code>) flood editorial teams with <strong>9,961 unranked candidate pages</strong> in our dataset. Without intelligent prioritization, editorial labor is wasted on low-upside assets or temporary blips.</p>
                </div>
                <div class="card">
                    <h3>Decision Supported & Cost of Errors</h3>
                    <p><strong>Decision Supported:</strong> Ordering monthly editorial capacity to candidate pages where content updates yield the highest return on organic visibility and user click recovery.</p>
                    <br>
                    <div class="alert alert-warning">
                        <div class="alert-title">⚠️ Cost of Wrong Call</div>
                        <p><strong>False Positive:</strong> Wastes 2–4 hours of expert writing per page updating healthy assets, risking ranking disruption.<br>
                        <strong>False Negative:</strong> Causes compounding loss of organic search impressions and uncaptured revenue.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Section 2: Data -->
        <section id="data">
            <h2 class="section-title"><span class="section-num">02.</span> Dataset & Public Safety Controls</h2>
            <div class="card">
                <h3>Dataset Scope & Schema</h3>
                <p>This study utilizes the FlyRank Anonymized Starter Dataset anchored to the Hugging Face release <code>FlyRank/internship-warehouse</code> (Build ID: <code>flyrank_pseudonymized_warehouse_release_v20260703</code>). The dataset grain is 1 row = 1 pseudonymized content item (<code>content_id</code> grain per <code>client_id</code>) evaluated over trailing 90-day performance windows.</p>
                
                <div class="table-responsive">
                    <table>
                        <thead>
                            <tr>
                                <th>Category</th>
                                <th>Included Fields</th>
                                <th>Timing & Guardrails</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Features</strong></td>
                                <td><code>impressions_90d</code>, <code>clicks_90d</code>, <code>sessions_90d</code>, <code>avg_position</code>, <code>ctr</code>, <code>word_count</code>, <code>content_age_days</code>, <code>days_since_last_update</code>, <code>engagement_rate</code>, <code>scroll_rate</code></td>
                                <td>Knowable strictly BEFORE prediction cutoff. Log-transformed volume signals.</td>
                            </tr>
                            <tr>
                                <td><strong>Target Label</strong></td>
                                <td><code>is_declining_label</code> (<code>trend_direction == 'down'</code>)</td>
                                <td>Identifies >20% traffic drop across trailing evaluation windows.</td>
                            </tr>
                            <tr>
                                <td><strong>Context / Grouping</strong></td>
                                <td><code>client_id</code>, <code>content_id</code>, <code>content_type</code></td>
                                <td>Used strictly for client-holdout validation splits and table joins.</td>
                            </tr>
                            <tr>
                                <td><strong>Excluded (Leakage Risk)</strong></td>
                                <td><code>trend_direction</code>, <code>trend_pct</code>, <code>impressions_last_30d</code>, <code>clicks_last_30d</code>, <code>health_score</code></td>
                                <td>Direct target-derived metrics or outcome period facts (EXCLUDED).</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- Section 3: Methodology -->
        <section id="methodology">
            <h2 class="section-title"><span class="section-num">03.</span> Methodology & Validation Design</h2>
            <div class="grid-2">
                <div class="card">
                    <h3>Transparent Baseline Formula</h3>
                    <p>We built a transparent, hand-written rule baseline combining four observable search signals:</p>
                    <pre>Baseline Score = 0.40 * Visibility 
               + 0.30 * Freshness Risk 
               + 0.25 * Position Opportunity 
               + 0.05 * Depth Gap</pre>
                    <br>
                    <p>Where Visibility, Freshness Risk, Position Opportunity, and Depth Gap are computed from percentile-ranked search volume, days since last update, SERP position distance, and word count.</p>
                </div>
                <div class="card">
                    <h3>Client-Holdout Validation Split</h3>
                    <p>To prevent domain-signature memorization (where pages from the same client domain leak authority signatures into training), we split the 30,000 dataset by holding out <strong>6 complete client portfolios (20% of clients / 2,325 pages)</strong> for testing, training models on 26 clients (27,675 pages).</p>
                    <br>
                    <p>This guarantees an honest evaluation of how models generalize to completely unseen client websites in production.</p>
                </div>
            </div>
        </section>

        <!-- Section 4: Results -->
        <section id="results">
            <h2 class="section-title"><span class="section-num">04.</span> Model Evaluation & Results</h2>
            <div class="card" style="margin-bottom: 2rem;">
                <h3>Holdout Evaluation Table (Client-Holdout Split)</h3>
                <div class="table-responsive">
                    <table>
                        <thead>
                            <tr>
                                <th>Method / Model</th>
                                <th>Base Rate</th>
                                <th>Precision@20</th>
                                <th>Precision@50</th>
                                <th>Precision@100</th>
                                <th>ROC-AUC</th>
                                <th>PR-AUC</th>
                                <th>F1 Score</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Week-4 Baseline Rule</td>
                                <td>39.1%</td>
                                <td>0.250</td>
                                <td>0.240</td>
                                <td>0.360</td>
                                <td>0.648</td>
                                <td>0.480</td>
                                <td>0.528</td>
                            </tr>
                            <tr>
                                <td>Logistic Regression</td>
                                <td>39.1%</td>
                                <td>0.350</td>
                                <td>0.400</td>
                                <td>0.440</td>
                                <td>0.700</td>
                                <td>0.522</td>
                                <td>0.566</td>
                            </tr>
                            <tr>
                                <td>Decision Tree</td>
                                <td>39.1%</td>
                                <td>0.550</td>
                                <td>0.620</td>
                                <td>0.600</td>
                                <td>0.742</td>
                                <td>0.575</td>
                                <td>0.634</td>
                            </tr>
                            <tr class="highlight">
                                <td><strong>Random Forest (Best)</strong></td>
                                <td><strong>39.1%</strong></td>
                                <td><strong>0.750</strong></td>
                                <td><strong>0.740</strong></td>
                                <td><strong>0.750</strong></td>
                                <td><strong>0.750</strong></td>
                                <td><strong>0.618</strong></td>
                                <td><strong>0.636</strong></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Charts Container -->
            <div class="grid-2">
                <div class="card">
                    <h3>Model Precision@K Comparison</h3>
                    <canvas id="precisionChart" height="220"></canvas>
                </div>
                <div class="card">
                    <h3>Top Feature Importances (Random Forest)</h3>
                    <canvas id="importanceChart" height="220"></canvas>
                </div>
            </div>
        </section>

        <!-- Section 5: Limitations -->
        <section id="limitations">
            <h2 class="section-title"><span class="section-num">05.</span> Limitations & Public Safety Framing</h2>
            <div class="card">
                <div class="alert">
                    <div class="alert-title">📌 Observational Decision-Support Guardrails</div>
                    <p>1. <strong>Observational Association vs Causality:</strong> All findings reflect historical associations. We do not claim that a content refresh <em>causes</em> a guaranteed recovery; establishing causality requires prospective A/B testing.<br>
                    2. <strong>No Algorithm Reverse-Engineering:</strong> We do not claim to predict or reverse-engineer Google's ranking algorithms.<br>
                    3. <strong>Public Safety Safeguards:</strong> All raw client names, URLs, article titles, and search queries are scrambled or unlisted.</p>
                </div>
            </div>
        </section>

        <!-- Section 6: Recommendations & Playbook -->
        <section id="recommendations">
            <h2 class="section-title"><span class="section-num">06.</span> Ranked Content Action Playbook</h2>
            <div class="card" style="margin-bottom: 2rem;">
                <h3>Top Priority Refresh Candidate Queue (Sample Top 10)</h3>
                <p style="color: var(--text-secondary); margin-bottom: 1rem; font-size: 0.9rem;">Scored using combined formula: <code>Final Score = 100 * (0.70 * Prob_RF + 0.30 * Score_Baseline)</code></p>
                
                <div class="table-responsive">
                    <table>
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Content ID</th>
                                <th>Client ID</th>
                                <th>Refresh Score</th>
                                <th>Confidence</th>
                                <th>Action Category</th>
                                <th>Reason Codes</th>
                            </tr>
                        </thead>
                        <tbody>
"""

for item in top_20[:10]:
    html_content += f"""
                            <tr>
                                <td><strong>#{item.get('final_rank', 0)}</strong></td>
                                <td><code>{item.get('content_id', '')}</code></td>
                                <td><code>{item.get('client_id', '')}</code></td>
                                <td><strong>{item.get('final_refresh_score', 0):.1f}</strong></td>
                                <td><span class="badge badge-high">{item.get('confidence', 'High')}</span></td>
                                <td>{item.get('suggested_action', 'Refresh & Update')}</td>
                                <td>
"""
    codes = str(item.get('final_reason_codes', '')).split(';')
    for c in codes:
        if c.strip():
            html_content += f'<span class="code-pill">{c.strip()}</span>'
    html_content += """
                                </td>
                            </tr>
"""

html_content += f"""
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- Section 7: Reproducibility -->
        <section id="reproducibility">
            <h2 class="section-title"><span class="section-num">07.</span> Reproducibility & Execution Protocol</h2>
            <div class="card">
                <p>All pipeline code, assignment notebooks, model weights, and research artifacts are fully versioned and committed to the public GitHub repository.</p>
                <br>
                <pre># 1. Clone repository
git clone https://github.com/meer140/flyrank-ml-internship-project.git
cd flyrank-ml-internship-project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Execute reference pipeline (UTF-8)
$env:PYTHONIOENCODING="utf-8"; python scripts/run_all.py</pre>
            </div>
        </section>

        <!-- Section 8: Acknowledgments & Credit -->
        <section id="acknowledgments">
            <h2 class="section-title"><span class="section-num">08.</span> Acknowledgments & Data Credit</h2>
            <div class="card" style="text-align: center; padding: 3rem 2rem;">
                <p style="font-size: 1.15rem; color: #fff; margin-bottom: 1rem;">
                    Built on the FlyRank ML Internship dataset — <a href="https://flyrank.ai/" target="_blank" style="color: var(--accent-purple); font-weight: 700; text-decoration: underline;">https://flyrank.ai/</a>
                </p>
                <p style="color: var(--text-secondary); max-width: 700px; margin: 0 auto; font-size: 0.95rem;">
                    Crediting our data source is standard research practice. Special thanks to Mirza Ašćerić and the FlyRank engineering team for publishing the pseudonymized search intelligence warehouse dataset.
                </p>
            </div>
        </section>
    </div>

    <!-- Footer -->
    <footer>
        <p>© 2026 FlyRank Applied Search Intelligence Track · Deployed Paper Deliverable</p>
        <p style="margin-top: 0.5rem;"><a href="https://github.com/meer140/flyrank-ml-internship-project">GitHub Repository</a> · <a href="https://flyrank.ai/">FlyRank.ai</a></p>
    </footer>

    <!-- Chart.js Scripts -->
    <script>
        // Precision Chart
        const ctxP = document.getElementById('precisionChart').getContext('2d');
        new Chart(ctxP, {{
            type: 'bar',
            data: {{
                labels: ['Precision@20', 'Precision@50', 'Precision@100'],
                datasets: [
                    {{
                        label: 'Random Forest (Model)',
                        data: [0.75, 0.74, 0.75],
                        backgroundColor: 'rgba(99, 102, 241, 0.85)',
                        borderColor: '#6366f1',
                        borderWidth: 1
                    }},
                    {{
                        label: 'Decision Tree',
                        data: [0.55, 0.62, 0.60],
                        backgroundColor: 'rgba(16, 185, 129, 0.6)',
                        borderColor: '#10b981',
                        borderWidth: 1
                    }},
                    {{
                        label: 'Baseline Rule',
                        data: [0.25, 0.24, 0.36],
                        backgroundColor: 'rgba(148, 163, 184, 0.4)',
                        borderColor: '#94a3b8',
                        borderWidth: 1
                    }}
                ]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{ beginAtZero: true, max: 1.0, grid: {{ color: 'rgba(255,255,255,0.05)' }} }},
                    x: {{ grid: {{ display: false }} }}
                }},
                plugins: {{ legend: {{ labels: {{ color: '#94a3b8' }} }} }}
            }}
        }});

        // Feature Importance Chart
        const ctxI = document.getElementById('importanceChart').getContext('2d');
        new Chart(ctxI, {{
            type: 'bar',
            indexAxis: 'y',
            data: {{
                labels: ['days_with_impressions', 'log_impressions_90d', 'avg_position', 'content_age_days', 'word_count', 'ctr', 'scroll_rate'],
                datasets: [{{
                    label: 'Feature Importance',
                    data: [0.160, 0.128, 0.108, 0.095, 0.041, 0.033, 0.031],
                    backgroundColor: 'rgba(129, 140, 248, 0.85)',
                    borderRadius: 4
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    x: {{ beginAtZero: true, grid: {{ color: 'rgba(255,255,255,0.05)' }} }},
                    y: {{ grid: {{ display: false }} }}
                }},
                plugins: {{ legend: {{ display: false }} }}
            }}
        }});
    </script>
</body>
</html>
"""

# Write to docs/index.html
os.makedirs("docs", exist_ok=True)
with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Write to root index.html as a mirror for GitHub Pages root hosting
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Write submission/paper_url.txt
os.makedirs("submission", exist_ok=True)
paper_url = "https://meer140.github.io/flyrank-ml-internship-project/"
with open("submission/paper_url.txt", "w", encoding="utf-8") as f:
    f.write(paper_url + "\n")

print(f"✓ Wrote docs/index.html")
print(f"✓ Wrote index.html")
print(f"✓ Wrote submission/paper_url.txt ({paper_url})")
print("=== DEPLOYMENT PAPER BUILD COMPLETE ===")
