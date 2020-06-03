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

# def registerUser(valueList):
#     insertValue = 'INSERT INTO COMPANY (NAME,TEAM,PASSWORD,TEL) VALUES ' + str(valueList) + ';'
#     status = operateInsert("userDB.db", insertValue)
#     return status
# def getValue():
#     select = '''SELECT name, team, password, tel  from COMPANY'''
#     values = operateSelect("userDB.db", select)
#     return values

# def getUserInfo(inputName):
#     select = "SELECT *  from COMPANY WHERE NAME = "+json.dumps(inputName)
#     values = operateSelect("userDB.db", select)
#     return values

# def deleteUserInfo(inputName):
#     deleteCondition = "DELETE FROM COMPANY WHERE NAME = "+json.dumps(inputName)
#     values = operateDelete("userDB.db", deleteCondition)
#     addTestToolLogSerever(session.get('username'), deleteCondition)
#     return values
#
# def updateUserInfo(inputName,updateName,updateTeam,updatePassword,updateTel):
#     updateCondition = "UPDATE COMPANY SET NAME = "+json.dumps(updateName)+", TEAM="+json.dumps(updateTeam)+", PASSWORD ="+json.dumps(updatePassword)+", TEL="+json.dumps(updateTel)+" WHERE NAME = "+json.dumps(inputName)
#     values = operateUpdate("userDB.db", updateCondition)
#     addTestToolLogSerever(session.get('username'), updateCondition)
#     return values

#### sqlite3 userDB.db  --> MySQL webRTC_per.db TestToolUser
def registerUser(valueList):
    cmd = 'INSERT INTO TestToolUser (NAME,TEAM,PASSWORD,TEL) VALUES ' + str(valueList) + ';'
    res = mysql_update(host=host, username=username, password=password, database=WebRTC_DB, cmd=cmd)
    return res

def getValue():
    cmd = '''SELECT NAME,TEAM,PASSWORD,TEL  from TestToolUser'''
    values = mysql_query(host=host, username=username, password=password, database=WebRTC_DB, cmd=cmd)
    return values

def getUserInfo(inputName):
    cmd = "SELECT *  from TestToolUser WHERE NAME = "+json.dumps(inputName)
    values = mysql_query(host=host, username=username, password=password, database=WebRTC_DB, cmd=cmd)
    return values

