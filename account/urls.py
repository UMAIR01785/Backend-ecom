from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('register/',RegisterView.as_view(),name="register"),
    path('activate/<uidb64>/<token>/',Activateview.as_view(),name="activate"),
    path('login/',TokenObtainPairView.as_view(),name='login'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('logout/',Logoutapiview.as_view(),name='logout'),
    path('reset/',Resetview.as_view(),name='reset'),
    path('resetpassword/<uid64>/<token>/',Resetpasswordview.as_view(),name='resetpassword')
]