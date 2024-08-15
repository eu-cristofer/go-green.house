# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 10:25:15 2023

@author: Cristofer Costa
"""

import numpy as np
import pandas as pd
import json
import plotly.graph_objects as go

# Define the birth timestamp for reference
birth = pd.Timestamp("2022-10-16 11:48:00")


def get_json_data(database):
    """
    Load and process the JSON database data, returning it as a pandas DataFrame.

    Parameters
    ----------
    database : str
        Path to the JSON database file containing baby data.

    Returns
    -------
    df : pd.DataFrame
        DataFrame with the index as pd.Datetime and a column representing
        the timedelta in months from the first entry in the series.
    """
    # Read data from the JSON file
    with open(database, "r", encoding="utf8") as file:
        json_data = json.load(file)

    # Convert JSON data to a DataFrame
    df = pd.DataFrame.from_dict(json_data, orient="index")
    # Convert the index to pd.Datetime
    df.index = pd.to_datetime(df.index)

    # Create a column with timedelta in months from the first sample
    delta = df.index - df.index[-1]
    df["Months"] = delta.days / 30.44  # Approximate average days in a month
    return df


# Load data for Sofia and Maria
sofia = get_json_data("DB_Sofia.json")
maria = get_json_data("DB_Maria.json")

# Read reference data from Excel files
# Source: https://www.who.int/tools/child-growth-standards/standards/weight-for-age
source = dict()
source["wfa_z"] = pd.read_excel("ref/wfa_girls_0-to-5-years_zscores.xlsx", index_col=0)
source["hcfa_z"] = pd.read_excel("ref/hcfa-girls-0-5-zscores.xlsx", index_col=0)
source["lfa_birth_z"] = pd.read_excel(
    "ref/lhfa_girls_0-to-2-years_zscores.xlsx", index_col=0
)

# Create a dictionary to map index to datetime based on months from birth
source_index = {i: birth + i * pd.DateOffset(months=1) for i in source["wfa_z"].index}


def plot_df(df, description, months_to_plot=12):
    """
    Plot reference curves and individual data for a given description.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing reference curves.
    description : str
        Column name from the girl data to plot.
    months_to_plot : int, optional
        Number of months to plot on the x-axis. The default is 12.

    Returns
    -------
    fig : plotly.graph_objects.Figure
        Figure object containing the plot.
    """
    fig = go.Figure()

    # Add reference curves to the plot
    fig.add_scatter(
        x=df.index,
        y=df.SD3neg.loc[:months_to_plot].values,
        mode="lines",
        name="-3",
        line={"color": "rgba(241, 148, 138, 0.5)"},
        showlegend=False,
    )
    fig.add_annotation(
        x=months_to_plot, y=df.SD3neg.loc[months_to_plot], text="-3", showarrow=False
    )

    fig.add_scatter(
        x=df.index,
        y=df.SD3.loc[:months_to_plot].values,
        mode="lines",
        name="3",
        line={"color": "rgba(241, 148, 138, 0.5)"},
        showlegend=False,
    )
    fig.add_annotation(
        x=months_to_plot, y=df.SD3.loc[months_to_plot], text="3", showarrow=False
    )

    fig.add_scatter(
        x=df.index,
        y=df.SD2neg.loc[:months_to_plot].values,
        mode="lines",
        name="-2",
        line={"color": "rgba(52, 152, 219, 0.5)"},
        showlegend=False,
    )
    fig.add_annotation(
        x=months_to_plot, y=df.SD2neg.loc[months_to_plot], text="-2", showarrow=False
    )

    fig.add_scatter(
        x=df.index,
        y=df.SD2.loc[:months_to_plot].values,
        mode="lines",
        name="2",
        line={"color": "rgba(52, 152, 219, 0.5)"},
        showlegend=False,
    )
    fig.add_annotation(
        x=months_to_plot, y=df.SD2.loc[months_to_plot], text="2", showarrow=False
    )

    fig.add_scatter(
        x=df.index,
        y=df.SD0.loc[:months_to_plot].values,
        mode="lines",
        name="0",
        line={"color": "rgba(26, 188, 156, 0.5)"},
        showlegend=False,
    )
    fig.add_annotation(
        x=months_to_plot, y=df.SD0.loc[months_to_plot], text="0", showarrow=False
    )

    # Dictionary for legend text
    legend = {
        "Peso": "Peso em [kg]",
        "Perímetro Cefálico": "Perímetro Cefálico [cm]",
        "Estatura": "Estatura [cm]",
    }

    # Add individual data points for Sofia and Maria
    fig.add_scatter(
        x=sofia["Months"],
        y=sofia[description].values,
        mode="markers",
        name="Sofia",
        marker=dict(size=10),
    )
    fig.add_scatter(
        x=maria["Months"],
        y=maria[description].values,
        mode="markers",
        name="Maria",
        marker=dict(size=10),
    )

    # Update plot layout
    fig.update_layout(
        autosize=False,
        width=750,
        height=550,
        title=description,
        title_x=0.5,
        xaxis=dict(title_text="Meses"),
        yaxis=dict(title_text=legend[description]),
        legend=dict(yanchor="top", xanchor="left", y=0.98, x=0.01),
    )
    return fig


if __name__ == '__main__':
    import plotly.io as pio
    
    # Read the HTML template
    with open('docs/template.html', 'r', encoding="utf8") as html:
        file = html.read()
    
    # Iterate over the keys and labels of the source dictionary
    for key, label in zip(source.keys(), ['Peso', 'Perímetro Cefálico', 'Estatura']):
        # Generate the plot for each reference data
        chart = plot_df(source[key], label, 22)
        # Convert the plotly chart to JSON format
        json_file = pio.to_json(chart)
        # Extract the data and layout from the JSON file
        str_data = json.dumps(json.loads(json_file)['data'])
        str_layout = json.dumps(json.loads(json_file)['layout'])
        # Replace the placeholders in the template with the actual data and layout
        file = file.replace(label.upper() + '_DATA', str_data)
        file = file.replace(label.upper() + '_LAYOUT', str_layout)
        
    # Write the modified HTML content to the output file
    with open('docs/index.html', 'w', encoding="utf8") as html:
        html.write(file)
