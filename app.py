from flask import render_template,send_from_directory,Flask,request,jsonify
from flask_bootstrap import Bootstrap
import os
from script.lib import *
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
def show():
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

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8888)