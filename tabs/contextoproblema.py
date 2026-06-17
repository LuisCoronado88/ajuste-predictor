import dash_bootstrap_components as dbc
from dash import html
import pandas as pd


def create_context_tab(
    df: pd.DataFrame
):

    total_cuentas = df["CUENTA"].nunique()

    total_ajustadas = (
        df["TARGET_AJUSTE"]
        .sum()
    )

    porcentaje_ajustadas = (
        df["TARGET_AJUSTE"]
        .mean()
        * 100
    )

    valor_total_ajustes = (
        df["VALOR_AJUSTE_PERIODO"]
        .sum()
    )

    return dbc.Container(

        [

            dbc.Alert(

                [

                    html.H2(
                        "AjustePredictor"
                    ),

                    html.P(
                        "Análisis histórico para identificar "
                        "cuentas con potencial de ajuste "
                    )

                ],
                color="primary"

            ),

            dbc.Row(

                [

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H3(
                                        f"{total_cuentas:,}"
                                    ),
                                    html.P(
                                        "Total Cuentas"
                                    )
                                ]
                            )
                        )
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H3(
                                        f"{total_ajustadas:,}"
                                    ),
                                    html.P(
                                        "Cuentas Ajustadas"
                                    )
                                ]
                            )
                        )
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H3(
                                        f"{porcentaje_ajustadas:.2f}%"
                                    ),
                                    html.P(
                                        "% Ajustadas"
                                    )
                                ]
                            )
                        )
                    ),

                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H3(
                                        f"${valor_total_ajustes:,.0f}"
                                    ),
                                    html.P(
                                        "Valor Total Ajustado"
                                    )
                                ]
                            )
                        )
                    ),

                ],

                className="mb-4"

            ),

            html.Hr(),

            html.H3(
                "Beneficios Esperados"
            ),

            html.Ul(

                [

                    html.Li(
                        "Reducción de pérdidas financieras"
                    ),

                    html.Li(
                        "Disminución de PQR"
                    ),

                    html.Li(
                        "Gestión proactiva de clientes"
                    ),

                    html.Li(
                        "Optimización operativa"
                    ),

                    html.Li(
                        "Priorización de inspecciones"
                    )

                ]

            )

        ],

        fluid=True

    )