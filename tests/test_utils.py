import pyspark
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
import pytest

from pyspark_utils.utils import (
    assert_df_close,
    keep_first_rows,
    with_columns,
)


spark_conf = {
    "master": "local",
    "spark.driver.maxResultSize": "3g",
    "spark.scheduler.mode": "FAIR",
    "spark.sql.session.timeZone": "UTC",
}


@pytest.fixture(scope="session")
def spark():
    conf = pyspark.SparkConf().setAll(list(spark_conf.items()))
    return SparkSession.builder.master("local").appName("test_io").config(conf=conf).getOrCreate()


@pytest.fixture(scope="session")
def spark_df(spark):
    return spark.createDataFrame(
        [
            [None, "a", 1, 1.0],
            ["b", "b", 1, 2.0],
            ["b", "b", None, 3.0],
            ["c", "c", None, 2.0],
            ["c", "c", 3, 4.0],
            ["d", None, 4, 2.0],
            ["d", None, 5, 6.0],
        ],
        ["col0", "col1", "col2", "col3"],
    )


def test_with_columns(spark_df):
    col4 = F.col("col3") + 2
    col5 = F.lit(True)

    transformed_df = with_columns(spark_df, col_func_mapping={"col4": col4, "col5": col5})
    expected_df = spark_df.withColumn("col4", col4).withColumn("col5", col5)

    assert_df_close(transformed_df, expected_df)


def test_keep_first_row(spark_df):
    transformed_df = keep_first_rows(spark_df, [F.col("col0")], [F.col("col3")])
    expected_df = spark_df.where(F.col("col3") <= 2)

    assert_df_close(transformed_df, expected_df)
