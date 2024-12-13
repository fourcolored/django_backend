CREATE USER replica WITH REPLICATION ENCRYPTED PASSWORD 'replica-db';
SELECT pg_create_physical_replication_slot('replication_slot');