import time

print("ingest worker started", flush=True)

while True:
    print("worker alive, sleeping...", flush=True)
    time.sleep(60)
