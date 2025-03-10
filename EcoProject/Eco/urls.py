from django.urls import path
from Eco import views

app_name = 'Eco'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('Challenges/', views.challenges, name='Challenges'),
    path('EducationalLinks/', views.educational_links, name='Educational Links'),
    path('LeaderBoard/', views.leaderboard, name='LeaderBoard'),
    path('AccountPage/', views.account_page, name='AccountPage'),
    path('update_email/', views.update_email, name='update_email'),
    path('update_picture/', views.update_picture, name='update_picture'),
    path('log_challenge/<int:challenge_id>/', views.log_challenge, name='log_challenge'),
]

