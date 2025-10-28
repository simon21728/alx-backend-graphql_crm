#!/usr/bin/env python3
import asyncio
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

LOG_FILE = "/tmp/order_reminders_log.txt"
GRAPHQL_URL = "http://localhost:8000/graphql"


async def main():
    # Create the transport and client
    transport = AIOHTTPTransport(url=GRAPHQL_URL)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Calculate date range
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # Define GraphQL query
    query = gql("""
        query ($date: Date!) {
            orders(orderDate_Gte: $date) {
                id
                customer {
                    email
                }
            }
        }
    """)

    # Execute query
    params = {"date": seven_days_ago}
    result = await client.execute_async(query, variable_values=params)

    # Log the results
    orders = result.get("orders", [])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        for order in orders:
            order_id = order.get("id")
            email = order.get("customer", {}).get("email")
            if order_id and email:
                f.write(f"{timestamp} - Order ID: {order_id}, Customer Email: {email}\n")

    print("Order reminders processed!")


if __name__ == "__main__":
    asyncio.run(main())
