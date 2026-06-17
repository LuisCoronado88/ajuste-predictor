import dash_bootstrap_components as dbc
from dash import html


def create_methodology_tab():

    return dbc.Container(

        [

            html.H2(
                "Metodología Analítica"
            ),

            dbc.Alert(

                """
                Datos Crudos
                → Limpieza
                → Feature Engineering
                → EDA
                → Machine Learning
                → Scoring
                → Monitoreo
                """,

                color="info"

            ),

            html.Hr(),

            html.H4(
                "Variable Objetivo"
            ),

            dbc.Card(
                dbc.CardBody(
                    """
                    TARGET_AJUSTE

                    0 = Sin ajuste

                    1 = Con ajuste
                    """
                )
            ),

            html.Br(),

            html.H4(
                "Variables Candidatas"
            ),

            html.Ul(

                [

                    html.Li("M3_PROMEDIO"),
                    html.Li("M3_PERIODO"),
                    html.Li("DELTA_M3"),
                    html.Li("FACTURACION_PROMEDIO"),
                    html.Li("FACTURACION_PERIODO"),
                    html.Li("DELTA_FACTURACION"),
                    html.Li("CANTIDAD_AJUSTES_ULT_6_MESES"),
                    html.Li("VALOR_AJUSTE_PROMEDIO"),
                    html.Li("CATEGORIA"),
                    html.Li("PLAN_FACTURACION")

                ]

            ),

            html.H4(
                "Hipótesis"
            ),

            dbc.Card(

                dbc.CardBody(

                    """
                    Las cuentas con mayores desviaciones
                    entre consumo histórico y consumo actual
                    presentan una mayor probabilidad
                    de requerir ajustes.
                    """

                )

            )

        ],

        fluid=True

    )