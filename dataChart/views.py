import json
import random

import psycopg2
from django.shortcuts import render

# Create your views here.
from dataChart.models import Poptbl


def conn():
    c = psycopg2.connect(database="test", user="postgres", password="123456", host="127.0.0.1", port="5432")
    return c

def chartLevel(request):
    c = conn()
    cursor=c.cursor()

    cursor.execute('SELECT CASE pref_name  '
                       'WHEN \'德岛\' THEN \'四国\' WHEN \'香川\' '
                       'THEN \'四国\' WHEN \'爱媛\' THEN \'四国\''
                       'WHEN \'高知\' THEN \'四国\''
                       'WHEN \'福冈\' THEN \'九州\''
                       'WHEN \'佐贺\' THEN \'九州\''
                       'WHEN \'长崎\' THEN \'九州\''
                       'ELSE \'其它\' END AS area,'
                       'COUNT(population) AS count FROM poptbl GROUP BY area')
    # 游标取出输出
    pops = cursor.fetchall()

    # 序列化json
    json1={'list':json.dumps(pops)}
    # 关闭连接
    c.close()

    return render(request,'level.html',json1)


def chartGender(request):
    c=conn()
    cursor=c.cursor()

    cursor.execute('SELECT pref_name AS area, '
                   'SUM(CASE sex WHEN \'1\' '
                   'THEN population ELSE 0 END)'
                   '  AS man,SUM(CASE sex'
                   ' WHEN \'2\' THEN population ELSE 0 END ) AS woman '
                   'FROM poptbl2 GROUP BY pref_name')

    # 获取数据结果集
    pops=cursor.fetchall()

    # 序列化为json
    jsonStr={'list':json.dumps(pops)}

    c.close()

    return render(request,'gender.html',jsonStr)


# 进入保存用户信息页面
def initAddUser(request):

    return render(request,'addUser.html',)


# 保存表单数据
def saveUser(request):
    username=request.POST['username']
    gender=request.POST.get('gender')
    iq=random.randint(0,100)
    eq=random.randint(0,100)
    strength=random.randint(0,100)
    speed=random.randint(0,100)
    tenacious=random.randint(0,100)
    c=conn()
    cursor=c.cursor()
    cursor.execute('insert into t_user(name,sex,iq,eq,strength,speed,tenacious) VALUES (%s,%s,%s,%s,%s,%s,%s)',
                   (username,bool(gender),iq,eq,strength,speed,tenacious))

    cursor.execute('select name,iq,eq,strength,speed,tenacious from t_user WHERE name=%s',(username,))

    user=cursor.fetchone()
    print(user)

    c.commit()
    c.close()

    jsonStr=json.dumps(user)
    users={'u':jsonStr}
    return render(request,'show.html',users)

