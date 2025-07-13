import datetime
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql("""
    query {
        totalCustomers: customers {
            totalCount
        }
        totalOrders: orders {
            totalCount
        }
        totalRevenue: orders {
            edges {
                node {
                    totalAmount
                }
            }
        }
    }
    """)

    try:
        result = client.execute(query)
        customers = result['totalCustomers']['totalCount']
        orders = result['totalOrders']['totalCount']
        revenue = sum(float(edge['node']['totalAmount']) 
                     for edge in result['totalRevenue']['edges'])
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = f"{timestamp} - Report: {customers} customers, {orders} orders, ${revenue:.2f} revenue\n"
        
        with open("/tmp/crm_report_log.txt", "a") as log:
            log.write(report)
        
        return report
    except Exception as e:
        return f"Error generating report: {str(e)}"