from soco_core.soco_client import SOCOClient

if __name__ == '__main__':
    QUERY_API_KEY = '[QUERY_KEY_API_KEY]'
    q_client = SOCOClient(QUERY_API_KEY)
    while True:
        q = input("Enter a query\n")
        resp = q_client.query({'query': q, 'n_best': 5})
        q_client.pprint(resp)
