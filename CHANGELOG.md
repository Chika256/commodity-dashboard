# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.6] - 2025-10-19
### Fixed
- Adopted pandas future_stack flag to silence stack() deprecation warnings in tests.

## [0.4.5] - 2025-10-19
### Fixed
- Updated Streamlit theme font to comply with supported options.
- Expanded Yahoo Finance retry message with network troubleshooting guidance and README tips.

## [0.4.4] - 2025-10-14
### Fixed
- Relaxed the custom `DataDownloadError` class so Streamlit caching can surface root causes without crashing.

## [0.4.3] - 2025-10-14
### Changed
- Harmonised code style with Ruff recommendations and refreshed Plotly builders.
- Re-ran Black formatting and tightened pytest configuration with caching helpers.

## [0.4.2] - 2025-10-14
### Changed
- Updated tests to expect `DataDownloadError` when schema validation fails during retries.

## [0.4.1] - 2025-10-14
### Added
- Dark theme configuration for Streamlit alongside documentation updates.
- README feature note highlighting the themed trading-floor experience.

## [0.4.0] - 2025-10-14
### Added
- Streamlit app with interactive controls, KPI metrics, alerts, and download option.
- Plotly chart builders for prices and returns with consistent styling.
- Smoke tests that exercise the cached data loader contract.

## [0.3.0] - 2025-10-14
### Added
- Analytics helpers for returns, moving averages, and daily change metrics with unit tests.

## [0.2.0] - 2025-10-14
### Added
- Centralised Pydantic settings with environment overrides and sensible defaults.
- Batched yfinance fetcher with retry/backoff logic and dataframe normalisation.

## [0.1.0] - 2025-10-14
### Added
- Initial repository structure with documentation, configuration scaffolding, and tooling manifests.
