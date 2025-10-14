"""Configuration models for the commodity dashboard."""

from __future__ import annotations

from functools import lru_cache
from typing import Tuple

from pydantic import BaseSettings, Field, conint, confloat, validator


class DashboardSettings(BaseSettings):
    """Centralised configuration for the dashboard.

    Using :class:`pydantic.BaseSettings` lets us override defaults with environment
    variables (prefixed with ``CCI_``) while keeping sensible local defaults for
    quick student demos. The settings file can grow with production needs without
    scattering magic numbers across the codebase.
    """

    default_tickers: Tuple[str, ...] = Field(
        ("CL=F", "BZ=F", "NG=F", "GC=F", "SI=F"),
        description="Tickers displayed when the app boots.",
    )
    default_interval: str = Field(
        "1d",
        description="Interval used when the user has not selected their own.",
        regex=r"^[0-9]+[mhdw]$|^1d$|^1h$|^5m$",
    )
    default_lookback_days: conint(gt=0) = Field(
        365, description="Number of trading days to look back when no range is chosen."
    )
    moving_average_windows: Tuple[conint(gt=0), ...] = Field(
        (20, 50), description="Rolling windows (in periods) applied to price series."
    )
    cache_ttl_seconds: conint(gt=0) = Field(
        300, description="TTL for Streamlit data cache to balance staleness and speed."
    )
    data_fetch_retries: conint(ge=1) = Field(
        3, description="Retry attempts for transient yfinance failures."
    )
    data_fetch_backoff: confloat(gt=0) = Field(
        1.5, description="Backoff multiplier between retry attempts."
    )
    max_tickers: conint(gt=0) = Field(
        10,
        description=(
            "Hard cap to avoid overwhelming the UI and Yahoo endpoints with "
            "excessive simultaneous downloads."
        ),
    )

    class Config:
        env_prefix = "CCI_"
        case_sensitive = False
        env_file = ".env"

    @validator("moving_average_windows")
    def ensure_sorted(cls, value: Tuple[int, ...]) -> Tuple[int, ...]:
        """Keep moving-average windows sorted for predictable UI ordering."""
        return tuple(sorted(value))


@lru_cache(maxsize=1)
def get_settings() -> DashboardSettings:
    """Return a cached instance of :class:`DashboardSettings`.

    The configuration rarely changes at runtime. Caching avoids repeated disk reads,
    environment parsing, and validation, keeping request handling fast.
    """

    return DashboardSettings()


__all__ = ["DashboardSettings", "get_settings"]
