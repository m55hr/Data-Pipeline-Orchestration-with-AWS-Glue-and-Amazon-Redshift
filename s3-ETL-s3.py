import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import lit
from awsglue.dynamicframe import DynamicFrame
import logging


logger=logging.getLogger('my_logger')
logger.setLevel(logging.INFO)

# Create a handler for CLoudWatch
handler=logging.StreamHandler( )
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.info('My log message')

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Amazon S3
AmazonS3_node1722374941636 = glueContext.create_dynamic_frame.from_catalog(database="glue-redshift-project", table_name="product", transformation_ctx="AmazonS3_node1722374941636")

logger.info('print schema of AmazonS3_node1722374941636 dynamic frame')
AmazonS3_node1722374941636.printSchema()

# Count the number of rows
count = AmazonS3_node1722374941636.count()
# Print and log the count
print("Number of rows in AmazonS3_node1722374941636 DynamicFrame:", count)
logger.info('Count for frame is {}'.format(count))

# Script generated for node Change Schema
ChangeSchema_node1722376217319 = ApplyMapping.apply(frame=AmazonS3_node1722374941636, mappings=[("marketplace", "string", "new_marketplace", "string"), ("customer_id", "long", "new_customer_id", "long"), ("product_id", "string", "new_product_id", "string"), ("seller_id", "string", "new_seller_id", "string"), ("sell_date", "string", "new_sell_date", "string"), ("quantity", "long", "new_quantity", "long"), ("year", "string", "new_year", "string")], transformation_ctx="ChangeSchema_node1722376217319")

#convert those string values to long values using the resolveChoice transform method with a cast:long option:
#This replaces the string values with null values
ResolveChoice_node = ChangeSchema_node1722376217319.resolveChoice(specs = [('new_seller_id','cast:long')],
transformation_ctx="ResolveChoice_node")
logger.info('print schema of ResolveChoice_node')
ResolveChoice_node.printSchema()

# Convert the DynamicFrame to a Spark DataFrame
logger.info('Converting DynamicFrame ResolveChoice_node into Spark DataFrame')
spark_data_frame = ResolveChoice_node.toDF()

# Log the start of the filtering process
logger.info('Filtering rows where new_seller_id is not null')
# Apply the filter on the Spark DataFrame
spark_data_frame_filter = spark_data_frame.where("new_seller_id is NOT NULL")

# Add the new column to the data frame
logger.info('create new column status with Active value')
spark_data_frame_filter = spark_data_frame_filter.withColumn("new_status", lit("Active"))
spark_data_frame_filter.show()

logger.info('convert spark dataframe into table view product_view. so that we can run sql ')
spark_data_frame_filter.createOrReplaceTempView("product_view")

logger.info('create dataframe by spark sql ')
product_sql_df = spark.sql("SELECT new_year,count(new_customer_id) as cnt,sum(new_quantity) as qty FROM product_view group by new_year ")

logger.info('display records after aggregate result')
product_sql_df.show()

# Convert the data frame back to a dynamic frame
logger.info('convert spark dataframe to glue dynamic frame ')
dynamic_frame = DynamicFrame.fromDF(product_sql_df, glueContext, "dynamic_frame")

logger.info('dynamic frame uploaded in bucket glue-redshift-project/output/ in parquet format ')

# Script generated for node Amazon S3
AmazonS3_node1722376237225 = glueContext.write_dynamic_frame.from_options(frame=dynamic_frame, connection_type="s3", format="glueparquet", connection_options={"path": "s3://glue-redshift-project/output/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="AmazonS3_node1722376237225")

logger.info('etl job processed successfully')
job.commit()
