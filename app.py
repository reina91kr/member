import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "wkddbswl" #암호키 설정

def getconn():
    conn = sqlite3.connect('./memberdb.db')
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/navbar/')
def navbar():
    return render_template('navbar.html')

@app.route('/memberlist/')
def memberlist():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member"
    cur.execute(sql)
    rs = cur.fetchall()     #db에서 가져온 데이터
    conn.close()
    return render_template('memberlist.html', rs=rs)    #받은 db를 다시 html로 보냄

@app.route('/member_view/<string:id>')
def member_view(id):     #id를 경로로 설정하고 매개변수 넘겨줌
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member WHERE mid = '%s' " % id
    cur.execute(sql)
    rs = cur.fetchone()
    conn.close()
    return render_template('member_view.html', rs = rs)

@app.route('/register/', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        #자료 수집하기
        id = request.form['mid']
        pwd = request.form['passwd1']
        name = request.form['name']
        age = request.form['age']
        date = request.form['regDate']

        conn = getconn()
        cur = conn.cursor()
        sql = "INSERT INTO member VALUES ('%s', '%s', '%s', '%s', '%s')" % (id, pwd, name, age, date)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect(url_for('memberlist'))   #url 경로로 이동

    else:
        return render_template('register.html') #get방식

@app.route("/login/", methods = ['GET', 'POST'])
def login():
    if request.method == "POST": #'POST'는 반드시 대문자 사용
        #자료 수집하기
        id = request.form['mid']
        pwd = request.form['passwd']

        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE mid = '%s' AND passwd = '%s'" % (id, pwd)
        cur.execute(sql)
        rs = cur.fetchone()
        conn.close()
        if rs:
            session['userID'] = id              #세션 발급
            return redirect(url_for('index'))
        else:
            error = "아이디나 비밀번호가 일치하지 않습니다."
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/logout/')
def logout():
    session.pop('userID')       #세션 삭제
    return redirect(url_for('index'))

app.run(debug=True)
