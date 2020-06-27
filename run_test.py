#!D:/PychramCode
# -*- coding: utf-8 -*-
# @Time : 2020/6/15 22:20
# @Author : 涛涛
# @Software: PyCharm
from common.handle_logging import log
import unittest
from BeautifulReport import BeautifulReport
from common import handle_path

log.info("--------------------开始执行案例-------------------")
print("开始执行案例哈哈哈","哈哈哈哈")

# 创建测试套件
suite = unittest.TestSuite()

# 添加测试用例到套件
loader = unittest.TestLoader()
suite.addTest(loader.discover(handle_path.CASE_DIR))

# 执行测试用例生成报告
bf = BeautifulReport(suite)
bf.report("注册接口",filename="bfreport.html",report_dir=handle_path.REPORT_DIR)
log.info("------------------测试案例执行结束--------------------")