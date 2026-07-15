# Nassau Candy Distributor — Shipping Route Efficiency Analysis

## Project Overview
This project analyzes factory-to-customer shipping route efficiency for Nassau Candy Distributor.
It covers 10,194 shipments across 5 factories, 4 regions, 4 ship modes, and 59 states/provinces.

## Problem Statement
Nassau Candy Distributor lacked visibility into which shipping routes were efficient and which
caused delays. This analysis builds that visibility using data-driven route benchmarking.

## Key Findings
- **Fastest Route:** Sugar Shack → Gulf (Efficiency Score: 100)
- **Slowest Route:** Sugar Shack → Pacific (Efficiency Score: 0)
- **Standard Class** shipping showed the lowest average lead time among all 4 ship modes
- **17 bottleneck states** identified (high volume + above-median lead time)
- **California** handles 19.6% of total shipment volume alone
- **Data Quality Finding:** Ship Date field has a systemic issue affecting 100% of records —
  lead time figures are directional, not literal

## Dashboard Pages
| Page | Description |
|------|-------------|
| Route Efficiency Overview | Bar chart + leaderboard of all 20 routes |
| Geographic Map | US choropleth heatmap by state |
| Ship Mode Comparison | Standard vs Expedited cost-time tradeoff |
| Route Drill-Down | State-level detail + order timeline + filters |

## How to Run
```bash
# Install dependencies
pip install streamlit pandas plotly

# Run the dashboard
cd dashboard
python -m streamlit run app.py
```

## Tech Stack
- **Python** — pandas, plotly, streamlit
- **Analysis:** Data cleaning, feature engineering, route aggregation, KPI benchmarking
- **Visualization:** Interactive Plotly charts, US choropleth map
- **Dashboard:** 4-page Streamlit web application

## Deliverables
- Research Paper (see Docs folder)
- Interactive Streamlit Dashboard
- Executive Summary for stakeholders

## Internship
**Organization:** Unified Mentor Pvt. Ltd.
**Duration:** April 2026 – Present
**Domain:** Data Analytics
