"""drf_beginners URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path, include
# from posts_1.views import ( PostListView,PostDetailView,PostDestroyView,PostCreateView,PostUpdateView
# ,PostListCreateAPIView,OwnerDetailView,CommentDetailView)
# from posts.views import PostMixinListView
# from posts.views importpost_list,post_detail
# from posts.views import PostAPIView


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api-auth/', include('rest_framework.urls')),
    
#     # path('api/',include('posts.urls')),


#     # path('api/apiposts/', PostAPIView.as_view(),name='apipost-list'),



#     path('api/posts/', PostListView.as_view(),name='post-list'),
#     path('api/posts/create/', PostCreateView.as_view(),name='post-create'),
    
#     path('api/posts/listcreate/', PostListCreateAPIView.as_view(),name='post-listcreate'),
    
#     path('api/posts/update/<pk>/', PostUpdateView.as_view(),name='post-update'),
#     path('api/posts/detail/<pk>/', PostDetailView.as_view(),name='post-detail'),
#     path('api/posts/delete/<pk>/', PostDestroyView.as_view(),name='post-destroy'),

#     path('api/owner/<pk>', OwnerDetailView.as_view(),name='owner-detail'),
#     path('api/comment/<pk>', CommentDetailView.as_view(),name='comment-detail'),


#     # path('api/posts/', PostView.as_view(),name='post-list'),
#     # path('api/posts/<pk>/', PostView.as_view(),name='post-detail'),


#     # path('api/post-list/', post_list,name='post-list'),
#     # path('api/posts/<int:pk>/', post_detail,name='post-detail')
# ]
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from posts.views import home, post_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/posts/', include('posts.urls')),
    path('', home, name='home'),
    path('posts/<pk>/', post_detail, name='post-detail')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    