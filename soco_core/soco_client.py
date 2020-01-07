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

    def _check_fields(self, fields, object):
        for f in fields:
            if f not in object['answer']:
                raise Exception("{} is required inside answer".format(f))

    def check_frame_format(self, data):
        for frame in data:
            if 'answer' not in frame:
                raise Exception("answer is required for frame")
            self._check_fields(['value', 'context', 'answer_start'], frame)

            # check questions
            if 'questions' in frame:
                if type(frame['questions']) is not list:
                    raise Exception("Expect list for questions")
                for q in frame['questions']:
                    self._check_fields(['value'], q)


    def _chunks(self, l: Sequence, n: int = 100) -> Generator[Sequence, None, None]:
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            is_last = i + n >= len(l)
            is_first = i == 0
            yield (l[i:i + n], is_first, is_last)

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

    def append_to_index(self, data, batch_size=100, **kwargs):
        self.check_frame_format(data)
        job_results = []
        op_id = str(uuid4())
        for batch, is_first, is_last in tqdm(self._chunks(data, n=batch_size), desc='appending to index'):
            data = {
                "data": batch,
                "op_id": op_id,
                "is_last": is_last,
            }
            data.update(**kwargs)
            result = requests.post(self.append_url, json=data, headers=self._get_header())
            if result.status_code >= 300:
                print("Error in appending to index at SOCO servers")
                return None
            job_results.append(json.loads(result.text))

        return job_results

    def replace_index(self, data, sync=False, batch_size=100, **kwargs):
        self.check_frame_format(data)
        job_results = []
        op_id = str(uuid4())
        print("Upload {} frames with op_id {}".format(len(data), op_id))

        for batch, is_first, is_last in tqdm(self._chunks(data, n=batch_size), desc='replacing index', total=len(data)/batch_size):
            data = {
                "op_id": op_id,
                "data": batch,
                "is_first": is_first,
                "is_last": is_last,
            }
            data.update(**kwargs)
            result = requests.post(self.replace_url, json=data, headers=self._get_header())
            if result.status_code >= 300:
                try:
                    error_data = json.loads(result.text)
                    print(error_data)
                except:
                    print("Error in replacing index at SOCO servers")
                return None

            job_results.append(json.loads(result.text))

        if sync:
            print("Uploading done. Waiting for backend to finish.")
            self.wait_for_ready(verbose=False)

        return job_results

    def status(self):
        result = requests.get(self.status_url, headers=self._get_header())
        if result.status_code >= 300:
            print("Error in connecting to the SOCO servers")
            return None
        return json.loads(result.text)

    @classmethod
    def pprint(cls, results):
        for r in results:
            print("({}) - {}".format(r['turn_meta']['prob'], r['message']['value']))
