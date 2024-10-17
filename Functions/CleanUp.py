import pandas as pd
import numpy as np

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
    

    #-----------identify the non numerical columns--------------
    print("-----------identify the non numerical columns -----------")

    non_numerical_columns = df.select_dtypes(include=['object']).columns.tolist()
    try:
        non_numerical_columns.remove(PrimarKey)
        print("primary_key is non numerical")
    except:
        print("primary_key is not non numerical")
    
    
    # in customer_region the missing values are better in nan so they do not show on the graphs
    df.loc[df['customer_region'] == '-', 'customer_region'] = np.nan
    
    #payment method is fine
    
    #-------------- building new key features -----------
    new_fetures_list = []
    # last_promo, on the other hand, is not very informative as it only tells us if someone never used a promo
    # in fact if someone had used multiple promos we would not know.
    # so the missing values are actually what gives us the information
    df.loc[df['last_promo'] == '-', 'last_promo'] = "No_Promo"
    df['used_promo']= df['last_promo'] != 'No_Promo'
    new_fetures_list.append("used_promo")    
    
    DOW_col_sum = df[DOW_col].sum(axis=1)
    new_fetures_list.append("DOW_col_sum")
    
    df['Product_by_Order'] = df['product_count'] /df['Total_Orders']
    new_fetures_list.append("Product_by_Order")

    df['delta_day_order'] = df['last_order'] - df['first_order'] + 1
    new_fetures_list.append('delta_day_order')
    
    
    cui_columns = [col for col in df.columns if col.startswith('CUI')]
    df['tot_value_cui'] = df[cui_columns].sum(axis=1)
    new_fetures_list.append('tot_value_cui')
    
    df['order_freq'] = df['product_count'] / df['delta_day_order']
    df['value_freq'] = df['tot_value_cui'] / df['delta_day_order']
    df['avg_order_value'] = df['tot_value_cui'] / df['product_count']

    new_fetures_list.append('order_freq')
    new_fetures_list.append('value_freq')
    new_fetures_list.append('avg_order_value')
    
    df['avg_order_value'] = np.where(df['product_count'] != 0, df['tot_value_cui'] / df['product_count'], 0)
    new_fetures_list.append('avg_order_value')

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