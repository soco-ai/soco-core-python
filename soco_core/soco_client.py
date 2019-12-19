import requests
from uuid import uuid4
import json
import time


class SOCOClient(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.query_url = 'https://api.soco.ai/v1/search/query'
        self.status_url = 'https://api.soco.ai/v1/index/status'

    def _get_header(self):
        return {'Content-Type': 'application/json', "Authorization": self.api_key}

    def query(self, query, n_best, uid=None, alpha_bm25=0, use_mrc=False, max_l2r=-1, filters=None):
        data = {
            "query": query,
            "n_best": n_best,
            "uid": uid if uid is not None else str(uuid4())
        }
        args = {'alpha_bm25': alpha_bm25, 'use_mrc': use_mrc, 'max_l2r': max_l2r, 'filters': filters}
        data.update(**args)
        result = requests.post(self.query_url, json=data, headers=self._get_header())
        if result.status_code >= 300:
            print("Error in connecting to the SOCO servers")
            return None

        return json.loads(result.text)

    def append_to_index(self, data):
        pass

    def replace_index(self, data):
        pass

    def status(self):
        result = requests.get(self.status_url, headers=self._get_header())
        if result.status_code >= 300:
            print("Error in connecting to the SOCO servers")
            return None
        return json.loads(result.text)

    def wait_for_ready(self, check_frequency=2, timeout=-1, verbose=False):
        start_time = time.time()
        time.sleep(0.5)
        while True:
            state = self.status()
            if state['status'] == 'ready':
                break

            elapsed_time = int(time.time() - start_time)
            if verbose:
                print("Have waited {} seconds with index size {}".format(int(time.time() - start_time), state['size']))

            if 0 < timeout < elapsed_time:
                print("Time out!")
                return

            time.sleep(check_frequency)

        print("Index is ready!")

    @classmethod
    def pprint(cls, results):
        for r in results:
            print("({}) - {}".format(r['turn_meta']['prob'], r['message']['value']))

