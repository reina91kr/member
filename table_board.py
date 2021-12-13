import sqlite3 as sql

def getconn():
    conn = sql.connect("./memberdb.db")
    return conn

def create_table():
    conn = getconn()
    cur = conn.cursor()
    sql = """
    CREATE TABLE board(
        bno         INTEGER     PRIMARY KEY     AUTOINCREMENT,
        title       TEXT        NOT NULL,
        content     TEXT        NOT NULL,
        create_date TIMESTAMP DATE DEFAULT(datetime('now', 'localtime')),
        mid         CHAR(5)     NOT NULL,
        FOREIGN KEY(mid) REFERENCES member(mid)
    """
    # bno - 글번호, title - 글제목, content - 글 내용, create_date - 작성일자, mid - 글쓴이
    cur.execute(sql)
    conn.commit()
    print("board 테이블 생성!")
    conn.close()


create_table()

