# -*- coding:utf-8 -*-

import logging
import logging.config

import os



from lib.myLogger import MyLoggerConfig
from lib.crawling_url_list import CrawlingUrl


working_dir = os.getcwd()
default_driver_path = working_dir+'/geckodriver'
default_driver_file_path = default_driver_path+'/geckodriver'
default_config_path = working_dir+'/sample.yaml'

def test_down_web_driver():
    from lib.webdriver_downloader import WebDriverDownloader

    print('#default dir ->', default_driver_path)

    downloder = WebDriverDownloader()
    downloder.download_web_driver()

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



def test_until():
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By

    target = 'http://snui.snu.ac.kr/ocw/index.php?mode=view&id=2937'
    crawl = CrawlingUrl(web_driver_path=default_driver_file_path, debug=True)
    driver = crawl.get_web_driver()
    driver.get(target)

    try:
        eles = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'param[name=flashvars]'))
        )
        for e in eles:
            print('#', e.get_attribute('value'))

    except EnvironmentError:
        print('#####err')


    finally:
        driver.quit()






def default_config():
    myLogger = MyLoggerConfig()
    myLogger.yaml_config_loader(default_config_path)
    logging.config.dictConfig(myLogger.get_myLogger_config())
