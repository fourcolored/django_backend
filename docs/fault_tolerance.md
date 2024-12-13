# Fault Tolerance and Resilience
Fault tolerance is system's ability to handle faults and Resilence is system's ability to recover from failures.
Failures in the System can occure because of the system component exchaustion, downtime, network issues.


Redudancy in critical components prevents single point of failures. By having redudant components, we can mitigate the impact of failures and ensure that the system continues to function even if one or more components fail.

## Database Replication
By creating replication of our database, we can acheive redudancy. We create multiple copy of the database, and keep them in sync with primary database. This ensures that if one of the databases fails, another one takes its place.

2 databases - primary and replica
```
services:
  primary-db:
    image: postgres
    volumes:
      - primary-data:/var/lib/postgesql/data
      - ./storage/00_init.sql:/docker-entrypoint-initdb.d/00_init.sql
    environment:
      POSTGRES_DB: ecommerce
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: primary
      POSTGRES_HOST_AUTH_METHOD: "scram-sha-256\nhost replication all 0.0.0.0/0 md5"
      POSTGRES_INITDB_ARGS: "--auth-host=scram-sha-256"
    command: |
      postgres 
      -c wal_level=replica 
      -c hot_standby=on 
      -c max_wal_senders=10 
      -c max_replication_slots=10 
      -c hot_standby_feedback=on
    ports:
      - "5438:5432"
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "postgres"]
      interval: 30s
      retries: 3
  
  replica-db:
    image: postgres
    volumes:
      - replica-data:/var/lib/postgesql/data
      - ./storage/replica_db/config/postgresql.conf:/config/postgresql.conf
    environment:
      PGUSER: replica
      PGPASSWORD: replica-db
    ports:
      - "5439:5432"
    command: |
      bash -c "
      rm -rf /var/lib/postgresql/data/*
      until pg_basebackup --pgdata=/var/lib/postgresql/data -R --slot=replication_slot --host=primary-db --port=5432 -U replica
      do
        echo 'Waiting for primary to connect...'
        sleep 1s
      done
      echo 'Backup done, starting replica...'
      chmod 0700 /var/lib/postgresql/data
      exec docker-entrypoint.sh postgres -c config_file=/config/postgresql.conf
      "
    depends_on:
      - primary-db
```

## Load balancer
Also we can achieve redudancy by creating several servers. If one fails other one takes its place.
Here we have 3 web servers and nginx distributes traffic across multiple servers, so no server is overwhelmed.
```
  web1:
    <<: *web
    ports:
      - "8000:8000"
  
  web2:
    <<: *web
  
  web3:
    <<: *web

  
  nginx:
    image: nginx:latest
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
    ports:
      - "80:80"
    depends_on:
      - web1
      - web2
      - web3
  
```
## Disaster Recovery Plan
As we said before, we implemented database replication, ensuring that all data inside of primary, always saved in replica database in real-time. So if primary fails, the data will be inside of replica.
But let's consider other solutions:
1. Use `pg_dump` utility for backing up user data and orders. These backups should be scheduled periodically to ensure a point-in-time recovery.
2. Point-in-Time Recovery (PITR): postgesql WAL allows you to recover to any point in time by replaying WAL files. This ensures minimal data loss during unexpected failures.
3. Do regular testing of backups: periodically test system backups by restoring them in a separate environment to ensure they are not corrupted and the recovery process works as intended.
4. Monitoring and Alerts: set up monitoring tools to detect failures in real time
5. to recover from database replica we need switch primary to replica