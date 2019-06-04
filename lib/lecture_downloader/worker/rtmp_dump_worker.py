import subprocess
from queue import Queue

class RtmpDumpWorker:

    def __init__(self, job_queue, save_dir) -> None:
        self.file_path=''
        self.options = []
        self.video_dir = 'video'

        self.rtmp_dump_path = None
        self.command = None

        self.live_option = '-v'
        self.source_option = '-r'
        self.object_option = '-o'
        self.save_dir = save_dir

        self.job_queue: Queue = job_queue

    def do_work(self):

        #1. rtmpdump path가져오기
        self.config_rtmpdump()
        #2. 영상 링크를 큐에서 가져옴.
        #2. jobqueue가 완료될때 까지 수행
        self.getting_job_and_work()

    def config_rtmpdump(self):
        import platform
        import os

        if os.path.isdir(self.save_dir) is not True:
            os.mkdir(self.save_dir, 0o777)

        if platform.system() == "Darwin": #macOS
            self.rtmp_dump_path = 'rtmpdump' #brew install path에 등록된 상태기준



    def getting_job_and_work(self):
        '''
        큐가 모두 빌때까지
        큐에서 링크를 가져와서 서브프로세스로 RTMPDUMP를 실행함.
        :return:
        '''
        proc = None
        while self.job_queue.empty() is not True:
                lecture_url = self.job_queue.get()
                proc = self.rtmpdump_call(lecture_url)
                proc.wait()



    def rtmpdump_call(self, lecture_url):

        rtmp_path = self.rtmp_dump_path

        filename = lecture_url['title']
        url = lecture_url['video']

        command = []
        live_option = '-v'

        source_option = "-r"
        source_option_value = url

        object_option = "-o"
        object_option_value = self.save_dir+"/" + filename

        # 순서가 중요합니다.
        command.append(rtmp_path)

        command.append(live_option)

        command.append(source_option)
        command.append(source_option_value)

        command.append(object_option)
        command.append(object_option_value)

        # subprocess.call(cmd)
        return subprocess.call(command, stdout=subprocess.PIPE)


