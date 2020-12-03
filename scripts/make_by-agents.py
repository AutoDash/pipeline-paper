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
    if 'bb_fields' not in data or 'ids' not in data['bb_fields']:
       return hist
    num_agents = 0
    viewed_ids = set()
    ids = data.get('bb_fields', {}).get('ids')
    collisions = data.get('bb_fields', {}).get('has_collision')
    for id, has_collision in zip(ids, collisions):
        if has_collision and id not in viewed_ids:
            viewed_ids.add(id)
            num_agents += 1
    hist[num_agents] = hist.get(num_agents, 0) + 1
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
    np.savetxt('by-agents.csv', Z, delimiter=',', fmt=['%s', '%d'], header='X,Y', comments='')
