<template>
  <div class="paiements-container">
    <div class="header-section">
      <h1 class="page-title">Mes Paiements</h1>
    </div>

    <!-- Statistiques financières -->
    <div class="finance-overview">
      <div class="finance-card total-earnings">
        <div class="finance-content">
          <h3>{{ formatMontant(totalGains) }}</h3>
          <p>Revenus totaux</p>
        </div>
      </div>
      
      <div class="finance-card monthly-earnings">
        <div class="finance-content">
          <h3>{{ formatMontant(gainsCurrentMonth) }}</h3>
          <p>Revenus ce mois-ci</p>
        </div>
      </div>
      
      <div class="finance-card pending-earnings">
        <div class="finance-content">
          <h3>{{ formatMontant(gainsPending) }}</h3>
          <p>Paiements en attente</p>
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
          <option value="traite">Traité</option>
          <option value="rejete">Rejeté</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label for="filter-date">Trier par:</label>
        <select id="filter-date" v-model="sortBy">
          <option value="date">Date</option>
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

    <!-- Liste des paiements -->
    <div v-if="isLoading" class="loading-indicator">
      <div class="spinner"></div>
      <p>Chargement en cours...</p>
    </div>
    
    <div v-else-if="filteredPaiements.length === 0" class="empty-state">
      <span class="empty-icon">💸</span>
      <p>Aucun paiement ne correspond à vos critères</p>
    </div>
    
    <div v-else class="paiements-list">
      <div v-for="paiement in filteredPaiements" :key="paiement.id" class="paiement-card">
        <div class="paiement-header" :class="'status-' + paiement.statut">
          <h3>Paiement #{{ paiement.reference }}</h3>
          <div class="paiement-badge" :class="'badge-' + paiement.statut">
            {{ getStatusLabel(paiement.statut) }}
          </div>
        </div>
        
        <div class="paiement-details">
          <div class="detail-row">
            <div class="detail-item">
              <span class="detail-label">Date:</span>
              <span class="detail-value">{{ formatDate(paiement.date) }}</span>
            </div>
            
            <div class="detail-item">
              <span class="detail-label">Montant:</span>
              <span class="detail-value highlight">{{ formatMontant(paiement.montant) }}</span>
            </div>
          </div>
          
          <div class="detail-row">
            <div class="detail-item">
              <span class="detail-label">Nombre de livraisons:</span>
              <span class="detail-value">{{ paiement.livraisons?.length || 0 }} livraison(s)</span>
            </div>
            
            <div class="detail-item">
              <span class="detail-label">Commission:</span>
              <span class="detail-value">{{ formatMontant(paiement.total_commission) }}</span>
            </div>
          </div>
        </div>
        
        <div class="paiement-actions">
          <button @click="viewPaiement(paiement)" class="action-btn view-btn">
            <span class="btn-icon">👁️</span>
            Détails
          </button>
          
          <button v-if="paiement.statut === 'traite'" @click="downloadReceipt(paiement)" class="action-btn download-btn">
            <span class="btn-icon">📄</span>
            Reçu
          </button>
        </div>
      </div>
    </div>

    <!-- Graphique des revenus -->
    <div class="earnings-chart-container">
      <h2 class="section-title">Évolution des revenus</h2>
      <div class="chart-controls">
        <div class="period-selector">
          <button 
            v-for="period in chartPeriods" 
            :key="period.value" 
            @click="selectChartPeriod(period.value)"
            :class="['period-btn', { active: chartPeriod === period.value }]"
          >
            {{ period.label }}
          </button>
        </div>
      </div>
      <div class="chart-wrapper" ref="chartContainer">
        <!-- Le graphique sera rendu ici -->
        <canvas id="earningsChart" ref="earningsChart"></canvas>
      </div>
    </div>

    <!-- Modal de détails -->
    <div v-if="showDetailModal && selectedPaiement" class="modal-overlay">
      <div class="modal-container modal-large">
        <div class="modal-header">
          <h3>Détails du paiement #{{ selectedPaiement.reference }}</h3>
          <button @click="showDetailModal = false" class="close-btn">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="paiement-status">
            <div class="paiement-badge large-badge" :class="'badge-' + selectedPaiement.statut">
              {{ getStatusLabel(selectedPaiement.statut) }}
            </div>
          </div>
          
          <div class="detail-section">
            <h4>Informations générales</h4>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">Référence:</span>
                <span class="detail-value">{{ selectedPaiement.reference }}</span>
              </div>
              
              <div class="detail-item">
                <span class="detail-label">Date:</span>
                <span class="detail-value">{{ formatDate(selectedPaiement.date) }}</span>
              </div>
              
              <div class="detail-item">
                <span class="detail-label">Montant Total:</span>
                <span class="detail-value highlight">{{ formatMontant(selectedPaiement.montant) }}</span>
              </div>
              
              <div class="detail-item">
                <span class="detail-label">Commission totale:</span>
                <span class="detail-value">{{ formatMontant(selectedPaiement.total_commission) }}</span>
              </div>
              
              <div class="detail-item">
                <span class="detail-label">Nombre de livraisons:</span>
                <span class="detail-value">{{ selectedPaiement.livraisons_details?.length || 0 }}</span>
              </div>
              
              <div class="detail-item">
                <span class="detail-label">Statut:</span>
                <span class="detail-value">{{ getStatusLabel(selectedPaiement.statut) }}</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section" v-if="selectedPaiement.livraisons_details && selectedPaiement.livraisons_details.length > 0">
            <h4>Livraisons associées</h4>
            <div class="livraisons-table">
              <div class="table-header">
                <div class="th">#</div>
                <div class="th">Client</div>
                <div class="th">Date</div>
                <div class="th">Montant Net</div>
                <div class="th">Commission</div>
                <div class="th">Statut</div>
              </div>
              
              <div v-for="livraison in selectedPaiement.livraisons_details" :key="livraison.id" class="table-row">
                <div class="td">{{ livraison.id || 'N/A' }}</div>
                <div class="td">{{ livraison.client_nom || 'N/A' }}</div>
                <div class="td">{{ formatDate(livraison.date_livraison_reelle || livraison.date_livraison_prevue) }}</div>
                <div class="td highlight">{{ formatMontant(livraison.montant - livraison.commission_plateforme) }}</div>
                <div class="td">{{ formatMontant(livraison.commission_plateforme) }}</div>
                <div class="td">
                  <span class="status-pill" :class="'pill-' + livraison.statut">{{ getLivraisonStatusLabel(livraison.statut) }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <div class="commission-info">
              <p class="info-text">Note: La commission est prélevée directement par la plateforme et n'affecte pas votre paiement.</p>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="showDetailModal = false" class="cancel-action-btn">Fermer</button>
          <button v-if="selectedPaiement.statut === 'traite'" @click="downloadReceipt(selectedPaiement)" class="download-action-btn">
            <span class="btn-icon">📄</span>
            Télécharger le reçu
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { toast } from 'vue3-toastify';
import Chart from 'chart.js/auto';

const router = useRouter();
const paiements = ref([]);
const isLoading = ref(true);
const showDetailModal = ref(false);
const selectedPaiement = ref(null);
const earningsChart = ref(null);
const chartContainer = ref(null);
const chartInstance = ref(null);

// Filtres
const statusFilter = ref('all');
const sortBy = ref('date');
const orderDirection = ref('desc');
const chartPeriod = ref('month'); // 'month', 'quarter', 'year'

const chartPeriods = [
  { value: 'month', label: 'Mois' },
  { value: 'quarter', label: 'Trimestre' },
  { value: 'year', label: 'Année' }
];

// Récupérer les paiements
const fetchPaiements = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/paiements/`);
    console.log('Données de paiement reçues:', response.data); // Pour déboguer
    paiements.value = response.data;
    
    // Générer le graphique après avoir récupéré les données
    await nextTick();
    generateChart();
  } catch (error) {
    console.error('Erreur lors de la récupération des paiements:', error);
    toast("Erreur lors du chargement des paiements", {
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
  
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return 'N/A';
    
    return date.toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch (error) {
    return 'N/A';
  }
};

// Formater un montant
const formatMontant = (montant) => {
  if (montant === undefined || montant === null || isNaN(parseFloat(montant))) return '0,00 €';
  return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(parseFloat(montant));
};

// Traduction des statuts
const getStatusLabel = (status) => {
  const labels = {
    'en_attente': 'En attente',
    'traite': 'Traité',
    'rejete': 'Rejeté'
  };
  return labels[status] || status;
};

// Traduction des statuts de livraison
const getLivraisonStatusLabel = (status) => {
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

// Computed pour les paiements filtrés
const filteredPaiements = computed(() => {
  let filtered = [...paiements.value];
  
  // Filtrer par statut
  if (statusFilter.value !== 'all') {
    filtered = filtered.filter(p => p.statut === statusFilter.value);
  }
  
  // Gestion spéciale pour le tri par montant (qui est un DecimalField)
  const sortProperty = sortBy.value === 'montant' ? 'montant' : 'date';
  
  // Trier
  filtered.sort((a, b) => {
    let valueA, valueB;
    
    if (sortProperty === 'montant') {
      valueA = parseFloat(a[sortProperty] || 0);
      valueB = parseFloat(b[sortProperty] || 0);
    } else {
      valueA = new Date(a[sortProperty] || 0);
      valueB = new Date(b[sortProperty] || 0);
    }
    
    return orderDirection.value === 'asc' 
      ? valueA - valueB 
      : valueB - valueA;
  });
  
  return filtered;
});

// Computed pour le total des gains
const totalGains = computed(() => {
  return paiements.value
    .filter(p => p.statut === 'traite')
    .reduce((total, paiement) => total + parseFloat(paiement.montant || 0), 0);
});

// Computed pour les gains du mois en cours
const gainsCurrentMonth = computed(() => {
  const now = new Date();
  const currentMonth = now.getMonth();
  const currentYear = now.getFullYear();
  
  return paiements.value
    .filter(p => {
      if (!p.date) return false;
      try {
        const paiementDate = new Date(p.date);
        return p.statut === 'traite' && 
               paiementDate.getMonth() === currentMonth && 
               paiementDate.getFullYear() === currentYear;
      } catch (e) {
        return false;
      }
    })
    .reduce((total, paiement) => total + parseFloat(paiement.montant || 0), 0);
});

// Computed pour les gains en attente
const gainsPending = computed(() => {
  return paiements.value
    .filter(p => p.statut === 'en_attente')
    .reduce((total, paiement) => total + parseFloat(paiement.montant || 0), 0);
});

// Voir les détails d'un paiement
const viewPaiement = async (paiement) => {
  try {
    isLoading.value = true;
    // Récupérer les détails complets du paiement
    const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/paiements/${paiement.id}/`);
    selectedPaiement.value = response.data;
    showDetailModal.value = true;
  } catch (error) {
    console.error('Erreur lors de la récupération des détails du paiement:', error);
    toast("Erreur lors du chargement des détails", {
      type: "error",
      autoClose: 3000,
    });
  } finally {
    isLoading.value = false;
  }
};
  
