import unittest
import subprocess
import multiprocessing
import multiprocessing as mp


def run(rtmpdump_path, option):
    print('call it')
    print(rtmpdump_path + option)
    # subprocess.call(["ls", "-l"])
    host = subprocess.check_output([rtmpdump_path, '-v', '-r', 'rtmp://vod2.snu.ac.kr/vod/_definst_/mp4:/vod2/1064/o-hss-071001-1_h.mp4', '-o', './hello'], stdin=subprocess.PIPE)
    print(host)
    print('end it')

def test_start():
    print('start')
    rtmpdump_path = "rtmpdump"
    cmd = ' -v -r rtmp://vod2.snu.ac.kr/vod/_definst_/mp4:/vod2/1064/o-hss-071001-1_h.mp4'
    # cmd = ' -v -r rtmp://vod2.snu.ac.kr/vod/_definst_/mp4:/vod2/1064/o-hss-071001-1_h.mp4 -o ./0_Introduction_to_OS_1'

    q = mp.Queue()
    q.put(cmd)
    p = mp.Process(target=run, args=(rtmpdump_path, cmd,))

    p.start()
    p.join()

test_start()