from soco_core.soco_client import SOCOClient

if __name__ == '__main__':
    QUERY_API_KEY = 'a9c46b81-642b-45ec-98f4-44adfc7d516c'
    q_client = SOCOClient(QUERY_API_KEY)
    while True:
        q = input("Enter a query\n")
        resp = q_client.query({'query': q, 'n_best': 5})
        q_client.pprint(resp)
