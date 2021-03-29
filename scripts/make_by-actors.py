import numpy as np
import firebase_admin as fb
from firebase_admin import credentials, db
from firebase_admin.db import Reference
from functools import reduce

FIREBASE_CRED_FILENAME = "autodash-9dccb-add3cdae62ea.json"

def histogram_by_duration(hist, data):
    (key, data) = data
    if data.get('is_cancelled', True):
        return hist
    if 'bb_fields' not in data:
       return hist
    num_actors = len(set([ obj.get('id') for obj in data['bb_fields'].get('objects', []) ]))
    hist[num_actors] = hist.get(num_actors, 0) + 1
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
    hist = reduce(histogram_by_duration, data, {})
    print(hist)
    dtype = [ ('X', object), ('Y', np.uint32) ]
    Z = np.array([ *hist.items() ], dtype=dtype)
    Z = np.sort(Z, axis=0)
    np.savetxt('by-actors.csv', Z, delimiter=',', fmt=['%s', '%d'], header='X,Y', comments='')

