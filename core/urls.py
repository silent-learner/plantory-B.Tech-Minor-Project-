from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name='index'),
    path("login/",views.LogIn,name='login'),
    path("signup/",views.signup,name='signup'),
    path("plantdisease/",views.plantdisease,name='plantdisease'),
    path("plantinfo/",views.plantinfo,name='plantinfo'),
    path("community/",views.community,name='community'),
    path("commentPage/<str:postId>/",views.commentPage,name='commentPage'),
    path('logout/', views.logoutUser, name="logout"),
]
