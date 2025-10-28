#!/usr/bin/env python3
import requests
from datetime import datetime, timedelta

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/order_reminders_log.txt"

# Define the date range: last 7 days
seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

# GraphQL query
query = """
query {
  orders(orderDate_Gte: "%s") {
    id
    customer {
      email
    }
  }
}
""" % seven_days_ago

# Send request
response = requests.post(GRAPHQL_URL, json={"query": query})

# Handle response
if response.status_code == 200:
    data = response.json()
    orders = data.get("data", {}).get("orders", [])

    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for order in orders:
            order_id = order.get("id")
            email = order.get("customer", {}).get("email")
            if order_id and email:
                f.write(f"{timestamp} - Order ID: {order_id}, Customer Email: {email}\n")

    print("Order reminders processed!")
else:
    print(f"Failed to fetch orders. Status code: {response.status_code}")
