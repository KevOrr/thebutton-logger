#!/usr/bin/env python3

import re, sys, time, traceback
from urllib.request import urlopen, Request

import websocket

FILE = 'websocket_log.log'
ERROR_LOG = 'errors.log'

n = 0
with open(FILE, 'a') as f:
    while True:
        try:
            req = Request('http://www.reddit.com/r/thebutton', headers={'User-Agent': '/u/elaifiknow using Python3 urllib'})
            sr_html = urlopen(req).read().decode('utf-8', errors='ignore')
            print('Fetched http://www.reddit.com/r/thebutton')
            url = re.search('"thebutton_websocket": "(.*?)"', sr_html).groups()[0]
            print('Found r.config.thebutton_websocket')
            print('Url is ' + url)
            ws = websocket.WebSocket()
            ws.connect(url)
            print('Successfully connected to websocket')
            print('Writing to ' + FILE + '\n')

            while True:
                _ = f.write(ws.recv() + '\n')
                f.flush()
                n += 1
                sys.stdout.write('Lines written: ' + str(n) + '       \r')
        except Exception:
            print('Lost connection to websocket, or other error. Logging to errors.log')
            with open(ERROR_LOG, 'a') as f2:
                f2.write(time.asctime(time.gmtime()) + '\n')
                traceback.print_exc(file=f2)
                f2.write('\n')
        except KeyboardInterrupt:
            break
