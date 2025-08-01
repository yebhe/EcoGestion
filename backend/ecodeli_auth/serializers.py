from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

User = get_user_model()

class UserModelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 
            'username',
            'email',
            'is_active',
            'first_name',
            'last_name',
            'phone_number',
            'password',
            'user_type'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True}
        }
    
    def create(self, validated_data):
        # Créer un utilisateur avec un statut par défaut
        validated_data['is_active'] = False
        user = User.objects.create_user(**validated_data)
        return user

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 
            'username',
            'is_superuser',
            'email',
            'first_name',
            'phone_number',
            'last_name',
            'user_type',
            'status'
        )

class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username')

class UserModelUpdatePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('password', 're_password')
    
    def validate(self, attrs):
        # Validation des mots de passe
        password = attrs.get('password')
        re_password = attrs.get('re_password')
        
        if password != re_password:
            raise serializers.ValidationError({
                "re_password": "Les mots de passe ne correspondent pas."
            })
        
        try:
            password_validation.validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({
                "password": list(e.messages)
            })
        
        return attrs

class PasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        # Vérifier que les nouveaux mots de passe correspondent
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({
                "confirm_password": "Les mots de passe doivent correspondre."
            })
        
        # Valider le nouveau mot de passe selon les règles de Django
        try:
            password_validation.validate_password(data['new_password'])
        except ValidationError as e:
            raise serializers.ValidationError({
                "new_password": list(e.messages)
            })
        
        return data
    
    def save(self):
        # Gérer la mise à jour du mot de passe
        user = self.context['request'].user
        old_password = self.initial_data['old_password']
        
        # Vérifier l'ancien mot de passe
        if not user.check_password(old_password):
            raise serializers.ValidationError({
                "old_password": "L'ancien mot de passe est incorrect."
            })
        
        # Définir le nouveau mot de passe
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user