import logging
import json
import time
from datetime import datetime, timedelta
import mymail

logging.basicConfig(format='[%(asctime)s]%(message)s',
        filename='/home/ddklsj/mylog/alphastock.log',
        level=logging.DEBUG)

URI = 'http://127.0.0.1:8098/tsignals/1'
INTERVAL_SEC = 300

def send_signal(ss, sysinfo='end'):
    nowdtm = datetime.now()
    nowdt = nowdtm.strftime('%Y%m%d')    
    nowtm = nowdtm.strftime('%H%M%S') 
    jdt = json.dumps({'sysid': 'r0com', 'sysinfo': sysinfo,
        'tdate': nowdt, 
        'ttime': nowtm, 
        'marketstarttm': ss.market_starttm, 
        'marketendtm': ss.market_endtm,
        'nextworkdt': ss.next_workdt, 
        'nextworktm': ss.next_worktm})
    resp = requests.post(URI, data=jdt)


def check_signal():
    resp = requests.get(URI)
    if resp.status_code != 200:
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    signal = resp.json()
    return signal['ttime'], signal['sysinfo']


class Scheduler(object):
    def __init__(self):
        self.refresh()

    def refresh(self):
        resp = requests.get(URI)
        #if resp.status_code != 200:
        #    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
        signal = resp.json()
        self.market_starttm = signal['marketstarttm'] \
                if signal['marketstarttm']  else '090100'
        self.market_endtm = signal['marketendtm'] \
                if signal['marketendtm'] else '150200'
        self.next_workdt = signal['nextworkdt'] \
                if signal['nextworkdt'] else (datetime.now() + timedelta(days=1)).strftime('%Y%m%d')
        self.next_worktm = signal['nextworktm'] \
                if signal['nextworktm'] else '090100'
        self.tdt = datetime.now().strftime('%Y%m%d')

    def get_nowtm(self):
        return datetime.now().strftime('%H%M%S')

    def before_tm(self, sec=INTERVAL_SEC):
        return (datetime.now() - timedelta(seconds=sec)).strftime('%H%M%S')

    def delay(self, sec=INTERVAL_SEC):
        logging.info("Sleep Sec: %f\n" % sec)
        if sec <= 0:
            return False
        time.sleep(sec)
        return True

    def sleep(self):
        interval = datetime.strptime(self.next_workdt + self.next_worktm, 
                "%Y%m%d%H%M%S") - datetime.now()
        sec = interval.total_seconds()
        self.delay(sec)
        self.refresh()
        return True


def main():
    ss = Scheduler()

    while True:
        logging.info("ss.market_endtm: %s" % ss.market_endtm)
        while ss.get_nowtm() <= ss.market_endtm:
            ttime, sysinfo = check_signal()
            #if sysinfo == "end": break
            if sysinfo != "end" and ttime < ss.before_tm():
                mymail.snd_ml("PC Error - " + datetime.now().strftime("%Y%m%d"), "PC Error")
                send_signal(ss)
            ss.delay()
        ss.sleep()


if __name__ == '__main__':
    main()
    #ss = Scheduler()
    #send_signal(ss)
