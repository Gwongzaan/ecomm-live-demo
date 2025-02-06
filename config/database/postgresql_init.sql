DO
$do$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname='live_demo') THEN

        CREATE USER live_demo WITH PASSWORD 'live_demo_pass_12345';
        CREATE TABLESPACE live_demo OWNER live_demo location '/var/lib/postgresql/data';
        CREATE DATABASE live_demo OWNER live_demo TABLESPACE live_demo;

        ALTER ROLE live_demo SET client_encoding TO 'utf8';
        ALTER ROLE live_demo SET default_transaction_isolation TO 'read committed';
        ALTER ROLE live_demo SET timezone TO 'UTC';
        GRANT ALL PRIVILEGES ON DATABASE live_demo TO live_demo;

    END IF;
END
$do$