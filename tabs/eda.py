from dash import dcc, html
import dash_bootstrap_components as dbc


def create_eda_tab():

    return dbc.Container(

        [

            html.H2(
                "Exploratory Data Analysis (EDA)",
                className="mb-4"
            ),

            # ==================================================
            # PIE
            # ==================================================

            dbc.Card(

                dbc.CardBody(

                    [

                        dcc.Graph(
                            id="pie-ajustes"
                        )

                    ]

                ),

                className="mb-4 shadow-sm"

            ),

            # ==================================================
            # BAR CHART
            # ==================================================

            dbc.Card(

                dbc.CardBody(

                    [

                        html.H5(
                            "Promedio de Ajuste"
                        ),

                        dcc.Dropdown(

                            id="segment-selector",

                            options=[

                                {
                                    "label": "Categoría",
                                    "value": "CATEGORIA"
                                },

                                {
                                    "label": "Plan Facturación",
                                    "value": "PLAN_FACTURACION"
                                }

                            ],

                            value="CATEGORIA",

                            clearable=False

                        ),

                        dcc.Graph(
                            id="bar-ajustes"
                        )

                    ]

                ),

                className="mb-4 shadow-sm"

            ),

            # ==================================================
            # HISTOGRAMA
            # ==================================================

            dbc.Card(

                dbc.CardBody(

                    [

                        html.H5(
                            "Distribuciones"
                        ),

                        dbc.Row(

                            [

                                dbc.Col(

                                    dcc.Dropdown(

                                        id="hist-variable",

                                        options=[

                                            {
                                                "label": "M3 Periodo",
                                                "value": "M3_PERIODO"
                                            },

                                            {
                                                "label": "Facturación Periodo",
                                                "value": "FACTURACION_PERIODO"
                                            }

                                        ],

                                        value="M3_PERIODO",

                                        clearable=False

                                    )

                                ),

                                dbc.Col(

                                    dcc.Dropdown(

                                        id="acd-filter"

                                    )

                                ),

                                dbc.Col(

                                    dcc.Dropdown(

                                        id="ciclo-filter"

                                    )

                                )

                            ]

                        ),

                        html.Br(),

                        dcc.Graph(
                            id="histograma-dinamico"
                        )

                    ]

                ),

                className="mb-4 shadow-sm"

            ),

            # ==================================================
            # HEATMAP
            # ==================================================

            dbc.Card(

                dbc.CardBody(

                    [

                        dcc.Graph(
                            id="heatmap-correlation"
                        )

                    ]

                ),

                className="mb-4 shadow-sm"

            ),

            # ==================================================
            # SCATTER
            # ==================================================

            dbc.Card(

                dbc.CardBody(

                    [

                        dcc.Graph(
                            id="scatter-ajustes"
                        )

                    ]

                ),

                className="mb-4 shadow-sm"

            ),

            html.Hr(),

            html.H3(
                "Preparación para Machine Learning"
            ),

            html.P(

                """
                Evaluación visual de la capacidad
                discriminatoria de las variables
                derivadas respecto a TARGET_AJUSTE.
                """

            ),

            # ==================================================
            # BOXPLOT M3
            # ==================================================

            dbc.Card(

                dbc.CardBody(

                    [

                        dcc.Graph(
                            id="boxplot-m3"
                        )

                    ]

                ),

                className="mb-4 shadow-sm"

            ),

            # ==================================================
            # BOXPLOT FACTURACION
            # ==================================================

            dbc.Card(

                dbc.CardBody(

                    [

                        dcc.Graph(
                            id="boxplot-facturacion"
                        )

                    ]

                ),

                className="mb-4 shadow-sm"

            )

        ],

        fluid=True

    )