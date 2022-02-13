# airflow
Data pipelines for various projects

# environment setup
add __init__.py to ./plugins and ./plugins/** to create namespaces
mark root directory (.) and ./plugins as "sources root"
In docker-compose.yaml, add the plugins directory to the PYTHONPATH (this part is already done but for reference)
Now, in PyCharm, the interpreter will find the namespaces without error and the Docker container will find the files
in the mounted volume fine.