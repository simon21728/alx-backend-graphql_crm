import requests
from datetime import datetime

def log_crm_heartbeat():
    """Logs a heartbeat message every 5 minutes."""
    log_file = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # Optional: check GraphQL hello field
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=3
        )
        if response.status_code == 200:
            msg = f"{timestamp} CRM is alive\n"
        else:
            msg = f"{timestamp} CRM heartbeat failed (GraphQL error)\n"
    except Exception:
        msg = f"{timestamp} CRM heartbeat failed (connection error)\n"

    with open(log_file, "a") as f:
        f.write(msg)
