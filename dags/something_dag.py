from datetime import timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from plugins.operators.something import HelloOperator


default_args = {
    "owner": "airflow",
    "start_date": "2020-05-13",
    "depends_on_past": False,
    "email": ["johndoe@abc.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(dag_id="something_dag", default_args=default_args, schedule_interval="@daily") as dag:
    main_task = DummyOperator(task_id="main_task")
    dummy_task2 = DummyOperator(task_id="dummy_task")
    hello_world = HelloOperator(task_id='hello-world', name='Aaron')
    main_task >> dummy_task2 >> hello_world
