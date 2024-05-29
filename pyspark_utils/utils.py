from typing import Dict, List, Optional

import pandas as pd
import pyspark
import pyspark.sql
import pyspark.sql.functions as F
from pyspark.sql.window import Window


def get_spark_session(app_name: str) -> pyspark.sql.SparkSession:
    """Recover appropriate SparkSession

    Args:
        app_name (str): Name of application

    Returns:
        pyspark.sql.SparkSession: A Spark session with name `app_name`
    """
    session = (
        pyspark.sql.SparkSession.builder.appName(app_name)
        .enableHiveSupport()
        .config("spark.sql.autoBroadcastJoinThreshold", -1)
        .getOrCreate()
    )
    return session


def assert_cols_in_df(
    df: pyspark.sql.DataFrame, *columns: List[str], df_name: Optional[str] = ""
) -> None:
    """Assserts that all specified columns are present in specified dataframe.
    If not, displays an informative message.

    Args:
        df (pyspark.sql.DataFrame): pyspark dataframe
        df_name (Optional[str], optional): list of column names. Defaults to "".
    """
    assert set(columns).issubset(
        df.columns
    ), f"Columns {' & '.join(set(columns[0]) - set(df.columns))} missing from dataframe {df_name}"


def assert_df_close(df1: pyspark.sql.DataFrame, df2: pyspark.sql.DataFrame, **kwargs) -> None:
    """Asserts that two dataframes are (almost) equal, even if the order of the columns is different.

    Args:
        df1 (pyspark.sql.DataFrame): _description_
        df2 (pyspark.sql.DataFrame): _description_
        kwargs (Optional[dict]): Any attribute of methods `pandas.testing.assert_frame_equal`
    """
    df1_pd: pd.DataFrame = df1.toPandas()
    df2_pd: pd.DataFrame = df2.toPandas()
    cols1 = sorted(df1_pd.columns)
    cols2 = sorted(df2_pd.columns)

    pd.testing.assert_frame_equal(
        df1_pd[cols1].sort_values(by=cols1).reset_index(drop=True),
        df2_pd[cols2].sort_values(by=cols2).reset_index(drop=True),
        **kwargs,
    )


def with_columns(
    df: pyspark.sql.DataFrame, col_func_mapping: Dict[str, pyspark.sql.Column]
) -> pyspark.sql.DataFrame:
    """Use multiple 'withColumn' calls on a dataframe in a single command.
    This function is tail recursive.

    Args:
        df (pyspark.sql.DataFrame): pyspark dataframe
        col_func_mapping (Dict[str, pyspark.sql.Column]): dict to map each column name with the function to apply to it

    Returns:
        pyspark.sql.DataFrame: A pyspark dataframe identical to `df` but with additional columns.
    """
    for col_name, col_func in col_func_mapping.items():
        df = df.withColumn(col_name, col_func)
    return df


def keep_first_rows(df: pyspark.sql.DataFrame, partition_cols, order_cols):
    """Keep the first row of each group defined by `partition_cols` and `order_cols`.

    Args:
        df (pyspark.sql.DataFrame): pyspark dataframe
        partition_cols (_type_): _description_
        order_cols (_type_): _description_

    Returns:
        _type_: _description_
    """
    return (
        df.withColumn(
            "rank",
            F.rank().over(
                Window.partitionBy(*partition_cols).orderBy(*order_cols + [F.rand(seed=1)])
            ),
            # We add a random column in case there are ties (ties are broken arbitrarily)
        )
        .filter(F.col("rank") == 1)
        .drop("rank")
    )
