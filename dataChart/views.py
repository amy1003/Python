import json

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