# -*- coding:utf-8 -*-

import unittest
import logging
import logging.config

import os

from lib.myLogger import MyLoggerConfig
from lib.crawling_url_list import CrawlingUrl

default_drvier_path = './geckodriver'
default_config_path = './sample.yaml'


def default_config():
    myLogger = MyLoggerConfig()
    myLogger.yaml_config_loader(default_config_path)
    logging.config.dictConfig(myLogger.get_myLogger_config())



class CrawlingTest(unittest.TestCase):

    def test_webdriver(self):
        from lib.webdriver_downloader import WebDriverDownloader

        print("#current dir : ", os.getcwd())

        downloder = WebDriverDownloader()
        downloder.download_web_driver()

        default_drvier_path = './geckodriver'

        crawl = CrawlingUrl(web_driver_path=default_drvier_path)
        driver = crawl.get_web_driver()
        driver.get('http://snui.snu.ac.kr/ocw/index.php?mode=view&id=2937')

        # element = WebDriverWait(driver, 60).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, 'param[name=flashvars]'))
        # )

        print('COMPLETE MORE')
    #
    # def test_load_base_page(self):
    #
    #     default_config()
    #     logger = logging.getLogger(__name__)
    #     logger.debug("Hello new world")
    #
    #     target = 'http://snui.snu.ac.kr/ocw/index.php?mode=view&id=2937'
    #
    #     crawl = CrawlingUrl(web_driver_path=default_drvier_path)
    #     driver = crawl.get_web_driver()
    #     driver.get(target)
    #
    #
    # def test_get_lecture_link(self):
    #
    #
    #     target = 'http://snui.snu.ac.kr/ocw/index.php?mode=view&id=2937'
    #     crawl = CrawlingUrl(web_driver_path=default_drvier_path)
    #     driver = crawl.get_web_driver()
    #     result = crawl.get_parsed_html_page(driver, target, '#class_room div a')
    #
    #     crawl.get_video_link(driver, result)
    #
    #
    # def test_starting(self):
    #
    #
    #     crawl = CrawlingUrl(web_driver_path=default_drvier_path, debug=True)
    #     crawl.start_crawling(url='')
