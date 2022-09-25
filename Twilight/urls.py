"""Twilight URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from game.views import mainpage, registerpage, loginpage, logoutpage, newgame, joingame, newplayer, draft, poolvoting, finalpick


urlpatterns = [
    path('', mainpage, name='mainpageurl'),
    path('register/', registerpage, name='registerurl'),
    path('login/', loginpage, name='loginurl'),
    path('logout/', logoutpage, name='logouturl'),
    path('admin/', admin.site.urls),
    path('newgame/', newgame, name='newgameurl'),
    path('joingame/', joingame, name='joingameurl'),
    path('newplayer/<str:gamepk>/', newplayer, name='newplayerurl'),
    path('draft/<int:gamepk>/', draft, name='drafturl'),
    path('poolvoting/<str:gamepk>/', poolvoting, name='poolvotingurl'),
    path('finalpick/<str:gamepk>/', finalpick, name='finalpickurl'),
    # path('searchgame/', searchgame, name='searchgameurl'),

]


