from django.urls import path
from .views import *

urlpatterns = [
    path('login/', InicioSesionView.as_view(), name='login'),
    path('signup/', RegistroView.as_view(), name='signup'),
    path('logout/', CierreSesionView.as_view(), name='logout'),
    path('get-api-token/', CustomAuthToken.as_view()),

    path('roles/', RolListCreateView.as_view(), name='roles-list-create'),
    path('roles/<int:pk>/', RolDetailView.as_view(), name='roles-detail'),
    path('perfiles/', PerfilListCreateView.as_view(), name='perfiles-list-create'),
    path('perfiles/<int:pk>/', PerfilDetailView.as_view(), name='perfiles-detail'),
]

# signup: inscribirse
# logout: cerrar sesión

