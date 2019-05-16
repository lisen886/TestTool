import testlink,json,sys
url = 'http://10.80.0.220/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
key = '83301958459ed090e8cf01f4d1832bce'
tlc = testlink.TestlinkAPIClient(url, key)
# tlc.listProjects()
def get_project():
    projects = []
    projectsInfo = tlc.getProjects()
    for project in projectsInfo:
        projects.append({"projectName":project['name'],"projectID":project['id']})
    return projects

def get_projectID(projectName):
    projects = get_project()
    for project in projects:
        if projectName == project["projectName"]:
            return project["projectID"]
    else:
        return False

def get_projectName():
    projectNames = []
    projectsInfo = tlc.getProjects()
    for project in projectsInfo:
        projectNames.append(project['name'])
    return projectNames

def get_project_testPlanName(projectName):
    projectID = get_projectID(projectName)
    if projectID:
        testPlans = []
        tps = tlc.getProjectTestPlans(projectID)
        for tp in tps:
            testPlans.append(tp["name"])
        return testPlans
    else:
        return False
def get_testcasenumber(dic_json):
    casenum = 0
    all_pass = 0
    all_fail = 0
    all_block = 0
    all_no_run = 0
    if isinstance(dic_json, dict):
        for key in dic_json:
            if isinstance(dic_json[key], dict):
                casenum += len(dic_json[key])
                for key2 in dic_json[key]:
                    if dic_json[key][key2]["exec_status"] == "p":
                        all_pass += 1
                    elif dic_json[key][key2]["exec_status"] == "f":
                        all_fail += 1
                    elif dic_json[key][key2]["exec_status"] == "b":
                        all_block += 1
                    elif dic_json[key][key2]["exec_status"] == "n":
                        all_no_run += 1
    run = all_pass + all_fail + all_block
    print("*******caseNum : %d, all run : %d, not run : %d*******" % (casenum,run,all_no_run))
    return casenum,run,all_no_run

def get_testplan_progress(projectID,testPlan):
    tps = tlc.getProjectTestPlans(projectID)
    runALL = 0
    caseALL = 0
    for tp in tps:
        if testPlan == tp["name"]:
            # print(tp["name"])
            cases = tlc.getTestCasesForTestPlan(tp["id"])
            caseNum,run,notrun=get_testcasenumber(cases)
            caseALL += caseNum
            runALL += run
            rate = float('%.2f' % (runALL / caseALL))*100
            # print('\033[1;35m  caseAll:%d, run:%d, rate:%0.2f %%\033[0m' % (caseALL,runALL,rate))
            return rate
    else:
        return False


