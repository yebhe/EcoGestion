<template>
    <div class="dashboard-container">
      <div class="dashboard-card">
        <div class="speedometer">
          <div class="speedometer-dial"></div>
          <div class="speedometer-center"></div>
        </div>
        
        <div class="content-wrapper">
          <h2 class="dashboard-title">Espace Livreur</h2>
          
          <div class="welcome-section" v-if="livreur">
            <h4 class="welcome-text">Bienvenue sur votre espace livreur, {{ user.first_name }}!</h4>
          </div>
          
          <div class="status-section" v-if="livreur">
            <div class="status-badge" :class="userStatusClass">
              {{ userStatusText }}
            </div>
          </div>
          
          <div class="stats-overview">
            <div class="stat-card">
              <span class="stat-icon">🚚</span>
              <div class="stat-content">
                <h3>{{ livraisonsEnCours.length }}</h3>
                <p>Livraisons en cours</p>
              </div>
            </div>
            
            <div class="stat-card">
              <span class="stat-icon">📦</span>
              <div class="stat-content">
                <h3>{{ livraisonsCompletees.length }}</h3>
                <p>Livraisons complétées</p>
              </div>
            </div>
            
            <div class="stat-card">
              <span class="stat-icon">💰</span>
              <div class="stat-content">
                <h3>{{ totalGains }} €</h3>
                <p>Revenus du mois</p>
              </div>
            </div>
          </div>
          
          <div class="button-grid">
            <router-link class="dashboard-btn" to="/livreur/cree-annonce">
              <span class="btn-icon">📋</span>
              <span class="btn-text">Créer une annonce</span>
            </router-link>
            <router-link class="dashboard-btn" to="/livreur/annonces">
              <span class="btn-icon">📋</span>
              <span class="btn-text">Gérer mes annonces</span>
            </router-link>
            
            <router-link class="dashboard-btn" to="/livreur/justificatifs">
              <span class="btn-icon">📄</span>
              <span class="btn-text">Gérer mes pièces justificatives</span>
            </router-link>
            
            <router-link class="dashboard-btn" to="/livreur/livraisons">
              <span class="btn-icon">🚚</span>
              <span class="btn-text">Gérer mes livraisons</span>
            </router-link>
            
            <router-link class="dashboard-btn" to="/livreur/paiements">
              <span class="btn-icon">💸</span>
              <span class="btn-text">Gérer mes paiements</span>
            </router-link>
            
            <router-link class="dashboard-btn" to="/livreur/planning">
              <span class="btn-icon">📅</span>
              <span class="btn-text">Gérer mon planning</span>
            </router-link>
            
            <router-link class="dashboard-btn" to="/update-profile">
              <span class="btn-icon">👤</span>
              <span class="btn-text">Modifier mon profil</span>
            </router-link>

            <router-link class="dashboard-btn" to="/update-password">
              <span class="btn-icon">👤</span>
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
          
          <div class="next-deliveries" v-if="prochaineLivraison">
            <h3 class="section-title">Prochaine livraison</h3>
            <div class="delivery-card">
              <div class="delivery-header">
                <h4>{{ prochaineLivraison.adresse_depart.substring(0, 20) }}... → {{ prochaineLivraison.adresse_arrivee.substring(0, 20) }}...</h4>
                <span class="delivery-date">{{ formatDate(prochaineLivraison.date_livraison_prevue) }}</span>
              </div>
              <div class="delivery-details">
                <p><strong>Client:</strong> {{ prochaineLivraison.client_nom }}</p>
                <p><strong>Montant:</strong> {{ prochaineLivraison.montant }} €</p>
                <router-link :to="`/livreur/livraisons/${prochaineLivraison.id}`" class="details-btn">
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
  const livreur = ref(null);
  const livraisons = ref([]);
  const activitesRecentes = ref([]);
  
  // Récupérer les informations de l'utilisateur
  const fetchUserData = async () => {
    try {
      // Récupérer le profil utilisateur
      const userResponse = await authStore.getUserProfile();
      user.value = userResponse;
      
      // Vérifier que l'utilisateur est bien un livreur
      if (user.value.user_type !== 'livreur') {
        router.push('/access-denied');
        return;
      }
      
      // Récupérer les livraisons
      const livraisonsResponse = await axios.get(`${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/livraisons/`);
      livraisons.value = livraisonsResponse.data;
      
      // Simuler des activités récentes pour la démo
      activitesRecentes.value = [
        { 
          id: 1, 
          type: 'livraison', 
          message: 'Livraison #124 marquée comme livrée', 
          date: new Date(Date.now() - 1000 * 60 * 30) // 30 minutes ago
        },
        { 
          id: 2, 
          type: 'paiement', 
          message: 'Paiement de 53,20€ reçu', 
          date: new Date(Date.now() - 1000 * 60 * 60 * 2) // 2 hours ago
        },
        { 
          id: 3, 
          type: 'annonce', 
          message: 'Nouvelle annonce de trajet créée', 
          date: new Date(Date.now() - 1000 * 60 * 60 * 5) // 5 hours ago
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
  
  // Calculer les livraisons en cours
  const livraisonsEnCours = computed(() => {
    return livraisons.value.filter(l => 
      ['en_attente', 'confirmee', 'en_preparation', 'en_cours'].includes(l.statut)
    );
  });
  
  // Calculer les livraisons complétées
  const livraisonsCompletees = computed(() => {
    return livraisons.value.filter(l => l.statut === 'livree');
  });
  
  // Calculer le total des gains du mois
  const totalGains = computed(() => {
    const now = new Date();
    const moisActuel = now.getMonth();
    const anneeActuelle = now.getFullYear();
    
    return livraisons.value
      .filter(l => {
        const dateLivraison = new Date(l.date_livraison_reelle || l.date_livraison_prevue);
        return l.statut === 'livree' && 
               dateLivraison.getMonth() === moisActuel && 
               dateLivraison.getFullYear() === anneeActuelle;
      })
      .reduce((total, livraison) => total + (parseFloat(livraison.montant) - parseFloat(livraison.commission_plateforme)), 0)
      .toFixed(2);
  });
  
  // Récupérer la prochaine livraison
  const prochaineLivraison = computed(() => {
    const livraisonsAVenir = livraisons.value
      .filter(l => ['en_attente', 'confirmee', 'en_preparation'].includes(l.statut))
      .sort((a, b) => new Date(a.date_livraison_prevue) - new Date(b.date_livraison_prevue));
    
    return livraisonsAVenir.length > 0 ? livraisonsAVenir[0] : null;
  });
  
  // Classe CSS pour le statut de l'utilisateur
  const userStatusClass = computed(() => {
    if (!user.value) return '';
    
    switch (user.value.status) {
      case 'approved':
        return 'status-approved';
      case 'pending':
        return 'status-pending';
      case 'rejected':
        return 'status-rejected';
      default:
        return '';
    }
  });
  
  // Texte pour le statut de l'utilisateur
  const userStatusText = computed(() => {
    if (!user.value) return '';
    
    switch (user.value.status) {
      case 'approved':
        return 'Compte validé';
      case 'pending':
        return 'En attente de validation';
      case 'rejected':
        return 'Compte rejeté';
      default:
        return '';
    }
  });
  
  // Récupérer l'icône pour le type d'activité
  const getActivityIcon = (type) => {
    switch (type) {
      case 'livraison':
        return '🚚';
      case 'paiement':
        return '💰';
      case 'annonce':
        return '📋';
      case 'justificatif':
        return '📄';
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
    background: linear-gradient(135deg, #001F54, #034078);
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
    background: #0A1128;
    border-radius: 50%;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  }
  
  .speedometer-dial {
    position: absolute;
    width: 4px;
    height: 40px;
    background: #1282A2;
    left: 48px;
    bottom: 50px;
    transform-origin: bottom;
    animation: revDial 2s ease-in-out infinite;
  }
  
  .speedometer-center {
    position: absolute;
    width: 20px;
    height: 20px;
    background: #1282A2;
    border-radius: 50%;
    left: 40px;
    bottom: 40px;
  }
  
  .content-wrapper {
    padding-top: 40px;
  }
  
  .dashboard-title {
    color: #0A1128;
    text-align: center;
    margin-bottom: 1.5rem;
    font-size: 2.5rem;
    text-transform: uppercase;
    letter-spacing: 2px;
  }
  
  .welcome-section {
    text-align: center;
    margin-bottom: 1rem;
    color: #034078;
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
    background-color: #4CAF50;
    color: white;
  }
  
  .status-pending {
    background-color: #FF9800;
    color: white;
  }
  
  .status-rejected {
    background-color: #F44336;
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
    color: #034078;
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
    background: #1282A2;
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
    background: #034078;
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
    color: #0A1128;
    border-left: 4px solid #1282A2;
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
  
  .activity-icon-livraison {
    background-color: #E3F2FD;
    color: #1976D2;
  }
  
  .activity-icon-paiement {
    background-color: #E8F5E9;
    color: #388E3C;
  }
  
  .activity-icon-annonce {
    background-color: #FFEBEE;
    color: #D32F2F;
  }
  
  .activity-icon-justificatif {
    background-color: #FFF8E1;
    color: #FFA000;
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
    background: #1282A2;
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
  
  .delivery-date {
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
    background: #034078;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 30px;
    text-decoration: none;
    font-size: 0.9rem;
    transition: all 0.3s ease;
  }
  
  .details-btn:hover {
    background: #1282A2;
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
    
    .delivery-date {
      margin-top: 0.5rem;
    }
  }
  </style>