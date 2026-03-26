from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('signup/', views.signup, name='signup'),

    # 🔥 ESTA ES LA CLAVE
    path('recommend/', views.recommend_movie, name='recommend'),
]