// Changer la période du graphique
const selectChartPeriod = (period) => {
  chartPeriod.value = period;
  generateChart();
};

// Générer le graphique des revenus
const generateChart = () => {
  // S'assurer que l'élément canvas existe
  if (!earningsChart.value) {
    console.error("L'élément canvas pour le graphique n'existe pas");
    return;
  }

  // Détruire le graphique précédent s'il existe
  if (chartInstance.value) {
    chartInstance.value.destroy();
  }
  
  const ctx = earningsChart.value.getContext('2d');
  if (!ctx) {
    console.error("Impossible d'obtenir le contexte 2D du canvas");
    return;
  }
  
  // Préparer les données selon la période sélectionnée
  const { labels, data } = prepareChartData();
  
  // Créer le nouveau graphique
  try {
    chartInstance.value = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Revenus',
          data: data,
          backgroundColor: 'rgba(14, 116, 144, 0.2)',
          borderColor: '#0e7490',
          borderWidth: 2,
          tension: 0.4,
          fill: true,
          pointBackgroundColor: '#0e7490',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                return formatMontant(context.parsed.y);
              }
            }
          }
        },
        scales: {
          x: {
            grid: {
              display: false
            }
          },
          y: {
            beginAtZero: true,
            ticks: {
              callback: function(value) {
                return formatMontant(value);
              }
            }
          }
        }
      }
    });
  } catch (error) {
    console.error('Erreur lors de la création du graphique:', error);
  }
};

