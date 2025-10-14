"""Plotting utilities for the commodity dashboard.

Plot construction is deferred to a later commit to isolate scaffolding changes.
"""

from __future__ import annotations

import pandas as pd


def price_chart(price_frame: pd.DataFrame) -> dict:
    """Return a Plotly figure dictionary once plotting helpers are implemented."""
    raise NotImplementedError("Price chart construction will be added after analytics.")


def returns_chart(returns_frame: pd.DataFrame) -> dict:
    """Return a Plotly figure dictionary once plotting helpers are implemented."""
    raise NotImplementedError("Returns chart construction will be added alongside analytics.")
