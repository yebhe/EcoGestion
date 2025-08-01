<template>
  <div class="ecodeli-home">
    <!-- Loader d'entrée -->
    <transition name="fade">
      <div v-if="isLoading" class="loader-wrapper">
        <div class="loader">
          <div class="loader-circle"></div>
          <div class="loader-logo">
            <span>ED</span>
          </div>
        </div>
      </div>
    </transition>

    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title" :class="{ 'animate-title': animateContent }">
            <span class="title-line">Livraison collaborative</span>
            <span class="title-line">écologique et solidaire</span>
          </h1>
          <p class="hero-subtitle" :class="{ 'animate-subtitle': animateContent }">
            EcoDeli connecte des particuliers pour livrer vos colis et offrir des services à la personne, partout en France.
          </p>
          <div class="hero-buttons" :class="{ 'animate-buttons': animateContent }">
            <router-link to="/services" class="btn btn-info">
              <span>Découvrir nos services</span>
              <i class="fas fa-arrow-right"></i>
            </router-link>
            <router-link to="/register" class="btn btn-secondary">
              <span>Devenir livreur</span>
              <i class="fas fa-user-plus"></i>
            </router-link>
          </div>
        </div>
        <div class="hero-image" :class="{ 'animate-image': animateContent }">
          <div class="icon-container">
            <div class="delivery-icon">
              <i class="fas fa-truck-moving"></i>
              <div class="path-circle"></div>
              <i class="fas fa-map-marker-alt location-marker"></i>
              <i class="fas fa-home destination-marker"></i>
            </div>
            <div class="floating-elements">
              <div class="floating-item eco-badge">
                <i class="fas fa-leaf"></i>
                <span>-30% CO2</span>
              </div>
              <div class="floating-item fast-badge">
                <i class="fas fa-bolt"></i>
                <span>Rapide</span>
              </div>
              <div class="floating-item secure-badge">
                <i class="fas fa-shield-alt"></i>
                <span>Sécurisé</span>
              </div>
            </div>
          </div>
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

    <!-- Services Section -->
    <section class="services-section">
      <div class="container">
        <div class="section-header" ref="servicesHeader">
          <h2 class="section-title" :class="{ 'animate-in': servicesVisible }">Nos Services</h2>
          <p class="section-subtitle" :class="{ 'animate-in': servicesVisible }">
            Découvrez toutes les solutions proposées par EcoDeli pour faciliter votre quotidien.
          </p>
        </div>
        
        <div class="services-grid" :class="{ 'animate-in': servicesVisible }">
          <div v-for="(service, index) in services" :key="index" 
            class="service-card" 
            :class="{ 'animate-in': servicesVisible }"
            :style="{ 'animation-delay': `${0.1 + (index * 0.1)}s` }">
            <div class="service-icon">
              <i :class="service.icon"></i>
            </div>
            <h3 class="service-title">{{ service.title }}</h3>
            <p class="service-description">{{ service.description }}</p>            
          </div>
        </div>
      </div>
    </section>

    <!-- Comment ça marche Section -->
    <section class="how-section">
      <div class="container">
        <div class="section-header" ref="howHeader">
          <h2 class="section-title light" :class="{ 'animate-in': howVisible }">Comment ça marche</h2>
          <p class="section-subtitle light" :class="{ 'animate-in': howVisible }">
            Suivez ces étapes simples pour utiliser nos services de livraison collaborative.
          </p>
        </div>
        
        <div class="steps-container" :class="{ 'animate-in': howVisible }">
          <div v-for="(step, index) in steps" :key="index" 
            class="step-card" 
            :class="{ 'animate-in': howVisible }"
            :style="{ 'animation-delay': `${0.1 + (index * 0.15)}s` }">
            <div class="step-number">{{ index + 1 }}</div>
            <div class="step-content">
              <h3 class="step-title">{{ step.title }}</h3>
              <p class="step-description">{{ step.description }}</p>
            </div>
            <div class="step-icon">
              <i :class="step.icon"></i>
            </div>
          </div>
          
          <div class="steps-progress-line">
            <div class="progress-dot" v-for="(_, index) in steps" :key="`dot-${index}`"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Témoignages Section -->
    <section class="testimonials-section">
      <div class="container">
        <div class="section-header" ref="testimonialsHeader">
          <h2 class="section-title" :class="{ 'animate-in': testimonialsVisible }">Témoignages</h2>
          <p class="section-subtitle" :class="{ 'animate-in': testimonialsVisible }">
            Découvrez ce que nos utilisateurs disent de nos services.
          </p>
        </div>
        
        <div class="testimonials-slider" :class="{ 'animate-in': testimonialsVisible }">
          <div class="slider-container" :style="{ transform: `translateX(-${currentSlide * 100}%)` }">
            <div v-for="(testimonial, index) in testimonials" :key="index" class="testimonial-card">
              <div class="testimonial-content">
                <div class="quote-icon">
                  <i class="fas fa-quote-left"></i>
                </div>
                <p class="testimonial-text">{{ testimonial.text }}</p>
                <div class="testimonial-rating">
                  <i v-for="n in 5" :key="n" class="fas fa-star" :class="{ 'active': n <= testimonial.rating }"></i>
                </div>
              </div>
              <div class="testimonial-author">
                <div class="author-avatar">
                  <i class="fas" :class="testimonial.avatarIcon"></i>
                </div>
                <div class="author-info">
                  <h4 class="author-name">{{ testimonial.name }}</h4>
                  <p class="author-type">{{ testimonial.type }}</p>
                </div>
              </div>
            </div>
          </div>
          
          <div class="slider-controls">
            <button @click="prevSlide" class="slider-control prev" :disabled="currentSlide === 0">
              <i class="fas fa-chevron-left"></i>
            </button>
            <div class="slider-dots">
              <button v-for="(_, index) in testimonials" :key="index" 
                @click="goToSlide(index)" 
                class="slider-dot" 
                :class="{ 'active': currentSlide === index }">
              </button>
            </div>
            <button @click="nextSlide" class="slider-control next" :disabled="currentSlide === testimonials.length - 1">
              <i class="fas fa-chevron-right"></i>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Call-to-Action Section -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-content" ref="ctaContent">
          <h2 class="cta-title" :class="{ 'animate-in': ctaVisible }">Rejoignez l'aventure EcoDeli</h2>
          <p class="cta-text" :class="{ 'animate-in': ctaVisible }">
            Que vous soyez client, livreur, commerçant ou prestataire, EcoDeli vous ouvre les portes d'une nouvelle économie collaborative.
          </p>
          <div class="cta-buttons" :class="{ 'animate-in': ctaVisible }">
            <router-link to="/register" class="btn btn-success">
              <span>S'inscrire</span>
              <i class="fas fa-user-plus"></i>
            </router-link>
            <a href="mailto:cheradiwissam11@gmail.com" class="btn btn-outline">
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
import { ref, onMounted, onUnmounted } from 'vue';

