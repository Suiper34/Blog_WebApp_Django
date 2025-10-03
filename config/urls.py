from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # keep users auth routes at top level
    path('', include('users.urls')),

    # redirect legacy auth profile URL to home
    path('accounts/profile/',
         RedirectView.as_view(pattern_name='home', permanent=False)),

    # blog routes (home and posts)
    path('', include('blog.urls')),

    # keep default auth views available
    path('accounts/', include('django.contrib.auth.urls')),
]
