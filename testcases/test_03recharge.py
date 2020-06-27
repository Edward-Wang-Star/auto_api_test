#!D:/PychramCode
# -*- coding: utf-8 -*-
# @Time : 2020/6/21 17:37
# @Author : 涛涛
# @Software: PyCharm

import unittest
from library.myddt import ddt, data
from common.handle_excel import HandleExcel
import os
from common.handle_path import DATA_DIR
from requests import request
from common.handle_config import conf
from jsonpath import jsonpath
from common.handle_db import HandleMysql
import decimal
from common.handle_logging import log

filename = os.path.join(DATA_DIR, "apicases.xlsx")


@ddt
class TestRecharge(unittest.TestCase):
    excel = HandleExcel(filename, "recharge")
    cases = excel.read_excel()
    db = HandleMysql()

    @classmethod
    def setUpClass(cls):
        # 用例的前置条件，进行登录操作
        # 准备登录所用的相关数据
        url = conf.get("env", "BASE_URL") + "/member/login"
        data = {
            "mobile_phone": conf.get("test_phone", "phone"),
            "pwd": conf.get("test_phone", "pwd")
        }
        headers = eval(conf.get("env", "headers"))
        response = request(method="post", url=url, json=data, headers=headers)
        res = response.json()
        cls.member_id = str(jsonpath(res, "$..id")[0])
        cls.token = "Bearer" + " " + jsonpath(res, "$..token")[0]
        print("member_id为", cls.member_id)
        print("token为", cls.token,type(cls.token))

    @data(*cases)
    def test_recharge(self, case):
        # 第一步：准备测试数据
        # 请求方法
        method = case["method"]
        # 请求url
        url = conf.get("env", "BASE_URL") + case["url"]
        # 请求数据
        case["data"] =case["data"].replace("#member_id#",self.member_id)
        data = eval(case["data"])
        # 请求头
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = self.token
        print(headers)
        # 期望结果
        expected = eval(case["expected"])
        # 用例回写行数
        row = case["case_id"] + 1
        # 数据库前置查询
        if case["check_sql"]:
            sql = case["check_sql"].format(self.member_id)
            print(sql)
            start_money = self.db.find_one(sql)["leave_amount"]
            print("充值前的金额为：", start_money)

        # 第二步：接口调用
        response = request(method=method, url=url, json=data, headers=headers)
        # 调用接口
        res = response.json()
        print("预期结果：{}".format(expected))
        print("实际结果：{}".format(res))
        # 数据库后置查询
        if case["check_sql"]:
            sql = case["check_sql"].format(self.member_id)
            end_money = self.db.find_one(sql)["leave_amount"]

        # 第三步：断言
        try:
            # 数据断言
            self.assertEqual(expected["code"], jsonpath(res, "$..code")[0])
            self.assertEqual(expected["msg"], jsonpath(res, "$..msg")[0])
            # 数据库断言
            if case["check_sql"]:
                # 将充值金额转换为decimal类型（数据库中的金额为decimal类型）
                recharge_money = decimal.Decimal(str(data["amount"]))
                self.assertEqual(recharge_money, end_money - start_money)
        except AssertionError as e:
            # 结果回写到excel中
            log.debug("----用例{}执行完成-------".format(case["title"]))
            log.exception(e)
            self.excel.write_excel(row=row, column=8, value="未通过")
            raise e
        else:
            # 结果回写到excel中
            log.info("---用例{}执行完成---------".format(case["title"]))
            self.excel.write_excel(row=row, column=8, value="通过")
