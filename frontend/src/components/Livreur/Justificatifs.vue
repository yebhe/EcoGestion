<template>
    <div class="justificatifs-container">
      <div class="header-section">
        <h1 class="page-title">Mes Pièces Justificatives</h1>
        <button @click="openUploadModal" class="add-btn">
          <span class="btn-icon">+</span>
          Ajouter un justificatif
        </button>
      </div>
  
      <!-- Statistiques -->
      <div class="stats-overview">
        <div class="stat-card">
          <span class="stat-icon">✅</span>
          <div class="stat-content">
            <h3>{{ justificatifsValides.length }}</h3>
            <p>Justificatifs validés</p>
          </div>
        </div>
        
        <div class="stat-card">
          <span class="stat-icon">⏳</span>
          <div class="stat-content">
            <h3>{{ justificatifsEnAttente.length }}</h3>
            <p>Justificatifs en attente</p>
          </div>
        </div>
        
        <div class="stat-card">
          <span class="stat-icon">❌</span>
          <div class="stat-content">
            <h3>{{ justificatifsRejetes.length }}</h3>
            <p>Justificatifs rejetés</p>
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
            <option value="valide">Validés</option>
            <option value="rejete">Rejetés</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="filter-type">Type de document:</label>
          <select id="filter-type" v-model="typeFilter">
            <option value="all">Tous</option>
            <option v-for="type in justificatifTypes" :key="type.id" :value="type.id">{{ type.nom }}</option>
          </select>
        </div>
      </div>
  
      <!-- Indications pour documents manquants -->
      <div v-if="documentsObligatoiresManquants.length > 0" class="missing-docs-alert">
        <div class="alert-header">
          <span class="alert-icon">⚠️</span>
          <h3>Documents obligatoires manquants</h3>
        </div>
        <p>Veuillez fournir les documents suivants pour compléter votre profil :</p>
        <ul class="missing-docs-list">
          <li v-for="doc in documentsObligatoiresManquants" :key="doc.id" class="missing-doc-item">
            <span class="doc-name">{{ doc.nom }}</span>
            <span class="doc-description">{{ doc.description }}</span>
            <button @click="uploadMissingDoc(doc)" class="upload-missing-btn">
              Téléverser
            </button>
          </li>
        </ul>
      </div>
  
      <!-- Liste des justificatifs -->
      <div v-if="isLoading" class="loading-indicator">
        <div class="spinner"></div>
        <p>Chargement en cours...</p>
      </div>
      
      <div v-else-if="filteredJustificatifs.length === 0" class="empty-state">
        <span class="empty-icon">📄</span>
        <p>Aucun justificatif ne correspond à vos critères</p>
        <button @click="openUploadModal" class="add-btn-secondary">
          Ajouter un justificatif
        </button>
      </div>
      
      <div v-else class="justificatifs-grid">
        <div v-for="justificatif in filteredJustificatifs" :key="justificatif.id" class="justificatif-card">
          <div class="justificatif-header" :class="'status-' + justificatif.statut">
            <h3>{{ getJustificatifTypeName(justificatif.type_justificatif) }}</h3>
            <div class="justificatif-badge" :class="'badge-' + justificatif.statut">
              {{ getStatusLabel(justificatif.statut) }}
            </div>
          </div>
          
          <div class="justificatif-details">
            <div class="detail-group">
              <span class="detail-icon">⏰</span>
              <div>
                <p class="detail-label">Date d'envoi</p>
                <p class="detail-value">{{ formatDate(justificatif.date_upload) }}</p>
              </div>
            </div>
            
            <div class="detail-group">
              <span class="detail-icon">📎</span>
              <div>
                <p class="detail-label">Fichier</p>
                <p class="detail-value">{{ getFileName(justificatif.fichier) }}</p>
              </div>
            </div>
          </div>
          
          <div v-if="justificatif.commentaire_admin" class="justificatif-comment">
            <h4>Commentaire administrateur :</h4>
            <p>{{ justificatif.commentaire_admin }}</p>
          </div>
          
          <div class="justificatif-actions">
            <a :href="justificatif.fichier" target="_blank" class="action-btn view-btn">
              <span class="btn-icon">👁️</span>
              Voir
            </a>
            
            <button v-if="justificatif.statut === 'rejete'" @click="remplacerJustificatif(justificatif)" class="action-btn replace-btn">
              <span class="btn-icon">🔄</span>
              Remplacer
            </button>
          </div>
        </div>
      </div>
  
      <!-- Modal d'upload -->
      <div v-if="showUploadModal" class="modal-overlay">
        <div class="modal-container">
          <div class="modal-header">
            <h3>{{ isReplacing ? 'Remplacer le justificatif' : 'Ajouter un justificatif' }}</h3>
            <button @click="closeUploadModal" class="close-btn">&times;</button>
          </div>
          
          <div class="modal-body">
            <form @submit.prevent="submitJustificatif" class="upload-form">
              <div class="form-group" v-if="!isReplacing">
                <label for="type_justificatif">Type de document *</label>
                <select id="type_justificatif" v-model="uploadForm.type_justificatif" required>
                <option value="">Sélectionnez un type</option>
                <option v-for="type in availableTypes" 
                        :key="type.id" 
                        :value="type.id"
                        :disabled="type.disabled">
                    {{ type.nom }}{{ type.obligatoire ? ' (Obligatoire)' : '' }}
                    <span v-if="type.disabled">(Déjà fourni - {{ getStatusLabel(type.existingStatus) }})</span>
                </option>
                </select>
                
                <div v-if="selectedTypeInfo" class="type-description">
                  <p>{{ selectedTypeInfo.description }}</p>
                </div>
              </div>
              
              <div class="form-group">
                <label for="fichier">Fichier *</label>
                <div class="file-upload-container">
                  <input type="file" id="fichier" ref="fileInput" @change="handleFileChange" class="file-input" accept=".pdf,.jpg,.jpeg,.png">
                  <div class="file-upload-preview" v-if="selectedFile">
                    <div class="file-info">
                      <span class="file-icon">{{ getFileIcon(selectedFile.name) }}</span>
                      <div class="file-details">
                        <p class="file-name">{{ selectedFile.name }}</p>
                        <p class="file-size">{{ formatFileSize(selectedFile.size) }}</p>
                      </div>
                    </div>
                    <button type="button" @click="removeSelectedFile" class="remove-file-btn">&times;</button>
                  </div>
                  <div v-else class="file-upload-placeholder">
                    <span class="upload-icon">📤</span>
                    <p>Cliquez ou glissez-déposez un fichier ici</p>
                    <p class="file-format-hint">Formats acceptés : PDF, JPG, PNG</p>
                  </div>
                </div>
              </div>
              
              <div class="form-error" v-if="formError">{{ formError }}</div>
            </form>
          </div>
          
          <div class="modal-footer">
            <button @click="closeUploadModal" class="cancel-action-btn">Annuler</button>
            <button @click="submitJustificatif" class="confirm-action-btn" :disabled="!selectedFile || submitInProgress">
              <span v-if="submitInProgress" class="mini-spinner"></span>
              <span v-else>{{ isReplacing ? 'Remplacer' : 'Envoyer' }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue';
  import axios from 'axios';
  
  const justificatifs = ref([]);
  const justificatifTypes = ref([]);
  const isLoading = ref(true);
  const statusFilter = ref('all');
  const typeFilter = ref('all');
  const showUploadModal = ref(false);
  const isReplacing = ref(false);
  const selectedFile = ref(null);
  const formError = ref('');
  const submitInProgress = ref(false);
  const replacingJustificatifId = ref(null);
  
  // Formulaire d'upload
  const uploadForm = ref({
    type_justificatif: '',
    fichier: null
  });
  
  // Récupérer les justificatifs
  const fetchJustificatifs = async () => {
    isLoading.value = true;
    try {
      const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/justificatifs/`);
      justificatifs.value = response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des justificatifs:', error);
    } finally {
      isLoading.value = false;
    }
  };
  
  // Récupérer les types de justificatifs
  const fetchJustificatifTypes = async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/types-justificatifs/`);
      justificatifTypes.value = response.data;
      console.log('les pieces', this.justificatifTypes)
    } catch (error) {
      console.error('Erreur lors de la récupération des types de justificatifs:', error);
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
  
  // Extraire le nom du fichier à partir du chemin
  const getFileName = (filePath) => {
    if (!filePath) return 'N/A';
    return filePath.split('/').pop();
  };
  
  // Obtenir le nom du type de justificatif à partir de l'ID
  const getJustificatifTypeName = (typeId) => {
    const type = justificatifTypes.value.find(t => t.id === typeId);
    return type ? type.nom : 'Type inconnu';
  };
  
  // Traduction des statuts
  const getStatusLabel = (status) => {
    const labels = {
      'en_attente': 'En attente',
      'valide': 'Validé',
      'rejete': 'Rejeté'
    };
    return labels[status] || status;
  };
  
  // Obtenir l'icône en fonction de l'extension du fichier
  const getFileIcon = (fileName) => {
    const extension = fileName.split('.').pop().toLowerCase();
    switch (extension) {
      case 'pdf':
        return '📄';
      case 'jpg':
      case 'jpeg':
      case 'png':
        return '🖼️';
      default:
        return '📎';
    }
  };
  
  // Formater la taille du fichier
  const formatFileSize = (bytes) => {
    if (bytes < 1024) {
      return bytes + ' octets';
    } else if (bytes < 1048576) {
      return (bytes / 1024).toFixed(1) + ' Ko';
    } else {
      return (bytes / 1048576).toFixed(1) + ' Mo';
    }
  };
  
  // Computed pour filtrer les justificatifs
  const filteredJustificatifs = computed(() => {
    let filtered = [...justificatifs.value];
    
    // Filtrer par statut
    if (statusFilter.value !== 'all') {
      filtered = filtered.filter(j => j.statut === statusFilter.value);
    }
    
    // Filtrer par type
    if (typeFilter.value !== 'all') {
      filtered = filtered.filter(j => j.type_justificatif === typeFilter.value);
    }
    
    // Trier par date d'upload (plus récent d'abord)
    filtered.sort((a, b) => new Date(b.date_upload) - new Date(a.date_upload));
    
    return filtered;
  });
  
  // Computed pour les statistiques
  const justificatifsValides = computed(() => {
    return justificatifs.value.filter(j => j.statut === 'valide');
  });
  
  const justificatifsEnAttente = computed(() => {
    return justificatifs.value.filter(j => j.statut === 'en_attente');
  });
  
  const justificatifsRejetes = computed(() => {
    return justificatifs.value.filter(j => j.statut === 'rejete');
  });
  
  // Computed pour les documents obligatoires manquants
  const documentsObligatoiresManquants = computed(() => {
    // Types obligatoires
    const typesObligatoires = justificatifTypes.value.filter(t => t.obligatoire);
    
    // Types déjà fournis et validés
    const typesValides = justificatifs.value
      .filter(j => j.statut === 'valide')
      .map(j => j.type_justificatif);
    
    // Types en attente de validation
    const typesEnAttente = justificatifs.value
      .filter(j => j.statut === 'en_attente')
      .map(j => j.type_justificatif);
    
    // Types obligatoires manquants (ni validés ni en attente)
    return typesObligatoires.filter(t => 
      !typesValides.includes(t.id) && !typesEnAttente.includes(t.id)
    );
  });
  
  // Computed pour l'information sur le type sélectionné
  const selectedTypeInfo = computed(() => {
    if (!uploadForm.value.type_justificatif) return null;
    return justificatifTypes.value.find(t => t.id === uploadForm.value.type_justificatif);
  });
  
  // Ouvrir le modal d'upload
  const openUploadModal = () => {
    isReplacing.value = false;
    uploadForm.value = {
      type_justificatif: '',
      fichier: null
    };
    selectedFile.value = null;
    formError.value = '';
    showUploadModal.value = true;
  };
  
  // Fermer le modal d'upload
  const closeUploadModal = () => {
    showUploadModal.value = false;
    formError.value = '';
    selectedFile.value = null;
  };
  
  // Gérer le changement de fichier
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Vérifier que le type de fichier est autorisé
      const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg'];
      if (!allowedTypes.includes(file.type)) {
        formError.value = 'Format de fichier non supporté. Veuillez télécharger un PDF, JPG ou PNG.';
        return;
      }
      
      // Vérifier la taille du fichier (max 5 Mo)
      const maxSize = 5 * 1024 * 1024; // 5 Mo en octets
      if (file.size > maxSize) {
        formError.value = 'Le fichier est trop volumineux. Taille maximale: 5 Mo.';
        return;
      }
      
      selectedFile.value = file;
      formError.value = '';
    }
  };
  
  // Supprimer le fichier sélectionné
  const removeSelectedFile = () => {
    selectedFile.value = null;
    if (this.$refs.fileInput) {
      this.$refs.fileInput.value = '';
    }
  };
  
  // Uploader un document manquant
  const uploadMissingDoc = (docType) => {
    isReplacing.value = false;
    uploadForm.value = {
      type_justificatif: docType.id,
      fichier: null
    };
    selectedFile.value = null;
    formError.value = '';
    showUploadModal.value = true;
  };
  
  // Remplacer un justificatif
  const remplacerJustificatif = (justificatif) => {
    isReplacing.value = true;
    replacingJustificatifId.value = justificatif.id;
    uploadForm.value = {
      type_justificatif: justificatif.type_justificatif,
      fichier: null
    };
    selectedFile.value = null;
    formError.value = '';
    showUploadModal.value = true;
  };
  
  // Soumettre le formulaire de justificatif
  const submitJustificatif = async () => {
  if (!selectedFile.value) {
    formError.value = 'Veuillez sélectionner un fichier';
    return;
  }
  
  if (!isReplacing.value && !uploadForm.value.type_justificatif) {
    formError.value = 'Veuillez sélectionner un type de document';
    return;
  }
  
  // Vérifier si un justificatif existe déjà pour ce type (sauf en cas de remplacement)
  if (!isReplacing.value) {
    const typeId = uploadForm.value.type_justificatif;
    const existingJustificatif = justificatifs.value.find(j => 
      j.type_justificatif == typeId && 
      (j.statut === 'en_attente' || j.statut === 'valide')
    );
    
    if (existingJustificatif) {
      // Demander confirmation pour remplacer
      if (!confirm(`Un justificatif de type "${getJustificatifTypeName(typeId)}" existe déjà. Voulez-vous le remplacer ?`)) {
        return;
      }
      
      // Configurer pour remplacer plutôt que créer
      isReplacing.value = true;
      replacingJustificatifId.value = existingJustificatif.id;
    }
  }
  
  submitInProgress.value = true;
  formError.value = '';
  
  try {
    // Créer un FormData pour l'upload de fichier
    const formData = new FormData();
    if (!isReplacing.value) {
      formData.append('type_justificatif', uploadForm.value.type_justificatif);
    }
    formData.append('fichier', selectedFile.value);
    
    let response;
    if (isReplacing.value) {
      // Mettre à jour un justificatif existant
      response = await axios.put(
        `${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/justificatifs/${replacingJustificatifId.value}/`, 
        formData, 
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );
      
      // Mettre à jour le justificatif dans la liste
      const index = justificatifs.value.findIndex(j => j.id === replacingJustificatifId.value);
      if (index !== -1) {
        justificatifs.value[index] = response.data;
      }
    } else {
      // Créer un nouveau justificatif
      response = await axios.post(
        `${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/justificatifs/`, 
        formData, 
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );
      
      // Ajouter le nouveau justificatif à la liste
      justificatifs.value.unshift(response.data);
    }
    
    closeUploadModal();
  } catch (error) {
    console.error('Erreur lors de l\'envoi du justificatif:', error);
    formError.value = error.response?.data?.detail || 'Une erreur est survenue lors de l\'envoi du justificatif';
  } finally {
    submitInProgress.value = false;
  }
};

