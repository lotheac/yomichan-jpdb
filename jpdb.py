#!/usr/bin/env python3

import http.client
import urllib.parse
import os
import sys
import typing
import logging

import bs4

logging.basicConfig(format='{asctime} {levelname} {message}',
        style='{', level=logging.INFO)
log = logging.getLogger()

def jpdb_add_word(word: str) -> None:
    conn = http.client.HTTPSConnection('jpdb.io')
    sid = os.environ['JPDB_SID']
    deck = 1
    hdrs = {'content-type': 'application/x-www-form-urlencoded',
            'cookie': f'sid={sid}'}
    params = urllib.parse.urlencode({'q': word, 'lang': 'japanese'})
    srch = f'/search?{params}'
    conn.request('GET', f'/search?{params}', headers=hdrs)
    resp = conn.getresponse()
    if resp.status != 200:
        raise ValueError(f'got resp {resp.status} from jpdb.io/search')
    soup = bs4.BeautifulSoup(resp, 'html.parser')
    res = soup.find(id='result-0')
    resword = ''.join(x for x in res.ruby if not isinstance(x, bs4.element.Tag))
    if word != resword:
        log.warning(f'{word!r} replaced by {resword!r}')
        word = resword
    
    form = res.find('form', action='/deck/1/add')
    if not form:
        log.warning(f'form not found; {word} already in deck?')
        return
    inputs = form.find_all('input', type='hidden')
    params = urllib.parse.urlencode({i.attrs['name']: i.attrs['value'] for i in inputs})
    conn.request('POST', '/deck/1/add', body=params, headers=hdrs)
    resp = conn.getresponse()
    log.info(f'added {word} {resp.status} {resp.reason}')
    while chunk := resp.read(4096):
        pass

if __name__ == '__main__':
    jpdb_add_word(sys.argv[1])
