<template>
    <div class="services-page">
      <!-- Hero Section -->
      <section class="services-hero">
        <div class="container">
          <div class="services-hero-content">
            <h1 class="services-title">Nos Services</h1>
            <p class="services-subtitle">Des solutions de livraison collaboratives, écologiques et adaptées à vos besoins</p>
          </div>
        </div>
        <div class="wave-divider">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 100">
            <path fill="#ffffff" fill-opacity="1" 
              d="M0,64L60,69.3C120,75,240,85,360,80C480,75,600,53,720,48C840,43,960,53,1080,58.7C1200,64,1320,64,1380,64L1440,64L1440,100L1380,100C1320,100,1200,100,1080,100C960,100,840,100,720,100C600,100,480,100,360,100C240,100,120,100,60,100L0,100Z">
            </path>
          </svg>
        </div>
      </section>
  
      <!-- Tabs Navigation Section -->
      <section class="services-tabs">
        <div class="container">
          <div class="tabs-container">
            <button 
              v-for="(category, index) in serviceCategories" 
              :key="index"
              class="tab-button" 
              :class="{ 'active': activeTab === index }"
              @click="activeTab = index">
              <i :class="category.icon"></i>
              <span>{{ category.title }}</span>
            </button>
          </div>
        </div>
      </section>
  
      <!-- Services Content Section -->
      <section class="services-content">
        <div class="container">
          <!-- Livraison de colis -->
          <div v-if="activeTab === 0" class="tab-content">
            <div class="tab-header">
              <div class="tab-icon">
                <i class="fas fa-box"></i>
              </div>
              <div class="tab-title">
                <h2>Livraison de colis</h2>
                <p>Envoyez vos colis partout en France grâce à notre réseau de livreurs particuliers</p>
              </div>
            </div>
            
            <div class="services-grid">
              <div class="service-card">
                <div class="service-card-icon">
                  <i class="fas fa-route"></i>
                </div>
                <h3>Livraison de ville à ville</h3>
                <p>Expédiez vos colis d'une ville à une autre via des livreurs qui effectuent déjà ce trajet.</p>
                <div class="service-features">
                  <div class="feature">
                    <i class="fas fa-leaf"></i>
                    <span>Écologique</span>
                  </div>
                  <div class="feature">
                    <i class="fas fa-wallet"></i>
                    <span>Économique</span>
                  </div>
                  <div class="feature">
                    <i class="fas fa-tachometer-alt"></i>
                    <span>Rapide</span>
                  </div>
                </div>
              </div>
              
              <div class="service-card">
                <div class="service-card-icon">
                  <i class="fas fa-truck"></i>
                </div>
                <h3>Livraison porte-à-porte</h3>
                <p>Faites livrer vos colis directement de votre adresse à celle du destinataire.</p>
                <div class="service-features">
                  <div class="feature">
                    <i class="fas fa-clock"></i>
                    <span>Sur-mesure</span>
                  </div>
                  <div class="feature">
                    <i class="fas fa-map-marker-alt"></i>
                    <span>Suivi GPS</span>
                  </div>
                  <div class="feature">
                    <i class="fas fa-shield-alt"></i>
                    <span>Sécurisé</span>
                  </div>
                </div>
              </div>
              
              <div class="service-card">
                <div class="service-card-icon">
                  <i class="fas fa-box-open"></i>
                </div>
                <h3>Livraison collaborative</h3>
                <p>Plusieurs livreurs se relaient pour acheminer votre colis sur de longues distances.</p>
                <div class="service-features">
                  <div class="feature">
                    <i class="fas fa-users"></i>
                    <span>Communautaire</span>
                  </div>
                  <div class="feature">
                    <i class="fas fa-euro-sign"></i>
                    <span>Prix réduit</span>
                  </div>
                  <div class="feature">
                    <i class="fas fa-road"></i>
                    <span>Longue distance</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Lâcher de chariot -->
          <div v-if="activeTab === 1" class="tab-content">
            <div class="tab-header">
              <div class="tab-icon">
                <i class="fas fa-shopping-basket"></i>
              </div>
              <div class="tab-title">
                <h2>Lâcher de chariot</h2>
                <p>Faites vos courses chez nos commerçants partenaires et faites-vous livrer à domicile</p>
              </div>
            </div>
            
            <div class="services-grid">
              <div class="service-card">
                <div class="service-card-icon">
                  <i class="fas fa-store"></i>
                </div>
                <h3>Courses alimentaires</h3>
                <p>Faites vos courses dans nos commerces partenaires et rentrez librement pendant qu'on vous livre.</p>
                <div class="service-partners">
                  <span>Partenaires :</span> Carrefour, Monoprix, Auchan, ...
                </div>
              </div>
              
              <div class="service-card">
                <div class="service-card-icon">
                  <i class="fas fa-shopping-bag"></i>
                </div>
                <h3>Shopping en boutique</h3>
                <p>Profitez de vos achats en boutique sans vous encombrer de sacs et paquets.</p>
                <div class="service-partners">
                  <span>Partenaires :</span> Galeries Lafayette, FNAC, Décathlon, ...
                </div>
              </div>
              
              <div class="service-card">
                <div class="service-card-icon">
                  <i class="fas fa-gift"></i>
                </div>
                <h3>Livraison de cadeaux</h3>
                <p>Achetez un cadeau en magasin et faites-le livrer directement chez la personne de votre choix.</p>
                <div class="service-features">
                  <div class="feature">
                    <i class="fas fa-gift"></i>
                    <span>Emballage cadeau</span>
                  </div>
                  <div class="feature">
                    <i class="fas fa-envelope"></i>
                    <span>Message personnalisé</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="how-it-works">
              <h3>Comment ça marche ?</h3>
              <div class="steps">
                <div class="step">
                  <div class="step-number">1</div>
                  <div class="step-content">
                    <h4>Faites vos courses normalement</h4>
                    <p>Rendez-vous dans l'un de nos commerces partenaires et faites vos achats</p>
                  </div>
                </div>
                <div class="step">
                  <div class="step-number">2</div>
                  <div class="step-content">
                    <h4>Demandez le service en caisse</h4>
                    <p>Indiquez simplement au caissier que vous souhaitez utiliser le service EcoDeli</p>
                  </div>
                </div>
                <div class="step">
                  <div class="step-number">3</div>
                  <div class="step-content">
                    <h4>Choisissez votre créneau</h4>
                    <p>Sélectionnez l'horaire qui vous convient pour la livraison</p>
                  </div>
                </div>
                <div class="step">
                  <div class="step-number">4</div>
                  <div class="step-content">
                    <h4>Rentrez les mains libres</h4>
                    <p>Partez sans vos courses et recevez-les à l'heure choisie chez vous</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Services à la personne -->
          <div v-if="activeTab === 2" class="tab-content">
            <div class="tab-header">
              <div class="tab-icon">
                <i class="fas fa-hands-helping"></i>
              </div>
              <div class="tab-title">
                <h2>Services à la personne</h2>
                <p>Transport quotidien, courses, accompagnement... Profitez de services personnalisés</p>
              </div>
            </div>
            
            <div class="service-categories">
              <div class="service-category">
                <h3>Transport de personnes</h3>
                <div class="services-grid">
                  <div class="service-card">
                    <div class="service-card-icon">
                      <i class="fas fa-user-friends"></i>
                    </div>
                    <h3>Transport quotidien</h3>
                    <p>Bénéficiez d'un accompagnement régulier pour vos trajets (médecin, courses, etc.).</p>
                    <div class="service-features">
                      <div class="feature">
                        <i class="fas fa-calendar-alt"></i>
                        <span>Régulier ou ponctuel</span>
                      </div>
                      <div class="feature">
                        <i class="fas fa-user-check"></i>
                        <span>Accompagnateurs vérifiés</span>
                      </div>
                    </div>
                  </div>
                  
                  <div class="service-card">
                    <div class="service-card-icon">
                      <i class="fas fa-plane"></i>
                    </div>
                    <h3>Transfert aéroport</h3>
                    <p>Faites-vous accompagner pour aller à l'aéroport ou en revenir.</p>
                    <div class="service-features">
                      <div class="feature">
                        <i class="fas fa-clock"></i>
                        <span>7j/7, 24h/24</span>
                      </div>
                      <div class="feature">
                        <i class="fas fa-luggage-cart"></i>
                        <span>Aide aux bagages</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="service-category">
                <h3>Aide à domicile</h3>
                <div class="services-grid">
                  <div class="service-card">
                    <div class="service-card-icon">
                      <i class="fas fa-shopping-cart"></i>
                    </div>
                    <h3>Courses à domicile</h3>
                    <p>Un livreur EcoDeli effectue vos courses selon votre liste et vous les livre.</p>
                    <div class="service-features">
                      <div class="feature">
                        <i class="fas fa-list-alt"></i>
                        <span>Selon votre liste</span>
                      </div>
                      <div class="feature">
                        <i class="fas fa-hand-holding-usd"></i>
                        <span>Prix transparent</span>
                      </div>
                    </div>
                  </div>
                  
                  <div class="service-card">
                    <div class="service-card-icon">
                      <i class="fas fa-broom"></i>
                    </div>
                    <h3>Petits travaux</h3>
                    <p>Bénéficiez d'une aide pour le ménage, le jardinage ou de petites réparations.</p>
                    <div class="service-features">
                      <div class="feature">
                        <i class="fas fa-certificate"></i>
                        <span>Personnel qualifié</span>
                      </div>
                      <div class="feature">
                        <i class="fas fa-thumbs-up"></i>
                        <span>Satisfaction garantie</span>
                      </div>
                    </div>
                  </div>
                  
                  <div class="service-card">
                    <div class="service-card-icon">
                      <i class="fas fa-paw"></i>
                    </div>
                    <h3>Garde d'animaux</h3>
                    <p>Un prestataire s'occupe de vos animaux pendant votre absence.</p>
                    <div class="service-features">
                      <div class="feature">
                        <i class="fas fa-heart"></i>
                        <span>Amoureux des animaux</span>
                      </div>
                      <div class="feature">
                        <i class="fas fa-home"></i>
                        <span>À votre domicile</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="testimonial-banner">
              <div class="testimonial-quote">
                <i class="fas fa-quote-left"></i>
                <p>Le service à la personne d'EcoDeli m'a sauvé la vie. Je peux maintenant me rendre à mes rendez-vous médicaux sans dépendre de ma famille.</p>
                <div class="testimonial-author">
                  <div class="author-avatar">
                    <i class="fas fa-user-circle"></i>
                  </div>
                  <div class="author-info">
                    <h4>Monique Leroy</h4>
                    <p>Utilisatrice services à la personne</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Stockage temporaire -->
          <div v-if="activeTab === 3" class="tab-content">
            <div class="tab-header">
              <div class="tab-icon">
                <i class="fas fa-warehouse"></i>
              </div>
              <div class="tab-title">
                <h2>Stockage temporaire</h2>
                <p>Stockez vos colis dans nos entrepôts pour une livraison ultérieure</p>
              </div>
            </div>
            
            <div class="services-grid">
              <div class="service-card">
                <div class="service-card-icon">
                  <i class="fas fa-box-open"></i>
                </div>
                <h3>Stockage de colis</h3>
                <p>Stockez vos colis en transit dans nos entrepôts sécurisés.</p>
                <div class="service-features">
                  <div class="feature">
                    <i class="fas fa-shield-alt"></i>
                    <span>Entrepôts sécurisés</span>
                  </div>
                  <div class="feature">
                    <i class="fas fa-thermometer-half"></i>
                    <span>Température contrôlée</span>
                  </div>
                </div>
              </div>
              
              <div class="service-card">
                <div class="service-card-icon">
                  <i class="fas fa-calendar-day"></i>
                </div>
                <h3>Livraison programmée</h3>
                <p>Planifiez la livraison de vos colis stockés à la date de votre choix.</p>
                <div class="service-features">
                  <div class="feature">
                    <i class="fas fa-calendar-check"></i>
                    <span>Date à la demande</span>
                  </div>
                  <div class="feature">
                    <i class="fas fa-bell"></i>
                    <span>Notifications</span>
                  </div>
                </div>
              </div>
              
              <div class="service-card">
                <div class="service-card-icon">
                  <i class="fas fa-boxes"></i>
                </div>
                <h3>Groupage de colis</h3>
                <p>Regroupez plusieurs colis pour une livraison unique et économique.</p>
                <div class="service-features">
                  <div class="feature">
                    <i class="fas fa-euro-sign"></i>
                    <span>Économique</span>
                  </div>
                  <div class="feature">
                    <i class="fas fa-leaf"></i>
                    <span>Écologique</span>
                  </div>
                </div>
              </div>
            </div>
            
          </div>
          
          <!-- Assurance colis -->
          <div v-if="activeTab === 4" class="tab-content">
            <div class="tab-header">
              <div class="tab-icon">
                <i class="fas fa-shield-alt"></i>
              </div>
              <div class="tab-title">
                <h2>Assurance colis</h2>
                <p>Protégez vos envois avec nos options d'assurance adaptées</p>
              </div>
            </div>
            
            <div class="insurance-plans">
              <div class="insurance-plan">
                <div class="plan-header">
                  <h3>Assurance Basique</h3>
                  <div class="plan-price">
                    <span class="price">2€</span>
                    <span class="period">par colis</span>
                  </div>
                </div>
                <div class="plan-features">
                    <div class="plan-feature">
                  <i class="fas fa-check"></i>
                  <span>Couverture jusqu'à 100€</span>
                </div>
                <div class="plan-feature">
                  <i class="fas fa-check"></i>
                  <span>Remboursement en cas de perte</span>
                </div>
                <div class="plan-feature">
                  <i class="fas fa-check"></i>
                  <span>Remboursement en cas de dommage</span>
                </div>
                <div class="plan-feature inactive">
                  <i class="fas fa-times"></i>
                  <span>Remboursement en cas de vol</span>
                </div>
                <div class="plan-feature inactive">
                  <i class="fas fa-times"></i>
                  <span>Remboursement en cas de retard</span>
                </div>
              </div>
            </div>
            
            <div class="insurance-plan featured">
              <div class="plan-badge">Recommandé</div>
              <div class="plan-header">
                <h3>Assurance Standard</h3>
                <div class="plan-price">
                  <span class="price">5€</span>
                  <span class="period">par colis</span>
                </div>
              </div>
              <div class="plan-features">
                <div class="plan-feature">
                  <i class="fas fa-check"></i>
                  <span>Couverture jusqu'à 500€</span>
                </div>
                <div class="plan-feature">
                  <i class="fas fa-check"></i>
                  <span>Remboursement en cas de perte</span>
                </div>
                <div class="plan-feature">
                  <i class="fas fa-check"></i>
                  <span>Remboursement en cas de dommage</span>
                </div>
                <div class="plan-feature">
                  <i class="fas fa-check"></i>
                  <span>Remboursement en cas de vol</span>
                </div>
                <div class="plan-feature inactive">
                  <i class="fas fa-times"></i>
                  <span>Remboursement en cas de retard</span>
                </div>
              </div>
            </div>
            
            <div class="insurance-plan">
              <div class="plan-header">
                <h3>Assurance Premium</h3>
                <div class="plan-price">
                  <span class="price">10€</span>
                  <span class="period">par colis</span>
                </div>
              </div>
              <div class="plan-features">
                <div class="plan-feature">
                  <i class="fas fa-check"></i>
                  <span>Couverture jusqu'à 1500€</span>
                </div>
                <div class="plan-feature">
                  <i class="fas fa-check"></i>
                  <span>Remboursement en cas de perte</span>
                </div>
                <div class="plan-feature">
                  <i class="fas fa-check"></i>
                  <span>Remboursement en cas de dommage</span>
                </div>
                <div class="plan-feature">
                  <i class="fas fa-check"></i>
                  <span>Remboursement en cas de vol</span>
                </div>
                <div class="plan-feature">
                  <i class="fas fa-check"></i>
                  <span>Remboursement en cas de retard</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="insurance-note">
            <i class="fas fa-info-circle"></i>
            <p>Pour les envois de valeur supérieure à 1500€, veuillez nous contacter directement pour une assurance sur-mesure.</p>
          </div>
          
          <div class="faq-section">
            <h3>Questions fréquentes sur l'assurance</h3>
            <div class="faq-items">
              <div class="faq-item">
                <div class="faq-question" @click="toggleFaq(0)">
                  <h4>Comment déclarer un sinistre ?</h4>
                  <i class="fas" :class="[expandedFaq === 0 ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
                </div>
                <div class="faq-answer" :class="{ 'expanded': expandedFaq === 0 }">
                  <p>Pour déclarer un sinistre, connectez-vous à votre compte EcoDeli et accédez à la section "Mes envois". Sélectionnez l'envoi concerné et cliquez sur "Déclarer un problème". Suivez ensuite les instructions pour compléter votre déclaration.</p>
                </div>
              </div>
              
              <div class="faq-item">
                <div class="faq-question" @click="toggleFaq(1)">
                  <h4>Quel est le délai de remboursement ?</h4>
                  <i class="fas" :class="[expandedFaq === 1 ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
                </div>
                <div class="faq-answer" :class="{ 'expanded': expandedFaq === 1 }">
                  <p>Le délai de remboursement est généralement de 5 à 10 jours ouvrés après validation de votre déclaration. Dans certains cas, une enquête plus approfondie peut être nécessaire, ce qui peut prolonger ce délai.</p>
                </div>
              </div>
              
              <div class="faq-item">
                <div class="faq-question" @click="toggleFaq(2)">
                  <h4>Quels justificatifs fournir en cas de sinistre ?</h4>
                  <i class="fas" :class="[expandedFaq === 2 ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
                </div>
                <div class="faq-answer" :class="{ 'expanded': expandedFaq === 2 }">
                  <p>En cas de sinistre, vous devrez fournir une preuve d'achat du bien transporté (facture, ticket de caisse), ainsi qu'une description détaillée du problème rencontré. Des photos du colis et/ou de son contenu endommagé peuvent également être demandées.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Call-to-Action Section -->
    <section class="services-cta">
      <div class="container">
        <div class="cta-content">
          <h2>Prêt à utiliser nos services ?</h2>
          <p>Rejoignez notre communauté de livreurs et clients satisfaits</p>
          <div class="cta-buttons">
            <router-link to="/register" class="btn btn-success">
              <span>Créer un compte</span>
              <i class="fas fa-user-plus"></i>
            </router-link>
            <a href="mailto:cheradiwissam11@gmail.com" class="btn btn-info">
                <span>Envoyer un email</span>
                <i class="fas fa-envelope"></i>
            </a>

          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'ServicesView',
  data() {
    return {
      activeTab: 0,
      expandedFaq: -1,
      serviceCategories: [
        {
          title: 'Livraison de colis',
          icon: 'fas fa-box'
        },
        {
          title: 'Lâcher de chariot',
          icon: 'fas fa-shopping-basket'
        },
        {
          title: 'Services à la personne',
          icon: 'fas fa-hands-helping'
        },
        {
          title: 'Stockage temporaire',
          icon: 'fas fa-warehouse'
        },
        {
          title: 'Assurance colis',
          icon: 'fas fa-shield-alt'
        }
      ]
    };
  },
  methods: {
    toggleFaq(index) {
      this.expandedFaq = this.expandedFaq === index ? -1 : index;
    }
  },
  mounted() {
    // Check if there's a service parameter in the URL to activate the corresponding tab
    const serviceParam = this.$route.query.service;
    if (serviceParam) {
      const tabIndex = this.serviceCategories.findIndex(cat => 
        cat.title.toLowerCase().replace(/\s+/g, '-') === serviceParam);
      
      if (tabIndex !== -1) {
        this.activeTab = tabIndex;
      }
    }
  }
};
</script>

