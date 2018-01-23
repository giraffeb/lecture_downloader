from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import lxml

class CrawlingUrl:

    def crawl_target_lecture(self, taret):
        '''
        // 
        https://chromium.googlesource.com/chromium/src/+/master/chrome/common/pref_names.cc
        질문해서 얻은 chrome profile preference json을 열어봐도 모르겠다.
        '''

        '''
        chrome에서 플래시를 사용하도록 설정을 허락한다.
        '''
        chrome_options = Options()
        prefs= {"profile.default_content_settings.state.flash": 1}
        prefs["profile.content_settings.plugin_whitelist.adobe-flash-player"] = 1
        prefs["profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player"] = 1

        # target = input("snui url : ")  # 해당 과목의 강의에 속하는 주소
        chrome_options.add_experimental_option("prefs", prefs)


        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        target = 'http://snui.snu.ac.kr/ocw/index.php?mode=view&id=2937'
        driver.get(target)

        lecture_page_html = driver.page_source
        bs_parsed_lecture_page = BeautifulSoup(lecture_page_html, "lxml")

        lecture_number = 0
        download_list = [];
        table = bs_parsed_lecture_page.find(attrs={"id":"class_room"})
        table = table.find('div')
        lecture_a_tag_list = table.find_all('a')


        for lecture_a_tag in lecture_a_tag_list:
            lecutre_link = lecture_a_tag['href']
            print("# : {0}".format(lecture_number) + " :: " + lecutre_link)

            driver.get(lecutre_link)
            lecture_page_html = driver.page_source
            bs_parsed_lecture_page = BeautifulSoup(lecture_page_html, 'lxml')

            urlencoded_rtmp_download_src = bs_parsed_lecture_page.find('param', {'name': 'flashvars'})["value"]
            rtmp_download_src = self.decode_url_encoding(urlencoded_rtmp_download_src)
            lecture_name = lecture_a_tag.text.strip().replace(" ", "_").replace("/", "_")

            print({"lecture_number" : lecture_number, "lecture_name": lecture_name, "rtmp_download_src": rtmp_download_src})
            download_list.append({"lecture_number" : str(lecture_number), "lecture_name": lecture_name, "rtmp_download_src": rtmp_download_src})
            lecture_number += 1


        return download_list


    def write_url_list_to_file(self,file_path, download_list):

        with open(file_path, "w", encoding="utf-8") as fp:
            for element in download_list:
                fp.writelines(element["lecture_number"]+"_"+element["lecture_name"] +","+element["rtmp_download_src"]+"\n")

        return 1

    def decode_url_encoding(self, original_str):
        from urllib.parse import urlsplit, parse_qs
        import urllib

        print(original_str)
        temp_str = urllib.parse.unquote(string = original_str, encoding='utf-8') #urlencoding -> decoding
        query = urlsplit(temp_str).query #url주소를 path, query 등으로 분리 query == parameters
        param = parse_qs(query) #paramter단위로 분리 -> dict로 반환

        file = param.get("file")[0]
        stream = param.get("streamer")[0]

        return stream+file
