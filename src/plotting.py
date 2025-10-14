"""Plotly chart builders for the commodity dashboard."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd
import plotly.graph_objects as go

_COLOR_PALETTE = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
]


def price_chart(price_frame: pd.DataFrame, moving_windows: Iterable[int]) -> go.Figure:
    """Construct an interactive price chart with optional moving averages."""

    fig = go.Figure()
    windows = [int(window) for window in moving_windows]

    for idx, (ticker, group) in enumerate(price_frame.groupby("ticker")):
        color = _COLOR_PALETTE[idx % len(_COLOR_PALETTE)]
        fig.add_trace(
            go.Scatter(
                x=group["datetime"],
                y=group["close"],
                mode="lines",
                name=f"{ticker} close",
                line=dict(color=color, width=2),
                hovertemplate=(
                    "<b>%{text}</b><br>Price: %{y:.2f}<br>"
                    "Time: %{x|%Y-%m-%d %H:%M}<extra></extra>"
                ),
                text=[ticker] * len(group),
            )
        )
        for window in windows:
            column = f"ma_{window}"
            if column not in group:
                continue
            fig.add_trace(
                go.Scatter(
                    x=group["datetime"],
                    y=group[column],
                    mode="lines",
                    name=f"{ticker} MA {window}",
                    line=dict(color=color, dash="dash"),
                    hovertemplate=(
                        f"<b>%{{text}}</b><br>MA {window}: %{{y:.2f}}<br>"
                        "Time: %{x|%Y-%m-%d %H:%M}<extra></extra>"
                    ),
                    text=[ticker] * len(group),
                    legendgroup=f"{ticker}-ma",
                    showlegend=True,
                )
            )

    fig.update_layout(
        title="Price history with moving averages",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
        template="plotly_white",
    )
    return fig


def returns_chart(returns_frame: pd.DataFrame) -> go.Figure:
    """Build a grouped bar chart of recent percentage returns."""

    recent = (
        returns_frame.sort_values("datetime")
        .groupby("ticker", group_keys=False)
        .tail(30)
    )

    fig = go.Figure()
    for idx, (ticker, group) in enumerate(recent.groupby("ticker")):
        color = _COLOR_PALETTE[idx % len(_COLOR_PALETTE)]
        fig.add_trace(
            go.Bar(
                x=group["datetime"],
                y=group["daily_return"],
                name=f"{ticker} daily return",
                marker_color=color,
                hovertemplate=(
                    "<b>%{text}</b><br>Return: %{y:.2%}<br>"
                    "Time: %{x|%Y-%m-%d %H:%M}<extra></extra>"
                ),
                text=[ticker] * len(group),
            )
        )

    fig.update_layout(
        title="Recent percentage returns",
        xaxis_title="Date",
        yaxis_title="Return",
        yaxis_tickformat=".2%",
        barmode="group",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white",
    )
    return fig


__all__ = ["price_chart", "returns_chart"]
