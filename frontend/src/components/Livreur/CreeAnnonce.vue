<template>
  <div class="annonces-container">
    <div class="header-section">
      <h1 class="page-title">Mes Annonces de Trajets</h1>
      <button @click="openNewAnnonceModal" class="add-btn">
        <span class="btn-icon">+</span>
        Créer une nouvelle annonce
      </button>
    </div>

    <!-- Statistiques -->
    <div class="stats-overview">
      <div class="stat-card">
        <span class="stat-icon">🚀</span>
        <div class="stat-content">
          <h3>{{ trajetsActifs.length }}</h3>
          <p>Trajets actifs</p>
        </div>
      </div>
      
      <div class="stat-card">
        <span class="stat-icon">✅</span>
        <div class="stat-content">
          <h3>{{ trajetsCompletes.length }}</h3>
          <p>Trajets complétés</p>
        </div>
      </div>
      
      <div class="stat-card">
        <span class="stat-icon">❌</span>
        <div class="stat-content">
          <h3>{{ trajetsAnnules.length }}</h3>
          <p>Trajets annulés</p>
        </div>
      </div>
    </div>

    <!-- Filtres -->
    <div class="filters-section">
      <div class="filter-group">
        <label for="filter-status">Statut:</label>
        <select id="filter-status" v-model="statusFilter">
          <option value="all">Tous</option>
          <option value="actif">Actifs</option>
          <option value="complete">Complétés</option>
          <option value="annule">Annulés</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label for="filter-date">Trier par:</label>
        <select id="filter-date" v-model="sortBy">
          <option value="date_depart">Date de départ</option>
          <option value="date_creation">Date de création</option>
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

    <!-- Liste des annonces -->
    <div v-if="isLoading" class="loading-indicator">
      <div class="spinner"></div>
      <p>Chargement en cours...</p>
    </div>
    
    <div v-else-if="filteredTrajets.length === 0" class="empty-state">
      <span class="empty-icon">📭</span>
      <p>Aucune annonce de trajet ne correspond à vos critères</p>
      <button @click="openNewAnnonceModal" class="add-btn-secondary">
        Créer une nouvelle annonce
      </button>
    </div>
    
    <div v-else class="trajets-list">
      <div v-for="trajet in filteredTrajets" :key="trajet.id" class="trajet-card" :class="'trajet-' + trajet.statut">
        <div class="trajet-header">
          <h3>{{ trajet.ville_depart }} → {{ trajet.ville_arrivee }}</h3>
          <div class="trajet-badge" :class="'badge-' + trajet.statut">
            {{ getStatusLabel(trajet.statut) }}
          </div>
        </div>
        
        <div class="trajet-details">
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
            <span class="detail-icon">💰</span>
            <div>
              <p class="detail-label">Montant</p>
              <p class="detail-value">{{ trajet.montant }}€</p>
            </div>
          </div>
          <div class="detail-group">
            <span class="detail-icon">📊</span>
            <div>
              <p class="detail-label">Commission</p>
              <p class="detail-value">{{ trajet.commission_plateforme }}€</p>
            </div>
          </div>
          
          <div class="detail-group">
            <span class="detail-icon">⚖️</span>
            <div>
              <p class="detail-label">Capacité</p>
              <p class="detail-value">{{ trajet.capacite_poids }} kg / {{ trajet.capacite_volume }} m³</p>
            </div>
          </div>
          <!-- Afficher la photo du produit -->
          <div v-if="trajet.photo_produit_url" class="trajet-image">
            <img :src="trajet.photo_produit_url" alt="Photo du trajet" class="trajet-thumbnail" />
           </div>
                
          <div class="detail-group">
            <span class="detail-icon">📦</span>
            <div>
              <p class="detail-label">Livraisons</p>
              <p class="detail-value">{{ trajet.livraisons ? trajet.livraisons.length : 0 }} affectée(s)</p>
            </div>
          </div>
        </div>
        
        <div class="trajet-actions">
          <button @click="viewTrajet(trajet)" class="action-btn view-btn">
            <span class="btn-icon">👁️</span>
            Détails
          </button>
          
          <button v-if="trajet.statut === 'actif'" @click="editTrajet(trajet)" class="action-btn edit-btn">
            <span class="btn-icon">✏️</span>
            Modifier
          </button>
          
          <button v-if="trajet.statut === 'actif'" @click="confirmCancelTrajet(trajet)" class="action-btn cancel-btn">
            <span class="btn-icon">❌</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de confirmation d'annulation -->
    <div v-if="showCancelModal" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h3>Confirmation d'annulation</h3>
          <button @click="showCancelModal = false" class="close-btn">&times;</button>
        </div>
        
        <div class="modal-body">
          <p>Êtes-vous sûr de vouloir annuler ce trajet ?</p>
          <p class="warning-text">Cette action est irréversible et toutes les livraisons associées seront également annulées.</p>
          
          <div v-if="selectedTrajet" class="modal-trajet-details">
            <p><strong>Trajet:</strong> {{ selectedTrajet.ville_depart }} → {{ selectedTrajet.ville_arrivee }}</p>
            <p><strong>Date de départ:</strong> {{ formatDate(selectedTrajet.date_depart) }}</p>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="showCancelModal = false" class="cancel-action-btn">Annuler</button>
          <button @click="cancelTrajet" class="confirm-action-btn" :disabled="cancelInProgress">
            <span v-if="cancelInProgress" class="mini-spinner"></span>
            <span v-else>Confirmer l'annulation</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de création/édition d'annonce -->
    <div v-if="showAnnonceModal" class="modal-overlay">
      <div class="modal-container modal-large">
        <div class="modal-header">
          <h3>{{ isEditing ? 'Modifier l\'annonce' : 'Nouvelle annonce de trajet' }}</h3>
          <button @click="closeAnnonceModal" class="close-btn">&times;</button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="submitAnnonceForm" class="annonce-form">
            <div class="form-row">
              <div class="form-group">
                <label for="adresse_depart">Adresse de départ *</label>
                <div class="address-input-container">
                  <input 
                    type="text" 
                    id="adresse_depart" 
                    v-model="annonceForm.adresse_depart" 
                    @input="onAddressInput('depart')"
                    @blur="validateAddress('depart')"
                    :class="{ 'error': addressValidation.depart.error, 'valid': addressValidation.depart.valid }"
                    required
                  >
                  <div v-if="addressValidation.depart.loading" class="address-loader">
                    <div class="mini-spinner"></div>
                  </div>
                  <div v-if="addressValidation.depart.valid" class="address-success">✓</div>
                </div>
                <div v-if="addressValidation.depart.error" class="field-error">
                  {{ addressValidation.depart.errorMessage }}
                </div>
                <div v-if="addressSuggestions.depart.length > 0" class="address-suggestions">
                  <div 
                    v-for="suggestion in addressSuggestions.depart" 
                    :key="suggestion.place_id"
                    @click="selectAddress('depart', suggestion)"
                    class="suggestion-item"
                  >
                    {{ suggestion.description }}
                  </div>
                </div>
              </div>
              
              <div class="form-group">
                <label for="adresse_arrivee">Adresse d'arrivée *</label>
                <div class="address-input-container">
                  <input 
                    type="text" 
                    id="adresse_arrivee" 
                    v-model="annonceForm.adresse_arrivee" 
                    @input="onAddressInput('arrivee')"
                    @blur="validateAddress('arrivee')"
                    :class="{ 'error': addressValidation.arrivee.error, 'valid': addressValidation.arrivee.valid }"
                    required
                  >
                  <div v-if="addressValidation.arrivee.loading" class="address-loader">
                    <div class="mini-spinner"></div>
                  </div>
                  <div v-if="addressValidation.arrivee.valid" class="address-success">✓</div>
                </div>
                <div v-if="addressValidation.arrivee.error" class="field-error">
                  {{ addressValidation.arrivee.errorMessage }}
                </div>
                <div v-if="addressSuggestions.arrivee.length > 0" class="address-suggestions">
                  <div 
                    v-for="suggestion in addressSuggestions.arrivee" 
                    :key="suggestion.place_id"
                    @click="selectAddress('arrivee', suggestion)"
                    class="suggestion-item"
                  >
                    {{ suggestion.description }}
                  </div>
                </div>
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="ville_depart">Ville de départ *</label>
                <input type="text" id="ville_depart" v-model="annonceForm.ville_depart" readonly>
              </div>
              
              <div class="form-group">
                <label for="ville_arrivee">Ville d'arrivée *</label>
                <input type="text" id="ville_arrivee" v-model="annonceForm.ville_arrivee" readonly>
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="code_postal_depart">Code postal de départ *</label>
                <input type="text" id="code_postal_depart" v-model="annonceForm.code_postal_depart" readonly>
              </div>
              
              <div class="form-group">
                <label for="code_postal_arrivee">Code postal d'arrivée *</label>
                <input type="text" id="code_postal_arrivee" v-model="annonceForm.code_postal_arrivee" readonly>
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="date_depart">Date et heure de départ *</label>
                <input 
                  type="datetime-local" 
                  id="date_depart" 
                  v-model="annonceForm.date_depart" 
                  @change="validateDates"
                  :min="minDateTime"
                  :class="{ 'error': dateValidation.depart.error }"
                  required
                >
                <div v-if="dateValidation.depart.error" class="field-error">
                  {{ dateValidation.depart.errorMessage }}
                </div>
              </div>
              
              <div class="form-group">
                <label for="date_arrivee">Date et heure d'arrivée *</label>
                <input 
                  type="datetime-local" 
                  id="date_arrivee" 
                  v-model="annonceForm.date_arrivee" 
                  @change="validateDates"
                  :min="annonceForm.date_depart || minDateTime"
                  :class="{ 'error': dateValidation.arrivee.error }"
                  required
                >
                <div v-if="dateValidation.arrivee.error" class="field-error">
                  {{ dateValidation.arrivee.errorMessage }}
                </div>
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="capacite_poids">Capacité de poids disponible (kg) *</label>
                <input 
                  type="number" 
                  id="capacite_poids" 
                  v-model="annonceForm.capacite_poids" 
                  min="0.1" 
                  step="0.1" 
                  max="50000"
                  required
                >
              </div>
              
              <div class="form-group">
                <label for="capacite_volume">Capacité de volume disponible (m³) *</label>
                <input 
                  type="number" 
                  id="capacite_volume" 
                  v-model="annonceForm.capacite_volume" 
                  min="0.1" 
                  step="0.1" 
                  max="1000"
                  required
                >
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="montant">Prix proposé (€) *</label>
                <input 
                  type="number" 
                  id="montant" 
                  v-model="annonceForm.montant" 
                  min="1" 
                  step="0.01"
                  max="10000"
                  required
                >
              </div> 
              <div class="form-group">
                <label for="photo_produit">Photo (optionnelle)</label>
                <input type="file" id="photo_produit" @change="onPhotoChange" accept="image/*" />
              </div>
              <div class="form-group">
                <label for="commentaire">Commentaire</label>
                <textarea 
                  id="commentaire" 
                  v-model="annonceForm.commentaire" 
                  rows="3"
                  maxlength="500"
                ></textarea>
              </div>
            </div>
            
            <div class="form-error" v-if="formError">{{ formError }}</div>
          </form>
        </div>
        
        <div class="modal-footer">
          <button @click="closeAnnonceModal" class="cancel-action-btn">Annuler</button>
          <button 
            @click="submitAnnonceForm" 
            class="confirm-action-btn" 
            :disabled="submitInProgress || !isFormValid"
          >
            <span v-if="submitInProgress" class="mini-spinner"></span>
            <span v-else>{{ isEditing ? 'Enregistrer les modifications' : 'Créer l\'annonce' }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de détails du trajet -->
    <div v-if="showDetailModal && selectedTrajet" class="modal-overlay">
      <div class="modal-container modal-large">
        <div class="modal-header">
          <h3>Détails du trajet</h3>
          <button @click="showDetailModal = false" class="close-btn">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="trajet-full-details">
            <div class="detail-section">
              <h4>Informations générales</h4>
              <div class="detail-item">
                <span class="detail-label">Statut:</span>
                <span class="trajet-badge" :class="'badge-' + selectedTrajet.statut">
                  {{ getStatusLabel(selectedTrajet.statut) }}
                </span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Créé le:</span>
                <span>{{ formatDate(selectedTrajet.date_creation) }}</span>
              </div>
            </div>
            
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
            
            <div class="detail-section" v-if="selectedTrajet.commentaire">
              <h4>Commentaire</h4>
              <p class="trajet-commentaire">{{ selectedTrajet.commentaire }}</p>
            </div>
            
            <div class="detail-section" v-if="selectedTrajet.livraisons && selectedTrajet.livraisons.length > 0">
              <h4>Livraisons associées ({{ selectedTrajet.livraisons.length }})</h4>
              <div class="livraisons-list">
                <div v-for="livraison in selectedTrajet.livraisons" :key="livraison.id" class="livraison-item">
                  <div class="livraison-header">
                    <span class="livraison-id">Livraison #{{ livraison.id }}</span>
                    <span class="livraison-badge" :class="'badge-' + livraison.statut">{{ getLivraisonStatusLabel(livraison.statut) }}</span>
                  </div>
                  <div class="livraison-details">
                    <p><strong>Client:</strong> {{ livraison.client_nom }}</p>
                    <p><strong>Date prévue:</strong> {{ formatDate(livraison.date_livraison_prevue) }}</p>
                    <p><strong>Montant:</strong> {{ livraison.montant }}€</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="showDetailModal = false" class="cancel-action-btn">Fermer</button>
          <div v-if="selectedTrajet.statut === 'actif'" class="action-buttons">
            <button @click="editTrajet(selectedTrajet); showDetailModal = false;" class="edit-action-btn">
              <span class="btn-icon">✏️</span>
              Modifier
            </button>
            <button @click="confirmCancelTrajet(selectedTrajet); showDetailModal = false;" class="delete-action-btn">
              <span class="btn-icon">❌</span>
              Annuler
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const trajets = ref([]);
const isLoading = ref(true);
const showCancelModal = ref(false);
const showAnnonceModal = ref(false);
const showDetailModal = ref(false);
const selectedTrajet = ref(null);
const cancelInProgress = ref(false);
const submitInProgress = ref(false);
const formError = ref('');
const isEditing = ref(false);
const photoFile = ref(null);

// Google Maps variables
let googleMapsLoaded = false;
let autocompleteService = null;
let placesService = null;
let geocoder = null;

// Filtres
const statusFilter = ref('all');
const sortBy = ref('date_depart');
const orderDirection = ref('desc');

// Validation des adresses
const addressValidation = ref({
  depart: { valid: false, error: false, loading: false, errorMessage: '' },
  arrivee: { valid: false, error: false, loading: false, errorMessage: '' }
});

const addressSuggestions = ref({
  depart: [],
  arrivee: []
});

// Validation des dates
const dateValidation = ref({
  depart: { error: false, errorMessage: '' },
  arrivee: { error: false, errorMessage: '' }
});

// Date minimale (maintenant + 2 heures)
const minDateTime = computed(() => {
  const now = new Date();
  now.setHours(now.getHours() + 2);
  return now.toISOString().slice(0, 16);
});

// Formulaire d'annonce
const annonceForm = ref({
  adresse_depart: '',
  ville_depart: '',
  code_postal_depart: '',
  montant: '',
  adresse_arrivee: '',
  ville_arrivee: '',
  code_postal_arrivee: '',
  date_depart: '',
  date_arrivee: '',
  capacite_poids: '',
  capacite_volume: '',
  commentaire: ''
});

// Validation globale du formulaire
const isFormValid = computed(() => {
  return addressValidation.value.depart.valid && 
         addressValidation.value.arrivee.valid &&
         !dateValidation.value.depart.error &&
         !dateValidation.value.arrivee.error &&
         annonceForm.value.date_depart &&
         annonceForm.value.date_arrivee &&
         annonceForm.value.capacite_poids &&
         annonceForm.value.capacite_volume &&
         annonceForm.value.montant;
});

// Initialiser Google Maps
const initGoogleMaps = () => {
  if (googleMapsLoaded) return;
  
  const script = document.createElement('script');
  script.src = `https://maps.googleapis.com/maps/api/js?key=${import.meta.env.VITE_GOOGLE_MAPS_API_KEY}&libraries=places&callback=initMapsCallback`;
  script.async = true;
  script.defer = true;
  
  window.initMapsCallback = () => {
    googleMapsLoaded = true;
    autocompleteService = new google.maps.places.AutocompleteService();
    const mapDiv = document.createElement('div');
    const map = new google.maps.Map(mapDiv);
    placesService = new google.maps.places.PlacesService(map);
    geocoder = new google.maps.Geocoder();
  };
  
  document.head.appendChild(script);
};

const onPhotoChange = (event) => {
  photoFile.value = event.target.files[0];
};
// Debounce function
const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

// Gérer la saisie d'adresse avec debounce
const onAddressInput = debounce((type) => {
  const address = annonceForm.value[`adresse_${type}`];
  
  if (address.length < 3) {
    addressSuggestions.value[type] = [];
    addressValidation.value[type] = { valid: false, error: false, loading: false, errorMessage: '' };
    return;
  }
  
  addressValidation.value[type].loading = true;
  addressValidation.value[type].error = false;
  
  if (!googleMapsLoaded || !autocompleteService) {
    addressValidation.value[type] = { 
      valid: false, 
      error: true, 
      loading: false, 
      errorMessage: 'Service de géolocalisation non disponible' 
    };
    return;
  }
  
  const request = {
    input: address,
    componentRestrictions: { country: 'fr' },
    types: ['address']
  };
  
  autocompleteService.getPlacePredictions(request, (predictions, status) => {
    addressValidation.value[type].loading = false;
    
    if (status === google.maps.places.PlacesServiceStatus.OK && predictions) {
      addressSuggestions.value[type] = predictions.slice(0, 5);
      addressValidation.value[type].error = false;
    } else {
      addressSuggestions.value[type] = [];
      addressValidation.value[type] = { 
        valid: false, 
        error: true, 
        loading: false, 
        errorMessage: 'Aucune adresse trouvée' 
      };
    }
  });
}, 300);

// Sélectionner une adresse suggérée
const selectAddress = (type, suggestion) => {
  annonceForm.value[`adresse_${type}`] = suggestion.description;
  addressSuggestions.value[type] = [];
  
  // Obtenir les détails de l'adresse
  if (placesService) {
    placesService.getDetails({
      placeId: suggestion.place_id,
      fields: ['address_components', 'formatted_address']
    }, (place, status) => {
      if (status === google.maps.places.PlacesServiceStatus.OK) {
        extractAddressComponents(type, place);
      }
    });
  }
};

// Extraire les composants de l'adresse
const extractAddressComponents = (type, place) => {
  let ville = '';
  let codePostal = '';
  
  for (const component of place.address_components) {
    const types = component.types;
    
    if (types.includes('locality')) {
      ville = component.long_name;
    } else if (types.includes('administrative_area_level_2') && !ville) {
      ville = component.long_name;
    } else if (types.includes('postal_code')) {
      codePostal = component.long_name;
    }
  }
  
  annonceForm.value[`ville_${type}`] = ville;
  annonceForm.value[`code_postal_${type}`] = codePostal;
  
  addressValidation.value[type] = { 
    valid: true, 
    error: false, 
    loading: false, 
    errorMessage: '' 
  };
};

// Valider une adresse manuellement
const validateAddress = (type) => {
  const address = annonceForm.value[`adresse_${type}`];
  
  if (!address || address.length < 5) {
    addressValidation.value[type] = { 
      valid: false, 
      error: true, 
      loading: false, 
      errorMessage: 'Adresse trop courte' 
    };
    return;
  }
  
  if (!googleMapsLoaded || !geocoder) {
    addressValidation.value[type] = { 
      valid: false, 
      error: true, 
      loading: false, 
      errorMessage: 'Service de validation non disponible' 
    };
    return;
  }
  
  addressValidation.value[type].loading = true;
  
  geocoder.geocode({
    address: address,
    componentRestrictions: { country: 'FR' }
  }, (results, status) => {
    addressValidation.value[type].loading = false;
    
    if (status === google.maps.GeocoderStatus.OK && results[0]) {
      extractAddressComponents(type, results[0]);
    } else {
      addressValidation.value[type] = { 
        valid: false, 
        error: true, 
        loading: false, 
        errorMessage: 'Adresse non valide ou introuvable'
        };
    }
  });
};

// Valider les dates
const validateDates = () => {
  const now = new Date();
  now.setHours(now.getHours() + 2);
  
  const dateDepart = new Date(annonceForm.value.date_depart);
  const dateArrivee = new Date(annonceForm.value.date_arrivee);
  
  // Validation date de départ
  if (dateDepart < now) {
    dateValidation.value.depart = {
      error: true,
      errorMessage: 'La date de départ doit être dans au moins 2 heures'
    };
  } else {
    dateValidation.value.depart = { error: false, errorMessage: '' };
  }
  
  // Validation date d'arrivée
  if (dateArrivee < dateDepart) {
    dateValidation.value.arrivee = {
      error: true,
      errorMessage: 'La date d\'arrivée doit être après la date de départ'
    };
  } else {
    dateValidation.value.arrivee = { error: false, errorMessage: '' };
  }
};

// Computed properties pour les trajets filtrés
const trajetsActifs = computed(() => 
  trajets.value.filter(t => t.statut === 'actif')
);

const trajetsCompletes = computed(() => 
  trajets.value.filter(t => t.statut === 'complete')
);

const trajetsAnnules = computed(() => 
  trajets.value.filter(t => t.statut === 'annule')
);

const filteredTrajets = computed(() => {
  let filtered = trajets.value;
  
  // Filtrer par statut
  if (statusFilter.value !== 'all') {
    filtered = filtered.filter(t => t.statut === statusFilter.value);
  }
  
  // Trier
  filtered.sort((a, b) => {
    const aValue = new Date(a[sortBy.value]);
    const bValue = new Date(b[sortBy.value]);
    
    if (orderDirection.value === 'asc') {
      return aValue - bValue;
    } else {
      return bValue - aValue;
    }
  });
  
  return filtered;
});

// Méthodes de gestion des trajets
const loadTrajets = async () => {
  try {
    isLoading.value = true;
    const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/trajets/`);
    trajets.value = response.data;
  } catch (error) {
    console.error('Erreur lors du chargement des trajets:', error);
    // Gérer l'erreur (notification, etc.)
  } finally {
    isLoading.value = false;
  }
};

const getStatusLabel = (statut) => {
  const labels = {
    'actif': 'Actif',
    'complete': 'Complété',
    'annule': 'Annulé'
  };
  return labels[statut] || statut;
};

const getLivraisonStatusLabel = (statut) => {
  const labels = {
    'en_attente': 'En attente',
    'confirmee': 'Confirmée',
    'en_cours': 'En cours',
    'livree': 'Livrée',
    'annulee': 'Annulée'
  };
  return labels[statut] || statut;
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString('fr-FR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// Méthodes pour les modals
const openNewAnnonceModal = () => {
  resetAnnonceForm();
  isEditing.value = false;
  showAnnonceModal.value = true;
  nextTick(() => {
    if (!googleMapsLoaded) {
      initGoogleMaps();
    }
  });
};

const editTrajet = (trajet) => {
  isEditing.value = true;
  selectedTrajet.value = trajet;
  
  // Remplir le formulaire avec les données du trajet
  annonceForm.value = {
    adresse_depart: trajet.adresse_depart,
    ville_depart: trajet.ville_depart,
    code_postal_depart: trajet.code_postal_depart,
    adresse_arrivee: trajet.adresse_arrivee,
    ville_arrivee: trajet.ville_arrivee,
    code_postal_arrivee: trajet.code_postal_arrivee,
    date_depart: new Date(trajet.date_depart).toISOString().slice(0, 16),
    date_arrivee: new Date(trajet.date_arrivee).toISOString().slice(0, 16),
    capacite_poids: trajet.capacite_poids,
    capacite_volume: trajet.capacite_volume,
    montant: trajet.montant,
    commentaire: trajet.commentaire || ''
  };
  
  // Marquer les adresses comme valides
  addressValidation.value.depart.valid = true;
  addressValidation.value.arrivee.valid = true;
  
  showAnnonceModal.value = true;
  nextTick(() => {
    if (!googleMapsLoaded) {
      initGoogleMaps();
    }
  });
};

const viewTrajet = (trajet) => {
  selectedTrajet.value = trajet;
  showDetailModal.value = true;
};

const confirmCancelTrajet = (trajet) => {
  selectedTrajet.value = trajet;
  showCancelModal.value = true;
};

const cancelTrajet = async () => {
  try {
    cancelInProgress.value = true;
    await axios.post(`${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/trajets/${selectedTrajet.value.id}/annuler/`);
    
    // Mettre à jour le trajet dans la liste
    const index = trajets.value.findIndex(t => t.id === selectedTrajet.value.id);
    if (index !== -1) {
      trajets.value[index].statut = 'annule';
    }
    
    showCancelModal.value = false;
    selectedTrajet.value = null;
    
    // Notification de succès
    // showNotification('Trajet annulé avec succès', 'success');
    
  } catch (error) {
    console.error('Erreur lors de l\'annulation du trajet:', error);
    // showNotification('Erreur lors de l\'annulation du trajet', 'error');
  } finally {
    cancelInProgress.value = false;
  }
};

const resetAnnonceForm = () => {
  annonceForm.value = {
    adresse_depart: '',
    ville_depart: '',
    code_postal_depart: '',
    adresse_arrivee: '',
    ville_arrivee: '',
    code_postal_arrivee: '',
    date_depart: '',
    date_arrivee: '',
    capacite_poids: '',
    capacite_volume: '',
    montant: '',
    commentaire: ''
  };
  
  addressValidation.value = {
    depart: { valid: false, error: false, loading: false, errorMessage: '' },
    arrivee: { valid: false, error: false, loading: false, errorMessage: '' }
  };
  
  dateValidation.value = {
    depart: { error: false, errorMessage: '' },
    arrivee: { error: false, errorMessage: '' }
  };
  
  addressSuggestions.value = {
    depart: [],
    arrivee: []
  };
  
  formError.value = '';
};

const closeAnnonceModal = () => {
  showAnnonceModal.value = false;
  selectedTrajet.value = null;
  resetAnnonceForm();
};

const submitAnnonceForm = async () => {
  if (!isFormValid.value) {
    formError.value = 'Veuillez remplir tous les champs obligatoires';
    return;
  }

  try {
    submitInProgress.value = true;
    formError.value = '';

    const formData = {
      ...annonceForm.value,
      montant: parseFloat(annonceForm.value.montant),
      capacite_poids: parseFloat(annonceForm.value.capacite_poids),
      capacite_volume: parseFloat(annonceForm.value.capacite_volume)
    };

    let response;
    if (isEditing.value) {
      response = await axios.put(`${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/trajets/${selectedTrajet.value.id}/`, formData);
      const index = trajets.value.findIndex(t => t.id === selectedTrajet.value.id);
      if (index !== -1) {
        trajets.value[index] = response.data;
      }
    } else {
      response = await axios.post(`${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/trajets/`, formData);
      trajets.value.unshift(response.data);
    }

    if (photoFile.value && response.data.id) {
      const imageFormData = new FormData();
      imageFormData.append('photo_produit', photoFile.value);

      await axios.post(
        `${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/trajets/${response.data.id}/upload_photo/`,
        imageFormData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );

      await loadTrajets();
    }

    closeAnnonceModal();
  } catch (error) {
    console.error('Erreur lors de la soumission:', error);
    formError.value = error.response?.data?.message || 'Erreur inattendue';
  } finally {
    submitInProgress.value = false;
  }
};

// Lifecycle
onMounted(() => {
  loadTrajets();
});
</script>

<style scoped>
.annonces-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 15px;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.add-btn {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(52, 152, 219, 0.3);
}

.add-btn:hover {
  background: linear-gradient(135deg, #2980b9, #3498db);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(52, 152, 219, 0.4);
}

.btn-icon {
  font-size: 1.2rem;
  font-weight: bold;
}

/* Statistiques */
.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border: 1px solid #e8f4f8;
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 2rem;
  padding: 10px;
  border-radius: 50%;
  background: #f8f9fa;
}

.stat-content h3 {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.stat-content p {
  color: #7f8c8d;
  margin: 0;
  font-size: 0.9rem;
}

/* Filtres */
.filters-section {
  background: white;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 30px;
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.filter-group label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
}

.filter-group select {
  padding: 8px 12px;
  border: 2px solid #e8f4f8;
  border-radius: 6px;
  background: white;
  font-size: 0.9rem;
  min-width: 150px;
  transition: border-color 0.2s ease;
}

.filter-group select:focus {
  outline: none;
  border-color: #3498db;
}

/* États de chargement et vide */
.loading-indicator {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e8f4f8;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
  display: block;
}

.empty-state p {
  color: #7f8c8d;
  font-size: 1.1rem;
  margin-bottom: 20px;
}

.add-btn-secondary {
  background: #95a5a6;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.add-btn-secondary:hover {
  background: #7f8c8d;
}

/* Liste des trajets */
.trajets-list {
  display: grid;
  gap: 20px;
}

.trajet-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #3498db;
  transition: all 0.3s ease;
}

.trajet-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.trajet-actif {
  border-left-color: #27ae60;
}

.trajet-complete {
  border-left-color: #95a5a6;
  opacity: 0.8;
}

.trajet-annule {
  border-left-color: #e74c3c;
  opacity: 0.7;
}

.trajet-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

.trajet-header h3 {
  font-size: 1.3rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.trajet-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.badge-actif {
  background: #d5f4e6;
  color: #27ae60;
}

.badge-complete {
  background: #ecf0f1;
  color: #95a5a6;
}

.badge-annule {
  background: #fadbd8;
  color: #e74c3c;
}

/* Détails du trajet */
.trajet-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.detail-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.detail-icon {
  font-size: 1.2rem;
  width: 24px;
  text-align: center;
}

.detail-label {
  font-size: 0.8rem;
  color: #7f8c8d;
  margin: 0 0 2px 0;
  font-weight: 500;
}

.detail-value {
  font-size: 0.9rem;
  color: #2c3e50;
  margin: 0;
  font-weight: 600;
}

/* Actions des trajets */
.trajet-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.action-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}

.view-btn {
  background: #3498db;
  color: white;
}

.view-btn:hover {
  background: #2980b9;
}

.edit-btn {
  background: #f39c12;
  color: white;
}

.edit-btn:hover {
  background: #e67e22;
}

.cancel-btn {
  background: #e74c3c;
  color: white;
}

.cancel-btn:hover {
  background: #c0392b;
}

/* Modals */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-container {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.modal-large {
  max-width: 800px;
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e8f4f8;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.3rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #7f8c8d;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: #f8f9fa;
  color: #2c3e50;
}

.modal-body {
  padding: 24px;
}

.modal-footer {
  padding: 20px 24px;
  border-top: 1px solid #e8f4f8;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* Formulaire d'annonce */
.annonce-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 12px;
  border: 2px solid #e8f4f8;
  border-radius: 6px;
  font-size: 0.9rem;
  transition: border-color 0.2s ease;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #3498db;
}

.form-group input.error {
  border-color: #e74c3c;
}

.form-group input.valid {
  border-color: #27ae60;
}

.form-group input[readonly] {
  background: #f8f9fa;
  color: #7f8c8d;
}

/* Validation des adresses */
.address-input-container {
  position: relative;
}

.address-loader,
.address-success {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
}

.address-success {
  color: #27ae60;
  font-weight: bold;
}

.mini-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #e8f4f8;
  border-top: 2px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.field-error {
  color: #e74c3c;
  font-size: 0.8rem;
  font-weight: 500;
}

.address-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 2px solid #e8f4f8;
  border-top: none;
  border-radius: 0 0 6px 6px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 100;
}

.suggestion-item {
  padding: 12px;
  cursor: pointer;
  transition: background 0.2s ease;
  font-size: 0.9rem;
}

.suggestion-item:hover {
  background: #f8f9fa;
}

.form-error {
  color: #e74c3c;
  font-size: 0.9rem;
  font-weight: 500;
  text-align: center;
  padding: 10px;
  background: #fadbd8;
  border-radius: 6px;
}

/* Boutons d'action des modals */
.cancel-action-btn {
  background: #95a5a6;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s ease;
}

.cancel-action-btn:hover {
  background: #7f8c8d;
}

.confirm-action-btn {
  background: #27ae60;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.confirm-action-btn:hover:not(:disabled) {
  background: #229954;
}

.confirm-action-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.edit-action-btn {
  background: #f39c12;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.edit-action-btn:hover {
  background: #e67e22;
}

.delete-action-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.delete-action-btn:hover {
  background: #c0392b;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.warning-text {
  color: #e67e22;
  font-weight: 500;
  margin: 10px 0;
}

.modal-trajet-details {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  margin: 15px 0;
}

/* Détails complets du trajet */
.trajet-full-details {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.detail-section {
  border-bottom: 1px solid #e8f4f8;
  padding-bottom: 20px;
}

.detail-section:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.detail-section h4 {
  margin: 0 0 15px 0;
  color: #2c3e50;
  font-size: 1.1rem;
  font-weight: 600;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  flex-wrap: wrap;
  gap: 10px;
}

.detail-item .detail-label {
  font-weight: 600;
  color: #7f8c8d;
  min-width: 150px;
}

.trajet-commentaire {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  margin: 0;
  color: #2c3e50;
  font-style: italic;
}

/* Livraisons associées */
.livraisons-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.livraison-item {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  border-left: 3px solid #3498db;
}

.livraison-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  flex-wrap: wrap;
  gap: 10px;
}

.livraison-id {
  font-weight: 600;
  color: #2c3e50;
}

.livraison-details p {
  margin: 5px 0;
  font-size: 0.9rem;
  color: #34495e;
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

/* Responsive */
@media (max-width: 768px) {
  .annonces-container {
    padding: 15px;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .header-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .stats-overview {
    grid-template-columns: 1fr;
  }
  
  .filters-section {
    flex-direction: column;
  }
  
  .trajet-details {
    grid-template-columns: 1fr;
  }
  
  .trajet-actions {
    justify-content: stretch;
  }
  
  .action-btn {
    flex: 1;
    justify-content: center;
  }
  
  .modal-container {
    margin: 10px;
    max-width: none;
  }
  
  .modal-footer {
    flex-direction: column;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .detail-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .detail-item .detail-label {
    min-width: auto;
  }
}
</style>