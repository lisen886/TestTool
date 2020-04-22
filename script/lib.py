from script.sqlOperate import *
import json
import configparser
from flask import session
conf = configparser.ConfigParser()
conf.read("extend.ini")
host = conf.get('mysql','host')
username = conf.get('mysql','username')
password = conf.get('mysql','password')
WebRTC_DB = conf.get('mysql','WebRTC_DB')
Native_DB = conf.get('mysql','Native_DB')

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
    addTestToolLogSerever(session.get('username'), deleteCondition)
    return values

def updateUserInfo(inputName,updateName,updateTeam,updatePassword,updateTel):
    updateCondition = "UPDATE COMPANY SET NAME = "+json.dumps(updateName)+", TEAM="+json.dumps(updateTeam)+", PASSWORD ="+json.dumps(updatePassword)+", TEL="+json.dumps(updateTel)+" WHERE NAME = "+json.dumps(inputName)
    values = operateUpdate("userDB.db", updateCondition)
    addTestToolLogSerever(session.get('username'), updateCondition)
    return values

def getPerKeyInfo():
    values = mysql_query(host=host,username=username, password=password,database=WebRTC_DB,cmd='SELECT * FROM CPU order by No ASC')
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
        values = mysql_query(host=host,username=username, password=password,database=WebRTC_DB,cmd=cmd)
        valueDict[table]=values
    return valueDict

def getConfigs():
    cmd = 'SELECT * FROM TestToolConfig'
    values = mysql_query(host=host,username=username, password=password,database=WebRTC_DB,cmd=cmd)
    return values

def updateConfigInfo(name,value):
    updateCondition = "UPDATE TestToolConfig SET Name = "+json.dumps(name)+", value="+json.dumps(value)+ " WHERE Name = "+json.dumps(name)
    mysql_update(host=host,username=username, password=password,database=WebRTC_DB,cmd=updateCondition)
    addTestToolLogSerever(session.get('username'), updateCondition)

def getWebRTCInfoSQL(index):
    cmd = 'SELECT * FROM '+index
    values = mysql_query(host=host,username=username, password=password,database=WebRTC_DB,cmd=cmd,cursorclass="dict")
    return values

def getWebRTCInfoByNoSQL(No,index):
    cmd = 'SELECT * FROM '+index+' where No ='+json.dumps(No)
    values = mysql_query(host=host,username=username, password=password,database=WebRTC_DB,cmd=cmd,cursorclass="dict")
    return values

def updateWebRTCInfoByNoSQL(data):
    cmd = "update {database[0]} set version='{version[0]}',browser='{browser[0]}',mode='{mode[0]}',codec='{codec[0]}',value={value[0]} where No={No[0]}".format(**data)
    res = mysql_update(host=host,username=username, password=password,database=WebRTC_DB,cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res

def insertWebRTCInfoByNoSQL(data):
    cmd = "INSERT INTO {database[0]} set version='{version[0]}',browser='{browser[0]}',mode='{mode[0]}',codec='{codec[0]}',value={value[0]}".format(**data)
    res = mysql_update(host=host,username=username, password=password,database=WebRTC_DB,cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res

def deleteWebRTCInfoByNoSQL(data):
    cmd = "DELETE FROM {database[0]} where No={No[0]}".format(**data)
    res = mysql_update(host=host,username=username, password=password,database=WebRTC_DB,cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res

def addTestToolLogSerever(Name,Log):
    cmd = "INSERT INTO TestToolLog set Name='{}',Log={}".format(Name,json.dumps(Log))
    res = mysql_update(host=host,username=username, password=password,database=WebRTC_DB,cmd=cmd)
    return res

def getSysLogSQL():
    cmd = "SELECT * FROM TestToolLog order by No desc"
    values = mysql_query(host=host,username=username, password=password,database=WebRTC_DB,cmd=cmd,cursorclass="dict")
    return values

def getRoleByNameSQL(Name):
    cmd = 'SELECT * FROM TestToolRole where Name ='+json.dumps(Name)
    values = mysql_query(host=host,username=username, password=password,database=WebRTC_DB,cmd=cmd,cursorclass="dict")
    try:
        role = values[0]["Role"]
    except:
        role = "None"
    return role

##### native mysql #####
def getNativeVersion():
    cmd = 'SELECT * FROM BugCount order by version ASC'
    values = mysql_query(host=host,username=username, password=password,database=Native_DB,cmd=cmd,cursorclass="dict")
    return values

def getNativePerInfo(version,indexList):
    indexList.append("version")
    cmd = 'SELECT '+",".join(indexList)+' FROM BugCount Where version in ' + str(version).replace("[","(").replace("]",")")
    values = mysql_query(host=host,username=username, password=password,database=Native_DB,cmd=cmd,cursorclass="dict")
    return values

def getNativeInfoSQL(index):
    cmd = 'SELECT * FROM '+index
    values = mysql_query(host=host,username=username, password=password,database=Native_DB,cmd=cmd,cursorclass="dict")
    return values

def getNativeInfoByVersionSQL(version,index):
    cmd = 'SELECT * FROM '+index+' where version ='+json.dumps(version)
    values = mysql_query(host=host,username=username, password=password,database=Native_DB,cmd=cmd,cursorclass="dict")
    return values

def updateNativeInfoByVersionSQL(data):
    cmd = "update {database[0]} set features={features[0]},total={total[0]},demo={demo[0]},sdk={sdk[0]},video={video[0]}," \
          "audio={audio[0]},crash={crash[0]},firstTimePassRate={firstTimePassRate[0]},acceptancePhase={acceptancePhase[0]},regressionPhase={regressionPhase[0]},acceptancePhaseRate={acceptancePhaseRate[0]},regressionPhaseRate={regressionPhaseRate[0]} where version='{version[0]}'".format(**data)
    res = mysql_update(host=host,username=username, password=password,database=Native_DB,cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res

def insertNativeInfoByVersionSQL(data):
    cmd = "INSERT INTO {database[0]} set version='{version[0]}',features={features[0]},total={total[0]},demo={demo[0]},sdk={sdk[0]},video={video[0]}," \
          "audio={audio[0]},crash={crash[0]},firstTimePassRate={firstTimePassRate[0]},acceptancePhase={acceptancePhase[0]},regressionPhase={regressionPhase[0]},acceptancePhaseRate={acceptancePhaseRate[0]},regressionPhaseRate={regressionPhaseRate[0]}".format(**data)
    res = mysql_update(host=host,username=username, password=password,database=Native_DB,cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res

def deleteNativeInfoByVersionSQL(data):
    cmd = "DELETE FROM {database[0]} where version='{version[0]}'".format(**data)
    res = mysql_update(host=host,username=username, password=password,database=Native_DB,cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res