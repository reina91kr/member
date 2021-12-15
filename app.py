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
        pwd = request.form['passwd']
        name = request.form['name']
        age = request.form['age']
        # date = request.form['regDate']

        conn = getconn()
        cur = conn.cursor()
        sql = "INSERT INTO member (mid, passwd, name, age) VALUES ('%s', '%s', '%s', %s)" % (id, pwd, name, age)
        cur.execute(sql)
        conn.commit()
        sql = "SELECT * FROM member WHERE mid = '%s'" % (id)
        cur.execute(sql)
        rs = cur.fetchone()
        if rs:
            session['userID'] = rs[0]       # 아이디 세션 발급
            session['userName'] = rs[2]     # 이름 세션 발급
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
            session['userID'] = rs[0]               #아이디 세션 발급
            session['userName'] = rs[2]             #이름 세션 발급
            return redirect(url_for('index'))
        else:
            error = "아이디나 비밀번호가 일치하지 않습니다."
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/logout/')
def logout():
    session.pop('userName')       #세션 삭제
    return redirect(url_for('index'))

@app.route('/member_del/<string:id>')       #삭제URL 만들기
def member_del(id):     #mid를 매개변수로 넘겨줌
    conn = getconn()
    cur = conn.cursor()
    sql = "DELETE FROM member WHERE mid = '%s'" % (id)
    cur.execute(sql)
    conn.commit()
    conn.close()

    return redirect(url_for('memberlist'))

@app.route('/member_edit/<string:id>', methods = ['GET','POST'])
def member_edit(id):
    if request.method=="POST":
        #자료 넘겨받기
        id = request.form['mid']
        pwd = request.form['passwd']
        name = request.form['name']
        age = request.form['age']
        # date = request.form['regDate']

        #db 연결
        conn = getconn()
        cur = conn.cursor()
        sql = "UPDATE member SET passwd='%s', name='%s', age = %s WHERE mid='%s'" % (pwd, name, age, id)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect(url_for('member_view', id=id))  # url 경로로 이동
    else:
        #회원 자료 가져오기
        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE mid = '%s'" % (id)
        cur.execute(sql)
        rs = cur.fetchone()
        conn.close()
        return render_template('member_edit.html', rs=rs)

@app.route('/boardlist/')
def boardlist():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM board ORDER BY bno DESC"       #게시글을 내림차순으로 정렬
    cur.execute(sql)
    rs = cur.fetchall()
    conn.close()
    return render_template('boardlist.html', rs = rs)

@app.route('/writing/', methods = ['GET','POST'])
def writing():
    if request.method == "POST":
        #자료 전달받기
        title = request.form['title']
        content = request.form['content']  #index는 대괄호
        mid = session.get('userName')     #글쓴이 = 로그인한 사람 / #get함수는 ()

        #db 연결하기
        conn = getconn()
        cur = conn.cursor()
        sql = "INSERT INTO board (title, content, mid) VALUES ('%s', '%s', '%s')" % (title, content, mid)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect (url_for('boardlist'))

    else:
        return render_template('writing.html')

@app.route('/board_view/<int:bno>/')
def board_view(bno):
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM board WHERE bno = %s" % (bno)
    cur.execute(sql)
    rs = cur.fetchone()
    conn.close()
    return render_template('board_view.html', rs = rs)

# 게시글 삭제
@ app.route('/board_del/<int:bno>/')
def board_del(bno):
    conn = getconn()
    cur = conn.cursor()
    sql = "DELETE FROM board WHERE bno = %s" % (bno)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return redirect(url_for('boardlist'))

#게시글 수정
@ app.route('/board_edit/<int:bno>/', methods=['GET', 'POST'])
def board_edit(bno):
    if request.method == "POST":    #POST방식 (수정하고 다시 보내주는 방식)
        #자료 전달 받음
        title = request.form['title']
        content = request.form['content']
        mid = session.get('userName') #자동입력

        conn = getconn()
        cur = conn.cursor()
        sql = "UPDATE board SET title = '%s', content ='%s', mid = '%s' WHERE bno = %s" % (title, content, mid, bno)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect(url_for('board_view', bno = bno))  # url 경로로 이동

    else:       #GET 방식 (board_view와 비슷)
        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM board WHERE bno = %s" % (bno)
        cur.execute(sql)
        rs = cur.fetchone()
        conn.close()
        return render_template('board_edit.html', rs = rs)

app.run(debug=True)
