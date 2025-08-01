<template>
  <div class="livraisons-container">

    <!-- Statistiques -->
    <div class="stats-overview">
      <div class="stat-card">
        <span class="stat-icon">⏳</span>
        <div class="stat-content">
          <h3>{{ livraisonsEnAttente.length }}</h3>
          <p>En attente</p>
        </div>
      </div>
      
      <div class="stat-card">
        <span class="stat-icon">🚚</span>
        <div class="stat-content">
          <h3>{{ livraisonsEnCours.length }}</h3>
          <p>En cours</p>
        </div>
      </div>
      
      <div class="stat-card">
        <span class="stat-icon">✅</span>
        <div class="stat-content">
          <h3>{{ livraisonsLivrees.length }}</h3>
          <p>Livrées</p>
        </div>
      </div>
      
      <div class="stat-card">
        <span class="stat-icon">❌</span>
        <div class="stat-content">
          <h3>{{ livraisonsAnnulees.length }}</h3>
          <p>Annulées</p>
        </div>
      </div>
    </div>

    <!-- Filtres -->
    <div class="filters-section">
      <div class="filter-group">
        <label for="filter-status">Statut:</label>
        <select id="filter-status" v-model="statusFilter">
          <option value="all">Tous</option>
          <option value="en_attente">En attente</option>
          <option value="confirmee">Confirmée</option>
          <option value="en_preparation">En préparation</option>
          <option value="en_cours">En cours</option>
          <option value="livree">Livrée</option>
          <option value="annulee">Annulée</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label for="filter-date">Trier par:</label>
        <select id="filter-date" v-model="sortBy">
          <option value="date_livraison_prevue">Date prévue</option>
          <option value="date_demande">Date de demande</option>
          <option value="montant">Montant</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label for="filter-order">Ordre:</label>
        <select id="filter-order" v-model="orderDirection">
          <option value="asc">Croissant</option>
          <option value="desc">Décroissant</option>
        </select>
      </div>
    </div>

    <!-- Liste des livraisons -->
    <div v-if="isLoading" class="loading-indicator">
      <div class="spinner"></div>
      <p>Chargement en cours...</p>
    </div>
    
    <div v-else-if="filteredLivraisons.length === 0" class="empty-state">
      <span class="empty-icon">📦</span>
      <p>Aucune livraison ne correspond à vos critères</p>
      <button @click="navigateToAnnoncesDisponibles" class="add-btn-secondary">
        Choisir une annonce disponible
      </button>
    </div>
    
    <div v-else class="livraisons-grid">
      <div v-for="livraison in filteredLivraisons" :key="livraison.id" class="livraison-card" :class="{'annonce-selectionnee': hasTrajetAnnonce(livraison)}">
        <div class="livraison-header" :class="'status-' + livraison.statut">
          <h3>Livraison #{{ livraison.id }}</h3>
          <div class="livraison-badge" :class="'badge-' + livraison.statut">
            {{ getStatusLabel(livraison.statut) }}
          </div>
        </div>
        
        <div v-if="hasTrajetAnnonce(livraison)" class="annonce-badge">
          <span class="badge-icon">📋</span> Annonce sélectionnée
        </div>
        
        <div class="livraison-details">
          <div class="detail-item">
            <span class="detail-label">Client:</span>
            <span class="detail-value">{{ livraison.client_nom }}</span>
          </div>
          
          <div class="detail-item">
            <span class="detail-label">Date prévue:</span>
            <span class="detail-value">{{ formatDate(livraison.trajet_annonce.date_arrivee) }}</span>
          </div>
          
          <div class="detail-item">
            <span class="detail-label">Adresse départ:</span>
            <span class="detail-value">{{ formatAddress(livraison.trajet_annonce.adresse_depart) }}</span>
          </div>
          
          <div class="detail-item">
            <span class="detail-label">Adresse arrivée:</span>
            <span class="detail-value">{{ formatAddress(livraison.trajet_annonce.adresse_arrivee) }}</span>
          </div>
          
          <div class="detail-item">
            <span class="detail-label">Montant:</span>
            <span class="detail-value">{{ formatMontant(livraison.trajet_annonce.montant) }}</span>
          </div>
          
          <div class="detail-item">
            <span class="detail-label">Commission:</span>
            <span class="detail-value">{{ formatMontant(livraison.trajet_annonce.commission_plateforme) }}</span>
          </div>
          
          <div v-if="livraison.trajet_annonce.photo_produit_url" class="trajet-image">
              <img :src="livraison.trajet_annonce.photo_produit_url" alt="Photo du trajet" class="trajet-thumbnail" />
            </div>

          <div v-if="livraison.poids || livraison.volume" class="detail-item">
            <span class="detail-label">Dimensions:</span>
            <span class="detail-value">
              {{ livraison.poids ? livraison.poids + ' kg' : '' }}
              {{ livraison.poids && livraison.volume ? ' / ' : '' }}
              {{ livraison.volume ? livraison.volume + ' m³' : '' }}
            </span>
          </div>
        </div>
        
        <div v-if="livraison.commentaire_client" class="livraison-comment">
          <h4>Commentaire client:</h4>
          <p>{{ livraison.commentaire_client }}</p>
        </div>
        
        <div v-if="livraison.commentaire_livreur" class="livraison-comment livreur-comment">
          <h4>Votre commentaire:</h4>
          <p>{{ livraison.commentaire_livreur }}</p>
        </div>
        
        <div class="livraison-actions">
          <button @click="viewLivraison(livraison)" class="action-btn view-btn">
            <span class="btn-icon">👁️</span>
            Détails
          </button>
          
          <button v-if="canUpdateStatus(livraison)" @click="openUpdateStatusModal(livraison)" class="action-btn update-btn">
            <span class="btn-icon">🔄</span>
            Mettre à jour
          </button>
          
          <button v-if="canAddComment(livraison)" @click="openCommentModal(livraison)" class="action-btn comment-btn">
            <span class="btn-icon">💬</span>
            Commenter
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de détails -->
    <div v-if="showDetailModal && selectedLivraison" class="modal-overlay">
      <div class="modal-container modal-large">
        <div class="modal-header">
          <h3>Détails de la livraison #{{ selectedLivraison.id }}</h3>
          <button @click="showDetailModal = false" class="close-btn">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="livraison-status">
            <div class="livraison-badge large-badge" :class="'badge-' + selectedLivraison.statut">
              {{ getStatusLabel(selectedLivraison.statut) }}
            </div>
          </div>
          
          <div class="detail-section">
            <h4>Informations générales</h4>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">Client:</span>
                <span class="detail-value">{{ selectedLivraison.client_nom }}</span>
              </div>
              
              <div class="detail-item">
                <span class="detail-label">Date de demande:</span>
                <span class="detail-value">{{ formatDate(selectedLivraison.dtrajet_annonce.date_demande) }}</span>
              </div>
              
              <div class="detail-item">
                <span class="detail-label">Date prévue:</span>
                <span class="detail-value">{{ formatDate(selectedLivraison.trajet_annonce.date_livraison_prevue) }}</span>
              </div>
              
              <div class="detail-item" v-if="selectedLivraison.date_livraison_reelle">
                <span class="detail-label">Date de livraison réelle:</span>
                <span class="detail-value">{{ formatDate(selectedLivraison.trajet_annonce.date_livraison_reelle) }}</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h4>Itinéraire</h4>
            <div class="detail-grid">
              <div class="detail-item full-width">
                <span class="detail-label">Adresse de départ:</span>
                <span class="detail-value">{{ selectedLivraison.trajet_annonce.adresse_depart }}</span>
              </div>
              
              <div class="detail-item full-width">
                <span class="detail-label">Adresse d'arrivée:</span>
                <span class="detail-value">{{ selectedLivraison.trajet_annonce.adresse_arrivee }}</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h4>Informations financières</h4>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">Montant total:</span>
                <span class="detail-value">{{ formatMontant(selectedLivraison.trajet_annonce.montant) }}</span>
              </div>
              
              <div class="detail-item">
                <span class="detail-label">Commission plateforme:</span>
                <span class="detail-value">{{ formatMontant(selectedLivraison.trajet_annonce.commission_plateforme) }}</span>
              </div>
              
              <div class="detail-item">
                <span class="detail-label">Montant net:</span>
                <span class="detail-value highlight">{{ formatMontant(selectedLivraison.trajet_annonce.montant - selectedLivraison.trajet_annonce.commission_plateforme) }}</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section" v-if="selectedLivraison.poids || selectedLivraison.volume">
            <h4>Caractéristiques</h4>
            <div class="detail-grid">
              <div class="detail-item" v-if="selectedLivraison.poids">
                <span class="detail-label">Poids:</span>
                <span class="detail-value">{{ selectedLivraison.poids }} kg</span>
              </div>
              
              <div class="detail-item" v-if="selectedLivraison.volume">
                <span class="detail-label">Volume:</span>
                <span class="detail-value">{{ selectedLivraison.volume }} m³</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section" v-if="selectedLivraison.commentaire_client">
            <h4>Commentaire du client</h4>
            <div class="comment-box client-comment">
              <p>{{ selectedLivraison.commentaire_client }}</p>
            </div>
          </div>
          
          <div class="detail-section" v-if="selectedLivraison.commentaire_livreur">
            <h4>Votre commentaire</h4>
            <div class="comment-box livreur-comment">
              <p>{{ selectedLivraison.commentaire_livreur }}</p>
            </div>
          </div>
          
          <div class="detail-section" 
               v-if="hasTrajetAnnonce(selectedLivraison)">
            <h4>Trajet associé</h4>
            <div class="trajet-box">
              <p><strong>De:</strong> {{ selectedLivraison.trajet_annonce.ville_depart }}</p>
              <p><strong>À:</strong> {{ selectedLivraison.trajet_annonce.ville_arrivee }}</p>
              <p><strong>Date départ:</strong> {{ formatDate(selectedLivraison.trajet_annonce.date_depart) }}</p>
              <router-link :to="`/livreur/trajets/${selectedLivraison.trajet_annonce.id}`" class="trajet-link">
                Voir le trajet
              </router-link>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="showDetailModal = false" class="cancel-action-btn">Fermer</button>
          <div class="action-buttons">
            <button v-if="canUpdateStatus(selectedLivraison)" @click="openUpdateStatusModal(selectedLivraison); showDetailModal = false;" class="update-action-btn">
              <span class="btn-icon">🔄</span>
              Mettre à jour le statut
            </button>
            <button v-if="canAddComment(selectedLivraison)" @click="openCommentModal(selectedLivraison); showDetailModal = false;" class="comment-action-btn">
              <span class="btn-icon">💬</span>
              Ajouter un commentaire
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de mise à jour du statut -->
    <div v-if="showStatusModal && selectedLivraison" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h3>Mettre à jour le statut</h3>
          <button @click="showStatusModal = false" class="close-btn">&times;</button>
        </div>
        
        <div class="modal-body">
          <p>Livraison #{{ selectedLivraison.id }} - {{ formatDate(selectedLivraison.date_livraison_prevue) }}</p>
          <p>Statut actuel: <span class="status-label" :class="'text-' + selectedLivraison.statut">{{ getStatusLabel(selectedLivraison.statut) }}</span></p>
          
          <div class="form-group">
            <label for="new-status">Nouveau statut:</label>
            <select id="new-status" v-model="newStatus" class="status-select">
              <option v-for="status in getNextPossibleStatuses(selectedLivraison)" :key="status" :value="status">
                {{ getStatusLabel(status) }}
              </option>
            </select>
          </div>
          
          <div class="status-description" v-if="newStatus">
            <p>{{ getStatusDescription(newStatus) }}</p>
          </div>
          
          <div class="form-error" v-if="statusUpdateError">{{ statusUpdateError }}</div>
        </div>
        
        <div class="modal-footer">
          <button @click="showStatusModal = false" class="cancel-action-btn">Annuler</button>
          <button @click="updateStatus" class="confirm-action-btn" :disabled="!newStatus || statusUpdateInProgress">
            <span v-if="statusUpdateInProgress" class="mini-spinner"></span>
            <span v-else>Confirmer</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Modal d'ajout de commentaire -->
    <div v-if="showCommentModal && selectedLivraison" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h3>Ajouter un commentaire</h3>
          <button @click="showCommentModal = false" class="close-btn">&times;</button>
        </div>
        
        <div class="modal-body">
          <p>Livraison #{{ selectedLivraison.id }} - {{ formatDate(selectedLivraison.date_livraison_prevue) }}</p>
          
          <div class="form-group">
            <label for="commentaire">Votre commentaire:</label>
            <textarea 
              id="commentaire" 
              v-model="commentaireText" 
              rows="5" 
              placeholder="Ajoutez ici des informations utiles pour le client ou l'administrateur..."></textarea>
          </div>
          
          <div class="form-error" v-if="commentError">{{ commentError }}</div>
        </div>
        
        <div class="modal-footer">
          <button @click="showCommentModal = false" class="cancel-action-btn">Annuler</button>
          <button @click="addComment" class="confirm-action-btn" :disabled="!commentaireText.trim() || commentInProgress">
            <span v-if="commentInProgress" class="mini-spinner"></span>
            <span v-else>Enregistrer</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { toast } from 'vue3-toastify';

