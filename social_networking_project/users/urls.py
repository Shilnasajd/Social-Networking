from django.urls import path
from .views import RegisterView, LoginView, PrintHelloWorldView, UserSearchAPIView
from .views import (
    RegisterView, 
    LoginView, 
    PrintHelloWorldView, 
    UserSearchAPIView,
    SendFriendRequestAPIView,
    AcceptRejectFriendRequestAPIView,
    ListFriendsAPIView,
    ListPendingFriendRequestsAPIView,
    UserListView
)
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('print_hello_world/', PrintHelloWorldView.as_view(), name='print_hello_world'),
    path('search/', UserSearchAPIView.as_view(), name='user-search'),
    path('friend-request/send/', SendFriendRequestAPIView.as_view(), name='send-friend-request'),
    path('friend-request/respond/', AcceptRejectFriendRequestAPIView.as_view(), name='respond-friend-request'),
    path('friends/', ListFriendsAPIView.as_view(), name='list-friends'),
    path('friend-requests/pending/', ListPendingFriendRequestsAPIView.as_view(), name='list-pending-friend-requests'),

    ]
