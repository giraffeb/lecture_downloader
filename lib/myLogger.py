# -*- coding:utf-8 -*-

import yaml


class MyLoggerConfig:
    def __init__(self):
        self.my_logger_config = {}


    def yaml_config_loader(self, fila_path='./sample.yaml'):
        with open(fila_path, 'r') as f:
            self.my_logger_config = yaml.safe_load(f.read())

    def get_myLogger_config(self):
        return self.my_logger_config


