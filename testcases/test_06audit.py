#!D:/PychramCode
# -*- coding: utf-8 -*-
# @Time : 2020/6/26 21:41
# @Author : 涛涛
# @Software: PyCharm
import unittest
from library.myddt import ddt, data
from common.handle_excel import HandleExcel
import os
from common.handle_path import DATA_DIR
from common.handle_db import HandleMysql
from common.handle_config import conf
import requests
import jsonpath
from common.handle_data import EnvData, replace_data
from common.handle_logging import log


@ddt
class TestAudit(unittest.TestCase):
    excel = HandleExcel(os.path.join(DATA_DIR, "apicases.xlsx"), "audit")
    cases = excel.read_excel()
    db = HandleMysql()

    @classmethod
    def setUpClass(cls):
        """普通用户和管理员用户登录"""
        # 普通用户登录
        # 数据准备
        url = conf.get("env", "BASE_URL") + "member/login"
        data = {"mobile_phone": conf.get("test_phone", "phone"), "pwd": conf.get("test_phone", "pwd")}
        headers = eval(conf.get("env", "headers"))
        response = requests.request(method="post", url=url, json=data, headers=headers)
        res1 = response.json()
        # 普通用户member_id和token获取
        user_member_id = jsonpath.jsonpath(res1, "$..id")[0]
        user_token = "Bearer" + " " + jsonpath.jsonpath(res1, "$..token")[0]
        # 管理员用户登录
        data2 = {"mobile_phone": conf.get("test_phone", "admin_phone"), "pwd": conf.get("test_phone", "admin_pwd")}
        response2 = requests.request(method="post", url=url, json=data2, headers=headers)
        res2 = response2.json()
        print(res2)
        # 管理员member_id和token获取
        admin_member_id = jsonpath.jsonpath(res2, "$..id")[0]
        admin_token = "Bearer" + " " + jsonpath.jsonpath(res2, "$..token")[0]
        # member_id和token存储
        setattr(EnvData, "user_member_id", user_member_id)
        setattr(EnvData, "user_token", user_token)
        setattr(EnvData, "admin_member_id", admin_member_id)
        setattr(EnvData, "admin_token", admin_token)

    def setUp(self):
        # 每条用例之前的前置条件：添加一个新的项目
        url = conf.get("env", "BASE_URL") + "/loan/add"
        data = {"member_id": getattr(EnvData, "user_member_id"), "title": "借钱实现财富自由", "amount": 2000, "loan_rate": 12.0,
                "loan_term": 3, "loan_date_type": 1, "bidding_days": 5}
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(EnvData, "user_token")
        response = requests.request(method="post", url=url, json=data, headers=headers)
        res = response.json()
        # 项目的id存储为环境变量
        setattr(EnvData, "loan_id", str(jsonpath.jsonpath(res, "$..id")[0]))

    @data(*cases)
    def test_audit(self, case):
        # 第一步：准备测试数据
        # 调用方法
        method = case["method"]
        # 调用地址
        url = conf.get("env", "BASE_URL") + case["url"]
        # 调用参数
        data = eval(replace_data(case["data"]))
        # 调用信息头
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(EnvData, "admin_token")
        # 预期结果
        expected = eval(case["expected"])
        # 是否有数据库校验
        if case["check_sql"]:
            sql = replace_data(case["check_sql"])
            start_count = self.db.find_count(sql)
        # 回写的行
        row = case["case_id"] + 1
        # 第二步：接口调用
        response = requests.request(method=method, url=url, json=data, headers=headers)
        res = response.json()
        if case["title"] == "审核通过" and res["msg"] == "OK":
            # 判断有“审核通过”的案例，已经审核通过，保存项目id
            setattr(EnvData, "pass_loan_id", str(data["loan_id"]))
            print("------------------------",EnvData.pass_loan_id)
        # 第三步：断言和回写
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            # 是否需要数据库校验
            if case["check_sql"]:
                sql = replace_data(case["check_sql"])
                status = self.db.find_one(sql)["status"]
                self.assertEqual(expected["status"], status)
        except AssertionError as e:
            # 结果回写excel中
            log.error("用例--{}--执行未通过".format(case["title"]))
            log.debug("预期结果：{}".format(expected))
            log.debug("实际结果：{}".format(res))
            log.exception(e)
            self.excel.write_excel(row=row, column=8, value="未通过")
            raise e
        else:
            # 结果回写excel中
            log.info("用例--{}--执行通过".format(case["title"]))
            self.excel.write_excel(row=row, column=8, value="通过")
