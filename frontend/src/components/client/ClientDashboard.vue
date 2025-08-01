<template>
  <div class="dashboard-container">
    <div class="dashboard-card">
      <div class="speedometer">
        <div class="speedometer-dial"></div>
        <div class="speedometer-center"></div>
      </div>
      
      <div class="content-wrapper">
        <h2 class="dashboard-title">Espace Client</h2>
        
        <div class="welcome-section" v-if="client">
          <h4 class="welcome-text">Bienvenue sur votre espace client, {{ user.first_name }}!</h4>
        </div>
        
        <div class="status-section" v-if="client">
          <div class="status-badge" :class="userStatusClass">
            {{ userStatusText }}
          </div>
        </div>
        
        <div class="stats-overview">
          <div class="stat-card">
            <span class="stat-icon">📦</span>
            <div class="stat-content">
              <h3>{{ commandesEnCours.length }}</h3>
              <p>Commandes en cours</p>
            </div>
          </div>
          
          <div class="stat-card">
            <span class="stat-icon">✓</span>
            <div class="stat-content">
              <h3>{{ commandesCompletees.length }}</h3>
              <p>Commandes livrées</p>
            </div>
          </div>
          
          <div class="stat-card">
            <span class="stat-icon">💰</span>
            <div class="stat-content">
              <h3>{{ totalDepenses }} €</h3>
              <p>Dépenses du mois</p>
            </div>
          </div>
        </div>
        
        <div class="button-grid">
          
          <router-link class="dashboard-btn" to="/client/suivi">
            <span class="btn-icon">🚚</span>
            <span class="btn-text">Suivi des colis</span>
          </router-link>
          
          <router-link class="dashboard-btn" to="/client/factures">
            <span class="btn-icon">💳</span>
            <span class="btn-text">Gérer mes factures</span>
          </router-link>
          
          <router-link class="dashboard-btn" to="/client/annonces">
            <span class="btn-icon">📢</span>
            <span class="btn-text">Créer une annonce</span>
          </router-link>
          
          <router-link class="dashboard-btn" to="/update-profile">
            <span class="btn-icon">👤</span>
            <span class="btn-text">Modifier mon profil</span>
          </router-link>

          <router-link class="dashboard-btn" to="/update-password">
            <span class="btn-icon">🔒</span>
            <span class="btn-text">Modifier mot de passe</span>
          </router-link>
        </div>
        
        <div class="recent-activity" v-if="activitesRecentes.length > 0">
          <h3 class="section-title">Activités récentes</h3>
          <ul class="activity-list">
            <li v-for="activite in activitesRecentes" :key="activite.id" class="activity-item">
              <div class="activity-icon" :class="getActivityIconClass(activite.type)">
                <span>{{ getActivityIcon(activite.type) }}</span>
              </div>
              <div class="activity-details">
                <p class="activity-message">{{ activite.message }}</p>
                <p class="activity-date">{{ formatDate(activite.date) }}</p>
              </div>
            </li>
          </ul>
        </div>
        
        <div class="next-deliveries" v-if="prochaineCommande">
          <h3 class="section-title">Prochaine livraison attendue</h3>
          <div class="delivery-card">
            <div class="delivery-header">
              <h4>Commande #{{ prochaineCommande.id }} - {{ formatDate(prochaineCommande.date_livraison_prevue) }}</h4>
              <span class="delivery-status">{{ prochaineCommande.statut }}</span>
            </div>
            <div class="delivery-details">
              <p><strong>De:</strong> {{ prochaineCommande.adresse_depart.substring(0, 25) }}...</p>
              <p><strong>À:</strong> {{ prochaineCommande.adresse_arrivee.substring(0, 25) }}...</p>
              <p><strong>Montant:</strong> {{ prochaineCommande.montant }} €</p>
              <router-link :to="`/client/commandes/${prochaineCommande.id}`" class="details-btn">
                Voir les détails
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/authStore';
import axios from 'axios';

const router = useRouter();
const authStore = useAuthStore();
const user = ref(null);
const client = ref(null);
const commandes = ref([]);
const activitesRecentes = ref([]);

