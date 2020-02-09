from soco_core import sentence_splitter
from uuid import uuid4
import re


class DocConvert(object):
    @classmethod
    def _get_context(cls, data, current_idx, prev_char, next_char, last_title, last_section):
        answer = data[current_idx]['text']
        budget = prev_char
        idx = current_idx - 1
        prev_context = []

        # COMPUTE PREV CONTEXT
        while idx >= 0:
            if budget <= 0:
                break

            text = data[idx]['text']
            if data[idx]['type'] in ['title', 'section']:
                break

            if text not in prev_context:
                prev_context.append(text)
                budget = budget - len(text)

            idx -= 1

        if last_section and last_section != answer:
            prev_context.append(last_section)

        if last_title and last_title != answer:
            prev_context.append(last_title)

        prev_context = prev_context[::-1]

        # COMPUTE NEXT CONTEXT
        budget = next_char
        idx = current_idx + 1
        next_context = []
        while idx < len(data):
            if budget <= 0:
                break
            if data[idx]['type'] == 'title':
                break
            next_context.append(data[idx]['text'])
            budget = budget - len(data[idx]['text'])
            idx += 1

        context = ' '.join(prev_context + [answer] + next_context)
        answer_start = len(' '.join(prev_context)) + 1 if len(prev_context) > 0 else 0
        assert context[answer_start:answer_start + len(answer)] == answer
        return {'context': context,
                'answer_start': answer_start,
                'value': answer,
                'displayable': False,
                'add_to_qa_index': True}

    @classmethod
    def _normalize_whitespace(cls, text):
        text= text.replace('\n', ' ').replace('\r', '').replace('\t', '').replace('\xa0', ' ')
        return text

    @classmethod
    def context2frame(cls, context, meta):
        frame = {'answer': context, 'meta': meta}
        return frame

    @classmethod
    def get_context_size(cls, lang):
        if lang == 'en':
            return 150
        elif lang == 'zh':
            return 75
        else:
            raise Exception("unknown language {}".format(lang))

    @classmethod
    def document_to_frames(cls, doc, lang, doc_meta=None, verbose=False, min_ans_len=5, max_ans_len=500):
        # CUT DOCUMENTS INTO SENTENCES
        flatten_data = []
        too_short_cnt = 0
        too_long_cnt = 0

        for chunk in doc:
            text = chunk['text']
            if text is None:
                continue

            text = cls._normalize_whitespace(text)
            uid = str(uuid4())
            chunk_type = chunk.get('type')

            if chunk_type != 'content':
                record = {'text': text, 'chunk_id': uid, 'type': chunk_type, 'answer_start': 0}
                flatten_data.append(record)
            else:
                sentences = sentence_splitter.split_sentence(text, lang=lang)
                for s in sentences:
                    if len(s) < min_ans_len:
                        too_short_cnt += 1
                        continue

                    if len(s) > max_ans_len:
                        too_long_cnt += 1
                        continue

                    answer_start = text.index(s)
                    record = {'text': s, 'chunk_id': uid, 'type': chunk_type, 'answer_start': answer_start}
                    flatten_data.append(record)
                    assert text[answer_start:answer_start + len(s)] == s

        # INDEX RAW SENTENCES AS FRAMES
        last_title = ''
        last_section = ''
        frames = []
        for f_id, f_data in enumerate(flatten_data):
            chunk_type = f_data['type']
            text = f_data['text']
            if chunk_type == 'title':
                last_title = text
            elif chunk_type == 'section':
                last_section = text

            context_size = cls.get_context_size(lang)
            if chunk_type in ['title', 'section']:
                context = cls._get_context(flatten_data, f_id, prev_char=0, next_char=context_size,
                                           last_title=last_title, last_section=last_section)
            else:
                context = cls._get_context(flatten_data, f_id, prev_char=context_size, next_char=context_size,
                                           last_title=last_title, last_section=last_section)

            meta = {'chunk_id': f_data['chunk_id'], 'chunk_type': chunk_type}
            if doc_meta is not None:
                meta.update(**doc_meta)

            frame = cls.context2frame(context, meta)

            frames.append(frame)

        if verbose:
            print("DONE PROCESS {} RAW DOCUMENTS with {} too short skip {} too long skip".format(len(frames),
                                                                                                 too_short_cnt,
                                                                                                 too_long_cnt))
        return frames
