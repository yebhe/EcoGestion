# livraison/views.py
from rest_framework import viewsets, permissions, status, filters
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO
from django.utils.translation import gettext as _
import datetime
from rest_framework.permissions import IsAuthenticated


User = get_user_model()

class IsLivreurUser(permissions.BasePermission):
    """
    Permission personnalisée pour vérifier que l'utilisateur est un livreur
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'livreur'

class ProfilLivreurViewSet(viewsets.ModelViewSet):
    serializer_class = ProfilLivreurSerializer
    permission_classes = [permissions.IsAuthenticated, IsLivreurUser]
    
    def get_queryset(self):
        return ProfilLivreur.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        profil = get_object_or_404(ProfilLivreur, user=request.user)
        serializer = self.get_serializer(profil)
        return Response(serializer.data)

class JustificatifViewSet(viewsets.ModelViewSet):
    serializer_class = JustificatifSerializer
    permission_classes = [permissions.IsAuthenticated, IsLivreurUser]
    
    def get_queryset(self):
        return Justificatif.objects.filter(livreur=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(livreur=self.request.user)

class JustificatifTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JustificatifType.objects.all()
    serializer_class = JustificatifTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class TrajetAnnonceViewSet(viewsets.ModelViewSet):
    serializer_class = TrajetAnnonceSerializer
    #permission_classes = [permissions.Is]
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        print("Utilisateur connecté :", self.request.user)
        return TrajetAnnonce.objects.order_by('-date_creation')

    def perform_create(self, serializer):
        serializer.save(livreur=self.request.user)
    
    @action(detail=True, methods=['post'], url_path='update_status')
    def update_status(self, request, pk=None):
        trajet = self.get_object()
        
        
        if trajet.statut != 'actif':
            return Response(
                {'error': 'Trajet déjà sélectionné ou invalide'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Utiliser une transaction pour assurer la cohérence
        try:
            with transaction.atomic():
                # 1. Mettre à jour le statut du trajet
                trajet.statut = 'selected'
                trajet.save()
                
                # 2. Créer automatiquement une livraison associée
                livraison = Livraison.objects.create(
                    livreur=request.user,
                    trajet_annonce=trajet,
                    statut='en_attente',
                    
                )
                
                # 3. Sérialiser les données pour la réponse
                trajet_serializer = TrajetAnnonceSerializer(trajet)
                livraison_serializer = LivraisonSerializer(livraison)
                
                return Response({
                    'success': True,
                    'message': 'Trajet sélectionné et livraison créée avec succès',
                    'trajet': trajet_serializer.data,
                    'livraison': livraison_serializer.data
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de la création de la livraison: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def annuler(self, request, pk=None):
        trajet = self.get_object()
        if trajet.statut == 'actif':
            trajet.statut = 'annule'
            trajet.save()
            return Response({'status': 'Trajet annulé'})
        return Response({'error': 'Ce trajet ne peut pas être annulé'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='upload_photo')
    def upload_photo(self, request, pk=None):
        """Upload ou mise à jour de la photo du produit"""
        trajet = self.get_object()
        
        if 'photo_produit' not in request.FILES:
            return Response(
                {'error': 'Aucun fichier photo fourni'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Supprimer l'ancienne photo si elle existe
        if trajet.photo_produit:
            trajet.photo_produit.delete(save=False)
        
        # Ajouter la nouvelle photo
        trajet.photo_produit = request.FILES['photo_produit']
        
        try:
            trajet.full_clean()  # Validation
            trajet.save()
            
            serializer = TrajetAnnonceSerializer(trajet, context={'request': request})
            return Response({
                'success': True,
                'message': 'Photo uploadée avec succès',
                'trajet': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de l\'upload: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['delete'], url_path='delete_photo')
    def delete_photo(self, request, pk=None):
        """Supprimer la photo du produit"""
        trajet = self.get_object()
        
        if not trajet.photo_produit:
            return Response(
                {'error': 'Aucune photo à supprimer'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            trajet.photo_produit.delete(save=True)
            
            serializer = TrajetAnnonceSerializer(trajet, context={'request': request})
            return Response({
                'success': True,
                'message': 'Photo supprimée avec succès',
                'trajet': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de la suppression: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





class LivraisonViewSet(viewsets.ModelViewSet):
    serializer_class = LivraisonSerializer
    
    def get_queryset(self):
        # TEMPORAIRE: Retourner toutes les livraisons pour voir les données
        return Livraison.objects.all().select_related('trajet_annonce', 'livreur')
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        livraison = self.get_object()
        nouveau_statut = request.data.get('statut')
        
        statuts_valides = [choix[0] for choix in Livraison._meta.get_field('statut').choices]
        if nouveau_statut not in statuts_valides:
            return Response({'error': 'Statut invalide'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Vérifier que la transition de statut est valide
        transitions_valides = {
            'en_attente': ['confirmee', 'annulee'],
            'confirmee': ['en_preparation', 'annulee'],
            'en_preparation': ['en_cours', 'annulee'],
            'en_cours': ['livree', 'annulee'],
            'livree': [],
            'annulee': []
        }
        
        if nouveau_statut not in transitions_valides.get(livraison.statut, []):
            return Response({
                'error': f'Transition de statut invalide de {livraison.statut} vers {nouveau_statut}'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Mettre à jour le statut
        livraison.statut = nouveau_statut
        if nouveau_statut == 'livree':
            livraison.date_livraison_reelle = timezone.now()
            
            self.gerer_facture_apres_livraison(livraison)
        livraison.save()
        
        return Response({'status': f'Statut mis à jour: {nouveau_statut}'})
    
    def gerer_facture_apres_livraison(self, livraison):
        """Créer ou mettre à jour la facture quand la livraison est marquée comme livrée"""
        try:
            # Essayer de récupérer la facture existante
            facture = livraison.facture
            facture.statut = 'livree_impayee'
            facture.date_livraison_confirmee = timezone.now()
            facture.delai_paiement = timezone.now() + timedelta(days=7)
            facture.save()
            
        except Facture.DoesNotExist:
            # Créer une nouvelle facture si elle n'existe pas
            if livraison.trajet_annonce and livraison.trajet_annonce.montant and livraison.client:
                montant_ht = float(livraison.trajet_annonce.montant) / 1.20  # Calculer HT depuis TTC
                
                facture = Facture.objects.create(
                    livraison=livraison,
                    client=livraison.client,
                    montant_ht=montant_ht,
                    statut='livree_impayee',
                    date_livraison_confirmee=timezone.now(),
                    delai_paiement=timezone.now() + timedelta(days=7)
                )
        
        # Notifier le client qu'il peut maintenant payer
        if hasattr(livraison, 'client') and livraison.client:
            # Créer une notification (vous devrez importer le modèle Notification)
            try:
                from .models import Notification
                Notification.objects.create(
                    destinataire=livraison.client,
                    titre="📦 Livraison effectuée - Paiement disponible",
                    message=f"Votre livraison #{livraison.id} a été effectuée avec succès ! Vous pouvez maintenant procéder au paiement. Délai: 7 jours.",
                    type_notification='paiement'
                )
            except:
                pass
    
    @action(detail=True, methods=['post'])
    def ajouter_commentaire(self, request, pk=None):
        livraison = self.get_object()
        commentaire = request.data.get('commentaire')
        
        if not commentaire:
            return Response({'error': 'Le commentaire ne peut pas être vide'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        livraison.commentaire_livreur = commentaire
        livraison.save()
        
        return Response({'status': 'Commentaire ajouté'})


class DisponibiliteViewSet(viewsets.ModelViewSet):
    serializer_class = DisponibiliteSerializer
    permission_classes = [permissions.IsAuthenticated, IsLivreurUser]
    
    def get_queryset(self):
        return Disponibilite.objects.filter(livreur=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(livreur=self.request.user)
        
    
    
# Ajout à livraison/views.py - Version optimisée

from rest_framework.permissions import IsAuthenticated

class TrajetDisponibleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset pour accéder aux trajets disponibles par tous les utilisateurs
    Utilisé pour permettre aux clients de voir et sélectionner des trajets
    """
    serializer_class = TrajetAnnonceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['date_depart', 'ville_depart', 'ville_arrivee']
    search_fields = ['ville_depart', 'ville_arrivee', 'code_postal_depart', 'code_postal_arrivee']
    ordering = ['date_depart']
    
    def get_queryset(self):
        # Seulement les trajets actifs et à venir sont disponibles
        now = timezone.now()
        return TrajetAnnonce.objects.filter(
            statut='actif',
            date_depart__gt=now
        )