// Récupérer les informations de l'utilisateur
const fetchUserData = async () => {
  try {
    // Récupérer le profil utilisateur
    const userResponse = await authStore.getUserProfile();
    user.value = userResponse;
    
    // Vérifier que l'utilisateur est bien un client
    if (user.value.user_type !== 'client') {
      router.push('/access-denied');
      return;
    }
    
    // Récupérer les commandes
    const commandesResponse = await axios.get(`${import.meta.env.VITE_APP_BASE_URL_API}/api/clients/commandes/`);
    commandes.value = commandesResponse.data;
    
    // Simuler des activités récentes pour la démo
    activitesRecentes.value = [
      { 
        id: 1, 
        type: 'commande', 
        message: 'Commande #587 confirmée', 
        date: new Date(Date.now() - 1000 * 60 * 25) // 25 minutes ago
      },
      { 
        id: 2, 
        type: 'paiement', 
        message: 'Paiement de 45,90€ effectué', 
        date: new Date(Date.now() - 1000 * 60 * 60 * 3) // 3 hours ago
      },
      { 
        id: 3, 
        type: 'livraison', 
        message: 'Colis #324 livré à votre adresse', 
        date: new Date(Date.now() - 1000 * 60 * 60 * 8) // 8 hours ago
      }
    ];
  } catch (error) {
    console.error('Erreur lors de la récupération des données:', error);
  }
};

