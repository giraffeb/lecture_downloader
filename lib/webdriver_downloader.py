import platform
import tarfile

import wget

import os


class WebDriverDownloader:

    def get_platform(self):
        sys_name = platform.system()
        print(sys_name)
        return sys_name

    def download_web_driver(self):

        working_dir = os.getcwd()
        default_driver_path = working_dir + '/geckodriver'


        gecko_path = '.geckodriver.tar.gz'
        down_path = ''
        sys_name = self.get_platform()

        if sys_name == 'Darwin': #macos
            down_path = 'https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-macos.tar.gz'
        elif sys_name == 'Linux':
            down_path = 'https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz'


        # linux version -> os 맞게 수정해야함.
        wget.download(
            down_path,
            out=gecko_path)

        tar = tarfile.open(gecko_path)
        tar.extractall(path=default_driver_path)
        tar.close()


