#!D:/PychramCode
# -*- coding: utf-8 -*-
# @Time : 2020/6/19 15:35
# @Author : 涛涛
# @Software: PyCharm

import os

# 获取项目所在的绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 测试模块所在目录的路径
CASE_DIR = os.path.join(BASE_DIR, "testcases")
# 测试数据的路径
DATA_DIR = os.path.join(BASE_DIR, "data")
# 配置文件所在路径
CONF_DIR = os.path.join(BASE_DIR, "conf")
# 测试报告所在路径
REPORT_DIR = os.path.join(BASE_DIR, r"outputs/reports")
# 日志所在路径
LOG_DIR = os.path.join(BASE_DIR, r"outputs/logs")
