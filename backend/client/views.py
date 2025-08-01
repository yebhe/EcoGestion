# from rest_framework import viewsets, permissions, status, filters
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
# from .models import (
#     ProfilClient, AdresseLivraison, AnnonceClient, Colis,
#     CommandeClient, FactureClient, SuiviColis, EvaluationClient
# )
# from .serializers import (
#     ProfilClientSerializer, AdresseLivraisonSerializer, 
#     AnnonceClientSerializer, AnnonceClientDetailSerializer,
#     ColisSerializer, ColisDetailSerializer,
#     CommandeClientSerializer, CommandeClientDetailSerializer,
#     FactureClientSerializer, SuiviColisSerializer, EvaluationClientSerializer
# )
# from rest_framework.views import APIView
# from rest_framework import permissions, status
# from django.db.models import Sum
# from django.utils import timezone
# from datetime import timedelta

# class IsOwnerOrReadOnly(permissions.BasePermission):
#     """
#     Permission personnalisée pour permettre uniquement aux propriétaires 
#     d'un objet de le modifier.
#     """
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
        
#         if hasattr(obj, 'client'):
#             return obj.client.user == request.user
#         elif hasattr(obj, 'user'):
#             return obj.user == request.user
#         return False


# class ProfilClientViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint pour afficher et modifier le profil client.
#     """
#     serializer_class = ProfilClientSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_queryset(self):
#         return ProfilClient.objects.filter(user=self.request.user)
    
#     def get_object(self):
#         queryset = self.get_queryset()
#         obj = get_object_or_404(queryset, user=self.request.user)
#         self.check_object_permissions(self.request, obj)
#         return obj
    
#     @action(detail=False, methods=['get'])
#     def me(self, request):
#         profil = self.get_object()
#         serializer = self.get_serializer(profil)
#         return Response(serializer.data)
    

# class AdresseLivraisonViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint pour afficher et modifier les adresses de livraison.
#     """
#     serializer_class = AdresseLivraisonSerializer
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
#     def get_queryset(self):
#         try:
#             client = ProfilClient.objects.get(user=self.request.user)
#             return AdresseLivraison.objects.filter(client=client)
#         except ProfilClient.DoesNotExist:
#             return AdresseLivraison.objects.none()
    
#     def perform_create(self, serializer):
#         client = ProfilClient.objects.get(user=self.request.user)
#         serializer.save(client=client)


# class AnnonceClientViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint pour afficher et modifier les annonces client.
#     """
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
#     filter_backends = [filters.OrderingFilter]
#     filterset_fields = ['type_annonce', 'statut']
#     ordering_fields = ['date_souhaitee', 'created_at', 'prix_propose']
#     ordering = ['-created_at']
    
#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return AnnonceClientDetailSerializer
#         return AnnonceClientSerializer
    
#     def get_queryset(self):
#         try:
#             client = ProfilClient.objects.get(user=self.request.user)
#             return AnnonceClient.objects.filter(client=client)
#         except ProfilClient.DoesNotExist:
#             return AnnonceClient.objects.none()
    
#     def perform_create(self, serializer):
#         client = ProfilClient.objects.get(user=self.request.user)
#         serializer.save(client=client)
    
#     @action(detail=True, methods=['post'])
#     def ajouter_colis(self, request, pk=None):
#         annonce = self.get_object()
        
#         # Vérifier que l'annonce est de type livraison
#         if annonce.type_annonce != 'LIVRAISON':
#             return Response(
#                 {"detail": "Vous ne pouvez ajouter un colis qu'à une annonce de type livraison."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         # Vérifier si un colis existe déjà
#         try:
#             colis = Colis.objects.get(annonce=annonce)
#             serializer = ColisSerializer(colis, data=request.data)
#         except Colis.DoesNotExist:
#             serializer = ColisSerializer(data=request.data)
        
