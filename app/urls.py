from django.urls import path
from .views import (
    homeView,
    loginView,
    registerView,
    logoutView,
    profileView,
    scanView,
    dashboardView,
    codeDetailView,
    adminScanView
)

urlpatterns = [
    path("", view=homeView, name="HomeView"),
    path("profile", view=profileView, name="ProfileView"),
    path("dashboard", view=dashboardView, name="DashboardView"),
    path("scan", view=scanView, name="ScanView"),
    path("my/scan", view=adminScanView, name="AdminScanView"),
    path("code/<str:uuid>", view=codeDetailView, name="CodeDetailView"),

    path("login", view=loginView, name="LoginView"),
    path("register", view=registerView, name="RegisterView"),
    path("logout", view=logoutView, name="LogoutView"),
]
