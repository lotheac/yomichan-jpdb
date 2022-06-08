#!/usr/bin/env python3

import http.client
import urllib.parse
import os
import sys
import typing

def jpdb_add_text(text: str) -> None:
    conn = http.client.HTTPSConnection('jpdb.io')
    sid = os.environ['JPDB_SID']
    deck = 1
    hdrs = {'content-type': 'application/x-www-form-urlencoded',
            'cookie': f'sid={sid}'}
    params = urllib.parse.urlencode({'id': deck, 'text': text})
    conn.request('POST', '/add_to_deck_from_text', body=params, headers=hdrs)
    resp = conn.getresponse()
    print(f'add {text}:', resp.status, resp.reason)
    while chunk := resp.read(4096):
        print(repr(chunk))
    if resp.status != 302:
        raise ValueError('not redirected from add_to_deck_from_text')
    loc = resp.getheader('Location')
    print(f'redir: {loc}')
    #conn.request('GET', loc, headers=hdrs)
    #resp = conn.getresponse()
    #print(resp.status, resp.reason)
    #while chunk := resp.read(4096):
    #    print(repr(chunk))
    confirm_id = urllib.parse.parse_qs(urllib.parse.urlparse(loc).query)['id'][0]
    params = urllib.parse.urlencode({'id': confirm_id})
    conn.request('POST', '/add_to_deck_from_text_confirm', body=params, headers=hdrs)
    resp = conn.getresponse()
    print(f'confirm {text}:', resp.status, resp.reason)
    while chunk := resp.read(4096):
        pass

if __name__ == '__main__':
    jpdb_add_text(sys.argv[1])