export default {
  name: 'HomeView',
  setup() {
    // État du chargement initial
    const isLoading = ref(true);
    
    // États pour les animations
    const animateContent = ref(false);
    const servicesVisible = ref(false);
    const howVisible = ref(false);
    const testimonialsVisible = ref(false);
    const ctaVisible = ref(false);

    // Références pour l'observation des sections
    const servicesHeader = ref(null);
    const howHeader = ref(null);
    const testimonialsHeader = ref(null);
    const ctaContent = ref(null);

    // État du slider de témoignages
    const currentSlide = ref(0);
    const autoSlideInterval = ref(null);

    // Données pour les services
    const services = [
      {
        icon: 'fas fa-box',
        title: 'Livraison de colis',
        description: 'Envoyez vos colis partout en France grâce à notre réseau de livreurs particuliers.',
        link: '/services/colis'
      },
      {
        icon: 'fas fa-shopping-basket',
        title: 'Lâcher de chariot',
        description: 'Faites vos courses chez nos commerçants partenaires et faites-vous livrer à domicile.',
        link: '/services/chariot'
      },
      {
        icon: 'fas fa-hands-helping',
        title: 'Services à la personne',
        description: 'Transport quotidien, courses, accompagnement... Profitez de services personnalisés.',
        link: '/services/personne'
      },
      {
        icon: 'fas fa-globe-europe',
        title: "Achats à l'étranger",
        description: "Faites-vous rapporter des produits introuvables en France par des voyageurs.",
        link: '/services/achats'
      },
      {
        icon: 'fas fa-warehouse',
        title: 'Stockage temporaire',
        description: 'Stockez vos colis dans nos entrepôts pour une livraison ultérieure.',
        link: '/services/stockage'
      },
      {
        icon: 'fas fa-shield-alt',
        title: 'Assurance colis',
        description: "Protégez vos envois avec nos options d'assurance adaptées.",
        link: '/services/assurance'
      }
    ];

    // Données pour les étapes
    const steps = [
      {
        title: "Inscrivez-vous",
        description: "Créez votre compte en quelques clics et complétez votre profil.",
        icon: 'fas fa-user-plus'
      },
      {
        title: 'Déposez une annonce',
        description: 'Indiquez ce que vous souhaitez envoyer, où et quand.',
        icon: 'fas fa-bullhorn'
      },
      {
        title: 'Trouvez un livreur',
        description: 'Choisissez parmi les livreurs disponibles sur votre trajet.',
        icon: 'fas fa-search'
      },
      {
        title: 'Suivez votre colis',
        description: 'Restez informé en temps réel du statut de votre livraison.',
        icon: 'fas fa-map-marker-alt'
      }
    ];

    // Données pour les témoignages avec icônes
    const testimonials = [
      {
        text: 'EcoDeli a révolutionné ma façon de gérer mes livraisons. Service rapide, écologique et avec un contact humain chaleureux !',
        rating: 5,
        name: 'Sophie Dupont',
        type: 'Cliente régulière',
        avatarIcon: 'fa-user-circle'
      },
      {
        text: "Devenir livreur chez EcoDeli m'a permis de compléter mes revenus tout en rendant service. La plateforme est intuitive et l'équipe très réactive !",
        rating: 5,
        name: 'Thomas Martin',
        type: 'Livreur',
        avatarIcon: 'fa-user-tie'
      },
      {
        text: "Depuis que j'ai rejoint EcoDeli comme commerçant partenaire, mes ventes ont augmenté de 30%. Le service lâcher de chariot est particulièrement apprécié !",
        rating: 4,
        name: 'Jean Petit',
        type: 'Commerçant partenaire',
        avatarIcon: 'fa-store'
      },
      {
        text: "Le service à la personne d'EcoDeli m'a sauvé la vie. Je peux maintenant me rendre à mes rendez-vous médicaux sans dépendre de ma famille.",
        rating: 5,
        name: 'Monique Leroy',
        type: 'Utilisatrice services à la personne',
        avatarIcon: 'fa-user-friends'
      }
    ];

    // Méthodes pour le slider
    const nextSlide = () => {
      currentSlide.value = (currentSlide.value + 1) % testimonials.length;
      resetAutoSlide();
    };

    const prevSlide = () => {
      currentSlide.value = (currentSlide.value - 1 + testimonials.length) % testimonials.length;
      resetAutoSlide();
    };

    const goToSlide = (index) => {
      currentSlide.value = index;
      resetAutoSlide();
    };

    const resetAutoSlide = () => {
      if (autoSlideInterval.value) {
        clearInterval(autoSlideInterval.value);
      }
      autoSlideInterval.value = setInterval(() => {
        nextSlide();
      }, 5000);
    };

    // Observer pour les animations au scroll
    const setupIntersectionObserver = () => {
      const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -100px 0px'
      };

      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.target === servicesHeader.value) {
            servicesVisible.value = entry.isIntersecting;
          } else if (entry.target === howHeader.value) {
            howVisible.value = entry.isIntersecting;
          } else if (entry.target === testimonialsHeader.value) {
            testimonialsVisible.value = entry.isIntersecting;
          } else if (entry.target === ctaContent.value) {
            ctaVisible.value = entry.isIntersecting;
          }
        });
      }, observerOptions);

      // Observer les éléments
      if (servicesHeader.value) observer.observe(servicesHeader.value);
      if (howHeader.value) observer.observe(howHeader.value);
      if (testimonialsHeader.value) observer.observe(testimonialsHeader.value);
      if (ctaContent.value) observer.observe(ctaContent.value);

      return observer;
    };

    onMounted(() => {
      // Simuler un chargement initial
      setTimeout(() => {
        isLoading.value = false;
        
        // Animer le contenu principal après le chargement
        setTimeout(() => {
          animateContent.value = true;
        }, 200);
      }, 1500);

      // Configurer l'observer pour les animations au scroll
      const observer = setupIntersectionObserver();

      // Démarrer le slider automatique
      resetAutoSlide();

      onUnmounted(() => {
        // Nettoyer les observers et timers
        observer.disconnect();
        
        if (autoSlideInterval.value) {
          clearInterval(autoSlideInterval.value);
        }
      });
    });

    return {
      isLoading,
      animateContent,
      servicesVisible,
      howVisible,
      testimonialsVisible,
      ctaVisible,
      servicesHeader,
      howHeader,
      testimonialsHeader,
      ctaContent,
      currentSlide,
      services,
      steps,
      testimonials,
      nextSlide,
      prevSlide,
      goToSlide
    };
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

