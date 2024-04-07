from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import MyLogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<str:title>", views.post, name="post"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("category/<str:name>", views.category, name="category"),
    path("tag/<str:name>", views.tag, name="tag"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("subscribe", views.subscribe, name="subscribe"),
    path("add_comment/<str:title>", views.add_comment, name="add_comment"),
    path("login", LoginView.as_view(), name="blog_login"),
    path("logout", MyLogoutView.as_view(), name="blog_logout"),
    path("user_profile/account<int:id>/", views.user_profile, name="user_profile"),
    path("user_profile/account<int:id>/update_profile/", views.update_profile, name="update_profile"),
    path("reg_user", views.reg_user, name="reg_user"),
    path("user_profile/account<int:id>/set_ava", views.set_ava, name="set_ava"),
    path("editing_post<int:id>",views.editing_post,name="editing_post"),
]
