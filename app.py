import sqlite3

from flask import Flask, render_template

app = Flask(__name__)

def getconn():
    conn = sqlite3.connect('./memberdb.db')
    return conn

@app.route('/')
def index():
    return render_template('index.html')


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

app.run(debug=True)
