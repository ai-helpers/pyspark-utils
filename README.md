# AI Helpers - PySpark utils

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ai-helpers_pyspark-utils&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ai-helpers_pyspark-utils)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=ai-helpers_pyspark-utils&metric=bugs)](https://sonarcloud.io/summary/new_code?id=ai-helpers_pyspark-utils)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=ai-helpers_pyspark-utils&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=ai-helpers_pyspark-utils)

`pyspark-utils` is a Python module that provides a collection of utilities to simplify and enhance the use of PySpark. These utilities are designed to make working with PySpark more efficient and to reduce boilerplate code.

## Table of Contents

- [AI Helpers - PySpark utils](#ai-helpers---pyspark-utils)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Getting Started](#getting-started)
  - [Utilities \& Examples](#utilities--examples)
  - [Contributing](#contributing)

## Installation

You can install the `pyspark-utils` module via pip:

```bash
pip install ai-helpers-pyspark-utils
```

## Getting Started

First, import the module in your Python script:

```python
import pyspark_utils as psu
```

Now you can use the utilities provided by `pyspark-utils`.

## Utilities & Examples

- `get_spark_session`: Recover appropriate SparkSession.
  
  Create a spark dataframe: 
  
  ```python
  >>> import pyspark_utils as psu

  >>> spark = psu.get_spark_session("example")
  >>> sdf = spark.createDataFrame(
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
  >>> sdf.show()
  +----+----+----+----+
  |col0|col1|col2|col3|
  +----+----+----+----+
  |NULL|   a|   1| 1.0|
  |   b|   b|   1| 2.0|
  |   b|   b|NULL| 3.0|
  |   c|   c|NULL| 2.0|
  |   c|   c|   3| 4.0|
  |   d|NULL|   4| 2.0|
  |   d|NULL|   5| 6.0|
  +----+----+----+----+ 
  ```

- `with_columns`: Use multiple 'withColumn' calls on a dataframe in a single command.

  ```python
  >>> import pyspark_utils as psu
  >>> import pyspark.sql.functions as F

  >>> col4 = F.col("col3") + 2
  >>> col5 = F.lit(True)

  >>> transformed_sdf = psu.with_columns(
    sdf, 
    col_func_mapping={"col4": col4, "col5": col5}
    )
  >>> transformed_sdf.show()
  +----+----+----+----+----+----+
  |col0|col1|col2|col3|col4|col5|
  +----+----+----+----+----+----+
  |NULL|   a|   1| 1.0| 3.0|true|
  |   b|   b|   1| 2.0| 4.0|true|
  |   b|   b|NULL| 3.0| 5.0|true|
  |   c|   c|NULL| 2.0| 4.0|true|
  |   c|   c|   3| 4.0| 6.0|true|
  |   d|NULL|   4| 2.0| 4.0|true|
  |   d|NULL|   5| 6.0| 8.0|true|
  +----+----+----+----+----+----+
  ```

- `keep_first_rows`: Keep the first row of each group defined by `partition_cols` and `order_cols`.

  ```python
  >>> transformed_sdf = psu.utils.keep_first_rows(sdf, [F.col("col0")], [F.col("col3")])
  >>> transformed_sdf.show()
  +----+----+----+----+
  |col0|col1|col2|col3|
  +----+----+----+----+
  |NULL|   a|   1| 1.0|
  |   b|   b|   1| 2.0|
  |   c|   c|NULL| 2.0|
  |   d|NULL|   4| 2.0|
  +----+----+----+----+
  ```

- `assert_cols_in_df`: Assserts that all specified columns are present in specified dataframe.

- `assert_df_close`: Asserts that two dataframes are (almost) equal, even if the order of the columns is different.

## Contributing

We welcome contributions to `pyspark-utils`. To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

Please ensure your code follows the project's coding standards and includes appropriate tests.
