from django.urls import path
from . import views, feed_view
from posts import reaction_views
from posts.comment import comments_views

urlpatterns = [
    path('delete-post/<int:pk>/', views.delete_post, name='delete-post'),
    path('create-post/', views.PostCreateView.as_view()),
    path('update-post/<int:pk>/', views.update_post, name='update-post'),
    path('users-timeline-post/<int:user_id>/', views.get_timeline_posts),

    # reaction
    path('react-post/<int:post_id>/', reaction_views.react_post),

    # comment
    path('get-comments/<int:post_id>/', comments_views.CommentView.as_view()),
    path('create-comment/', comments_views.CommentView.as_view()),
    path('update-comment/<int:comment_id>/', comments_views.CommentView.as_view()),
    path('delete-comment/<int:comment_id>/', comments_views.CommentView.as_view()),

    # feed
    path('feed/', feed_view.FeedView.as_view()),
]