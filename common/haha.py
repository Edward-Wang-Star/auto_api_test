#!D:/PychramCode
# -*- coding: utf-8 -*-
# @Time : 2020/6/21 14:04
# @Author : 涛涛
# @Software: PyCharm

def random_phone():
    """随机生成数据库中没有的手机号"""
    while True:
        phone = "155"
        for i in range(8):
            r =  random.randint(0,9)
            phone= phone + str(r)
        sql = "SELECT * FROM futureloan.member WHERE mobile_phone={}".format(phone)
        res =cls.db.find_one(sql)
        if res == 0:
            return phone


if __name__ == '__main__':
    phone = random_phone()
    print(phone)