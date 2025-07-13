import datetime
import os
import django
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    with open("/tmp/crm_heartbeat_log.txt", "a") as log:
        log.write(f"{timestamp} CRM is alive\n")

def update_low_stock():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")
    django.setup()
    
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=True)
    
    mutation = gql("""
    mutation {
        updateLowStockProducts {
            message
            products {
                id
                name
                stock
            }
        }
    }
    """)
    
    result = client.execute(mutation)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("/tmp/low_stock_updates_log.txt", "a") as log:
        log.write(f"\n[{timestamp}] {result['updateLowStockProducts']['message']}:\n")
        for product in result['updateLowStockProducts']['products']:
            log.write(f"- {product['name']} (ID:{product['id']}): Stock → {product['stock']}\n")