// Préparer les données pour le graphique
const prepareChartData = () => {
  // Filtrer les paiements traités uniquement
  const paiementsTraites = paiements.value.filter(p => p.statut === 'traite');
  let labels = [];
  let data = [];
  
  if (paiementsTraites.length === 0) {
    // Renvoyer des données par défaut si aucun paiement n'est disponible
    if (chartPeriod.value === 'month') {
      return { 
        labels: Array.from({length: 31}, (_, i) => (i + 1).toString()), 
        data: Array(31).fill(0) 
      };
    } else if (chartPeriod.value === 'quarter') {
      return { 
        labels: Array.from({length: 13}, (_, i) => `S${i + 1}`), 
        data: Array(13).fill(0) 
      };
    } else if (chartPeriod.value === 'year') {
      return { 
        labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'], 
        data: Array(12).fill(0) 
      };
    }
    return { labels: [], data: [] };
  }
  
  const now = new Date();
  
  if (chartPeriod.value === 'month') {
    // Données pour le mois en cours (par jour)
    const currentMonth = now.getMonth();
    const currentYear = now.getFullYear();
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
    
    // Initialiser les données pour chaque jour du mois
    for (let day = 1; day <= daysInMonth; day++) {
      labels.push(day.toString());
      data.push(0);
    }
    
    // Ajouter les paiements
    paiementsTraites.forEach(paiement => {
      try {
        const paiementDate = new Date(paiement.date);
        if (paiementDate.getMonth() === currentMonth && paiementDate.getFullYear() === currentYear) {
          const day = paiementDate.getDate() - 1; // Array est 0-indexed
          if (day >= 0 && day < data.length) {
            data[day] += parseFloat(paiement.montant || 0);
          }
        }
      } catch (e) {
        console.error('Erreur lors du traitement de la date du paiement:', e);
      }
    });
  } else if (chartPeriod.value === 'quarter') {
    // Données pour le trimestre en cours (par semaine)
    const currentQuarter = Math.floor(now.getMonth() / 3);
    const currentYear = now.getFullYear();
    const startMonth = currentQuarter * 3;
    
    // Créer des labels pour les semaines du trimestre (environ 13)
    for (let week = 1; week <= 13; week++) {
      labels.push(`S${week}`);
      data.push(0);
    }
    
    // Ajouter les paiements
    paiementsTraites.forEach(paiement => {
      try {
        const paiementDate = new Date(paiement.date);
        const paiementMonth = paiementDate.getMonth();
        if (paiementDate.getFullYear() === currentYear && 
            Math.floor(paiementMonth / 3) === currentQuarter) {
          // Calculer la semaine approximative dans le trimestre
          const monthOffset = paiementMonth - startMonth;
          const weekInMonth = Math.floor(paiementDate.getDate() / 7);
          const weekInQuarter = monthOffset * 4 + weekInMonth;
          if (weekInQuarter >= 0 && weekInQuarter < 13) {
            data[weekInQuarter] += parseFloat(paiement.montant || 0);
          }
        }
      } catch (e) {
        console.error('Erreur lors du traitement de la date du paiement:', e);
      }
    });
  } else if (chartPeriod.value === 'year') {
    // Données pour l'année en cours (par mois)
    const currentYear = now.getFullYear();
    const months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'];
    
    labels = [...months];
    data = Array(12).fill(0);
    
    // Ajouter les paiements
    paiementsTraites.forEach(paiement => {
      try {
        const paiementDate = new Date(paiement.date);
        if (paiementDate.getFullYear() === currentYear) {
          const month = paiementDate.getMonth();
          if (month >= 0 && month < 12) {
            data[month] += parseFloat(paiement.montant || 0);
          }
        }
      } catch (e) {
        console.error('Erreur lors du traitement de la date du paiement:', e);
      }
    });
  }
  
  return { labels, data };
};

