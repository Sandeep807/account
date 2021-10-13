from django.urls import path
from .views import *
urlpatterns = [
    path('',RegisterView.as_view()),
    path('verify/',VerifyOtp.as_view()),
    path('get/',GetAllData.as_view()),
]
