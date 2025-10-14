"""Analytics helpers for commodity price series."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

import numpy as np
import pandas as pd

_REQUIRED_COLUMNS = {"ticker", "datetime", "adj_close", "close"}


def _validate_frame(
    price_frame: pd.DataFrame, required: Sequence[str] | None = None
) -> pd.DataFrame:
    """Ensure the dataframe contains the columns we rely on and is sorted.

    Returning a sorted copy keeps downstream analytics deterministic while leaving
    the caller's dataframe untouched (important for Streamlit state caching).
    """

    required = set(required or _REQUIRED_COLUMNS)
    missing = required.difference(price_frame.columns)
    if missing:
        raise ValueError(f"Dataframe is missing required columns: {sorted(missing)}")

    sorted_frame = price_frame.sort_values(["ticker", "datetime"]).reset_index(
        drop=True
    )
    return sorted_frame


def compute_daily_returns(price_frame: pd.DataFrame) -> pd.DataFrame:
    """Return percentage returns per observation for each ticker.

    The function uses adjusted close prices where available to better reflect the
    true economic return. Missing values are forward-filled before computing the
    percentage change to avoid dropping sparse intraday data.
    """

    frame = _validate_frame(price_frame)
    frame["adj_close"] = frame.groupby("ticker")["adj_close"].ffill()
    returns = frame.copy()
    returns["daily_return"] = (
        returns.groupby("ticker")["adj_close"]
        .pct_change()
        .replace([np.inf, -np.inf], np.nan)
    )
    returns["daily_return"] = returns["daily_return"].fillna(0.0)
    return returns[["ticker", "datetime", "daily_return"]]


def add_moving_averages(
    price_frame: pd.DataFrame, windows: Iterable[int]
) -> pd.DataFrame:
    """Add moving-average columns (``ma_<window>``) to the dataframe copy."""

    frame = _validate_frame(price_frame)
    windows = sorted({int(window) for window in windows if int(window) > 0})
    if not windows:
        raise ValueError("At least one positive moving-average window is required.")

    enriched = frame.copy()
    for window in windows:
        column_name = f"ma_{window}"
        enriched[column_name] = enriched.groupby("ticker", group_keys=False)[
            "adj_close"
        ].transform(lambda series, w=window: series.rolling(w, min_periods=1).mean())
    return enriched


def daily_change(price_frame: pd.DataFrame) -> pd.Series:
    """Return the latest day-over-day percentage change per ticker."""

    frame = _validate_frame(price_frame)
    latest_change = (
        frame.groupby("ticker", group_keys=True)["adj_close"]
        .apply(_latest_pct_change)
        .rename("daily_change")
    )
    return latest_change


def _latest_pct_change(series: pd.Series) -> float:
    """Helper that computes the last percentage move for a ticker series."""

    if len(series) < 2:
        return 0.0
    last, prev = series.iloc[-1], series.iloc[-2]
    if prev == 0:
        return 0.0
    return float((last - prev) / prev)


__all__ = [
    "compute_daily_returns",
    "add_moving_averages",
    "daily_change",
]
