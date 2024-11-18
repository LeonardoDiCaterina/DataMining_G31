import pandas as pd # type: ignore
import numpy as np # type: ignore


def safe_divide(series1, series2):
    ZeroDivisionError_count = 0
    Exception_count = 0
    result = []
    for val1, val2 in zip(series1, series2):
        try:
            result.append(val1 / val2)
        except ZeroDivisionError:
            ZeroDivisionError_count += 1 
            result.append(np.nan)
        except Exception as e:
            print(f"Error: {e}")
            Exception_count += 1
            result.append(np.nan)
    return pd.Series(result)


def cleanUp(df):
    """
    **Purpose:**

    - Cleans and preprocesses the raw data for subsequent analysis.
    - Ensures consistent data preparation across multiple notebooks, preventing modifications to the original data or the need for additional tables.

    **Arguments:**

    - `df (pandas.DataFrame)`: The raw data to be processed.

    **Returns:**

    - `tuple`: A tuple containing:
        - `pandas.DataFrame`: The cleaned and preprocessed data, including any newly generated feature columns.
        - `dict`: A dictionary containing lists of various types of columns:
            - `non_numerical_columns`: List of non-numerical columns.
            - `new_features_list`: List of newly generated feature columns.
            - `numerical_columns`: List of numerical columns.
            - `CUI_col`: List of columns starting with 'CUI'.
            - `HR_col`: List of columns starting with 'HR'.
            - `DOW_col`: List of columns starting with 'DOW'.

    **Output:**

    - Presence of repetitions in the primary key.

    **Example Usage:**

    ```
    import pandas as pd
    import numpy as np

    # Load the raw data
    raw_data = pd.read_csv("path/to/your/data.csv")

    # Preprocess the data
    cleaned_data, columns_dict = cleanUp(raw_data)

    # Perform analysis on the cleaned data

    """
    
    #-----------looking for incostisencies -----------
    print("-----------looking for incostisencies -----------")

    # identify the primary key
    PrimarKey = 'customer_id'
    
    # check for repeated values in the primary key
    x=df[PrimarKey].value_counts()
    repeated_df_Id = x[x>1] 
    
    repetitions_df = []
    try:
        repetitions_df = df[df[PrimarKey] == repeated_df_Id.index[0]]
        size_rep = len(repetitions_df)

    except:
        size_rep = 0
    
    if size_rep > 0:
        print("There are repeated values in the dataset")
        print(repetitions_df)
        
        
    DOW_col = [col for col in df.columns if col.startswith('DOW')]
    HR_col = [col for col in df.columns if col.startswith('HR')]
    DOW_col_sum = df[DOW_col].sum(axis=1)
    HR_col_sum = df[HR_col].sum(axis=1)
    Delta_DOW_HR = DOW_col_sum-HR_col_sum
    
    HR_col_from1 = HR_col.copy()
    HR_col_from1.remove('HR_0')   
    
    HR_col_from1_sum = df[HR_col_from1].sum(axis=1)
    df['HR_0'] = DOW_col_sum - HR_col_from1_sum 
        
    
    #-----------identify the numerical columns -----------
    print("-----------identify the numerical columns -----------")

    numerical_columns = df.select_dtypes(include=np.number).columns
    try:
        numerical_columns.remove(PrimarKey)
        print("primary_key is numerical")

    except:
        print("primary_key is not numerical")
    

    #-----------Identify the non numerical columns--------------
    print("-----------Identify the non numerical columns -----------")

    non_numerical_columns = df.select_dtypes(include=['object']).columns.tolist()
    try:
        non_numerical_columns.remove(PrimarKey)
        print("primary_key is non numerical")
    except:
        print("primary_key is numerical")
    #----------- Drop uslesless rows ------------
    print("----------- Drop uslesless rows ------------")
    l_df = len(df)  
    df = df[df['tot_value_cui'] != 0]
    print(f"tot_value_cui, removed {l_df - len(df)} rows")
    l_df = len(df)
    df = df[df['product_count'] != 0]
    print(f"product_count, removed {l_df - len(df)} rows")
    l_df = len(df)
    df = df[df['order_count'] != 0]
    print(f"order_count, removed {l_df - len(df)} rows")
    l_df = len(df)
    
    #----------- Fill missing values ------------
    print("----------- Fill missing values ------------")
    
    # in customer_age we willl fill the missing values with the median because the distribution is skewed
    df['customer_age'] = df['customer_age'].fillna(df['customer_age'].median())
    print(f"customer_age, subsitution with median: {df['customer_age'].median()}")
    
    # in first_order we will fill the missing values with 0 because we assume that the customer where there before the stat of the dataset
    df['first_order'] = df['first_order'].fillna(0)
    print(f"first_order, subsitution with 0")
    
    #
    
    # in customer_region the missing values are better in nan so they do not show on the graphs
    df.loc[df['customer_region'] == '-', 'customer_region'] = np.nan
    
    #payment method is fine
    
    #-------------- building new key features -----------
    print("-------------- building new key features -----------")
    new_fetures_list = []
    
    #----- (1) customer_city
    print("----- (1) customer_city")
    
    df['customer_city'] = df['customer_region'].str[0]
    new_fetures_list.append('customer_city')
    #----- (2) used_promo
    print("----- (2) used_promo")

    df.loc[df['last_promo'] == '-', 'last_promo'] = "No_Promo"
    df['used_promo']= df['last_promo'] != 'No_Promo'
    new_fetures_list.append("used_promo") 

    #----- (3) order_count
    print("----- (3) order_count")
    
    df['order_count'] = df[DOW_col].sum(axis=1)
    new_fetures_list.append("order_count")


    #----- (4) avg_product_by_order
    print("----- (4) avg_product_by_order")
   
    df['avg_product_by_order'] = safe_divide(df['product_count'],df['order_count'])
    new_fetures_list.append("avg_product_by_order")

    #----- (5) delta_day_order
    print("----- (5) delta_day_order")
   
    df['delta_day_order'] = df['last_order'] - df['first_order'] + 1
    new_fetures_list.append('delta_day_order')

    #----- (6) tot_value_cui
    print("----- (6) tot_value_cui")
   
    cui_columns = [col for col in df.columns if col.startswith('CUI')]
    df['tot_value_cui'] = df[cui_columns].sum(axis=1)
    new_fetures_list.append('tot_value_cui')
    
    #----- (7) order_freq
    print("----- (7) order_freq")
   
    df['order_freq'] = safe_divide(df['order_count'], df['delta_day_order'])
    new_fetures_list.append('order_freq')
   
    #----- (8) value_freq
    print("----- (8) value_freq")
   
    df['value_freq'] =safe_divide(df['tot_value_cui'], df['delta_day_order'])
    new_fetures_list.append('value_freq')
   
    #----- (9) value_freq
    print("----- (9) value_freq")
   
    df['product_freq'] = safe_divide(df['product_count'], df['delta_day_order'])
    new_fetures_list.append('product_freq')

    #----- (10) avg_order_value
    print("----- (10) avg_order_value")
   
    df['avg_order_value'] = safe_divide(df['tot_value_cui'], df['order_count'])
    new_fetures_list.append('avg_order_value')
    df['avg_order_value'] = np.where(df['product_count'] != 0, df['tot_value_cui'] / df['product_count'], 0)
    #----- (11) avg_product_value
    print("#----- (11) avg_product_value")
   
    df['avg_product_value'] = safe_divide(df['tot_value_cui'], df['product_count'])
    new_fetures_list.append('avg_product_value')



    #-------------- create dictionary -----------
    
    CUI_col = [col for col in df.columns if col.startswith('CUI')]
    HR_col = [col for col in df.columns if col.startswith('HR')]
    
    columns_dict = {
    'non_numerical_columns': non_numerical_columns,
    'new_features_list': new_fetures_list,
    'numerical_columns': numerical_columns,
    'CUI_col': CUI_col,
    'HR_col': HR_col,
    'DOW_col': DOW_col
    }
    return df, columns_dict

def count_outliers(df, column_name):
    """
    Count the number of outliers in a specified column of a DataFrame using the IQR method.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    column_name (str): The name of the column to analyze.

    Returns:
    int: The number of outliers in the specified column.
    """
    # Calculate Q1 (25th percentile) and Q3 (75th percentile)
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)

    # Calculate IQR (Interquartile Range)
    IQR = Q3 - Q1

    # Define outliers as values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Count the outliers
    outliers = df[(df[column_name] < lower_bound) | (df[column_name] > upper_bound)]
    outlier_count = outliers.shape[0]

    return outlier_count