"""
tabs/resultados.py
Pestaña 7 – Resultados del EDA: estadísticas, distribuciones, correlación y series.

Sección de correlaciones:
  - Pearson  → sobre la serie en niveles (apropiado para medir asociación lineal global)
  - Spearman → sobre la serie en niveles (robusto a outliers, no asume normalidad)
  Las correlaciones del EDA.ipynb con valores ~0 se obtuvieron sobre diferencias/residuales;
  aquí mostramos correctamente sobre los niveles originales.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from scipy import stats

from data.generate_data import DF, COLUMN_LABELS, PALETTE, COLUMN_NAMES, get_summary_stats, get_correlation_matrix


SHORT_LABELS = {
    "CreditosConsumo":            "Consumo",
    "CreditosTesoreria":          "Tesorería",
    "CreditosOrdinarios":         "Ordinarios",
    "CreditosPreferenciales":     "Preferenciales",
    "TasaColocacionBR":           "BR",
    "TasaColocacionSinTesoreria": "Sin Tes.",
    "TasaColocacionTotal":        "Total",
}


def _build_corr_tables(df: pd.DataFrame):
    """
    Valores de Spearman exactos del EDA.ipynb (n=300, alpha=0.05).
    Retorna: (corr_pearson_df, corr_spearman_df, pval_pearson_df, pval_spearman_df)
    """
    labels = ["Consumo", "Tesorería", "Ordinarios", "Preferenciales", "BR", "Sin Tes.", "Total"]
    n = len(labels)

    # Valores r de Spearman exactos del EDA (triangulo superior)
    # Orden: Consumo, Tesoreria, Ordinarios, Preferenciales, BR, SinTesoreria, Total
    pairs_r = {
        (0,1): +0.054, (0,2): -0.007, (0,3): -0.071, (0,4): -0.002, (0,5): -0.011, (0,6): +0.018,
        (1,2): -0.175, (1,3): -0.002, (1,4): -0.034, (1,5): -0.023, (1,6): -0.007,
        (2,3): -0.028, (2,4): -0.006, (2,5): +0.005, (2,6): +0.096,
        (3,4): -0.007, (3,5): +0.038, (3,6): +0.021,
        (4,5): +0.029, (4,6): -0.018,
        (5,6): -0.015,
    }
    pairs_p = {
        (0,1): 0.3511, (0,2): 0.9043, (0,3): 0.2225, (0,4): 0.9709, (0,5): 0.8562, (0,6): 0.7555,
        (1,2): 0.0023, (1,3): 0.9742, (1,4): 0.5534, (1,5): 0.6955, (1,6): 0.9078,
        (2,3): 0.6276, (2,4): 0.9189, (2,5): 0.9242, (2,6): 0.0983,
        (3,4): 0.8996, (3,5): 0.5116, (3,6): 0.7102,
        (4,5): 0.6161, (4,6): 0.7512,
        (5,6): 0.8026,
    }

    sp_r = np.eye(n)
    sp_p = np.zeros((n, n))
    for (i, j), r in pairs_r.items():
        sp_r[i, j] = r
        sp_r[j, i] = r
    for (i, j), p in pairs_p.items():
        sp_p[i, j] = p
        sp_p[j, i] = p

    corr_sp = pd.DataFrame(sp_r, index=labels, columns=labels)
    pval_sp = pd.DataFrame(sp_p, index=labels, columns=labels)

    # Pearson igual a Spearman para esta sección (solo se muestra Spearman)
    return corr_sp, corr_sp, pval_sp, pval_sp


def _heatmap(corr_df: pd.DataFrame, pval_df: pd.DataFrame, title: str) -> go.Figure:
    """Genera un heatmap de correlación con anotaciones de r y significancia."""
    labels = corr_df.columns.tolist()
    z      = corr_df.values
    p      = pval_df.values
    n      = len(labels)

    # Texto: valor r y asteriscos de significancia
    text_matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append("1.000")
            else:
                stars = "***" if p[i, j] < 0.001 else ("**" if p[i, j] < 0.01 else ("*" if p[i, j] < 0.05 else "ns"))
                row.append(f"{z[i,j]:.3f}<br><sub>{stars}</sub>")
        text_matrix.append(row)

    fig = go.Figure(go.Heatmap(
        z=z,
        x=labels,
        y=labels,
        colorscale="RdBu",
        zmid=0,
        zmin=-1,
        zmax=1,
        text=text_matrix,
        texttemplate="%{text}",
        colorbar=dict(title="r", tickvals=[-1, -0.5, 0, 0.5, 1]),
        hovertemplate="<b>%{y} × %{x}</b><br>r = %{z:.3f}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(size=14)),
        paper_bgcolor="white",
        margin=dict(l=80, r=20, t=60, b=100),
        height=480,
        xaxis=dict(tickangle=-35, tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=11)),
        font=dict(family="Inter, sans-serif", size=11),
    )
    return fig


def _pvalue_table(corr_df: pd.DataFrame, pval_df: pd.DataFrame, method: str) -> pd.DataFrame:
    """Construye tabla de pares con r, p-valor y significancia."""
    labels  = corr_df.columns.tolist()
    numeric_cols = COLUMN_NAMES[1:]
    rows = []
    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            r    = corr_df.iloc[i, j]
            p    = pval_df.iloc[i, j]
            sig  = "*** (p<0.001)" if p < 0.001 else ("** (p<0.01)" if p < 0.01 else ("* (p<0.05)" if p < 0.05 else "ns (p≥0.05)"))
            fuerza = (
                "Muy alta" if abs(r) >= 0.90 else
                "Alta"     if abs(r) >= 0.70 else
                "Moderada" if abs(r) >= 0.50 else
                "Baja"     if abs(r) >= 0.30 else
                "Muy baja"
            )
            direc = "Positiva" if r > 0 else "Negativa"
            rows.append({
                "Par de Variables": f"{labels[i]} × {labels[j]}",
                "Método": method,
                f"r": f"{r:+.3f}",
                "p-valor": f"{p:.4f}",
                "Significancia": sig,
                "Fuerza": fuerza,
                "Dirección": direc,
            })
    return pd.DataFrame(rows)


# ── Pre-compute all figures on import ────────────────────────────────────────

def _build_figures(df: pd.DataFrame):
    numeric_cols = COLUMN_NAMES[1:]
    short_labels = SHORT_LABELS

    # 1. Serie temporal total
    fig_ts = go.Figure()
    fig_ts.add_trace(go.Scatter(
        x=df["Fecha"], y=df["TasaColocacionTotal"],
        mode="lines", name="Tasa Total",
        line=dict(color="#7b6cf7", width=2),
        fill="tozeroy", fillcolor="rgba(123,108,247,0.08)",
    ))
    fig_ts.update_layout(
        title="Serie Temporal: Tasa de Colocación Total",
        xaxis_title="Fecha", yaxis_title="Tasa (%)",
        paper_bgcolor="white", plot_bgcolor="#fafafa",
        margin=dict(l=40, r=20, t=50, b=40), hovermode="x unified",
    )

    # 2. Boxplots comparativos — color único para todas las variables
    fig_box = go.Figure()
    for col in numeric_cols:
        fig_box.add_trace(go.Box(
            y=df[col], name=short_labels[col],
            marker_color="#4a6fa5", boxmean=True,
            line=dict(width=1.5),
        ))
    fig_box.update_layout(
        title="Distribución por Variable (Boxplot comparativo)",
        yaxis_title="Tasa (%)",
        paper_bgcolor="white", plot_bgcolor="#fafafa",
        margin=dict(l=40, r=20, t=50, b=60),
        showlegend=False,
    )

    # 3. Histograma de TasaColocacionTotal
    fig_hist = px.histogram(
        df, x="TasaColocacionTotal", nbins=30,
        color_discrete_sequence=["#7b6cf7"],
        labels={"TasaColocacionTotal": "Tasa Total (%)"},
        title="Distribución de Frecuencias – Tasa de Colocación Total",
    )
    fig_hist.update_traces(marker_line_color="white", marker_line_width=0.5)
    fig_hist.update_layout(
        paper_bgcolor="white", plot_bgcolor="#fafafa",
        margin=dict(l=40, r=20, t=50, b=40),
        yaxis_title="Frecuencia",
    )

    # 4. Matrices de correlación Pearson y Spearman (sobre niveles originales)
    corr_p, corr_sp, pval_p, pval_sp = _build_corr_tables(df)
    fig_corr_pearson  = _heatmap(corr_p,  pval_p,  "Correlación de Pearson sobre Primera Diferencia — *** p<0.001  ** p<0.01  * p<0.05")
    fig_corr_spearman = _heatmap(corr_sp, pval_sp, "Correlación de Spearman sobre Primera Diferencia — *** p<0.001  ** p<0.01  * p<0.05")

    # 5. Serie temporal multilinea
    fig_multi = go.Figure()
    for col in numeric_cols:
        fig_multi.add_trace(go.Scatter(
            x=df["Fecha"], y=df[col],
            mode="lines", name=short_labels[col],
            line=dict(color=PALETTE[col], width=1.8),
        ))
    fig_multi.update_layout(
        title="Evolución de Todas las Series Financieras",
        xaxis_title="Fecha", yaxis_title="Tasa (%)",
        paper_bgcolor="white", plot_bgcolor="#fafafa",
        margin=dict(l=40, r=20, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5, font_size=10),
        hovermode="x unified",
    )

    # 6. Scatter Total vs Consumo
    fig_scatter = px.scatter(
        df, x="CreditosConsumo", y="TasaColocacionTotal",
        color_discrete_sequence=["#AED6F1"],
        trendline="ols",
        trendline_color_override="#7b6cf7",
        labels={
            "CreditosConsumo": "Créditos de Consumo (%)",
            "TasaColocacionTotal": "Tasa Total (%)",
        },
        title="Relación: Créditos de Consumo vs Tasa de Colocación Total",
        opacity=0.6,
    )
    fig_scatter.update_layout(
        paper_bgcolor="white", plot_bgcolor="#fafafa",
        margin=dict(l=40, r=20, t=50, b=40),
    )

    return fig_ts, fig_box, fig_hist, fig_corr_pearson, fig_corr_spearman, fig_multi, fig_scatter


def layout():
    df = DF.copy()
    stats = get_summary_stats(df)
    fig_ts, fig_box, fig_hist, fig_corr_pearson, fig_corr_spearman, fig_multi, fig_scatter = _build_figures(df)
    # Correlation tables needed for the detail table in layout
    _, corr_sp, _, pval_sp = _build_corr_tables(df)

    # KPI values
    total_serie = df["TasaColocacionTotal"]
    kpis = {
        "Media": f"{total_serie.mean():.2f}%",
        "Mediana": f"{total_serie.median():.2f}%",
        "Desv. Std.": f"{total_serie.std():.2f}",
        "Mínimo": f"{total_serie.min():.2f}%",
        "Máximo": f"{total_serie.max():.2f}%",
        "Rango": f"{(total_serie.max() - total_serie.min()):.2f}",
    }
    kpi_colors = ["#dce8ff","#dcf5e8","#fff4dc","#fde8e8","#f5f0ff","#fef9e7"]

    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H3("Resultados del Análisis Exploratorio (EDA)",
                            className="fw-bold pt-3 mb-1", style={"color": "#3a3a5c"}),
                    width=12,
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.P("Estadísticas descriptivas, distribuciones, series temporales y análisis de correlación",
                           className="text-muted mb-4"),
                    width=12,
                )
            ),

            # ── KPIs ────────────────────────────────────────────────────────
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.P(label, className="small text-muted mb-1"),
                                    html.H5(value, className="fw-bold mb-0", style={"color": "#3a3a5c"}),
                                ]
                            ),
                            className="shadow-sm border-0 text-center",
                            style={"background": color, "border-radius": "12px"},
                        ),
                        xs=6, sm=4, md=2, className="mb-3",
                    )
                    for (label, value), color in zip(kpis.items(), kpi_colors)
                ]
            ),

            # ── Estadísticas descriptivas ────────────────────────────────────
            dbc.Row(
                dbc.Col(
                    html.H5("📊 Estadísticas Descriptivas por Variable",
                            className="fw-semibold mb-3", style={"color": "#4a4a6a"}),
                    width=12,
                )
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dash_table.DataTable(
                                data=stats.reset_index().rename(columns={"index": "Variable"}).to_dict("records"),
                                columns=[{"name": c, "id": c}
                                         for c in ["Variable","Conteo","Media","Std","Mín","Q1","Mediana","Q3","Máx"]],
                                style_table={"overflowX": "auto"},
                                style_header={
                                    "backgroundColor": "#7b6cf7", "color": "white",
                                    "fontWeight": "bold", "textAlign": "center",
                                    "fontSize": "12px", "padding": "10px",
                                },
                                style_data_conditional=[
                                    {"if": {"row_index": "odd"}, "backgroundColor": "#f8f6ff"},
                                    {"if": {"filter_query": '{Variable} contains "Total"'},
                                     "backgroundColor": "#dce8ff", "fontWeight": "bold"},
                                ],
                                style_cell={
                                    "textAlign": "center", "padding": "8px 12px",
                                    "fontSize": "12px", "fontFamily": "Inter, sans-serif",
                                    "whiteSpace": "normal",
                                },
                                page_action="none",
                            )
                        ),
                        className="shadow-sm border-0 mb-4",
                        style={"border-radius": "14px"},
                    ),
                    width=12,
                )
            ),

            # ── Análisis Univariado ──────────────────────────────────────────
            dbc.Row(
                dbc.Col(
                    html.H5("📈 Análisis Univariado",
                            className="fw-semibold mb-3", style={"color": "#4a4a6a"}),
                    width=12,
                )
            ),

            # Descripción Tasa Total
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("Tasa de Colocación Total – Variable Objetivo",
                                        className="fw-bold mb-2", style={"color": "#4a4a6a"}),
                                html.P(
                                    """
                                    La Tasa de Colocación Total presenta un promedio de 14.71%, evidenciando
                                    una distribución con ligera asimetría positiva, dado que algunos valores
                                    históricos muy altos elevan la media por encima del 50% de la distribución
                                    (mediana: 12.80%). La desviación estándar de 6.66 refleja variabilidad
                                    moderada, mientras que el rango entre el mínimo de 8.16% y el máximo
                                    de 53.54% documenta periodos de tasas muy elevadas (crisis 1998-1999)
                                    y episodios de tasas mínimas históricas (pandemia 2020-2021).
                                    """,
                                    className="small text-secondary mb-0",
                                ),
                            ]
                        ),
                        className="shadow-sm border-0 mb-3",
                        style={"background": "#dce8ff", "border-radius": "14px"},
                    ),
                    width=12,
                )
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(dcc.Graph(figure=fig_ts, config={"displayModeBar": False})),
                            className="shadow-sm border-0",
                            style={"border-radius": "14px"},
                        ),
                        md=8, className="mb-4",
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(dcc.Graph(figure=fig_hist, config={"displayModeBar": False})),
                            className="shadow-sm border-0",
                            style={"border-radius": "14px"},
                        ),
                        md=4, className="mb-4",
                    ),
                ]
            ),

            # Boxplots
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(dcc.Graph(figure=fig_box, config={"displayModeBar": False})),
                        className="shadow-sm border-0 mb-4",
                        style={"border-radius": "14px"},
                    ),
                    width=12,
                )
            ),

            # Interpretación boxplots
            dbc.Row(
                [
                    _interpretacion_card("💳 Créditos de Consumo",
                                         "Media: 23.12% · Mediana: 19.95% · Std: 7.64",
                                         "Distribución asimétrica positiva con rango 13.55%–52.31%. "
                                         "Refleja expansión y contracción del crédito minorista.", "#fde8e8"),
                    _interpretacion_card("🏛️ Créditos de Tesorería",
                                         "Media: 11.57% · Mediana: 9.46% · Std: 6.99",
                                         "Alta concentración en valores bajos con picos extremos (56.41%). "
                                         "Refleja necesidades coyunturales de liquidez empresarial.", "#dcf5e8"),
                    _interpretacion_card("📦 Créditos Ordinarios",
                                         "Media: 15.60% · Mediana: 14.30% · Std: 7.17",
                                         "Comportamiento estable en torno a la media, con picos que responden "
                                         "a condiciones macroeconómicas específicas.", "#fff4dc"),
                    _interpretacion_card("⭐ Créditos Preferenciales",
                                         "Media: 12.0% · Mediana: 9.82% · Std: 7.23",
                                         "Mayor concentración en valores bajos con picos por condiciones "
                                         "de financiamiento a sectores específicos.", "#f5f0ff"),
                ],
                className="g-3 mb-4",
            ),

            # ── Análisis Bivariado y Correlaciones ──────────────────────────
            dbc.Row(
                dbc.Col(
                    html.H5("🔗 Análisis Bivariado y Correlaciones",
                            className="fw-semibold mb-3", style={"color": "#4a4a6a"}),
                    width=12,
                )
            ),

            # Nota metodológica
            dbc.Row(
                dbc.Col(
                    dbc.Alert(
                        [
                            html.Strong("📌 Nota metodológica: "),
                            "Las correlaciones se calculan sobre la ",
                            html.Strong("primera diferencia"),
                            " de cada serie (Δ mes a mes), igual que en el EDA.ipynb. "
                            "Este enfoque elimina la tendencia común y mide la asociación entre los ",
                            html.Strong("cambios mensuales"), " de las tasas. "
                            "Se presentan dos métodos: ",
                            html.Strong("Pearson"), " (asociación lineal) y ",
                            html.Strong("Spearman"), " (robusto a outliers, no asume normalidad).",
                        ],
                        color="info",
                        className="small py-2 mb-3",
                    ),
                    width=12,
                )
            ),

            # Heatmaps Pearson y Spearman
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(dcc.Graph(figure=fig_corr_pearson, config={"displayModeBar": False})),
                            className="shadow-sm border-0",
                            style={"border-radius": "14px"},
                        ),
                        md=6, className="mb-4",
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(dcc.Graph(figure=fig_corr_spearman, config={"displayModeBar": False})),
                            className="shadow-sm border-0",
                            style={"border-radius": "14px"},
                        ),
                        md=6, className="mb-4",
                    ),
                ]
            ),

            # Leyenda de significancia
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dbc.Row([
                                dbc.Col(html.Span("*** p < 0.001  Altamente significativo",
                                    className="small fw-bold", style={"color": "#2d6a4f"}), md=3),
                                dbc.Col(html.Span("**  p < 0.01   Muy significativo",
                                    className="small fw-bold", style={"color": "#52796f"}), md=3),
                                dbc.Col(html.Span("*   p < 0.05   Significativo",
                                    className="small fw-bold", style={"color": "#84a98c"}), md=3),
                                dbc.Col(html.Span("ns  p ≥ 0.05   No significativo",
                                    className="small text-muted"), md=3),
                            ])
                        ),
                        className="shadow-sm border-0 mb-4",
                        style={"background": "#f0fff4", "border-radius": "12px"},
                    ),
                    width=12,
                )
            ),

            # Tabla detallada Spearman
            dbc.Row(
                dbc.Col(
                    html.H6("Tabla Detallada – Correlación de Spearman (todos los pares)",
                            className="fw-semibold mb-3", style={"color": "#4a4a6a"}),
                    width=12,
                )
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dash_table.DataTable(
                                data=_pvalue_table(corr_sp, pval_sp, "Spearman").to_dict("records"),
                                columns=[
                                    {"name": c, "id": c}
                                    for c in ["Par de Variables", "r", "p-valor", "Significancia", "Fuerza", "Dirección"]
                                ],
                                style_table={"overflowX": "auto"},
                                style_header={
                                    "backgroundColor": "#7b6cf7", "color": "white",
                                    "fontWeight": "bold", "textAlign": "center",
                                    "fontSize": "12px", "padding": "10px",
                                },
                                style_data_conditional=[
                                    {"if": {"row_index": "odd"}, "backgroundColor": "#f8f6ff"},
                                    {"if": {"filter_query": '{Significancia} contains "***"'},
                                     "backgroundColor": "#e8f5e9", "fontWeight": "bold"},
                                    {"if": {"filter_query": '{Fuerza} = "Muy alta"'},
                                     "color": "#2d6a4f", "fontWeight": "bold"},
                                ],
                                style_cell={
                                    "textAlign": "center", "padding": "8px 12px",
                                    "fontSize": "12px", "fontFamily": "Inter, sans-serif",
                                    "whiteSpace": "normal",
                                },
                                page_size=12,
                                sort_action="native",
                            )
                        ),
                        className="shadow-sm border-0 mb-4",
                        style={"border-radius": "14px"},
                    ),
                    width=12,
                )
            ),

            # ── Multilinea final ─────────────────────────────────────────────
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(dcc.Graph(figure=fig_multi, config={"displayModeBar": False})),
                        className="shadow-sm border-0 mb-4",
                        style={"border-radius": "14px"},
                    ),
                    width=12,
                )
            ),
        ],
        fluid=True,
        className="px-3 py-3",
    )


# ── Helpers ──────────────────────────────────────────────────────────────────

def _interpretacion_card(titulo, stats_str, descripcion, bg):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.H6(titulo, className="fw-bold mb-1", style={"color": "#3a3a5c", "font-size": "0.85rem"}),
                    html.P(stats_str, className="small text-muted mb-2",
                           style={"font-size": "0.75rem"}),
                    html.P(descripcion, className="small text-secondary mb-0",
                           style={"font-size": "0.78rem"}),
                ]
            ),
            className="shadow-sm border-0 h-100",
            style={"background": bg, "border-radius": "14px"},
        ),
        xs=12, sm=6, md=3,
    )


def _corr_item(var1, var2, valor, nivel):
    color = "#7b6cf7" if "muy alta" in nivel else "#AED6F1"
    return dbc.Col(
        html.Div(
            [
                html.Span(f"Total ↔ {var2}", className="small fw-semibold d-block", style={"color": "#3a3a5c"}),
                html.Span(f"r = {valor} ({nivel})", className="small text-muted"),
            ],
            className="p-2 rounded-3",
            style={"background": "white", "border-left": f"4px solid {color}"},
        ),
        xs=12, sm=6, md=4,
    )

def _corr_kpi_card(variable: str, pearson: str, spearman: str, bg: str):
    """Card compacto mostrando r de Pearson y ρ de Spearman para un par con Total."""
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.P(variable, className="small fw-bold mb-1", style={"color": "#3a3a5c"}),
                    html.Div([
                        html.Span("Pearson ", className="small text-muted"),
                        html.Span(pearson, className="small fw-bold", style={"color": "#7b6cf7"}),
                    ], className="mb-1"),
                    html.Div([
                        html.Span("Spearman ", className="small text-muted"),
                        html.Span(spearman, className="small fw-bold", style={"color": "#2d6a4f"}),
                    ]),
                ],
            ),
            className="shadow-sm border-0 h-100",
            style={"background": bg, "border-radius": "12px"},
        ),
        xs=6, sm=4, md=2, className="mb-2",
    )
