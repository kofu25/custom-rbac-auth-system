from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    LoginView, RegisterView, LogoutView, 
    UserProfileView, ProductMockView, AccessRuleViewSet
)

router = DefaultRouter()
router.register(r'rules', AccessRuleViewSet, basename='rules')

urlpatterns = [
    path('api/register/', RegisterView.as_view()),
    path('api/login/', LoginView.as_view()),
    path('api/logout/', LogoutView.as_view()),
    path('api/profile/', UserProfileView.as_view()),
    path('api/products/', ProductMockView.as_view()),
    path('api/admin/', include(router.urls)),
]