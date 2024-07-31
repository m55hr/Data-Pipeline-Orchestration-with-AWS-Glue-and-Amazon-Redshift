Project: Data Pipeline Orchestration with AWS Glue and Amazon Redshift
Objective: Develop a robust data pipeline for efficient data processing and analytics.
Workflow Overview:
Data Ingestion: Files were periodically uploaded and partitioned into an S3 bucket.
Data Cataloging: AWS Glue crawlers were employed to update the Data Catalog, maintaining accurate schema definitions.
ETL Process:
Transformation and Cleansing: Performed using Glue Studio with PySpark and Glue DataFrames.
Data Storage: Transformed data was stored as Parquet files in S3.
Data Warehousing:
Table Creation: New tables were created in Amazon Redshift to store the processed Parquet files.
Data Loading: The refined data was loaded into Redshift for efficient querying and analytics.
Security and Connectivity: Utilized VPC gateway endpoints for secure data transfer between S3 and Redshift.
Final ETL Job: The AWS Glue Data Catalog was leveraged to streamline the final ETL job, integrating the data into Redshift.
This pipeline enabled streamlined data management and analytics, ensuring secure and efficient data flow.
![overview](https://github.com/user-attachments/assets/b48bdd19-2b17-4e8b-a024-688d7e0402f6)
![glue workflow](https://github.com/user-attachments/assets/cdaa9278-3722-42f1-919d-50f58f4794e1)

