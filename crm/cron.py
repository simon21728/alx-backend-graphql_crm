from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def update_low_stock():
    """Executes the UpdateLowStockProducts mutation and logs updates."""
    log_file = "/tmp/low_stock_updates_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Configure GraphQL client
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)

    try:
        # Define GraphQL mutation
        mutation = gql("""
        mutation {
            updateLowStockProducts {
                success
                message
                updatedProducts {
                    id
                    name
                    stock
                }
            }
        }
        """)

        # Execute mutation
        response = client.execute(mutation)
        result = response.get("updateLowStockProducts", {})

        # Log updated products
        with open(log_file, "a") as f:
            f.write(f"{timestamp} - {result.get('message', 'No response')}\n")
            for product in result.get("updatedProducts", []):
                f.write(f"   Product: {product['name']}, New Stock: {product['stock']}\n")

    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"{timestamp} - Failed to update low stock products: {e}\n")

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
