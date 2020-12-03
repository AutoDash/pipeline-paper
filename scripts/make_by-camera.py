import numpy as np
import firebase_admin as fb
from firebase_admin import credentials, db
from firebase_admin.db import Reference
from functools import reduce
from matplotlib import pyplot as plt

FIREBASE_CRED_FILENAME = "autodash-9dccb-add3cdae62ea.json"

def pie_by_camera(hist, data):
    (key, data) = data
    if not data.get('enum_tags'):
        return hist
    enum_tags = data['enum_tags']
    if 'StationaryCamera' in enum_tags:
        hist.update({ 'StationaryCamera': hist.get('StationaryCamera', 0) + 1 })
    elif 'ManHeldCamera' in enum_tags:
        hist.update({ 'ManHeldCamera': hist.get('ManHeldCamera', 0) + 1 })
    else:
        hist.update({ 'DashCamera': hist.get('DashCamera', 0) + 1 })

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
    ax.pie(pie.values(), labels=pie.keys(), autopct='%1.1f%%')
    fig.savefig('by-camera.png')
