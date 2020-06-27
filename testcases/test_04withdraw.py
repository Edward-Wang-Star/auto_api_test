#!D:/PychramCode
# -*- coding: utf-8 -*-
# @Time : 2020/6/22 20:36
# @Author : 涛涛
# @Software: PyCharm

import unittest
from library.myddt import ddt, data
from common.handle_excel import HandleExcel
from common.handle_db import HandleMysql
from common.handle_path import DATA_DIR
from common.handle_config import conf
import os
import requests
import jsonpath
import decimal
from common.handle_logging import log


@ddt
class TestWithdraw(unittest.TestCase):
    excel = HandleExcel(os.path.join(DATA_DIR, "apicases.xlsx"), "withdraw")
    cases = excel.read_excel()
    db = HandleMysql()

    @classmethod
    def setUpClass(cls):
        # 第一步：准备用例数据
        # 请求方法
        method = "post"
        # 请求地址
        url = conf.get("env", "BASE_URL") + "/member/login"
        # 请求参数
        data = {"mobile_phone": conf.get("test_phone", "phone"), "pwd": conf.get("test_phone", "pwd")}
        # 请求头
        headers = eval(conf.get("env", "headers"))
        response = requests.request(method=method, url=url, json=data, headers=headers)
        res = response.json()
        print("登录出参：", res)
        cls.member_id = str(jsonpath.jsonpath(res, "$..id")[0])
        cls.token = "Bearer" + " " + jsonpath.jsonpath(res, "$..token")[0]
        print("提取到的用户id" , cls.member_id)
        print("提取到token",cls.token)

    @data(*cases)
    def test_withdraw(self, case):
        # 第一步：准备用例数据
        # 请求方法
        method = case["method"]
        # 请求地址
        url = conf.get("env", "BASE_URL") + case["url"]
        # 请求参数，替换用例中#member_id#
        data = eval(case["data"].replace("#member_id#",self.member_id))
        # 请求头
        headers = eval(conf.get("env","headers"))
        headers["Authorization"] = self.token
        # 期望结果
        expected = eval(case["expected"])
        # 数据库前置查询
        if case["check_sql"]:
            sql = case["check_sql"].format(self.member_id)
            start_money =self.db.find_one(sql)["leave_amount"]
        # 需要回写的行
        row = case["case_id"] + 1

        # 第二步：接口调用
        response = requests.request(method=method, url=url, json=data, headers=headers)
        res = response.json()
        print("预期结果：",expected)
        print("实际结果：",res)

        # 数据库后置查询
        if case["check_sql"]:
            sql = case["check_sql"].format(self.member_id)
            end_money =self.db.find_one(sql)["leave_amount"]

        # 第三步：数据断言和数据库断言
        try:
            self.assertEqual(expected["code"],res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            # 数据库断言
            if case["check_sql"]:
                recharge_money = decimal.Decimal(str(data["amount"]))
                self.assertEqual(recharge_money,start_money-end_money)
        except AssertionError as e:
            # 结果回写到excel中
            log.error("用例{}执行未通过".format(case["title"]))
            log.debug("预期结果：{}".format(expected))
            log.debug("实际结果：{}".format(res))
            log.exception(e)
            self.excel.write_excel(row=row, column=8, value="未通过")
            raise e
        else:
            log.info("用例--{}--执行通过".format(case["title"]))
            self.excel.write_excel(row=row,column=8,value="通过")




