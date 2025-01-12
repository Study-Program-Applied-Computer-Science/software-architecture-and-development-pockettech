CREATE DATABASE finance_management;

CREATE USER fin_user WITH PASSWORD 'password';

-- Grant CONNECT to the database
GRANT CONNECT ON DATABASE finance_management TO fin_user;

-- Grant USAGE on the public schema
GRANT USAGE ON SCHEMA public TO fin_user;

-- Grant full privileges (SELECT, INSERT, UPDATE, DELETE, CREATE, DROP) on all current tables
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO fin_user;

-- Grant CREATE and DROP privileges on the public schema itself
GRANT CREATE ON SCHEMA public TO fin_user;