from rest_framework.routers import DefaultRouter

from battlefield import views

router = DefaultRouter()
router.register('', views.BattleViewSet, basename='battle')

urlpatterns = [

]

urlpatterns += router.urls
