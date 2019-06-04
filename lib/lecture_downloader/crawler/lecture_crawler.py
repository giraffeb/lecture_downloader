import logging
import copy
import timeit

from bs4 import BeautifulSoup
from selenium.webdriver.firefox.webdriver import WebDriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from lib.lecture_downloader.file_writer.file_writer import FileWriter

logging.basicConfig(level=logging.INFO)

class LectureCrawler:
    def __init__(self, target_webdriver, target_file_writer, lecture_page_list_query, lecture_video_query):
        self.debug = False #파싱 제한용

        self.web_driver :webdriver = target_webdriver
        self.file_writer: FileWriter = target_file_writer

        self.target_lecture_url = ''
        self.lecture_page_list_query = lecture_page_list_query
        self.lecture_video_query = lecture_video_query

        self.lecture_url_list = []
        self.complete_lecture_url_list = []

    # 크롤링의 작동 순서입니다.
    def do_crawling(self):

        # 1. 강의 url입력받기
        self.input_target_url()
        # 2. 강의 페이지에서 하위강의 제목, url 리스트 가져오기
        self.lecture_url_list = self.crawl_lecture_urls(self.target_lecture_url)
        # 3. 하위강의 url에서 video url가져오기
        self.complete_lecture_url_list = self.crawl_lecture_video_links(self.lecture_url_list)
        # 4. 하위강의 제목, video url 리스트 만들기 (3번에서 통합됨.
        # 5. 4번 내용을 파일로 저장하기
        self.file_writer.setting_lecture_list(self.complete_lecture_url_list)
        self.file_writer.save_file()


    def input_target_url(self):
        '''
        강의 url을 입력받습니다.
        :return:
        '''
        self.target_lecture_url = input('강의 url을 입력해주세요.')
        return

    def crawl_lecture_urls(self, target_lecture_url):
        '''
        강의 url에서 세부강의들의 제목과 페이지 링크를 리스트로 저장합니다.
        :return:
        '''
        print('# crawler lecture list page')
        start = timeit.default_timer()

        self.web_driver.get(target_lecture_url)

        target_page_plain_text = self.web_driver.page_source
        lecture_a_tag_list = BeautifulSoup(target_page_plain_text, "lxml").select(self.lecture_page_list_query)

        lecture_number = 0
        result_link_list = []

        suffix = '.mp4'
        for a_tag in lecture_a_tag_list:
            lecture_dict = {}

            lecture_dict['title'] = str(lecture_number)+'_' + a_tag.text + suffix
            lecture_dict['url'] = a_tag['href']

            result_link_list.append(lecture_dict)
            lecture_number += 1

        stop = timeit.default_timer()

        logging.info('[crawling lecture url list] time: %s, link: %s ', stop-start, self.target_lecture_url)

        return result_link_list

    def crawl_lecture_video_links(self, lecture_url_list):
        import timeit
        '''
        https://beomi.github.io/2017/10/29/HowToMakeWebCrawler-ImplicitWait-vs-ExplicitWait/
        WEBDRIVER until 기
        :param driver: 
        :param video_a_tag_list:
        :return:
        '''

        lecture_count = 0

        temp_complete_lecture_url_list = []
        print('# crawler video link')

        for lecture_link in self.lecture_url_list:
            if lecture_count > 5 and self.debug is True:  # debug mode TODO: 디버그 이후 삭제
                break

            # timeit 속도측정용
            start = timeit.default_timer()
            lucture_link_url = lecture_link['url']
            self.web_driver.get(lucture_link_url)

            # 해당엘리먼트가 로드되길 최대 120초까지 기다림
            urlencode_rtmp_src = ''

            try:
                eles = WebDriverWait(self.web_driver, 120).until(
                    # EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'param[name=flashvars]'))
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.lecture_video_query))
                )
                urlencode_rtmp_src = eles[0].get_attribute('value')

            except EnvironmentError:
                print('#####Until Error')

            new_lecture_dict = copy.deepcopy(lecture_link)

            rtmp_src = self.decode_url_encoding(urlencode_rtmp_src)  # urlencode된 값 디코드하기
            new_lecture_dict['video'] = rtmp_src

            temp_complete_lecture_url_list.append(new_lecture_dict)
            # timeit
            stop = timeit.default_timer()
            logging.info('[parsing time video link] time: %s, title: %s, link: %s, video: %s ', stop - start, new_lecture_dict['title'], lucture_link_url, rtmp_src)

        return temp_complete_lecture_url_list

    def decode_url_encoding(self, original_str):
        from urllib.parse import urlsplit, parse_qs
        import urllib
        '''
        urlencode된 값을 다시 원래 텍스트로 디코드합니다.
        :param original_str: 
        :return: 
        '''

        temp_str = urllib.parse.unquote(string=original_str, encoding='utf-8')  # urlencoding -> decoding
        query = urlsplit(temp_str).query  # url주소를 path, query 등으로 분리 query == parameters
        param = parse_qs(query)  # paramter단위로 분리 -> dict로 반환

        file = param.get("file")[0]
        stream = param.get("streamer")[0]

        return stream + file

