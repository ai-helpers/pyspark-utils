from pkg_resources import DistributionNotFound, get_distribution
from .utils import get_spark_session, assert_cols_in_df, assert_df_close, with_columns  # noqa: F401

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "pyspark-utils"
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound
