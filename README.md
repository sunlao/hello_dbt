# Hello DBT

## Overview

This is a reference implementation of using DBT [(documentation)](https://docs.getdbt.com/) demonstrating how to:

* Enrich data for consumption with best practice opinions
  * only write select statements
    * no DDL needed
    * No insert / update / merge / delete needed
* Testing sql enrichment as a first class object
  * Schema tests
  * business logic tests
* Simplified process to:
  * seed data
  * slowly changing dimensions

## Prerequisites

Review the async-service [wiki](https://github.com/sunlao/async-service/wiki) Mac Pre-Req and Virtual Environments:

* Virtual Environment
* containers
* postgres

Locally this repo uses the following environment variables in a `.env`

* APP_CODE=hdbt
* ENV=test
* DB_NAME=db_${APP_CODE}
* DB_ADMIN_USER=${APP_CODE}_admin
* DB_HOST_PORT=5431
* DB_CONTAINER_PORT=5432
* DB_CONTAINER_HOST=${APP_CODE}-postgres
* DB_ADMIN_PWD={manually create a unique secret}
* DB_DATA_PWD={manually create a unique secret}
* DB_APP_PWD={manually create a unique secret}

Note: we do not store passwords in repos so `.env` files are in the `.gitignore` file

## Configuration files

* `.gitignore` - a fine start to common things that should be ignored in a python repo
* build.py - pythonic orchestration of the build via the make file
* destroy.py - pythonic orchestration of the destroy via the make file
* `docker-compose.yml` - containerized orchestration for MySQL & Postgres
* `Makefile` - Build / destroy executor
* `requirements.txt` - used to list python modules required for a repo
* `tox.ini` - config file for Tox
* `VERSION` - place to store the semantic version of the repo

## DEMO Script

### Summary

This repo has already been initialized for DBT. This was done manually in the `\src` folder with the command: `dbt init hello`. This creates a dbt project called `hello` and all the file structures in `src/hello`. `dbt parse` was also ran by the container entry point (see above documentation for more info). In addition the following was manually added / modified.

* `deploy/dbt-runtime/profiles.yml` is copied to to the containers users' `.dbt` folder to provide dbt connection to postgres.
* `src/hello/dbt_project.yml` has been modified post init, with minimalist opinions for SSP and the demo.
* Seed data added for DBT demo data can be found in `src/hello/data`
* yaml file for seed schema tests in `src/hello/models/working`
* yaml file for model schema tests in `src/hello/models/consumption`
* two simple select statements in `src/hello/tests/consumption` for data tests

This demo will do the following:

* Load seed data
* Enrich seed data to a new consumption object
* Assert tests of seed data
* Test new objects

With this we can see the execution framework for DBT models and tests demonstrating the ease of:

* Model and test execution framework
* Management of model dependencies
* dynamic DDL and SQL for enriching data
* Creation of thirty-two schema and data tests from two YAML files and two simple select statements

***Note: There are a lot of terms in the Data Warehouse space that DBT uses that are not yet industry standard. DBT is asserting them in a specific consistent way that is slowly becoming the new standard. The website documentation linked above explains this in detail.***

### Create and Validate Environment

From project root execute:

Start a postgres db container, a db-deploy container that will configure postgres, and a dbt runtime container.

```SHELL
make up
```

Test Database with repo helpers.

```SHELL
tox
```

* Assert Postgres database
* Assert Postgres dbt schemas exist
* NOTE: the app user:
  * can connect to postgres - `select "postgres";`
  * does not have permissions select from table in consumption schema. (or any table)

From project root, assert DBT in dbt_runtime container and get DBT setup information:

```SHELL
docker exec -ti dbt_runtime sh -c "cd /src/hello && dbt debug"
```

* `profiles.yml` file [OK found and valid]
* `dbt_project.yml` file [OK found and valid]
* Required dependencies:
  * git [OK found]
* Connection test: OK connection ok

Show no raw tables exist:

Execute in favorite SQL editor with admin account for Postgres:

```SQL
select count(*)
from
raw.raw_customers;

select count(*)
from
raw.raw_customers_delete;

select count(*)
from
raw.raw_customers_new;

select count(*)
from
raw.raw_customers_update;

select count(*)
from
raw.raw_orders;

select count(*)
from
raw.raw_payments;
```

Show seed files in `src/hello/data`

Execute in root folder to load seed objects:

```SHELL
docker exec -ti dbt_runtime sh -c "cd /src/hello && dbt seed"
```

Re-Execute SQL above from "Show no raw tables exist"

Execute in favorite SQL editor with admin account for postgres:

```SQL
select count(*)
from
stage.customers_delete;

select count(*)
from
stage.customers_init;

select count(*)
from
stage.customers_new;

select count(*)
from
stage.customers_update;

select count(*)
from
working.customers;

select count(*)
from
consumption.customer_summary;

select count(*)
from
consumption.order_summary;
```

```SHELL
docker exec -ti dbt_runtime sh -c "cd /src/hello && dbt run"
```

Re-Execute SQL above from "Show tables exist"

* Show schema tests
  * `src/hello/models/working/schema.yml`
  * `src/hello/models/consumption/schema.yml`
* Show data tests
  * `src/hello/tests/consumption`

```SHELL
docker exec -ti dbt_runtime sh -c "cd /src/hello && dbt test"
docker exec -ti dbt_runtime sh -c "cd /src/hello && dbt test --models order_summary"
```

### Incremental Model Scenarios

copy files representing new streams of data

Show types of updates:

```bash
docker cp demo_data/raw_customers_delete.csv dbt_runtime:/src/hello/seeds/raw_customers_delete.csv
docker cp demo_data/raw_customers_new.csv dbt_runtime:/src/hello/seeds/raw_customers_new.csv
docker cp demo_data/raw_customers_update.csv dbt_runtime:/src/hello/seeds/raw_customers_update.csv
```

***Note simultaneous update and delete which could happen***

```bash
docker exec -ti dbt_runtime sh -c "cd /src/hello && dbt seed"
docker exec -ti dbt_runtime sh -c "cd /src/hello && dbt run"
```

Execute in favorite SQL editor with admin account for postgres:

```SQL
select *
from
consumption.customer_summary;
```

You will see the updated data in the consumption table
You will see deleted data in the consumption table

***note audit columns***

### Snapshot

If you want to keep track of the historical data, execute in the root folder:

```bash
docker exec -ti dbt_runtime sh -c "cd /src/hello && dbt seed"
docker exec -ti dbt_runtime sh -c "cd /src/hello && dbt snapshot"
```

Execute in favorite SQL editor with admin account for postgres:

```SQL
select *
from
snapshots.customer_snapshot;
```

You will see in the new schema a snapshot of `raw_customers.csv` with columns - dbt_updated_at, dbt_valid_from and dbt_valid_to.

Change some value in raw_customers.csv, and copy file to docker container with executing following:

```bash
docker cp ./src/hello/seeds/raw_customers.csv dbt_runtime:/src/hello/seeds/raw_customers.csv
docker exec -ti dbt_runtime sh -c "cd /src/hello && dbt seed"
docker exec -ti dbt_runtime sh -c "cd /src/hello && dbt snapshot"
```

Re-execute in favorite SQL editor with admin account for postgres:

```SQL
select *
from
snapshots.customer_snapshot;
```

You will see the updated data in the snapshot table.

### Posthook and Macro

We already added a posthook for model `consumption` in `dbt_project.yml`:

```SHELL
models:
  stage:
  raw:
  working:
  consumption:
    +post-hook: "{{ grant_select_on_schemas(['consumption'], 'hdbt_app') }}"
```

You will now see all consumption data as hdbt_app.

### Documentation

DBT self documenting feature shows a graph of all the data associated elements how the entities relate to each other.

There are lots of ways to use DBT docs. Below you can

* generate docs
* copy necessary files to host machine
* modify index

#### Generate

```bash
docker exec -ti dbt_runtime sh -c "cd /src/hello && dbt docs generate"
```

#### Copy

```bash
for f in $(docker exec -it dbt_runtime sh -c "ls src/hello/target/*.json" | tr -d '\r') ; do docker cp dbt_runtime:${f} ./docs; done
for f in $(docker exec -it dbt_runtime sh -c "ls src/hello/target/*.html" | tr -d '\r') ; do docker cp dbt_runtime:${f} ./docs; done
docker cp dbt_runtime:/src/hello/target/graph.gpickle ./docs/graph.gpickle 
```

#### Index

```bash
python merge_index.py
```

open full path to `.docs/index.html' in browser
