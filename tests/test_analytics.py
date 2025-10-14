"""Unit tests for analytics helpers."""

from __future__ import annotations

import pandas as pd
import pytest

from src import analytics


@pytest.fixture()
def sample_prices() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "ticker": ["CL=F", "CL=F", "BZ=F", "BZ=F"],
            "datetime": pd.to_datetime(
                ["2024-01-01", "2024-01-02", "2024-01-01", "2024-01-02"], utc=True
            ),
            "adj_close": [70.0, 71.4, 75.0, 74.25],
            "close": [70.0, 71.4, 75.0, 74.25],
        }
    )


def test_compute_daily_returns(sample_prices: pd.DataFrame) -> None:
    result = analytics.compute_daily_returns(sample_prices)

    cl_returns = result[result["ticker"] == "CL=F"]["daily_return"].tolist()
    bz_returns = result[result["ticker"] == "BZ=F"]["daily_return"].tolist()

    assert cl_returns == [0.0, pytest.approx(0.02)]  # 1.4 increase on 70 is 2%
    assert bz_returns == [0.0, pytest.approx(-0.01)]  # Drop from 75 -> 74.25 ~ -1%


def test_add_moving_averages(sample_prices: pd.DataFrame) -> None:
    enriched = analytics.add_moving_averages(sample_prices, windows=(2, 3))

    assert {"ma_2", "ma_3"}.issubset(enriched.columns)
    cl_slice = enriched[enriched["ticker"] == "CL=F"].sort_values("datetime")
    assert cl_slice.iloc[0]["ma_2"] == pytest.approx(70.0)
    assert cl_slice.iloc[1]["ma_2"] == pytest.approx((70.0 + 71.4) / 2)


def test_daily_change(sample_prices: pd.DataFrame) -> None:
    changes = analytics.daily_change(sample_prices)

    assert changes.loc["CL=F"] == pytest.approx(0.02)
    assert changes.loc["BZ=F"] == pytest.approx(-0.01)


def test_windows_validation(sample_prices: pd.DataFrame) -> None:
    with pytest.raises(ValueError):
        analytics.add_moving_averages(sample_prices, windows=())
