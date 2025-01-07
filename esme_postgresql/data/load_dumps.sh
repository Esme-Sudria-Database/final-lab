#!/bin/bash
set -e -x

# Set default postgres user if not provided
: "${POSTGRES_USER:=postgres}"

databases=("ecommerce" "hospital")

for database in "${databases[@]}"; do
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
      CREATE DATABASE ${database};
      GRANT ALL PRIVILEGES ON DATABASE ${database} TO postgres;
EOSQL

  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "${database}" < /data/"${database}".sql.dump
done