/* Animation de chargement */
.loader-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.loader {
  width: 100px;
  height: 100px;
  position: relative;
}

.loader-circle {
  border: 5px solid rgba(255, 255, 255, 0.3);
  border-top: 5px solid white;
  border-radius: 50%;
  width: 100%;
  height: 100%;
  animation: spin 1s linear infinite;
}

.loader-logo {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  font-size: 24px;
  color: var(--primary-color);
  background: white;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.7); }
  70% { box-shadow: 0 0 0 20px rgba(255, 255, 255, 0); }
  100% { box-shadow: 0 0 0 0 rgba(255, 255, 255, 0); }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* Conteneur principal */
.ecodeli-home {
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
.hero-section {
  position: relative;
  min-height: 100vh;
  padding: 100px 0 50px;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #e0f2f1, #b2dfdb);
  overflow: hidden;
}

.hero-section .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  z-index: 1;
}

.hero-content {
  flex: 1;
  max-width: 600px;
  padding-right: 40px;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 20px;
  color: var(--dark-color);
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.title-line {
  display: block;
  margin-bottom: 5px;
}

.hero-title.animate-title {
  opacity: 1;
  transform: translateY(0);
}

.hero-subtitle {
  font-size: 1.2rem;
  line-height: 1.6;
  margin-bottom: 30px;
  color: #333333;  /* Texte plus foncé */
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s ease 0.2s, transform 0.8s ease 0.2s;
}

.hero-subtitle.animate-subtitle {
  opacity: 1;
  transform: translateY(0);
}

.hero-buttons {
  display: flex;
  gap: 15px;
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s ease 0.4s, transform 0.8s ease 0.4s;
}

.hero-buttons.animate-buttons {
  opacity: 1;
  transform: translateY(0);
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 25px;
  border-radius: 30px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
  gap: 10px;
}

.btn i {
  font-size: 0.9rem;
  transition: transform 0.3s ease;
}

.btn:hover i {
  transform: translateX(5px);
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  box-shadow: 0 4px 10px rgba(0, 121, 107, 0.3);
}

.btn-primary:hover {
  box-shadow: 0 6px 15px rgba(0, 121, 107, 0.4);
  transform: translateY(-2px);
}

.btn-secondary {
  background: white;
  color: var(--primary-color);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.btn-secondary:hover {
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.hero-image {
  flex: 1;
  max-width: 500px;
  transform: translateX(30px);
  opacity: 0;
  transition: all 1s ease 0.6s;
}

.hero-image.animate-image {
  transform: translateX(0);
  opacity: 1;
}

/* Animation de livraison */
.icon-container {
  position: relative;
  width: 100%;
  height: 380px;
  background: white;  /* Fond blanc pur pour mieux voir les éléments */
  border-radius: 15px;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid #e0e0e0;  /* Bordure légère */
}

.delivery-icon {
  position: relative;
  width: 80%;
  height: 70%;
}

.delivery-icon .fa-truck-moving {
  position: absolute;
  font-size: 3.5rem;
  color: var(--primary-color);
  animation: drive 5s infinite linear;
  top: 40%;
  left: 0;
  z-index: 5;
  filter: drop-shadow(0 2px 5px rgba(0, 0, 0, 0.2));  /* Ajouter une ombre */
}

.path-circle {
  position: absolute;
  width: 100%;
  height: 100px;
  border: 3px dashed rgba(0, 121, 107, 0.5);  /* Plus visible */
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.location-marker {
  position: absolute;
  font-size: 2.5rem;  /* Plus grand */
  color: #f44336;  /* Rouge plus vif */
  top: 10%;
  left: 10%;
  animation: pulse-marker 2s infinite;
  filter: drop-shadow(0 2px 3px rgba(0, 0, 0, 0.2));
}

.destination-marker {
  position: absolute;
  font-size: 2.5rem;  /* Plus grand */
  color: #00897b;  /* Vert plus vif */
  top: 20%;
  right: 10%;
  animation: pulse-marker 2s infinite 1s;
  filter: drop-shadow(0 2px 3px rgba(0, 0, 0, 0.2));
}

@keyframes drive {
  0% {
    transform: translateX(0) rotate(0deg);
  }
  25% {
    transform: translateX(60%) rotate(5deg);
  }
  50% {
    transform: translateX(100%) rotate(0deg);
  }
  75% {
    transform: translateX(60%) rotate(-5deg);
  }
  100% {
    transform: translateX(0) rotate(0deg);
  }
}

@keyframes pulse-marker {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.8;
  }
}

.floating-elements {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.floating-item {
  position: absolute;
  padding: 10px 15px;
  border-radius: 20px;
  background: white;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);  /* Ombre plus visible */
  animation: float 4s ease-in-out infinite;
  border: 1px solid #e0e0e0;
}

.floating-item i {
  font-size: 1.2rem;  /* Plus grand */
}

.eco-badge {
  top: 20px;
  left: -15px;
  animation-delay: 0.5s;
}

.eco-badge i {
  color: #4caf50;  /* Vert plus vif */
}

.fast-badge {
  bottom: 40px;
  right: -15px;
  animation-delay: 1s;
}

.fast-badge i {
  color: #ff9800;  /* Orange */
}

.secure-badge {
  bottom: -15px;
  left: 80px;
  animation-delay: 1.5s;
}

.secure-badge i {
  color: #2196f3;  /* Bleu vif */
}

.floating-item span {
  font-weight: 600;  /* Plus gras */
  color: #333;  /* Plus foncé */
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
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

/* Services Section */
.services-section {
  padding: 80px 0;
  background-color: white;
}

.section-header {
  text-align: center;
  margin-bottom: 50px;
}

.section-title {
  font-size: 2.5rem;
  color: var(--dark-color);
  margin-bottom: 15px;
  position: relative;
  display: inline-block;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;  /* Plus large */
  height: 4px;  /* Plus visible */
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
  border-radius: 3px;
}

.section-title.light {
  color: white;
}

.section-title.light::after {
  background: linear-gradient(90deg, white, rgba(255, 255, 255, 0.7));
}

.section-title.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.section-subtitle {
  font-size: 1.1rem;
  color: #333333;  /* Plus foncé */
  max-width: 700px;
  margin: 0 auto;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease 0.2s, transform 0.6s ease 0.2s;
}

.section-subtitle.light {
  color: rgba(255, 255, 255, 1);  /* Blanc pur */
}

.section-subtitle.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease 0.4s, transform 0.6s ease 0.4s;
}

.services-grid.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.service-card {
  background: white;
  border-radius: var(--border-radius);
  padding: 30px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);  /* Ombre plus prononcée */
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  opacity: 0;
  transform: translateY(30px);
  border: 1px solid #e0e0e0;  /* Bordure légère */
}

.service-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 5px;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s ease;
}

.service-card:hover {
  transform: translateY(-10px) !important;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);  /* Ombre plus visible au survol */
}

