from flask import render_template,send_from_directory,Flask,request,jsonify,Response
from flask_bootstrap import Bootstrap
import os
from script.lib import *
from script.countTestPlan import *
app = Flask(__name__)
bootstrap = Bootstrap(app)
root_cwd = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/index",methods = ['POST'])
def index():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = getUserInfo(username)
        if user:
            if username == str(list(user[0])[0]) and password == str(list(user[0])[2]):
                return render_template("index.html")
            else:
                return "<h1>login Failure !</h1>"
        else:
            return "<h1>login Failure !</h1>"
@app.route("/index.html",methods=['GET','POST'])
def showHome():
    return render_template("index.html")


@app.route("/users",methods=['GET','POST'])
def showUser():
    values = getValue()
    return render_template("showDir/users.html",value=values)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/insertSQL",methods = ['POST'])
def insertSQL():
    if request.method == "POST":
        name = request.form.get('inputName')
        password = request.form.get('inputPassword')
        team = request.form.get('inputTeam')
        tel = request.form.get('inputTel')
        status = registerUser((name,team,password,tel))
        if status != False:
            return render_template("index.html")
        else:
            return render_template("register.html")

@app.route('/deleteUser',methods=['POST','GET'])
def deleteUser():
    userName=request.form.get('catename')
    status = deleteUserInfo(userName)
    if status != False:
        return jsonify({'status': 200, 'message': 'pass'})
    else:
        return jsonify({'status': 400, 'message': 'error'})

@app.route('/updateUser',methods=['POST','GET'])
def updateUser():
    userName=request.form.get('userName')
    team=request.form.get('team')
    password=request.form.get('password')
    tel=request.form.get('tel')
    status = updateUserInfo(userName,userName,team,password,tel)
    if status != False:
        return jsonify({'status': 200, 'message': 'pass'})
    else:
        return jsonify({'status': 400, 'message': 'error'})

@app.route("/excel2xml",methods=['GET','POST'])
def showExcel2xml():
    return render_template("showDir/excel2xml.html")

@app.route("/getTestProgress",methods=['GET','POST'])
def showGetTestProgress():
    projectNames = get_projectName()
    return render_template("showDir/testProgress.html",names=projectNames)

def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/getTestPlan',methods=['POST','GET'])
def getTestPlan():
    project = request.form.get('testProject')
    testPlans = get_project_testPlanName(project)
    dataList = []
    for testPlan in testPlans:
        dataList.append({"name":testPlan})
    datas = {
        "data": dataList
    }
    content = json.dumps(datas)
    resp = Response_headers(content)
    return resp

@app.route('/getProcessChart',methods=['POST','GET'])
def getProcessChart():
    testPlan = request.form.get('testPlan')
    testproject = request.form.get('testproject')
    projectID = get_projectID(testproject)
    progress = get_testplan_progress(projectID,testPlan)
    dataList = []
    dataList.append({"name": testPlan, "rate": progress})
    datas = {
        "data": dataList
    }
    content = json.dumps(datas)
    resp = Response_headers(content)
    return resp
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8888)