#         if serializer.is_valid():
#             serializer.save(annonce=annonce)
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ColisViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     API endpoint pour afficher les colis.
#     """
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return ColisDetailSerializer
#         return ColisSerializer
    
#     def get_queryset(self):
#         try:
#             client = ProfilClient.objects.get(user=self.request.user)
#             return Colis.objects.filter(annonce__client=client)
#         except ProfilClient.DoesNotExist:
#             return Colis.objects.none()


# class CommandeClientViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint pour afficher et modifier les commandes client.
#     """
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
#     filter_backends = [filters.OrderingFilter]
#     filterset_fields = ['statut']
#     ordering_fields = ['created_at']
#     ordering = ['-created_at']
    
#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return CommandeClientDetailSerializer
#         return CommandeClientSerializer
    
#     def get_queryset(self):
#         try:
#             client = ProfilClient.objects.get(user=self.request.user)
#             return CommandeClient.objects.filter(client=client)
#         except ProfilClient.DoesNotExist:
#             return CommandeClient.objects.none()
    
#     def perform_create(self, serializer):
#         client = ProfilClient.objects.get(user=self.request.user)
        
#         # Générer une référence unique
#         import uuid
#         reference = f"CMD-{uuid.uuid4().hex[:8].upper()}"
        
#         serializer.save(client=client, reference=reference)

#     @action(detail=True, methods=['post'])
#     def initialiser_paiement(self, request, pk=None):
#         commande = self.get_object()
        
#         # Vérifier que la commande est en attente de paiement
#         if commande.statut != 'ATTENTE_PAIEMENT':
#             return Response(
#                 {"detail": "Cette commande n'est pas en attente de paiement."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         # Code pour initialiser le paiement avec Stripe
#         try:
#             import stripe
#             from django.conf import settings
#             import datetime
            
#             stripe.api_key = settings.STRIPE_SECRET_KEY
            
#             # Créer l'intention de paiement
#             payment_intent = stripe.PaymentIntent.create(
#                 amount=int(commande.montant_total * 100),  # Stripe utilise les centimes
#                 currency="eur",
#                 metadata={"commande_id": commande.id}
#             )
            
#             # Mettre à jour la commande
#             commande.stripe_payment_intent = payment_intent.id
#             commande.save()
            
#             return Response({
#                 "client_secret": payment_intent.client_secret,
#                 "publishable_key": settings.STRIPE_PUBLISHABLE_KEY
#             })
#         except Exception as e:
#             return Response(
#                 {"detail": f"Erreur lors de l'initialisation du paiement: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )


# class FactureClientViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     API endpoint pour afficher les factures client.
#     """
#     serializer_class = FactureClientSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_queryset(self):
#         try:
#             client = ProfilClient.objects.get(user=self.request.user)
#             return FactureClient.objects.filter(commande__client=client)
#         except ProfilClient.DoesNotExist:
#             return FactureClient.objects.none()


# class SuiviColisViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     API endpoint pour afficher le suivi des colis.
#     """
#     serializer_class = SuiviColisSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_queryset(self):
#         try:
#             client = ProfilClient.objects.get(user=self.request.user)
#             return SuiviColis.objects.filter(colis__annonce__client=client)
#         except ProfilClient.DoesNotExist:
#             return SuiviColis.objects.none()


# class EvaluationClientViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint pour afficher et modifier les évaluations client.
#     """
#     serializer_class = EvaluationClientSerializer
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
#     def get_queryset(self):
#         try:
#             client = ProfilClient.objects.get(user=self.request.user)
#             return EvaluationClient.objects.filter(client=client)
#         except ProfilClient.DoesNotExist:
#             return EvaluationClient.objects.none()
    
#     def perform_create(self, serializer):
#         client = ProfilClient.objects.get(user=self.request.user)
#         serializer.save(client=client)
        

