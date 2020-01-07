import json
from soco_core.convertors import DocConvert
import os


def load_example_frame_data(name):
    cur_path = os.path.dirname(os.path.abspath(__file__))
    if name == 'mr.sun':
        doc = json.load(open(os.path.join(cur_path, '..', 'resources/mr-sun.json')))
        frames = DocConvert.document_to_frames(doc, lang='en', doc_meta={'doc_id': 'mr.sun', 'doc_title': 'Our Mr. Sun'})
        return frames
    else:
        raise Exception("Unknown {} frame example".format(name))


def load_example_doc_data(name):
    if name == 'mr.sun':
        doc = json.load('../resources/mr-sun.json')
        return doc
    else:
        raise Exception("Unknown {} frame example".format(name))


if __name__ == '__main__':
    x = load_example_frame_data('mr.sun')
    print(x)
    json.dump(x, open('../resources/mr-sun-frames.json', 'w'), indent=2)
