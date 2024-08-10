from rest_framework.routers import DefaultRouter

from arena import views

router = DefaultRouter()
router.register('', views.ArenaViewSet, basename='arena')

urlpatterns = [

]

urlpatterns += router.urls
