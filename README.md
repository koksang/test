<a name="readme-top"></a>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>


<!-- GETTING STARTED -->
## Getting Started

![insights_report](insights_report.png)

Currently, the setup can only be done in a single machine. Everything is in containers, runs on docker-compose, so you will need docker installed.

### Prerequisites

You will need a Google Cloud Platform account in order to setup BigQuery and the credentials in order for it to work
* [Google Cloud Platform][gcp-url]
* [Application Authentication][appauth-url]

You will need python libraries and dependency manager such as *pip*. I use *poetry*
* [Poetry][poetry-url]

    ```console
    $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
    ```

### Installation
1. Clone the repo

    ```console
    $ git clone https://github.com/koksang/test.git
    ```

2. To install dependencies locally especially **DBT**, you can do
    * Poetry

        ```console
        $ poetry install
        ```
    Or if you use *pip*
    * Pip
        ```console
        $ poetry export -f requirements.txt --without-hashes
        $ pip install -r requirements.txt

        ---> 100%
        ```

3. Start `docker-compose.yaml` by doing as below. It will start in detached mode

    ```console
    $ docker-compose -f infra/docker-compose.yaml up -d
    ```

4. Set environment variables
    * Google Cloud specific

        ```console
        $ export AIRFLOW_HOME=${YOUR PATH TO AIRFLOW_HOME}
        $ export DBT_PROJECT_DIR=${YOUR DBT_PROJECT_DIR}
        $ export DBT_PROFILES_DIR=${YOUR DBT_PROFILES_DIR}
        $ export PROJECT_ID=${YOUR GCP PROJECT_ID}
        $ export BUCKET=${YOUR GCS BUCKET}
        ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

1. Start a local airflow cluster
    * Create airflow database

        ```console
        $ airflow db init
        $ airflow users create -u admin -r Admin --password admin -e admin -f admin -l admin
        ```

    * Start airflow webserver

        ```console
        $ airflow webserver
        ```
    
    * Start airflow scheduler

        ```console
        $ airflow scheduler
        ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- setup -->
[gcp-url]: https://cloud.google.com
[appauth-url]: https://cloud.google.com/docs/authentication/getting-started#setting_the_environment_variable
[poetry-url]: https://python-poetry.org/docs/#installation

<!-- results -->
[dashboard-url]: insights_report.png