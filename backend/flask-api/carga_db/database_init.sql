CREATE DATABASE sanjus;

CREATE ROLE sanjus_app WITH
    LOGIN
    NOSUPERUSER
    CREATEDB
    CREATEROLE
    INHERIT
    NOREPLICATION
    CONNECTION LIMIT -1
    PASSWORD 'inovacnj';

CREATE SCHEMA sanjus
    AUTHORIZATION sanjus_app;

ALTER ROLE sanjus_app IN DATABASE sanjus
    SET search_path TO sanjus, public, "$user";