<style scoped>
/* Variables CSS avec couleurs améliorées pour plus de visibilité */
:root {
  --primary-color: #00796b;    /* Vert plus foncé et saturé */
  --secondary-color: #00a878;  /* Vert secondaire plus visible */
  --accent-color: #0277bd;     /* Bleu plus foncé */
  --light-color: #ffffff;      /* Blanc pur */
  --dark-color: #004d40;       /* Vert très foncé pour le texte */
  --grey-color: #f5f5f5;       /* Gris clair */
  --text-color: #212121;       /* Presque noir pour le texte */
  --shadow: 0 4px 15px rgba(0, 0, 0, 0.15);  /* Ombre plus visible */
  --transition: all 0.3s ease;
  --border-radius: 10px;
}

/* Base Styles */
.services-page {
  width: 100%;
  overflow-x: hidden;
  background-color: #ffffff;
  color: var(--text-color);
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Hero Section */
.services-hero {
  position: relative;
  padding: 100px 0 50px;
  background: linear-gradient(135deg, #00796b, #00a878);
  color: white;
  text-align: center;
}

.services-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 20px;
  text-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.services-subtitle {
  font-size: 1.2rem;
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.6;
}

.wave-divider {
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 100px;
  overflow: hidden;
  line-height: 0;
}

.wave-divider svg {
  position: relative;
  display: block;
  width: 100%;
  height: 100px;
}

/* Tabs Navigation */
.services-tabs {
  background-color: white;
  padding: 20px 0;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.tabs-container {
  display: flex;
  justify-content: center;
  overflow-x: auto;
  padding: 10px 0;
  gap: 10px;
}

.tab-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 20px;
  background-color: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: var(--transition);
  color: var(--text-color);
  border: 1px solid transparent;
  min-width: 120px;
}

.tab-button i {
  font-size: 1.5rem;
  margin-bottom: 8px;
  color: var(--primary-color);
}

.tab-button span {
  font-size: 0.9rem;
  font-weight: 500;
  text-align: center;
}

.tab-button:hover {
  background-color: rgba(0, 121, 107, 0.05);
  border-color: rgba(0, 121, 107, 0.1);
}

.tab-button.active {
  background-color: rgba(0, 121, 107, 0.1);
  border-color: rgba(0, 121, 107, 0.2);
  color: var(--primary-color);
  font-weight: 600;
}

.tab-button.active i {
  color: var(--secondary-color);
}

/* Services Content Section */
.services-content {
  padding: 60px 0;
  background-color: #f9f9f9;
}

.tab-content {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.tab-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  background: white;
  padding: 30px;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  border: 1px solid #e0e0e0;
}

.tab-icon {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
  color: white;
  font-size: 2rem;
  flex-shrink: 0;
  box-shadow: 0 5px 15px rgba(0, 121, 107, 0.3);
}

.tab-title {
  flex: 1;
}

.tab-title h2 {
  font-size: 2rem;
  margin-bottom: 5px;
  color: var(--dark-color);
}

.tab-title p {
  font-size: 1.1rem;
  color: #555;
}

/* Services Grid */
.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-bottom: 30px;
}

.service-card {
  background: white;
  border-radius: var(--border-radius);
  padding: 30px;
  box-shadow: var(--shadow);
  transition: var(--transition);
  position: relative;
  overflow: hidden;
  border: 1px solid #e0e0e0;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
}

.service-card-icon {
  width: 60px;
  height: 60px;
  background: rgba(0, 121, 107, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  color: var(--primary-color);
  font-size: 1.5rem;
}

.service-card h3 {
  font-size: 1.3rem;
  margin-bottom: 15px;
  color: var(--dark-color);
  font-weight: 600;
}

.service-card p {
  font-size: 1rem;
  color: #555;
  margin-bottom: 20px;
  line-height: 1.6;
  flex-grow: 1;
}

.service-features {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.feature {
  display: flex;
  align-items: center;
  gap: 10px;
}

.feature i {
  color: var(--primary-color);
  font-size: 0.9rem;
}

.service-partners, 
.popular-items {
  margin-bottom: 20px;
  font-size: 0.95rem;
  padding: 10px 15px;
  background: rgba(0, 121, 107, 0.05);
  border-radius: 5px;
  line-height: 1.6;
}

.service-partners span,
.popular-items span {
  font-weight: 600;
  color: var(--dark-color);
}

/* How It Works Section */
.how-it-works {
  background: white;
  border-radius: var(--border-radius);
  padding: 30px;
  box-shadow: var(--shadow);
  border: 1px solid #e0e0e0;
}

.how-it-works h3 {
  font-size: 1.6rem;
  margin-bottom: 30px;
  color: var(--dark-color);
  text-align: center;
  position: relative;
  padding-bottom: 15px;
}

.how-it-works h3::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
  transform: translateX(-50%);
  border-radius: 3px;
}

.steps {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.step {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  padding: 20px;
  border-radius: var(--border-radius);
  transition: var(--transition);
  background: rgba(0, 121, 107, 0.03);
  border: 1px solid rgba(0, 121, 107, 0.1);
}

.step:hover {
  background: rgba(0, 121, 107, 0.05);
  transform: translateX(5px);
}

.step-number {
  width: 40px;
  height: 40px;
  background: var(--primary-color);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  flex-shrink: 0;
  box-shadow: 0 4px 10px rgba(0, 121, 107, 0.3);
}

.step-content h4 {
  font-size: 1.1rem;
  margin-bottom: 5px;
  color: var(--dark-color);
}

.step-content p {
  font-size: 0.95rem;
  color: #555;
  line-height: 1.5;
}

/* Testimonial Banner */
.testimonial-banner {
  background: white;
  border-radius: var(--border-radius);
  padding: 30px;
  box-shadow: var(--shadow);
  border: 1px solid #e0e0e0;
}

.testimonial-quote {
  position: relative;
  padding-left: 60px;
}

.testimonial-quote i {
  position: absolute;
  top: 0;
  left: 0;
  font-size: 2.5rem;
  color: rgba(0, 121, 107, 0.2);
}

.testimonial-quote p {
  font-size: 1.1rem;
  line-height: 1.7;
  margin-bottom: 20px;
  color: #555;
  font-style: italic;
}

.testimonial-author {
  display: flex;
  align-items: center;
}

.author-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  color: white;
  font-size: 1.5rem;
  border: 2px solid white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.author-info h4 {
  font-size: 1rem;
  margin-bottom: 5px;
  color: var(--dark-color);
}

.author-info p {
  font-size: 0.9rem;
  color: #666;
}

/* Locations Section */
.locations-section {
  background: white;
  border-radius: var(--border-radius);
  padding: 30px;
  box-shadow: var(--shadow);
  border: 1px solid #e0e0e0;
}

.locations-section h3 {
  font-size: 1.6rem;
  margin-bottom: 30px;
  color: var(--dark-color);
  text-align: center;
}

.locations-map {
  height: 300px;
  background: rgba(0, 121, 107, 0.05);
  border-radius: var(--border-radius);
  position: relative;
  overflow: hidden;
  margin-bottom: 30px;
  border: 1px solid rgba(0, 121, 107, 0.1);
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 600"><path fill="rgba(0,121,107,0.1)" d="M85.7,45.1C71.2,56,67,81.7,59.6,100.9c-10.9,28.4-27.4,51.2-27.8,82.9 c-0.4,34.9,5.8,65.8,23.2,93.4c19.9,31.4,31.4,64.1,47.9,96.7c9.7,19.3,17.5,46.6,30.8,65c11.9,16.5,32.5,24.5,47.7,37.4 c20.7,17.5,56.7,25.4,83.7,9.1c22.8-13.8,28.1-44.5,34.4-68.7c14.2-55.2,27.4-112.5,39.3-168.7c4.1-19.3,5-45.2-8.4-62.3 c-25.8-32.9-63.3-69.6-107.8-72.4c-40.2-2.5-39.2,17.9-46.4-29.7c-2.3-15.1-41-38.5-53-43.5C109.7,33.1,93.5,39.1,85.7,45.1z"/></svg>');
}

.locations-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.location-marker {
  position: absolute;
  transform: translate(-50%, -50%);
}

.location-dot {
  width: 14px;
  height: 14px;
  background: var(--primary-color);
  border-radius: 50%;
  border: 3px solid white;
  box-shadow: 0 0 0 2px var(--primary-color);
  display: inline-block;
  position: relative;
  z-index: 1;
}

.location-label {
  position: absolute;
  white-space: nowrap;
  font-size: 0.9rem;
  font-weight: 600;
  background: white;
  padding: 3px 10px;
  border-radius: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  color: var(--dark-color);
  z-index: 2;
}

.locations-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.location-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 15px;
  border-radius: var(--border-radius);
  transition: var(--transition);
  background: rgba(0, 121, 107, 0.03);
  border: 1px solid rgba(0, 121, 107, 0.1);
}

.location-item:hover {
  background: rgba(0, 121, 107, 0.05);
  transform: translateX(5px);
}

.location-item i {
  color: var(--primary-color);
  font-size: 1.2rem;
  margin-top: 3px;
}

.location-details h4 {
  font-size: 1rem;
  margin-bottom: 5px;
  color: var(--dark-color);
}

.location-details p {
  font-size: 0.9rem;
  color: #666;
}

/* Insurance Plans */
.insurance-plans {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  margin-bottom: 30px;
}

.insurance-plan {
  background: white;
  border-radius: var(--border-radius);
  padding: 30px;
  box-shadow: var(--shadow);
  border: 1px solid #e0e0e0;
  transition: var(--transition);
  position: relative;
  overflow: hidden;
}

.insurance-plan:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
}

.insurance-plan.featured {
  border-color: var(--primary-color);
  box-shadow: 0 10px 25px rgba(0, 121, 107, 0.2);
}

.plan-badge {
  position: absolute;
  top: 12px;
  right: -30px;
  background: var(--primary-color);
  color: white;
  padding: 5px 30px;
  font-size: 0.8rem;
  font-weight: 600;
  transform: rotate(45deg);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.plan-header {
  text-align: center;
  padding-bottom: 20px;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.plan-header h3 {
  font-size: 1.4rem;
  margin-bottom: 15px;
  color: var(--dark-color);
}

.plan-price {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.price {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--primary-color);
}

.period {
  font-size: 0.9rem;
  color: #777;
}

.plan-features {
  margin-bottom: 25px;
}

.plan-feature {
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px dashed #eee;
}

.plan-feature i {
  margin-right: 10px;
  font-size: 0.9rem;
}

.plan-feature i.fa-check {
  color: var(--secondary-color);
}

.plan-feature i.fa-times {
  color: #e57373;
}

.plan-feature.inactive {
  color: #999;
}

.insurance-note {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 20px;
  border-radius: var(--border-radius);
  background: rgba(0, 121, 107, 0.05);
  border: 1px solid rgba(0, 121, 107, 0.1);
  margin-bottom: 40px;
}

.insurance-note i {
  color: var(--primary-color);
  font-size: 1.5rem;
  margin-top: 3px;
}

.insurance-note p {
  font-size: 0.95rem;
  color: #555;
  line-height: 1.6;
}

/* FAQ Section */
.faq-section {
  background: white;
  border-radius: var(--border-radius);
  padding: 30px;
  box-shadow: var(--shadow);
  border: 1px solid #e0e0e0;
}

.faq-section h3 {
  font-size: 1.6rem;
  margin-bottom: 30px;
  color: var(--dark-color);
  text-align: center;
}

.faq-items {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.faq-item {
  border: 1px solid #eee;
  border-radius: 10px;
  overflow: hidden;
}

.faq-question {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
  background: #f9f9f9;
  cursor: pointer;
  transition: var(--transition);
}

.faq-question:hover {
  background: #f0f0f0;
}

.faq-question h4 {
  font-size: 1.1rem;
  color: var(--dark-color);
  font-weight: 600;
}

.faq-question i {
  color: var(--primary-color);
  font-size: 1rem;
  transition: var(--transition);
}

.faq-answer {
  height: 0;
  overflow: hidden;
  transition: height 0.3s ease;
}

.faq-answer.expanded {
  height: auto;
  padding: 15px 20px;
}

.faq-answer p {
  font-size: 1rem;
  color: #555;
  line-height: 1.6;
}

/* Services CTA */
.services-cta {
  padding: 60px 0;
  background: linear-gradient(135deg, #00796b, #00a878);
  color: white;
  text-align: center;
}

.services-cta h2 {
  font-size: 2.5rem;
  margin-bottom: 15px;
  font-weight: 700;
}

.services-cta p {
  font-size: 1.2rem;
  margin-bottom: 30px;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
  opacity: 0.9;
}

.cta-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  padding: 15px 30px;
  border-radius: 30px;
  text-decoration: none;
  font-weight: 600;
  transition: var(--transition);
  gap: 10px;
  font-size: 1.1rem;
}

.cta-button.primary {
  background: white;
  color: var(--primary-color);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.cta-button.primary:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.cta-button.secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.cta-button.secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-5px);
}

/* Responsive Design */
@media (max-width: 992px) {
  .services-hero {
    padding: 80px 0 50px;
  }
  
  .services-title {
    font-size: 2.5rem;
  }
  
  .tabs-container {
    justify-content: flex-start;
  }
  
  .tab-button {
    min-width: auto;
    flex: 0 0 auto;
  }
  
  .locations-map {
    height: 300px;
  }
}

@media (max-width: 768px) {
  .services-hero {
    padding: 60px 0 50px;
  }
  
  .services-title {
    font-size: 2rem;
  }
  
  .tab-header {
    flex-direction: column;
    text-align: center;
    padding: 20px;
  }
  
  .tab-icon {
    margin-right: 0;
    margin-bottom: 15px;
  }
  
  .how-it-works,
  .testimonial-banner,
  .locations-section,
  .faq-section {
    padding: 20px;
  }
  
  .steps {
    gap: 15px;
  }
  
  .step {
    padding: 15px;
  }
  
  .insurance-plans {
    gap: 20px;
  }
  
  .insurance-plan {
    padding: 20px;
  }
  
  .services-cta {
    padding: 40px 0;
  }
  
  .services-cta h2 {
    font-size: 2rem;
  }
}

@media (max-width: 576px) {
  .services-tabs {
    padding: 10px 0;
  }
  
  .tab-button {
    padding: 8px 12px;
  }
  
  .tab-button i {
    font-size: 1.2rem;
  }
  
  .tab-button span {
    font-size: 0.8rem;
  }
  
  .services-content {
    padding: 40px 0;
  }
  
  .services-grid {
    grid-template-columns: 1fr;
  }
  
  .service-card {
    padding: 20px;
  }
  
  .cta-buttons {
    flex-direction: column;
    gap: 15px;
  }
}
</style>