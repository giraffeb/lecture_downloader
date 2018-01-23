# -*- coding:utf-8 -*-

import subprocess
import multiprocessing

class RtmpDumpCall:

    def makeUrlListFromFile(self, file_path):
        '''
        :param file_path:
        :return:

        미리 수집된 url_text가 저장된 파일에서 하나씩 꺼내서 list로 반환함.
        '''
        url_list = []
        with open(file_path, "r", encoding="utf-8") as fp:
            for line in fp:
                splitted_line = line.rstrip().split(",")
                file_name = self.replace_windows_file_reserved_chracters(splitted_line[0])
                url_list.append({"url": splitted_line[1], "fileName": file_name})

        return url_list



    '''
    Multiprocessing.Manager().Queue() 객체에 파일에 미리 수집된 url주소를 입력함.
    '''
    def setUrlQueueFromFile(self, rtmp_path, dir, urlList):
        '''
        :param urlList:
        :param urlQueue:
        :return:

        list: urlList에서 하나씩 꺼내서 Queue: urlQueue에 하나씩 담는 일만함.
        이후 변경에 대응해서 분리
        '''
        urlQueue = multiprocessing.Manager().Queue()
        for url in urlList:
            cmd = self.generate_rtmp_command(rtmp_path, url.get("url"), dir, url.get("fileName") )
            urlQueue.put(cmd)

        return urlQueue

    def replace_windows_file_reserved_chracters(self, original_file_name):
        import re
        # limit = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]


        p = re.compile(r'[^ /?<>|\*\\:]')
        m = p.findall(original_file_name)

        new_file_name = ''.join(map(str,m))
        return new_file_name

    def generate_rtmp_command(self, rtmp_path, url, dir, filename):
        new_url = " -o " + url
        new_filename = " -r" + dir + "/" + filename

        command = rtmp_path + new_url + new_filename

        return command

    def downloadVideoWithMultiProcess(self, urlQueue):
        while urlQueue.empty() == False:
            cmd = urlQueue.get()


            host = subprocess.run(cmd, stdin=subprocess.PIPE, check=True)
        return host.returncode

