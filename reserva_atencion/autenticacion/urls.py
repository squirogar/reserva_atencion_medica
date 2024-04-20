from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = "auth"

urlpatterns = [
    path("login/", views.ingresar, name="login"),
    path("registro/", views.registro, name="registro"),
    path("logout/", views.cerrar_sesion, name="cerrar_sesion"),
    
    
    
    # vistas de djagno
    path(
        "password_reset/", 
        auth_views.PasswordResetView.as_view(
            template_name="autenticacion/password_reset.html",
            email_template_name="autenticacion/password_reset_email.html",
            success_url=reverse_lazy('auth:password_reset_done')), 
        name="password_reset"
    ), #as_view() ya que es una clase que debe convertirse a view
    
    path(
        "password_reset/done/", 
        auth_views.PasswordResetDoneView.as_view(
            template_name="autenticacion/password_reset_done.html"
        ), 
        name="password_reset_done"
    ),
    
    path(
        "reset/<uidb64>/<token>/", 
        auth_views.PasswordResetConfirmView.as_view(
            template_name="autenticacion/password_reset_confirm.html",
            success_url=reverse_lazy('auth:password_reset_complete')), 
        name="password_reset_confirm"
    ), #debe si o si contener esos parámetros. Estos parametros son sacados de la documentacion de django. uidb64 es el user id codificado, token es el token para ver si la contraseña es valida.
    
    path(
        "reset/done/", 
        auth_views.PasswordResetCompleteView.as_view(
            template_name="autenticacion/password_reset_complete.html"
        ), 
        name="password_reset_complete"),
]
