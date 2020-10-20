
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    
    CREATE DATABASE sanjus;
    
    CREATE USER sanjus_app WITH PASSWORD 'inovacnj';
    CREATE SCHEMA sanjus AUTHORIZATION sanjus_app;
    ALTER ROLE sanjus_app IN DATABASE sanjus SET search_path TO sanjus, public, '$user';
EOSQL

