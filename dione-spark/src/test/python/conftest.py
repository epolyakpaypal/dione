import pytest
from pyspark.sql import SparkSession
import os
import shutil
import sys
import ntpath

print(sys.path)


def remove_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)


@pytest.fixture(scope="session")
def spark_session():

    remove_folder('metastore_db')
    remove_folder('spark-warehouse')

    dione_jars = [
        "dione-hadoop/target/dione-hadoop-0.5.1-SNAPSHOT.jar",
        "dione-spark/target/dione-spark-0.5.1-SNAPSHOT.jar"
    ]

    spark_jars = [
        "https://repo1.maven.org/maven2/com/databricks/spark-avro_2.11/4.0.0/spark-avro_2.11-4.0.0.jar",
        "https://repo1.maven.org/maven2/org/apache/parquet/parquet-avro/1.8.2/parquet-avro-1.8.2.jar",
        "https://repo1.maven.org/maven2/org/apache/avro/avro/1.8.0/avro-1.8.0.jar",
    ]

    spark = (SparkSession.builder
             .appName("dione_python_test")
             .master("local[1]")
             .enableHiveSupport()
             .config("spark.sql.shuffle.partitions", 3)
             .config("spark.jars", ",".join(dione_jars + spark_jars))
             .config("spark.driver.extraClassPath", ":".join([ntpath.basename(f) for f in (dione_jars + spark_jars)]))
             .config("spark.executor.extraClassPath", ":".join([ntpath.basename(f) for f in (dione_jars + spark_jars)]))
             # .config("spark.driver.extraClassPath", ":".join(dione_jars + spark_jars))
             # .config("spark.executor.extraClassPath", ":".join(dione_jars + spark_jars))
             # .config("spark.driver.userClassPathFirst", "true")
             # .config("spark.executor.userClassPathFirst", "true")
             .getOrCreate()
             )

    return spark