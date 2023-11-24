#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset


function createDatabase {
echo "Creating database ${POSTGRES_DB}"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
CREATE DATABASE ${POSTGRES_DB};
GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};
ALTER ROLE ${POSTGRES_USER} WITH PASSWORD ${POSTGRES_PASSWORD};
EOSQL
}

if [ "$( psql -XtAc "SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB'" -U "$POSTGRES_USER" )" = '1' ]
then
    echo "Database already exists"
else
    createDatabase
fi
