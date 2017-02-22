#

#TODO :rtms downloader 붙이기  :D


import urllib.parse
from bs4 import BeautifulSoup
from selenium import webdriver

print("######START TABLE SEARCHING ######")
target = input("snui url : ")

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get(target)


html = driver.page_source
soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')


index = 0
downloadList=[];
table = soup.find('table')


for atag in table.find_all('a'):


    print("# : {0}".format(index) +" :: " + atag['href'])
    index = index + 1
    driver.get(atag['href'])
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    player = soup.find('object', {'type': 'application/x-shockwave-flash'})
    src = soup.find('param', {'name': 'flashvars'})
    content = atag.text.strip().replace(u'\xa0', u' ').replace(" ", "_").replace("/","_")
    print(content)
    print(player["data"])
    print(src['value'])
    downloadList.append({"siteUrl": atag['href'], "contentName": content, "player": player["data"] , "flashvars": src['value']})

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
    str = stream+file+","+e.get("contentName")
    print(str)
    fd.write(str+'\n')

fd.close()



#
# # add http://www.nirsoft.net/utils/rtmp_dump_helper.html
# # rtms dump do
#