// Filtrer les types de justificatifs disponibles (désactiver ceux déjà fournis sauf si rejeté)
const availableTypes = computed(() => {
  if (isReplacing.value) return justificatifTypes.value;
  
  return justificatifTypes.value.map(type => {
    const existingJustificatif = justificatifs.value.find(j => 
      j.type_justificatif === type.id && 
      (j.statut === 'en_attente' || j.statut === 'valide')
    );
    
    return {
      ...type,
      disabled: !!existingJustificatif,
      existingStatus: existingJustificatif ? existingJustificatif.statut : null
    };
  });
});

  // Exécuter à l'initialisation du composant
  onMounted(() => {
    fetchJustificatifs();
    fetchJustificatifTypes();
  });
  </script>
  
  <style scoped>
  .justificatifs-container {
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
    grid-template-columns: repeat(3, 1fr);
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
  
  .missing-docs-alert {
    background-color: #fffbeb;
    border: 1px solid #fcd34d;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .alert-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
  }
  
  .alert-icon {
    font-size: 1.5rem;
  }
  
  .alert-header h3 {
    margin: 0;
    color: #92400e;
    font-size: 1.2rem;
  }
  
  .missing-docs-alert p {
    margin: 0 0 1rem;
    color: #92400e;
  }
  
  .missing-docs-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .missing-doc-item {
    display: flex;
    align-items: center;
    padding: 0.75rem;
    background-color: white;
    border-radius: 6px;
    margin-bottom: 0.75rem;
  }
  
  .missing-doc-item:last-child {
    margin-bottom: 0;
  }
  
  .doc-name {
    font-weight: 600;
    color: #1F2937;
    margin-right: 1rem;
    flex: 0 0 20%;
  }
  
  .doc-description {
    color: #6B7280;
    flex: 1;
  }
  
  .upload-missing-btn {
    background-color: #0e7490;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0.5rem 0.75rem;
    font-size: 0.9rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .upload-missing-btn:hover {
    background-color: #155e75;
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
  
  .justificatifs-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .justificatif-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .justificatif-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
  }
  
  .justificatif-header {
    padding: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #E5E7EB;
  }
  
  .status-en_attente {
    background-color: #fef9c3;
  }
  
  .status-valide {
    background-color: #dcfce7;
  }
  
  .status-rejete {
    background-color: #fee2e2;
  }
  
  .justificatif-header h3 {
    margin: 0;
    font-size: 1.1rem;
    color: #1F2937;
  }
  
  .justificatif-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 600;
  }
  
  .badge-en_attente {
    background-color: #fef9c3;
    color: #854d0e;
  }
  
  .badge-valide {
    background-color: #dcfce7;
    color: #166534;
  }
  
  .badge-rejete {
    background-color: #fee2e2;
    color: #b91c1c;
  }
  
  .justificatif-details {
    padding: 1.25rem;
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
  
  .justificatif-comment {
    padding: 1.25rem;
    background-color: #f3f4f6;
    border-top: 1px solid #E5E7EB;
    border-bottom: 1px solid #E5E7EB;
  }
  
  .justificatif-comment h4 {
    margin: 0 0 0.5rem;
    font-size: 0.95rem;
    color: #374151;
  }
  
  .justificatif-comment p {
    margin: 0;
    color: #4B5563;
    font-size: 0.9rem;
  }
  
  .justificatif-actions {
    padding: 1rem;
    display: flex;
    gap: 0.75rem;
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
    text-decoration: none;
  }
  
  .view-btn {
    background-color: #f3f4f6;
    color: #1F2937;
  }
  
  .view-btn:hover {
    background-color: #e5e7eb;
  }
  
  .replace-btn {
    background-color: #dbeafe;
    color: #1e40af;
    margin-left: auto;
  }
  
  .replace-btn:hover {
    background-color: #bfdbfe;
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
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
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
  
  .mini-spinner {
    display: inline-block;
    width: 1rem;
    height: 1rem;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-left-color: white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  
  .upload-form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .form-group label {
    font-size: 0.95rem;
    font-weight: 500;
    color: #374151;
  }
  
  .form-group select {
    padding: 0.625rem;
    border: 1px solid #D1D5DB;
    border-radius: 6px;
    font-size: 0.95rem;
  }
  
  .type-description {
    margin-top: 0.5rem;
    padding: 0.75rem;
    background-color: #f3f4f6;
    border-radius: 6px;
    font-size: 0.9rem;
    color: #4B5563;
  }
  
  .file-upload-container {
    position: relative;
    border: 2px dashed #D1D5DB;
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
  }
  
  .file-upload-container:hover {
    border-color: #0e7490;
  }
  
  .file-input {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
  }
  
  .file-upload-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
  }
  
  .upload-icon {
    font-size: 2.5rem;
    color: #9CA3AF;
  }
  
  .file-upload-placeholder p {
    margin: 0;
    color: #4B5563;
  }
  
  .file-format-hint {
    font-size: 0.8rem;
    color: #6B7280;
  }
  
  .file-upload-preview {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #f3f4f6;
    padding: 0.75rem;
    border-radius: 6px;
  }
  
  .file-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  
  .file-icon {
    font-size: 1.5rem;
  }
  
  .file-details {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .file-name {
    margin: 0;
    font-weight: 500;
    color: #111827;
    font-size: 0.95rem;
  }
  
  .file-size {
    margin: 0;
    color: #6B7280;
    font-size: 0.8rem;
  }
  
  .remove-file-btn {
    background: none;
    border: none;
    font-size: 1.25rem;
    color: #6B7280;
    cursor: pointer;
    transition: color 0.3s ease;
  }
  
  .remove-file-btn:hover {
    color: #ef4444;
  }
  
  .form-error {
    color: #b91c1c;
    font-size: 0.9rem;
    margin-top: 0.5rem;
  }
  
  @media (max-width: 768px) {
    .justificatifs-container {
      padding: 1rem;
    }
    
    .header-section {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
    
    .stats-overview {
      grid-template-columns: 1fr;
    }
    
    .filters-section {
      flex-direction: column;
      gap: 1rem;
    }
    
    .justificatif-details {
      grid-template-columns: 1fr;
    }
    
    .missing-doc-item {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
    }
    
    .doc-name {
      flex: initial;
      margin-right: 0;
    }
    
    .upload-missing-btn {
      align-self: flex-end;
    }
  }

</style>