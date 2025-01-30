from django.urls import path
from . import views

# create urls

urlpatterns = [
        path('', views.TD_list, name='TD_list'),
        path('<int:year>/<int:month>/<int:day>/<slug:TD>/', views.TD_detail, name='TD_detail'),

]