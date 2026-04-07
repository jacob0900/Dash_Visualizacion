"""
tabs/contexto.py
Pestaña 2 – Contexto e impacto del sistema financiero colombiano.
"""

from dash import html
import dash_bootstrap_components as dbc


def layout():
    return dbc.Container(
        [
            # ── Título ──────────────────────────────────────────────────────
            dbc.Row(
                dbc.Col(
                    html.H3(
                        "Contexto del Sistema Financiero Colombiano",
                        className="fw-bold mb-1 pt-3",
                        style={"color": "#3a3a5c"},
                    ),
                    width=12,
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.P(
                        "Impacto empresarial, hogares y transmisión de política monetaria",
                        className="text-muted mb-4",
                    ),
                    width=12,
                )
            ),

            # ── Descripción del contexto ─────────────────────────────────────
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("🏦 Sistema Crediticio Colombiano",
                                            className="fw-semibold mb-3", style={"color": "#4a4a6a"}),
                                    html.P(
                                        """
                                        El sistema financiero colombiano es uno de los más desarrollados
                                        de América Latina. El Banco de la República actúa como autoridad
                                        monetaria fijando tasas de referencia que influyen directamente
                                        en las tasas de colocación del sistema bancario, determinando
                                        el costo del crédito para hogares y empresas.
                                        """,
                                        className="text-secondary",
                                    ),
                                    html.P(
                                        """
                                        Las modalidades de crédito analizadas (consumo, tesorería, ordinario
                                        y preferencial) representan distintos segmentos del mercado y
                                        responden de manera diferenciada a los ciclos económicos y
                                        decisiones de política monetaria.
                                        """,
                                        className="text-secondary",
                                    ),
                                ]
                            ),
                            className="shadow-sm border-0 h-100",
                            style={"background": "#f0f4ff", "border-radius": "14px"},
                        ),
                        md=6, className="mb-3",
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("🏢 Impacto Empresarial",
                                            className="fw-semibold mb-3", style={"color": "#4a4a6a"}),
                                    html.P(
                                        """
                                        Las empresas colombianas dependen en gran medida del crédito
                                        de tesorería y ordinario para financiar su capital de trabajo
                                        y proyectos de inversión. Variaciones en las tasas de colocación
                                        afectan directamente:
                                        """,
                                        className="text-secondary",
                                    ),
                                    html.Ul(
                                        [
                                            html.Li("El costo de financiamiento empresarial", className="text-secondary"),
                                            html.Li("La inversión y generación de empleo", className="text-secondary"),
                                            html.Li("La capacidad de expansión de las pymes", className="text-secondary"),
                                            html.Li("La rentabilidad del sector bancario", className="text-secondary"),
                                        ]
                                    ),
                                ]
                            ),
                            className="shadow-sm border-0 h-100",
                            style={"background": "#dcf5e8", "border-radius": "14px"},
                        ),
                        md=6, className="mb-3",
                    ),
                ],
                className="mb-3",
            ),

            # ── Modalidades de crédito ───────────────────────────────────────
            dbc.Row(
                dbc.Col(
                    html.H5("📋 Modalidades de Crédito Analizadas",
                            className="fw-semibold mb-3", style={"color": "#4a4a6a"}),
                    width=12,
                )
            ),
            dbc.Row(
                [
                    _credito_card("💳", "Consumo",
                                  "Financiamiento de bienes y servicios para personas naturales. "
                                  "Refleja el nivel de confianza del consumidor y el acceso al crédito minorista.",
                                  "#dce8ff"),
                    _credito_card("🏛️", "Tesorería",
                                  "Créditos de corto plazo para empresas que requieren liquidez inmediata. "
                                  "Altamente sensibles a las condiciones del mercado monetario.",
                                  "#fff4dc"),
                    _credito_card("📦", "Ordinarios",
                                  "Créditos comerciales estándar para actividades productivas. "
                                  "Principal fuente de financiamiento del sector empresarial.",
                                  "#dcf5e8"),
                    _credito_card("⭐", "Preferenciales",
                                  "Créditos a tasas favorables para grandes empresas con bajo riesgo. "
                                  "Indicador de las condiciones del crédito corporativo.",
                                  "#fde8e8"),
                ],
                className="g-3 mb-4",
            ),

            # ── Transmisión monetaria ────────────────────────────────────────
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("⚙️ Mecanismo de Transmisión Monetaria",
                                        className="fw-semibold mb-3", style={"color": "#4a4a6a"}),
                                dbc.Row(
                                    [
                                        _paso_card("1", "Decisión del Banco de la República",
                                                   "Fija la tasa de intervención (referencia)"),
                                        _paso_card("2", "Ajuste del Sistema Bancario",
                                                   "Los bancos adaptan sus tasas activas y pasivas"),
                                        _paso_card("3", "Impacto en el Crédito",
                                                   "Cambia el costo y volumen del crédito otorgado"),
                                        _paso_card("4", "Efecto en la Economía Real",
                                                   "Inversión, consumo y actividad económica"),
                                    ],
                                    className="g-2",
                                ),
                            ]
                        ),
                        className="shadow-sm border-0",
                        style={"background": "#f5f0ff", "border-radius": "14px"},
                    ),
                    width=12,
                )
            ),
        ],
        fluid=True,
        className="px-3 py-3",
    )


# ── Helpers ──────────────────────────────────────────────────────────────────

def _credito_card(icon, title, desc, bg):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(icon, className="fs-2 mb-2"),
                    html.H6(title, className="fw-bold mb-2", style={"color": "#3a3a5c"}),
                    html.P(desc, className="small text-secondary mb-0"),
                ]
            ),
            className="shadow-sm border-0 h-100 text-center",
            style={"background": bg, "border-radius": "14px"},
        ),
        xs=12, sm=6, md=3,
    )


def _paso_card(num, title, desc):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        num,
                        className="rounded-circle d-flex align-items-center justify-content-center fw-bold text-white mb-2 mx-auto",
                        style={
                            "width": "36px", "height": "36px",
                            "background": "#7b6cf7", "font-size": "1rem",
                        },
                    ),
                    html.P(title, className="fw-semibold small mb-1 text-center", style={"color": "#3a3a5c"}),
                    html.P(desc, className="small text-muted text-center mb-0"),
                ]
            ),
            className="border-0 text-center",
            style={"background": "#f8f6ff", "border-radius": "12px"},
        ),
        xs=12, sm=6, md=3,
    )
