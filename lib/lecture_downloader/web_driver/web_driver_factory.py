from lib.lecture_downloader.web_driver.firefox_web_driver import FirefoxWebDriverBuilder

class WebDriverFactory:
    @staticmethod
    def create_web_driver(web_driver_type):

        if web_driver_type == 'firefox':
            return FirefoxWebDriverBuilder().set_default_options().build()
        else:
            raise ValueError("지원되지 않는 웹드라이버 입니다.")
