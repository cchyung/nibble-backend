from django.conf.urls import url, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'^trucks', views.TruckViewSet)
router.register(r'^trucks(?P<truck_uuid>[\w-]+)/schedule', views.PostViewSet)
router.register(r'^me/trucks', views.MyTrucksViewSet)
router.register(r'^me/trucks/(?P<truck_uuid>[\w-]+)/schedule', views.PostViewSet)


urlpatterns = [
    url(r'^$', views.root_view),
    url(r'^', include(router.urls)),
]