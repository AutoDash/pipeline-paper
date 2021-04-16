import numpy as np
import firebase_admin as fb
from firebase_admin import credentials, db
from firebase_admin.db import Reference
from functools import reduce, partial

FIREBASE_CRED_FILENAME = "autodash-9dccb-add3cdae62ea.json"
RELEVANT_CLASSES = ['car', 'bus', 'truck', 'van', 'motorcycle', 'train', 'streetcar', 'pedestrian', 'bicycle', 'animal']
NOOP_CLASSES = ['NONE', 'test']
OTHER_CLASS = 'other'

def histogram_by_class(hist, data, seen):
    (key, data) = data
    if data.get('is_cancelled', True) or 'bb_fields' not in data or (data.get('url'), data.get('start_i')) in seen:
        return hist
    seen.add((data.get('url'), data.get('start_i')))
    viewed_ids = set()
    for obj in data['bb_fields'].get('objects', []):
        if obj['id'] not in viewed_ids:
            viewed_ids.add(obj['id'])
            obj_class = obj['class']
            if obj_class in RELEVANT_CLASSES + NOOP_CLASSES:
                hist[obj_class] = hist.get(obj_class, 0) + 1
            else:
                hist[OTHER_CLASS] = hist.get(OTHER_CLASS, 0) + 1 
    return hist

if __name__ == '__main__':
    cred = credentials.Certificate(FIREBASE_CRED_FILENAME)
    print('Created credentials')
    fb_app = fb.initialize_app(cred, {
            'databaseURL': 'https://autodash-9dccb.firebaseio.com/',
            'databaseAuthVariableOverride': {
                'uid': 'pipeline-worker'
            }
        })
    print('Created app')
    metadata = db.reference('metadata')
    print('Retrieved data')
    data = [ val for val in metadata.get().items() ]
    hist = reduce(partial(histogram_by_class, seen = set()), data, {})
    del hist['NONE']
    del hist['test']
    other = hist[OTHER_CLASS]
    del hist[OTHER_CLASS]
    items = [ *hist.items() ]
    items.sort(key=lambda x:x[1], reverse=True)
    items.append((OTHER_CLASS, other))
    print(items)
    dtype = [ ('X', object), ('Y', np.uint32) ]
    Z = np.array(items, dtype=dtype)
    np.savetxt('by-classes.csv', Z, delimiter=',', fmt=['%s', '%d'], header='X,Y', comments='')

