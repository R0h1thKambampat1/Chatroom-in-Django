from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("profile/<str:id>/", views.userProfile, name="user-profile"),
    path("", views.home, name="home"),
    path("room/<str:id>/",views.room, name="room"),
    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/", views.updateRoom, name="update-room"),
    path("update-room/<str:id>/", views.updateRoom, name="update-room"),
    path("delete-room/<str:id>/", views.deleteRoom, name="delete-room"),
    path("delete-message/<str:id>/", views.deleteMessage, name="delete-message"),
    path("update-user/", views.updateUser, name="update-user"),
    path("topics/", views.topicsPage, name="topics"),
    path("activity/",views.activityPage, name="activity")

]
