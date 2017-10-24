from django.conf.urls import url, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'^trucks', views.TruckViewSet)
router.register(r'^trucks(?P<truck_uuid>[\w-]+)/schedule', views.PostViewSet)


urlpatterns = [
    url(r'^$', views.root_view),
    url(r'^', include(router.urls)),
    url(r'^users/signup/$', views.UserSignUp.as_view(), name='user-register'),
]