from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# app_name = 'client'

# router = DefaultRouter()
# router.register(r'profil', views.ProfilClientViewSet, basename='profil')
# router.register(r'adresses', views.AdresseLivraisonViewSet, basename='adresse')
# router.register(r'annonces', views.AnnonceClientViewSet, basename='annonce')
# router.register(r'colis', views.ColisViewSet, basename='colis')
# router.register(r'commandes', views.CommandeClientViewSet, basename='commande')
# router.register(r'factures', views.FactureClientViewSet, basename='facture')
# router.register(r'suivi', views.SuiviColisViewSet, basename='suivi')
# router.register(r'evaluations', views.EvaluationClientViewSet, basename='evaluation')

urlpatterns = [
    # path('', include(router.urls)),
    # URLs personnalisées supplémentaires
    # path('me/', views.ProfilClientViewSet.as_view({'get': 'me'}), name='me'),
    # path('dashboard/', views.ClientDashboardView.as_view(), name='dashboard'),

]