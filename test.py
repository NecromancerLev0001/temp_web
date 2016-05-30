import web
import json
from alphacheck.statusinfo import StatusInfo
from alphacheck import infoman


def main():
    ifman = infoman.InfoRepository()
    print(ifman.jinfo('com000'))

    sinfo = StatusInfo('com000', 'live')
    print('jsondumps:', sinfo.jinfo())
    ifman.jupdate(sinfo.jinfo())
    print(ifman.jinfo('com000'))

if __name__ == "__main__":
    main()
