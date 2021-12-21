from django.conf.urls import url

from .views import index, landing_page, login, louisville_concierge, register, rules

urlpatterns = [
    url(r'^rules/', rules, name="rules"),
    url(r'^register/', register, name="register"),
    url(r'^louisville_concierge/', louisville_concierge, name="louisville_concierge"),
    url(r'^login/', login, name="login"),
    url(r'^landing_page/', landing_page, name="landing_page"),
    url(r'^', index, name="index"),
]
