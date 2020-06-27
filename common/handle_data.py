#!D:/PychramCode
# -*- coding: utf-8 -*-
# @Time : 2020/6/26 20:04
# @Author : 涛涛
# @Software: PyCharm
import re
from common.handle_config import conf

class EnvData:
    """定义一个类，用来保存用例执行过程中，提取出来的环境变量"""
    pass


def replace_data(data):
    """对于传进的字符串，通过正则表达式来替换数据"""
    while re.search("#(.*?)#",data):
        # 返回一个匹配对象
        res  = re.search("#(.*?)#",data)
        # 获取匹配到的数据
        key = res.group()
        # 匹配到括号中内容
        item = res.group(1)
        try:
            # 获取配置文件中对应的值
            value = conf.get("test_phone",item)
        except:
            # 通过环境变量获取对应的值
            value = getattr(EnvData,item)
        # 通过key找到对应的value，替换成value
        data  = data.replace(key,value)
    return data


