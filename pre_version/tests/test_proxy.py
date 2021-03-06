import os

working_dir = os.getcwd()
default_driver_path = working_dir+'/geckodriver'
default_driver_file_path = default_driver_path+'/geckodriver'
default_config_path = working_dir+'/logger.yaml'


# def test_one():
#
#     print('#third')
#
#     target = 'http://snui.snu.ac.kr/ocw/index.php?mode=view&id=2937'
#     crawler = CrawlingUrl(web_driver_path=default_driver_file_path)
#     driver = crawler.get_web_driver_for_test()
#
#     result = crawler.get_parsed_html_page(driver, target, '#class_room div a')
#
#     for l in result:
#         lecture_link = l['href']
#         print(lecture_link)
#     crawler.get_video_link(driver, result)


def test_proxy_two():
    print("TEST2")
    import requests
    import timeit


    test_proxy = '206.189.234.211:80'
    # test_proxy = 'http://kproxyx.xyz/'

    proxies = {
        'http': test_proxy
    }

    # Create the session and set the proxies.
    s = requests.Session()
    s.proxies = proxies

    # Make the HTTP request through the session.
    # 시작부분 코드

    start = timeit.default_timer()
    url = 'http://snui.snu.ac.kr/main/css/NanumGothic.woff'
    r = s.get(url)
    stop = timeit.default_timer()
    print('SECOND -> ',stop - start)

    # Check if the proxy was indeed used (the text should contain the proxy IP).
    # print(r.text)

def test_proxy_three():
    print("TEST3")
    import requests
    import timeit

    # Create the session and set the proxies.
    s = requests.Session()

    # Make the HTTP request through the session.
    # 시작부분 코드

    start = timeit.default_timer()
    url = 'http://snui.snu.ac.kr/main/css/NanumGothic.woff'
    r = s.get(url)
    stop = timeit.default_timer()
    print('SECOND -> ', stop - start)

    # Check if the proxy was indeed used (the text should contain the proxy IP).
    # print(r.text)
