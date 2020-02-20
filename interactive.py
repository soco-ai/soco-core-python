from soco_core.soco_client import SOCOClient

if __name__ == '__main__':
    QUERY_API_KEY = '727bb6b3-455c-4ee5-8f48-c2ab95837e56'
    q_client = SOCOClient(QUERY_API_KEY)
    while True:
        q = input("Enter a query\n")
        resp = q_client.query({'query': q, 'n_best': 5})
        q_client.pprint(resp)
