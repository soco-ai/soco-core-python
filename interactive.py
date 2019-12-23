from soco_core.soco_client import SOCOClient
from soco_core.examples import load_example_frame_data

if __name__ == '__main__':
    QUERY_API_KEY = '727bb6b3-455c-4ee5-8f48-c2ab95837e56'

    q_client = SOCOClient(QUERY_API_KEY)
    while True:
        q = input("Enter a query\n")
        resp = q_client.query(q, 5, alpha_bm25=0.01)
        q_client.pprint(resp)
