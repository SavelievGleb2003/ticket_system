from django.urls import path
from . import views

# create urls

urlpatterns = [
        path('', views.ListTD.as_view(), name='TD_list'),
        path('register/', views.register, name='register'),
        path('<int:year>/<int:month>/<int:day>/<slug:TD>/', views.TD_detail, name='TD_detail'),
        path('<int:id_d>/share/',views.send_email, name='send_email'),
        path('<int:id_d>/comment/',views.add_comment, name='add_comment')

]