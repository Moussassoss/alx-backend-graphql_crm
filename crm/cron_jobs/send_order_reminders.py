#!/usr/bin/env python3

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta
import pytz

# Define GraphQL endpoint
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=False,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Query for recent orders (within 7 days)
query = gql("""
query {
  orders(lastDays: 7) {
    id
    customer {
      email
    }
  }
}
""")

try:
    result = client.execute(query)
    orders = result.get("orders", [])
    timestamp = datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S")

    with open("/tmp/order_reminders_log.txt", "a") as log_file:
        for order in orders:
            log_file.write(f"{timestamp} - Reminder for order {order['id']} -> {order['customer']['email']}\n")

    print("Order reminders processed!")

except Exception as e:
    print(f"Error: {e}")
