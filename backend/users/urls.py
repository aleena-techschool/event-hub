from django.urls import path
from .views import home,login_view, signup_view, dashboard, admin_dashboard,logout_view,admin_edit_event,admin_delete_event

urlpatterns = [
    path("", home, name="home"),
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("dashboard/", dashboard, name="dashboard"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("logout/", logout_view, name="logout"),
    path("admin-edit-event/<int:id>/", admin_edit_event),
    path("admin-delete-event/<int:id>/", admin_delete_event),
]
