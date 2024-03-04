from django.urls import path
from .views import *

urlpatterns = [
    path('', TrackExpense.as_view())
]
