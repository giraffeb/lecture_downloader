# -*- coding:utf-8 -*-
import logging
import logging.config
import multiprocessing as mp

from crawling_url_list import CrawlingUrl
from myLogger import MyLoggerConfig
from rtmpdumcall import RtmpDumpPrepare

'''
서로 호출하는 것만 만들어 놓아야겠다.
'''



'''
메인에는 단순하게 로직만 넣기.

'''

default_file_path = "./list.txt"
default_process_number = 4
default_dir_path = '.'
default_web_driver_path = './geckodriver'

#rtmpdump_path = "./rtmpdump-2-2.3/rtmpdump "
rtmpdump_path = "rtmpdump"
default_number_of_process = 4
max_number_of_process = 4


def crawling_procedure(debug_flag):
    logging.info('##crawling Start')
    logging.info('## 강의 모든 링크를 수집하기위해 강의 url을 입력해주세요.')
    target_lecture_link = input("snui url : ")  # 해당 과목의 강의에 속하는 주소


    crawl = CrawlingUrl(web_driver_path=default_web_driver_path, file_path=default_file_path, debug=debug_flag)#객체 생성
    crawl.start_crawling(url=target_lecture_link) #list.txt생성


def video_download_procedure():
    logging.info("##video download Start")

    object_dir = input("저장할 디렉토리 : (기본값 = 현재 디렉토리)")
    number_of_process = input("다중다운로드 수(기본값 : {}, 최대 :{}) :".format(default_number_of_process, max_number_of_process))

    if number_of_process == '':
        number_of_process = default_process_number
    elif int(number_of_process) > max_number_of_process:
        number_of_process = max_number_of_process

    if object_dir == '':
        object_dir = default_dir_path


    logging.info('dir : %s' % object_dir)
    logging.info('number of process : %d' % default_number_of_process)

    rtmp_prepare = RtmpDumpPrepare()
    down_list = rtmp_prepare.load_lecture_url_from_file(default_file_path)

    rtmpdump_cmd_queue = rtmp_prepare.generate_process_queue(rtmpdump_path, object_dir, down_list)

    processList = []

    for i in range(number_of_process):
        cur_process = mp.Process(target=rtmp_prepare.download_start, args=(rtmpdump_cmd_queue,))
        # p = DownloadProcess(urlQueue, i)
        cur_process.start()
        processList.append(cur_process)

    for p in processList:
        p.join()


def main():
    my_logger = MyLoggerConfig()
    my_logger.yaml_config_loader()
    logging.config.dictConfig(my_logger.get_myLogger_config())

    #1 크롤링하기
    crawling_procedure(debug_flag=True)
    #2 다운로드하기
    video_download_procedure()

if __name__ == "__main__":
    main()