# lecture_downloader

###Pycharm project upload.<br>
windows 8환경에서 테스트 되었습니다.<br>
내부에서 rtmpdump를 사용합니다.<br>
python3.X 버전을 사용했습니다<br>

### 필요한 Python 라이브러리
    1) BeautifulSoup4
    2) selenium
    3) lxml
    4) chromeDriver
    ** python3가 먼저 설치 되어 있어야합니다.

### 패치노트

    1) windows filename limit
    윈도우 파일시스템에서 이름으로 제한되는 문자들을 제거하는 부분 추가함
    [\, /, :, *, ?, ", <, >, |]



### 프로그램 구성
    crawlingUrlList.py 실행 후 -> rtmpdumcall.py 실행

    1) crawlingUrlList.py
        snui의 열린강좌의 url에 접근해서 해당 강좌의 url리스트를 가져옴

    2) rtmpdumcall.py
        crawlingUrlList.py실행 후 list.txt가 생성되면, 저장된 url을 접근해서 다운로드함.
        저장 디렉토리 지정, 다운로드 프로세스 수 지정 가능


### 라이브러리 설치
    python에 내장된 pip를 이용해서 다운로드함

    1) pip로 python lib설치
    ```
        $> pip install beautiful4
        $> pip install selenium
        $> pip install lxml
    ```

    2) chrome driver download
    https://sites.google.com/a/chromium.org/chromedriver/downloads
    운영체제에 맞는 것을 선택해서
    프로그램이 있는 폴더에 풀어주세요.
