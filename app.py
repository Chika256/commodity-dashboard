"""Streamlit entrypoint for the CCI Commodity Dashboard."""

from __future__ import annotations

import datetime as dt
from typing import Iterable, Sequence

import pandas as pd
import streamlit as st

from src.analytics import add_moving_averages, compute_daily_returns, daily_change
from src.config import get_settings
from src.data import DataDownloadError, fetch_prices
from src.plotting import price_chart, returns_chart

settings = get_settings()


def _load_price_data_uncached(
    tickers: Sequence[str],
    start: dt.datetime,
    end: dt.datetime,
    interval: str,
) -> pd.DataFrame:
    """Standalone loader to simplify unit testing and caching composition."""

    return fetch_prices(tickers, start=start, end=end, interval=interval)


@st.cache_data(ttl=settings.cache_ttl_seconds, show_spinner=False)
def load_price_data(
    tickers: Sequence[str],
    start: dt.datetime,
    end: dt.datetime,
    interval: str,
) -> pd.DataFrame:
    """Shared cache so streamlit does not hammer Yahoo Finance on every rerun."""

    return _load_price_data_uncached(tickers, start, end, interval)


def _infer_date_range(default_days: int) -> tuple[dt.date, dt.date]:
    today = dt.date.today()
    start = today - dt.timedelta(days=default_days)
    return start, today


def _parse_moving_average_input(selection: Iterable[int]) -> tuple[int, ...]:
    windows = sorted({int(window) for window in selection if int(window) > 0})
    if not windows:
        st.warning("Please select at least one moving-average window; defaulting to 20.")
        return (20,)
    return tuple(windows)


def _render_kpis(latest_rows: pd.DataFrame, changes: pd.Series, threshold: float) -> None:
    """Display per-ticker KPIs in responsive columns."""

    columns = st.columns(len(latest_rows))
    alerting = []
    for column, (ticker, row) in zip(columns, latest_rows.iterrows(), strict=False):
        change_pct = changes.get(ticker, 0.0) * 100
        with column:
            st.metric(
                label=f"{ticker} price",
                value=f"${row.close:,.2f}",
                delta=f"{change_pct:+.2f}% vs prev close",
            )
            st.caption(
                "Volume: {}".format(f"{int(row.volume):,}" if row.volume else "n/a"),
                help="Helps gauge how active today's session is versus history.",
            )
        if abs(change_pct) >= threshold:
            alerting.append((ticker, change_pct))

    if alerting:
        formatted = ", ".join(f"{ticker} ({change:+.2f}%)" for ticker, change in alerting)
        st.warning(
            f"Alert threshold breached for: {formatted}.",
            icon="🚨",
        )
    else:
        st.info(
            "All monitored commodities are within the chosen intraday threshold.",
            icon="✅",
        )


def _render_tables(price_frame: pd.DataFrame, returns_frame: pd.DataFrame) -> None:
    """Render recent datapoints to give traders quick tabular context."""

    recent_prices = (
        price_frame.sort_values("datetime", ascending=False)
        .groupby("ticker", group_keys=False)
        .head(5)
        .sort_values(["ticker", "datetime"], ascending=[True, False])
    )
    st.subheader("Recent prints")
    st.caption("Latest ticks help traders double-check the chart narrative.")
    st.dataframe(
        recent_prices,
        hide_index=True,
        use_container_width=True,
    )

    recent_returns = (
        returns_frame.sort_values("datetime", ascending=False)
        .groupby("ticker", group_keys=False)
        .head(10)
        .sort_values(["ticker", "datetime"], ascending=[True, False])
    )
    st.subheader("Return tape")
    st.caption("Quickly compare momentum across commodities.")
    st.dataframe(
        recent_returns,
        hide_index=True,
        use_container_width=True,
    )


