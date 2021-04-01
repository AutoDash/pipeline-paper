import numpy as np
import firebase_admin as fb
from firebase_admin import credentials, db
from firebase_admin.db import Reference
from functools import reduce
from matplotlib import pyplot as plt

FIREBASE_CRED_FILENAME = "autodash-9dccb-add3cdae62ea.json"
YOUTUBE_LABEL = "YouTube"
REDDIT_LABEL = "Reddit"
IMGUR_LABEL = "imgur.com"
GFYCAT_LABEL = "gfycat.com"
STREAMABLE_LABEL = "streamable.com"

def pie_by_source(hist, data):
    (key, data) = data
    if not data.get('download_src'):
        return hist
    src = data['download_src']
    if src == YOUTUBE_LABEL or src == 'youtube.com':
        hist.update({ YOUTUBE_LABEL: hist.get(YOUTUBE_LABEL, 0) + 1 })
    elif src == REDDIT_LABEL:
        hist.update({ REDDIT_LABEL: hist.get(REDDIT_LABEL, 0) + 1 })
    elif src == GFYCAT_LABEL:
        hist.update({ GFYCAT_LABEL: hist.get(GFYCAT_LABEL, 0) + 1 })
    elif src == STREAMABLE_LABEL:
        hist.update({ STREAMABLE_LABEL: hist.get(STREAMABLE_LABEL, 0) + 1 })
    elif src == IMGUR_LABEL:
        hist.update({ IMGUR_LABEL: hist.get(IMGUR_LABEL, 0) + 1 })       
    else:
        print(src)

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
    pie = reduce(pie_by_source, data, {})
    fig, ax = plt.subplots()
    plt.rcParams['font.size'] = 16.0
    plt.rcParams['text.usetex'] = True
    values = list(pie.values())
    keys = list(pie.keys())
    # Format the labels and values with LaTeX typeface
    for i in range(len(keys)):
        keys[i] = r'$\mathrm{{{0}}}$'.format(keys[i])
    patches, texts, wedgepcts = ax.pie(values, labels=keys, autopct=r'$%.1f\%%$')
    
    for i, j in zip(values, keys):
        print(str(i) + ' ' + j)
    
    fig.tight_layout()
    fig.savefig('by-source.png', dpi=300, bbox_inches='tight', pad_inches=0)