# class ClientDashboardView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get(self, request):
#         try:
#             client = ProfilClient.objects.get(user=request.user)
#         except ProfilClient.DoesNotExist:
#             return Response({"detail": "Profil client non trouvé."}, status=status.HTTP_404_NOT_FOUND)
        
#         date_debut = timezone.now() - timedelta(days=30)
        
#         annonces_stats = {
#             'total': AnnonceClient.objects.filter(client=client).count(),
#             'actives': AnnonceClient.objects.filter(client=client, statut='ACTIVE').count(),
#             'en_cours': AnnonceClient.objects.filter(client=client, statut='EN_COURS').count(),
#             'terminees': AnnonceClient.objects.filter(client=client, statut='TERMINEE').count(),
#             'annulees': AnnonceClient.objects.filter(client=client, statut='ANNULEE').count(),
#             'recentes': AnnonceClient.objects.filter(client=client, created_at__gte=date_debut).count(),
#         }
        
#         commandes_stats = {
#             'total': CommandeClient.objects.filter(client=client).count(),
#             'en_attente': CommandeClient.objects.filter(client=client, statut='ATTENTE_PAIEMENT').count(),
#             'en_cours': CommandeClient.objects.filter(client=client, statut__in=['PAIEMENT_CONFIRME', 'EN_PREPARATION', 'EN_COURS_LIVRAISON']).count(),
#             'livrees': CommandeClient.objects.filter(client=client, statut='LIVREE').count(),
#             'annulees': CommandeClient.objects.filter(client=client, statut='ANNULEE').count(),
#             'recentes': CommandeClient.objects.filter(client=client, created_at__gte=date_debut).count(),
#             'montant_total': CommandeClient.objects.filter(client=client).aggregate(total=Sum('montant_total'))['total'] or 0,
#         }
        
#         colis_stats = {
#             'total': Colis.objects.filter(annonce__client=client).count(),
#             'en_transit': SuiviColis.objects.filter(
#                 colis__annonce__client=client, 
#                 statut__in=['PRIS_EN_CHARGE', 'EN_TRANSIT', 'EN_ENTREPOT', 'EN_LIVRAISON']
#             ).values('colis').distinct().count(),
#             'livres': SuiviColis.objects.filter(
#                 colis__annonce__client=client, 
#                 statut='LIVRE'
#             ).values('colis').distinct().count(),
#             'incidents': SuiviColis.objects.filter(
#                 colis__annonce__client=client, 
#                 statut='INCIDENT'
#             ).values('colis').distinct().count(),
#         }
        
#         dernieres_annonces = AnnonceClient.objects.filter(client=client).order_by('-created_at')[:5]
        
#         dernieres_commandes = CommandeClient.objects.filter(client=client).order_by('-created_at')[:5]
        
#         colis_en_transit = []
#         for colis in Colis.objects.filter(annonce__client=client):
#             dernier_suivi = SuiviColis.objects.filter(colis=colis).order_by('-date_evenement').first()
#             if dernier_suivi and dernier_suivi.statut != 'LIVRE':
#                 colis_data = ColisSerializer(colis).data
#                 colis_data['dernier_statut'] = dernier_suivi.statut
#                 colis_data['dernier_statut_libelle'] = dernier_suivi.get_statut_display()
#                 colis_data['derniere_maj'] = dernier_suivi.date_evenement
#                 colis_data['derniere_localisation'] = dernier_suivi.localisation
#                 colis_en_transit.append(colis_data)
        
#         # Construire la réponse
#         response_data = {
#             'annonces_stats': annonces_stats,
#             'commandes_stats': commandes_stats,
#             'colis_stats': colis_stats,
#             'dernieres_annonces': AnnonceClientSerializer(dernieres_annonces, many=True).data,
#             'dernieres_commandes': CommandeClientSerializer(dernieres_commandes, many=True).data,
#             'colis_en_transit': colis_en_transit,
#             'nb_adresses': AdresseLivraison.objects.filter(client=client).count(),
#         }
        
#         return Response(response_data)