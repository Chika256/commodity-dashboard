"""Smoke tests to ensure importability and cached loader contracts."""

from __future__ import annotations

import datetime as dt

import pandas as pd
import pytest


def test_import_app() -> None:
    import app

    assert hasattr(app, "main")


def test_cached_loader(monkeypatch: pytest.MonkeyPatch) -> None:
    import app

    sample = pd.DataFrame(
        {
            "ticker": ["CL=F"],
            "datetime": [pd.Timestamp("2024-01-01", tz="UTC")],
            "open": [70.0],
            "high": [71.0],
            "low": [69.5],
            "close": [70.5],
            "adj_close": [70.5],
            "volume": [1000],
        }
    )

    def fake_fetch(*_, **__):
        return sample

    monkeypatch.setattr(app, "fetch_prices", fake_fetch)
    app.load_price_data.clear()

    start = dt.datetime(2024, 1, 1, tzinfo=dt.UTC)
    end = dt.datetime(2024, 1, 2, tzinfo=dt.UTC)
    result = app.load_price_data(("CL=F",), start, end, "1d")

    pd.testing.assert_frame_equal(result, sample)
