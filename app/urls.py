    # app/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('new_post/', views.new_post, name='new_post'),
    path('search/', views.search, name='search'),
    path('download_file/<int:post_id>/', views.download_file, name='download_file'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'), 
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
