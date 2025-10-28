from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """Logs a heartbeat message every 5 minutes to confirm CRM health."""
    log_file = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # Set up GraphQL transport
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    try:
        # Query the GraphQL hello field
        query = gql("{ hello }")
        response = client.execute(query)

        # Check if response is valid
        if response and "hello" in response:
            msg = f"{timestamp} CRM is alive\n"
        else:
            msg = f"{timestamp} CRM heartbeat failed (no 'hello' response)\n"
    except Exception as e:
        msg = f"{timestamp} CRM heartbeat failed (GraphQL error: {e})\n"

    # Append to log file
    with open(log_file, "a") as f:
        f.write(msg)
