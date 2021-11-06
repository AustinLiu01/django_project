from django.urls import path
from . import views

# 正在部署的应用的名称
app_name = 'display'

urlpatterns = [
    path('display-list/', views.display_list, name='display_list'),
]
