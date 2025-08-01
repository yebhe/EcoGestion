# livraison/urls.py
# This should already be in your code, but make sure the router is set up correctly
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'profil', ProfilLivreurViewSet, basename='profil-livreur')
router.register(r'justificatifs', JustificatifViewSet, basename='justificatif')
router.register(r'types-justificatifs', JustificatifTypeViewSet)
router.register(r'trajets', TrajetAnnonceViewSet, basename='trajet')
router.register(r'livraisons', LivraisonViewSet, basename='livraison')
router.register(r'paiements', PaiementViewSet, basename='paiement')
router.register(r'disponibilites', DisponibiliteViewSet, basename='disponibilite')
router.register(r'trajets-disponibles', TrajetDisponibleViewSet, basename='trajet-disponible')

urlpatterns = [
    path('livreurs/', include(router.urls)),
    path('mes-livraisons/', MesLivraisonsClientView.as_view(), name='mes-livraisons'),
    path('livraison/<int:livraison_id>/statut/', StatutLivraisonView.as_view(), name='statut-livraison'),
    path('livreurs/paiements/<int:pk>/receipt/', PaiementViewSet.as_view({'get': 'receipt'}), name='paiement-receipt'),
   
]