.service-card:hover::before {
  transform: scaleX(1);
}

.service-card.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.service-icon {
  font-size: 3rem;  /* Plus grand */
  margin-bottom: 20px;
  color: var(--primary-color);
  transition: all 0.3s ease;
  background: rgba(0, 121, 107, 0.1);  /* Fond d'icône léger */
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.service-card:hover .service-icon {
  transform: scale(1.1);
  color: var(--secondary-color);
  background: rgba(0, 168, 120, 0.1);  /* Change au survol */
}

.service-title {
  font-size: 1.4rem;
  margin-bottom: 15px;
  color: var(--dark-color);
  font-weight: 600;
}

.service-description {
  color: #333333;  /* Plus foncé */
  margin-bottom: 20px;
  line-height: 1.6;
}

.service-link {
  display: inline-flex;
  align-items: center;
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  gap: 5px;
  transition: all 0.3s ease;
}

.service-link:hover {
  color: var(--secondary-color);
}

.service-link:hover i {
  transform: translateX(5px);
}

.service-link i {
  transition: transform 0.3s ease;
}

/* Comment ça marche Section */
.how-section {
  padding: 80px 0;
  position: relative;
  background: linear-gradient(135deg, #00796b, #00a878);  /* Gradient plus fort */
  color: white;
  overflow: hidden;
}

.how-section .container {
  position: relative;
  z-index: 1;
}

.steps-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
  position: relative;
  max-width: 800px;
  margin: 0 auto;
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease 0.4s, transform 0.6s ease 0.4s;
}

.steps-container.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.steps-progress-line {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 25px;
  width: 3px;  /* Plus épais */
  background: rgba(255, 255, 255, 0.5);  /* Plus visible */
  z-index: 0;
}

.progress-dot {
  position: absolute;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background: white;
  left: -6px;
  z-index: 1;
  box-shadow: 0 0 0 5px rgba(255, 255, 255, 0.2);  /* Halo lumineux */
}

.progress-dot:nth-child(1) { top: 40px; }
.progress-dot:nth-child(2) { top: calc(25% + 40px); }
.progress-dot:nth-child(3) { top: calc(50% + 40px); }
.progress-dot:nth-child(4) { top: calc(75% + 40px); }

.step-card {
  display: flex;
  align-items: flex-start;
  background: rgba(255, 255, 255, 0.2);  /* Plus visible */
  border-radius: var(--border-radius);
  padding: 25px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);  /* Ombre plus prononcée */
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 2;
  opacity: 0;
  transform: translateX(-30px);
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.3);  /* Bordure légère */
}

