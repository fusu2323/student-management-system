# -*- coding: utf-8 -*-
"""学生信息管理系统 - 数据库模块"""
import os,sqlite3,hashlib
TIDB_CONFIG={
    "host":"gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    "port":4000,
    "user":"23fjQ2u7KMmNNeg.root",
    "password":"KSxZ9Cy61SdOxe5p",
    "database":"student_db",
    "charset":"utf8mb4",
    "ssl":{"ssl":True},
    "autocommit":True,
}
DB_TYPE="sqlite";MYSQL_CONFIG={}
SQLITE_PATH=os.path.join(os.path.dirname(__file__),"student.db")
try:
    import pymysql
    tc=pymysql.connect(**TIDB_CONFIG)
    tc.close()
    DB_TYPE="mysql";MYSQL_CONFIG=TIDB_CONFIG
    print("[DB] TiDB Cloud 连接成功")
except Exception:
    print("[DB] SQLite 模式")

def get_connection():
    if DB_TYPE=="mysql":return pymysql.connect(**MYSQL_CONFIG)
    conn=sqlite3.connect(SQLITE_PATH);conn.row_factory=sqlite3.Row;return conn

def qmark():return"%s" if DB_TYPE=="mysql" else"?"

def init_database():
    conn=get_connection();cur=conn.cursor()
    if DB_TYPE=="mysql":
        for s in[
            "CREATE TABLE IF NOT EXISTS users(id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(50) UNIQUE NOT NULL,password VARCHAR(128) NOT NULL,created_at DATETIME DEFAULT CURRENT_TIMESTAMP)ENGINE=InnoDB CHARSET=utf8mb4",
            "CREATE TABLE IF NOT EXISTS majors(id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(50) UNIQUE NOT NULL,department VARCHAR(50),created_at DATETIME DEFAULT CURRENT_TIMESTAMP)ENGINE=InnoDB CHARSET=utf8mb4",
            "CREATE TABLE IF NOT EXISTS classes(id INT AUTO_INCREMENT PRIMARY KEY,class_name VARCHAR(50) UNIQUE NOT NULL,major_id INT NOT NULL,grade VARCHAR(10),FOREIGN KEY(major_id)REFERENCES majors(id))ENGINE=InnoDB CHARSET=utf8mb4",
            "CREATE TABLE IF NOT EXISTS students(id INT AUTO_INCREMENT PRIMARY KEY,student_id VARCHAR(20) UNIQUE NOT NULL,name VARCHAR(50) NOT NULL,gender VARCHAR(4) DEFAULT'男',birth_date DATE,class_id INT NOT NULL,enrollment_year VARCHAR(10),phone VARCHAR(20),address VARCHAR(200),FOREIGN KEY(class_id)REFERENCES classes(id))ENGINE=InnoDB CHARSET=utf8mb4",
        ]:cur.execute(s)
    else:
        for s in[
            "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL,password TEXT NOT NULL,created_at TEXT DEFAULT(datetime('now','localtime')))",
            "CREATE TABLE IF NOT EXISTS majors(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT UNIQUE NOT NULL,department TEXT,created_at TEXT DEFAULT(datetime('now','localtime')))",
            "CREATE TABLE IF NOT EXISTS classes(id INTEGER PRIMARY KEY AUTOINCREMENT,class_name TEXT UNIQUE NOT NULL,major_id INTEGER NOT NULL,grade TEXT,FOREIGN KEY(major_id)REFERENCES majors(id))",
            "CREATE TABLE IF NOT EXISTS students(id INTEGER PRIMARY KEY AUTOINCREMENT,student_id TEXT UNIQUE NOT NULL,name TEXT NOT NULL,gender TEXT DEFAULT'男',birth_date TEXT,class_id INTEGER NOT NULL,enrollment_year TEXT,phone TEXT,address TEXT,FOREIGN KEY(class_id)REFERENCES classes(id))",
        ]:cur.execute(s)
    pwd=hashlib.sha256("abc123".encode()).hexdigest()
    cur.execute(f"SELECT id FROM users WHERE username={qmark()}",("kitty",))
    if not cur.fetchone():cur.execute(f"INSERT INTO users(username,password)VALUES({qmark()},{qmark()})",("kitty",pwd))

    cur.execute("SELECT COUNT(*)as cnt FROM majors")
    if(cur.fetchone()[0]if DB_TYPE=="mysql" else cur.fetchone()["cnt"])==0:
        for m in[("计算机科学与技术","计算机学院"),("软件工程","计算机学院"),("数字媒体技术","信息工程学院"),("数据科学与大数据技术","信息工程学院"),("人工智能","计算机学院")]:
            cur.execute(f"INSERT INTO majors(name,department)VALUES({qmark()},{qmark()})",m)

    cur.execute("SELECT COUNT(*)as cnt FROM classes")
    if(cur.fetchone()[0]if DB_TYPE=="mysql" else cur.fetchone()["cnt"])==0:
        for c in[("数媒25101班",3,"2025"),("数媒25102班",3,"2025"),("计科25101班",1,"2025"),("计科25102班",1,"2025"),("软工25101班",2,"2025"),("大数据25101班",4,"2025"),("人工智能25101班",5,"2025")]:
            cur.execute(f"INSERT INTO classes(class_name,major_id,grade)VALUES({qmark()},{qmark()},{qmark()})",c)

    cur.execute("SELECT COUNT(*)as cnt FROM students")
    if(cur.fetchone()[0]if DB_TYPE=="mysql" else cur.fetchone()["cnt"])==0:
        for s in[
            ("2024001","张三","男","2005-03-15",1,"2025","13800138001","南京市鼓楼区"),
            ("2024002","李四","女","2005-07-22",1,"2025","13800138002","南京市玄武区"),
            ("2024003","王五","男","2005-11-08",1,"2025","13800138003","南京市建邺区"),
            ("2024004","赵六","女","2005-06-30",2,"2025","13800138004","南京市秦淮区"),
            ("2024005","陈七","男","2004-12-01",2,"2025","13800138005","南京市栖霞区"),
            ("2024006","周八","女","2005-09-18",3,"2025","13800138006","南京市雨花台区"),
            ("2024007","吴九","男","2005-04-25",3,"2025","13800138007","南京市江宁区"),
            ("2024008","郑十","女","2004-08-12",4,"2025","13800138008","南京市浦口区"),
            ("2024009","刘廿","男","2005-01-05",5,"2025","13800138009","南京市六合区"),
            ("2024010","孙悦","女","2005-10-20",6,"2025","13800138010","南京市溧水区"),
        ]:cur.execute(f"INSERT INTO students(student_id,name,gender,birth_date,class_id,enrollment_year,phone,address)VALUES({qmark()},{qmark()},{qmark()},{qmark()},{qmark()},{qmark()},{qmark()},{qmark()})",s)
    conn.commit();conn.close()

