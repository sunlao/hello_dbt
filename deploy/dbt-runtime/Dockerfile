FROM python:3.12-slim-bullseye

RUN mkdir -p /src

RUN apt-get update
RUN apt-get install -y --no-install-recommends libpq-dev python3-dev
RUN apt-get install -y --no-install-recommends gcc
RUN apt-get install -y --no-install-recommends git

RUN pip install --upgrade pip
COPY ./deploy/dbt-runtime/requirements.txt .
RUN pip install -r requirements.txt

COPY ./src /src

# create the app user
RUN addgroup app
RUN useradd -g app app

# copy entrypoint.sh
COPY ./deploy/dbt-runtime/entrypoint.sh /src/entrypoint.sh

# chown all the files to the app user
RUN chown -R app:app /src
RUN chmod 770 /src/entrypoint.sh

COPY ./deploy/dbt-runtime/profiles.yml home/app/.dbt/profiles.yml

ARG DBT_PWD
ENV DBT_PWD $DBT_PWD
RUN echo $

RUN sed -i 's/DBT_SECRET/'"$DBT_PWD"'/' home/app/.dbt/profiles.yml

RUN cd /src/hello && dbt deps
RUN chown -R app:app home/app/
RUN chown -R app:app /src

# change to the app user
USER app

# run entrypoint.sh
ENTRYPOINT ["/src/entrypoint.sh"]
