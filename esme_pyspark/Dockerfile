FROM quay.io/jupyter/pyspark-notebook

USER root

# Install PostgreSQL JDBC driver and psycopg2
RUN wget https://jdbc.postgresql.org/download/postgresql-42.6.0.jar -O /usr/local/spark/jars/postgresql-42.6.0.jar && \
    pip install psycopg2-binary

USER ${NB_UID}
