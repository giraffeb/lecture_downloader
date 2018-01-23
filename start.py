# -*- coding:utf-8 -*-
from multiprocessing import Process
from rtmpdumcall import RtmpDumpCall
from crawling_url_list import CrawlingUrl


def main():
    default_file_path = "./list.txt"
    default_process_number = 4

    target_lecture_link = ""

    print("######START TABLE SEARCHING ######")
    target_lecture_link = input("snui url : ")  # 해당 과목의 강의에 속하는 주소


    crawl = CrawlingUrl()
    download_list = crawl.crawl_target_lecture(taret=target_lecture_link)
    crawl.write_url_list_to_file(default_file_path, download_list)

    print("######RTMP DUMP CALL######")
    dir = input("download dir : (default -> current directory)")
    np = input("number of process(default : 1, MAX :4) :")

    numberOfProcess = 0
    if np == "":
        numberOfProcess = default_process_number
    elif int(np) > 4:
        numberOfProcess = 4


    if dir == "":
        dir = "./"

    print('dir : %s'%dir)
    print('number of process : %d'%numberOfProcess)

    rtmp = RtmpDumpCall()
    rtmp_path = "./rtmpdump-2.3/rtmpdump.exe -v "
    down_list = rtmp.makeUrlListFromFile(default_file_path)

    urlQueue = rtmp.setUrlQueueFromFile(rtmp_path, dir, down_list)

    processList =[]
    for i in range(numberOfProcess):
        p = Process(target=rtmp.downloadVideoWithMultiProcess, args=(urlQueue, ))
        # p = DownloadProcess(urlQueue, i)
        p.start()
        processList.append(p)

    for p in processList:
        p.join()


if __name__ == "__main__":
    main()