def verify_user(u,p):
    conn=get_connection();cur=conn.cursor();h=hashlib.sha256(p.encode()).hexdigest()
    cur.execute(f"SELECT*FROM users WHERE username={qmark()}AND password={qmark()}",(u,h));r=cur.fetchone();conn.close();return dict(r)if r else None

# Majors
def get_majors():
    conn=get_connection();cur=conn.cursor();cur.execute("SELECT*FROM majors ORDER BY id");rows=[dict(r)for r in cur.fetchall()];conn.close();return rows

def add_major(name,dept):
    conn=get_connection();cur=conn.cursor()
    try:cur.execute(f"INSERT INTO majors(name,department)VALUES({qmark()},{qmark()})",(name,dept));conn.commit();return True,"添加成功"
    except Exception as e:return False,str(e)
    finally:conn.close()

# Classes
def get_classes(major_id=None):
    conn=get_connection();cur=conn.cursor();sql="SELECT c.*,m.name as major_name FROM classes c JOIN majors m ON c.major_id=m.id WHERE 1=1";params=[]
    if major_id:sql+=f" AND c.major_id={qmark()}";params.append(major_id)
    cur.execute(sql+" ORDER BY c.class_name",params);rows=[dict(r)for r in cur.fetchall()];conn.close();return rows

def add_class(name,major_id,grade):
    conn=get_connection();cur=conn.cursor()
    try:cur.execute(f"INSERT INTO classes(class_name,major_id,grade)VALUES({qmark()},{qmark()},{qmark()})",(name,major_id,grade));conn.commit();return True,"添加成功"
    except Exception as e:return False,str(e)
    finally:conn.close()

def update_class(cid,name,major_id,grade):
    conn=get_connection();cur=conn.cursor()
    try:cur.execute(f"UPDATE classes SET class_name={qmark()},major_id={qmark()},grade={qmark()} WHERE id={qmark()}",(name,major_id,grade,cid));conn.commit();return True,"更新成功"
    except Exception as e:return False,str(e)
    finally:conn.close()