// Télécharger le reçu
const downloadReceipt = async (paiement) => {
  try {
    // Show loading toast
    const toastId = toast("Génération du reçu en cours...", {
      type: "info",
      autoClose: false,
    });
    
    // Make API request to get PDF
    const response = await axios.get(
      `${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/paiements/${paiement.id}/receipt/`,
      { responseType: 'blob' }
    );
    
    // Create a URL for the blob
    const url = window.URL.createObjectURL(new Blob([response.data]));
    
    // Create temp link element to trigger download
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `recu_paiement_${paiement.reference}.pdf`);
    document.body.appendChild(link);
    
    // Trigger download and clean up
    link.click();
    window.URL.revokeObjectURL(url);
    link.remove();
    
    // Update toast
    toast.update(toastId, {
      render: "Reçu téléchargé avec succès!",
      type: "success",
      autoClose: 3000,
    });
  } catch (error) {
    console.error('Erreur lors du téléchargement du reçu:', error);
    toast("Erreur lors de la génération du reçu", {
      type: "error",
      autoClose: 3000,
    });
  }
};

// Observer les changements de dimensions du conteneur
const resizeChart = () => {
  if (chartInstance.value) {
    chartInstance.value.resize();
  }
};

// Surveiller les changements de filtres pour mettre à jour le graphique
watch([chartPeriod], () => {
  generateChart();
});

