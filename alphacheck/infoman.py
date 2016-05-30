from .statusinfo import StatusInfo
import json
from datetime import datetime, timedelta
from logger import log_info

class InfoRepository:
    __shared_state = {}
    __repo = {}

    def __init__(self, sInfo=StatusInfo()):
        self.__dict__ = self.__shared_state
        self.state = 'Init'
        self.supdate(sInfo)

    def supdate(self, sInfo):
        self.__repo.update({sInfo.sysid: sInfo.jinfo()})

    def jupdate(self, tInfo):
        #dInfo = json.loads(tInfo)
        #self.__repo.update({dInfo['sysid']: tInfo})

        dInfo = json.loads(tInfo)
        dInfo['server_tm'] = datetime.now().strftime('%H%M%S')
        sInfo = StatusInfo(ddata=dInfo)
        self.__repo.update({sInfo.sysid: sInfo.jinfo()})

    def sinfo(self, sysid):
        tdata = json.loads(self.__repo[sysid])
        return StatusInfo(ddata=tdata)
        
    def jinfo(self, sysid):
        return self.__repo[sysid]

    def errSys(self):
        for rkey in self.__repo.keys():
            if self.sinfo(rkey).isError():
                log_info('ERROR >> ')
                log_info('sysid: %s' % (rkey))
                log_info('tm: %s' % self.sinfo(rkey).tm)
                log_info('<< ERROR')
                self.__repo.pop(rkey)
                return rkey

    def __str__(self):
        return self.state

ifman = InfoRepository()

