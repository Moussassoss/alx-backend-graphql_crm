import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Configure the GraphQL endpoint
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=False,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

def log_crm_heartbeat():
    """Logs CRM heartbeat every 5 minutes"""
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message)

    # Optional GraphQL hello query to check API responsiveness
    try:
        query = gql("{ hello }")
        result = client.execute(query)
        f.write(f"{timestamp} - GraphQL responded: {result}\n")
    except Exception as e:
        f.write(f"{timestamp} - GraphQL request failed: {e}\n")


def update_low_stock():
    """Runs every 12 hours — updates low-stock products via GraphQL mutation"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    mutation = gql("""
    mutation {
      updateLowStockProducts {
        message
        updatedProducts {
          name
          stock
        }
      }
    }
    """)

    try:
        result = client.execute(mutation)
        data = result.get("updateLowStockProducts", {})
        updated = data.get("updatedProducts", [])
        message = data.get("message", "No message")

        with open("/tmp/low_stock_updates_log.txt", "a") as log:
            log.write(f"{timestamp} - {message}\n")
            for product in updated:
                log.write(f"{timestamp} - {product['name']} new stock: {product['stock']}\n")

    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as log:
            log.write(f"{timestamp} - Error: {e}\n")
