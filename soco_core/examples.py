import json
from soco_core.convertors import DocConvert
import os


def load_example_frame_data(name):
    cur_path = os.path.dirname(os.path.abspath(__file__))
    if name == 'mr-sun':
        doc = json.load(open(os.path.join(cur_path, '..', 'resources/mr-sun.json')))
        frames = DocConvert.document_to_frames(doc, lang='en', doc_meta={'doc_id': 'mr.sun', 'doc_title': 'Our Mr. Sun'})
        return frames
    else:
        raise Exception("Unknown {} frame example".format(name))


def load_example_doc_data(names):
    cur_path = os.path.dirname(os.path.abspath(__file__))
    docs = []
    for n in names:
        doc = json.load(open(os.path.join(cur_path, '..', 'resources/{}'.format(n))))
        docs.append(doc)
    return docs

if __name__ == '__main__':
    x = load_example_doc_data(['mr-sun.json', 'technology.json'])
    print(x)
