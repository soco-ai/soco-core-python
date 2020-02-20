from soco_core.soco_client import SOCOClient
from soco_core.examples import load_example_doc_data

if __name__ == '__main__':
    ADMIN_API_KEY = '898706a0-ecb2-457d-8f89-eea1c406f0ca'
    a_client = SOCOClient(ADMIN_API_KEY)

    # add data
    print("Add some data to the index")
    docs = load_example_doc_data(['mr-sun.json', 'technology.json'])
    a_client.delete_data()
    a_client.add_data(docs)
    print("Read {} documents".format(len(a_client.read_data())))

    print("Publish the index")
    a_client.abort(sync=False)
    a_client.publish()

    print("Make a query")
    QUERY_API_KEY = '727bb6b3-455c-4ee5-8f48-c2ab95837e56'
    q_client = SOCOClient(QUERY_API_KEY)
    responses = q_client.query({"query": "what is the distance from earth to sun?", "n_best": 10})
    SOCOClient.pprint(responses)
