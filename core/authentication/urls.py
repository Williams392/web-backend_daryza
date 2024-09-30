from django.urls import path
from .views import InicioSesionView, RegistroView, CierreSesionView, CustomAuthToken

#from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', InicioSesionView.as_view(), name='login'),
    path('signup/', RegistroView.as_view(), name='signup'),
    path('logout/', CierreSesionView.as_view(), name='logout'),
    #path('get-api-token/', obtain_auth_token),
    path('get-api-token/', CustomAuthToken.as_view()),
]

# signup: inscribirse
# logout: cerrar sesión

