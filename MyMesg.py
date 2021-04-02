import logging

import requests

LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s "
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a '
logging.basicConfig(level=logging.INFO,
                    format=LOG_FORMAT,
                    datefmt=DATE_FORMAT,
                    filename=r"log/info.log"
                    )


class MyMesg:

    baseMesgUrl = 'https://sc.ftqq.com/'
    sckey = 'SCU142685Tfd06f72db3371db1938bb69054c0bcef5fed785b32f38'

    def __init__(self, title):
        self.title = title

    def sendMesg(self, text):
        furl = MyMesg.baseMesgUrl + MyMesg.sckey + '.send' + '?text=' + self.title + '&desp=' + text
        logging.info('通过Server酱发送消息链接:' + furl)
        result = requests.get(url=furl)
        logging.info('发送结果' + str(result))
