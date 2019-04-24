# -*- coding:utf-8 -*-

import logging
import os
import pytest

from lib.rtmpdumpcall import RtmpDumpPrepare

logging.basicConfig(level=logging.DEBUG)
cwd = os.getcwd()
sample_file_path = cwd + '/tests/' + 'list.txt'


def test_file_path():

    cwd = os.getcwd()  # Get the current working directory (cwd)
    files = os.listdir(cwd)  # Get all the files in that directory

    print("Files in '%s': %s" % (cwd, files))

def test_load_lecture_url_from_file():
    # logging.basicConfig(level=logging.DEBUG)
    logging.debug('test_test_load_lecture_url_from_file')

    rtmp = RtmpDumpPrepare()
    list = rtmp.load_lecture_url_from_file(sample_file_path)
    # print(*list, sep='\n')


def test_replace_windows_file_reserved_chracters():
    print('윈도우 파일시스템 이름 규칙 테스트')

    logging.debug('test_replace_windows_file_reserved_chracters')
    rtmp = RtmpDumpPrepare()
    list = rtmp.load_lecture_url_from_file(sample_file_path)

    for line in list:
        file_name = rtmp.replace_windows_file_reserved_chracters(line['fileName'])
        print(file_name)


def test_generate_rtmp_command():
    print('명령어 생성 테스트')

    logging.debug('test_generate_rtmp_command call')
    rtmp = RtmpDumpPrepare()
    #, rtmp_path, url, dir, filename):

    list = rtmp.load_lecture_url_from_file(sample_file_path)

    for line in list:
        file_name = rtmp.replace_windows_file_reserved_chracters(line['fileName'])
        url = rtmp.replace_windows_file_reserved_chracters(line['url'])
        cmd = rtmp.generate_rtmpdump_command(rtmp_path='rtmpdump_path', url=url, dir='/virtual/', filename=file_name)
        print('#command string# "',cmd,'"')


def test_setUrlQueueFromFile():
    print('멀티큐 생성 ')

    rtmp = RtmpDumpPrepare()
    list = rtmp.load_lecture_url_from_file(sample_file_path)
    #def setUrlQueueFromFile(self, rtmp_path, dir, urlList):
    resultList = rtmp.generate_process_queue(rtmpdump_path='rtmpdump_path', objective_dir_path='/virtual', lecture_urls=list)

    while resultList.qsize() > 0:
        print(resultList.get())
