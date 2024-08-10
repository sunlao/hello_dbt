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

## DEMO Script

### Summary

This repo has already been initialized for DBT. This was done manually in the `\src` folder with the command: `dbt init hello`. This creates a dbt project called `hello` and all the file structures in `src/hello`.  In addition the following was manually added / modified.

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

From project root, assert DBT in dbt_runtime container and get DBT setup information:

```SHELL
docker exec -ti dbt_runtime sh -c "cd /src/hello && dbt debug"
```

* `profiles.yml` file [OK found and valid]
* `dbt_project.yml` file [OK found and valid]
* Required dependencies:
  * git [OK found]
* Connection test: OK connection ok
