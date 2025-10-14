"""Analytics helpers for commodity price series.

Functions are stubbed initially to keep the first commit focused on scaffolding.
"""

from __future__ import annotations

import pandas as pd


def compute_daily_returns(price_frame: pd.DataFrame) -> pd.DataFrame:
    """Compute daily returns once data layer is ready."""
    raise NotImplementedError("Analytics implementation lands in a later commit.")


def add_moving_averages(price_frame: pd.DataFrame, windows: tuple[int, ...]) -> pd.DataFrame:
    """Add moving averages to the dataset when analytics are implemented."""
    raise NotImplementedError("Moving averages will be added in analytics commit.")


def daily_change(price_frame: pd.DataFrame) -> float:
    """Return the most recent daily percentage change once implemented."""
    raise NotImplementedError("Daily change logic will follow once analytics exist.")
