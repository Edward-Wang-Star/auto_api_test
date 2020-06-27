#!D:/PychramCode
# -*- coding: utf-8 -*-
# @Time : 2020/6/19 15:36
# @Author : 涛涛
# @Software: PyCharm

import logging
from logging.handlers import TimedRotatingFileHandler
from common import handle_path
import os
log_file = os.path.join(handle_path.LOG_DIR,"api.log")

class HandleLogger():
    """
    处理日志的模块
    """
    # 创建一个日志收集器
    @ staticmethod
    def create_logger():
        # 创建一个日志收集器
        log = logging.getLogger("taotao")
        # 设置日志收集器收集的等级
        log.setLevel("DEBUG")

        # 设置输出的渠道和输出的等级
        # 文件输出
        file_handle = TimedRotatingFileHandler(log_file,encoding="utf-8",when="D",interval=1, backupCount=7)
        file_handle.setLevel("DEBUG")
        log.addHandler(file_handle)
        # 控制台输出
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel("INFO")
        log.addHandler(stream_handler)
        # 创建一个输出的格式对象
        formats = r'%(asctime)s -- [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
        form = logging.Formatter(formats)

        # 将输出格式添加到输出的渠道中
        file_handle.setFormatter(form)
        stream_handler.setFormatter(form)

        return log


log = HandleLogger.create_logger()
