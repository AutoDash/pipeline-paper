import numpy as np
import firebase_admin as fb
from firebase_admin import credentials, db
from firebase_admin.db import Reference
from functools import reduce, partial

FIREBASE_CRED_FILENAME = "autodash-9dccb-add3cdae62ea.json"

def histogram_by_duration(hist, data, seen):
    (key, data) = data
    if 'end_i' not in data or 'start_i' not in data:
        return hist
    if data.get('is_cancelled', True) or 'bb_fields' not in data or (data.get('url'), data.get('start_i')) in seen:
        return hist
    seen.add((data.get('url'), data.get('start_i')))
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
    hist = reduce(partial(histogram_by_duration, seen = set()), data, [])
    hist, bins = np.histogram(hist, bins=10, range=(65, 1500))
    """
    if float('inf') in hist:
        hist['Unknown'] = hist[float('inf')]
        del hist[float('inf')]
    """
    print(bins)
    print(hist)
    bin_intervals = [str(int(x))+ "-" + str(int(y) - 1) for x,y in zip(bins[:-2], bins[1:-1])]
    bin_intervals.append(str(int(bins[-2]))+ "-" + str(int(bins[-1])))
    print(bin_intervals)
    dtype = [ ('X', object), ('Y', np.uint32) ]
    Z = np.array([ *zip(bin_intervals, hist) ], dtype=dtype)
    np.savetxt('by-duration.csv', Z, delimiter=',', fmt=['%s', '%d'], header='X,Y', comments='')

