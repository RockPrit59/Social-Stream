from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from feed import views as feed_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Core Feed
    path('', user_views.home, name='home'),
    path('search/', user_views.search_users, name='search_users'),
    path('api/posts/', feed_views.api_post_list, name='api_post_list'),
    
    # User Auth
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    
    # Profile & Social
    path('profile/', user_views.profile, name='profile'),
    path('profile/<str:username>/', user_views.public_profile, name='public_profile'),
    path('profile/<str:username>/follow/', user_views.follow_user, name='follow_user'), # <--- THIS WAS MISSING
    path('chat/<str:username>/', user_views.chat_room, name='chat_room'),
    path('profile/<str:username>/block/', user_views.block_user, name='block_user'),

    # Post Actions
    path('post/<int:pk>/like/', user_views.like_post, name='like_post'),
    path('post/<int:pk>/comment/', user_views.add_comment, name='add_comment'),
    path('post/<int:pk>/update/', user_views.update_post, name='update_post'),
    path('post/<int:pk>/delete/', user_views.delete_post, name='delete_post'),
]

# This part handles the images
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)