.step-card:hover {
  background: rgba(255, 255, 255, 0.3);  /* Plus visible au survol */
  transform: translateX(0) scale(1.03) !important;
}

.step-card.animate-in {
  opacity: 1;
  transform: translateX(0);
}

.step-number {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: white;
  color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin-right: 20px;
  flex-shrink: 0;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.step-content {
  flex: 1;
}

.step-title {
  font-size: 1.3rem;
  margin-bottom: 10px;
  font-weight: 600;
}

.step-description {
  font-size: 1rem;  /* Plus grande */
  color: rgba(255, 255, 255, 1);  /* Blanc pur */
  line-height: 1.6;
}

.step-icon {
  font-size: 2.5rem;  /* Plus grand */
  margin-left: 20px;
  color: rgba(255, 255, 255, 0.9);  /* Plus visible */
  transition: all 0.3s ease;
}

.step-card:hover .step-icon {
  transform: scale(1.2);
  color: white;
  text-shadow: 0 0 15px rgba(255, 255, 255, 0.7);  /* Effet lumineux */
}

/* Testimonials Section */
.testimonials-section {
  padding: 80px 0;
  background-color: #f9f9f9;
}

.testimonials-slider {
  position: relative;
  max-width: 900px;
  margin: 0 auto;
  overflow: hidden;
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease 0.4s, transform 0.6s ease 0.4s;
}

.testimonials-slider.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.slider-container {
  display: flex;
  transition: transform 0.5s ease;
}

.testimonial-card {
  min-width: 100%;
  padding: 20px;
}

.testimonial-content {
  background: white;
  border-radius: var(--border-radius);
  padding: 30px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);  /* Ombre plus prononcée */
  position: relative;
  margin-bottom: 30px;
  border: 1px solid #e0e0e0;
}

