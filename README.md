[![Build Status](https://travis-ci.org/giraffeb/lecture_downloader.svg?branch=master)](https://travis-ci.org/giraffeb/lecture_downloader)
# lecture_downloader

### Pycharm project upload.<br>

#### 19-04-23 변경점
사용시스템을 맥으로 변경하면서 수정해봄<br>
윈도우에서 사용시에는 코드 변경이 필요함<br>
* mac os 10.14.3
* rtmpdump v2.4 --> brew install rtmpdump
* firefox v66.0.3
* geckodriver v0.24.0

### 필요한 Python 라이브러리
    1) BeautifulSoup4
    2) selenium
    3) lxml
    4) gecko WebDriver
    5) firefox
    6) adobe flash
    ** python3가 먼저 설치 되어 있어야합니다.

### 패치노트

    1) windows filename limit
    윈도우 파일시스템에서 이름으로 제한되는 문자들을 제거하는 부분 추가함
    [\, /, :, *, ?, ", <, >, |]



### 프로그램 구성
    start.py 실행

    1) start.py
       프로그램 실행


### 라이브러리 설치(r)
    python에 내장된 pip를 이용해서 다운로드함

    1) pip install -r requirements.txt
    
    2) chrome driver download
    https://sites.google.com/a/chromium.org/chromedriver/downloads
    운영체제에 맞는 것을 선택해서
    프로그램이 있는 폴더에 풀어주세요.
