import requests
import json
import time
from datetime import datetime, timedelta
from alphacheck.statusinfo import StatusInfo
#import mymail

#logging.basicConfig(format='[%(asctime)s]%(message)s',
#        filename='/home/lsj/mylog/check_signal.log',
#        level=logging.DEBUG)

URI = 'http://127.0.0.1:8077/signals/'

def send_signal(sysinfo='checking'):
    sinfo = StatusInfo('com001', sysinfo)
    sinfo.workdt_flg = 'Y'
    resp = requests.post(URI, data=sinfo.jinfo())
    if resp.status_code != 200:
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))


def main():
    pass


if __name__ == '__main__':
    for i in range(5):
        time.sleep(3)
        send_signal('live')
