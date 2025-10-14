# Architecture Overview

This document explains how the CCI Commodity Dashboard pulls market data, computes analytics, and presents interactive visuals.

## High-level flow
```
+------------------+       +-------------------+       +-----------------+       +------------------+
| Streamlit UI     |  -->  | Data Layer        |  -->  | Analytics Layer |  -->  | Plotting Layer   |
| (app.py)         |       | (src/data.py)     |       | (src/analytics) |       | (src/plotting)   |
+------------------+       +-------------------+       +-----------------+       +------------------+
         ^                         |                          |                         |
         |                         v                          v                         v
         |                +-------------------+       +-----------------+       +------------------+
         |                | Pydantic Config   |       | Cached datasets |       | Plotly figures    |
         |                | (src/config.py)   |       | (st.cache_data) |       | returned to UI    |
         |                +-------------------+       +-----------------+       +------------------+
         |
         +------------------------- User input drives parameter selection ------------------------->
```

## Modules
- `src/config.py`: Centralized configuration using Pydantic models. Keeps defaults (tickers, lookback windows, cache TTL) and validates environment overrides.
- `src/data.py`: Responsible for batched downloads from `yfinance`, cache control, schema validation, and retry logic to handle transient network failures.
- `src/analytics.py`: Houses pure functions for computing returns, moving averages, and daily change metrics. Designed for unit modularity and easy testing.
- `src/plotting.py`: Builds Plotly figures with consistent styling, tooltips, and accessibility-focused labeling.
- `app.py`: Streamlit presentation layer that orchestrates configuration, fetches data, calls analytics, renders charts, and surfaces alerts.

## Caching strategy
- `st.cache_data` wraps the data-fetch function to memoize results per `(tickers, start, end, interval)` key.
- Cache TTL defaulted from configuration (e.g., 5 minutes) to balance speed and freshness.
- Additional in-function defensive caching (local dictionary) may be used for derived computations to avoid recomputation.

## Error handling
- The data layer implements retries with exponential backoff for `yfinance` calls, surfacing user-friendly messages in the UI when data is temporarily unavailable.
- Validation ensures required columns (`Open`, `High`, `Low`, `Close`, `Volume`) exist before analytics run.
- App-level error boundaries capture exceptions, presenting actionable remediation steps (e.g., widen the date range, reduce tickers).

## Decisions & trade-offs
- **Streamlit for UI**: Enables rapid, interactive dashboards without heavy frontend work. Trade-off: less granular control vs. React, but acceptable for fast prototypes.
- **yfinance data source**: Free and accessible without keys. Trade-off: Dependent on Yahoo Finance uptime; mitigated via retries and caching.
- **Plotly**: Delivers interactive charts with zoom/hover features. Trade-off: Slightly heavier than Matplotlib, but the interactivity is valuable for traders.
- **Testing with pytest**: Keeps analytics/data logic reliable. Integration tests are limited due to network constraints; mitigated by mocking in unit tests.
- **Pre-commit tooling**: Forces consistent style and linting. Slight onboarding overhead but critical for production-quality submissions.
