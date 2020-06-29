from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to operate!
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Binh Phan',
    'depends_on_past': False,
    'start_date': days_ago(31),
    'email': ['example@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

#instantiates a directed acyclic graph
dag = DAG(
    'ml_pipeline',
    default_args=default_args,
    description='A simple Machine Learning pipeline',
    schedule_interval=timedelta(days=30),
)

# instantiate tasks using Operators.
#BashOperator defines tasks that execute bash scripts. In this case, we run Python scripts for each task.
download_images = BashOperator(
    task_id='download_images',
    bash_command='python3 /usr/local/airflow/scripts/download_images.py',
    dag=dag,
)
train = BashOperator(
    task_id='train',
    depends_on_past=False,
    bash_command='python3 /usr/local/airflow/scripts/train.py',
    retries=3,
    dag=dag,
)
serve_commands = """
    lsof -i tcp:8008 | awk 'NR!=1 {print $2}' | xargs kill;
    python3 /usr/local/airflow/scripts/serve.py serve
    """
serve = BashOperator(
    task_id='serve',
    depends_on_past=False,
    bash_command=serve_commands,
    retries=3,
    dag=dag,
)

#sets the ordering of the DAG. The >> directs the 2nd task to run after the 1st task. This means that
#download images runs first, then train, then serve.
download_images >> train >> serve
