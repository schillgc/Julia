from django.urls import re_path

from .views import index, landing_page, login, louisville_concierge, register, rules

urlpatterns = [
    re_path(r'^rules/', rules, name="rules"),
    re_path(r'^register/', register, name="register"),
    re_path(r'^louisville_concierge/', louisville_concierge, name="louisville_concierge"),
    re_path(r'^login/', login, name="login"),
    re_path(r'^landing_page/', landing_page, name="landing_page"),
    re_path(r'^', index, name="index"),
]
