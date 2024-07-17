import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
import dash_bootstrap_components as dbc


def load_data(file_path):
    # Load spreadsheet
    xl = pd.ExcelFile(file_path)

    # Load sheets into DataFrames by their names
    df_4a = xl.parse('Table 4a')
    df_3c = xl.parse('Table 3c')

    return df_4a, df_3c


def combine_dataframes(df1, df2):
    # Check DataFrame's index
    df1.set_index('Time period', inplace=True)
    df2.set_index('Time period', inplace=True)

    # Join the two DataFrames
    df_combined = df1.join(df2, lsuffix='_4a', rsuffix='_3c')

    return df_combined


def filter_data(df):
    # Filter data for September, October and November 2023
    df_filtered = df.loc[['Sep 2023', 'Oct 2023', 'Nov 2023']]

    return df_filtered


def remove_outliers(df):
    # Calculate quartiles and IQR
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1

    # Remove outliers
    df = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]

    return df


def handle_missing_values(df):
    # Check for missing values in all columns
    missing_values = df.isnull().sum()
    print("Missing values: \n", missing_values)

    # Fill missing values with the mean of the column
    df.fillna(df.mean(), inplace=True)

    return df


def convert_to_numeric(df):
    # Convert all columns to numeric
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df


def plot_trends(df, title, xlabel, ylabel, legend_size):
    fig = go.Figure()
    for col in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines+markers', name=col))
    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        autosize=False,
        width=1000,
        height=600,
        legend=dict(font=dict(size=legend_size))
    )
    return fig


def trends(df, categories, title, color_palette):
    fig = go.Figure()
    for i, category in enumerate(categories):
        fig.add_trace(go.Scatter(x=df.index, y=df[category], mode='lines', name=category, stackgroup='one',
                                 line=dict(width=0.5, color=color_palette[i])))
    fig.update_layout(title_text=title, xaxis_title='Time Period', yaxis_title='Value')
    return fig


def plot_bar(df, title, xlabel, ylabel, colors):
    fig = go.Figure(data=[go.Bar(x=df.index, y=df[col], name=col, marker_color=colors) for col in df.columns])
    fig.update_layout(
        title_text=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        barmode='group'
    )
    return fig


def plot_stacked_area(df, title, xlabel, ylabel):
    # Create a copy of the DataFrame
    df = df.copy()

    # Group the column names
    df['Housing'] = df[
        ['Public new housing_4a', 'Private new housing_4a', 'Total new housing_4a', 'Public housing R&M_4a',
         'Private housing R&M_4a']].sum(axis=1)
    df['New Work'] = df[['Infrastructure new work_4a', 'Public other new work_4a', 'Private industrial new work_4a',
                         'Private commercial new work_4a']].sum(axis=1)
    df['R&M'] = df['All R&M_4a'] - df['Total housing R&M_4a']

    color_palette = ['#e6194b', '#3cb44b', '#ffe119']
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df.index, y=df['Housing'], mode='lines', name='Housing', stackgroup='one',
                             line=dict(width=0.5, color=color_palette[0])))
    fig.add_trace(go.Scatter(x=df.index, y=df['New Work'], mode='lines', name='New Work', stackgroup='one',
                             line=dict(width=0.5, color=color_palette[1])))
    fig.add_trace(go.Scatter(x=df.index, y=df['R&M'], mode='lines', name='R&M', stackgroup='one',
                             line=dict(width=0.5, color=color_palette[2])))

    fig.update_layout(title_text=title, xaxis_title=xlabel, yaxis_title=ylabel)

    return fig


