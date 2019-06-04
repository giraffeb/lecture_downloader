import pytest

import yaml
import json


default_config_data = json.loads('{"file_writer": {"file_path": "list.txt"}, "web_driver": {"type": "firefox"}, "job_manager": {"thread_pool_size": 4, "save_dir": "video"}, "worker": {"rtmp_path": "rtmpdump"}, "crawler": {"lecture_page_list_query": "#class_room div a", "lecture_video_query": "param[name=flashvars]"}}')
default_config_path = 'config/config.yaml'


def test_config_column():

    config = None
    with open(default_config_path, 'r') as f:
        config = yaml.load(f)

    config_list = list(config)
    default_config_data_list = list(default_config_data)

    for i in range(len(config_list)):
        print( default_config_data_list[i] +' :: '+ config_list[i])
        assert default_config_data_list[i] == config_list[i]



def test_config_column_value():

    config = None
    with open(default_config_path, 'r') as f:
        config = yaml.load(f)

    for column_name in default_config_data:
        config_list = list(config[column_name])
        default_config_data_list = list(default_config_data[column_name])
        print('#COLUMN NAME : '+column_name)
        for i in range(len(config_list)):
            print('##COMPARE ',config_list[i], ' -> ', config[column_name][config_list[i]], default_config_data[column_name][default_config_data_list[i]])
            assert config[column_name][config_list[i]] == default_config_data[column_name][default_config_data_list[i]]