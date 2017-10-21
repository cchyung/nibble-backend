from django.conf.urls import url, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'trucks', views.TruckViewSet)
router.register(r'posts', views.PostViewSet)


urlpatterns = [
    url(r'^$', views.root_view),
    url(r'^', include(router.urls)),
    url(r'^users/signup$', views.UserSignUp.as_view(), name='user-register'),
    url(r'^trucks/(?P<truck_uuid>[\w-]+)/posts/$', views.TruckPosts.as_view(), name='truck-posts'),
    url(r'^trucks/(?P<truck_uuid>[\w-]+)/posts/(?P<uuid>[\w-]+)/$', views.TruckPostDetail.as_view(), name='truck-post-detail'),
]