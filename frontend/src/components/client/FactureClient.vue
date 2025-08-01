<!-- ConfirmerLivraison.vue - Pour les livreurs -->
<template>
  <div class="confirmer-livraison">
    <div v-if="livraison" class="livraison-card">
      
      <!-- Header -->
      <div class="card-header">
        <h3>🚚 Livraison #{{ livraison.id }}</h3>
        <div class="statut" :class="livraison.statut">
          <span class="badge">{{ livraison.statut_display }}</span>
        </div>
      </div>

      <!-- Détails de la livraison -->
      <div class="details">
        <div v-if="livraison.trajet_info" class="trajet">
          <h4>📍 Itinéraire</h4>
          <div class="route">
            <span class="point">{{ livraison.trajet_info.depart }}</span>
            <span class="arrow">→</span>
            <span class="point">{{ livraison.trajet_info.arrivee }}</span>
          </div>
          <div class="date">
            🕒 {{ formatDate(livraison.trajet_info.date_depart) }}
          </div>
        </div>

        <div v-if="livraison.client" class="client-info">
          <h4>👤 Client</h4>
          <p>{{ livraison.client.nom || 'Client' }}</p>
        </div>
      </div>

      <!-- Étapes de livraison -->
      <div class="etapes">
        <div class="etape" :class="{ completed: isEtapeComplete('en_cours') }">
          <span class="numero">1</span>
          <span class="texte">En cours de livraison</span>
        </div>
        <div class="etape" :class="{ completed: livraison.statut === 'livree', active: livraison.statut === 'en_cours' }">
          <span class="numero">2</span>
          <span class="texte">Confirmer la livraison</span>
        </div>
        <div class="etape" :class="{ completed: paiementEffectue }">
          <span class="numero">3</span>
          <span class="texte">Recevoir le paiement</span>
        </div>
      </div>

      <!-- Actions selon le statut -->
      <div class="actions">
        <!-- Si en cours, peut confirmer -->
        <div v-if="livraison.statut === 'en_cours'">
          <div class="action-info">
            <h4>✅ Livraison effectuée ?</h4>
            <p>Confirmez que vous avez bien livré le colis au client</p>
          </div>
          <button @click="confirmerLivraison" class="btn-confirmer" :disabled="loading">
            <span v-if="loading">
              <div class="mini-spinner"></div>
              Confirmation...
            </span>
            <span v-else>
              ✅ J'ai livré le colis
            </span>
          </button>
        </div>

        <!-- Si livré, en attente paiement -->
        <div v-else-if="livraison.statut === 'livree' && !paiementEffectue">
          <div class="success-info">
            <h4>✅ Livraison confirmée !</h4>
            <p>Le client a été notifié et peut maintenant procéder au paiement.</p>
            <div class="timing">
              <span class="icon">⏰</span>
              <span>Le client a 7 jours pour payer</span>
            </div>
          </div>
          <div class="gain-prevu">
            <span class="label">Gain prévu :</span>
            <span class="montant">{{ calculerGainLivreur() }}€</span>
            <small>(après commission 10%)</small>
          </div>
        </div>
        
        <!-- Si payé -->
        <div v-else-if="paiementEffectue">
          <div class="paiement-recu">
            <h4>💰 Paiement reçu !</h4>
            <p>Le client a payé. Vous avez reçu votre paiement.</p>
            <div class="montant-recu">
              {{ calculerGainLivreur() }}€
            </div>
          </div>
        </div>

        <!-- Autres statuts -->
        <div v-else>
          <div class="info-attente">
            <p>Livraison en préparation...</p>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'FactureClient', 
  props: {
    livraisonId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      livraison: null,
      loading: false,
      paiementEffectue: false
    }
  },
  mounted() {
    this.chargerLivraison()
    // Vérifier le paiement toutes les 30 secondes
    this.intervalId = setInterval(this.verifierPaiement, 30000)
  },
  beforeUnmount() {
    if (this.intervalId) {
      clearInterval(this.intervalId)
    }
  },
  methods: {
    async chargerLivraison() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL_API}/api/livreurs/livraisons/${this.livraisonId}/`)
        this.livraison = response.data
        await this.verifierPaiement()
      } catch (error) {
        console.error('Erreur chargement livraison:', error)
      }
    },

    async confirmerLivraison() {
      this.loading = true
      try {
        const response = await axios.post(`${import.meta.env.VITE_APP_BASE_URL_API}/api/confirmer-livraison/${this.livraisonId}/`)
        
        if (response.data.success) {
          // Actualiser les données
          await this.chargerLivraison()
          
          // Afficher le succès
          alert('✅ Livraison confirmée ! Le client a été notifié et peut maintenant payer.')
        }
      } catch (error) {
        console.error('Erreur confirmation:', error)
        alert('Erreur lors de la confirmation: ' + (error.response?.data?.error || error.message))
      }
      this.loading = false
    },

    async verifierPaiement() {
      if (!this.livraison || this.livraison.statut !== 'livree') return
      
      try {
        // Vérifier si une facture payée existe pour cette livraison
        const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL_API}/api/mes-gains/`)
        const paiements = response.data.paiements || []
        
        // Chercher un paiement pour cette livraison
        this.paiementEffectue = paiements.some(p => 
          p.livraison_id === this.livraison.id && p.statut === 'complete'
        )
      } catch (error) {
        console.error('Erreur vérification paiement:', error)
      }
    },

    calculerGainLivreur() {
      if (!this.livraison?.trajet_annonce?.montant) return 0
      const montantTotal = parseFloat(this.livraison.trajet_annonce.montant)
      const commission = montantTotal * 0.10
      return (montantTotal - commission).toFixed(2)
    },

    isEtapeComplete(statutRequis) {
      const statuts = ['en_attente', 'confirmee', 'en_preparation', 'en_cours', 'livree']
      const indexActuel = statuts.indexOf(this.livraison?.statut)
      const indexRequis = statuts.indexOf(statutRequis)
      return indexActuel >= indexRequis
    },

    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.confirmer-livraison {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.livraison-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e9ecef;
}

