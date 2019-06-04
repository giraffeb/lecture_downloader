# -*- coding:utf-8 -*-

import subprocess
import multiprocessing
import logging

'''
파일에 저장된 동영상링크 정보를 
다운로드 가능한 링크주소로 변환함.
'''
class RtmpDumpPrepare:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def load_lecture_url_from_file(self, lecture_urls_file_path):
        '''
        :param lecture_urls_file_path:
        :return:

        파일로 저장된 강의 동영상 값을 기준으로 다운로드 가능한 주소를 생성함.
        '''
        url_list = []
        with open(lecture_urls_file_path, "r", encoding="utf-8") as fp:
            for line in fp:
                splitted_line = line.rstrip().split(",")
                file_name = self.replace_windows_file_reserved_chracters(splitted_line[0])
                url_list.append({"url": splitted_line[1], "fileName": file_name})

        return url_list


    '''
    Multiprocessing.Manager().Queue() 객체에 파일에 미리 수집된 url주소를 입력함.
    '''
    def generate_process_queue(self, rtmpdump_path, objective_dir_path, lecture_urls):
        '''
        list: urlList에서 하나씩 꺼내서 Queue: urlQueue에 하나씩 담는 일만함.
        rtmp_dump프로그램 주소와 와 파라미터로 다운로드 링크를 넘김 저장해서 큐에 담아둠

        :param rtmpdump_path:
        :param objective_dir_path:
        :param lecture_urls_file_path:
        :return:
        '''
        rtmpdump_cmd_queue = multiprocessing.Manager().Queue()

        for lecture_url in lecture_urls:
            cmd = self.generate_rtmpdump_command(rtmpdump_path, lecture_url.get("url"), objective_dir_path, lecture_url.get("fileName"))
            rtmpdump_cmd_queue.put(cmd)

        return rtmpdump_cmd_queue


    def replace_windows_file_reserved_chracters(self, original_file_name):
        '''
        다운로드한 영상의 제목을 만듬 -> 윈도우 파일 시스템에서 사용 불가능한 부분 제거
        load_lecture_url_from_file에 사용됨
        :param original_file_name:
        :return:
        '''
        import re
        # limit = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]


        p = re.compile(r'[^ /?<>|\*\\:]')
        m = p.findall(original_file_name)

        new_file_name = ''.join(map(str,m))
        return new_file_name

    def generate_rtmpdump_command(self, rtmp_path, url, dir, filename):
        '''
        명령어에 필요한 옵션과 링크 주소를 보냄
        setUrlQueueFromFile에 사용됨.
        :param rtmp_path:
        :param url:
        :param dir:
        :param filename:
        :return:
        '''
        command = []
        live_option =  '-v'

        source_option = "-r"
        source_option_value = url

        object_option = "-o"
        object_option_value = dir + "/" + filename

        #순서가 중요합니다.
        command.append(rtmp_path)

        command.append(live_option)

        command.append(source_option)
        command.append(source_option_value)

        command.append(object_option)
        command.append(object_option_value)


        return command

    def download_start(self, lecture_job_queue):

        '''
        process에 의해서 실행되는 함수
        :param lecture_job_queue: 
        :return: 
        '''

        while lecture_job_queue.empty() == False:
            cmd = lecture_job_queue.get()
            print(cmd)
            host = subprocess.call(cmd, stdin=subprocess.PIPE)
        return host.returncode

