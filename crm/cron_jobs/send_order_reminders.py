import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL client setup
transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculate date range
start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()

# GraphQL query
query = gql("""
query {
    pendingOrders: orders(filter: { 
        order_date_gte: "%s", 
        status: "pending" 
    }) {
        id
        customer {
            email
        }
    }
}
""" % start_date)

# Execute and log
result = client.execute(query)
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open("/tmp/order_reminders_log.txt", "a") as log:
    log.write(f"[{timestamp}] Reminders Sent:\n")
    for order in result['pendingOrders']:
        log_entry = f"Order {order['id']} - {order['customer']['email']}\n"
        log.write(log_entry)

print("Order reminders processed!")