// Formater une date
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('fr-FR', { 
    day: '2-digit', 
    month: '2-digit', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// Calculer les commandes en cours
const commandesEnCours = computed(() => {
  return commandes.value.filter(c => 
    ['en_attente', 'confirmee', 'en_preparation', 'en_cours'].includes(c.statut)
  );
});

// Calculer les commandes complétées
const commandesCompletees = computed(() => {
  return commandes.value.filter(c => c.statut === 'livree');
});

// Calculer le total des dépenses du mois
const totalDepenses = computed(() => {
  const now = new Date();
  const moisActuel = now.getMonth();
  const anneeActuelle = now.getFullYear();
  
  return commandes.value
    .filter(c => {
      const dateCommande = new Date(c.date_commande);
      return dateCommande.getMonth() === moisActuel && 
             dateCommande.getFullYear() === anneeActuelle;
    })
    .reduce((total, commande) => total + parseFloat(commande.montant), 0)
    .toFixed(2);
});

// Récupérer la prochaine commande à être livrée
const prochaineCommande = computed(() => {
  const commandesAVenir = commandes.value
    .filter(c => ['confirmee', 'en_preparation', 'en_cours'].includes(c.statut))
    .sort((a, b) => new Date(a.date_livraison_prevue) - new Date(b.date_livraison_prevue));
  
  return commandesAVenir.length > 0 ? commandesAVenir[0] : null;
});

// Classe CSS pour le statut de l'utilisateur
const userStatusClass = computed(() => {
  if (!user.value) return '';
  
  switch (user.value.status) {
    case 'verified':
      return 'status-approved';
    case 'pending':
      return 'status-pending';
    case 'suspended':
      return 'status-rejected';
    default:
      return '';
  }
});

// Texte pour le statut de l'utilisateur
const userStatusText = computed(() => {
  if (!user.value) return '';
  
  switch (user.value.status) {
    case 'verified':
      return 'Compte vérifié';
    case 'pending':
      return 'Vérification en cours';
    case 'suspended':
      return 'Compte suspendu';
    default:
      return '';
  }
});

// Récupérer l'icône pour le type d'activité
const getActivityIcon = (type) => {
  switch (type) {
    case 'commande':
      return '📦';
    case 'paiement':
      return '💰';
    case 'livraison':
      return '🚚';
    case 'adresse':
      return '📍';
    default:
      return '📌';
  }
};

// Récupérer la classe CSS pour le type d'activité
const getActivityIconClass = (type) => {
  return `activity-icon-${type}`;
};

// Exécuter à l'initialisation du composant
onMounted(() => {
  fetchUserData();
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+Pro:wght@400;600;700&display=swap');

.dashboard-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1A5276, #3498DB);
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Source Serif Pro', serif;
  padding: 20px;
  perspective: 1000px;
}

.dashboard-card {
  background: rgba(254, 252, 251, 0.95);
  border-radius: 20px;
  margin-top: 75px;
  padding: 2rem;
  width: 100%;
  max-width: 900px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  position: relative;
  transform-style: preserve-3d;
  animation: cardEntry 1s ease-out;
}

.speedometer {
  position: absolute;
  top: -50px;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 100px;
  background: #154360;
  border-radius: 50%;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.speedometer-dial {
  position: absolute;
  width: 4px;
  height: 40px;
  background: #5DADE2;
  left: 48px;
  bottom: 50px;
  transform-origin: bottom;
  animation: revDial 2s ease-in-out infinite;
}

.speedometer-center {
  position: absolute;
  width: 20px;
  height: 20px;
  background: #5DADE2;
  border-radius: 50%;
  left: 40px;
  bottom: 40px;
}

.content-wrapper {
  padding-top: 40px;
}

.dashboard-title {
  color: #154360;
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 2.5rem;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.welcome-section {
  text-align: center;
  margin-bottom: 1rem;
  color: #1A5276;
  animation: slideIn 0.5s ease-out;
}

.status-section {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.status-badge {
  padding: 0.5rem 1.5rem;
  border-radius: 50px;
  font-weight: 600;
  font-size: 0.9rem;
  animation: fadeIn 0.5s ease-out;
}

.status-approved {
  background-color: #2ECC71;
  color: white;
}

.status-pending {
  background-color: #F39C12;
  color: white;
}

.status-rejected {
  background-color: #E74C3C;
  color: white;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-icon {
  font-size: 2rem;
  margin-right: 1rem;
}

.stat-content h3 {
  font-size: 1.8rem;
  margin: 0;
  color: #1A5276;
}

.stat-content p {
  margin: 0.3rem 0 0;
  color: #777;
  font-size: 0.9rem;
}

.button-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.dashboard-btn {
  background: #3498DB;
  color: white;
  padding: 1rem;
  border-radius: 15px;
  text-decoration: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  text-align: center;
}

.dashboard-btn:hover {
  background: #2980B9;
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.btn-icon {
  font-size: 1.5rem;
}

.btn-text {
  font-size: 0.9rem;
  font-weight: 500;
}

.section-title {
  margin-top: 0;
  color: #154360;
  border-left: 4px solid #3498DB;
  padding-left: 1rem;
  margin-bottom: 1rem;
}

.activity-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.activity-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #f0f0f0;
  animation: fadeIn 0.5s ease-out;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 1rem;
  font-size: 1.2rem;
}

.activity-icon-commande {
  background-color: #D6EAF8;
  color: #3498DB;
}

.activity-icon-paiement {
  background-color: #D5F5E3;
  color: #2ECC71;
}

.activity-icon-livraison {
  background-color: #FAE5D3;
  color: #E67E22;
}

.activity-icon-adresse {
  background-color: #FADBD8;
  color: #E74C3C;
}

.activity-details {
  flex: 1;
}

.activity-message {
  margin: 0 0 0.3rem;
  font-weight: 500;
}

.activity-date {
  margin: 0;
  font-size: 0.8rem;
  color: #777;
}

.delivery-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  animation: slideIn 0.5s ease-out;
}

.delivery-header {
  background: #3498DB;
  color: white;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.delivery-header h4 {
  margin: 0;
  font-size: 1.1rem;
}

.delivery-status {
  font-size: 0.9rem;
  background: rgba(255, 255, 255, 0.2);
  padding: 0.3rem 0.7rem;
  border-radius: 20px;
}

.delivery-details {
  padding: 1rem;
}

.delivery-details p {
  margin: 0.5rem 0;
}

.details-btn {
  display: inline-block;
  margin-top: 1rem;
  background: #2980B9;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 30px;
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.details-btn:hover {
  background: #3498DB;
  transform: translateY(-2px);
}

@keyframes cardEntry {
  from {
    opacity: 0;
    transform: translateY(30px) rotateX(10deg);
  }
  to {
    opacity: 1;
    transform: translateY(0) rotateX(0);
  }
}

@keyframes revDial {
  0% { transform: rotate(-90deg); }
  50% { transform: rotate(90deg); }
  100% { transform: rotate(-90deg); }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@media (max-width: 768px) {
  .dashboard-card {
    margin-top: 60px;
    padding: 1.5rem;
  }
  
  .dashboard-title {
    font-size: 2rem;
  }
  
  .stats-overview {
    grid-template-columns: 1fr;
  }
  
  .button-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .button-grid {
    grid-template-columns: 1fr;
  }
  
  .delivery-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .delivery-status {
    margin-top: 0.5rem;
  }
}
</style>