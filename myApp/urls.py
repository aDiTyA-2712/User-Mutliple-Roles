from django.urls import path
from .views import UserListView,UserUpdateView,LoginView,UserDetailsView,add_user

urlpatterns=[
    
    path('users/',UserListView.as_view(),name='user-list'),
    path('update/<str:username>',UserUpdateView.as_view(),name='user-update'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('details/', UserDetailsView.as_view(), name='user-details'),
    path('add-user/', add_user, name='add_user'),

]