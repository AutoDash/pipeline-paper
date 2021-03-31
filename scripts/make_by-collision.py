import numpy as np
import firebase_admin as fb
from firebase_admin import credentials, db
from firebase_admin.db import Reference
from functools import reduce
from matplotlib import pyplot as plt

FIREBASE_CRED_FILENAME = "autodash-9dccb-add3cdae62ea.json"
NO_COLLISION_LABEL = "No\ Collision"
MULTI_COLLISION_LABEL = "Multi\ Collision"
SIMPLE_COLLISION_LABEL = "Simple\ Collision"

def pie_by_collision(hist, data):
    (key, data) = data
    if not data.get('enum_tags'):
        return hist
    enum_tags = data['enum_tags']
    if 'MultiCollision' in enum_tags:
        hist.update({ MULTI_COLLISION_LABEL: hist.get(MULTI_COLLISION_LABEL, 0) + 1 })
    elif 'NoCollision' in enum_tags:
        hist.update({ NO_COLLISION_LABEL: hist.get(NO_COLLISION_LABEL, 0) + 1 })
    else:
        hist.update({ SIMPLE_COLLISION_LABEL : hist.get(SIMPLE_COLLISION_LABEL, 0) + 1 })

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
    plt.rcParams['font.size'] = 12.0
    plt.rcParams['text.usetex'] = True
    values = list(pie.values())
    keys = list(pie.keys())
    for i in range(len(keys)):
        keys[i] = r'$\mathrm{{{0}}}$'.format(keys[i])
    ax.pie(values, labels=keys, autopct=r'$%.1f\%%$')
    fig.tight_layout()
    fig.savefig('by-collision.png', bbox_inches='tight', pad_inches=0)
