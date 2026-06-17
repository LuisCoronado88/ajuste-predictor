from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from dash import (
    Dash,
    Input,
    Output,
    html
)

from data.data_loader import load_dataset

from tabs.contextoproblema import (
    create_context_tab
)

from tabs.metodologia import (
    create_methodology_tab
)

from tabs.eda import (
    create_eda_tab
)


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

DATA_PATH = Path("data/DataAjuste.csv")

df = load_dataset(DATA_PATH)


# ==========================================================
# APP
# ==========================================================

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.FLATLY
    ],
    suppress_callback_exceptions=True
)

server = app.server

app.title = "AjustePredictor"


# ==========================================================
# LAYOUT
# ==========================================================

app.layout = dbc.Container(

    [

        html.H1(
            "AjustePredictor",
            className="main-title"
        ),

        html.P(
            (
                "Sistema Analítico para Identificación "
                "Temprana de Ajustes de Facturación"
            ),
            className="text-center mb-4"
        ),

        dbc.Tabs(

            [

                dbc.Tab(
                    label="Contexto del Problema",
                    tab_id="context"
                ),

                dbc.Tab(
                    label="Metodología",
                    tab_id="methodology"
                ),

                dbc.Tab(
                    label="EDA",
                    tab_id="eda"
                ),

            ],

            id="tabs",
            active_tab="context"

        ),

        html.Br(),

        html.Div(
            id="tab-content"
        )

    ],

    fluid=True

)


# ==========================================================
# RENDER TABS
# ==========================================================

@app.callback(
    Output(
        "tab-content",
        "children"
    ),
    Input(
        "tabs",
        "active_tab"
    )
)
def render_tab(active_tab):

    if active_tab == "context":
        return create_context_tab(df)

    if active_tab == "methodology":
        return create_methodology_tab()

    return create_eda_tab()


# ==========================================================
# FILTROS
# ==========================================================

@app.callback(
    Output(
        "acd-filter",
        "options"
    ),
    Output(
        "acd-filter",
        "value"
    ),
    Output(
        "ciclo-filter",
        "options"
    ),
    Output(
        "ciclo-filter",
        "value"
    ),
    Input(
        "tabs",
        "active_tab"
    )
)
def load_filters(_):

    acd_values = sorted(
        df["ACD_CODIGO"]
        .dropna()
        .unique()
    )

    ciclo_values = sorted(
        df["CICLO"]
        .dropna()
        .unique()
    )

    return (

        [
            {
                "label": str(i),
                "value": i
            }
            for i in acd_values
        ],

        acd_values,

        [
            {
                "label": str(i),
                "value": i
            }
            for i in ciclo_values
        ],

        ciclo_values

    )


# ==========================================================
# PIE CHART
# ==========================================================

@app.callback(
    Output(
        "pie-ajustes",
        "figure"
    ),
    Input(
        "tabs",
        "active_tab"
    )
)
def update_pie(_):

    pie_df = (
        df["TARGET_AJUSTE"]
        .map(
            {
                0: "Sin Ajuste",
                1: "Con Ajuste"
            }
        )
        .value_counts()
        .reset_index()
    )

    pie_df.columns = [
        "Estado",
        "Cantidad"
    ]

    fig = px.pie(
        pie_df,
        names="Estado",
        values="Cantidad",
        title="Distribución de Ajustes"
    )

    return fig


# ==========================================================
# BAR CHART
# ==========================================================

@app.callback(
    Output(
        "bar-ajustes",
        "figure"
    ),
    Input(
        "segment-selector",
        "value"
    )
)
def update_bar(segment):

    grouped = (
        df.groupby(segment)
        ["VALOR_AJUSTE_PROMEDIO"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        grouped,
        x=segment,
        y="VALOR_AJUSTE_PROMEDIO",
        title=f"Ajuste Promedio por {segment}"
    )

    return fig


# ==========================================================
# HISTOGRAMA DINÁMICO
# ==========================================================

@app.callback(
    Output(
        "histograma-dinamico",
        "figure"
    ),
    Input(
        "hist-variable",
        "value"
    ),
    Input(
        "acd-filter",
        "value"
    ),
    Input(
        "ciclo-filter",
        "value"
    )
)
def update_histogram(
    variable,
    acd_values,
    ciclo_values
):

    filtered = df.copy()

    if acd_values:

        filtered = filtered[
            filtered["ACD_CODIGO"]
            .isin(acd_values)
        ]

    if ciclo_values:

        filtered = filtered[
            filtered["CICLO"]
            .isin(ciclo_values)
        ]

    fig = px.histogram(
        filtered,
        x=variable,
        nbins=40,
        title=f"Distribución de {variable}"
    )

    return fig


# ==========================================================
# HEATMAP
# ==========================================================

@app.callback(
    Output(
        "heatmap-correlation",
        "figure"
    ),
    Input(
        "tabs",
        "active_tab"
    )
)
def update_heatmap(_):

    corr_cols = [

        "FACTURACION_PROMEDIO",
        "FACTURACION_PERIODO",
        "M3_PROMEDIO",
        "M3_PERIODO",
        "DELTA_M3",
        "DELTA_FACTURACION",
        "VALOR_AJUSTE_PROMEDIO"

    ]

    corr_matrix = (
        df[corr_cols]
        .corr(method="pearson")
    )

    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        title="Mapa de Correlación Pearson"
    )

    return fig


# ==========================================================
# SCATTER
# ==========================================================

@app.callback(
    Output(
        "scatter-ajustes",
        "figure"
    ),
    Input(
        "tabs",
        "active_tab"
    )
)
def update_scatter(_):

    fig = px.scatter(
        df,
        x="DELTA_M3",
        y="VALOR_AJUSTE_PROMEDIO",
        color="TARGET_AJUSTE",
        hover_data=[
            "CUENTA",
            "CATEGORIA",
            "PLAN_FACTURACION"
        ],
        title="DELTA_M3 vs Valor Ajuste Promedio"
    )

    return fig


# ==========================================================
# BOXPLOT DELTA_M3
# ==========================================================

@app.callback(
    Output(
        "boxplot-m3",
        "figure"
    ),
    Input(
        "tabs",
        "active_tab"
    )
)
def update_box_m3(_):

    fig = px.box(
        df,
        x="TARGET_AJUSTE",
        y="DELTA_M3",
        color="TARGET_AJUSTE",
        points="outliers",
        title="DELTA_M3 por Estado de Ajuste"
    )

    return fig


# ==========================================================
# BOXPLOT DELTA_FACTURACION
# ==========================================================

@app.callback(
    Output(
        "boxplot-facturacion",
        "figure"
    ),
    Input(
        "tabs",
        "active_tab"
    )
)
def update_box_facturacion(_):

    fig = px.box(
        df,
        x="TARGET_AJUSTE",
        y="DELTA_FACTURACION",
        color="TARGET_AJUSTE",
        points="outliers",
        title="DELTA_FACTURACION por Estado de Ajuste"
    )

    return fig


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":
    app.run(
        debug=True
    )