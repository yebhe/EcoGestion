from rest_framework import serializers
from .models import (
    ProfilClient, AdresseLivraison, AnnonceClient, Colis,
    CommandeClient, FactureClient, SuiviColis, EvaluationClient
)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'email']


class ProfilClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ProfilClient
        fields = [
            'id', 'user', 'telephone', 'date_naissance', 'photo_profil',
            'notification_email', 'notification_sms', 'notification_push',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AdresseLivraisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdresseLivraison
        fields = [
            'id', 'client', 'nom_adresse', 'destinataire', 'adresse',
            'complement_adresse', 'code_postal', 'ville', 'pays',
            'instructions_speciales', 'par_defaut', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        # Si l'utilisateur n'a pas d'adresse et que par_defaut n'est pas défini,
        # on définit automatiquement cette adresse comme adresse par défaut
        if 'client' in data and not data.get('par_defaut'):
            if not AdresseLivraison.objects.filter(client=data['client']).exists():
                data['par_defaut'] = True
        return data


class AdresseLivraisonLightSerializer(serializers.ModelSerializer):
    """Version allégée du serializer d'adresse pour les inclusions"""
    class Meta:
        model = AdresseLivraison
        fields = ['id', 'nom_adresse', 'adresse', 'code_postal', 'ville']


class ColisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colis
        fields = [
            'id', 'annonce', 'taille', 'poids', 'longueur', 'largeur',
            'hauteur', 'contenu', 'fragile', 'photo', 'instructions_speciales',
            'assurance_souhaitee', 'valeur_declaree', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ColisDetailSerializer(serializers.ModelSerializer):
    evenements_suivi = serializers.SerializerMethodField()
    
    class Meta:
        model = Colis
        fields = [
            'id', 'annonce', 'taille', 'poids', 'longueur', 'largeur',
            'hauteur', 'contenu', 'fragile', 'photo', 'instructions_speciales',
            'assurance_souhaitee', 'valeur_declaree', 'created_at', 'updated_at',
            'evenements_suivi'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_evenements_suivi(self, obj):
        evenements = obj.evenements_suivi.all().order_by('-date_evenement')
        return SuiviColisSerializer(evenements, many=True).data


class AnnonceClientSerializer(serializers.ModelSerializer):
    adresse_depart = AdresseLivraisonLightSerializer(read_only=True)
    adresse_arrivee = AdresseLivraisonLightSerializer(read_only=True)
    adresse_depart_id = serializers.PrimaryKeyRelatedField(
        queryset=AdresseLivraison.objects.all(),
        source='adresse_depart',
        write_only=True,
        required=False
    )
    adresse_arrivee_id = serializers.PrimaryKeyRelatedField(
        queryset=AdresseLivraison.objects.all(),
        source='adresse_arrivee',
        write_only=True
    )
    
    class Meta:
        model = AnnonceClient
        fields = [
            'id', 'client', 'type_annonce', 'titre', 'description', 'prix_propose',
            'adresse_depart', 'adresse_arrivee', 'adresse_depart_id', 'adresse_arrivee_id',
            'date_souhaitee', 'heure_souhaitee', 'statut', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'client', 'statut', 'created_at', 'updated_at']
    
    def validate(self, data):
        # Vérifier que l'adresse de départ appartient bien au client
        if 'adresse_depart' in data and data['adresse_depart'] is not None:
            if data['adresse_depart'].client.user != self.context['request'].user:
                raise serializers.ValidationError({"adresse_depart": "Cette adresse ne vous appartient pas."})
        
        # Vérifier que l'adresse d'arrivée appartient bien au client
        if 'adresse_arrivee' in data:
            if data['adresse_arrivee'].client.user != self.context['request'].user:
                raise serializers.ValidationError({"adresse_arrivee": "Cette adresse ne vous appartient pas."})
        
        return data


class AnnonceClientDetailSerializer(AnnonceClientSerializer):
    colis = ColisSerializer(read_only=True)
    
    class Meta(AnnonceClientSerializer.Meta):
        fields = AnnonceClientSerializer.Meta.fields + ['colis']


class SuiviColisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuiviColis
        fields = [
            'id', 'colis', 'statut', 'date_evenement', 'description',
            'localisation', 'latitude', 'longitude', 'photo_preuve'
        ]
        read_only_fields = ['id', 'date_evenement']


class CommandeClientSerializer(serializers.ModelSerializer):
    adresse_livraison = AdresseLivraisonLightSerializer(read_only=True)
    adresse_livraison_id = serializers.PrimaryKeyRelatedField(
        queryset=AdresseLivraison.objects.all(),
        source='adresse_livraison',
        write_only=True
    )
    
    class Meta:
        model = CommandeClient
        fields = [
            'id', 'client', 'annonce', 'reference', 'montant_total', 'statut',
            'adresse_livraison', 'adresse_livraison_id', 'date_paiement',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'client', 'reference', 'statut', 'date_paiement',
            'created_at', 'updated_at'
        ]
    
    def validate_adresse_livraison_id(self, value):
        # Vérifier que l'adresse appartient au client
        if value.client.user != self.context['request'].user:
            raise serializers.ValidationError("Cette adresse ne vous appartient pas.")
        return value


class CommandeClientDetailSerializer(CommandeClientSerializer):
    annonce = AnnonceClientSerializer(read_only=True)
    facture = serializers.SerializerMethodField()
    
    class Meta(CommandeClientSerializer.Meta):
        fields = CommandeClientSerializer.Meta.fields + ['facture']
    
    def get_facture(self, obj):
        try:
            facture = obj.facture
            return FactureClientSerializer(facture).data
        except FactureClient.DoesNotExist:
            return None


class FactureClientSerializer(serializers.ModelSerializer):
    commande = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = FactureClient
        fields = [
            'id', 'commande', 'numero_facture', 'date_emission', 'date_echeance',
            'montant_ht', 'montant_tva', 'montant_ttc', 'statut', 'fichier_pdf'
        ]
        read_only_fields = [
            'id', 'commande', 'numero_facture', 'date_emission', 'date_echeance',
            'montant_ht', 'montant_tva', 'montant_ttc', 'statut', 'fichier_pdf'
        ]


class EvaluationClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationClient
        fields = [
            'id', 'client', 'commande', 'note', 'commentaire', 'date_evaluation'
        ]
        read_only_fields = ['id', 'client', 'date_evaluation']
    
    def validate_commande(self, value):
        # Vérifier que la commande appartient au client
        user = self.context['request'].user
        if value.client.user != user:
            raise serializers.ValidationError("Cette commande ne vous appartient pas.")
        
        # Vérifier que la commande est bien livrée/terminée
        if value.statut != 'LIVREE':
            raise serializers.ValidationError("Vous ne pouvez évaluer que des commandes livrées.")
            
        # Vérifier qu'il n'y a pas déjà une évaluation pour cette commande
        try:
            evaluation = EvaluationClient.objects.get(commande=value)
            if evaluation.id != getattr(self.instance, 'id', None):
                raise serializers.ValidationError("Une évaluation existe déjà pour cette commande.")
        except EvaluationClient.DoesNotExist:
            pass
            
        return value