def main() -> None:
    """Create the Streamlit layout and orchestrate data, analytics, and visuals."""

    st.set_page_config(
        page_title="CCI Real-Time Commodity Dashboard",
        layout="wide",
        page_icon="📈",
    )
    st.title("CCI Real-Time Commodity Dashboard")
    st.caption(
        "Live commodities view tailored for Castleton Commodities International. "
        "Use the sidebar to compare contracts, study momentum, and trigger alerts."
    )
    st.sidebar.header("Controls")
    st.sidebar.caption(
        "Configure the universe and analytics knobs to mirror your trading run-book."
    )

    default_start, default_end = _infer_date_range(settings.default_lookback_days)
    # Sidebar inputs provide guardrails and educational tooltips for students new to FX/commodities.
    tickers = st.sidebar.multiselect(
        "Commodities",
        options=settings.default_tickers,
        default=list(settings.default_tickers[:3]),
        help="Pick the contracts you want to study side-by-side.",
    )
    if not tickers:
        st.warning("Select at least one commodity to plot.")
        st.stop()

    date_range = st.sidebar.date_input(
        "Date range",
        value=(default_start, default_end),
        help="Use a narrower window when selecting high-frequency intervals like 5 minutes.",
    )
    if isinstance(date_range, tuple):
        start_date, end_date = date_range
    else:  # streamlit returns single date if user picks one
        start_date = date_range
        end_date = default_end
    start_dt = dt.datetime.combine(start_date, dt.time.min)
    end_dt = dt.datetime.combine(end_date, dt.time.max)

    interval = st.sidebar.selectbox(
        "Interval",
        options=("5m", "1h", "1d"),
        index=(0 if settings.default_interval == "5m" else 2),
        help="Higher frequency unlocks intraday monitoring; daily keeps long-term context.",
    )

    ma_choice = st.sidebar.multiselect(
        "Moving-average windows",
        options=[5, 10, 20, 50, 100, 200],
        default=list(settings.moving_average_windows),
        help="Overlay rolling trends to smooth noisy price action.",
    )
    ma_windows = _parse_moving_average_input(ma_choice)

    threshold = st.sidebar.slider(
        "Alert threshold (%)",
        min_value=0.5,
        max_value=10.0,
        value=3.0,
        step=0.5,
        help="Highlight contracts whose day move beats this threshold.",
    )

    with st.spinner("Fetching market data..."):
        try:
            prices = load_price_data(tuple(tickers), start_dt, end_dt, interval)
        except DataDownloadError as error:
            st.error(
                "Unable to download data from Yahoo Finance. "
                "Please try a smaller date window or slower interval.",
            )
            st.code(str(error))
            st.stop()

    if prices.empty:
        st.info("No data returned for the given filters. Adjust the range or interval.")
        st.stop()

    enriched = add_moving_averages(prices, ma_windows)
    returns = compute_daily_returns(prices)
    changes = daily_change(prices)

    latest_rows = (
        enriched.sort_values("datetime")
        .groupby("ticker", group_keys=False)
        .tail(1)
        .set_index("ticker")
    )

    _render_kpis(latest_rows, changes, threshold)

    st.subheader("Price action")
    st.caption("Visualise how each contract trades versus its moving averages.")
    price_fig = price_chart(enriched, ma_windows)
    st.plotly_chart(price_fig, use_container_width=True)

    st.subheader("Momentum snapshot")
    st.caption("Bar chart emphasises cross-commodity swings for the selected window.")
    returns_fig = returns_chart(returns)
    st.plotly_chart(returns_fig, use_container_width=True)

    _render_tables(enriched, returns)

    st.download_button(
        label="Download latest dataset (CSV)",
        data=enriched.to_csv(index=False).encode("utf-8"),
        file_name="cci_commodities.csv",
        mime="text/csv",
    )

    with st.expander("Need a refresher?", expanded=False):
        st.markdown(
            "- **Ticker**: the short code traders use for each contract.\n"
            "- **Moving average**: a smoothed price trend to spot momentum shifts.\n"
            "- **Day % change**: today's move relative to the last close."
        )


if __name__ == "__main__":
    main()