.testimonial-content::after {
  content: '';
  position: absolute;
  bottom: -15px;
  left: 30px;
  width: 30px;
  height: 30px;
  background: white;
  transform: rotate(45deg);
  box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1);
  z-index: -1;
  border-right: 1px solid #e0e0e0;
  border-bottom: 1px solid #e0e0e0;
}

.quote-icon {
  font-size: 2.5rem;  /* Plus grand */
  color: rgba(0, 121, 107, 0.2);  /* Plus visible */
  position: absolute;
  top: 20px;
  left: 20px;
}

.testimonial-text {
  font-size: 1.1rem;
  line-height: 1.7;
  color: #333333;  /* Plus foncé */
  margin-bottom: 20px;
  position: relative;
  z-index: 1;
  font-style: italic;  /* Texte en italique */
}

.testimonial-rating {
  display: flex;
  gap: 5px;
}

.testimonial-rating i {
  color: #ddd;
  font-size: 1.2rem;
}

.testimonial-rating i.active {
  color: #FFC107;  /* Jaune vif */
}

.testimonial-author {
  display: flex;
  align-items: center;
  padding-left: 30px;
}

.author-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 15px;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  border: 2px solid white;  /* Bordure blanche */
}

.author-avatar i {
  font-size: 30px;
  color: white;
}

