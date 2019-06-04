from lib.lecture_downloader.downloader.video_downloader import VideoDownloader
from lib.lecture_downloader.crawler.lecture_crawler import LectureCrawler

'''
강의 다운로드의 객체입니다.
크롤러와 다운로더, 설정파일을 가집니다.
'''
class LectureDownloader:
    def __init__(self, crawler, downloader) -> None:
        self.crawler: LectureCrawler = crawler
        self.downloader: VideoDownloader = downloader
        self.config = None

    def crawl(self) -> None:
        self.crawler.do_crawling()

    def download(self) -> None:
        self.downloader.do_download()

    def start(self) -> None:
        '''
        크롤링 후 다운로드를 실행합니다.
        :return:
        '''
        self.crawl()
        self.download()
