from django.conf.urls import url
from CountryCapital import views

app_name = 'CountryCapital'


urlpatterns = [
    url(r'^register/$',views.register, name='register'),
    url(r'^user_login/$',views.user_login, name='user_login'),
    url(r'^spellgame/$', views.spell_check, name='spellgame'),
    url(r'^spellgamenext/$', views.spellgame_next, name='spellgamenext')
]
