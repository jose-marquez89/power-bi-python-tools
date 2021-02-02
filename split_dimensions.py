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
               sample_size: int = 1000) -> list:
    """Splits musco fact table into a proper star schema"""

    if reduce_size:
        fact_table = fact_table.sample(sample_size,
                                       replace=False,
                                       random_state=42)