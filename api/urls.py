from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


schema_view = get_schema_view(
   openapi.Info(
      title="Edytor Tras API",
      default_version='v1',
      description="API do zarządzania trasami i punktami",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('route/', views.PointListCreateView.as_view(), name='point-list-create'),
    path('route/<int:pk>/', views.PointListDetailDeleteView.as_view(), name='pointlist-detail-delete'),
    path('route/<int:route_id>/punkty/', views.PointListView.as_view(), name='point-list'),
    path('route/<int:route_id>/punkty/new/', views.PointCreateView.as_view(), name='point-create'),
    path('route/<int:route_id>/punkty/<int:point_id>/delete/', views.PointDeleteView.as_view(), name='point-delete'),
]

urlpatterns += [
    path('token/', obtain_auth_token),
]

urlpatterns += [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]