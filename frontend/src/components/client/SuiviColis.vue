<template>
  <div class="mes-livraisons">
    <!-- Header avec animation -->
    <div class="header">
      <h2>📦 Mes Livraisons</h2>
      <div class="stats" v-if="!loading && livraisons.length > 0">
        <span class="total">{{ livraisons.length }} livraison{{ livraisons.length > 1 ? 's' : '' }}</span>
      </div>
    </div>

    <!-- Loading avec spinner -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Chargement...</p>
    </div>
    
    <div v-else>
      <!-- Grid des livraisons -->
      <div class="livraisons-grid">
        <div 
          v-for="livraison in livraisons" 
          :key="livraison.id" 
          class="livraison-card"
          :class="{ 'completed': livraison.statut === 'livree' }"
        >
          
          <!-- Header de la card -->
          <div class="card-header">
            <div class="numero">
              <span class="icon">📦</span>
              <strong>#{{ livraison.id }}</strong>
            </div>
            <div class="statut" :class="livraison.statut">
              <span class="badge">
                <i class="status-icon" :class="getStatusIcon(livraison.statut)"></i>
                {{ livraison.statut_display }}
              </span>
            </div>
          </div>

          <!-- Trajet avec design moderne -->
          <div v-if="livraison.trajet_info" class="trajet">
            <div class="route">
              <span class="location">
                📍 {{ livraison.trajet_info.depart }}
              </span>
              <div class="arrow">→</div>
              <span class="location">
                🎯 {{ livraison.trajet_info.arrivee }}
              </span>
            </div>
            <div class="date">
              🕒 {{ formatDate(livraison.trajet_info.date_depart) }}
            </div>
          </div>

          <!-- Livreur avec avatar -->
          <div class="livreur">
            <div class="avatar">{{ getInitials(livraison.livreur_nom) }}</div>
            <div class="name">
              <strong>{{ livraison.livreur_nom }}</strong>
              <small>Votre livreur</small>
            </div>
          </div>

          <!-- Message du livreur -->
          <div v-if="livraison.commentaire_livreur" class="message">
            <div class="message-header">
              💬 Message du livreur
            </div>
            <p>{{ livraison.commentaire_livreur }}</p>
          </div>

          <!-- Progress bar pour les statuts en cours -->
          <div v-if="isInProgress(livraison.statut)" class="progress">
            <div class="progress-bar" :style="{ width: getProgress(livraison.statut) + '%' }"></div>
          </div>

        </div>
      </div>

      <!-- État vide avec illustration -->
      <div v-if="livraisons.length === 0" class="vide">
        <div class="empty-icon">📭</div>
        <h3>Aucune livraison</h3>
        <p>Vous n'avez pas encore de livraisons en cours</p>
      </div>
      
      <!-- Bouton actualiser moderne -->
      <button @click="actualiser" class="btn-actualiser" :disabled="loading">
        <span class="btn-icon">🔄</span>
        Actualiser
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MesLivraisons',
  data() {
    return {
      livraisons: [],
      loading: false
    }
  },
  mounted() {
    this.charger()
  },
  methods: {
    async charger() {
      this.loading = true
      try {
        const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL_API}/api/mes-livraisons/`)
        this.livraisons = response.data
      } catch (error) {
        console.error('Erreur:', error)
      }
      this.loading = false
    },
    
    actualiser() {
      this.charger()
    },
    
    formatDate(dateStr) {
      const date = new Date(dateStr)
      return date.toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    getInitials(name) {
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
    },

    getStatusIcon(statut) {
      const icons = {
        'en_attente': '⏳',
        'confirmee': '✅',
        'en_preparation': '📦',
        'en_cours': '🚚',
        'livree': '🎉',
        'annulee': '❌'
      }
      return icons[statut] || '📦'
    },

    isInProgress(statut) {
      return ['confirmee', 'en_preparation', 'en_cours'].includes(statut)
    },

    getProgress(statut) {
      const progress = {
        'en_attente': 10,
        'confirmee': 25,
        'en_preparation': 50,
        'en_cours': 80,
        'livree': 100,
        'annulee': 0
      }
      return progress[statut] || 0
    }
  }
}
</script>

<style scoped>
.mes-livraisons {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Header moderne */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px 0;
}

.header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stats {
  background: #f8f9fa;
  padding: 8px 16px;
  border-radius: 20px;
  color: #6c757d;
  font-weight: 500;
}

/* Loading avec spinner */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 20px;
  color: #6c757d;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Grid responsive */
.livraisons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

/* Cards modernes */
.livraison-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.livraison-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.livraison-card.completed {
  border-left: 4px solid #28a745;
}

.livraison-card.completed::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 40px 40px 0;
  border-color: transparent #28a745 transparent transparent;
}

/* Header de card */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.numero {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.1rem;
}

.icon {
  font-size: 1.2rem;
}

/* Statuts colorés */
.statut {
  margin: 0;
}

.badge {
  padding: 8px 16px;
  border-radius: 25px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.statut.en_attente .badge {
  background: linear-gradient(135deg, #ffc107, #ffb300);
  color: #212529;
}

.statut.confirmee .badge {
  background: linear-gradient(135deg, #17a2b8, #138496);
  color: white;
}

.statut.en_preparation .badge {
  background: linear-gradient(135deg, #fd7e14, #e55a00);
  color: white;
}

.statut.en_cours .badge {
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
}

.statut.livree .badge {
  background: linear-gradient(135deg, #28a745, #1e7e34);
  color: white;
}

.statut.annulee .badge {
  background: linear-gradient(135deg, #dc3545, #c82333);
  color: white;
}

/* Trajet design */
.trajet {
  margin: 20px 0;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 12px;
  border-left: 4px solid #667eea;
}

.route {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.location {
  font-weight: 500;
  color: #495057;
  padding: 4px 8px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.arrow {
  font-size: 1.2rem;
  color: #667eea;
  font-weight: bold;
}

.date {
  color: #6c757d;
  font-size: 0.9rem;
  font-weight: 500;
}

/* Livreur avec avatar */
.livreur {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 20px 0;
  padding: 12px;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  border-radius: 12px;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.9rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.name strong {
  display: block;
  color: #2c3e50;
  margin-bottom: 2px;
}

.name small {
  color: #6c757d;
  font-size: 0.8rem;
}

/* Messages */
.message {
  background: linear-gradient(135deg, #e3f2fd, #f3e5f5);
  padding: 16px;
  border-radius: 12px;
  margin: 16px 0;
  border-left: 4px solid #2196f3;
}

.message-header {
  font-weight: 600;
  color: #1976d2;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.message p {
  margin: 0;
  color: #424242;
  line-height: 1.5;
}

/* Progress bar */
.progress {
  height: 6px;
  background: #e9ecef;
  border-radius: 3px;
  margin-top: 16px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 3px;
  transition: width 0.3s ease;
  animation: progress-glow 2s ease-in-out infinite alternate;
}

@keyframes progress-glow {
  0% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.4); }
  100% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.8); }
}

/* État vide */
.vide {
  text-align: center;
  padding: 80px 20px;
  color: #6c757d;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
  opacity: 0.7;
}

.vide h3 {
  margin: 0 0 12px 0;
  color: #495057;
}

.vide p {
  margin: 0;
  font-size: 1.1rem;
}

/* Bouton moderne */
.btn-actualiser {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 14px 28px;
  border-radius: 50px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 30px auto 0;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-actualiser:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(102, 126, 234, 0.4);
}

.btn-actualiser:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-icon {
  font-size: 1.1rem;
  animation: rotate 2s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .livraisons-grid {
    grid-template-columns: 1fr;
  }
  
  .route {
    flex-direction: column;
    gap: 8px;
  }
  
  .arrow {
    transform: rotate(90deg);
  }
  
  .header {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
}
</style>