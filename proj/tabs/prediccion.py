"""
tabs/prediccion.py
Pestaña 8 – Prueba de estacionariedad (ADF y KPSS).
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from data.generate_data import DF
from model.train_model import load_model_results


def _acf_plot(series: pd.Series, nlags: int = 40, title: str = "ACF"):
    """Calcula y grafica la función de autocorrelación."""
    from statsmodels.tsa.stattools import acf
    acf_vals, confint = acf(series.dropna(), nlags=nlags, alpha=0.05)
    lags = list(range(len(acf_vals)))
    conf = 1.96 / np.sqrt(len(series))

    fig = go.Figure()
    fig.add_hline(y=0, line_color="gray", line_width=1)
    fig.add_hrect(y0=-conf, y1=conf, fillcolor="rgba(123,108,247,0.1)", line_width=0)
    for lag, val in zip(lags, acf_vals):
        color = "#7b6cf7" if abs(val) > conf else "#AED6F1"
        fig.add_trace(go.Bar(x=[lag], y=[val], marker_color=color, showlegend=False, width=0.6))
    fig.update_layout(
        title=title, xaxis_title="Lag", yaxis_title="Autocorrelación",
        paper_bgcolor="white", plot_bgcolor="#fafafa",
        margin=dict(l=40, r=20, t=50, b=40), height=280,
    )
    return fig


def _pacf_plot(series: pd.Series, nlags: int = 40, title: str = "PACF"):
    """Calcula y grafica la función de autocorrelación parcial."""
    from statsmodels.tsa.stattools import pacf
    pacf_vals = pacf(series.dropna(), nlags=nlags)
    lags = list(range(len(pacf_vals)))
    conf = 1.96 / np.sqrt(len(series))

    fig = go.Figure()
    fig.add_hline(y=0, line_color="gray", line_width=1)
    fig.add_hrect(y0=-conf, y1=conf, fillcolor="rgba(163,216,234,0.2)", line_width=0)
    for lag, val in zip(lags, pacf_vals):
        color = "#A8D8EA" if abs(val) > conf else "#dcf5e8"
        fig.add_trace(go.Bar(x=[lag], y=[val], marker_color=color, showlegend=False, width=0.6))
    fig.update_layout(
        title=title, xaxis_title="Lag", yaxis_title="Autocorrelación Parcial",
        paper_bgcolor="white", plot_bgcolor="#fafafa",
        margin=dict(l=40, r=20, t=50, b=40), height=280,
    )
    return fig


def layout():
    df   = DF.copy()
    res  = load_model_results()
    serie = df.set_index("Fecha")["TasaColocacionTotal"]
    serie_diff = serie.diff().dropna()

    # ── ACF / PACF serie original y diferenciada
    fig_acf_orig   = _acf_plot(serie,      title="ACF – Serie Original")
    fig_pacf_orig  = _pacf_plot(serie,     title="PACF – Serie Original")
    fig_acf_diff   = _acf_plot(serie_diff, title="ACF – Primera Diferencia")
    fig_pacf_diff  = _pacf_plot(serie_diff,title="PACF – Primera Diferencia")

    # ── Serie temporal + primera diferencia
    fig_ts = go.Figure()
    fig_ts.add_trace(go.Scatter(x=serie.index, y=serie.values, mode="lines",
                                name="Serie Original", line=dict(color="#7b6cf7", width=1.8)))
    fig_ts.update_layout(title="Serie Original: Tasa de Colocación Total",
                         xaxis_title="Fecha", yaxis_title="Tasa (%)",
                         paper_bgcolor="white", plot_bgcolor="#fafafa",
                         margin=dict(l=40, r=20, t=50, b=40), height=260)

    fig_diff = go.Figure()
    fig_diff.add_trace(go.Scatter(x=serie_diff.index, y=serie_diff.values, mode="lines",
                                  name="Primera Diferencia", line=dict(color="#A9DFBF", width=1.8)))
    fig_diff.add_hline(y=0, line_dash="dash", line_color="gray")
    fig_diff.update_layout(title="Primera Diferencia (d=1)",
                           xaxis_title="Fecha", yaxis_title="Δ Tasa (%)",
                           paper_bgcolor="white", plot_bgcolor="#fafafa",
                           margin=dict(l=40, r=20, t=50, b=40), height=260)

    adf_orig  = res["serie_original"]["adf"]
    kpss_orig = res["serie_original"]["kpss"]
    adf_diff  = res["primera_diferencia"]["adf"]
    kpss_diff = res["primera_diferencia"]["kpss"]

    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H3("Prueba de Estacionariedad",
                            className="fw-bold pt-3 mb-1", style={"color": "#3a3a5c"}),
                    width=12,
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.P("Tests ADF y KPSS aplicados a la Tasa de Colocación Total y su primera diferencia",
                           className="text-muted mb-4"),
                    width=12,
                )
            ),

            # ── ¿Qué es estacionariedad? ─────────────────────────────────────
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("ℹ️ ¿Por qué importa la estacionariedad?",
                                        className="fw-semibold mb-3", style={"color": "#4a4a6a"}),
                                html.P(
                                    """
                                    Un proceso estacionario tiene media, varianza y autocovarianza
                                    constantes en el tiempo. Esta propiedad es esencial para que los
                                    modelos ARIMA sean válidos: si la serie no es estacionaria, los
                                    parámetros estimados son inconsistentes y las predicciones no son
                                    confiables. La estacionariedad se verifica con pruebas estadísticas
                                    formales antes de cualquier modelado.
                                    """,
                                    className="text-secondary mb-0",
                                ),
                            ]
                        ),
                        className="shadow-sm border-0 mb-4",
                        style={"background": "#f0f4ff", "border-radius": "14px"},
                    ),
                    width=12,
                )
            ),

            # ── Series temporales ────────────────────────────────────────────
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(dcc.Graph(figure=fig_ts, config={"displayModeBar": False})),
                            className="shadow-sm border-0",
                            style={"border-radius": "14px"},
                        ),
                        md=6, className="mb-4",
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(dcc.Graph(figure=fig_diff, config={"displayModeBar": False})),
                            className="shadow-sm border-0",
                            style={"border-radius": "14px"},
                        ),
                        md=6, className="mb-4",
                    ),
                ]
            ),

            # ── Resultados ADF ───────────────────────────────────────────────
            dbc.Row(
                dbc.Col(
                    html.H5("🔬 Test ADF (Augmented Dickey-Fuller)",
                            className="fw-semibold mb-3", style={"color": "#4a4a6a"}),
                    width=12,
                )
            ),
            dbc.Row(
                [
                    _test_card("Serie Original", adf_orig, "#dce8ff"),
                    _test_card("Primera Diferencia (d=1)", adf_diff, "#dcf5e8"),
                ],
                className="g-3 mb-4",
            ),

            # ── Resultados KPSS ──────────────────────────────────────────────
            dbc.Row(
                dbc.Col(
                    html.H5("🔬 Test KPSS (Kwiatkowski-Phillips-Schmidt-Shin)",
                            className="fw-semibold mb-3", style={"color": "#4a4a6a"}),
                    width=12,
                )
            ),
            dbc.Row(
                [
                    _test_card("Serie Original", kpss_orig, "#fff4dc"),
                    _test_card("Primera Diferencia (d=1)", kpss_diff, "#fde8e8"),
                ],
                className="g-3 mb-4",
            ),

            # ── Interpretación conjunta ──────────────────────────────────────
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("📌 Interpretación Conjunta ADF + KPSS",
                                        className="fw-semibold mb-2", style={"color": "#4a4a6a"}),
                                html.P(res["interpretacion_conjunta"],
                                       className="text-secondary mb-0 fw-semibold"),
                            ]
                        ),
                        className="shadow-sm border-0 mb-4",
                        style={"background": "#f5f0ff", "border-radius": "14px",
                               "border-left": "5px solid #7b6cf7"},
                    ),
                    width=12,
                )
            ),

            # ── ACF / PACF ───────────────────────────────────────────────────
            dbc.Row(
                dbc.Col(
                    html.H5("📊 Función de Autocorrelación (ACF) y Autocorrelación Parcial (PACF)",
                            className="fw-semibold mb-3", style={"color": "#4a4a6a"}),
                    width=12,
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(dcc.Graph(figure=fig_acf_orig, config={"displayModeBar": False})),
                            className="shadow-sm border-0",
                            style={"border-radius": "14px"},
                        ),
                        md=6, className="mb-3",
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(dcc.Graph(figure=fig_pacf_orig, config={"displayModeBar": False})),
                            className="shadow-sm border-0",
                            style={"border-radius": "14px"},
                        ),
                        md=6, className="mb-3",
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(dcc.Graph(figure=fig_acf_diff, config={"displayModeBar": False})),
                            className="shadow-sm border-0",
                            style={"border-radius": "14px"},
                        ),
                        md=6, className="mb-3",
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(dcc.Graph(figure=fig_pacf_diff, config={"displayModeBar": False})),
                            className="shadow-sm border-0",
                            style={"border-radius": "14px"},
                        ),
                        md=6, className="mb-3",
                    ),
                ]
            ),

            # ── Próximos pasos ───────────────────────────────────────────────
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("🚀 Próximos Pasos",
                                        className="fw-semibold mb-3", style={"color": "#4a4a6a"}),
                                dbc.Row(
                                    [
                                        _paso_item("1", "Identificación ARIMA",
                                                   "Con base en los resultados de ACF y PACF, "
                                                   "determinar los parámetros óptimos (p, d, q)."),
                                        _paso_item("2", "Estimación del Modelo",
                                                   "Ajustar el modelo ARIMA y evaluar la bondad "
                                                   "de ajuste con AIC y BIC."),
                                        _paso_item("3", "Validación de Residuales",
                                                   "Verificar que los residuales sean ruido blanco "
                                                   "(normalidad e independencia)."),
                                        _paso_item("4", "Pronóstico",
                                                   "Generar proyecciones con intervalos de confianza "
                                                   "para los próximos períodos."),
                                    ],
                                    className="g-3",
                                ),
                            ]
                        ),
                        className="shadow-sm border-0",
                        style={"background": "#f8f9ff", "border-radius": "14px"},
                    ),
                    width=12,
                )
            ),
        ],
        fluid=True,
        className="px-3 py-3",
    )


# ── Helpers ──────────────────────────────────────────────────────────────────

def _test_card(titulo: str, result: dict, bg: str):
    icono = "✅" if result["es_estacionaria"] else "⚠️"
    pval_color = "#28a745" if result["es_estacionaria"] else "#dc3545"
    crit_vals = result.get("valores_criticos", {})

    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.H6(f"{icono} {titulo}", className="fw-bold mb-3", style={"color": "#3a3a5c"}),
                    dbc.Row(
                        [
                            dbc.Col([
                                html.P("Estadístico", className="small text-muted mb-0"),
                                html.H5(f"{result['estadistico']:.4f}", className="fw-bold mb-0",
                                        style={"color": "#3a3a5c"}),
                            ], width=6),
                            dbc.Col([
                                html.P("p-valor", className="small text-muted mb-0"),
                                html.H5(f"{result['p_value']:.4f}", className="fw-bold mb-0",
                                        style={"color": pval_color}),
                            ], width=6),
                        ],
                        className="mb-3",
                    ),
                    html.P("Valores Críticos:", className="small text-muted mb-1"),
                    html.Div(
                        [
                            html.Span(
                                f"{k}: {v}  ",
                                className="small me-2 px-2 py-1 rounded",
                                style={"background": "white", "font-size": "0.75rem"},
                            )
                            for k, v in crit_vals.items()
                        ],
                        className="mb-3",
                    ),
                    html.Hr(className="my-2"),
                    html.P(result["hipotesis_nula"],
                           className="small text-muted fst-italic mb-2"),
                    html.P(result["conclusion"],
                           className="small fw-semibold mb-0",
                           style={"color": pval_color}),
                ]
            ),
            className="shadow-sm border-0 h-100",
            style={"background": bg, "border-radius": "14px"},
        ),
        md=6,
    )


def _paso_item(num, titulo, desc):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        num,
                        className="rounded-circle fw-bold text-white d-flex align-items-center "
                                  "justify-content-center mb-2 mx-auto",
                        style={"width": "32px", "height": "32px",
                               "background": "#7b6cf7", "font-size": "0.9rem"},
                    ),
                    html.H6(titulo, className="fw-bold text-center mb-2", style={"color": "#3a3a5c"}),
                    html.P(desc, className="small text-secondary text-center mb-0"),
                ]
            ),
            className="border-0 text-center",
            style={"background": "#f8f6ff", "border-radius": "12px"},
        ),
        xs=12, sm=6, md=3,
    )
