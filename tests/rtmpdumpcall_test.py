import unittest
from lib.rtmpdumpcall import RtmpDumpPrepare
import logging

class rtmpdumpTest(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    def test_makeUrlListFromFile(self):
        print('')
        # logging.basicConfig(level=logging.DEBUG)
        logging.debug('test_makeUrlListFromFile')

        rtmp = RtmpDumpPrepare()
        list = rtmp.load_lecture_url_from_file('./list.txt')
        print(*list, sep='\n')


    def test_replace_windows_file_reserved_chracters(self):
        print('윈도우 파일시스템 이름 규칙 테스트')

        logging.debug('test_replace_windows_file_reserved_chracters')
        rtmp = RtmpDumpPrepare()
        list = rtmp.load_lecture_url_from_file('./list.txt')

        for line in list:
            file_name = rtmp.replace_windows_file_reserved_chracters(line['fileName'])
            print(file_name)


    def test_generate_rtmp_command(self):
        print('명령어 생성 테스트')
        logging.debug('test_generate_rtmp_command call')
        rtmp = RtmpDumpPrepare()
        #self, rtmp_path, url, dir, filename):

        list = rtmp.load_lecture_url_from_file('./list.txt')

        for line in list:
            file_name = rtmp.replace_windows_file_reserved_chracters(line['fileName'])
            url = rtmp.replace_windows_file_reserved_chracters(line['url'])
            cmd = rtmp.generate_rtmpdump_command(rtmp_path='rtmpdump_path', url=url, dir='/virtual/', filename=file_name)
            print('#command string# "',cmd,'"')


    def test_setUrlQueueFromFile(self):
        print('멀티큐 생성 ')
        rtmp = RtmpDumpPrepare()
        list = rtmp.load_lecture_url_from_file('./list.txt')
        #def setUrlQueueFromFile(self, rtmp_path, dir, urlList):
        resultList = rtmp.generate_process_queue(rtmpdump_path='rtmpdump_path', objective_dir_path='/virtual', lecture_urls_file_path=list)

        while resultList.qsize() > 0:
            print(resultList.get())




