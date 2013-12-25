# Clean up some extra fancy punctuation

import re
from app import brain

punc = '“”‘’–."'

def merge_count_dicts(x, y):
    """
    Merges y into x,
    where each is a dictionary of {'term': count}
    """
    for k, v_y in y.items():
        try:
            v_x = x[k]
            x[k] = v_y + v_x
        except KeyError:
            x[k] = v_y
    return x


if __name__ == '__main__':
    knowledge_copy = brain.MKV.knowledge.copy()
    for k,v in knowledge_copy.items():
        try:
            term = k[0]
            if set(punc).intersection(term):
                term_ = re.sub(r'['+punc+']', '', term)
                k_ = (term_,)

                try:
                    brain.MKV.knowledge[k_] = merge_count_dicts(brain.MKV.knowledge[k_], v)
                except KeyError:
                    brain.MKV.knowledge[k_] = v
        except IndexError:
            pass

    # brain.MKV.save()