// Exécuter à l'initialisation du composant
onMounted(async () => {
  await fetchPaiements();
  
  // Configurer l'observateur de redimensionnement
  if (window.ResizeObserver) {
    const resizeObserver = new ResizeObserver(resizeChart);
    if (chartContainer.value) {
      resizeObserver.observe(chartContainer.value);
    }
    
    // Nettoyer l'observateur quand le composant est détruit
    return () => {
      if (chartInstance.value) {
        chartInstance.value.destroy();
      }
      resizeObserver.disconnect();
    };
  }
});
</script>

<style scoped>
.paiements-container {
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

.finance-overview {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.finance-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.finance-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.finance-content h3 {
  font-size: 2.2rem;
  margin: 0 0 0.5rem;
  color: #0A1128;
}

.finance-content p {
  margin: 0;
  color: #6B7280;
  font-size: 1.1rem;
}

.total-earnings {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
}

.total-earnings h3 {
  color: #166534;
}

.monthly-earnings {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
}

.monthly-earnings h3 {
  color: #1e40af;
}

.pending-earnings {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
}

.pending-earnings h3 {
  color: #0c4a6e;
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
  border: 1px solid #D1D5DB;border-radius: 6px;
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
  margin-bottom: 2rem;
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

.paiements-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.paiement-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.paiement-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.paiement-header {
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #E5E7EB;
}

.status-en_attente {
  background-color: #f0f9ff;
}

.status-traite {
  background-color: #f0fdf4;
}

.status-rejete {
  background-color: #fef2f2;
}

.paiement-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #1F2937;
}

.paiement-badge {
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
  background-color: #e0f2fe;
  color: #0c4a6e;
}

.badge-traite {
  background-color: #dcfce7;
  color: #166534;
}

.badge-rejete {
  background-color: #fee2e2;
  color: #b91c1c;
}

.paiement-details {
  padding: 1.25rem;
}

.detail-row {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
}

.detail-row:last-child {
  margin-bottom: 0;
}

.detail-item {
  flex: 1;
}

.full-width {
  flex: 0 0 100%;
}

.detail-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #4B5563;
  display: block;
  margin-bottom: 0.25rem;
}

.detail-value {
  font-size: 1rem;
  color: #1F2937;
}

.highlight {
  font-weight: 600;
  color: #0e7490;
}

.paiement-actions {
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

.download-btn {
  background-color: #dbeafe;
  color: #1e40af;
  margin-left: auto;
}

.download-btn:hover {
  background-color: #bfdbfe;
}

.earnings-chart-container {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.section-title {
  margin: 0 0 1.5rem;
  font-size: 1.5rem;
  color: #0A1128;
}

.chart-controls {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1.5rem;
}

.period-selector {
  display: flex;
  gap: 0.5rem;
  background-color: #f3f4f6;
  padding: 0.25rem;
  border-radius: 8px;
}

.period-btn {
  padding: 0.5rem 1rem;
  border: none;
  background: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  color: #4B5563;
  cursor: pointer;
  transition: all 0.3s ease;
}

.period-btn:hover {
  background-color: #e5e7eb;
}

.period-btn.active {
  background-color: #0e7490;
  color: white;
}

.chart-wrapper {
  height: 300px;
  position: relative;
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
  align-items: center;
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

.download-action-btn {
  padding: 0.625rem 1.25rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: #2563eb;
  color: white;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.download-action-btn:hover {
  background-color: #1d4ed8;
}

.paiement-status {
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
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.livraisons-table {
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  overflow: hidden;
}

.table-header {
  display: grid;
  grid-template-columns: 0.5fr 2fr 1.5fr 1fr 1fr 1fr;
  background-color: #F9FAFB;
  border-bottom: 1px solid #E5E7EB;
}

.table-row {
  display: grid;
  grid-template-columns: 0.5fr 2fr 1.5fr 1fr 1fr 1fr;
  border-bottom: 1px solid #E5E7EB;
}

.table-row:last-child {
  border-bottom: none;
}

.th, .td {
  padding: 0.75rem;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
}

.th {
  font-weight: 600;
  color: #4B5563;
}

.status-pill {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  text-align: center;
}

.pill-en_attente {
  background-color: #fef9c3;
  color: #854d0e;
}

.pill-confirmee {
  background-color: #e0f2fe;
  color: #0c4a6e;
}

.pill-en_preparation {
  background-color: #f0fdf4;
  color: #166534;
}

.pill-en_cours {
  background-color: #dbeafe;
  color: #1e40af;
}

.pill-livree {
  background-color: #dcfce7;
  color: #166534;
}

.pill-annulee {
  background-color: #fee2e2;
  color: #b91c1c;
}

.commission-info {
  background-color: #f0f9ff;
  border-left: 4px solid #0e7490;
  padding: 1rem;
  border-radius: 0 6px 6px 0;
}

.info-text {
  margin: 0;
  font-size: 0.9rem;
  color: #0c4a6e;
}

@media (max-width: 768px) {
  .paiements-container {
    padding: 1rem;
  }
  
  .finance-overview {
    grid-template-columns: 1fr;
  }
  
  .filters-section {
    flex-direction: column;
    gap: 1rem;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
  
  .table-header, .table-row {
    grid-template-columns: 0.5fr 1.5fr 1fr 1fr 1fr 1fr;
  }
  
  .period-selector {
    width: 100%;
    justify-content: space-between;
  }
  
  .period-btn {
    flex: 1;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .detail-row {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .table-header, .table-row {
    grid-template-columns: 0.5fr 1.5fr 1fr 1fr;
  }
  
  .th:nth-child(5), .td:nth-child(5),
  .th:nth-child(6), .td:nth-child(6) {
    display: none;
  }
  
  .paiement-actions {
    flex-wrap: wrap;
  }
  
  .download-btn {
    margin-left: 0;
  }
  
  .modal-footer {
    flex-direction: column;
    gap: 1rem;
  }
  
  .download-action-btn {
    width: 100%;
    justify-content: center;
  }
}

</style>