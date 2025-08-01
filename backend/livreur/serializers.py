# livraison/serializers.py
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'phone_number']
        read_only_fields = ['id', 'email', 'username']

class JustificatifTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JustificatifType
        fields = '__all__'

class ProfilLivreurSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ProfilLivreur
        fields = '__all__'
        read_only_fields = ['user']

class JustificatifSerializer(serializers.ModelSerializer):
    type_nom = serializers.ReadOnlyField(source='type_justificatif.nom')
    
    class Meta:
        model = Justificatif
        fields = ['id', 'livreur', 'type_justificatif', 'type_nom', 'fichier', 'date_upload', 'statut', 'commentaire_admin']
        read_only_fields = ['livreur', 'date_upload', 'statut', 'commentaire_admin']



class TrajetAnnonceSerializer(serializers.ModelSerializer):
    livreur_nom = serializers.ReadOnlyField(source='livreur.get_full_name')
    photo_produit_url = serializers.SerializerMethodField()  # Ajout pour l'URL complète
    
    class Meta:
        model = TrajetAnnonce
        fields = '__all__'
        read_only_fields = ['livreur', 'date_creation', 'livreur_nom']
    
    def get_photo_produit_url(self, obj):
        """Retourne l'URL complète de la photo"""
        if obj.photo_produit:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo_produit.url)
            return obj.photo_produit.url
        return None
    
    def validate_photo_produit(self, value):
        """Validation de la photo"""
        if value:
            # Vérifier la taille du fichier (max 5MB)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError('La taille de l\'image ne doit pas dépasser 5MB')
            
            # Vérifier le format
            valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            if not any(value.name.lower().endswith(ext) for ext in valid_extensions):
                raise serializers.ValidationError('Format d\'image non supporté. Utilisez JPG, PNG ou WebP')
        
        return value
    
class LivraisonSerializer(serializers.ModelSerializer):
    livreur_nom = serializers.ReadOnlyField(source='livreur.get_full_name')
    trajet_annonce = TrajetAnnonceSerializer(read_only=True)

    class Meta:
        model = Livraison
        fields = '__all__'
        read_only_fields = [
            'livreur',
            'livreur_nom',
            'commission_plateforme',
            'trajet_annonce'
        ]

class PaiementSerializer(serializers.ModelSerializer):
    livraisons_details = LivraisonSerializer(source='livraisons', many=True, read_only=True)
    montant = serializers.SerializerMethodField()
    total_commission = serializers.SerializerMethodField()
    
    class Meta:
        model = Paiement
        fields = ['id', 'livreur', 'livraisons', 'livraisons_details', 'date', 'reference', 
                  'statut', 'montant', 'total_commission']
        read_only_fields = ['livreur', 'reference', 'date', 'statut', 'livraisons_details']
        
    def get_montant(self, obj):
        return obj.montant
    
    def get_total_commission(self, obj):
        return obj.total_commission

class DisponibiliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disponibilite
        fields = '__all__'
        read_only_fields = ['livreur']
        

class StatutLivraisonClientSerializer(serializers.ModelSerializer):
    """Serializer simple pour que le client voie le statut de ses livraisons"""
    
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    livreur_nom = serializers.CharField(source='livreur.get_full_name', read_only=True)
    trajet_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Livraison
        fields = [
            'id',
            'statut',
            'statut_display',
            'livreur_nom',
            'trajet_info',
            'commentaire_client',
            'commentaire_livreur'
        ]
        read_only_fields = [
            'id', 'statut', 'statut_display', 'livreur_nom', 
            'trajet_info', 'commentaire_client', 'commentaire_livreur'
        ]
    
    def get_trajet_info(self, obj):
        """Infos basiques du trajet"""
        if obj.trajet_annonce:
            return {
                'depart': obj.trajet_annonce.ville_depart,
                'arrivee': obj.trajet_annonce.ville_arrivee,
                'date_depart': obj.trajet_annonce.date_depart
            }
        return None
    


# Ajoutez ces serializers à la fin de votre fichier serializers.py

# SERIALIZERS POUR LE SUIVI CLIENT
class StatutLivraisonClientSerializer(serializers.ModelSerializer):
    """Serializer pour que le client voie le statut de ses livraisons"""
    
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    livreur_nom = serializers.CharField(source='livreur.get_full_name', read_only=True)
    trajet_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Livraison
        fields = [
            'id',
            'statut',
            'statut_display',
            'livreur_nom',
            'trajet_info',
            'commentaire_client',
            'commentaire_livreur'
        ]
        read_only_fields = [
            'id', 'statut', 'statut_display', 'livreur_nom', 
            'trajet_info', 'commentaire_client', 'commentaire_livreur'
        ]
    
    def get_trajet_info(self, obj):
        """Infos basiques du trajet"""
        if obj.trajet_annonce:
            return {
                'depart': obj.trajet_annonce.ville_depart,
                'arrivee': obj.trajet_annonce.ville_arrivee,
                'date_depart': obj.trajet_annonce.date_depart
            }
        return None

# SERIALIZERS POUR LES FACTURES
class FactureSerializer(serializers.ModelSerializer):
    """Serializer pour les factures"""
    
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    livraison = StatutLivraisonClientSerializer(read_only=True)
    
    class Meta:
        model = Facture
        fields = [
            'id', 'numero', 'livraison', 'montant_ht', 'taux_tva',
            'montant_tva', 'montant_ttc', 'date_creation', 'date_echeance',
            'date_paiement_client', 'date_liberation_fonds', 'statut', 'statut_display',
            'confirmation_livraison_livreur', 'confirmation_reception_client',
            'date_confirmation_livreur', 'date_confirmation_client', 'delai_auto_liberation'
        ]
        read_only_fields = '__all__'

# SERIALIZERS POUR LES COMPTES LIVREURS
class CompteLivreurSerializer(serializers.ModelSerializer):
    """Serializer pour les comptes livreurs"""
    
    class Meta:
        model = CompteLivreur
        fields = ['id', 'nom_titulaire', 'stripe_account_id', 'stripe_verified', 'date_creation']
        read_only_fields = ['id', 'stripe_account_id', 'stripe_verified', 'date_creation']

# SERIALIZERS POUR LES PAIEMENTS LIVREURS
class PaiementLivreurSerializer(serializers.ModelSerializer):
    """Serializer pour l'historique des paiements livreurs"""
    
    facture_numero = serializers.CharField(source='facture.numero', read_only=True)
    livraison_id = serializers.IntegerField(source='facture.livraison.id', read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    
    class Meta:
        model = PaiementLivreur
        fields = [
            'id', 'facture_numero', 'livraison_id', 'montant_brut', 
            'commission_plateforme', 'montant_net', 'statut', 'statut_display', 
            'date_paiement'
        ]
        read_only_fields = '__all__'

# SERIALIZERS POUR LES NOTIFICATIONS
class NotificationSerializer(serializers.ModelSerializer):
    """Serializer pour les notifications"""
    
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['id', 'destinataire', 'date_creation']