def deleteUserInfo(inputName):
    cmd = "DELETE FROM TestToolUser WHERE NAME = "+json.dumps(inputName)
    res = mysql_update(host=host, username=username, password=password, database=WebRTC_DB, cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res

def updateUserInfo(inputName,updateName,updateTeam,updatePassword,updateTel):
    cmd = "UPDATE TestToolUser SET NAME = "+json.dumps(updateName)+", TEAM="+json.dumps(updateTeam)+", PASSWORD ="+json.dumps(updatePassword)+", TEL="+json.dumps(updateTel)+" WHERE NAME = "+json.dumps(inputName)
    print(cmd)
    res = mysql_update(host=host, username=username, password=password, database=WebRTC_DB, cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res

def getPerKeyInfo():
    values = mysql_query(host=host,username=username, password=password,database=WebRTC_DB,cmd='SELECT * FROM CPU order by No ASC')
    keyInfo = {}
    versionList = []
    browserList = []
    modeList = []
    codecList = []
    for No,version,browser,mode,codec,value,extend in values:
        versionList.append(version)
        browserList.append(browser)
        modeList.append(mode)
        codecList.append(codec)
    keyInfo['version'] = list(sorted(set(versionList)))
    keyInfo['browser'] = list(sorted(set(browserList)))
    keyInfo['mode'] = list(sorted(set(modeList)))
    keyInfo['codec'] = list(sorted(set(codecList)))
    return keyInfo

def getPerInfo(table_index,version,browser,mode,codec,extend,AV_extend_check):
    valueDict = {}
    for table in json.loads(table_index):
        if table == "视频卡顿率":
            cmd = 'SELECT * FROM ' + table + ' WHERE version in ' + version.replace("[", "(").replace("]",")") + ' and browser in ' + browser.replace("[", "(").replace("]", ")") + ' and mode in ' + mode.replace("[", "(").replace("]",")") + ' and codec in ' + codec.replace("[", "(").replace("]", ")") + ' and extend in ' + extend.replace("[", "(").replace("]",")") + 'ORDER BY version asc'
        elif table == "音频抗丢包边界":
            cmd = 'SELECT * FROM ' + table + ' WHERE version in ' + version.replace("[", "(").replace("]",")") + ' and browser in ' + browser.replace("[", "(").replace("]", ")") + ' and mode in ' + mode.replace("[", "(").replace("]",")") + ' and codec in ' + codec.replace("[", "(").replace("]", ")") + ' and extend in ' + AV_extend_check.replace("[", "(").replace("]",")") + 'ORDER BY version asc'
        else:
            cmd = 'SELECT * FROM ' + table + ' WHERE version in ' + version.replace("[","(").replace("]",")") +' and browser in ' + browser.replace("[","(").replace("]",")")+' and mode in ' + mode.replace("[","(").replace("]",")")+' and codec in ' + codec.replace("[","(").replace("]",")") + 'ORDER BY version asc'
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
    cmd = "update {database[0]} set version='{version[0]}',browser='{browser[0]}',mode='{mode[0]}',codec='{codec[0]}',value={value[0]},extend='{extend[0]}' where No={No[0]}".format(**data)
    res = mysql_update(host=host,username=username, password=password,database=WebRTC_DB,cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res

def insertWebRTCInfoByNoSQL(data):
    cmd = "INSERT INTO {database[0]} set version='{version[0]}',browser='{browser[0]}',mode='{mode[0]}',codec='{codec[0]}',value={value[0]},extend='{extend[0]}'".format(**data)
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
          "audio={audio[0]},crash={crash[0]},firstTimePassRate={firstTimePassRate[0]},acceptancePhase={acceptancePhase[0]},regressionPhase={regressionPhase[0]},acceptancePhaseRate={acceptancePhaseRate[0]},regressionPhaseRate={regressionPhaseRate[0]},fallbackRate={fallbackRate[0]},cloudCrashRate={cloudCrashRate[0]},codeChangeLine={codeChangeLine[0]},bugsForChange={bugsForChange[0]} where version='{version[0]}'".format(**data)
    res = mysql_update(host=host,username=username, password=password,database=Native_DB,cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res

def insertNativeInfoByVersionSQL(data):
    cmd = "INSERT INTO {database[0]} set version='{version[0]}',features={features[0]},total={total[0]},demo={demo[0]},sdk={sdk[0]},video={video[0]}," \
          "audio={audio[0]},crash={crash[0]},firstTimePassRate={firstTimePassRate[0]},acceptancePhase={acceptancePhase[0]},regressionPhase={regressionPhase[0]},acceptancePhaseRate={acceptancePhaseRate[0]},regressionPhaseRate={regressionPhaseRate[0]},fallbackRate={fallbackRate[0]},cloudCrashRate={cloudCrashRate[0]},codeChangeLine={codeChangeLine[0]},bugsForChange={bugsForChange[0]}".format(**data)
    res = mysql_update(host=host,username=username, password=password,database=Native_DB,cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res

def deleteNativeInfoByVersionSQL(data):
    cmd = "DELETE FROM {database[0]} where version='{version[0]}'".format(**data)
    res = mysql_update(host=host,username=username, password=password,database=Native_DB,cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res

##### cloudRecord mysql #####
def getCloudRecordVersion():
    cmd = 'SELECT * FROM cloudRecord order by version ASC'
    values = mysql_query(host=host,username=username, password=password,database=Native_DB,cmd=cmd,cursorclass="dict")
    return values

def getCloudRecordPerInfo(version,indexList):
    indexList.append("version")
    cmd = 'SELECT '+",".join(indexList)+' FROM cloudRecord Where version in ' + str(version).replace("[","(").replace("]",")")
    values = mysql_query(host=host,username=username, password=password,database=Native_DB,cmd=cmd,cursorclass="dict")
    return values

def getCloudRecordInfoSQL(index):
    cmd = 'SELECT * FROM '+index
    values = mysql_query(host=host,username=username, password=password,database=Native_DB,cmd=cmd,cursorclass="dict")
    return values

def getCloudRecordInfoByVersionSQL(version,index):
    cmd = 'SELECT * FROM '+index+' where version ='+json.dumps(version)
    values = mysql_query(host=host,username=username, password=password,database=Native_DB,cmd=cmd,cursorclass="dict")
    return values

def updateCloudRecordInfoByVersionSQL(data):
    cmd = "update {database[0]} set bugs={bugs[0]},passRate={passRate[0]},packages={packages[0]} where version='{version[0]}'".format(**data)
    res = mysql_update(host=host,username=username, password=password,database=Native_DB,cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res

def insertCloudRecordInfoByVersionSQL(data):
    cmd = "INSERT INTO {database[0]} set version='{version[0]}',bugs={bugs[0]},passRate={passRate[0]},packages={packages[0]}".format(**data)
    res = mysql_update(host=host,username=username, password=password,database=Native_DB,cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res

def deleteCloudRecordInfoByVersionSQL(data):
    cmd = "DELETE FROM {database[0]} where version='{version[0]}'".format(**data)
    res = mysql_update(host=host,username=username, password=password,database=Native_DB,cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res

# AVC
def getAVCVersion():
    cmd = 'SELECT * FROM AVC_CPU order by Version ASC'
    values = mysql_query(host=host,username=username, password=password,database=Native_DB,cmd=cmd,cursorclass="dict")
    return values

def getAVCPerInfo(version_checkList,selectPlatform,selectScene,app_avc_checkList,profile_avc_checkList,index_avc_checkList):
    valueDict = {}
    for table in index_avc_checkList:
        cmd = 'SELECT * FROM ' + 'AVC_'+table + ' WHERE Version in ' + str(version_checkList).replace("[","(").replace("]",")") +' and App in ' + str(app_avc_checkList).replace("[","(").replace("]",")")+' and Profile in ' + str(profile_avc_checkList).replace("[","(").replace("]",")")+" and Platform = '" + selectPlatform+"' and Scene = '" + selectScene + "' ORDER BY Version asc"
        values = mysql_query(host=host,username=username, password=password,database=Native_DB,cmd=cmd)
        valueDict[table]=values
    return valueDict

def getAVCJiraInfo(version_checkList,selectPlatform,selectScene,app_avc_checkList,profile_avc_checkList,index_avc_checkList):
    cmd = 'SELECT * FROM ' + 'AVC_' + index_avc_checkList + ' WHERE Version in ' + str(version_checkList).replace("[", "(").replace("]", ")") + ' and App in ' + str(app_avc_checkList).replace("[", "(").replace("]",")") + ' and Profile in ' + str(profile_avc_checkList).replace("[", "(").replace("]",")") + " and Platform = '" + selectPlatform + "' and Scene = '" + selectScene + "' ORDER BY Version asc"
    values = mysql_query(host=host, username=username, password=password, database=Native_DB, cmd=cmd,cursorclass="dict")
    return values

def getAVCInfoSQL(index):
    cmd = 'SELECT * FROM '+'AVC_' + index
    values = mysql_query(host=host,username=username, password=password,database=Native_DB,cmd=cmd,cursorclass="dict")
    return values

def getAVCInfoByNoSQL(No,index):
    cmd = 'SELECT * FROM ' + 'AVC_' + index+' where No ='+json.dumps(No)
    values = mysql_query(host=host,username=username, password=password,database=Native_DB,cmd=cmd,cursorclass="dict")
    return values

def updateAVCInfoByNoSQL(data):
    if data.get("database")[0] == "Jira统计":
        cmd = "update AVC_{database[0]} set Version='{Version[0]}',App='{App[0]}',Platform='{Platform[0]}',Scene='{Scene[0]}',Profile='{Profile[0]}',Bugs='{Bugs[0]}',Links='{Links[0]}' where No={No[0]}".format(**data)
    else:
        cmd = "update AVC_{database[0]} set Version='{Version[0]}',App='{App[0]}',Platform='{Platform[0]}',Scene='{Scene[0]}',Profile='{Profile[0]}',Value={Value[0]} where No={No[0]}".format(**data)
    res = mysql_update(host=host,username=username, password=password,database=Native_DB,cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res

def insertAVCInfoByNoSQL(data):
    if data.get("database")[0] == "Jira统计":
        cmd = "INSERT INTO AVC_{database[0]} set Version='{Version[0]}',App='{App[0]}',Platform='{Platform[0]}',Scene='{Scene[0]}',Profile='{Profile[0]}',Bugs='{Bugs[0]}',Links='{Links[0]}'".format(**data)
    else:
        cmd = "INSERT INTO AVC_{database[0]} set Version='{Version[0]}',App='{App[0]}',Platform='{Platform[0]}',Scene='{Scene[0]}',Profile='{Profile[0]}',Value='{Value[0]}'".format(**data)
    res = mysql_update(host=host,username=username, password=password,database=Native_DB,cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res

def deleteAVCInfoByNoSQL(data):
    cmd = "DELETE FROM AVC_{database[0]} where No='{No[0]}'".format(**data)
    res = mysql_update(host=host,username=username, password=password,database=Native_DB,cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res

# AVC全平台质量跟踪报告
def getAVCQuality():
    cmd = 'SELECT * FROM AVC_Quality_Crash order by Version ASC'
    values = mysql_query(host=host,username=username, password=password,database=Native_DB,cmd=cmd,cursorclass="dict")
    return values

def getAVCQualityVersionByPlatformSQL(Platform):
    cmd = "SELECT * FROM AVC_Quality_Crash where Platform='{}' order by Version ASC".format(Platform)
    values = mysql_query(host=host,username=username, password=password,database=Native_DB,cmd=cmd,cursorclass="dict")
    return values

def getAVCQualityPerInfo(version,selectPlatform,search_interval,index):
    if index=="AVC_Quality_Crash":
        cmd = "SELECT * FROM {} Where Platform = '{}' and Time>DATE_SUB(CURDATE(), INTERVAL {}) and Version in ".format(index,selectPlatform,search_interval) + str(version).replace("[","(").replace("]",")")
    elif index == "AVC_Quality_Count":
        cmd = "SELECT * FROM {} Where Platform = '{}' and Time>DATE_SUB(CURDATE(), INTERVAL {})".format(index,selectPlatform,search_interval)
    values = mysql_query(host=host,username=username, password=password,database=Native_DB,cmd=cmd,cursorclass="dict")
    return values

def getAVCQualityInfoSQL(index):
    cmd = 'SELECT * FROM {}'.format(index)
    values = mysql_query(host=host,username=username, password=password,database=Native_DB,cmd=cmd,cursorclass="dict")
    return values

def getAVCQualityInfoByNoSQL(No,index):
    cmd = 'SELECT * FROM ' + index+' where No ='+json.dumps(No)
    values = mysql_query(host=host,username=username, password=password,database=Native_DB,cmd=cmd,cursorclass="dict")
    return values

def updateAVCQualityInfoByNoSQL(data):
    if data.get("database")[0] == "AVC_Quality_Crash":
        cmd = "update AVC_Quality_Crash set Platform='{Platform[0]}',Version='{Version[0]}',Time='{Time[0]}',Value='{Value[0]}' where No={No[0]}".format(**data)
    else:
        cmd = "update AVC_Quality_Count set Platform='{Platform[0]}',Native='{Native[0]}',RTM='{RTM[0]}',WebRTC='{WebRTC[0]}',Doc='{Doc[0]}',App='{App[0]}',Time='{Time[0]}' where No={No[0]}".format(**data)
    res = mysql_update(host=host,username=username, password=password,database=Native_DB,cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res

def insertAVCQualityInfoByNoSQL(data):
    if data.get("database")[0] == "AVC_Quality_Crash":
        cmd = "INSERT INTO AVC_Quality_Crash set Platform='{Platform[0]}',Version='{Version[0]}',Time='{Time[0]}',Value='{Value[0]}'".format(**data)
    else:
        cmd = "INSERT INTO AVC_Quality_Count set Platform='{Platform[0]}',Native='{Native[0]}',RTM='{RTM[0]}',WebRTC='{WebRTC[0]}',Doc='{Doc[0]}',App='{App[0]}',Time='{Time[0]}'".format(**data)
    res = mysql_update(host=host,username=username, password=password,database=Native_DB,cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res

def deleteAVCQualityInfoByNoSQL(data):
    cmd = "DELETE FROM {database[0]} where No='{No[0]}'".format(**data)
    res = mysql_update(host=host,username=username, password=password,database=Native_DB,cmd=cmd)
    addTestToolLogSerever(session.get('username'), cmd)
    return res