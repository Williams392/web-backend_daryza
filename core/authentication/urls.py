from django.urls import path
from .views import *

urlpatterns = [
    path('login/', InicioSesionView.as_view(), name='login'),
    path('signup/', UserView.as_view(), name='signup'),
    path('logout/', CierreSesionView.as_view(), name='logout'),
    path('get-api-token/', CustomAuthToken.as_view()),

    path('roles/', RolListCreateView.as_view(), name='roles-list-create'),
    path('roles/<int:pk>/', RolDetailView.as_view(), name='roles-detail'),
    
    path('users/', UserView.as_view(), name='users-list-create'),
    path('users/<int:pk>/', UserView.as_view(), name='users-detail'),
]

# signup: inscribirse
# logout: cerrar sesión

