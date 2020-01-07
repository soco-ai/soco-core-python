from soco_core.soco_client import SOCOClient
from soco_core.examples import load_example_frame_data

if __name__ == '__main__':
    ADMIN_API_KEY = '898706a0-ecb2-457d-8f89-eea1c406f0ca'

    a_client = SOCOClient(ADMIN_API_KEY)

    print("Add some data to the index")
    frames = load_example_frame_data('mr.sun')
    print("Loaded {} frames.".format(len(frames)))
    a_client.replace_index(frames, sync=True, db_encoder_id='bert-base-uncase-answer-squad-4head')


    print("Make a query")
    QUERY_API_KEY = '727bb6b3-455c-4ee5-8f48-c2ab95837e56'
    q_client = SOCOClient(QUERY_API_KEY)
    responses = q_client.query("what is the distance from earth to sun?", 10)
    SOCOClient.pprint(responses)
