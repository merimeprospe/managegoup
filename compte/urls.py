from django.urls import path
from . import views
urlpatterns = [
    path('adminDashboard1', views.adminDashboard1, name='adminDashboard1'),
    path('adminDashboard2', views.adminDashboard2, name='adminDashboard2'),
    path('projet/<id>', views.projet, name='projet'),
    path('notif', views.notif, name='notif'),
    path('supprime/<id>', views.delet_p, name='delet_p'),
    path('modifier/<id>', views.modif_p, name='modif_p'),
    path('supprime_a/<id>', views.delet_a, name='delet_a'),
    path('supprime_ap/<id>,<pk>', views.delet_ap, name='delet_ap'),
    path('aide', views.aide, name='aide'),
    path('espace', views.espace, name='espace'),
    path('supprime1/<id>', views.delet_p1, name='delet_p1'),
    path('supprime_a1/<id>', views.delet_a1, name='delet_a1'),
    path('carte', views.carte, name='carte'),
    path('supprime_c/<id>', views.supp, name='supp'),
    path('supprime_c1/<id>,<pk>', views.supp1, name='supp1'),
    path('supprime2/<id>', views.delet_p2, name='delet_p2'),
    path('supprime_a2/<id>', views.delet_a2, name='delet_a2'),
    path('profile/<id>', views.profile, name='profile'),
    path('delet_n/<id>,<pk>', views.delet_n, name='delet_n'),
    path('delet_no/<id>,<pk>', views.delet_no, name='delet_no'),
    path('delet_np/<id>', views.delet_np, name='delet_np'),
    path('delet_T/<id>', views.supp_t, name='delet_t'),
    path('modif_t/<id>', views.modif_t, name='madif_t'),
    path('modif_t_d/<id>', views.modif_t_d, name='madif_t_d'),
    path('carte/views/<str:tache_id>', views.views_tache_by_id, name='views')
]
