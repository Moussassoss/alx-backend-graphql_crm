import datetime
import requests

def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message)

    # Optional GraphQL ping
    try:
        response = requests.post("http://localhost:8000/graphql", json={"query": "{ hello }"})
        if response.ok:
            f.write(f"{timestamp} - GraphQL endpoint responded OK\n")
    except Exception as e:
        f.write(f"{timestamp} - GraphQL endpoint failed: {e}\n")
