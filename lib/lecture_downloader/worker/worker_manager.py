from concurrent.futures import ThreadPoolExecutor
from lib.lecture_downloader.worker.rtmp_dump_worker import RtmpDumpWorker

from queue import Queue
'''


'''
class JobManager:

    def __init__(self, size, save_dir) -> None:
        '''
        :param size: 스레드 풀 사이즈
        :param job_queue: 다운로드할 강의의 타이틀과 동영상 주소를 가지고 있는 job_queue thread safe함
        '''
        self.thread_pool_size = size
        self.thread_pool_executor = ThreadPoolExecutor(self.thread_pool_size) #Worker를 실행한 스레드 풀

        self.save_dir = save_dir

        self.job_queue: Queue = None
        self.worker = None


    def prepare_worker(self, job_queue):
        self.job_queue = job_queue
        self.worker = RtmpDumpWorker(job_queue=self.job_queue, save_dir=self.save_dir)

    def do_work(self):

        future_list = []

        for i in range(self.thread_pool_size):
            temp_future = self.thread_pool_executor.submit(self.worker.do_work)
            future_list.append(temp_future)

        for worker_future in future_list:
            worker_future.result()




