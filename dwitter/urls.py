from django.urls import path

from .views import dashboard, profile_list, profile, like_dweet


app_name = "dwitter"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
    path("like/<int:dweet_id>/", like_dweet, name="like_dweet"),
]
