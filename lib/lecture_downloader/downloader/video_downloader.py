from lib.lecture_downloader.file_writer.file_writer import FileWriter
from lib.lecture_downloader.worker.worker_manager import JobManager

from queue import Queue


class VideoDownloader:

    def __init__(self, file_writer, job_manager) -> None:

        self.file_writer = file_writer
        self.job_queue = Queue()
        self.job_manager: JobManager= job_manager
        self.job_manager.job_queque = self.job_queue


    def do_download(self):

        #1. 파일에서 강의 리스트 읽어오기.
        self.load_lecture_list()
        #2. 읽어온 내용을 JOB으로 만들기
        self.job_making()
        #3. worker에 준비하기
        self.job_manager.prepare_worker(self.job_queue)
        #4. woker할당하기
        self.job_manager.do_work()


    def load_lecture_list(self):
        self.file_writer.load_file()

    def job_making(self):
        for row in self.file_writer.lecture_url_list:
            self.job_queue.put(row)








