import unittest
import logging
import logging.config
from myLogger import MyLoggerConfig


def default_config():
    myLogger = MyLoggerConfig()
    myLogger.yaml_config_loader('../sample.yaml')
    logging.config.dictConfig(myLogger.get_myLogger_config())


class crawlingTest(unittest.TestCase):

    def test_load_base_page(self):
        from crawling_url_list import CrawlingUrl

        default_config()
        logger = logging.getLogger(__name__)
        logger.debug("Hello new world")

        target = 'http://snui.snu.ac.kr/ocw/index.php?mode=view&id=2937'

        crawl = CrawlingUrl(web_driver_path='../geckodriver')
        driver = crawl.get_web_driver()
        driver.get(target)


    def test_get_lecture_link(self):
        from crawling_url_list import CrawlingUrl


        target = 'http://snui.snu.ac.kr/ocw/index.php?mode=view&id=2937'
        crawl = CrawlingUrl(web_driver_path='../geckodriver')
        driver = crawl.get_web_driver()
        result = crawl.get_parsed_html_page(driver, target, '#class_room div a')

        crawl.get_video_link(driver, result)


    def test_starting(self):
        from crawling_url_list import CrawlingUrl

        crawl = CrawlingUrl(web_driver_path='../geckodriver', debug=True)
        crawl.start_crawling(url='')


