import json

import psycopg2
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.

def conn():
    c = psycopg2.connect(database="test", user="postgres", password="123456", host="127.0.0.1", port="5432")
    return c

# 初始化进入保存教师信息页面
def initSaveTeacher(request):
    return render(request,'teacher/register.html',)

# 保存教师信息
def saveTeacher(request):
    name=request.POST.get('name')
    password=request.POST.get('password')
    c=conn()
    cursor=c.cursor()
    cursor.execute('insert into stu_teacher(name,password) VALUES(%s,%s)',(name,password))
    c.commit()
    c.close()
    return render(request,'teacher/login.html',)

# 初始化进入教师登录页面
def initLoginTeacher(request):
    return render(request,'teacher/login.html',)

# 登录
def loginTeacher(request):
    c=conn()
    cursor=c.cursor()
    name=request.POST.get('name')
    password=request.POST.get('password')
    cursor.execute('SELECT id FROM stu_teacher where name=%s AND password=%s',(name,password))
    teacher=cursor.fetchone()
    c.close()
    # 判断是否登录成功
    if teacher[0] is not None:
        request.session['name']=name
        return HttpResponseRedirect('/teacher/index')
    else:
        message={'msg':'用户名或密码错误!!!'}
        return render(request,'teacher/login.html',message)

# 主页
def index(request):
    name=request.session.get('name')
    return render(request,'teacher/index.html',{'name':name})

def left(request):
    return render(request,'teacher/left.html')

def top(request):
    return render(request,'teacher/top.html')

def foot(request):
    return render(request,'teacher/foot.html')

# 用户注销
def logout(request):
    try:
        del request.session['name']
    except KeyError:
        pass
    return HttpResponseRedirect('/index')

def category(request):
    c = conn()
    cursor = c.cursor()
    sql='select CASE WHEN category=(select id from stu_category where cname=\'ACCP 8.0\') ' \
        'THEN classname ELSE \'-\' END AS ACCP,CASE WHEN category=(select id from stu_category where cname=\'学士后 Java\') ' \
        'THEN classname ELSE \'-\'END AS Java,CASE WHEN category=(select id from stu_category where cname=\'学士后 UI\') ' \
        'THEN classname ELSE \'-\'END AS UI from stu_class'
    cursor.execute(sql)
    lists=cursor.fetchall()
    c.close()
    json1={'list':lists}
    return render(request,'teacher/category.html',json1)

# 种类图表显示
def cChart(request):
    c = conn()
    cursor = c.cursor()
    sql='select c1.cname,count(1) from stu_category c1 ' \
        'inner join stu_class c2 on c1.id=c2.category ' \
        'group by c1.cname'
    cursor.execute(sql)
    lists=cursor.fetchall()
    c.close()
    json1={'list':json.dumps(lists)}
    return render(request,'teacher/categoryChart.html',json1)

# 进入保存学员信息页面
def initSaveStudent(request):
    c = conn()
    cursor = c.cursor()
    sql='select id,classname from stu_class'
    cursor.execute(sql)
    list=cursor.fetchall()
    c.close()
    return render(request,'student/register.html',{"list":list})

# 保存学员信息
def saveStudent(request):
    name=request.POST.get('name')
    password=request.POST.get('password')
    academic=request.POST.get('academic')
    class1=request.POST.get('class')
    c = conn()
    cursor = c.cursor()
    sql='insert into stu_student(name,class,academic,password) VALUES(%s,%s,%s,%s)'
    cursor.execute(sql,(name,class1,academic,password))
    c.commit()
    c.close()
    return HttpResponse("<h3 style='color:blue'>学员保存成功!!!</h3>")

# 查询学员总记录数
def count():
    c = conn()
    cursor = c.cursor()
    sql = 'select count(1) from stu_student'
    cursor.execute(sql)
    rs = cursor.fetchone()
    c.close()
    return rs

# 学员信息分页统计
def student(request,page):
    # 获取总记录数
    rs=count()[0]
    page_size=8
    last_page = int(rs / page_size) if int(rs % page_size) == 0 else int(rs / page_size) + 1
    if int(page)<1:
        page=1
    if int(page)>last_page:
        page=last_page
    start = (int(page)-1)*page_size
    c=conn()
    cursor = c.cursor()
    sql2='select s.name,s.academic,c.classname from stu_student s ' \
         'left join stu_class c on s.class=c.id ORDER BY s.id limit %s offset %s'
    cursor.execute(sql2,(page_size,start))
    list=cursor.fetchall()
    ds={'list':list,'last':last_page,'page':page}
    c.close()
    return render(request,'student/show.html',{'ds':ds})

# 分组统计
def class_chart(request):
    c = conn()
    cursor = c.cursor()
    sql='select c.classname,count(1) from stu_class c inner join stu_student s on c.id=s.class  group by c.classname '
    cursor.execute(sql)
    list=cursor.fetchall()
    c.close()
    return render(request,'student/classChart.html',{'list':json.dumps(list)})

# 学历统计
def academic_chart(request):
    c = conn()
    cursor = c.cursor()
    sql='select sum(stu.one) as cz,sum(stu.two) as gz,sum(stu.three) as dz,sum(stu.four) as bk from ' \
        '(select  CASE WHEN academic=\'初中\' THEN count(1) ELSE 0 END AS one,' \
        'CASE WHEN academic=\'高中\' THEN count(1) ELSE 0 END AS two,' \
        'CASE WHEN academic=\'大专\' THEN count(1) ELSE 0 END AS three,' \
        'CASE WHEN academic=\'本科\' THEN count(1) ELSE 0 END AS four FROM stu_student group by academic) as stu'
    cursor.execute(sql)
    rs=cursor.fetchone()
    # 元组拆包
    a,b,c1,d = rs
    # 将Decimal转化为int,使用tuple记录
    rs=(int(a),int(b),int(c1),int(d))
    c.close()
    return render(request,'student/academicChart.html',{'rs':json.dumps(rs)})
