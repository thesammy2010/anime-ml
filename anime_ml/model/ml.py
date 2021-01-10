# type: ignore[import]

from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import SparkSession

from anime_ml.api.dump import DATA_FILEPATH, FEATURES_FILENAME


def ml() -> None:

    spark = SparkSession.builder.appName("anime-ml").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    data = spark.read.json(f"{DATA_FILEPATH}/{FEATURES_FILENAME}")
    # data = spark.read.json("anime_ml/data/2021-01-10-features.json")

    # data.head()
    # data.describe().show()
    data.printSchema()