class ReservationLivraisonViewSet(viewsets.ModelViewSet):
    """
    Viewset pour permettre aux clients de réserver un trajet
    Version optimisée qui utilise les informations du trajet directement
    """
    serializer_class = LivraisonSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Les clients ne voient que leurs propres livraisons
        return Livraison.objects.filter(client=self.request.user)
    
    def perform_create(self, serializer):
        # Récupérer le trajet sélectionné
        trajet_id = self.request.data.get('trajet_annonce')
        if not trajet_id:
            raise serializers.ValidationError({"trajet_annonce": "Le trajet est obligatoire"})
            
        trajet = get_object_or_404(TrajetAnnonce, id=trajet_id, statut='actif')
        
        # Récupérer et valider le poids et le volume
        poids = float(self.request.data.get('poids', 0))
        volume = float(self.request.data.get('volume', 0))
        
        if not poids or poids <= 0:
            raise serializers.ValidationError({"poids": "Le poids doit être positif"})
            
        if not volume or volume <= 0:
            raise serializers.ValidationError({"volume": "Le volume doit être positif"})
        
        if poids > trajet.capacite_poids:
            raise serializers.ValidationError({
                'poids': f'Le poids ({poids} kg) dépasse la capacité disponible ({trajet.capacite_poids} kg)'
            })
            
        if volume > trajet.capacite_volume:
            raise serializers.ValidationError({
                'volume': f'Le volume ({volume} m³) dépasse la capacité disponible ({trajet.capacite_volume} m³)'
            })
        
        # Calculer la commission et le montant (à adapter selon votre logique de prix)
        montant = self.calculer_montant(poids, volume, trajet)
        commission = montant * 0.10  # Par exemple 10% de commission
        
        # Récupérer le commentaire client s'il existe
        commentaire_client = self.request.data.get('commentaire_client', '')
        
        # Enregistrer la livraison en utilisant les données du trajet
        serializer.save(
            client=self.request.user,
            livreur=trajet.livreur,
            trajet_annonce=trajet,
            # Utiliser les adresses du trajet directement
            adresse_depart=trajet.adresse_depart,
            adresse_arrivee=trajet.adresse_arrivee,
            # Utiliser la date du trajet comme date de livraison prévue
            date_livraison_prevue=trajet.date_arrivee,
            montant=montant,
            commission_plateforme=commission,
            poids=poids,
            volume=volume,
            commentaire_client=commentaire_client,
            statut='en_attente'
        )
        
        # Mettre à jour les capacités du trajet
        trajet.capacite_poids -= poids
        trajet.capacite_volume -= volume
        trajet.save()
        
        # Si le trajet n'a plus de capacité, le marquer comme complété
        if trajet.capacite_poids <= 0 or trajet.capacite_volume <= 0:
            trajet.statut = 'complete'
            trajet.save()
        
    def calculer_montant(self, poids, volume, trajet):
        """
        Calculer le montant de la livraison en fonction du poids, du volume et du trajet
        À adapter selon votre logique de tarification
        """
        # Base de calcul: 2€ par kg + 10€ par m³
        montant_base = (poids * 2) + (volume * 10)
        
        # Ajouter un coût kilométrique (exemple: 0.5€ par km)
        # Cette méthode simplifiée pourrait être remplacée par un calcul de distance réel
        # entre les villes de départ et d'arrivée
        distance_km = 20  # Exemple, à remplacer par un calcul réel
        montant_distance = distance_km * 0.5
        
        return montant_base + montant_distance
    
    # Ajout à livraison/views.py - Endpoint d'annulation client

