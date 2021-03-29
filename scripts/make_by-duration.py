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
    if 'end_i' not in data or 'start_i' not in data:
        return hist
    hist.append(data.get('end_i', float('inf')) - data.get('start_i', float('-inf')))
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
    hist = reduce(histogram_by_duration, data, [])
    print(hist)
    hist, bins = np.histogram(hist, bins=10, range=(65, 1500))
    """
    if float('inf') in hist:
        hist['Unknown'] = hist[float('inf')]
        del hist[float('inf')]
    """
    dtype = [ ('X', np.uint32), ('Y', np.uint32) ]
    Z = np.array([ *zip(bins, hist) ], dtype=dtype)
    np.savetxt('by-duration.csv', Z, delimiter=',', fmt=['%s', '%d'], header='X,Y', comments='')

