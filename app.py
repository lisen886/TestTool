from flask import render_template,send_from_directory,Flask,request,jsonify,Response,abort,session
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
import os,time,base64
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


UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 上传文件
@app.route('/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['file']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = secure_filename(f.filename)
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        return jsonify({"errno": 0, "errmsg": "上传成功"})
    else:
        return jsonify({"errno": 1001, "errmsg": "上传失败"})

@app.route('/download/<filename>', methods=['GET','POST'], strict_slashes=False)
def download(filename):
    print(filename)
    # if request.method=="GET":
    #     if os.path.isfile(os.path.join('upload', filename)):
    #         return send_from_directory('upload',filename.encode('utf-8').decode('utf-8'), as_attachment=True)
    #     abort(404)
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8888)