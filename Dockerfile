FROM apache/airflow:2.2.3
COPY requirements-docker.txt /opt/airflow/requirements.txt
RUN pip install -r /opt/airflow/requirements.txt