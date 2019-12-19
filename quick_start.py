from soco_core.soco_client import SOCOClient
from soco_core.examples import load_example_data
import time

if __name__ == '__main__':
    QUERY_API_KEY = '727bb6b3-455c-4ee5-8f48-c2ab95837e56'
    ADMIN_API_KEY = '898706a0-ecb2-457d-8f89-eea1c406f0ca'

    q_client = SOCOClient(QUERY_API_KEY)
    a_client = SOCOClient(ADMIN_API_KEY)

    print("## Add some data to the index")
    data = load_example_data('Mr.Sun')
    a_client.append_to_index(data)

    print("## Wait for indexing is done ... ")
    a_client.wait_for_ready(timeout=10)

    print("## Make a query")
    responses = q_client.query("how many images", 10)
    SOCOClient.pprint(responses)
