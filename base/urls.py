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
    path('send-message-ajax/<str:pk>/', views.send_message_ajax, name='send-message-ajax'),
    
    # Plant Guides URLs
    path('guides/', views.guidesHome, name='guides'),
    path('guide/<str:pk>/', views.guideDetail, name='guide'),
    path('create-guide/', views.createGuide, name='create-guide'),
    path('update-guide/<str:pk>/', views.updateGuide, name='update-guide'),
    path('delete-guide/<str:pk>/', views.deleteGuide, name='delete-guide'),
    
    # Cultivation Techniques URLs
    path('techniques/', views.techniquesHome, name='techniques'),
    path('technique/<str:pk>/', views.techniqueDetail, name='technique'),
    path('create-technique/', views.createTechnique, name='create-technique'),
    path('update-technique/<str:pk>/', views.updateTechnique, name='update-technique'),
    path('delete-technique/<str:pk>/', views.deleteTechnique, name='delete-technique'),
    path('like-technique/<str:pk>/', views.likeTechnique, name='like-technique'),
    
    # Main Techniques Information URLs
    path('techniques/vertical/', views.verticalTechniqueInfo, name='vertical-technique'),
    path('techniques/wall-mounted/', views.wallMountedTechniqueInfo, name='wall-mounted-technique'),
    path('techniques/hydroponics/', views.hydroponicsTechniqueInfo, name='hydroponics-technique'),
    path('techniques/recycled-materials/', views.recycledMaterialsTechniqueInfo, name='recycled-materials-technique'),
    path('techniques/aquaponics/', views.aquaponicsTechniqueInfo, name='aquaponics-technique'),
    
    # Friendship URLs
    path('send-friend-request/<str:pk>/', views.send_friend_request, name='send-friend-request'),
    path('accept-friend-request/<str:pk>/', views.accept_friend_request, name='accept-friend-request'),
    path('reject-friend-request/<str:pk>/', views.reject_friend_request, name='reject-friend-request'),
    path('remove-friend/<str:pk>/', views.remove_friend, name='remove-friend'),

    # 3D Cultivation Models URLs
    path('3d-models/', views.cultivation3d_home, name='cultivation3d_home'),
    path('3d-models/create/', views.create_3d_model, name='create_3d_model'),
    path('3d-models/<str:pk>/', views.cultivation3d_detail, name='cultivation3d_detail'),
    path('3d-models/<str:pk>/status/', views.check_model_status, name='check_model_status'),
    path('3d-models/<str:pk>/delete/', views.delete_3d_model, name='delete_3d_model'),
]