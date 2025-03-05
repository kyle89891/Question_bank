"""
URL configuration for question_bank_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from question_bank import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('question/create/', views.create_question, name='create_question'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('question/<int:pk>/delete/', views.delete_question, name='delete_question'),
    path('',views.add_show,name='addshow'),
    path('delete/<int:id>/',views.delete_data,name="deleted"),
    path('<int:id>/',views.update_data,name="updated"), 
    path('login/',views.login_view, name='login'),
    path('questions/', views.submit_answers, name='submit_answers'),
    path('result/',views.submit_answers,name='result'),
    path('questions_computer/',views.submit_answers2,name='computer'),
    path('questions_maths/',views.submit_answers3,name='maths'),
    path('logout/',views.logout_page,name='logout'),
    ####################################################
    path('api/subjects',views.getSub),
    path('api/onesubject',views.getoneSub),
    path('api/addsubject',views.addSub),
    path('api/delsubject',views.removesub),
]

