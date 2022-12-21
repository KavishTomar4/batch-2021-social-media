from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginhandle, name = 'login'),
    path('signup', views.signuphandle, name = 'signup'),
    path('home/<str:section>', views.homepage, name= 'home'),
    path('logout', views.logouthandle, name= 'logout'),
    path('profile', views.profilepage, name= 'profile'),
    path('profile/<str:user_name>', views.other_profile, name= 'profile_one'),
    path('upload', views.uploadpage , name = 'upload'),
    path('comments', views.commentpage , name = 'comments'),
    path('makecomments', views.makecomments, name= 'makecomments'),
    path('makereply',  views.makereply, name = 'makereply'),
    path('makesuggestions' , views.suggestions, name='makesuggestions'),
    path('notification', views.notificationhandler, name ='notification'),
    path('update', views.editprofilepage, name = 'update'),
    path('deletephoto', views.deletephoto, name = 'deletephoto'),
    path('deletecomment', views.deletecomment, name= 'deletecomment'),
    path('credits', views.credits, name= 'credits')
    

]
