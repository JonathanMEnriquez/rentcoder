from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.landing_page),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard/(?P<user_id>\d+)$', views.dashboard),
    url(r'^order$', views.order),
    url(r'^checkout$', views.checkout),
    url(r'^home/admin$', views.admin_home),
    url(r'^home/admin/users$', views.admin_users),
    url(r'^home/admin/coders$', views.admin_coders),
    url(r'^home/admin/orders$', views.admin_orders),
    url(r'^edit/user/(?P<user_id>\d+)$', views.edit_user),
    url(r'^edit/users/(?P<user_id>\d+)$', views.edit_user_process),
    url(r'^edit/coder/(?P<coder_id>\d+)$', views.edit_coder),
    url(r'^edit/coders/(?P<coder_id>\d+)$', views.edit_coder_process),
    url(r'^edit/order/(?P<order_id>\d+)$', views.edit_order),
    url(r'^edit/orders/(?P<order_id>\d+)$', views.edit_order_process),
    url(r'^coder_profile/(?P<coder_id>\d+)$', views.coder_profile),
    url(r'^process/(?P<action>\w+)$', views.process),
]