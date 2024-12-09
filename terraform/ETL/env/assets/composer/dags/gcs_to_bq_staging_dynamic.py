from airflow import DAG
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GoogleCloudStorageToBigQueryOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
with DAG(
    'gcs_to_bigquery_staging_dynamic',
    default_args=default_args,
    description='Load data from GCS ingestion bucket to BigQuery staging layer',
    schedule_interval='@hourly',  # Adjust as needed
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # Dummy task to start the pipeline
    start_task = DummyOperator(
        task_id='start_pipeline'
    )

    # Sensor to check for new files in the ingestion bucket
    detect_new_file = GCSObjectExistenceSensor(
        task_id='detect_new_file',
        bucket='your-ingestion-bucket',  # Replace with your GCS bucket name
        object='data/*.csv',  # Wildcard to match data files (e.g., CSV files)
        timeout=600,  # Time to wait for new files (10 minutes)
        poke_interval=30,  # Check every 30 seconds
        mode='poke',
    )

    # Task to load data into BigQuery staging layer
    load_to_bigquery = GoogleCloudStorageToBigQueryOperator(
        task_id='load_to_bigquery',
        bucket='your-ingestion-bucket',  # Replace with your GCS bucket name
        source_objects=['data/*.csv'],  # Match uploaded files
        destination_project_dataset_table='your-project.your_dataset.staging_table',  # Replace with your BigQuery table
        schema_fields=[
            {"name": "column1", "type": "STRING", "mode": "NULLABLE"},
            {"name": "column2", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "column3", "type": "TIMESTAMP", "mode": "NULLABLE"},
        ],
        source_format='CSV',
        skip_leading_rows=1,
        write_disposition='WRITE_APPEND',  # Appends data to the staging table
        create_disposition='CREATE_IF_NEEDED',  # Creates the table if it doesn't exist
    )

    # Dummy task to end the pipeline
    end_task = DummyOperator(
        task_id='end_pipeline'
    )

    # Define task dependencies
    start_task >> detect_new_file >> load_to_bigquery >> end_task
