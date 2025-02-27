from django.urls import path
from Eco import views

app_name = 'Eco'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'), # New mapping!
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('Challenges/', views.challenges, name='Challenges'),
    path('EducationalLinks/', views.educational_links, name='Educational Links'),
    path('LeaderBoard/', views.leaderboard, name='LeaderBoard'),

]

