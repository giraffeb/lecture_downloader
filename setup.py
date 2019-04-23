from setuptools import setup, find_packages

setup(
    name = 'lectuure_downloader',
    version = '0.1',
    description = '서울대학교 열린강좌 영상 다운로더',
    author = 'giraffeb',
    author_email = 'rwpark07@gmail.com',
    url = 'https://github.com/giraffeb/lecture_downloader',
    install_requires = [],
    script = 'start.py',
    packages = find_packages(exclude = []),
    python_requires = '>=3',
    classifier = [
        'Programming Language :: Python :: 3.7'
    ]
)