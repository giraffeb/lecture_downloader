import pytest

from lib.lecture_downloader.crawler.lecture_crawler import LectureCrawler
from lib.lecture_downloader.web_driver.web_driver_factory import WebDriverFactory
from lib.lecture_downloader.file_writer.file_writer import FileWriter

import yaml
import json

config = None
config_path = 'config/config.yaml'

with open(config_path, 'r') as f:
    config = yaml.full_load(f)

web_driver = WebDriverFactory.create_web_driver('firefox')
file_writer = FileWriter('test_example.txt')

lecture_page_list_query = config['crawler']['lecture_page_list_query']
lecture_video_query = config['crawler']['lecture_video_query']

crawler = LectureCrawler(target_webdriver=web_driver
                             , target_file_writer=file_writer
                             , lecture_page_list_query=lecture_page_list_query
                             , lecture_video_query=lecture_video_query)

example_list = None
example_list_path = 'test/example_list.txt'
with open(example_list_path, 'r') as f:
    example_list = json.load(f)


def test_lecture_list_crawling():
    crawl_list = crawler.crawl_lecture_urls('http://snui.snu.ac.kr/ocw/index.php?mode=view&id=2937')
    crawl_list = file_writer.do_file_name_filtering(crawl_list)

    for i in range(len(crawl_list)):
        assert crawl_list[i]['title'] == example_list[i]['title']
        assert crawl_list[i]['url'] == example_list[i]['url']


def test_lecture_video_list_crawling():
    #1
    crawler.target_lecture_url = 'http://snui.snu.ac.kr/ocw/index.php?mode=view&id=2937'
    crawler.lecture_url_list = crawler.crawl_lecture_urls(crawler.target_lecture_url)
    # 3. 하위강의 url에서 video url가져오기
    crawler.complete_lecture_url_list = crawler.crawl_lecture_video_links(crawler.lecture_url_list)
    # 4. 하위강의 제목, video url 리스트 만들기 (3번에서 통합됨.
    # 5. 4번 내용을 파일로 저장하기
    crawler.file_writer.setting_lecture_list(crawler.complete_lecture_url_list)
    crawler.file_writer.save_file()

    crawl_list = crawler.file_writer.complete_lecture_url_list

    for i in range(len(crawl_list)):
        assert crawl_list[i]['title'] == example_list[i]['title']
        assert crawl_list[i]['url'] == example_list[i]['url']
        assert crawl_list[i]['video'] == example_list[i]['video']




