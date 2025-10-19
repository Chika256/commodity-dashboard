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

## 2025-10-14
- **Change:** Adjusted data-layer unit test to assert our wrapped `DataDownloadError` contract.
- **Why:** Keeps test expectations aligned with the retry logic surfacing root causes via exception chaining.
- **Alternatives considered:** Relaxing the error handling to bubble raw ValueErrors, but that would leak inconsistent messaging into the UI.

## 2025-10-14
- **Change:** Applied Ruff fixes, modern typing updates, and tightened chart hover templates.
- **Why:** Keeps the codebase idiomatic and ensures lint/test automation passes cleanly for recruiters.
- **Alternatives considered:** Suppressing Ruff warnings, but we chose to embrace the recommendations for long-term maintainability.

## 2025-10-14
- **Change:** Replaced the frozen dataclass-based `DataDownloadError` with a standard exception to play nicely with Streamlit caching internals.
- **Why:** Streamlit reassigns `__traceback__` on cached exceptions; the frozen dataclass blocked that and crashed the UI.
- **Alternatives considered:** Catching the Streamlit context manager earlier, but the cleaner fix was to make the exception mutable like other RuntimeError subclasses.
