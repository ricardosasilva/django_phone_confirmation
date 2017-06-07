from django.conf.urls import url

from phone_confirmation import views


urlpatterns = [
    url(r'^confirmation/$', views.ConfirmationView.as_view(), name='confirmation'),
    url(r'^activation-key/$', views.ActivationKeyView.as_view(), name='activation-key'),
    url(r'^activation-key/(?P<activation_key>[\w:.]+)/$', views.GetActivationKeyView.as_view(), name='view-activation-key')
]