const router = useRouter();
const livraisons = ref([]);
const isLoading = ref(true);
const showDetailModal = ref(false);
const showStatusModal = ref(false);
const showCommentModal = ref(false);
const selectedLivraison = ref(null);
const newStatus = ref('');
const commentaireText = ref('');
const statusUpdateError = ref('');
const commentError = ref('');
const statusUpdateInProgress = ref(false);
const commentInProgress = ref(false);

// Filtres
const statusFilter = ref('all');
const sortBy = ref('date_livraison_prevue');
const orderDirection = ref('desc');

// Récupérer les livraisons
const fetchLivraisons = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/livraisons/`);
    livraisons.value = response.data;
    console.log('les livraisons', livraisons.value);
  } catch (error) {
    console.error('Erreur lors de la récupération des livraisons:', error);
    toast("Erreur lors du chargement des livraisons", {
      type: "error",
      autoClose: 3000,
    });
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

// Formater une adresse (afficher seulement le début pour la liste)
const formatAddress = (address) => {
  if (!address) return 'N/A';
  return address.length > 30 ? address.substring(0, 30) + '...' : address;
};

// Formater un montant
const formatMontant = (montant) => {
  if (montant === undefined || montant === null) return 'N/A';
  return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(montant);
};

// Vérifier si une livraison a un trajet annonce associé
const hasTrajetAnnonce = (livraison) => {
  return livraison && 
         livraison.trajet_annonce && 
         livraison.trajet_annonce.id && 
         livraison.trajet_annonce.ville_depart && 
         livraison.trajet_annonce.ville_arrivee;
};

// Traduction des statuts
const getStatusLabel = (status) => {
  const labels = {
    'en_attente': 'En attente',
    'confirmee': 'Confirmée',
    'en_preparation': 'En préparation',
    'en_cours': 'En cours',
    'livree': 'Livrée',
    'annulee': 'Annulée'
  };
  return labels[status] || status;
};

// Description des statuts
const getStatusDescription = (status) => {
  const descriptions = {
    'confirmee': 'Vous confirmez avoir pris connaissance de cette livraison et vous engagez à l\'effectuer.',
    'en_preparation': 'Vous êtes en train de préparer cette livraison (chargement, etc.).',
    'en_cours': 'Vous avez pris en charge la livraison et êtes en route.',
    'livree': 'La livraison a été effectuée avec succès.',
    'annulee': 'La livraison est annulée et ne sera pas effectuée.'
  };
  return descriptions[status] || '';
};

// Détermine les prochains statuts possibles selon le statut actuel
const getNextPossibleStatuses = (livraison) => {
  const transitions = {
    'en_attente': ['confirmee', 'annulee'],
    'confirmee': ['en_preparation', 'annulee'],
    'en_preparation': ['en_cours', 'annulee'],
    'en_cours': ['livree', 'annulee'],
    'livree': [],
    'annulee': []
  };
  
  return transitions[livraison.statut] || [];
};

// Vérifie si le statut peut être mis à jour
const canUpdateStatus = (livraison) => {
  return getNextPossibleStatuses(livraison).length > 0;
};

// Vérifie si un commentaire peut être ajouté
const canAddComment = (livraison) => {
  return livraison.statut !== 'annulee';
};

// Computed pour les livraisons filtrées
const filteredLivraisons = computed(() => {
  let filtered = [...livraisons.value];

  // ✅ Filtrer uniquement les livraisons avec un trajet sélectionné
  filtered = filtered.filter(l => l.trajet_annonce && l.trajet_annonce.statut === 'selected');

  // ✅ Filtrer par statut (s'il est défini dans le filtre)
  if (statusFilter.value !== 'all') {
    filtered = filtered.filter(l => l.statut === statusFilter.value);
  }

  // ✅ Trier selon le champ choisi
  const sortProperty = sortBy.value;

  filtered.sort((a, b) => {
    let valueA, valueB;

    if (sortProperty === 'montant') {
      valueA = parseFloat(a[sortProperty]);
      valueB = parseFloat(b[sortProperty]);
    } else {
      valueA = new Date(a[sortProperty]);
      valueB = new Date(b[sortProperty]);
    }

    return orderDirection.value === 'asc'
      ? valueA - valueB
      : valueB - valueA;
  });

  return filtered;
});
;

// Computed pour les statistiques
const livraisonsEnAttente = computed(() => {
  return livraisons.value.filter(l => l.statut === 'en_attente');
});

const livraisonsEnCours = computed(() => {
  return livraisons.value.filter(l => 
    ['confirmee', 'en_preparation', 'en_cours'].includes(l.statut)
  );
});

const livraisonsLivrees = computed(() => {
  return livraisons.value.filter(l => l.statut === 'livree');
});

const livraisonsAnnulees = computed(() => {
  return livraisons.value.filter(l => l.statut === 'annulee');
});

// Navigation vers les annonces disponibles
const navigateToAnnoncesDisponibles = () => {
  router.push('/annonces-disponibles');
};

// Voir les détails d'une livraison
const viewLivraison = (livraison) => {
  selectedLivraison.value = livraison;
  showDetailModal.value = true;
};

// Ouvrir le modal de mise à jour du statut
const openUpdateStatusModal = (livraison) => {
  selectedLivraison.value = livraison;
  newStatus.value = '';
  statusUpdateError.value = '';
  showStatusModal.value = true;
};

// Mettre à jour le statut
const updateStatus = async () => {
  if (!newStatus.value || !selectedLivraison.value) return;
  
  statusUpdateInProgress.value = true;
  statusUpdateError.value = '';
  
  try {
    const response = await axios.post(
      `${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/livraisons/${selectedLivraison.value.id}/update_status/`,
      { statut: newStatus.value }
    );
    
    // Mettre à jour la livraison dans la liste
    const index = livraisons.value.findIndex(l => l.id === selectedLivraison.value.id);
    if (index !== -1) {
      // Si le statut est 'livree', ajouter la date de livraison réelle
      if (newStatus.value === 'livree') {
        livraisons.value[index].date_livraison_reelle = new Date().toISOString();
      }
      
      livraisons.value[index].statut = newStatus.value;
    }
    
    showStatusModal.value = false;
    toast(`Statut mis à jour: ${getStatusLabel(newStatus.value)}`, {
      type: "success",
      autoClose: 3000,
    });
  } catch (error) {
    console.error('Erreur lors de la mise à jour du statut:', error);
    statusUpdateError.value = error.response?.data?.error || 'Une erreur est survenue lors de la mise à jour du statut';
  } finally {
    statusUpdateInProgress.value = false;
  }
};

// Ouvrir le modal d'ajout de commentaire
const openCommentModal = (livraison) => {
  selectedLivraison.value = livraison;
  commentaireText.value = livraison.commentaire_livreur || '';
  commentError.value = '';
  showCommentModal.value = true;
};

// Ajouter un commentaire
const addComment = async () => {
  if (!commentaireText.value.trim() || !selectedLivraison.value) return;
  
  commentInProgress.value = true;
  commentError.value = '';
  
  try {
    const response = await axios.post(
      `${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/livraisons/${selectedLivraison.value.id}/ajouter_commentaire/`,
      { commentaire: commentaireText.value.trim() }
    );
    
    // Mettre à jour la livraison dans la liste
    const index = livraisons.value.findIndex(l => l.id === selectedLivraison.value.id);
    if (index !== -1) {
      livraisons.value[index].commentaire_livreur = commentaireText.value.trim();
    }
    
    showCommentModal.value = false;
    toast('Commentaire ajouté avec succès', {
      type: "success",
      autoClose: 3000,
    });
  } catch (error) {
    console.error('Erreur lors de l\'ajout du commentaire:', error);
    commentError.value = error.response?.data?.error || 'Une erreur est survenue lors de l\'ajout du commentaire';
  } finally {
    commentInProgress.value = false;
  }
};

// Exécuter à l'initialisation du composant
onMounted(() => {
  fetchLivraisons();
});
</script>

<style scoped>
.livraisons-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  color: #0A1128;
  margin: 0;
}
.trajet-image {
  margin-top: 10px;
  text-align: center;
}

.trajet-thumbnail {
  max-height: 200px;
  max-width: 100%;
  object-fit: cover;
  border-radius: 8px;
}
.add-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #0e7490;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-btn:hover {
  background-color: #155e75;
}

.btn-icon {
  font-size: 1.2rem;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 2.5rem;
  margin-right: 1.5rem;
}

.stat-content h3 {
  font-size: 2rem;
  margin: 0;
  color: #0A1128;
}

.stat-content p {
  margin: 0.3rem 0 0;
  color: #6B7280;
  font-size: 1rem;
}

.filters-section {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
  background-color: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 500;
  color: #374151;
}

.filter-group select {
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
  height:40px;
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
  margin-bottom: 1.5rem;
}

.add-btn-secondary {
  background-color: #0e7490;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-btn-secondary:hover {
  background-color: #155e75;
  transform: translateY(-2px);
}

.livraisons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.livraison-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
}

.livraison-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.annonce-selectionnee {
  border-left: 4px solid #3b82f6;
}

.annonce-badge {
  position: absolute;
  top: 50px;
  right: 0;
  background-color: #bfdbfe;
  color: #1e40af;
  padding: 0.25rem 0.75rem;
  font-size: 0.8rem;
  font-weight: 600;
  border-top-left-radius: 8px;
  border-bottom-left-radius: 8px;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.badge-icon {
  font-size: 1rem;
}

.livraison-header {
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #E5E7EB;
}

.status-en_attente {
  background-color: #fef9c3;
}

.status-confirmee, .status-en_preparation {
  background-color: #e0f2fe;
}

.status-en_cours {
  background-color: #dbeafe;
}

.status-livree {
  background-color: #dcfce7;
}

.status-annulee {
  background-color: #fee2e2;
}

.livraison-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #1F2937;
}

.livraison-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 600;
}

.large-badge {
  padding: 0.5rem 1rem;
  font-size: 1rem;
}

.badge-en_attente {
  background-color: #fef9c3;
  color: #854d0e;
}

.badge-confirmee {
  background-color: #e0f2fe;
  color: #0c4a6e;
}

.badge-en_preparation {
  background-color: #f0fdf4;
  color: #166534;
}

.badge-en_cours {
  background-color: #dbeafe;
  color: #1e40af;
}

.badge-livree {
  background-color: #dcfce7;
  color: #166534;
}

.badge-annulee {
  background-color: #fee2e2;
  color: #b91c1c;
}

.text-en_attente {
  color: #854d0e;
}

.text-confirmee {
  color: #0c4a6e;
}

.text-en_preparation {
  color: #166534;
}

.text-en_cours {
  color: #1e40af;
}

.text-livree {
  color: #166534;
}

.text-annulee {
  color: #b91c1c;
}

.livraison-details {
  padding: 1.25rem;
}

.detail-item {
  display: flex;
  margin-bottom: 0.75rem;
}

.detail-item:last-child {
  margin-bottom: 0;
}

.detail-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #4B5563;
  width: 35%;
}

.detail-value {
  font-size: 0.9rem;
  color: #1F2937;
  flex: 1;
}

.highlight {
  font-weight: 600;
  color: #0e7490;
}

.livraison-comment {
  padding: 1rem;
  background-color: #f9fafb;
  border-top: 1px solid #E5E7EB;
}

.livraison-comment h4 {
  margin: 0 0 0.5rem;
  font-size: 0.9rem;
  color: #4B5563;
}

.livraison-comment p {
  margin: 0;
  font-size: 0.9rem;
  color: #1F2937;
}

.livreur-comment {
  background-color: #f0f9ff;
}

.livraison-actions {
  padding: 1rem;
  display: flex;
  gap: 0.75rem;
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

.update-btn {
  background-color: #dbeafe;
  color: #1e40af;
}

.update-btn:hover {
  background-color: #bfdbfe;
}

.comment-btn {
  background-color: #e0f2fe;
  color: #0c4a6e;
  margin-left: auto;
}

.comment-btn:hover {
  background-color: #bae6fd;
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
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.modal-large {
  max-width: 800px;
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
  justify-content: space-between;
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

.confirm-action-btn, .update-action-btn, .comment-action-btn {
  padding: 0.625rem 1.25rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.confirm-action-btn {
  background-color: #0e7490;
  color: white;
}

.confirm-action-btn:hover {
  background-color: #155e75;
}

.confirm-action-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.update-action-btn {
  background-color: #2563eb;
  color: white;
}

.update-action-btn:hover {
  background-color: #1d4ed8;
}

.comment-action-btn {
  background-color: #0ea5e9;
  color: white;
}

.comment-action-btn:hover {
  background-color: #0284c7;
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
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

.livraison-status {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.detail-section {
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #E5E7EB;
  padding-bottom: 1.5rem;
}

.detail-section:last-child {
  border-bottom: none;
  padding-bottom: 0;
  margin-bottom: 0;
}

.detail-section h4 {
  font-size: 1.1rem;
  color: #0e7490;
  margin: 0 0 1rem 0;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.full-width {
  grid-column: span 2;
}

.comment-box {
  background-color: #f9fafb;
  padding: 1rem;
  border-radius: 8px;
}

.client-comment {
  background-color: #f9fafb;
}

.trajet-box {
  background-color: #f0f9ff;
  padding: 1rem;
  border-radius: 8px;
}

.trajet-box p {
  margin: 0.5rem 0;
}

.trajet-link {
  display: inline-block;
  margin-top: 0.75rem;
  background-color: #0e7490;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  text-decoration: none;
  font-size: 0.9rem;
  transition: background-color 0.3s ease;
}

.trajet-link:hover {
  background-color: #155e75;
}

.form-group {
  margin-top: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.form-group select, .form-group textarea {
  width: 100%;
  padding: 0.625rem;
  border: 1px solid #D1D5DB;
  border-radius: 6px;
  font-size: 0.95rem;
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.form-group select:focus, .form-group textarea:focus {
  outline: none;
  border-color: #0e7490;
  box-shadow: 0 0 0 2px rgba(14, 116, 144, 0.2);
}

.status-description {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #f0f9ff;
  border-radius: 6px;
  color: #0c4a6e;
}

.status-select {
  font-weight: 500;
}

.status-label {
  font-weight: 600;
}

.form-error {
  margin-top: 1rem;
  color: #b91c1c;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .livraisons-container {
    padding: 1rem;
  }
  
  .stats-overview {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .filters-section {
    flex-direction: column;
    gap: 1rem;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
  
  .full-width {
    grid-column: auto;
  }
}

@media (max-width: 480px) {
  .stats-overview {
    grid-template-columns: 1fr;
  }
  
  .livraison-actions {
    flex-wrap: wrap;
  }
  
  .comment-btn {
    margin-left: 0;
  }
  
  .modal-footer {
    flex-direction: column;
  }
  
  .action-buttons {
    flex-direction: column;
    width: 100%;
  }
}
</style>