from django.urls import path
from .views import (
    homeView,
    loginView,
    registerView,
    logoutView,
    profileView,
    scanView,
    dashboardView,
)

urlpatterns = [
    path("", view=homeView, name="HomeView"),
    path("profile", view=profileView, name="ProfileView"),
    path("dashboard", view=dashboardView, name="DashboardView"),
    path("scan", view=scanView, name="ScanView"),
    path("login", view=loginView, name="LoginView"),
    path("register", view=registerView, name="RegisterView"),
    path("logout", view=logoutView, name="LogoutView"),
]
