import numpy as np
import firebase_admin as fb
from firebase_admin import credentials, db
from firebase_admin.db import Reference
from functools import reduce
from matplotlib import pyplot as plt

FIREBASE_CRED_FILENAME = "autodash-9dccb-add3cdae62ea.json"
STATIONARY_CAMERA_LABEL= "Stationary\ Camera"
MANHELD_CAMERA_LABEL= "Manheld\ Camera"
DASHCAM_LABEL= "Dashcam"

def pie_by_camera(hist, data):
    (key, data) = data
    if not data.get('enum_tags'):
        return hist
    enum_tags = data['enum_tags']
    if 'StationaryCamera' in enum_tags:
        hist.update({ STATIONARY_CAMERA_LABEL: hist.get(STATIONARY_CAMERA_LABEL, 0) + 1 })
    elif 'ManHeldCamera' in enum_tags:
        hist.update({ MANHELD_CAMERA_LABEL: hist.get(MANHELD_CAMERA_LABEL, 0) + 1 })
    else:
        hist.update({ DASHCAM_LABEL: hist.get(DASHCAM_LABEL, 0) + 1 })

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
    pie = reduce(pie_by_camera, data, {})
    fig, ax = plt.subplots()
    plt.rcParams['font.size'] = 12.0
    plt.rcParams['text.usetex'] = True
    values = list(pie.values())
    keys = list(pie.keys())
    for i in range(len(keys)):
        keys[i] = r'$\mathrm{{{0}}}$'.format(keys[i])
    ax.pie(values, labels=keys, autopct=r'$%.1f\%%$')
    fig.tight_layout()
    fig.savefig('by-camera.png', bbox_inches='tight', pad_inches=0)