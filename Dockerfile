FROM apache/airflow:2.2.3
RUN pip install --no-cache-dir apache-airflow-providers-microsoft-mssql==2.0.1 \
                                python-dotenv
# todo: copy requirements.txt??