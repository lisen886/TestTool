from script.sqlOperate import *
import json

def creatTable():
    creatTable = '''CREATE TABLE COMPANY
                   (NAME           TEXT PRIMARY KEY   NOT NULL,
                   TEAM        CHAR(50),
                   PASSWORD       INT  NOT NULL,
                   TEL          INT );
                   '''
    operateCreatTable("userDB.db", creatTable)
def registerUser(valueList):
    insertValue = 'INSERT INTO COMPANY (NAME,TEAM,PASSWORD,TEL) VALUES ' + str(valueList) + ';'
    status = operateInsert("userDB.db", insertValue)
    return status
def getValue():
    select = '''SELECT name, team, password, tel  from COMPANY'''
    values = operateSelect("userDB.db", select)
    return values

def getUserInfo(inputName):
    select = "SELECT *  from COMPANY WHERE NAME = "+json.dumps(inputName)
    values = operateSelect("userDB.db", select)
    return values

def deleteUserInfo(inputName):
    deleteCondition = "DELETE FROM COMPANY WHERE NAME = "+json.dumps(inputName)
    values = operateDelete("userDB.db", deleteCondition)
    return values

def updateUserInfo(inputName,updateName,updateTeam,updatePassword,updateTel):
    updateCondition = "UPDATE COMPANY SET NAME = "+json.dumps(updateName)+", TEAM="+json.dumps(updateTeam)+", PASSWORD ="+json.dumps(updatePassword)+", TEL="+json.dumps(updateTel)+" WHERE NAME = "+json.dumps(inputName)
    values = operateUpdate("userDB.db", updateCondition)
    return values