# Dans la classe ReservationLivraisonViewSet, ajoutez cette méthode

    @action(detail=True, methods=['post'])
    def annuler(self, request, pk=None):
        """
        Permet au client d'annuler une livraison en attente de confirmation
        """
        livraison = self.get_object()
        
        # Vérifier que la livraison peut être annulée
        if livraison.statut != 'en_attente':
            return Response({
                'error': 'Seules les livraisons en attente de confirmation peuvent être annulées'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Annuler la livraison
        livraison.statut = 'annulee'
        livraison.save()
        
        # Si un trajet était associé, restaurer ses capacités
        if livraison.trajet_annonce:
            trajet = livraison.trajet_annonce
            
            # Restaurer les capacités du trajet
            if livraison.poids and livraison.poids > 0:
                trajet.capacite_poids += livraison.poids
            
            if livraison.volume and livraison.volume > 0:
                trajet.capacite_volume += livraison.volume
            
            # Réactiver le trajet si nécessaire
            if trajet.statut == 'complete':
                trajet.statut = 'actif'
                
            trajet.save()
        
        return Response({'status': 'Livraison annulée'})
        
# recu pdf
class PaiementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaiementSerializer
    permission_classes = [permissions.IsAuthenticated, IsLivreurUser]
    
    def get_queryset(self):
        return Paiement.objects.filter(livreur=self.request.user)
    
    @action(detail=True, methods=['get'])
    def receipt(self, request, pk=None):
        paiement = self.get_object()
        
        # Create a file-like buffer to receive PDF data
        buffer = BytesIO()
        
        # Create the PDF object using the buffer as its "file"
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4  # 595.2, 841.8 points
        
        # Set up the document with company info
        p.setFont('Helvetica-Bold', 18)
        p.drawString(50, height - 50, "EcoDeli")
        
        p.setFont('Helvetica', 10)
        p.drawString(50, height - 70, "123 Rue de la Livraison")
        p.drawString(50, height - 85, "75002 Paris, France")
        p.drawString(50, height - 100, "Email: wissam@EcoDeli.com")
        p.drawString(50, height - 115, "Tel: +33 1 23 45 67 89")
        
        # Add receipt title and number
        p.setFont('Helvetica-Bold', 14)
        p.drawString(50, height - 160, f"REÇU DE PAIEMENT #{paiement.reference}")
        
        # Add recipient info (livreur)
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, height - 200, "Destinataire:")
        p.setFont('Helvetica', 10)
        p.drawString(50, height - 215, f"Nom: {paiement.livreur.get_full_name()}")
        p.drawString(50, height - 230, f"ID: {paiement.livreur.id}")
        if hasattr(paiement.livreur, 'profil_livreur'):
            p.drawString(50, height - 245, f"IBAN: {paiement.livreur.profil_livreur.iban}")
        
        # Add payment details
        p.setFont('Helvetica-Bold', 12)
        p.drawString(300, height - 200, "Détails du paiement:")
        p.setFont('Helvetica', 10)
        p.drawString(300, height - 215, f"Date: {paiement.date.strftime('%d/%m/%Y')}")
        p.drawString(300, height - 230, f"Statut: {paiement.get_statut_display()}")
        p.drawString(300, height - 245, f"Montant: {paiement.montant:.2f} €")
        p.drawString(300, height - 260, f"Commission totale: {paiement.total_commission:.2f} €")
        
        # Add table with deliveries details
        if paiement.livraisons.exists():
            # Table header
            data = [["#", "Client", "Date", "Montant Net", "Commission", "Statut"]]
            
            # Table data
            for livraison in paiement.livraisons.all():
                date = livraison.date_livraison_reelle or livraison.date_livraison_prevue
                date_str = date.strftime('%d/%m/%Y') if date else "N/A"
                
                montant = float(livraison.montant) if livraison.montant is not None else 0
                commission = float(livraison.commission_plateforme) if livraison.commission_plateforme is not None else 0
                montant_net = montant - commission
                
                data.append([
                    str(livraison.id),
                    livraison.client.get_full_name() if hasattr(livraison, 'client') and livraison.client else "N/A",
                    date_str,
                    f"{montant_net:.2f} €",
                    f"{commission:.2f} €",
                    livraison.get_statut_display()
                ])
            
            # Create the table
            table = Table(data, colWidths=[30, 130, 90, 70, 70, 80])
            
            # Style the table
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])
            
            table.setStyle(style)
            
            # Draw the table
            table.wrapOn(p, width - 100, height)
            table.drawOn(p, 50, height - 350)
        
        # Add summary
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, height - 400 if paiement.livraisons.exists() else height - 300, "Récapitulatif:")
        
        y_position = height - 420 if paiement.livraisons.exists() else height - 320
        
        p.setFont('Helvetica', 10)
        p.drawString(50, y_position, f"Nombre de livraisons: {paiement.livraisons.count()}")
        p.drawString(50, y_position - 15, f"Montant total: {paiement.montant:.2f} €")
        p.drawString(50, y_position - 30, f"Commission totale: {paiement.total_commission:.2f} €")
        p.drawString(50, y_position - 45, f"Note: La commission est prélevée directement par la plateforme")
        
        # Add footer
        p.setFont('Helvetica-Oblique', 8)
        p.drawString(50, 50, "Ce document est un reçu officiel émis par EcoDeli.")
        p.drawString(50, 35, f"Date d'émission: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        # Add page number
        p.drawRightString(width - 50, 35, f"Page 1/1")
        
        # Close the PDF object cleanly
        p.showPage()
        p.save()
        
        # Get the value of the BytesIO buffer and return response
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="receipt_{paiement.reference}.pdf"'
        
        return response
    


# Ajoutez à votre livraison/views.py

class MesLivraisonsClientView(APIView):
    """Vue pour que le client voie ses livraisons et leur statut"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Liste des livraisons du client connecté"""
        # Adaptez selon votre champ client dans le modèle Livraison
        # Si vous n'avez pas de champ client, vous devrez l'ajouter au modèle
        livraisons = Livraison.objects.filter(
            # client=request.user  # Si vous avez un champ client
            # Ou une autre logique selon votre structure
        ).order_by('-id')
        
        serializer = StatutLivraisonClientSerializer(livraisons, many=True)
        return Response(serializer.data)

class StatutLivraisonView(APIView):
    """Vue pour voir le statut d'une livraison spécifique"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, livraison_id):
        """Statut d'une livraison"""
        livraison = get_object_or_404(Livraison, id=livraison_id)
        # Vérifiez que c'est bien la livraison du client
        # if livraison.client != request.user:
        #     return Response({'error': 'Non autorisé'}, status=403)
        
        serializer = StatutLivraisonClientSerializer(livraison)
        return Response(serializer.data)




