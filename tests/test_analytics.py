"""Analytics unit tests will be fleshed out in later commits."""

import pytest


@pytest.mark.xfail(reason="Analytics not yet implemented")
def test_compute_daily_returns_placeholder():
    from src import analytics

    with pytest.raises(NotImplementedError):
        analytics.compute_daily_returns(None)  # type: ignore[arg-type]
