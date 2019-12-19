from soco_core.soco_client import SOCOClient
from soco_core.examples import load_example_frame_data

if __name__ == '__main__':
    QUERY_API_KEY = '727bb6b3-455c-4ee5-8f48-c2ab95837e56'
    ADMIN_API_KEY = '898706a0-ecb2-457d-8f89-eea1c406f0ca'

    q_client = SOCOClient(QUERY_API_KEY)
    a_client = SOCOClient(ADMIN_API_KEY)

    print("## Add some data to the index")
    data = load_example_frame_data('mr.sun')
    a_client.replace_index(data)

    print("## Wait for indexing is done ... ")
    a_client.wait_for_ready(check_frequency=2, timeout=10, verbose=False)

    print("## Make a query")
    responses = q_client.query("how many images", 10)
    SOCOClient.pprint(responses)
