"""Tests for the data fetching utilities."""

from __future__ import annotations

from typing import Any, Dict

import pandas as pd
import pytest

from src import data


class DummyDownloader:
    """Utility to capture arguments passed to yfinance.download during tests."""

    def __init__(self, frame: pd.DataFrame):
        self.frame = frame
        self.calls: list[Dict[str, Any]] = []

    def __call__(self, *args: Any, **kwargs: Any) -> pd.DataFrame:
        self.calls.append({"args": args, "kwargs": kwargs})
        return self.frame


def _sample_multi_index_frame() -> pd.DataFrame:
    dates = pd.date_range("2024-01-01", periods=2, freq="D")
    columns = pd.MultiIndex.from_product(
        [["Open", "High", "Low", "Close", "Adj Close", "Volume"], ["CL=F", "BZ=F"]]
    )
    values = [
        [72, 74, 70, 73, 73, 1000, 68, 70, 66, 69, 69, 900],
        [73, 75, 71, 74, 74, 1100, 69, 71, 67, 70, 70, 950],
    ]
    return pd.DataFrame(values, index=dates, columns=columns)


def _sample_single_ticker_frame() -> pd.DataFrame:
    dates = pd.date_range("2024-01-01", periods=2, freq="D")
    columns = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
    values = [
        [25.5, 26, 25, 25.7, 25.7, 5000],
        [26.0, 27, 25.8, 26.5, 26.5, 5200],
    ]
    frame = pd.DataFrame(values, index=dates, columns=columns)
    frame.index.name = "Date"
    return frame


def test_fetch_prices_transforms_multi_index(monkeypatch: pytest.MonkeyPatch) -> None:
    frame = _sample_multi_index_frame()
    downloader = DummyDownloader(frame)
    monkeypatch.setattr(data.yf, "download", downloader)

    result = data.fetch_prices(["CL=F", "BZ=F"], interval="1d", retries=1)

    assert set(result["ticker"]) == {"CL=F", "BZ=F"}
    assert list(result.columns) == [
        "ticker",
        "datetime",
        "open",
        "high",
        "low",
        "close",
        "adj_close",
        "volume",
    ]
    assert downloader.calls[0]["kwargs"]["interval"] == "1d"
    assert len(result) == 4
    assert result["datetime"].dt.tz is not None


def test_fetch_prices_handles_single_ticker(monkeypatch: pytest.MonkeyPatch) -> None:
    frame = _sample_single_ticker_frame()
    downloader = DummyDownloader(frame)
    monkeypatch.setattr(data.yf, "download", downloader)

    result = data.fetch_prices(["NG=F"], interval="1h", retries=1)

    assert (result["ticker"] == "NG=F").all()
    assert result.loc[0, "open"] == pytest.approx(25.5)


def test_fetch_prices_missing_columns(monkeypatch: pytest.MonkeyPatch) -> None:
    frame = _sample_single_ticker_frame().drop(columns=["Adj Close"])
    downloader = DummyDownloader(frame)
    monkeypatch.setattr(data.yf, "download", downloader)

    with pytest.raises(data.DataDownloadError) as excinfo:
        data.fetch_prices(["CL=F"], retries=1)
    assert isinstance(excinfo.value.__cause__, ValueError)
