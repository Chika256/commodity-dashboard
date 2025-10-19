# CCI Commodity Dashboard

A real-time commodity price monitoring dashboard. The dashboard surfaces live market data, contextual analytics, and visualizations to support trading decisions for WTI crude, Brent, Natural Gas, Gold, and Silver.

## Why it matters for a front-office internship
- Demonstrates ability to build resilient data pipelines and latency-aware UIs that traders rely on.
- Highlights familiarity with commodities markets, intraday analytics, and risk-aware alerting.
- Showcases production-ready Python tooling (testing, linting, pre-commit) expected in CCI engineering teams.

## Features
- Streamlit UI with interactive filters for tickers, date range, price interval, moving averages, and alert thresholds.
- Live data retrieval via `yfinance` with caching to minimize redundant network calls.
- Analytics including daily returns, rolling moving averages, and day-over-day percentage changes.
- Plotly charts for price history and returns, plus tabular snapshots of the latest market context.
- KPI header with automated alerts when daily percentage moves breach user-defined thresholds.
- One-click CSV export so candidates can share example market snapshots with interviewers.
- Trading-floor inspired dark theme configured via `.streamlit/config.toml`.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
pre-commit install
streamlit run app.py
```

## Tests
```bash
pytest
```

## Troubleshooting
- If the dashboard shows an “Unable to download data” message, Yahoo Finance may be blocked by your VPN or network filter. Try disconnecting from restrictive networks, widen the date range, or fall back to the daily interval.
- Streamlit caches memoized responses; use the `⋮` menu → **Clear cache** if you change environments or encounter stale data.

## Screenshot
![Dashboard preview](docs/assets/dashboard-preview.png "Placeholder preview - replace with actual screenshot once captured")

## Project structure
```
cci-commodity-dashboard/
├─ app.py
├─ src/
│  ├─ config.py
│  ├─ data.py
│  ├─ analytics.py
│  └─ plotting.py
├─ tests/
│  ├─ test_data.py
│  ├─ test_analytics.py
│  └─ test_smoke.py
├─ docs/
│  ├─ DEVLOG.md
│  └─ ROADMAP.md
├─ README.md
├─ ARCHITECTURE.md
├─ ELI5.md
├─ CHANGELOG.md
└─ requirements.txt
```

## Contributing
1. Create a feature branch.
2. Ensure formatting via `black` and linting with `ruff`.
3. Run `pytest` before opening a pull request.
4. Update `CHANGELOG.md` and `docs/DEVLOG.md` with the change rationale.

## License
MIT License. See [LICENSE](LICENSE) if added in future roadmap.
