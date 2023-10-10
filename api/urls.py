from django.urls import path
from api.views import ProfileView, LoginView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name="user_profile"),
    path('login/', LoginView.as_view(), name="user_login"),

]