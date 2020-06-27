#!D:/PychramCode
# -*- coding: utf-8 -*-
# @Time : 2020/6/19 17:51
# @Author : 涛涛
# @Software: PyCharm

from library.myddt import ddt,data
import unittest
from common.handle_excel import HandleExcel
from requests import request
from common.handle_logging import log
from common.handle_config import conf
from common import handle_path
import os

# filename = r"D:\PychramCode\auto_api_test\data\apicases.xlsx"
filename = os.path.join(handle_path.DATA_DIR,"apicases.xlsx")


@ddt
class LoginTestCase(unittest.TestCase):
    excel = HandleExcel(filename, "login")
    cases = excel.read_excel()

    @data(*cases)
    def test_login(self, cases):
        # 第一步：准备用例数据
        # 请求方法
        method = cases["method"]
        # 请求地址
        url = cases["url"]
        # 请求参数
        data = eval(cases["data"])
        # 请求头
        headers = eval(conf.get("env", "headers"))
        # 预期结果
        expected = eval(cases["expected"])
        # 用例所在行
        row = cases["case_id"] + 1
        # 调用接口请求
        response = request(method=method, url=url, json=data, headers=headers)
        # 获取实际结果
        res = response.json()
        # print("预期结果为：", expected)
        # print("实际结果为：", res)
        # 断言
        try:
            # 断言两个字段是否相同
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
        except AssertionError as e:
            # 断言结果回写到excel中
            log.error("用例---{}----执行未通过".format(cases["title"]))
            log.debug("预期结果为：{}".format(expected))
            log.debug("实际结果为：{}".format(res))
            log.exception(e)
            self.excel.write_excel(row=row, column=8, value="不通过")
            # 抛出异常
            raise e
        else:
            # 结果回写到excel中
            log.info("用例---{}----执行通过".format(cases["title"]))
            self.excel.write_excel(row=row, column=8, value="通过")
