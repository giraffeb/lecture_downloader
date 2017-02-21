#

#TODO :rtms downloader 붙이기  :D


import urllib.parse
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('http://snui.snu.ac.kr/ocw/index.php?mode=view&id=626')


html = driver.page_source
soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')


index = 0
downloadList=[];
table = soup.find('table')
print("######START TABLE SEARCHING ######")
for atag in table.find_all('a'):


    print("# : {0}".format(index) +" :: " + atag['href'])
    index = index + 1
    driver.get(atag['href'])
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    player = soup.find('object', {'type': 'application/x-shockwave-flash'})
    src = soup.find('param', {'name': 'flashvars'})
    print(player["data"])
    print(src['value'])
    downloadList.append({"siteUrl": atag['href'], "player": player["data"] , "flashvars": src['value']})

dicList=[{}]
str = ""
file=""
stream=""
fd=open("list.txt","w")

for e in downloadList:
    temp = urllib.parse.unquote(e.get('flashvars'))
    el = temp.split("&")
    str = ""
    for p in el:
        newe = p.split("=")
        dicList.append({newe[0] : newe[1]})

        for de in dicList:
            if de.get("file"):
               file = de.get("file")
            elif de.get('streamer'):
                stream = de.get('streamer')
    str = stream+file
    print(str)
    fd.write(str+'\n')

fd.close()



#
# # add http://www.nirsoft.net/utils/rtmp_dump_helper.html
# # rtms dump do
#
