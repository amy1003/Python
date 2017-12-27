"""chart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from Student import views_stu
from dataChart import views

urlpatterns = [
    # 后台管理
    url(r'^admin/', admin.site.urls),
    # 数据统计
    url(r'level/', views .chartLevel),
    url(r'gender/', views.chartGender),
    url(r'addUser/', views.initAddUser),
    url(r'saveUser$', views.saveUser),
    # Teacher模块
    url(r'initSaveTeacher', views_stu.initSaveTeacher),
    url(r'saveTeacher', views_stu.saveTeacher),
    url(r'initLoginTeacher', views_stu.initLoginTeacher),
    url(r'loginTeacher', views_stu.loginTeacher),
    url(r'logout', views_stu.logout),
    url(r'index', views_stu.index),
    url(r'left', views_stu.left),
    url(r'top', views_stu.top),
    url(r'foot', views_stu.foot),
    # 数据图表
    url(r'class/category', views_stu.category),
    url(r'class/cChart', views_stu.cChart),
    # 学员统计
    url(r'student/save', views_stu.initSaveStudent),
    url(r'save_student', views_stu.saveStudent),
    url(r'query_student/(\d+)/$', views_stu.student),
    url(r'student/class_chart', views_stu.class_chart),
    url(r'student/academic_chart', views_stu.academic_chart),


]
