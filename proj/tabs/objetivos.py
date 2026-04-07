"""
tabs/objetivos.py
Pestaña 4 – Objetivos y justificación del proyecto.
"""

from dash import html
import dash_bootstrap_components as dbc


def layout():
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H3("Objetivos del Proyecto",
                            className="fw-bold pt-3 mb-1", style={"color": "#3a3a5c"}),
                    width=12,
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.P("Metas de análisis, modelado y aporte al conocimiento financiero colombiano",
                           className="text-muted mb-4"),
                    width=12,
                )
            ),

            # ── Objetivo General ─────────────────────────────────────────────
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Div("🎯", className="fs-1 text-center"),
                                            width=2, className="d-flex align-items-center justify-content-center",
                                        ),
                                        dbc.Col(
                                            [
                                                html.H5("Objetivo General",
                                                        className="fw-bold mb-2", style={"color": "#4a4a6a"}),
                                                html.P(
                                                    """
                                                    Predecir la evolución de la Tasa de Colocación Total del sistema
                                                    financiero colombiano mediante técnicas de análisis de series de
                                                    tiempo, utilizando los datos históricos mensuales del Banco de la
                                                    República (1998–2025), con el fin de aportar una herramienta de
                                                    apoyo a la toma de decisiones financieras y de política monetaria.
                                                    """,
                                                    className="text-secondary mb-0",
                                                ),
                                            ],
                                            width=10,
                                        ),
                                    ]
                                )
                            ]
                        ),
                        className="shadow-sm border-0 mb-4",
                        style={"background": "#f0f4ff", "border-radius": "14px"},
                    ),
                    width=12,
                )
            ),

            # ── Objetivos Específicos ────────────────────────────────────────
            dbc.Row(
                dbc.Col(
                    html.H5("📌 Objetivos Específicos",
                            className="fw-semibold mb-3", style={"color": "#4a4a6a"}),
                    width=12,
                )
            ),
            dbc.Row(
                [
                    _obj_card("1", "Exploración de Datos (EDA)",
                              "Realizar un análisis exploratorio completo de las series históricas de "
                              "tasas de colocación, identificando tendencias, ciclos, estacionalidad "
                              "y valores atípicos.", "#dce8ff"),
                    _obj_card("2", "Prueba de Estacionariedad",
                              "Determinar mediante pruebas estadísticas (ADF y KPSS) si las series "
                              "son estacionarias o requieren transformaciones para su modelado "
                              "mediante ARIMA.", "#dcf5e8"),
                    _obj_card("3", "Modelado Econométrico",
                              "Construir y ajustar un modelo ARIMA para capturar los patrones "
                              "lineales y estacionales de la serie, evaluando la bondad de ajuste "
                              "mediante métricas estadísticas.", "#fff4dc"),
                    _obj_card("4", "Comparación de Modelos",
                              "Comparar el desempeño del modelo ARIMA frente a enfoques de redes "
                              "neuronales, seleccionando el modelo con mejor capacidad predictiva "
                              "según métricas de error.", "#fde8e8"),
                ],
                className="g-3 mb-4",
            ),
            dbc.Row(
                [
                    _obj_card("5", "Visualización Interactiva",
                              "Desarrollar un dashboard interactivo en Dash que presente los "
                              "resultados del análisis, las proyecciones y los indicadores clave "
                              "de forma clara y accesible.", "#f5f0ff"),
                    _obj_card("6", "Aporte Empírico",
                              "Contribuir con evidencia empírica sobre el comportamiento del crédito "
                              "en Colombia, documentando hallazgos sobre los mecanismos de "
                              "transmisión de la política monetaria.", "#fef9e7"),
                ],
                className="g-3 mb-4",
            ),

            # ── Justificación ────────────────────────────────────────────────
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("💡 Justificación",
                                        className="fw-semibold mb-3", style={"color": "#4a4a6a"}),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H6("Justificación Teórica",
                                                        className="fw-bold text-primary mb-2"),
                                                html.P(
                                                    """
                                                    Las tasas de interés son una de las variables más relevantes
                                                    en macroeconomía y finanzas. Comprender su comportamiento
                                                    temporal permite validar teorías económicas y contribuir
                                                    al acervo de conocimiento sobre el sistema financiero
                                                    colombiano.
                                                    """,
                                                    className="small text-secondary",
                                                ),
                                            ],
                                            md=4,
                                        ),
                                        dbc.Col(
                                            [
                                                html.H6("Justificación Práctica",
                                                        className="fw-bold text-success mb-2"),
                                                html.P(
                                                    """
                                                    Las instituciones financieras, empresas y formuladores
                                                    de política pueden utilizar proyecciones de tasas para
                                                    optimizar decisiones de crédito, inversión y gestión
                                                    del riesgo financiero.
                                                    """,
                                                    className="small text-secondary",
                                                ),
                                            ],
                                            md=4,
                                        ),
                                        dbc.Col(
                                            [
                                                html.H6("Justificación Metodológica",
                                                        className="fw-bold text-warning mb-2"),
                                                html.P(
                                                    """
                                                    La combinación de modelos estadísticos clásicos (ARIMA)
                                                    con métodos de aprendizaje automático permite explorar
                                                    la complementariedad de enfoques y establecer mejores
                                                    prácticas de modelado para series financieras.
                                                    """,
                                                    className="small text-secondary",
                                                ),
                                            ],
                                            md=4,
                                        ),
                                    ]
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


def _obj_card(num, title, desc, bg):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        f"OE{num}",
                        className="fw-bold mb-2 px-2 py-1 rounded-pill d-inline-block small",
                        style={"background": "#7b6cf7", "color": "white"},
                    ),
                    html.H6(title, className="fw-bold mb-2 mt-1", style={"color": "#3a3a5c"}),
                    html.P(desc, className="small text-secondary mb-0"),
                ]
            ),
            className="shadow-sm border-0 h-100",
            style={"background": bg, "border-radius": "14px"},
        ),
        xs=12, sm=6, md=3,
    )
