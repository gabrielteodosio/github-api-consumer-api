from django.contrib import admin
from django.urls import path, include

from core.views import home_view, authorize, get_repos, get_commits, get_commit

urlpatterns = [
    path('', home_view, name='home'),

    path('authorize/', authorize, name='authorize'),
    path('commits/', get_commits, name='commits'),
    path('commit/', get_commit, name='commit'),
    path('repos/', get_repos, name='repos'),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
