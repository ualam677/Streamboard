from django.contrib import admin
from django.urls import path

from scoreboard.views import player_list, test_view

urlpatterns = [
    path('api/test/', test_view, name='test')
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/players/', player_list, name='player-list'),
]