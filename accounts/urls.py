from django.urls import path
from .views import LoginView
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('api/token-auth/', obtain_jwt_token),
    path('api/login/', LoginView.as_view(), name='login'),

    # other app-specific URL patterns
]