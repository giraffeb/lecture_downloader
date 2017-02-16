#

#TODO :rtms downloader 붙이기  :D



import requests
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('http://snui.snu.ac.kr/ocw/index.php?mode=view&id=626')


html = driver.page_source
soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')


index = 0
table = soup.find('table')
print("######START TABLE SEARCHING ######")
for atag in table.find_all('a'):

    print("# : {0}".format(index) +" :: " + atag['href'])
    index = index + 1
    driver.get(atag['href'])
    player = soup.find('object', {'type': 'application/x-shockwave-flash'})
    src = soup.find('param', {'name': 'flashvars'})
    print(player["data"])
    print(src['value'])

# add http://www.nirsoft.net/utils/rtmp_dump_helper.html
# rtms dump do

