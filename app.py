# -*- coding:utf-8 -*-
from flask import render_template,send_from_directory,Flask,request,jsonify,Response,abort,session,redirect,url_for
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
import platform,time,random
from script.lib import *
from script.countTestPlan import *
from script.excel2xml import *
import script.excel2jira as e2j
app = Flask(__name__)
app.secret_key="asdada1231"
bootstrap = Bootstrap(app)
root_cwd = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])
file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
@app.before_request
def before_request():
    if request.path == "/login/" or request.path == "/register" or request.path == "/insertSQL":
        return None
    if request.path == "/static/css/style.css" or request.path == "/static/js/vector.js" or request.path == "/static/img/TestTool.png":
        return None
    if "username" not in session:
        return redirect("/login/")
    return None

@app.route("/")
def index():
     return render_template("index.html")

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = getUserInfo(username)
        if user:
            if username == str(list(user[0])[0]) and password == str(list(user[0])[2]):
                session['username'] = username
                session.permanent = True
                # return redirect(url_for('index'))
                # return render_template("index.html")
                return redirect('/')
            # else:
                # return render_template("login.html")
        else:
            return redirect('/register')
    return render_template("login.html")

@app.context_processor
def my_context_processor():
    user = session.get('username')
    if user:
        return {'login_user': user}
    return {}

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/users",methods=['GET','POST'])
def showUser():
    values = getValue()
    return render_template("showDir/users.html",value=values)

@app.route("/setting",methods=['GET','POST'])
def showSetting():
    configs = getConfigs()
    return render_template("showDir/showSetting.html",value=configs)

@app.route("/getConfig",methods=['GET','POST'])
def getConfig():
    configs = getConfigs()
    if configs != False:
        config_dict = {}
        for config in configs:
            config_dict[config[1]]=config[2]
        return jsonify({'status': 200, 'message': config_dict})
    else:
        return jsonify({'status': 400, 'message': 'error'})

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
            session['username'] = name
            session.permanent = True
            return redirect("/")
        else:
            return render_template("register.html")

@app.route('/deleteUser',methods=['POST','GET'])
def deleteUser():
    userName=request.form.get('catename')
    status = deleteUserInfo(userName)
    if status != False:
        if session.get('username') == userName:
            session.pop('username')
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

@app.route('/updateConfig',methods=['POST','GET'])
def updateConfig():
    name=request.form.get('Name')
    value=request.form.get('value')
    status = updateConfigInfo(name,value)
    if status != False:
        return jsonify({'status': 200, 'message': 'pass'})
    else:
        return jsonify({'status': 400, 'message': 'error'})

@app.route("/excel2xml",methods=['GET','POST'])
def showExcel2xml():
    xmls = get__xmlfile(file_dir)
    return render_template("showDir/excel2xml.html",files =xmls)

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

# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 上传文件
@app.route('/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['file']  # 从表单的file字段获取文件，myfile为该表单的name值
    fileName = "".join(f.filename.split())
    if f and allowed_file(fileName):  # 判断是否是允许上传的文件类型
        # fname = secure_filename(f.filename)  # 获取安全的文件名，中文解决：https://blog.csdn.net/weixin_33725126/article/details/88268067
        # ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        # unix_time = int(time.time())
        # new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
        file = os.path.join(file_dir, fileName)
        f.save(file)  # 保存文件到upload目录
        generate_xml(file)
        xml_file_name = fileName.split(".")[0]+".xml"
        datas = {"status": 200, "msg": xml_file_name}
    else:
        datas = {"status": 501, "msg": fileName}
    content = json.dumps(datas)
    resp = Response_headers(content)
    return resp

# 上传文件
@app.route('/upload_excel2jira', methods=['POST'], strict_slashes=False)
def upload_excel2jira():
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['file']  # 从表单的file字段获取文件，myfile为该表单的name值
    userName = request.form.get('userName')
    passWord = request.form.get('passWord')
    checkJiraExistFlag = request.form.get('checkJiraExistFlag')
    fileName = "".join(f.filename.split())
    if f and allowed_file(fileName):  # 判断是否是允许上传的文件类型
        file = os.path.join(file_dir, fileName)
        f.save(file)
        try:
            resList = e2j.excel2jira(userName, passWord,checkJiraExistFlag).import2jira(file)
        except Exception as e:
            resList = [e.args]
        datas = {"status": 200, "msg": resList}
    else:
        datas = {"status": 501, "msg": fileName}
    content = json.dumps(datas)
    resp = Response_headers(content)
    return resp

@app.route('/download/<filename>', methods=['GET','POST'], strict_slashes=False)
def download(filename):
    if request.method=="GET":
        file = secure_filename(filename)
        if file == "ExcelTemplate.xlsx":
            if os.path.isfile(os.path.join('script', file)):
                return send_from_directory('script',file.encode('utf-8').decode('utf-8'), as_attachment=True)
            abort(404)
        else:
            if os.path.isfile(os.path.join('upload', file)):
                return send_from_directory('upload',file.encode('utf-8').decode('utf-8'), as_attachment=True)
            abort(404)

@app.route('/deleteFile/<filename>', methods=['GET','POST'], strict_slashes=False)
def deleteFile(filename):
    if request.method=="GET":
        file = secure_filename(filename)
    elif request.method == "POST":
        file = request.form.get('catename')
    if os.path.isfile(os.path.join('upload', file)):
        filefirstname = os.path.join(file_dir, file).split(".")[0]
        print("要删除的文件：%s"% filefirstname)
        sysstr = platform.system()
        if (sysstr == "Windows"):
            cmd = "del "+filefirstname+".*"
        else:
            cmd = "rm "+filefirstname+".*"
        try:
            os.system(cmd)
            datas = {"status": 200, "msg": "源文件删除成功"}
        except:
            datas = {"status": 401, "msg": "源文件删除失败"}
        content = json.dumps(datas)
        resp = Response_headers(content)
        return resp

@app.route("/showPerf",methods=['GET','POST'])
def showPerf():
    values = getPerKeyInfo()
    versions = values.get("version")
    browsers = values.get("browser")
    modes = values.get("mode")
    codecs = values.get("codec")
    return render_template("showDir/showReport.html", versions=versions, browsers=browsers, modes=modes, codecs=codecs)

@app.route("/getCPUMEM",methods=['GET','POST'])
def getCPUMEM():
    xlist = []
    cpulist = []
    memlist = []
    for i in range(20):
        xlist.append(time.strftime('%H:%M:%S', time.localtime(time.time())))
        cpulist.append(random.randint(0,300))
        memlist.append(random.randint(200,400))
    datas = {
        "xcontent": xlist,
        "data": [{"name":"CPU","data":cpulist},{"name":"内存","data":memlist}]
    }
    content = json.dumps(datas)
    resp = Response_headers(content)
    return resp

@app.route("/showQearyResult",methods=['GET','POST'])
def showQearyResult():
    version_checkList = request.form.get('version_check')
    browser_checkList = request.form.get('browser_check')
    mode_checkList = request.form.get('mode_check')
    codec_checkList = request.form.get('codec_check')
    index_checkList = request.form.get('index_check')
    info_dict = getPerInfo(index_checkList,version_checkList,browser_checkList,mode_checkList,codec_checkList)
    new_data = []
    for browser in json.loads(browser_checkList):
        for mode in json.loads(mode_checkList):
            for codec in json.loads(codec_checkList):
                if browser == 'safari' and codec == "vp8":
                    continue
                for key in info_dict.keys():
                    new_xlist = []
                    new_value = []
                    for value in info_dict[key]:
                        if browser in value and mode in value and codec in value:
                            new_xlist.append(value[1])
                            new_value.append(value[5])
                    new_data.append({"name":"_".join([key,browser,mode,codec]),
                                     "data":new_value,
                                     "xcontent":new_xlist
                                     })

    datas = {
        "data": new_data
    }
    content = json.dumps(datas)
    resp = Response_headers(content)
    return resp

@app.route("/excel2jira")
def api_excel2jira():
     return render_template("showDir/excel2jira.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8888)