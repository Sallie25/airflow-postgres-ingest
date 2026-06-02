"""
Airflow DAG for orchestrating NYC taxi data ingestion into PostgreSQL.

This DAG demonstrates how to:
- Schedule data ingestion pipelines
- Execute Docker containers as Airflow tasks
- Pass parameters to ingestion scripts
- Monitor and manage data workflows
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

# Default arguments for all tasks in the DAG
default_args = {
    'owner': 'data-engineer',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1),
    'email': ['admin@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
with DAG(
    dag_id='taxi_ingestion_pipeline',
    default_args=default_args,
    description='Orchestrate NYC taxi data ingestion into PostgreSQL',
    schedule_interval='@monthly',  # Run on the first day of each month
    catchup=False,  # Don't backfill historical runs
    tags=['data-ingestion', 'taxi', 'postgres'],
) as dag:

    # Task: Ingest yellow taxi trip data
    ingest_yellow_taxi = DockerOperator(
        task_id='ingest_yellow_taxi_data',
        image='taxi-ingest:latest',
        command=[
            '--pg_user=root',
            '--pg_pass=root',
            '--pg_host=pgdatabase',
            '--pg_port=5432',
            '--pg_db=ny_taxi',
            '--target_table=yellow_taxi_data',
            '--zone_table=taxi_zone_lookup',
            '--year={{ execution_date.year }}',
            '--month={{ execution_date.month }}',
            '--chunksize=100000',
        ],
        docker_url='unix://var/run/docker.sock',
        network_mode='airflow-postgres-ingest_default',
        auto_remove=True,
    )

    # Set task dependencies (currently just one task, but structure allows for more)
    ingest_yellow_taxi


if __name__ == '__main__':
    dag.cli()
