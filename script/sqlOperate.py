# -*- coding: utf-8 -*-
import sqlite3
import pymysql

def operateCreatTable(DBNAME,value):
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()
    try:
        c.execute(value)
    except:
        print("Create table failed.The table already exists.")
        return False
    conn.commit()
    conn.close()

def operateInsert(DBNAME,value):
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()
    try:
        c.execute(value)
    except:
        print("This userName has been registered.")
        return False
    conn.commit()
    conn.close()

def operateSelect(DBNAME,condition):
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()
    values = []
    try:
        cursor = c.execute(condition)
        for row in cursor:
            values.append(row)
        conn.close()
    except:
        print("Please check your SQL script:%s."%condition)
        return False
    return values

def operateUpdate(DBNAME,value):
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()
    try:
        c.execute(value)
    except:
        print("Please check your SQL script:%s."%value)
        return False
    conn.commit()
    print("Total number of rows updated :", conn.total_changes)
    if conn.total_changes == 0:
        return False
    conn.close()

def operateDelete(DBNAME,value):
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()
    try:
        c.execute(value)
    except:
        print("Please check your SQL script%s."%value)
        return False
    conn.commit()
    print("Total number of rows deleted :", conn.total_changes)
    if conn.total_changes == 0:
        return False
    conn.close()




# creatTable = '''CREATE TABLE COMPANY
#            (ID            INT      NOT NULL,
#            NAME           TEXT PRIMARY KEY   NOT NULL,
#            AGE            INT     NOT NULL,
#            ADDRESS        CHAR(50),
#            SALARY         REAL);
#            '''
# insertValue = '''INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (2, 'lisen', 23, 'china', 28000 );
#
# '''
# operateCreatTable("testDB.db",creatTable)
# operateInsert("testDB.db",insertValue)
# select = '''SELECT id, name, address, salary  from COMPANY'''
# values = operateSelect("testDB.db",select)
# print(values)


def mysql_query(host,username,password,database,cmd):
    try:
        # 打开数据库连接
        db = pymysql.connect(host,username,password,database,charset='utf8')

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # 使用execute方法执行SQL语句
        cursor.execute(cmd)

        fetch_all = cursor.fetchall()

        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        db.close()
        return fetch_all
    except Exception as e:
        print(e)

def mysql_update(host,username,password,database,cmd):
    try:
        # 打开数据库连接
        db = pymysql.connect(host,username,password,database, charset='utf8')

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # 使用execute方法执行SQL语句
        cursor.execute(cmd)
        db.commit()
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        db.close()
    except Exception as e:
        print(e)