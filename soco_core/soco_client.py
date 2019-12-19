import requests
from uuid import uuid4
import json
import time
from typing import Sequence, Generator
from tqdm import tqdm


class SOCOClient(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.query_url = 'https://api.soco.ai/v1/search/query'
        self.status_url = 'https://api.soco.ai/v1/index/status'
        self.append_url = 'https://api.soco.ai/v1/index/append'
        self.replace_url = 'https://api.soco.ai/v1/index/replace'

    def _get_header(self):
        return {'Content-Type': 'application/json', "Authorization": self.api_key}

    def _chunks(self, l: Sequence, n: int = 100) -> Generator[Sequence, None, None]:
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            is_last = i + n >= len(l)
            yield (l[i:i + n], is_last)

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

    def append_to_index(self, data, batch_size=100):
        job_results = []
        for batch, is_last in tqdm(self._chunks(data, n=batch_size), desc='appending to index'):
            data = {
                "data": batch,
                "is_last": is_last,
            }
            result = requests.post(self.append_url, json=data, headers=self._get_header())
            if result.status_code >= 300:
                print("Error in appending to index at SOCO servers")
                return None
            job_results.append(json.loads(result.text))

        return job_results

    def replace_index(self, data, batch_size=100):
        job_results = []
        print("Upload {} frames".format(len(data)))
        for batch, is_last in tqdm(self._chunks(data, n=batch_size), desc='replacing index'):
            data = {
                "data": batch,
                "is_last": is_last,
            }
            result = requests.post(self.replace_url, json=data, headers=self._get_header())
            if result.status_code >= 300:
                print("Error in replacing index at SOCO servers")
                return None
            job_results.append(json.loads(result.text))

        return job_results

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
