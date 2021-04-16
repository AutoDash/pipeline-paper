import numpy as np
import firebase_admin as fb
from firebase_admin import credentials, db
from firebase_admin.db import Reference
from functools import reduce
from pprint import pprint

FIREBASE_CRED_FILENAME = "autodash-9dccb-add3cdae62ea.json"

def count_bbs(count, data):
    (key, data) = data
    count['all_urls'].add(data.get('url'))
    if data.get('is_cancelled', True):
        return count
    if (data.get('url'), data.get('start_i')) in count.get('seen', set()):
        count['duplicated'].add((data.get('url'), data.get('start_i')))
    if 'bb_fields' in data and len(data['bb_fields']) > 0:
        if (data.get('url'), data.get('start_i')) not in count.get('seen', set()):
            count.update({ 'total': count.get('total', 0) + 1 })
        if 'collision_locations' in data['bb_fields'] and len(data['bb_fields']['collision_locations']) > 0:
            count.update({ 'collision': count.get('collision', 0) + 1 })
        if 'accident_locations' in data['bb_fields'] and len(data['bb_fields']['accident_locations']) > 0:
            count.update({ 'nested_accident': count.get('nested_accident', 0) + 1 })
    if 'accident_locations' in data and len(data['accident_locations']) > 0:
        count.update({ 'accident': count.get('accident', 0) + 1 })
    if not data.get('url'):
        count.update({ 'no_url': count.get('no_url', set()) + data.id })
    count['seen'].add((data['url'], data.get('start_i')))
    return count

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
    count = reduce(count_bbs, data, { 'seen':set(), 'duplicated': set(), 'all_urls': set() })
    del count['seen']
    del count['duplicated']
    all_urls = count['all_urls']
    if None in all_urls:
        del all_urls[None]
    count['all_urls'] = len(all_urls)
    pprint(count)

