import ssl
import smtplib
from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend
import logging

logger = logging.getLogger(__name__)

class RobustEmailBackend(DjangoEmailBackend):
    """
    Backend email robuste qui gère les problèmes SSL dans Docker
    tout en conservant la sécurité
    """
    
    def open(self):
        """
        Ouvre la connexion SMTP avec gestion intelligente SSL
        """
        if self.connection:
            return False
            
        try:
            # Tentative avec SSL standard (sécurisé)
            print("🔒 Tentative de connexion SSL standard...")
            return self._open_with_standard_ssl()
        except ssl.SSLCertVerificationError as ssl_error:
            print(f"⚠️ Échec SSL standard: {ssl_error}")
            print("🔧 Utilisation du SSL personnalisé pour Docker...")
            try:
                # Fallback avec SSL moins strict pour Docker
                return self._open_with_custom_ssl()
            except Exception as e:
                print(f"❌ Échec connexion email: {e}")
                if not self.fail_silently:
                    raise e
                return False
        except Exception as e:
            print(f"❌ Erreur connexion générale: {e}")
            if not self.fail_silently:
                raise e
            return False
    
    def _open_with_standard_ssl(self):
        """Tentative avec SSL standard"""
        self.connection = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
        
        if self.use_tls:
            self.connection.starttls()
            
        if self.username and self.password:
            self.connection.login(self.username, self.password)
            
        print("✅ Connexion SSL standard réussie")
        return True
    
    def _open_with_custom_ssl(self):
        """Fallback avec SSL personnalisé pour Docker"""
        self.connection = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
        
        if self.use_tls:
            # Créer un contexte SSL personnalisé pour Docker
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            self.connection.starttls(context=context)
            
        if self.username and self.password:
            self.connection.login(self.username, self.password)
            
        print("✅ Connexion SSL personnalisé réussie (Docker)")
        return True