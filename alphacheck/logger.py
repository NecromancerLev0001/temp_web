import logging

logging.basicConfig(format='[%(asctime)s]%(message)s',
        filename='/home/ddklsj/mylog/alphastock.log',
        level=logging.DEBUG)


log_info = lambda s: logging.info(s)

