import time
from django.db import connections

def query_performance_test():
    # Query on primary database
    with connections['default'].cursor() as cursor:
        start_time = time.time()
        cursor.execute("SELECT * FROM core_store;")
        primary_result = cursor.fetchone()
        primary_time = time.time() - start_time
        print(f"Primary DB Query Time: {primary_time:.4f} seconds")

    # Query on replica database
    with connections['replica'].cursor() as cursor:
        start_time = time.time()
        cursor.execute("SELECT * FROM core_store;") 
        replica_result = cursor.fetchone()
        replica_time = time.time() - start_time
        print(f"Replica DB Query Time: {replica_time:.4f} seconds")

query_performance_test()
