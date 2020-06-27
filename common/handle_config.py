#!D:/PychramCode
# -*- coding: utf-8 -*-
# @Time : 2020/6/19 15:35
# @Author : 涛涛
# @Software: PyCharm

from configparser import ConfigParser
import os
from common.handle_path import CONF_DIR

class HandleConfig(ConfigParser):
    """
    配置文件解析器的封装
    """

    def __init__(self, filename):
        super().__init__()
        self.read(filename, encoding="utf-8")


conf = HandleConfig(os.path.join(CONF_DIR,"config.ini"))

