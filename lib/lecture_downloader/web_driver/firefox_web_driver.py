import os
import os.path
import tarfile
import platform

import wget

import logging

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

'''
    크롤링에 필요한 파이어폭스 웹드라이버(gecko)를
    #1. OS에 맞게 다운로드 합니다.
    #2. 크롤링에 필요한 설정을 주입합니다.
    #3. 드라이버를 반환합니다.
    '''
class FirefoxWebDriverBuilder:

    def __init__(self):
        self.driver = None

        self.current_dir = os.getcwd()

        self.default_web_driver_download_file_name = self.current_dir + '/geckodriver.tar.gz'
        self.default_web_driver_dir = self.current_dir+'/gecko_web_driver_dir'
        self.default_web_driver_file_name = self.default_web_driver_dir+'/geckodriver'

        self.web_driver_download_url = {'macOS': 'https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-macos.tar.gz'
                                       ,'linux': 'https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz'}

        self.firefox_profile = FirefoxProfile()
        self.firefox_options = webdriver.FirefoxOptions()
        self.implicitly_wait_time = 60 #default

    def __is_exist_web_driver(self) -> bool:
        '''
        webdriver를 이미 다운로드했는지 체크.
        :return:
        '''
        flag = os.path.isfile(self.default_web_driver_file_name)
        return flag

    def __download_web_driver(self):
        '''
        Firefox geckodriver를 OS에 맡게 다운로드합니다.
        :return:
        '''
        if self.__is_exist_web_driver() is True:
            return
        else:
            os_type = platform.system()
            downpath = ''

            if os_type == 'Darwin':  # macos
                downpath = self.web_driver_download_url.get('macOS')
            elif os_type == 'Linux':
                downpath = self.web_driver_download_url.get('linux')

            #1. webdriver 압축파일 받음
            wget.download(downpath,
                            out=self.default_web_driver_download_file_name)
            #2. 압축파일 읽기
            tar = tarfile.open(self.default_web_driver_download_file_name)
            #3. 압축파일 압축해제 -> path지정
            tar.extractall(path=self.default_web_driver_dir)
            tar.close()

    def __default_setting_web_driver(self):
        '''
        FireFox Webdriver 플래시, 헤드리스 등 옵션 설정합니다.
        :return:
        '''
        #1. flash 허용
        self.firefox_profile.set_preference("plugin.state.flash", 2)

        #2. headless 모드 설정
        self.firefox_options.add_argument('-headless')

    def set_default_options(self):
        self.__is_exist_web_driver()
        self.__download_web_driver()
        self.__default_setting_web_driver()

        return self

    def build(self):
        '''
        사용자가 호출하기될 최종적인 메소드
        :return:
        '''

        #1. profile, options적용 webdriver 객체생성
        driver = webdriver.Firefox(executable_path=self.default_web_driver_file_name,
                                   firefox_profile=self.firefox_profile,
                                   options=self.firefox_options)
        #2. 암시적 대기시간 설정.
        driver.implicitly_wait(self.implicitly_wait_time)
        self.driver = driver

        return self.driver
