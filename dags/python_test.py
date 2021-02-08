from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago


from datetime import datetime
default_args = {
    'owner': 'airflow',
}
dag_name = 'Create_Basic_Dag'
def test_function():
    string = "this is a test function of the python operator"
    print(string)
    return string



dag = DAG(
    dag_name,
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(2)
)


with dag:
    t1 = PythonOperator(
        task_id = dag.dag_id + '_test_function',
        python_callable=test_function,
        dag = dag


    )

    t2 = DummyOperator(
        task_id = dag.dag_id + '_dummyoperator',
        dag=dag
    )

    t3 = DummyOperator(
        task_id = dag.dag_id + '_dummyoperator2',
        dag= dag
    )


t1 >> [t2,t3]