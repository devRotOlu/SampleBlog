from . import views
from django.urls import path

urlpatterns = [
    path("homepage/",views.homepage,name="posts_home"),
    # path("",views.list_posts,name="list_posts"),
    path("",views.PostListCreateView.as_view(),name="list_posts"),
    # path("<int:post_id>/",views.get_post,name="get_post"),
    # path("update/<int:post_id>/",views.update_post,name="update_post"),
    # path("delete/<int:post_id>/",views.delete_post,name="delete_post")
    path("<int:pk>/",views.PostRetrieveUpdateAndDeleteView.as_view(),name="get_post"),
    path("user_posts/",view=views.get_user_posts,name="user_posts/"),
    # path("author_posts/",view=views.AuthorPosts.as_view(),name="author_posts")
    path("author_posts/<username>",view=views.AuthorPosts.as_view(),name="author_posts")
]