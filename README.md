# CCI Commodity Dashboard

A real-time commodity price monitoring dashboard built for showcasing front-office engineering skills relevant to Castleton Commodities International (CCI). The dashboard surfaces live market data, contextual analytics, and visualizations to support trading decisions for WTI crude, Brent, Natural Gas, Gold, and Silver.

## Why it matters for a front-office internship
- Demonstrates ability to build resilient data pipelines and latency-aware UIs that traders rely on.
- Highlights familiarity with commodities markets, intraday analytics, and risk-aware alerting.
- Showcases production-ready Python tooling (testing, linting, pre-commit) expected in CCI engineering teams.

## Features
- Streamlit UI with interactive filters for tickers, date range, price interval, moving averages, and alert thresholds.
- Live data retrieval via `yfinance` with caching to minimize redundant network calls.
- Analytics including daily returns, rolling moving averages, and day-over-day percentage changes.
- Plotly charts for price history and returns, plus tabular snapshots of the latest market context.
- Alert callouts when daily percentage moves breach user-defined thresholds.

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
