from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from .views import MissionViewSet, TargetViewSet

# router = SimpleRouter()
router = DefaultRouter()
router.register(r'missions', MissionViewSet, basename='mission')
router.register(r'targets', TargetViewSet, basename='target')

urlpatterns = router.urls

# urlpatterns = [
#     path('', MissionViewSet.as_view({'get': 'list', 'post': 'create'}), name='missions-list-create'),
#     path('targets/', include(router.urls)),  # Інтеграція Targets у той же шлях
# ]
