from django.urls import path
from .views import *

urlpatterns = [
    path('expenses/', TrackExpense.as_view()),
    path('signup/', SignUpView.as_view(), name = 'signup'),
    path('signin/', SignInView.as_view(), name = 'signin'),
    path('signout/', SignOutView.as_view(), name = 'signout'),
]
