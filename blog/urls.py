from django.urls import path

from . import views

# Only expose blog-related views here. Registration/login/logout live in users.urls.
urlpatterns = [
    path('', views.home, name='home'),
    path('all-blogs/', views.all_blogs, name='all_blogs'),
    path('post/<int:post_id>/', views.show_post, name='show_post'),
    path('add-post/', views.add_post, name='add_post'),
    path('edit-post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('about/', views.about_page, name='about_page'),
    path('contact/', views.contact_page, name='contact_page'),
]
