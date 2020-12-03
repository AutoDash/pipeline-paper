import numpy as np
import firebase_admin as fb
from firebase_admin import credentials, db
from firebase_admin.db import Reference
from functools import reduce
from matplotlib import pyplot as plt

FIREBASE_CRED_FILENAME = "autodash-9dccb-add3cdae62ea.json"

def pie_by_collision(hist, data):
    (key, data) = data
    if not data.get('enum_tags'):
        return hist
    enum_tags = data['enum_tags']
    if 'MultiCollision' in enum_tags:
        hist.update({ 'MultiCollision': hist.get('MultiCollision', 0) + 1 })
    elif 'NoCollision' in enum_tags:
        hist.update({ 'NoCollision': hist.get('NoCollision', 0) + 1 })
    else:
        hist.update({ 'SimpleCollision': hist.get('SimpleCollision', 0) + 1 })

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
    pie = reduce(pie_by_collision, data, {})
    fig, ax = plt.subplots()
    ax.pie(pie.values(), labels=pie.keys(), autopct='%1.1f%%')
    fig.savefig('by-collision.png')
