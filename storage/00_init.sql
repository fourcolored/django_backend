CREATE USER replica WITH REPLICATION ENCRYPTED PASSWORD 'replica-db';
SELECT pg_create_physical_replication_slot('replication_slot');

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO replica;