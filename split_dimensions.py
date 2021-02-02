import pandas as pd

def split_dimension(fact: pd.DataFrame, id_name: str,
                    columns: list) -> pd.DataFrame:
    """
    Breaks off a dimension from the fact table
    """

    dimension = fact[columns].copy()
    dimension = dimension.drop_duplicates()
    dimension = dimension.reset_index(drop=True)
    dimension[id_name] = dimension.index

    return dimension

def split_fact(fact_table: pd.DataFrame,
               dimensions: dict,
               reduce_size: bool = True,
               sample_size: int = 1000,
               reduced_cols: list = None) -> list:
    """
    Splits fact table into a proper star schema.
    Returns a fact table with 1000 samples by default.
    """

    if reduce_size:
        fact_table = fact_table.sample(sample_size,
                                       replace=False,
                                       random_state=42)
    
    dataframes = []

    for id, cols in dimensions.items():
        dimension = split_dimension(fact_table, id, cols)
        dataframes.append(dimension)

        # merge id into dimension
        fact_table = fact_table.merge(dimension, on=cols, how="inner")
    
    if reduced_cols is not None:
        fact_table = fact_table[reduced_cols]

    dataframes.append(fact_table)

    return dataframes