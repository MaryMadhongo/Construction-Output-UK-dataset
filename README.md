# Construction-Output-UK-dataset
Big Data Visualisation Product Development
This project is part of an R&D initiative at a data science start-up. It develops a Big Data visualization tool for junior government officials. The tool analyzes the Construction Output UK dataset from September 2023 to November 2023 , focusing on housing market trends and maintenance sectors, to provide data-driven narratives for journalists in public media.
Functions Included:
1. load_data(file_path):
* Function to load data from an Excel spreadsheet and return specified DataFrames.
2. combine_dataframes(df1, df2):
* Function to combine two DataFrames by their index and return a single DataFrame.
3. filter_data(df):
* Function to filter data for specified time periods (September, October, and November 2023).
4. remove_outliers(df):
* Function to remove outliers from the DataFrame using the Interquartile Range (IQR) method.
5. handle_missing_values(df):
* Function to handle missing values in the DataFrame by filling them with the mean of the column.
6. convert_to_numeric(df):
* Function to convert all columns in the DataFrame to numeric data type.
7. trends(df, categories, title, color_palette):
* Function to plot trends for each category in the DataFrame on a single graph.
8. plot_trends(df, title, xlabel, ylabel, legend_size):
* Function to plot trends for each column in the DataFrame on a single graph.
9. plot_bar(df, title, xlabel, ylabel, colors):
* Function to plot a bar chart for each column in the DataFrame.
10. plot_stacked_area(df, title, xlabel, ylabel):
* Function to plot a stacked area chart for the DataFrame.
11. main():
* Main function to call the above functions and execute the data analysis and visualization pipeline.
Dependencies:
pandas
plotly
dash
dash_bootstrap_components
Usage:
1. Setup Python Environment: Ensure you have a Python environment set up. You can use an Integrated Development Environment (IDE) like PyCharm, Jupyter Notebook, or Visual Studio Code.
2. Install Dependencies: Install the required dependencies (pandas, plotly, dash, and dash_bootstrap_components) in your Python environment. You can do this using pip:
3. Python -  pip install pandas, plotly ,dash, dash_bootstrap_components
4. Load Libraries: At the start of your script, import the necessary libraries. This includes pandas for data manipulation, plotly for interactive plots, and dash for building web-based visualizations.
5. Update File Path: Update the file_path variable in the script to specify the path to your Excel file found on https://www.ons.gov.uk/businessindustryandtrade/constructionindustry/datasets/outputintheconstructionindustry .
6. Run the Code: Execute the script in your Python environment to analyze and visualize the data. You can do this by running the main() function.
7. View the Dashboard: The dashboard will be served on a local web server and can be viewed in a web browser on http://127.0.0.1:8050/.
