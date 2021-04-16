import numpy as np
import firebase_admin as fb
from firebase_admin import credentials, db
from firebase_admin.db import Reference
from functools import reduce, partial

FIREBASE_CRED_FILENAME = "autodash-9dccb-add3cdae62ea.json"

def histogram_by_agents(hist, data, seen):
    (key, data) = data
    if data.get('is_cancelled', True) or 'bb_fields' not in data or (data.get('url'), data.get('start_i')) in seen:
        return hist
    seen.add((data.get('url'), data.get('start_i')))
    num_agents = 0
    viewed_ids = set()
    for obj in data['bb_fields'].get('objects', []):
        if obj['has_collision'] and obj['id'] not in viewed_ids:
            viewed_ids.add(obj['id'])
            num_agents += 1
    if 'CollisionWithRecordingVehicle' in data.get('enum_tags', []):
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
    hist = reduce(partial(histogram_by_agents, seen = set()), data, {})
    print(hist)
    dtype = [ ('X', object), ('Y', np.uint32) ]
    Z = np.array([ *hist.items() ], dtype=dtype)
    Z = np.sort(Z, axis=0)
    np.savetxt('by-agents.csv', Z, delimiter=',', fmt=['%s', '%d'], header='X,Y', comments='')
