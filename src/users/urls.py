from django.urls import path
from .views import login_view,  logout_view, register_view, user_verification

urlpatterns = [
    path('login/', login_view, name="login"),
    path('registration/', register_view, name="registration"),
    path('verification/', user_verification, name="user_verification"),
    path('logout/', logout_view, name="logout")
]
