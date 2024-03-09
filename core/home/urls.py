from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    )

urlpatterns = [
    path('expenses/', TrackExpense.as_view()),
    path('signup/', SignUpView.as_view(), name = 'signup'),
    path('signin/', SignInView.as_view(), name = 'signin'),
    path('signout/', SignOutView.as_view(), name = 'signout'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh')
]
