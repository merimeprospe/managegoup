from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth import views
from personne.views import activate, acceuil, Signup, login_view, PasswordChange, PasswordChangeDone


urlpatterns = [
    path('', acceuil, name='acceuil'),
    path('cree_p', Signup, name='cree_p'),
    path('login', login_view, name='login'),
    path('PasswordChange', PasswordChange),
    path('PasswordChange/done', PasswordChangeDone),
    path('logout', view=LogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>', activate, name='activate'),

    path('reset_password', views.PasswordResetView.as_view(template_name='personne/password_reset.html'), name='reset_password'),
    path('reset_password_send', views.PasswordResetDoneView.as_view(template_name='personne/password_reset_sent.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>', views.PasswordResetConfirmView.as_view(template_name='personne/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete', views.PasswordResetCompleteView.as_view(template_name='personne/password_reset_complete.html'), name='password_reset_complete'),


]
