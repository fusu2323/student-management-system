# -*- coding: utf-8 -*-
"""学生信息管理系统 - Streamlit"""
import streamlit as st
import pandas as pd
from database import *

st.set_page_config(page_title="学生信息管理系统",page_icon="",layout="wide",initial_sidebar_state="expanded")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:"Nunito",system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14px;color:#2d1b2e;background:#fff8fa}
.stButton>button{font-size:13px;height:32px;padding:0 16px;border-radius:8px;border:2px solid #f0c4d8;background:#fff;color:#2d1b2e;font-weight:600;transition:all .2s;box-shadow:0 1px 3px rgba(255,107,157,.1)}
.stButton>button:hover{background:#fff0f5;border-color:#ff6b9d;transform:translateY(-1px);box-shadow:0 2px 8px rgba(255,107,157,.2)}
.stButton>button:active{transform:translateY(0);box-shadow:none}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#ff6b9d,#ff8e53);border-color:transparent;color:#fff;box-shadow:0 2px 8px rgba(255,107,157,.3)}
.stButton>button[kind="primary"]:hover{box-shadow:0 4px 16px rgba(255,107,157,.4);transform:translateY(-1px)}
.stButton>button[kind="primary"]:active{transform:translateY(0)}
.stTextInput input,.stNumberInput input{font-size:13px;height:32px;min-height:32px;border-radius:8px;border:2px solid #f0c4d8;background:#fff;color:#2d1b2e;padding:0 12px}
.stTextInput input:focus,.stNumberInput input:focus{border-color:#ff6b9d;box-shadow:0 0 0 3px rgba(255,107,157,.12);outline:none}
.stSelectbox [data-baseweb="select"]>div{font-size:13px;height:32px;min-height:32px;border-radius:8px;border:2px solid #f0c4d8;background:#fff}
.stSelectbox [data-baseweb="select"]>div:focus-within{border-color:#ff6b9d;box-shadow:0 0 0 3px rgba(255,107,157,.12)}
label,.stSelectbox label,.stTextInput label{font-size:12px;font-weight:600;color:#b86b8a;margin-bottom:4px;text-transform:uppercase;letter-spacing:.04em}
.stDataFrame{font-size:13px}
.stDataFrame thead th{font-size:12px;font-weight:600;color:#b86b8a;background:linear-gradient(180deg,#fff0f5,#fff);border-bottom:2px solid #f0c4d8;padding:10px 14px}
.stDataFrame tbody td{border-bottom:1px solid #fde8f0;padding:9px 14px}
.stDataFrame tbody tr:hover td{background:#fff5f8}
[data-testid="stMetricValue"]{font-size:28px;font-weight:800;color:#ff6b9d}
[data-testid="stMetricLabel"]{font-size:12px;color:#b86b8a;font-weight:600}
[data-testid="stMetric"]{background:linear-gradient(135deg,#fff0f5,#fff8fa);border:2px solid #fde8f0;border-radius:10px;padding:16px;text-align:center}
.stTabs [data-baseweb="tab-list"]{gap:4px;border-bottom:2px solid #f0c4d8;padding-bottom:0}
.stTabs [data-baseweb="tab"]{font-size:13px;padding:10px 20px;border-radius:10px 10px 0 0;border:2px solid transparent;color:#b86b8a;font-weight:600;margin-bottom:-2px;background:transparent}
.stTabs [data-baseweb="tab"]:hover{color:#ff6b9d;background:rgba(255,107,157,.06)}
.stTabs [aria-selected="true"]{color:#ff6b9d;background:#fff;border-color:#f0c4d8;border-bottom-color:#fff}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#fff5f8,#fff8fa);border-right:2px solid #fde8f0}
[data-testid="stSidebar"] .stRadio label{font-size:13px;color:#b86b8a;font-weight:600;padding:8px 12px;border-radius:8px;transition:all .15s}
[data-testid="stSidebar"] .stRadio label:hover{background:rgba(255,107,157,.08);color:#ff6b9d}
[data-testid="stSidebar"] .stRadio [data-checked="true"] label{background:rgba(255,107,157,.12);color:#ff6b9d}
div[data-testid="stForm"]{border:none;background:none;padding:0}
.block-container{padding-top:48px;padding-left:32px;padding-right:32px;max-width:960px}
.stDivider{margin:20px 0}
hr{border-color:#f0c4d8;margin:24px 0}
h1,h2,h3{color:#2d1b2e;font-weight:700}
h3{font-size:22px;letter-spacing:-.01em}
.stCaption{font-size:13px;color:#b86b8a}
header[data-testid="stHeader"]{background:linear-gradient(90deg,#fff5f8,#fff8fa);border-bottom:1px solid #fde8f0}
#MainMenu,footer{display:none}
@media(max-width:768px){.block-container{padding:16px;padding-top:40px}}
</style>""",unsafe_allow_html=True)

@st.cache_resource
def setup():init_database()
setup()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

def login():
    c1,c2,c3 = st.columns([0.3,0.4,0.3])
    with c2:
        st.markdown("### 学生信息管理系统")
        st.caption("请登录以继续")
        with st.form("login"):
            u = st.text_input("用户名",placeholder="kitty")
            p = st.text_input("密码",type="password",placeholder="abc123")
            if st.form_submit_button("登录",type="primary",use_container_width=True):
                user = verify_user(u,p)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("用户名或密码错误")

def home():
    s = get_statistics()
    st.markdown("### 学生信息管理系统")
    st.caption("学生信息管理 · 专业班级维护 · 多维度统计")
    st.divider()
    c1,c2,c3 = st.columns(3)
    c1.metric("学生总数",s["total_students"])
    c2.metric("专业数",s["total_majors"])
    c3.metric("班级数",s["total_classes"])
    st.divider()
    st.markdown("#### 各专业学生人数")
    if s["major_stats"]:
        df = pd.DataFrame(s["major_stats"])
        df.columns = ["专业","人数"]
        st.bar_chart(df.set_index("专业"),height=240,use_container_width=True)
    st.divider()
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("#### 各班级人数")
        if s["class_stats"]:
            df = pd.DataFrame(s["class_stats"])
            df.columns = ["班级","专业","人数"]
            st.dataframe(df,use_container_width=True,hide_index=True)
    with col2:
        st.markdown("#### 性别分布")
        if s["gender_stats"]:
            df = pd.DataFrame(s["gender_stats"])
            df.columns = ["性别","人数"]
            st.dataframe(df,use_container_width=True,hide_index=True)

def student_page():
    st.markdown("### 学生管理")
    t1,t2 = st.tabs(["学生列表","添加学生"])
    classes = get_classes()
    cls_map = {c["id"]:c["class_name"] for c in classes}
    years = [s["enrollment_year"] for s in query_students() if s.get("enrollment_year")]

    with t1:
        c1,c2,c3,c4 = st.columns(4)
        kw = c1.text_input("搜索",placeholder="学号或姓名...",label_visibility="collapsed")
        cf = c2.selectbox("班级",["全部"]+list(cls_map.values()),label_visibility="collapsed")
        cid = None
        if cf != "全部":
            cid = [k for k,v in cls_map.items() if v==cf][0]
        gf = c3.selectbox("性别",["全部","男","女"],label_visibility="collapsed")
        gv = gf if gf != "全部" else None
        yf = c4.selectbox("入学年份",["全部"]+sorted(set(years),reverse=True),label_visibility="collapsed")
        yv = yf if yf != "全部" else None

        students = query_students(kw=kw if kw else None,class_id=cid,gender=gv,enrollment_year=yv)
        if students:
            df = pd.DataFrame(students)[["id","student_id","name","gender","class_name","major_name","enrollment_year","phone"]]
            df.columns = ["ID","学号","姓名","性别","班级","专业","入学年份","手机"]
            st.dataframe(df,use_container_width=True,hide_index=True)
            st.caption(f"{len(students)} 条记录")
        else:
            st.caption("暂无学生记录")

        st.divider()
        if students:
            opts = {f"[{s['id']}]{s['name']}({s['student_id']})":s for s in students}
            sel = st.selectbox("选择编辑",list(opts.keys()),label_visibility="collapsed")
            s = opts[sel]
            with st.form("edit_student"):
                c1,c2,c3 = st.columns(3)
                nid = c1.text_input("学号",value=s["student_id"])
                nm = c2.text_input("姓名",value=s["name"])
                gd = c3.selectbox("性别",["男","女"],index=0 if s["gender"]=="男" else 1)
                bd = c1.text_input("出生日期",value=s.get("birth_date","") or "",placeholder="YYYY-MM-DD")
                idx = list(cls_map.keys()).index(s["class_id"]) if s["class_id"] in cls_map else 0
                ck = c2.selectbox("班级",list(cls_map.values()),index=idx)
                ey = c1.text_input("入学年份",value=s.get("enrollment_year","") or "",placeholder="2025")
                ph = c2.text_input("手机",value=s.get("phone","") or "")
                ad = c3.text_input("地址",value=s.get("address","") or "")
                cid2 = [k for k,v in cls_map.items() if v==ck][0]
                c1,c2 = st.columns(2)
                if c1.form_submit_button("保存",type="primary"):
                    ok,msg = update_student(s["id"],nid,nm,gd,bd,cid2,ey,ph,ad)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                if c2.form_submit_button("删除",type="secondary"):
                    ok,msg = delete_student(s["id"])
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

    with t2:
        with st.form("add_student"):
            c1,c2,c3 = st.columns(3)
            nid = c1.text_input("学号",placeholder="2024001")
            nm = c2.text_input("姓名",placeholder="张三")
            gd = c3.selectbox("性别",["男","女"])
            bd = c1.text_input("出生日期",placeholder="2005-03-15")
            ck = c2.selectbox("班级",list(cls_map.values()))
            ey = c3.text_input("入学年份",placeholder="2025")
            ph = c1.text_input("手机",placeholder="13800138000")
            ad = c2.text_input("地址",placeholder="南京市...")
            if st.form_submit_button("添加",type="primary",use_container_width=True):
                if not nid or not nm:
                    st.error("学号和姓名为必填")
                else:
                    cid3 = [k for k,v in cls_map.items() if v==ck][0]
                    ok,msg = add_student(nid,nm,gd,bd,cid3,ey,ph,ad)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

def org_page():
    st.markdown("### 专业与班级管理")
    t1,t2,t3 = st.tabs(["专业管理","班级管理","添加"])
    with t1:
        majors = get_majors()
        if majors:
            df = pd.DataFrame(majors)[["id","name","department"]]
            df.columns = ["ID","专业名称","所属院系"]
            st.dataframe(df,use_container_width=True,hide_index=True)
        with st.form("add_major"):
            c1,c2 = st.columns(2)
            nm = c1.text_input("专业名称",placeholder="软件工程")
            dp = c2.text_input("所属院系",placeholder="计算机学院")
            if st.form_submit_button("添加专业",type="primary"):
                ok,msg = add_major(nm,dp)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
    with t2:
        classes = get_classes()
        if classes:
            df = pd.DataFrame(classes)[["id","class_name","major_name","grade"]]
            df.columns = ["ID","班级名称","所属专业","年级"]
            st.dataframe(df,use_container_width=True,hide_index=True)
        majors_list = get_majors()
        m_map = {m["id"]:m["name"] for m in majors_list}
        if classes:
            opts = {c["class_name"]:c for c in classes}
            sel = st.selectbox("选择班级编辑",list(opts.keys()),label_visibility="collapsed")
            c = opts[sel]
            with st.form("edit_class"):
                c1,c2 = st.columns(2)
                cn = c1.text_input("班级名称",value=c["class_name"])
                mk = c2.selectbox("所属专业",list(m_map.values()))
                mid = [k for k,v in m_map.items() if v==mk][0]
                gr = c1.text_input("年级",value=c.get("grade","") or "")
                c1,c2 = st.columns(2)
                if c1.form_submit_button("保存",type="primary"):
                    ok,msg = update_class(c["id"],cn,mid,gr)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                if c2.form_submit_button("删除",type="secondary"):
                    ok,msg = delete_class(c["id"])
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
    with t3:
        with st.form("add_class"):
            c1,c2 = st.columns(2)
            cn = c1.text_input("班级名称",placeholder="计科25101班")
            mk = c2.selectbox("所属专业",list(m_map.values()))
            mid2 = [k for k,v in m_map.items() if v==mk][0]
            gr = c1.text_input("年级",placeholder="2025")
            if st.form_submit_button("添加班级",type="primary"):
                ok,msg = add_class(cn,mid2,gr)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

def stats_page():
    s = get_statistics()
    st.markdown("### 统计概览")
    c1,c2,c3 = st.columns(3)
    c1.metric("学生总数",s["total_students"])
    c2.metric("专业数",s["total_majors"])
    c3.metric("班级数",s["total_classes"])
    st.divider()
    st.markdown("#### 各专业学生人数")
    if s["major_stats"]:
        df = pd.DataFrame(s["major_stats"])
        df.columns = ["专业","人数"]
        st.bar_chart(df.set_index("专业"),height=260,use_container_width=True)
    st.divider()
    c1,c2 = st.columns(2)
    with c1:
        st.markdown("#### 各班级人数")
        if s["class_stats"]:
            df = pd.DataFrame(s["class_stats"])
            df.columns = ["班级","专业","人数"]
            st.dataframe(df,use_container_width=True,hide_index=True)
    with c2:
        st.markdown("#### 入学年份分布")
        if s["year_stats"]:
            df = pd.DataFrame(s["year_stats"])
            df.columns = ["年份","人数"]
            st.dataframe(df,use_container_width=True,hide_index=True)

def main():
    with st.sidebar:
        st.markdown("**学生管理**")
        st.caption(f"{st.session_state.user['username']}已登录")
        st.divider()
        m = st.radio("导航",["首页","学生管理","专业与班级","统计概览"],label_visibility="collapsed")
        st.divider()
        if st.button("退出登录",use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
    if m == "首页":
        home()
    elif m == "学生管理":
        student_page()
    elif m == "专业与班级":
        org_page()
    elif m == "统计概览":
        stats_page()

if __name__ == "__main__":
    if not st.session_state.logged_in:
        login()
    else:
        main()
