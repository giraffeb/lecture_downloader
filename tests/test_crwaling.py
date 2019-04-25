# -*- coding:utf-8 -*-

import unittest
import logging
import logging.config

import os

from lib.myLogger import MyLoggerConfig
from lib.crawling_url_list import CrawlingUrl


working_dir = os.getcwd()
default_driver_path = working_dir+'/geckodriver'
default_driver_file_path = default_driver_path+'/geckodriver'
default_config_path = working_dir+'/sample.yaml'

def test_webdriver():
    from lib.webdriver_downloader import WebDriverDownloader

    print('#default dir ->', default_driver_path)

    downloder = WebDriverDownloader()
    downloder.download_web_driver()


    crawl = CrawlingUrl(web_driver_path=default_driver_file_path)
    driver = crawl.get_web_driver()
    driver.get('http://snui.snu.ac.kr/ocw/index.php?mode=view&id=2937')

    # element = WebDriverWait(driver, 60).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, 'param[name=flashvars]'))
    # )

    print('COMPLETE MORE')

def test_load_base_page():

    default_config()
    logger = logging.getLogger(__name__)
    logger.debug("Hello new world")

    target = 'http://snui.snu.ac.kr/ocw/index.php?mode=view&id=2937'

    crawl = CrawlingUrl(web_driver_path=default_driver_file_path)
    driver = crawl.get_web_driver()
    driver.get(target)


def test_get_lecture_link():


    target = 'http://snui.snu.ac.kr/ocw/index.php?mode=view&id=2937'
    crawl = CrawlingUrl(web_driver_path=default_driver_file_path)
    driver = crawl.get_web_driver()
    result = crawl.get_parsed_html_page(driver, target, '#class_room div a')

    crawl.get_video_link(driver, result)


def test_starting():


    crawl = CrawlingUrl(web_driver_path=default_driver_file_path, debug=True)
    crawl.start_crawling(url='')



def default_config():
    myLogger = MyLoggerConfig()
    myLogger.yaml_config_loader(default_config_path)
    logging.config.dictConfig(myLogger.get_myLogger_config())
