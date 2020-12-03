import numpy as np
import firebase_admin as fb
from firebase_admin import credentials, db
from firebase_admin.db import Reference
from functools import reduce

FIREBASE_CRED_FILENAME = "autodash-9dccb-add3cdae62ea.json"

def histogram_by_class(hist, data):
    (key, data) = data
    if data.get('is_cancelled', True):
        return hist
    viewed_ids = set()
    clss = data.get('bb_fields', {}).get('clss', [])
    ids = data.get('bb_fields', {}).get('ids', [])
    for cls, id in zip(clss, ids):
        if id not in viewed_ids:
            viewed_ids.add(id)
            hist[cls] = hist.get(cls, 0) + 1
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
    hist = reduce(histogram_by_class, data, {})
    print(hist)
    dtype = [ ('X', object), ('Y', np.uint32) ]
    Z = np.array([ *hist.items() ], dtype=dtype)
    np.savetxt('by-classes.csv', Z, delimiter=',', fmt=['%s', '%d'], header='X,Y', comments='')

