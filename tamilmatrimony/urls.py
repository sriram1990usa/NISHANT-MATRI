from django.urls import path, re_path as url
from django.contrib.auth.views import LoginView, LogoutView

from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name='tamilmatrimony'

urlpatterns = [

    url(r'^$', profile_list, name='list'),

    url(r'^search/$', profile_search_list, name='search1'),
    url(r'^search_by_id/$', profile_search_id, name='search2'),

    url(r'^create/$', profile_create, name='create'),
    url(r'^myprofile/$', my_profile, name='myprofile'),
    url(r'^all_profiles/$', profile_list_all, name='allprofiles'),

    url(r'^myprofile/edit/$', myprofile_update, name='myedit'),
    
    url(r'^register/', register, name="register"),    
    url(r'^logout/', logout_view, name="logout"),
    path('login/', LoginView.as_view(), name='login'),  
  
    path('profiles/details/<slug:slug>/', profile_detail, name='detail'), 
    path('profiles/<slug:slug>/edit/', profile_update, name='edit'),    

    path('profiles/<slug:slug>/delete/', profile_delete, name='delete'), 
]