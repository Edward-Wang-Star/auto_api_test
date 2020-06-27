#!D:/PychramCode
# -*- coding: utf-8 -*-
# @Time : 2020/6/22 22:23
# @Author : 涛涛
# @Software: PyCharm

import unittest
from common.handle_excel import HandleExcel
from common.handle_db import HandleMysql
from library.myddt import ddt, data
import os
from common.handle_path import DATA_DIR
import requests
from common.handle_config import conf
import jsonpath
from  common.handle_data import EnvData,replace_data
from common.handle_logging import log
@ddt
class TestAdd(unittest.TestCase):
    excel = HandleExcel(os.path.join(DATA_DIR, "apicases.xlsx"),"add")
    cases = excel.read_excel()
    db = HandleMysql()

    @classmethod
    def setUpClass(cls):
        """先用普通用户登录"""
        headers = eval(conf.get("env", "headers"))
        url = conf.get("env", "BASE_URL") + "member/login"
        data = {"mobile_phone": conf.get("test_phone", "phone"), "pwd": conf.get("test_phone", "pwd")}
        response = requests.request(
            method="post", url=url,
            json=data,
            headers=headers)
        res = response.json()
        log.info("--------登录结果：{}--------".format(res))
        member_id = str(jsonpath.jsonpath(res,"$..id")[0])
        token = "Bearer " + jsonpath.jsonpath(res,"$..token")[0]
        # 将提取出的数据保存为EnvData的类属性
        setattr(EnvData,"member_id",member_id)
        setattr(EnvData,"token",token)



    @data(*cases)
    def test_add(self, case):
        # 第一步：准备数据

        # 请求方法
        method = case["method"]
        # 请求地址
        url = os.path.join(conf.get("env","BASE_URL")) + case["url"]
        # 请求参数
        data = eval(replace_data(case["data"]))
        # 请求头
        headers = eval(conf.get("env","headers"))
        headers["Authorization"]=getattr(EnvData,"token")
        # 预期结果
        expected = eval(case["expected"])
        log.info("--------预期结果：{}----------".format(expected))
        # 回写的行
        row = case["case_id"] + 1
        # 数据库前置查询
        if case["check_sql"]:
            start_count = self.db.find_count(replace_data(case["check_sql"]))
        # 第二步：接口调用
        response = requests.request(method=method, url=url, json=data, headers=headers)
        # 实际结果
        res = response.json()
        log.info("--------实际结果：{}----------".format(res))

        # 数据断言和数据库断言
        try:
            self.assertEqual(expected["code"],res["code"])
            self.assertEqual(expected["msg"],res["msg"])
            # 数据库后置查询
            if case["check_sql"]:
                end_count = self.db.find_count(replace_data(case["check_sql"]))
                self.assertEqual(1,end_count-start_count)
        except AssertionError as e:
            # 结果回写到excel中
            log.error("用例--{}--执行未通过".format(case["title"]))
            log.debug("预期结果：{}".format(expected))
            log.debug("实际结果：{}".format(res))
            log.exception(e)
            self.excel.write_excel(row,8,value = "未通过")
        else:
            # 结果回写excel中
            log.info("用例--{}--执行通过".format(case["title"]))
            self.excel.write_excel(row,8,value = "通过")