/* Header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e9ecef;
}

.card-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.4rem;
}

.badge {
  padding: 8px 16px;
  border-radius: 25px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
}

.statut.en_cours .badge {
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
}

.statut.livree .badge {
  background: linear-gradient(135deg, #28a745, #1e7e34);
  color: white;
}

/* Détails */
.details {
  margin-bottom: 24px;
}

.trajet, .client-info {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 16px;
}

.trajet h4, .client-info h4 {
  margin: 0 0 12px 0;
  color: #495057;
  font-size: 1rem;
}

.route {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.point {
  background: white;
  padding: 8px 12px;
  border-radius: 8px;
  color: #495057;
  font-weight: 500;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.arrow {
  color: #007bff;
  font-weight: bold;
  font-size: 1.2rem;
}

.date {
  color: #6c757d;
  font-size: 0.9rem;
}

/* Étapes */
.etapes {
  display: flex;
  justify-content: space-between;
  margin-bottom: 32px;
  padding: 20px 0;
  position: relative;
}

.etapes::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 15%;
  right: 15%;
  height: 2px;
  background: #e9ecef;
  z-index: 1;
}

.etape {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  position: relative;
  z-index: 2;
  flex: 1;
}

.numero {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e9ecef;
  color: #6c757d;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  border: 3px solid white;
}

.etape.completed .numero {
  background: #28a745;
  color: white;
}

.etape.active .numero {
  background: #007bff;
  color: white;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.texte {
  text-align: center;
  font-size: 0.85rem;
  color: #6c757d;
  font-weight: 500;
}

.etape.completed .texte {
  color: #28a745;
}

.etape.active .texte {
  color: #007bff;
}

/* Actions */
.actions {
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  padding: 24px;
  border-radius: 12px;
}

.action-info h4 {
  margin: 0 0 8px 0;
  color: #2c3e50;
}

.action-info p {
  margin: 0 0 20px 0;
  color: #6c757d;
}

.btn-confirmer {
  width: 100%;
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  border: none;
  padding: 16px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-confirmer:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(40, 167, 69, 0.3);
}

.btn-confirmer:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.mini-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #ffffff;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Success info */
.success-info h4 {
  margin: 0 0 12px 0;
  color: #28a745;
}

.success-info p {
  margin: 0 0 16px 0;
  color: #6c757d;
}

.timing {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #fd7e14;
  font-weight: 500;
}

.gain-prevu {
  background: white;
  padding: 16px;
  border-radius: 8px;
  margin-top: 16px;
  text-align: center;
  border: 2px solid #28a745;
}

.gain-prevu .label {
  color: #6c757d;
  font-size: 0.9rem;
}

.gain-prevu .montant {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #28a745;
  margin: 4px 0;
}

.gain-prevu small {
  color: #6c757d;
  font-size: 0.8rem;
}

/* Paiement reçu */
.paiement-recu {
  text-align: center;
}

.paiement-recu h4 {
  margin: 0 0 12px 0;
  color: #28a745;
  font-size: 1.2rem;
}

.paiement-recu p {
  margin: 0 0 16px 0;
  color: #6c757d;
}

.montant-recu {
  font-size: 2rem;
  font-weight: 700;
  color: #28a745;
  background: white;
  padding: 16px;
  border-radius: 12px;
  border: 2px solid #28a745;
}

/* Info attente */
.info-attente {
  text-align: center;
  color: #6c757d;
}

/* Responsive */
@media (max-width: 768px) {
  .etapes {
    flex-direction: column;
    gap: 16px;
  }
  
  .etapes::before {
    display: none;
  }
  
  .route {
    flex-direction: column;
    gap: 8px;
  }
  
  .arrow {
    transform: rotate(90deg);
  }
}
</style>