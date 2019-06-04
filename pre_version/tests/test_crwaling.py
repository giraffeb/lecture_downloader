# -*- coding:utf-8 -*-

import logging
import logging.config
import os

import pytest

from pre_version.lib.crawling_url_list import CrawlingLecture

working_dir = os.getcwd()
default_driver_path = working_dir+'/geckodriver'
default_driver_file_path = default_driver_path+'/geckodriver'
# default_config_path = working_dir+'/logger.yaml'


@pytest.mark.first
def test_down_web_driver():
    print('#first')

    from pre_version.lib.webdriver_downloader import WebDriverDownloader
    from time import sleep

    print('#default dir ->', default_driver_path)

    downloder = WebDriverDownloader()
    downloder.download_web_driver()
    sleep(3)

@pytest.mark.second
def test_load_base_page():
    print('#second')

    # default_config()
    logger = logging.getLogger(__name__)
    logger.debug("Hello new world")

    target = 'http://snui.snu.ac.kr/ocw/index.php?mode=view&id=2937'

    crawl = CrawlingLecture(web_driver_path=default_driver_file_path)
    driver = crawl.get_web_driver() #Test Version
    driver.get(target)

    page_html = driver.page_source
    print(page_html[:100])


#시간제한
# @pytest.mark.third
# def test_get_lecture_link():
#     import timeit
#     print('#third')
#
#     target = 'http://snui.snu.ac.kr/ocw/index.php?mode=view&id=2937'
#     crawler = CrawlingUrl(web_driver_path=default_driver_file_path)
#     driver = crawler.get_web_driver() #Test Version
#     start = timeit.default_timer()
#     result = crawler.get_parsed_html_page(driver, target, '#class_room div a')
#
#
#     for l in result:
#         lecture_link = l['href']
#         print(lecture_link)
#
#
#     stop = timeit.default_timer()
#     print('#link list getting time -> ', stop - start)
#
#     crawler.get_video_link(driver, result)

#시간제한
# @pytest.mark.forth
# def test_get_lecture_link_one():
#     import timeit
#     print('#third')
#
#     target = 'http://snui.snu.ac.kr/ocw/index.php?mode=view&id=2937'
#     crawler = CrawlingUrl(web_driver_path=default_driver_file_path)
#     driver = crawler.get_web_driver()  # Test Version
#     start = timeit.default_timer()
#     result = crawler.get_parsed_html_page(driver, target, '#class_room div a')
#
#     for l in result:
#         lecture_link = l['href']
#         print(lecture_link)
#         break
#
#     stop = timeit.default_timer()
#     print('#link list getting time -> ', stop - start)
#
#     crawler.get_video_link(driver, result)




# def default_config():
#     myLogger = MyLoggerConfig()
#     myLogger.yaml_config_loader(default_config_path)
#     logging.config.dictConfig(myLogger.get_myLogger_config())
