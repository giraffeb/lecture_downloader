# -*- coding:utf-8 -*-
import logging
import timeit

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CrawlingLecture:

    def __init__(self, file_path='./list.txt', char_encoding='utf-8', web_driver_path='', debug=False):

        self.debug = debug

        self.file_path = file_path
        self.char_encoding = char_encoding
        self.web_driver_path = web_driver_path

        self.driver = None


    def start_crawling(self, url):
        '''
        크롤링하는 로직.
        :param url:
        :return:
        '''

        #1 강의를 받을 URL입력받음
        if url == '' or url == None:
            print('URL이 입력되지 않았습니다.')
            exit()

        #2 webdriver 가져오기
        driver = self.get_web_driver()

        #3 #1에서 입력받은 URL를 파싱해서 target_query에 해당하는 정보를 저장함.
        #해당강의의 전체링크 리스트임.
        lecture_a_tag_list = self.crawl_page(driver=driver, url=url, target_query='#class_room div a')

        lecuture_list = self.crawl_video_link_from_url(driver, lecture_a_tag_list)
        self.save_file_video_url_list(file_path=self.file_path, download_list=lecuture_list)
        logging.debug('file writing complete')


    def setting_option(self):
        firefoxProfile = FirefoxProfile()
        firefoxProfile.set_preference("plugin.state.flash", 2)

        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')

        driver = webdriver.Firefox(executable_path=self.web_driver_path, firefox_profile=firefoxProfile,
                                   options=options)
        driver.implicitly_wait(60)
        self.driver = driver


    def get_web_driver(self):
        self.setting_option()

        return self.driver

    def crawl_page(self, driver, url, target_query):
        start = timeit.default_timer()

        driver.get(url)

        url_plain_text = driver.page_source
        bs_html = BeautifulSoup(url_plain_text, "lxml")  # 해당 텍스트를 해석 -> lxml? 구조화된 문서로 해석합니다.
        query_result_list = bs_html.select(target_query)

        result_link_list = []
        for link in query_result_list:
            result_link_list.append(link['href'])

        stop = timeit.default_timer()
        logging.info('parse lecture list time: %s', stop-start)

        return result_link_list

    def crawl_video_link_from_url(self, driver, video_a_tag_list):
        '''
        https://beomi.github.io/2017/10/29/HowToMakeWebCrawler-ImplicitWait-vs-ExplicitWait/
        WEBDRIVER until 기
        :param driver: 
        :param video_a_tag_list:
        :return:
        '''
        lecture_number = 0

        download_list = []
        print('# video link parse time')
        for lecture_link in video_a_tag_list:
            if lecture_number > 5 and self.debug is True:  # debug mode TODO: 디버그 이후 삭제
                break

            print('#LECTURE LINK-> ', lecture_link)
            # timeit 속도측정용
            start = timeit.default_timer()

            driver.get(lecture_link)

            # 해당엘리먼트가 로드되길 최대 120초까지 기다림
            urlencode_rtmp_src = ''
            try:
                eles = WebDriverWait(driver, 120).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'param[name=flashvars]'))
                )
                print('#ELES COUNT -> ', len(eles))
                for e in eles:
                    # print('#', e.get_attribute('value'))
                    urlencode_rtmp_src = e.get_attribute('value')
                    break

            except EnvironmentError:
                print('#####Until Error')

            # lecture_page_html = driver.page_source
            # parsed_lecture_page = BeautifulSoup(lecture_page_html, 'lxml')  # plain text -> lxml

            lecture_name = lecture_link.text.strip().replace(" ", "_").replace("/","_")  # 링크에서 윈도우 파일시스템 -> 파일명으로 불가능한 공백이나 슬래시 값들 대체 TODO: windows 파일 시스템 기준으로 이름, 및 문자인코딩 고려해서 수정하기.

            rtmp_src = self.decode_url_encoding(urlencode_rtmp_src)  # urlencode된 값 디코드하기

            print({"lecture_number": lecture_number,
                   "lecture_name": lecture_name,
                   "rtmp_download_src": rtmp_src})  # TODO: logging으로 변경하기.

            download_list.append(
                {"lecture_number": str(lecture_number),
                 "lecture_name": lecture_name,
                 "rtmp_download_src": rtmp_src}
            )  # 리스트에 저장하기. lecture_a_tag와 lecture_link관계 확인하기.
            lecture_number += 1

            # timeit
            stop = timeit.default_timer()

        return download_list



    def save_file_video_url_list(self, file_path, download_list):
        '''
        얻어온 강의 동영상 링크를 파일로 저장함.
        {"lecture_number": , "lecture_name": , "rtmp_download_src": }

        :param file_path:
        :param download_list:
        :return:
        '''

        with open(file_path, "w", encoding="utf-8") as fp:
            for element in download_list:
                fp.writelines(element["lecture_number"] + "_" + element["lecture_name"] + "," + element[
                    "rtmp_download_src"] + "\n")

        return 1

    @staticmethod
    def decode_url_encoding(original_str):
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
