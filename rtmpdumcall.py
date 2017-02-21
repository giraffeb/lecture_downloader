import io
import os
from multiprocessing import Process, Queue
import subprocess
import logging


def getUrlList(urlList):
    fd = open("list.txt","r")
    ptr=0
    strl= ""
    fdend = fd.seek(0,io.SEEK_END)
    fd.seek(0,io.SEEK_SET)
    index=0
    # print(fdend)

    while fd.tell() < fdend :
        strl = fd.readline()
        strl = strl.replace("\n", "")
        urlList.append(strl)
        # print(strl)
        # print(fd.tell())

        index + 1
    fd.close()
    # str2 = "rtmp://vod2.snu.ac.kr/vod/_definst_/mp4:/vod2/1120/o-hss-071024-2_h.mp4"
    # host = subprocess.Popen("./rtmpdump-2.3/rtmpdump.exe -v -r "+str2+" -o 0", stdout=subprocess.PIPE).communicate()
    # print(host[0] + host[1])




def downloadVideo(command, url, filename):
    print(url)
    url=" -r" + url
    filename = " -o "+filename
    parameter = command + url + filename
    host = subprocess.Popen(parameter)
    print(host.communicate())




if __name__=='__main__':
    urlList = []

    getUrlList(urlList)
    urlListIndex=0


    # index=0
    # for el in urlList:
    #     print(str(index) +" "+ el)
    #     index += 1

    command = "./rtmpdump-2.3/rtmpdump.exe -v"
    url=""
    filename=""
    processes = []
    endFlag = False

    for i in range(0, 4):
        if urlListIndex < len(urlList):
            temp = Process(target=downloadVideo, args=(command, urlList[urlListIndex], str(urlListIndex)))
            processes.append(temp)
            urlListIndex += 1
            temp.start()


    while endFlag == False :


        for p in processes:
            p.join()
            if p.is_alive() == False and urlListIndex < len(urlList):
                temp = Process(target=downloadVideo, args=(command, urlList[urlListIndex], filename))
                processes.append(temp)
                urlListIndex += 1
                temp.start()
                continue

        if urlListIndex == len(urlList):
            endFlag = True


    #
    # while(True):
    #
    #     for p in processes:
    #         if p.is_alive() == False:
    #             p.start()
    #
    #     for p in processes:
    #         p.join()
    #
    #     if urlListIndex < len(urlList):
    #         for p in processes:
    #             if p.is_alive() == False:
    #                 p = Process(target=downloadVideo, args=(command, urlList[urlListIndex], filename))
    #                 urlListIndex += 1
    #     elif urlListIndex == len(urlList) :
    #         break


    print("end")
