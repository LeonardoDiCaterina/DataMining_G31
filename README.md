# DataMining_G31
Group 31 data mining project
# Data Analysis and Visualization Notebook

This Jupyter Notebook is dedicated to the analysis and visualization of customer data from the `DM2425_ABCDEats_DATASET.csv` file. The notebook includes various steps to clean, analyze, and visualize the data to extract meaningful insights.

## Table of Contents

1. **Importing Packages and Data**
    - Import necessary libraries such as `pandas`, `numpy`, `matplotlib.pyplot`, and `seaborn`.
    - Load the dataset into a DataFrame.

2. **Data Exploration**
    - Display the first few rows of the DataFrame.
    - Identify unique values in the `customer_region` column.
    - Calculate the number of rows lost by removing NaN values.
    - Summarize key statistics for the DataFrame.
    - Explore non-numerical columns and their unique values.

3. **Data Cleaning**
    - Replace specific values with NaN.
    - Drop rows with NaN values and compare the shape of the DataFrame before and after.

4. **Feature Engineering**
    - Create new features such as `delta_day_order`, `tot_value_cui`, `order_freq`, `value_freq`, and `avg_order_value`.
    - Append these new features to a list for further analysis.

5. **Data Validation**
    - Check for NaN and infinite values in the new features.
    - Describe the new features to understand their statistical properties.

6. **Age Analysis**
    - Summarize customer age statistics.
    - Visualize the distribution and impact of age on various metrics using violin plots and scatter plots.
    - Add error bars to scatter plots for better visualization.

7. **Region Analysis**
    - Analyze and visualize the impact of customer region on various metrics.
    - Create bar plots with error bars to show average values and their standard deviations across regions.
    - Summarize regional statistics in a DataFrame.

## Key Variables

- `df`: The main DataFrame containing the customer data.
- `noNaN_df`: DataFrame after removing rows with NaN values.
- `new_fetures_list`: List of newly engineered features.
- `region_stats`: DataFrame summarizing statistics for different regions.
- `age_order_freq`, `age_order_value_mean`, `age_value_freq`, etc.: DataFrames containing age-related metrics.
- `avg_age_per_region`, `avg_order_value_per_region`, etc.: Series containing region-related metrics.

This notebook provides a comprehensive analysis of customer data, focusing on age and region-specific insights, and employs various visualization techniques to present the findings effectively.
