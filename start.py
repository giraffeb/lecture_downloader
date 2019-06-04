from lib.lecture_downloader.lecture_downloader import LectureDownloader
from lib.lecture_downloader.web_driver.web_driver_factory import WebDriverFactory
from lib.lecture_downloader.file_writer.file_writer import FileWriter
from lib.lecture_downloader.crawler.lecture_crawler import LectureCrawler
from lib.lecture_downloader.downloader.video_downloader import VideoDownloader
from lib.lecture_downloader.worker.worker_manager import JobManager

import yaml

def load_config(path):
    config_file = open(path, "r")
    config_object = yaml.load(config_file, Loader=yaml.FullLoader)

    return config_object

def main():

    config = load_config('config/config.yaml')

    thread_pool_size = config['job_manager']['thread_pool_size']
    save_dir = config['job_manager']['save_dir']

    lecture_page_list_query = config['crawler']['lecture_page_list_query']
    lecture_video_query = config['crawler']['lecture_video_query']

    web_driver = WebDriverFactory.create_web_driver(web_driver_type='firefox')
    file_writer = FileWriter(lecture_link_file='list.txt')

    job_manager = JobManager(size=thread_pool_size, save_dir=save_dir)

    lecture_crawler = LectureCrawler(target_webdriver=web_driver
                                     , target_file_writer=file_writer
                                     , lecture_page_list_query=lecture_page_list_query
                                     , lecture_video_query=lecture_video_query)

    rtmp_downloader = VideoDownloader(file_writer=file_writer, job_manager=job_manager)

    lecture_downloader = LectureDownloader(crawler=lecture_crawler, downloader=rtmp_downloader)

    lecture_downloader.start()

if __name__ == "__main__":
    main()