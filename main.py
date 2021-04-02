# -*-coding:utf-8-*-

import sys
import time
import requests
import logging

from selenium.common.exceptions import TimeoutException

from MyMesg import MyMesg

LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s "
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a '
logging.basicConfig(level=logging.INFO,
                    format=LOG_FORMAT,
                    datefmt=DATE_FORMAT,
                    filename=r"log/info.log"
                    )


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as Expect
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver import FirefoxOptions

# https://www.cnblogs.com/lishanlei/p/10707857.html python变量作用域

# 房地产销售页面
url = 'http://www.fangdi.com.cn/new_house/new_house_detail.html?project_id=069c616823d32fc8'
basemesgurl = 'https://sc.ftqq.com/'
sckey = ''
title = '销售情况'
total = 0


def load_driver_path():
    platform = sys.platform
    if platform.__contains__('darwin'):
        logging.info('System is OsX')
        return 'driver/mac_geckodriver'
    if platform.__contains__('linux'):
        logging.info('System is linux')
        return 'driver/linux_geckodriver'


def dos_can():
    global total
    global execFlag
    try:
        mesg = ''
        # 启动浏览器
        options = FirefoxOptions()
        options.add_argument('--headless')
        driver_path = load_driver_path()
        browser = webdriver.Firefox(options=options, executable_path=driver_path)

        # 开始获取内容
        browser.get(url)

        Wait(browser, 100).until(
            Expect.presence_of_element_located((By.ID, "salesInformation"))
        )
        navBar = browser.find_element_by_id('salesInformation')
        logging.info(str(navBar.text))
        logging.info('-----------------------')
        insist = navBar.find_elements_by_class_name('new_house_sale_list')

        if len(insist) == 0:
            logging.info('未抓取到数据')
            return

        csList = insist[0].find_elements_by_class_name('text_ellipsis')
        logging.info(csList[0].text)
        mesg = mesg + csList[0].text + '\n'

        csList1 = insist[1].find_elements_by_class_name('text_ellipsis')
        logging.info(csList1[0].text)
        mesg = mesg + csList1[0].text + '\n'

        csList2 = insist[3].find_elements_by_class_name('text_ellipsis')
        logging.info(csList2[0].text)
        mesg = mesg + csList2[0].text + '\n'

        csList3 = insist[5].find_elements_by_class_name('text_ellipsis')
        logging.info(csList3[0].text)
        mesg = mesg + csList3[0].text + '\n'
        logging.info('----------------------')

        # 获取月销售情况
        salespeed = browser.find_element_by_id('saleSpeed')

        # 获取总销售量
        items = salespeed.find_elements_by_class_name('business_sale_item')
        spans = items[-1].find_elements_by_xpath('span')
        nowTotal = int(spans[-1].text)

        if nowTotal <= total:
            logging.info('销售量未发生变化，原来%s,现在%s' % (total, nowTotal))
            return ""

        temp = total
        total = nowTotal
        mesg = mesg + '总销售量：' + str(total) + ' 上次' + str(temp) + '套'

        # 发送消息
        MyMesg(title).sendMesg(mesg)
    except TimeoutException as t:
        logging.error('获取数据超时', t)
    except Exception as e:
        logging.error('操作异常', e)
    finally:
        browser.close()
        browser.quit()
    return ""


if __name__ == "__main__":
    logging.info("爬虫脚本开启，准备获取网页数据")
    a = 1
    while 1 == a:
        logging.info("--------------------------扫描开始--------------------------------")
        dos_can()
        time.sleep(1800)
