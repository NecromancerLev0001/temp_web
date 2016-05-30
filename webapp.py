import sys
import thread
import time
import web
from alphacheck.mailman import snd_ml
from alphacheck.logger import log_info
from alphacheck.infoman import ifman
from datetime import datetime

urls = (
        '/signals/(.*)', 'Signal',
        '/', 'Index',
        '/(.*)/', 'Redirect' 
        )

class Index:
    def GET(self):
        return('hello world!') 

    def POST(self):
        pass


class Signal:
    def GET(self, sig_id):
        return ifman.jinfo(sig_id)

    def POST(self, sig_id):
        log_info('Signal-POST: %s' % web.data())
        ifman.jupdate(web.data())
        return 'ok'


class Redirect:
        def GET(self, path):
            web.seeother('/' + path)

    
if __name__ == "__main__":
    app = web.application(urls, globals())
    thread.start_new_thread(app.run, ())
    try:
        while True:
            time.sleep(65)
            err_sys = ifman.errSys()
            if err_sys:
                err_msg = '[%s] SYSTEM ERROR(%s)' % (err_sys, datetime.now().strftime('%Y%m%d%H%M%S'))
                snd_ml(err_msg, err_msg)
                continue
    except (KeyboardInterrupt, SystemExit):
        print('\nMAIN PROGRAM TERMINATE(keyboard interrupt)')
        log_info('MAIN PROGRAM TERMINATE(keyboard interrupt)')
        sys.exit(0)
