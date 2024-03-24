import pandas as pd
from dataclasses import dataclass
from typing import Optional

@dataclass
class ColumnStats:
    mean: float
    std: float
    count: int

def calculate_column_stats_for_anomily_detection(df: pd.DataFrame, column_name: str, group_by_column: Optional[str] = None) -> ColumnStats:
    """
    Calculates statistics (average, standard deviation, and row count) for a specified column in a Pandas DataFrame,
    optionally grouped by another column. The grouped values are first summed up.

    Args:
        df (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column for which to compute the statistics.
        group_by_column (str, optional): The name of the column to group by (default is None).

    Returns:
        ColumnStats: A data class containing statistics for the specified column(s).
    """
    # Ensure the column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")

    if group_by_column:
        # Group the DataFrame by the specified column and sum the values
        grouped_df = df.groupby(group_by_column)[column_name].sum()
    else:
        # Use the original column if no grouping is specified
        grouped_df = df[column_name]

    # Calculate statistics for the grouped values
    return ColumnStats(mean=grouped_df.mean(), std=grouped_df.std(), count=grouped_df.count())

# Example usage:
if __name__ == "__main__":
    data = {'A': [10, 20, 30], 'B': [30, 40, 50], 'C': [50, 60, 70], 'ZZ': [2, 6, 6]}
    df = pd.DataFrame(data)
    column_to_analyze = 'B'
    group_by_column = 'ZZ'
    stats_result = calculate_column_stats_for_anomily_detection(df, column_to_analyze, group_by_column)
    print(f"Statistics for column '{column_to_analyze}':")
    print(stats_result)