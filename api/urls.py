from django.conf.urls import url, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'^trucks', views.TruckViewSet)
router.register(r'^trucks/(?P<truck_uuid>[\w-]+)/menu', views.MenuViewSet)
router.register(r'^trucks/(?P<truck_uuid>[\w-]+)/schedule', views.PostViewSet)

# Owner Views
router.register(r'^me/trucks', views.MyTrucksViewSet)
router.register(r'^me/trucks/(?P<truck_uuid>[\w-]+)/schedule', views.MyPostViewSet)
router.register(r'^me/trucks/(?P<truck_uuid>[\w-]+)/menu', views.MyMenuViewSet)


urlpatterns = [
    url(r'^$', views.root_view),
    url(r'^', include(router.urls)),
    url(r'^me/trucks/likes$', views.MyTruckLikes.as_view()),
    url(r'^trucks/(?P<truck_uuid>[\w-]+)/like/$', views.like_truck),
    url(r'^trucks/(?P<truck_uuid>[\w-]+)/ratings/$', views.CreateRatingView.as_view()),
    url(r'^trucks/(?P<truck_uuid>[\w-]+)/ratings/(?P<id>[\d]+)/$', views.RatingDetailView.as_view())
]