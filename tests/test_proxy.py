import os

from lib.crawling_url_list import CrawlingUrl

working_dir = os.getcwd()
default_driver_path = working_dir+'/geckodriver'
default_driver_file_path = default_driver_path+'/geckodriver'
default_config_path = working_dir+'/sample.yaml'


# def test_one():
#
#     print('#third')
#
#     target = 'http://snui.snu.ac.kr/ocw/index.php?mode=view&id=2937'
#     crawl = CrawlingUrl(web_driver_path=default_driver_file_path)
#     driver = crawl.get_web_driver_for_test()
#
#     result = crawl.get_parsed_html_page(driver, target, '#class_room div a')
#
#     for l in result:
#         lecture_link = l['href']
#         print(lecture_link)
#     # crawl.get_video_link(driver, result)


def test_proxy_two():
    import requests

    test_proxy = '206.189.234.211:80'
    # test_proxy = 'http://kproxyx.xyz/'

    proxies = {
        'http': test_proxy
    }

    # Create the session and set the proxies.
    s = requests.Session()
    s.proxies = proxies

    # Make the HTTP request through the session.
    r = s.get('http://www.naver.com/')

    # Check if the proxy was indeed used (the text should contain the proxy IP).
    print(r.text)
