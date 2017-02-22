from multiprocessing import Pool
import io
import subprocess


def f(x):
    return x*x



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
        print(strl)
        strl = strl.replace("\n", "")
        parts = strl.split(",")
        urlList.append({"url":parts[0], "fileName":parts[1]})
        index + 1
    fd.close()

def downloadVideo(command, url, filename):
    print(url)
    print(filename)
    url=" -r" + url
    filename = " -o " + filename
    parameter = command + url + filename
    host = subprocess.Popen(parameter)
    print(host.communicate())

if __name__ == '__main__':

    dir = input("download dir : ")
    np = input("number of process(default : 1, MAX :4) :")

    numberOfProcess = 0
    if np == "":
        numberOfProcess = 1
    if int(np) > 4:
        numberOfProcess = 4
    numberOfProcess = int(np)

    urlList = []

    command = "./rtmpdump-2.3/rtmpdump.exe -v"
    getUrlList(urlList)
    urlListIndex = 0

    while urlListIndex <= len(urlList):
        pool = Pool(processes=numberOfProcess)
        for i in range(numberOfProcess):
            if urlListIndex <= len(urlList):
                print(urlList[urlListIndex].get("url"))
                print(urlList[urlListIndex].get("fileNAme"))
                filename = dir+"\\"+urlList[urlListIndex].get("fileName")
                url = urlList[urlListIndex].get("url")
                res = pool.apply_async(downloadVideo, (command, url, filename))
                urlListIndex += 1
        pool.close()
        pool.join()
