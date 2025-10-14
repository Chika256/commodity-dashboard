"""Tests for the data layer will be added alongside the implementation."""

import pytest


@pytest.mark.xfail(reason="Data layer not yet implemented")
def test_fetch_prices_not_implemented():
    from src import data

    with pytest.raises(NotImplementedError):
        data.fetch_prices(["CL=F"])
