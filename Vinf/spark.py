
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_extract



spark = SparkSession.builder.appName("dakoty").getOrCreate()
xml_file_path = "C:\\Users\\Ivo\Desktop\\VINF\\data\\enwiki-latest-pages-articles19.xml-p27121851p28621850"

df = spark.read.format('com.databricks.spark.xml').option('rowTag', 'page').load(sys.argv[1])

reduced_df = df.select(col("title").alias("Name"), col("revision.text._VALUE").alias("wiki text"))

location_pattern = r'\|\s*location\s*=\s*(\d*\[\[([^\[\]]+)\]\])'
tenants_pattern = r'\| tenants = \[\[([^\[\]]+)\]\]'
capacity_pattern = r'capacity = (\d{1,3}(?:,\d{3})*)'

stadiums = reduced_df.filter(col("wiki text").ilike("%\n| tenants =%") & col("wiki text").ilike("%football stadium%") & col("wiki text").ilike("%England%"))

result = (
    stadiums
    .withColumn("tenant", regexp_extract(col("wiki text"), tenants_pattern, 1))
    .withColumn("location", regexp_extract(col("wiki text"), location_pattern, 1))
    .withColumn("capacity", regexp_extract(col("wiki text"), capacity_pattern, 1))
)


result.select("Name", "tenant", "location", "capacity", "wiki text").show()
result.select("Name", "tenant", "location", "capacity").write.csv(sys.argv[2], header=True)

spark.stop()
