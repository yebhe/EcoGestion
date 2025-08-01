<template>
  <div class="annonces-container">
    <div class="header-section">
      <h1 class="page-title">Annonces de Trajets Disponibles</h1>
    </div>

    <!-- Filtres -->
    <div class="filters-section">
      <div class="filter-group">
        <label for="filter-ville-depart">Ville de départ:</label>
        <input 
          type="text" 
          id="filter-ville-depart" 
          v-model="villeDepart" 
          placeholder="Filtrer par ville de départ"
          @input="applyFilters"
        />
      </div>
      
      <div class="filter-group">
        <label for="filter-ville-arrivee">Ville d'arrivée:</label>
        <input 
          type="text" 
          id="filter-ville-arrivee" 
          v-model="villeArrivee" 
          placeholder="Filtrer par ville d'arrivée"
          @input="applyFilters"
        />
      </div>
      
      <div class="filter-group">
        <label for="filter-date">Date minimum:</label>
        <input 
          type="date" 
          id="filter-date" 
          v-model="dateMin"
          @change="applyFilters"
        />
      </div>
      
      <div class="filter-group">
        <label for="filter-order">Trier par:</label>
        <select id="filter-order" v-model="sortBy" @change="applyFilters">
          <option value="date_depart">Date de départ</option>
          <option value="ville_depart">Ville de départ</option>
          <option value="ville_arrivee">Ville d'arrivée</option>
        </select>
      </div>
    </div>

    <!-- Liste des annonces -->
    <div v-if="isLoading" class="loading-indicator">
      <div class="spinner"></div>
      <p>Chargement en cours...</p>
    </div>
    
    <div v-else-if="filteredTrajets.length === 0" class="empty-state">
      <span class="empty-icon">📭</span>
      <p>Aucune annonce de trajet disponible ne correspond à vos critères</p>
      <p class="empty-subtitle">Essayez de modifier vos filtres ou revenez plus tard</p>
    </div>
    
    <div v-else class="trajets-list">
      <div v-for="trajet in filteredTrajets" :key="trajet.id" class="trajet-card trajet-actif">
        <div class="trajet-header">
          <h3>{{ trajet.ville_depart }} → {{ trajet.ville_arrivee }}</h3>
          <div class="trajet-badge badge-actif">
            Disponible
          </div>
        </div>
        
        <div class="trajet-details">
          <div class="detail-group">
            <span class="detail-icon">👤</span>
            <div>
              <p class="detail-label">Livreur</p>
              <p class="detail-value">{{ trajet.livreur_nom }}</p>
            </div>
          </div>
          
          <div v-if="trajet.photo_produit_url" class="trajet-image">
              <img :src="trajet.photo_produit_url" alt="Photo du trajet" class="trajet-thumbnail" />
            </div>

          <div class="detail-group">
            <span class="detail-icon">🗓️</span>
            <div>
              <p class="detail-label">Départ</p>
              <p class="detail-value">{{ formatDate(trajet.date_depart) }}</p>
            </div>
          </div>
          
          <div class="detail-group">
            <span class="detail-icon">🏁</span>
            <div>
              <p class="detail-label">Arrivée</p>
              <p class="detail-value">{{ formatDate(trajet.date_arrivee) }}</p>
            </div>
          </div>
          
          <div class="detail-group">
            <span class="detail-icon">⚖️</span>
            <div>
              <p class="detail-label">Capacité</p>
              <p class="detail-value">{{ trajet.capacite_poids }} kg / {{ trajet.capacite_volume }} m³</p>
            </div>
          </div>
        </div>
        
        <div class="trajet-actions">
          <button @click="viewTrajet(trajet)" class="action-btn view-btn">
            <span class="btn-icon">👁️</span>
            Détails
          </button>
          
          <button 
            @click="selectTrajet(trajet)" 
            class="action-btn select-btn"
            :disabled="trajet.isSelecting"
          >
            <span v-if="trajet.isSelecting" class="mini-spinner"></span>
            <span v-else class="btn-icon">✓</span>
            {{ trajet.isSelecting ? 'Sélection...' : 'Sélectionner' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de détails du trajet -->
    <div v-if="showDetailModal && selectedTrajet" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h3>Détails du trajet</h3>
          <button @click="showDetailModal = false" class="close-btn">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="trajet-full-details">
            <div class="detail-section">
              <h4>Itinéraire</h4>
              <div class="detail-item">
                <span class="detail-label">Départ:</span>
                <span>{{ selectedTrajet.adresse_depart }}, {{ selectedTrajet.code_postal_depart }} {{ selectedTrajet.ville_depart }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Arrivée:</span>
                <span>{{ selectedTrajet.adresse_arrivee }}, {{ selectedTrajet.code_postal_arrivee }} {{ selectedTrajet.ville_arrivee }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Date de départ:</span>
                <span>{{ formatDate(selectedTrajet.date_depart) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Date d'arrivée:</span>
                <span>{{ formatDate(selectedTrajet.date_arrivee) }}</span>
              </div>
            </div>
            
            <div class="detail-section">
              <h4>Livreur</h4>
              <div class="detail-item">
                <span class="detail-label">Nom:</span>
                <span>{{ selectedTrajet.livreur_nom }}</span>
              </div>
            </div>
            
            <div class="detail-section">
              <h4>Capacité</h4>
              <div class="detail-item">
                <span class="detail-label">Poids disponible:</span>
                <span>{{ selectedTrajet.capacite_poids }} kg</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Volume disponible:</span>
                <span>{{ selectedTrajet.capacite_volume }} m³</span>
              </div>
            </div>
            <div v-if="selectedTrajet.photo_produit_url" class="trajet-image">
              <img :src="selectedTrajet.photo_produit_url" alt="Photo du trajet" class="trajet-thumbnail" />
            </div>
            
            <div class="detail-section" v-if="selectedTrajet.commentaire">
              <h4>Commentaire du livreur</h4>
              <p class="trajet-commentaire">{{ selectedTrajet.commentaire }}</p>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="showDetailModal = false" class="cancel-action-btn">Fermer</button>
          <button 
            @click="selectTrajet(selectedTrajet); showDetailModal = false;" 
            class="confirm-action-btn"
            :disabled="selectedTrajet.isSelecting"
          >
            <span v-if="selectedTrajet.isSelecting" class="mini-spinner"></span>
            <span v-else>Sélectionner ce trajet</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Message de succès -->
    <div v-if="successMessage" class="success-toast">
      <div class="toast-content">
        <span class="toast-icon">✅</span>
        <span>{{ successMessage }}</span>
        <button @click="successMessage = ''" class="toast-close">&times;</button>
      </div>
    </div>

    <!-- Message d'erreur -->
    <div v-if="errorMessage" class="error-toast">
      <div class="toast-content">
        <span class="toast-icon">❌</span>
        <span>{{ errorMessage }}</span>
        <button @click="errorMessage = ''" class="toast-close">&times;</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const trajets = ref([]);
const isLoading = ref(true);
const showDetailModal = ref(false);
const selectedTrajet = ref(null);
const successMessage = ref('');
const errorMessage = ref('');

// Filtres
const villeDepart = ref('');
const villeArrivee = ref('');
const dateMin = ref('');
const sortBy = ref('date_depart');

// Récupérer les trajets disponibles
const fetchTrajets = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/trajets/`);
    // Ajouter une propriété pour gérer l'état de sélection
    console.log('les trajets', response.data);
    trajets.value = response.data.map(trajet => ({
      ...trajet,
      isSelecting: false
    }));
  } catch (error) {
    console.error('Erreur lors de la récupération des trajets:', error);
    errorMessage.value = 'Erreur lors du chargement des trajets';
  } finally {
    isLoading.value = false;
  }
};

// Formater une date
const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// Appliquer les filtres
const applyFilters = () => {
  // Cette fonction est appelée quand les filtres changent
  // Elle met à jour filteredTrajets via le computed
};

// Computed pour les trajets filtrés
const filteredTrajets = computed(() => {
  let filtered = [...trajets.value];
  
  // Filtrer par ville de départ
  if (villeDepart.value) {
    filtered = filtered.filter(t => 
      t.ville_depart.toLowerCase().includes(villeDepart.value.toLowerCase())
    );
  }
  
  // Filtrer par ville d'arrivée
  if (villeArrivee.value) {
    filtered = filtered.filter(t => 
      t.ville_arrivee.toLowerCase().includes(villeArrivee.value.toLowerCase())
    );
  }
  
  // Filtrer par date minimum
  if (dateMin.value) {
    const minDate = new Date(dateMin.value);
    filtered = filtered.filter(t => {
      const departDate = new Date(t.date_depart);
      return departDate >= minDate;
    });
  }
  
  // Filtrer pour ne garder que les trajets actifs
  filtered = filtered.filter(t => t.statut === 'actif');
  
  // Trier
  filtered.sort((a, b) => {
    if (sortBy.value === 'ville_depart') {
      return a.ville_depart.localeCompare(b.ville_depart);
    } else if (sortBy.value === 'ville_arrivee') {
      return a.ville_arrivee.localeCompare(b.ville_arrivee);
    } else {
      // date_depart par défaut
      return new Date(a.date_depart) - new Date(b.date_depart);
    }
  });
  
  return filtered;
});

// Voir les détails d'un trajet
const viewTrajet = (trajet) => {
  selectedTrajet.value = trajet;
  showDetailModal.value = true;
};

// Sélectionner un trajet (version simplifiée)
const selectTrajet = async (trajet) => {
  // Marquer le trajet comme en cours de sélection
  trajet.isSelecting = true;
  errorMessage.value = '';
  successMessage.value = '';
  
  try {
    const csrfToken = document.cookie.match(/csrftoken=([^;]+)/)?.[1];
    
    // Appeler l'endpoint pour sélectionner le trajet
    const response = await axios.post(
      `${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/trajets/${trajet.id}/update_status/`,
      {},
      {
        headers: {
          "X-CSRFToken": csrfToken,
        },
        withCredentials: true,
      }
    );
    
    // Afficher le message de succès
    successMessage.value = response.data.status || 'Trajet sélectionné avec succès!';
    
    // Mettre à jour le statut du trajet localement
    trajet.statut = 'selected';
    
    // Optionnel: rediriger vers une page de détails ou actualiser la liste
    // router.push('/livreur/livraisons');
    
    // Actualiser la liste des trajets après 2 secondes
    setTimeout(() => {
      fetchTrajets();
    }, 2000);
    
  } catch (error) {
    console.error('Erreur lors de la sélection du trajet:', error);
    errorMessage.value = error.response?.data?.error || 'Erreur lors de la sélection du trajet';
  } finally {
    trajet.isSelecting = false;
    
    // Fermer le modal s'il est ouvert
    if (showDetailModal.value) {
      showDetailModal.value = false;
    }
  }
};

// Auto-hide messages after 5 seconds
const autoHideMessages = () => {
  if (successMessage.value) {
    setTimeout(() => {
      successMessage.value = '';
    }, 5000);
  }
  if (errorMessage.value) {
    setTimeout(() => {
      errorMessage.value = '';
    }, 5000);
  }
};

// Watch for message changes to auto-hide
const watchMessages = () => {
  if (successMessage.value || errorMessage.value) {
    autoHideMessages();
  }
};

// Exécuter à l'initialisation du composant
onMounted(() => {
  fetchTrajets();
});
</script>

<style scoped>
.annonces-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header-section {
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  color: #0A1128;
  margin: 0;
}

.filters-section {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 2rem;
  background-color: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 200px;
}

.filter-group label {
  font-weight: 500;
  color: #374151;
}

.filter-group input, .filter-group select {
  padding: 0.5rem;
  border: 1px solid #D1D5DB;
  border-radius: 6px;
  background-color: #F9FAFB;
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #0e7490;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
}

.empty-state p {
  font-size: 1.1rem;
  color: #6B7280;
  margin-bottom: 0.5rem;
}

.empty-subtitle {
  font-size: 0.9rem;
  color: #9CA3AF;
}

.trajets-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.trajet-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.trajet-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.trajet-actif {
  border-left: 4px solid #22c55e;
}

.trajet-header {
  background-color: #F9FAFB;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #E5E7EB;
}.trajet-image {
  margin-top: 10px;
  text-align: center;
}

.trajet-thumbnail {
  max-height: 200px;
  max-width: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.trajet-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #1F2937;
}

.trajet-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 600;
}

.badge-actif {
  background-color: #dcfce7;
  color: #166534;
}

.trajet-details {
  padding: 1rem;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.detail-group {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.detail-icon {
  font-size: 1.2rem;
}

.detail-label {
  font-size: 0.75rem;
  color: #6B7280;
  margin: 0;
}

.detail-value {
  font-size: 0.9rem;
  font-weight: 500;
  color: #374151;
  margin: 0;
}

.trajet-actions {
  padding: 1rem;
  display: flex;
  gap: 0.5rem;
  border-top: 1px solid #E5E7EB;
  background-color: #F9FAFB;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-btn {
  background-color: #f3f4f6;
  color: #1F2937;
}

.view-btn:hover {
  background-color: #e5e7eb;
}

.select-btn {
  background-color: #0e7490;
  color: white;
  margin-left: auto;
}

.select-btn:hover:not(:disabled) {
  background-color: #155e75;
}

.select-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-container {
  background-color: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.modal-header {
  padding: 1.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #E5E7EB;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #111827;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6B7280;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1.25rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  border-top: 1px solid #E5E7EB;
}

.cancel-action-btn {
  padding: 0.625rem 1.25rem;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  background-color: white;
  color: #4B5563;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-action-btn:hover {
  background-color: #F3F4F6;
}

.confirm-action-btn {
  padding: 0.625rem 1.25rem;
  border: none;
  border-radius: 8px;
  background-color: #0e7490;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.confirm-action-btn:hover:not(:disabled) {
  background-color: #155e75;
}

.confirm-action-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.trajet-full-details {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.detail-section {
  border-bottom: 1px solid #E5E7EB;
  padding-bottom: 1.25rem;
}

.detail-section:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.detail-section h4 {
  font-size: 1.1rem;
  color: #1F2937;
  margin: 0 0 1rem 0;
}

.detail-item {
  display: flex;
  margin-bottom: 0.75rem;
}

.detail-item:last-child {
  margin-bottom: 0;
}

.detail-item .detail-label {
  font-size: 0.95rem;
  font-weight: 500;
  color: #4B5563;
  width: 35%;
}

.trajet-commentaire {
  background-color: #F9FAFB;
  padding: 1rem;
  border-radius: 8px;
  font-size: 0.95rem;
  color: #4B5563;
  margin: 0;
}

.mini-spinner {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-left-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Toast notifications */
.success-toast, .error-toast {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 2000;
  max-width: 400px;
  border-radius: 8px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  animation: slideIn 0.3s ease-out;
}

.success-toast {
  background-color: #dcfce7;
  border: 1px solid #bbf7d0;
  color: #166534;
}

.error-toast {
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  color: #b91c1c;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
}

.toast-icon {
  font-size: 1.25rem;
}

.toast-close {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  margin-left: auto;
  color: inherit;
  opacity: 0.7;
}

.toast-close:hover {
  opacity: 1;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .annonces-container {
    padding: 1rem;
  }
  
  .trajet-details {
    grid-template-columns: 1fr;
  }
  
  .success-toast, .error-toast {
    right: 10px;
    left: 10px;
    max-width: none;
  }
}
</style>