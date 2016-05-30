import json
from datetime import datetime, timedelta

CHECK_START_TM = '070000'

class StatusInfo(object):
    def __init__(self, sysid='com000', sysinfo='checking', ddata=None):
        if ddata:
            self.refreshFromStr(ddata)
        else:
            self.refreshFromNothing(sysid, sysinfo)

    def getNowTm(self):
        return datetime.now().strftime('%H%M%S')

    def beforeTm(self, sec):
        return (datetime.now() - timedelta(seconds=sec)).strftime('%Y%m%d%H%M%S')

    def before6m(self):
        return self.beforeTm(360)

    def refreshFromNothing(self, sysid, sysinfo):
        nowdtm = datetime.now()
        nowdt = nowdtm.strftime('%Y%m%d')    
        nowtm = nowdtm.strftime('%H%M%S') 
        # Initialization
        self.sysid = sysid 
        self.sysinfo = sysinfo
        self.tdate = nowdt
        self.wk_dt = '' 
        self.tm = nowtm 
        self.server_tm = nowtm 
        self.mk_starttm = ''
        self.mk_endtm = ''
        self.next_workdt = ''
        self.next_starttm = ''
 
    def refreshFromStr(self, ddata):
        self.sysid = ddata['sysid']
        self.sysinfo = ddata['sysinfo']
        self.tdate = ddata['tdate']
        self.wk_dt = ddata['wk_dt']
        self.tm = ddata['tm']
        self.server_tm = ddata['server_tm']
        self.mk_starttm =  ddata['mk_starttm']
        self.mk_endtm = ddata['mk_endtm']
        self.next_workdt = ddata['next_workdt']
        self.next_starttm = ddata['next_starttm']
   
    def jinfo(self):
        return json.dumps({'sysid': self.sysid, 
            'sysinfo': self.sysinfo,
            'tdate': self.tdate, 
            'wk_dt': self.wk_dt, 
            'tm': self.tm, 
            'server_tm': self.server_tm, 
            'mk_starttm': self.mk_starttm, 
            'mk_endtm': self.mk_endtm,
            'next_workdt': self.next_workdt, 
            'next_starttm': self.next_starttm})

    def isCheckTm(self):
        if CHECK_START_TM <= self.getNowTm() and self.getNowTm() <= self.mk_endtm:
            return True
        return False

    def isTmOver(self):
        if self.tdate + self.server_tm < self.before6m():
            return True
        return False

    def isUncheckDt(self):
        if self.tdate != self.wk_dt:
            return True
        return False

    def isError(self):
        if self.isUncheckDt() or self.sysinfo == 'checking':
            return False
        if self.isCheckTm() and self.isTmOver():
            self.sysinfo = 'checking'
            return True
        return False


    def __repr__(self):
        return '[%s / %s]' % (self.sysid, self.sysinfo)

