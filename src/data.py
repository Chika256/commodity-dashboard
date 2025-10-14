"""Data fetching utilities for the commodity dashboard."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Iterable, Sequence

import pandas as pd
import yfinance as yf

from .config import get_settings

LOGGER = logging.getLogger(__name__)

_REQUIRED_COLUMNS = ("Open", "High", "Low", "Close", "Adj Close", "Volume")


@dataclass(frozen=True)
class DataDownloadError(RuntimeError):
    """Raised when the Yahoo Finance request fails after retries."""

    message: str

    def __str__(self) -> str:  # pragma: no cover - delegation keeps repr tidy
        return self.message


def _prepare_index(data: pd.DataFrame, tickers: Sequence[str]) -> pd.DataFrame:
    """Re-shape yfinance output into a tidy dataframe.

    Parameters
    ----------
    data:
        DataFrame returned by ``yfinance.download``.
    tickers:
        Tickers requested, used when the result is single-column.
    """

    if isinstance(data.columns, pd.MultiIndex):
        tidy = data.stack(level=1).rename_axis(index=["datetime", "ticker"]).reset_index()
    else:
        # yfinance returns a flat index for single tickers; pivot to match multi format.
        tidy = (
            data.reset_index()
            .assign(ticker=tickers[0])
            .rename(columns={data.index.name or "Date": "datetime"})
        )
    return tidy


def _normalise_columns(tidy: pd.DataFrame) -> pd.DataFrame:
    """Rename yfinance columns and ensure dtypes are consistent."""

    column_map = {
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Adj Close": "adj_close",
        "Volume": "volume",
    }
    missing = [col for col in _REQUIRED_COLUMNS if col not in tidy.columns]
    if missing:
        raise ValueError(f"Missing columns in price data: {missing}")

    renamed = tidy.rename(columns=column_map)
    renamed["datetime"] = pd.to_datetime(renamed["datetime"], utc=True)

    float_cols = ["open", "high", "low", "close", "adj_close"]
    for column in float_cols:
        renamed[column] = pd.to_numeric(renamed[column], errors="coerce").astype(float)
    renamed["volume"] = pd.to_numeric(renamed["volume"], errors="coerce").fillna(0).astype(int)

    renamed = renamed.sort_values(["ticker", "datetime"]).reset_index(drop=True)
    return renamed[["ticker", "datetime", "open", "high", "low", "close", "adj_close", "volume"]]


def fetch_prices(
    tickers: Iterable[str],
    start: str | pd.Timestamp | None = None,
    end: str | pd.Timestamp | None = None,
    interval: str | None = None,
    retries: int | None = None,
    backoff: float | None = None,
) -> pd.DataFrame:
    """Download price data for the supplied tickers.

    Parameters
    ----------
    tickers:
        Iterable of ticker symbols accepted by Yahoo Finance.
    start, end:
        Optional boundaries for the download window (inclusive). Accepts strings or
        :class:`pandas.Timestamp` objects.
    interval:
        Sampling cadence (e.g., ``"1d"``, ``"1h"``, ``"5m"``). Defaults to the
        configuration value when omitted.
    retries:
        Override retry attempts for unit tests or specialised flows.
    backoff:
        Override exponential backoff multiplier.
    """

    tickers = tuple(dict.fromkeys(tickers))  # Removes duplicates while preserving order.
    settings = get_settings()

    if not tickers:
        raise ValueError("At least one ticker is required to fetch prices.")
    if len(tickers) > settings.max_tickers:
        raise ValueError(
            f"Requested {len(tickers)} tickers but max_tickers is {settings.max_tickers}."
        )

    interval = interval or settings.default_interval
    retries = retries or settings.data_fetch_retries
    backoff = backoff or settings.data_fetch_backoff

    attempt = 0
    delay = 0.0
    last_exception: Exception | None = None

    while attempt < retries:
        if delay:
            time.sleep(delay)
        try:
            raw = yf.download(
                tickers=" ".join(tickers),
                start=start,
                end=end,
                interval=interval,
                auto_adjust=False,
                progress=False,
                threads=True,
                group_by="ticker",
            )
            if raw is None or raw.empty:
                raise ValueError("Received empty dataframe from yfinance.")

            tidy = _prepare_index(raw, tickers)
            normalised = _normalise_columns(tidy)
            return normalised
        except Exception as exc:  # noqa: BLE001 - we need to retry on anything transient.
            last_exception = exc
            attempt += 1
            delay = backoff * attempt
            LOGGER.warning("Price download failed (attempt %s/%s): %s", attempt, retries, exc)

    message = "Price download failed after retries" if last_exception else "Unknown failure"
    raise DataDownloadError(message) from last_exception


__all__ = ["fetch_prices", "DataDownloadError"]
