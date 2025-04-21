from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    path('register/', views.registerPage, name = "register"),

    path('', views.home, name = "home"),
    path('room/<str:pk>', views.room, name = "room"),
    path('profile/<str:pk>/', views.userProfile, name ="user-profile"),

    path('create-room/', views.createRoom, name ="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name ="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name ="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name ="delete-message"),
    
    path('update-user/', views.updateUser, name ="update-user"),

    path('topics/', views.topicsPage, name ="topics"),
    path('activity/', views.activityPage, name ="activity"),
    path('like-room/<str:pk>/', views.likeRoom, name='like-room'),
    path('like-message/<str:pk>/', views.likeMessage, name='like-message'),
    
    # Plant Guides URLs
    path('guides/', views.guidesHome, name='guides'),
    path('guide/<str:pk>/', views.guideDetail, name='guide'),
    path('create-guide/', views.createGuide, name='create-guide'),
    path('update-guide/<str:pk>/', views.updateGuide, name='update-guide'),
    path('delete-guide/<str:pk>/', views.deleteGuide, name='delete-guide'),
    
    # Cultivation Techniques URLs
    path('techniques/', views.techniquesHome, name='techniques'),
    path('technique/<str:pk>/', views.techniqueDetail, name='technique'),
]