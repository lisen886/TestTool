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

def getPerKeyInfo():
    values = mysql_query('SELECT * FROM CPU order by No ASC')
    keyInfo = {}
    versionList = []
    browserList = []
    modeList = []
    codecList = []
    for No,version,browser,mode,codec,value in values:
        versionList.append(version)
        browserList.append(browser)
        modeList.append(mode)
        codecList.append(codec)
    keyInfo['version'] = list(sorted(set(versionList)))
    keyInfo['browser'] = list(sorted(set(browserList)))
    keyInfo['mode'] = list(sorted(set(modeList)))
    keyInfo['codec'] = list(sorted(set(codecList)))
    return keyInfo

def getPerInfo(table_index,version,browser,mode,codec):
    valueDict = {}
    for table in json.loads(table_index):
        cmd = 'SELECT * FROM ' + table + ' WHERE version in ' + version.replace("[","(").replace("]",")") +' and browser in ' + browser.replace("[","(").replace("]",")")+' and mode in ' + mode.replace("[","(").replace("]",")")+' and codec in ' + codec.replace("[","(").replace("]",")" + 'ORDER BY No asc')
        values = mysql_query(cmd)
        valueDict[table]=values
    return valueDict

def getConfigs():
    cmd = 'SELECT * FROM TestToolConfig'
    values = mysql_query(cmd)
    return values

def updateConfigInfo(name,value):
    updateCondition = "UPDATE TestToolConfig SET Name = "+json.dumps(name)+", value="+json.dumps(value)+ " WHERE Name = "+json.dumps(name)
    mysql_update(updateCondition)