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

    - `pandas.DataFrame`: The cleaned and preprocessed data, including any newly generated feature columns.
    
    **Output**
    
    - presence of repetitions in the primary key
    
    **Example Usage:**

    ```
    import pandas as pd
    import numpy as np

    # Load the raw data
    raw_data = pd.read_csv("path/to/your/data.csv")

    # Preprocess the data
    cleaned_data = cleanUp(raw_data)

    # Perform analysis on the cleaned data
    """
    
    
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
        
    
    #-----------identify the numerical columns -----------
    numerical_columns = df.select_dtypes(include=np.number).columns
    try:
        numerical_columns.remove(PrimarKey)
        print("primary_key is numerical")

    except:
        print("primary_key is not numerical")
    

    #-----------identify th non numerical columns--------------
    non_numerical_columns = df.select_dtypes(include=['object']).columns.tolist()
    try:
        non_numerical_columns.remove(PrimarKey)
        print("primary_key is non numerical")
    except:
        print("primary_key is not non numerical")
    
    
    # in customer_region the missing values are better in nan so they do not show on the graphs
    df.loc[df['customer_region'] == '-', 'customer_region'] = np.nan
    
    # last_promo, on the other hand, is not very informative as it only tells us if someone never used a promo
    # in fact if someone had used multiple promos we would not know.
    # so the missing values are actually what gives us the information
    df.loc[df['last_promo'] == '-', 'last_promo'] = "No_Promo"
    df['last_promo'].unique()
    
    #payment method is fine
    
    #-------------- building new key features -----------
    new_fetures_list = []
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
    
    return df