.author-name {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 5px;
  color: var(--dark-color);
}

.author-type {
  font-size: 0.9rem;
  color: #555555;  /* Plus foncé */
  background: rgba(0, 121, 107, 0.1);  /* Fond coloré */
  padding: 2px 8px;
  border-radius: 10px;
  display: inline-block;
}

.slider-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 30px;
  gap: 10px;
}

.slider-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ddd;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.slider-dot.active {
  background: var(--primary-color);
  transform: scale(1.2);
  box-shadow: 0 0 0 3px rgba(0, 121, 107, 0.2);  /* Halo */
}

.slider-control {
  width: 44px;  /* Plus grand */
  height: 44px;  /* Plus grand */
  border-radius: 50%;
  background: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15);
  color: var(--primary-color);
  transition: all 0.3s ease;
}

.slider-control:hover:not(:disabled) {
  background: var(--primary-color);
  color: white;
  transform: translateY(-2px);
}

.slider-control:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.slider-dots {
  display: flex;
  gap: 8px;
  margin: 0 10px;
}

/* CTA Section */
.cta-section {
  padding: 80px 0;
  position: relative;
  background: linear-gradient(135deg, #00796b, #00a878);  /* Plus foncé */
  color: white;
  overflow: hidden;
}

.cta-section .container {
  position: relative;
  z-index: 1;
}

.cta-content {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.1);  /* Fond légèrement visible */
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(5px);
}

.cta-title {
  font-size: 2.5rem;
  margin-bottom: 20px;
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease, transform 0.6s ease;
  text-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);  /* Ombre de texte */
}

.cta-title.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.cta-text {
  font-size: 1.2rem;
  margin-bottom: 30px;
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease 0.2s, transform 0.6s ease 0.2s;
}

.cta-text.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.cta-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease 0.4s, transform 0.6s ease 0.4s;
}

.cta-buttons.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.btn-light {
  background: white;
  color: var(--primary-color);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);  /* Ombre plus visible */
}

.btn-light:hover {
  background: #f5f5f5;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
}

.btn-outline {
  background: transparent;
  color: white;
  border: 2px solid white;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.btn-outline:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

/* Responsive Design */
@media (max-width: 992px) {
  .hero-section .container {
    flex-direction: column;
    text-align: center;
  }

  .hero-content {
    max-width: 100%;
    padding-right: 0;
    margin-bottom: 50px;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-buttons {
    justify-content: center;
  }

  .hero-image {
    max-width: 100%;
  }

  .service-card {
    padding: 25px;
  }

  .testimonial-content {
    padding: 25px;
  }
}

@media (max-width: 768px) {
  .services-grid {
    grid-template-columns: 1fr;
  }

  .step-card {
    padding: 20px;
  }

  .step-icon {
    display: none;
  }

  .cta-buttons {
    flex-direction: column;
    gap: 15px;
  }

  .hero-title {
    font-size: 2rem;
  }

  .section-title {
    font-size: 2rem;
  }
}

@media (max-width: 576px) {
  .hero-section {
    padding: 70px 0 40px;
  }

  .hero-title {
    font-size: 1.8rem;
  }

  .services-section,
  .how-section,
  .testimonials-section,
  .cta-section {
    padding: 50px 0;
  }

  .step-number {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
  }

  .author-avatar {
    width: 45px;
    height: 45px;
  }
  
  .cta-content {
    padding: 25px;
  }
}
</style>