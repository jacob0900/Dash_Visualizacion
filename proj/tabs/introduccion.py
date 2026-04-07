"""
tabs/introduccion.py
Pestaña 1 – Introducción.
Diseño inspirado en la imagen de referencia: título grande a la derecha,
texto en dos columnas, botones de acceso con iconos, citas académicas.
"""

from dash import html
import dash_bootstrap_components as dbc

# ── URLs — editar aquí ────────────────────────────────────────────────────────
GITHUB_URL      = "https://github.com/tu-usuario/tu-repositorio"
LINKEDIN_URL_1  = "https://www.linkedin.com/in/jacobo-londo%C3%B1o-baquero-a2b86733a/"        # Tu LinkedIn
LINKEDIN_URL_2  = "https://www.linkedin.com/in/jesus-david-barrios-97181b337/" # LinkedIn compañero


def layout():
    return dbc.Container([

        # ── Bloque superior: título a la derecha, texto a la izquierda ──────
        dbc.Row([

            # Columna izquierda: descripción del proyecto (estilo imagen ref.)
            dbc.Col([
                html.H4("Descripción del Proyecto",
                        className="fw-bold mb-3",
                        style={"color": "#1a1a2e", "font-size": "1.25rem",
                               "border-bottom": "2px solid #c0392b",
                               "padding-bottom": "8px"}),

                html.P([
                    """El análisis de las tasas de colocación y los créditos en Colombia
                    constituye un insumo fundamental para comprender la dinámica del sistema
                    financiero y la transmisión de la política monetaria. El Banco de la República,
                    como autoridad monetaria, recopila y publica series estadísticas históricas
                    que permiten estudiar la evolución de estas variables desde finales del siglo XX """,
                    html.Span("(Banco de la República, 2024).", className="fst-italic text-muted"),
                ], style={"color": "#2c2c2c", "font-size": "1.05rem", "line-height": "1.9",
                          "text-align": "justify"}),

                html.P([
                    """En el contexto económico colombiano, las tasas de interés de colocación
                    reflejan tanto las decisiones de política monetaria como las condiciones de
                    liquidez y riesgo en el mercado financiero. Diversos estudios han señalado
                    que la variabilidad de estas tasas está asociada con ciclos de expansión y
                    contracción del crédito, afectando directamente la actividad económica y el
                    acceso de los hogares y empresas al financiamiento """,
                    html.Span("(Clavijo, 2019; Villar & Salamanca, 2021).", className="fst-italic text-muted"),
                ], style={"color": "#2c2c2c", "font-size": "1.05rem", "line-height": "1.9",
                          "text-align": "justify"}),

                html.P([
                    """La predicción de series financieras mediante modelos econométricos
                    como ARIMA ha sido ampliamente documentada en la literatura como una
                    herramienta eficaz para capturar patrones temporales en tasas de interés """,
                    html.Span("(Box & Jenkins, 1976; Hamilton, 1994).", className="fst-italic text-muted"),
                    """ El objetivo central de este trabajo es predecir la evolución de la
                    Tasa de Colocación Total mediante técnicas de series de tiempo, aportando
                    evidencia empírica sobre los mecanismos de transmisión de la política monetaria
                    en Colombia.""",
                ], style={"color": "#2c2c2c", "font-size": "1.05rem", "line-height": "1.9",
                          "text-align": "justify"}),

                html.P([
                    """Los datos utilizados en el análisis provienen del sistema estadístico
                    oficial del Banco de la República y comprenden registros mensuales desde
                    marzo de 1998 hasta agosto de 2025, abarcando 330 observaciones de siete
                    series financieras. Este horizonte temporal permite identificar tendencias
                    estructurales, ciclos y cambios de régimen en el comportamiento del crédito
                    colombiano """,
                    html.Span("(Urrutia & Namen, 2012).", className="fst-italic text-muted"),
                ], className="mb-0",
                   style={"color": "#2c2c2c", "font-size": "1.05rem", "line-height": "1.9",
                          "text-align": "justify"}),

            ], md=7, className="pe-4 pt-4 pb-3"),

            # Columna derecha: título grande + botones (estilo imagen ref.)
            dbc.Col([
                html.Div([
                    html.H2("ANÁLISIS DE TASAS DE INTERÉS DE COLOCACIÓN",
                            style={"color": "#1a1a2e", "font-size": "1.6rem",
                                   "font-weight": "800", "line-height": "1.3",
                                   "letter-spacing": "-0.3px", "text-align": "right"}),
                    html.P("EN EL SISTEMA FINANCIERO COLOMBIANO",
                           style={"color": "#c0392b", "font-size": "0.95rem",
                                  "font-weight": "700", "letter-spacing": "1px",
                                  "text-align": "right", "margin-top": "4px"}),
                    html.Hr(style={"border-color": "#c0392b", "border-width": "2px",
                                   "margin": "16px 0"}),
                    html.P("Banco de la República de Colombia",
                           style={"text-align": "right", "color": "#4a4a6a",
                                  "font-size": "0.95rem", "font-weight": "600"}),
                    html.P("Series históricas mensuales · 1998 – 2025",
                           style={"text-align": "right", "color": "#6a6a8a",
                                  "font-size": "0.88rem", "margin-top": "-8px"}),
                ], className="pt-4 pb-2"),

                # Botones de acceso (estilo imagen ref.)
                html.Div([
                    html.P("Acceso y recursos", className="fw-semibold text-end mb-2",
                           style={"color": "#1a1a2e", "font-size": "0.85rem",
                                  "text-transform": "uppercase", "letter-spacing": "0.5px"}),
                    html.Div([
                        _boton_icono("⌥", "Repositorio GitHub", GITHUB_URL),
                        _boton_icono("in", "LinkedIn — Autor 1", LINKEDIN_URL_1),
                        _boton_icono("in", "LinkedIn — Autor 2", LINKEDIN_URL_2),
                    ], className="d-flex flex-column gap-2"),
                ], className="mt-3"),

            ], md=5, className="ps-4 pt-2 pb-3",
               style={"border-left": "1px solid #d4d6e0"}),

        ], className="mb-4 mt-2",
           style={"background": "white", "border-radius": "12px",
                  "border": "1px solid #e4e6ee", "box-shadow": "0 2px 12px rgba(0,0,0,0.06)"}),

        # ── KPIs ─────────────────────────────────────────────────────────────
        dbc.Row([
            _kpi_card("Período de Análisis", "1998 – 2025",         "#e8edf7"),
            _kpi_card("Frecuencia de Datos", "Mensual",              "#e8f4ee"),
            _kpi_card("Observaciones",       "330 registros",        "#fef9e7"),
            _kpi_card("Variables",           "7 series financieras", "#fdf2f2"),
        ], className="g-3 mb-4"),

        # ── Referencias bibliográficas ────────────────────────────────────────
        dbc.Row(dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Referencias Bibliográficas",
                    className="fw-bold mb-3",
                    style={"color": "#1a1a2e", "font-size": "0.95rem",
                           "text-transform": "uppercase", "letter-spacing": "0.5px"}),
            html.Ul([
                html.Li("Banco de la República. (2024). Series estadísticas de tasas de interés de "
                        "colocación. Sistema de información estadística. banrep.gov.co",
                        style={"font-size": "0.92rem", "color": "#3a3a5c", "line-height": "1.7",
                               "margin-bottom": "6px"}),
                html.Li("Box, G. E. P., & Jenkins, G. M. (1976). Time Series Analysis: Forecasting "
                        "and Control. Holden-Day.",
                        style={"font-size": "0.92rem", "color": "#3a3a5c", "line-height": "1.7",
                               "margin-bottom": "6px"}),
                html.Li("Clavijo, S. (2019). Política monetaria y transmisión crediticia en Colombia. "
                        "Debate de Coyuntura Económica, ANIF.",
                        style={"font-size": "0.92rem", "color": "#3a3a5c", "line-height": "1.7",
                               "margin-bottom": "6px"}),
                html.Li("Hamilton, J. D. (1994). Time Series Analysis. Princeton University Press.",
                        style={"font-size": "0.92rem", "color": "#3a3a5c", "line-height": "1.7",
                               "margin-bottom": "6px"}),
                html.Li("Urrutia, M., & Namen, O. M. (2012). Historia del crédito en Colombia en el "
                        "siglo XX. Borradores de Economía, Banco de la República, No. 724.",
                        style={"font-size": "0.92rem", "color": "#3a3a5c", "line-height": "1.7",
                               "margin-bottom": "6px"}),
                html.Li("Villar, L., & Salamanca, D. (2021). Transmisión de la política monetaria "
                        "al crédito bancario en Colombia. Ensayos sobre Política Económica, 39(89), 1–22.",
                        style={"font-size": "0.92rem", "color": "#3a3a5c", "line-height": "1.7"}),
            ], className="ps-3 mb-0"),
        ]), className="shadow-sm border-0",
           style={"background": "#f8f9fc", "border-radius": "12px",
                  "border-left": "4px solid #1a1a2e"}), width=12)),

    ], fluid=True, className="px-3 py-3")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _boton_icono(icono, texto, url):
    return html.A(
        html.Div([
            html.Span(icono, style={"font-size": "1.1rem", "font-weight": "800",
                                    "width": "32px", "display": "inline-block",
                                    "text-align": "center", "color": "#1a1a2e"}),
            html.Span(texto, style={"font-size": "0.9rem", "font-weight": "600",
                                    "color": "#1a1a2e"}),
        ], style={"display": "flex", "align-items": "center", "gap": "10px",
                  "padding": "9px 16px", "background": "#f0f0f8",
                  "border-radius": "8px", "border": "1px solid #d4d6e0",
                  "cursor": "pointer", "transition": "background 0.15s"}),
        href=url, target="_blank", style={"text-decoration": "none"},
    )


def _kpi_card(title, value, bg):
    return dbc.Col(dbc.Card(dbc.CardBody([
        html.P(title, className="text-muted mb-1 fw-semibold",
               style={"font-size": "0.82rem", "text-transform": "uppercase",
                      "letter-spacing": "0.4px"}),
        html.H5(value, className="fw-bold mb-0",
                style={"color": "#1a1a2e", "font-size": "1.05rem"}),
    ]), className="shadow-sm border-0 h-100",
       style={"background": bg, "border-radius": "12px",
              "border-left": "3px solid #1a1a2e"}),
    xs=12, sm=6, md=3)
