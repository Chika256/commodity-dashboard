# Development Log

## 2025-10-14
- **Change:** Initialized project structure, added documentation skeleton, configured tooling manifests.
- **Why:** Establish a professional baseline that mirrors front-office engineering discipline.
- **Alternatives considered:** Starting with code-only scaffold, but opted to front-load documentation to reinforce clarity.

## 2025-10-14
- **Change:** Implemented Pydantic settings and resilient data fetching with transformation tests.
- **Why:** Ensure downstream analytics receive clean, validated market data with predictable schema.
- **Alternatives considered:** Calling yfinance per ticker (simpler) but rejected to avoid N+1 network calls.

## 2025-10-14
- **Change:** Delivered analytics layer covering returns, moving averages, and alert-ready daily change calculations.
- **Why:** Traders need both momentum context and percent move summaries to act on pricing signals.
- **Alternatives considered:** Calculating metrics directly in Streamlit, but that would complicate testing and reuse.

## 2025-10-14
- **Change:** Built Streamlit UI with Plotly charts, KPI alerts, caching, and CSV export.
- **Why:** Showcase front-office friendly UX where traders can filter, visualise, and react quickly.
- **Alternatives considered:** Bokeh dashboard, but Streamlit aligned better with rapid prototyping and deployment simplicity.

## 2025-10-14
- **Change:** Added Streamlit dark theme and documented UI polish decisions.
- **Why:** Align the demo with real trading floors that prefer low-glare dashboards.
- **Alternatives considered:** Leaving the default Streamlit theme, but it felt too clinical for the target audience.