def main():
    # Usage of functions
    file_path = "C:\\Users\\HP\\Desktop\\Masters\\Data Visualization(15)\\newdata.xlsx"
    print(file_path)

    df_4a, df_3c = load_data(file_path)
    df_combined = combine_dataframes(df_4a, df_3c)
    df_filtered = filter_data(df_combined)
    df_filtered = remove_outliers(df_filtered)
    df_filtered = handle_missing_values(df_filtered)
    df_filtered = convert_to_numeric(df_filtered)

    # Filter preprocessed data for September, October and November 2023
    df_filtered = df_filtered.loc[['Sep 2023', 'Oct 2023', 'Nov 2023']]
    print(df_filtered.head())

    # Get column names for each sheet
    columns_4a = [col for col in df_filtered.columns if col.endswith('_4a')]
    columns_3c = [col for col in df_filtered.columns if col.endswith('_3c')]

    # Create filtered DataFrames for each sheet
    df_4a_filtered = df_filtered[columns_4a]
    df_3c_filtered = df_filtered[columns_3c]

    # EDA
    # Descriptive statistics
    print(df_4a_filtered.describe())
    print(df_3c_filtered.describe())

    # Correlation matrix
    print(df_4a_filtered.corr())
    print(df_3c_filtered.corr())

    # Create plots
    sectors_to_plot = ['Total new housing_4a', 'Infrastructure new work_4a', 'All new work_4a', 'Total housing R&M_4a']
    df_subset = df_4a_filtered[sectors_to_plot]
    trends_plot = plot_trends(df_subset, 'Trend of Each Sector Over Time', 'Time Period', 'Value', 6)
    trends_plot.update_layout(height=300, width=500, legend=dict(x=0.5, y=-0.3, xanchor='center',
                                                                 orientation='h'), margin=dict(t=50, b=100))

    df_subset = df_4a_filtered[['Total new housing_4a']]
    color1 = '#0000cd'
    bar_plot1 = plot_bar(df_subset, 'Trend in Total New Housing Construction', 'Time Period', 'Value', color1)
    bar_plot1.update_layout(height=300, width=500, legend=dict(x=0.5, y=-0.3, xanchor='center',
                                                               orientation='h'), margin=dict(t=50, b=100))

    df_subset1 = df_3c_filtered[['Infrastructure new work_3c', 'Total new housing_3c']]
    color_palette1 = ['#0000FF', '#FFA500']
    trends_plot1 = trends(df_subset1, ['Infrastructure new work_3c', 'Total new housing_3c'], 'Infrastructure vs '
                                                                                              'Housing',
                          color_palette1)
    trends_plot1.update_layout(height=300, width=500, legend=dict(x=0.5, y=-0.3, xanchor='center',
                                                                  orientation='h'), margin=dict(t=50, b=100))

    df_subset2 = df_4a_filtered[['Public new housing_4a', 'Private new housing_4a']]
    color_palette2 = ['#008080', '#800000']
    trends_plot2 = trends(df_subset2, ['Public new housing_4a', 'Private new housing_4a'], 'Public vs Private Housing',
                          color_palette2)
    trends_plot2.update_layout(height=300, width=500, legend=dict(x=0.5, y=-0.3, xanchor='center',
                                                                  orientation='h'), margin=dict(t=50, b=100))

    df_subset = df_4a_filtered[['Total housing R&M_4a']]
    color2 = '#ef9b20'  # A shade of orange
    bar_plot2 = plot_bar(df_subset, 'Trend in Total Housing Repair & Maintenance', 'Time Period', 'Value', color2)
    bar_plot2.update_layout(height=300, width=500, legend=dict(x=0.5, y=-0.3, xanchor='center',
                                                               orientation='h'), margin=dict(t=50, b=100))

    stacked_area_plot = plot_stacked_area(df_4a_filtered, 'Overall Trend in the Construction Industry', 'Time Period',
                                          'Value')
    stacked_area_plot.update_layout(height=300, width=500, legend=dict(x=0.5, y=-0.3, xanchor='center',
                                                                       orientation='h'), margin=dict(t=50, b=100))

    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Define the layout of the dashboard
    app.layout = dbc.Container([
        dbc.Row([
            dbc.Col(dcc.Graph(id='graph-1', figure=trends_plot), md=4),  # Set md to 4
            dbc.Col(dcc.Graph(id='graph-2', figure=bar_plot1), md=4),
            dbc.Col(dcc.Graph(id='graph-3', figure=trends_plot1), md=4)
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='graph-4', figure=trends_plot2), md=4),
            dbc.Col(dcc.Graph(id='graph-5', figure=bar_plot2), md=4),
            dbc.Col(dcc.Graph(id='graph-6', figure=stacked_area_plot), md=4)
        ])
    ], fluid=True)

    # Run the Dash app
    if __name__ == '__main__':
        app.run_server(debug=True)


# Call the main function
main()
