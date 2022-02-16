# airflow
Data pipelines for various projects

# environment setup
add __init__.py to ./plugins and ./plugins/** to create namespaces
mark root directory (.) and ./plugins as "sources root"
In docker-compose.yaml, add the plugins directory to the PYTHONPATH (this part is already done but for reference)
Now, in PyCharm, the interpreter will find the namespaces without error and the Docker container will find the files
in the mounted volume fine.

add the following variables and their values to a .env file:

AIRFLOW__CORE__FERNET_KEY=
AIRFLOW__SMTP__SMTP_MAIL_FROM=
AIRFLOW__SMTP__SMTP_PASSWORD_SECRET=
AIRFLOW__SMTP__SMTP_USER=
AIRFLOW__SMTP__SMTP_HOST=

redcap_token=
redcap_url=

db_server=
db_port=
db_schema=
db_uid=
db_pwd=

BE SURE THAT YOU'RE .env FILE DOES NOT GET TRACKED BY GIT!

Holy cow, what a weird bug. When using Docker as a remote interpreter with a Windows host, the run/debug configuration
of a given script needs to have the path volume mounted (docker run -v flag). However, the config GUI in PyCharm will
convert the generated path from folder selection dialog into a Unix-style format (e.g /c/). A workaround is to manually 
type the host path and ensure the drive letter is lower case.
https://youtrack.jetbrains.com/issue/IDEA-266072

# Docker compose
Extending the Docker compose file provided by Airflow.
Added airflow-connections service to create connections without exposing secrets