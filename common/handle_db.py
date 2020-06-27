#!D:/PychramCode
# -*- coding: utf-8 -*-
# @Time : 2020/6/21 12:49
# @Author : 涛涛
# @Software: PyCharm
import pymysql
from common.handle_config import conf

class HandleMysql:
    """处理mysql数据库连接"""
    def __init__(self):
        "创建初始化方法进行数据库连接"
        # 创建连接
        self.con =pymysql.connect(
            host =conf.get("mysql","host"),
            port =conf.getint("mysql","port"),
            user = conf.get("mysql","user"),
            password=conf.get("mysql","password"),
            cursorclass = pymysql.cursors.DictCursor
        )
        #创建一个游标对象
        self.cur = self.con.cursor()

    def find_all(self,sql):
        """
        查询sql语句返回的所有数据
        :param sql:需要执行的sql语句
        :return:查询到的所有数据
        """
        self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchall()

    def find_one(self,sql):
        """
        查询sql语句返回的一条数据
        :param sql:需要执行的sql语句
        :return:查询到的所有数据中的第一条数据
        """
        self.con.commit()
        self.cur.execute(sql)
        return  self.cur.fetchone()

    def find_count(self, sql):
        """
        sql语句查询到的数据条数
        :param sql: 查询的sql
        :return:查询到的数据条数
        """
        self.con.commit()
        res = self.cur.execute(sql)
        return res

    def update(self,sql):
        """
        增删改的操作
        :param sql:需要执行的sql语句
        :return:
        """
        self.cur.execute(sql)
        self.con.commit()

    def close(self):
        """
        断开游标，关闭连接
        :return:
        """
        self.cur.close()
        self.con.close()



if __name__ == '__main__':
    db = HandleMysql()

