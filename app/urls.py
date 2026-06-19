from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("board/", views.board, name="board"),
    path("my-profile/", views.my_profile, name="my_profile"),
    path("user/<int:user_id>/", views.user_profile, name="user_profile"),
    path("users/", views.users_list, name="users_list"),
    path("search/", views.search, name="search"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("post/delete/<int:post_id>/", views.delete_post, name="delete_post"),
]