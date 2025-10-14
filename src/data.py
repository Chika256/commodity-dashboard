"""Data access layer for commodity prices.

Real implementations with caching and retries arrive in later commits.
"""

from __future__ import annotations

from typing import Iterable

import pandas as pd


def fetch_prices(
    tickers: Iterable[str], start: str | None = None, end: str | None = None
) -> pd.DataFrame:
    """Temporary stub that raises while the data layer is under construction."""
    raise NotImplementedError("Data fetching will be implemented in the data-layer commit.")
