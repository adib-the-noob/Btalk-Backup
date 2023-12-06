from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from fake_data_generators.fake_user import generateFakeUser
from fake_data_generators.fake_posts import generateFakePosts

urlpatterns = [
    # apps
    path('admin/', admin.site.urls),
    path('user/', include("authcore.urls")),
    path('friends/', include("friends.urls")),
    path('chat/', include("chat.urls")),
    path('posts/', include("posts.urls")),
    path('profiles/', include("profiles.urls")),
    path('notifications/', include("notifications.urls")),

    # faker
    path('fake-user/<int:users>/', generateFakeUser),
    path('fake-posts/<int:user>/<int:total_post>/', generateFakePosts),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 