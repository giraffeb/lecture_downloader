from multiprocessing import Process
import io
import subprocess
import multiprocessing

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
        urlList.put({"url":parts[0], "fileName":parts[1]})
        index + 1
    fd.close()


def downloadVideo(command, dir, urlList):
    while True:
        item = urlList.get()
        if item is None:
            break
        print(item.get("url"))
        print(item.get("fileName"))

        filename = dir + "\\" + item.get("fileName")
        url = item.get("url")
        url=" -r" + url
        filename = " -o " + filename
        parameter = command + url + filename
        host = subprocess.run(parameter, stdin=subprocess.PIPE, check=True)
    return host.returncode

if __name__ == '__main__':

    dir = input("download dir : ")
    np = input("number of process(default : 1, MAX :4) :")

    numberOfProcess = 0
    if np == "":
        numberOfProcess = 1
    if int(np) > 4:
        numberOfProcess = 4
    numberOfProcess = int(np)

    urlList = multiprocessing.Queue()

    command = "./rtmpdump-2.3/rtmpdump.exe -v "
    getUrlList(urlList)
    urlListIndex = 0

    processList =[]
    # while urlListIndex <= urlList.maxsize:
    for i in range(numberOfProcess):
        p = Process(target=downloadVideo, args=(command, dir, urlList))
        processList.append(p)
        p.start()

    for p in processList:
        p.join()

