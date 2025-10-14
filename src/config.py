"""Configuration models for the commodity dashboard.

Detailed settings will be implemented in a dedicated commit.
"""

from __future__ import annotations

from pydantic import BaseModel


class DashboardSettings(BaseModel):
    """Placeholder settings to be expanded with defaults and validation."""

    tickers: tuple[str, ...] = ("CL=F", "BZ=F", "NG=F", "GC=F", "SI=F")
