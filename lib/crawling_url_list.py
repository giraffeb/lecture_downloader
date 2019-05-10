# -*- coding:utf-8 -*-

import logging

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

'''

'''


class CrawlingUrl:

    def __init__(self, file_path='./list.txt', char_encoding='utf-8', web_driver_path='', debug=False):

        self.debug = debug
        self.file_path = file_path;
        self.char_encoding = char_encoding;
        self.web_driver_path = web_driver_path

        self.default_lecture_url = 'http://snui.snu.ac.kr/ocw/index.php?mode=view&id=2937'

        # chrome config #
        # self.chrome_pref = {
        #     "profile.default_content_setting_values.plugins": 1,
        #     "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
        #     "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
        #               "PluginsAllowedForUrls": "http://snui.snu.ac.kr"
        # }

    '''
    강의링크를 가져와서 동영상 주소를 리스트로 반환하는 함수
    '''

    def get_web_driver(self):
        print('get_web_driver called')

        # Chrome config #
        # chrome_options = webdriver.ChromeOptions()
        #
        # chrome_options.add_argument("--disable-features=EnableEphemeralFlashPermission")
        # chrome_options.add_experimental_option("prefs", self.chrome_pref)
        # driver = webdriver.Chrome(executable_path=self.web_driver_path, chrome_options=chrome_options)

        firefoxProfile = FirefoxProfile()
        firefoxProfile.set_preference("plugin.state.flash", 2)

        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')

        ## Disable Flash
        # firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')

        driver = webdriver.Firefox(executable_path=self.web_driver_path, firefox_profile=firefoxProfile,
                                   options=options)

        driver.implicitly_wait(60)

        return driver

    def get_web_driver_for_test(self):
        from selenium.webdriver.common.proxy import Proxy, ProxyType
        print('get_web_driver called')

        # myProxy = 'http://kproxyx.xyz/'
        myProxy = '206.189.234.211:80'

        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': myProxy,
            'ftpProxy': myProxy,
            'sslProxy': myProxy,
            'noProxy': ''  # set this value as desired
        })


        firefoxProfile = FirefoxProfile()
        firefoxProfile.set_preference("plugin.state.flash", 2)

        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')

        driver = webdriver.Firefox(executable_path=self.web_driver_path, firefox_profile=firefoxProfile,
                                   options=options, proxy=myProxy)

        driver.implicitly_wait(120)

        return driver

    def get_parsed_html_page(self, driver, url, query):
        driver.get(url)

        url_plain_text = driver.page_source
        bs_html = BeautifulSoup(url_plain_text, "lxml")  # 해당 텍스트를 해석 -> lxml? 구조화된 문서로 해석합니다.
        query_result = bs_html.select(query)

        return query_result

    def get_video_link(self, driver, video_a_tag_list):
        import timeit
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
        for lecture_a_tag in video_a_tag_list:
            if lecture_number > 5 and debug is True :  # debug mode TODO: 디버그 이후 삭제
                break

            #timeit
            start = timeit.default_timer()

            lecture_link = lecture_a_tag['href']
            print('videoLink')
            # print("# : {0}".format(lecture_number) + " :: " + lecture_link)  # TODO: logging으로 변경하기.

            driver.get(lecture_link)

            # urlencode_rtmp_src = parsed_lecture_page.find('param', {'name': 'flashvars'})["value"] #동영상 주소 값
            urlencode_rtmp_src = ''
            try:
                eles = WebDriverWait(driver, 120).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'param[name=flashvars]'))
                )
                for e in eles:
                    # print('#', e.get_attribute('value'))
                    urlencode_rtmp_src = e.get_attribute('value')
                    break

            except EnvironmentError:
                print('#####Until Error')

            lecture_page_html = driver.page_source
            parsed_lecture_page = BeautifulSoup(lecture_page_html, 'lxml')  # plain text -> lxml

            rtmp_src = self.decode_url_encoding(urlencode_rtmp_src)  # urlencode된 값 디코드하기
            lecture_name = lecture_a_tag.text.strip().replace(" ", "_").replace("/",
                                                                                "_")  # 링크에서 윈도우 파일시스템 -> 파일명으로 불가능한 공백이나 슬래시 값들 대체 TODO: windows 파일 시스템 기준으로 이름, 및 문자인코딩 고려해서 수정하기.

            print({"lecture_number": lecture_number, "lecture_name": lecture_name,
                   "rtmp_download_src": rtmp_src})  # TODO: logging으로 변경하기.
            download_list.append({"lecture_number": str(lecture_number), "lecture_name": lecture_name,
                                  "rtmp_download_src": rtmp_src})  # 리스트에 저장하기. lecture_a_tag와 lecture_link관계 확인하기.
            lecture_number += 1

            #timeit
            stop = timeit.default_timer()
            print('SECOND -> ', stop - start)

        return download_list

    # 제외
    # def start_crawling(self, url):
    #
    #     if url == '' or url == None:
    #         print("default url -> ", self.default_lecture_url)
    #         url=self.default_lecture_url
    #
    #     driver = self.get_web_driver()
    #     lecture_a_tag_list = self.get_parsed_html_page(driver=driver,url=url, query='#class_room div a')
    #
    #     lecuture_list = self.get_video_link(driver, lecture_a_tag_list)
    #     self.write_url_list_to_file(file_path=self.file_path, download_list=lecuture_list)
    #     logging.debug('file writing complete')

    '''
    얻어온 강의 동영상 링크를 파일로 저장함.
    '''

    def write_url_list_to_file(self, file_path, download_list):
        '''
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

    '''
    urlencode된 값을 다시 원래 텍스트로 디코드합니다.
    '''

    def decode_url_encoding(self, original_str):
        from urllib.parse import urlsplit, parse_qs
        import urllib

        temp_str = urllib.parse.unquote(string=original_str, encoding='utf-8')  # urlencoding -> decoding
        query = urlsplit(temp_str).query  # url주소를 path, query 등으로 분리 query == parameters
        param = parse_qs(query)  # paramter단위로 분리 -> dict로 반환

        file = param.get("file")[0]
        stream = param.get("streamer")[0]

        return stream + file
