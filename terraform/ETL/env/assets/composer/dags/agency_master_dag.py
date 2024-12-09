#deploying the master dag to composer airflow 
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.operators.gcs import GCSFileTransformOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime

with DAG(
    "etl_pipeline",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    start = DummyOperator(task_id="start")

    extract = GCSFileTransformOperator(
        task_id="extract_data",
        source_bucket="source_bucket",
        source_object="data.csv",
        destination_bucket="staging_bucket",
        transform_script="/path/to/extract_script.py",
    )

    transform = BigQueryInsertJobOperator(
        task_id="transform_data",
        configuration={
            "query": {
                "query": "SELECT * FROM `staging_table` WHERE condition = true",
                "destinationTable": {"projectId": "project", "datasetId": "dataset", "tableId": "transformed_table"},
                "writeDisposition": "WRITE_TRUNCATE",
            }
        },
    )

    load = BigQueryInsertJobOperator(
        task_id="load_data",
        configuration={
            "query": {
                "query": "SELECT * FROM `transformed_table`",
                "destinationTable": {"projectId": "project", "datasetId": "final_dataset", "tableId": "final_table"},
                "writeDisposition": "WRITE_APPEND",
            }
        },
    )

    end = DummyOperator(task_id="end")

    start >> extract >> transform >> load >> end