def delete_class(cid):
    conn=get_connection();cur=conn.cursor()
    cur.execute(f"SELECT COUNT(*)as cnt FROM students WHERE class_id={qmark()}",(cid,))
    if(cur.fetchone()[0]if DB_TYPE=="mysql" else cur.fetchone()["cnt"])>0:conn.close();return False,"该班级下有学生，无法删除"
    cur.execute(f"DELETE FROM classes WHERE id={qmark()}",(cid,));conn.commit();conn.close();return True,"删除成功"

# Students
def add_student(sid,name,gender,birth,class_id,enrollment_year,phone,address):
    conn=get_connection();cur=conn.cursor()
    try:cur.execute(f"INSERT INTO students(student_id,name,gender,birth_date,class_id,enrollment_year,phone,address)VALUES({qmark()},{qmark()},{qmark()},{qmark()},{qmark()},{qmark()},{qmark()},{qmark()})",(sid,name,gender,birth,class_id,enrollment_year,phone,address));conn.commit();return True,"添加成功"
    except Exception as e:return False,str(e)
    finally:conn.close()

def query_students(kw=None,class_id=None,gender=None,enrollment_year=None):
    conn=get_connection();cur=conn.cursor()
    sql="SELECT s.*,c.class_name,m.name as major_name FROM students s JOIN classes c ON s.class_id=c.id JOIN majors m ON c.major_id=m.id WHERE 1=1";params=[]
    if kw:sql+=f" AND (s.name LIKE {qmark()} OR s.student_id LIKE {qmark()})";params.extend([f"%{kw}%",f"%{kw}%"])
    if class_id and class_id!="全部":sql+=f" AND s.class_id={qmark()}";params.append(class_id)
    if gender and gender!="全部":sql+=f" AND s.gender={qmark()}";params.append(gender)
    if enrollment_year and enrollment_year!="全部":sql+=f" AND s.enrollment_year={qmark()}";params.append(enrollment_year)
    cur.execute(sql+" ORDER BY s.student_id",params);rows=[dict(r)for r in cur.fetchall()];conn.close();return rows

def update_student(sid,student_id,name,gender,birth,class_id,enrollment_year,phone,address):
    conn=get_connection();cur=conn.cursor()
    try:cur.execute(f"UPDATE students SET student_id={qmark()},name={qmark()},gender={qmark()},birth_date={qmark()},class_id={qmark()},enrollment_year={qmark()},phone={qmark()},address={qmark()} WHERE id={qmark()}",(student_id,name,gender,birth,class_id,enrollment_year,phone,address,sid));conn.commit();return True,"更新成功"
    except Exception as e:return False,str(e)
    finally:conn.close()

def delete_student(sid):
    conn=get_connection();cur=conn.cursor()
    try:cur.execute(f"DELETE FROM students WHERE id={qmark()}",(sid,));conn.commit();return True,"删除成功"
    except Exception as e:return False,str(e)
    finally:conn.close()

def get_statistics():
    conn=get_connection();cur=conn.cursor();s={}
    cur.execute("SELECT COUNT(*)as cnt FROM students");s["total_students"]=cur.fetchone()["cnt"if DB_TYPE=="sqlite" else 0]
    cur.execute("SELECT COUNT(*)as cnt FROM majors");s["total_majors"]=cur.fetchone()["cnt"if DB_TYPE=="sqlite" else 0]
    cur.execute("SELECT COUNT(*)as cnt FROM classes");s["total_classes"]=cur.fetchone()["cnt"if DB_TYPE=="sqlite" else 0]
    cur.execute("SELECT gender,COUNT(*)as cnt FROM students GROUP BY gender");s["gender_stats"]=[dict(r)for r in cur.fetchall()]
    cur.execute("""SELECT c.class_name,m.name as major_name,COUNT(s.id)as cnt
        FROM classes c JOIN majors m ON c.major_id=m.id LEFT JOIN students s ON s.class_id=c.id
        GROUP BY c.id ORDER BY cnt DESC""");s["class_stats"]=[dict(r)for r in cur.fetchall()]
    cur.execute("""SELECT m.name,COUNT(s.id)as cnt
        FROM majors m LEFT JOIN classes c ON c.major_id=m.id LEFT JOIN students s ON s.class_id=c.id
        GROUP BY m.id ORDER BY cnt DESC""");s["major_stats"]=[dict(r)for r in cur.fetchall()]
    cur.execute("SELECT enrollment_year,COUNT(*)as cnt FROM students WHERE enrollment_year IS NOT NULL AND enrollment_year!='' GROUP BY enrollment_year ORDER BY enrollment_year");s["year_stats"]=[dict(r)for r in cur.fetchall()]
    conn.close();return s

if __name__=="__main__":init_database();print("OK")
