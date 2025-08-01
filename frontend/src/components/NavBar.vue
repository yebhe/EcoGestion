<template>
  <nav class="navbar" :class="{ 'navbar-scrolled': scrolled }">
    <div class="navbar-content">
      <!-- Logo avec animation avancée -->
      <div class="navbar-logo" @mouseover="animateLogo" @mouseout="resetLogo">
        <div class="logo-container">
          <div class="logo-icon" :class="{ 'logo-animated': isLogoAnimated }">
            <span>ED</span>
            <div class="logo-particles" v-if="isLogoAnimated">
              <span v-for="n in 6" :key="n" class="particle"></span>
            </div>
          </div>
          <div class="logo-shadow"></div>
        </div>
        <router-link to="/" class="navbar-brand" :class="{ 'text-animated': isLogoAnimated }">
          <span class="brand-eco">Eco</span><span class="brand-deli">Deli</span>
        </router-link>
      </div>
      
      <!-- Navigation Links avec animations améliorées -->
      <div class="navbar-links" :class="{ 'active': menuOpen }">
        <div class="nav-group">
          <router-link to="/" class="navbar-link" @mouseover="hoverLink = 'home'" @mouseout="hoverLink = null" :class="{ 'link-hover': hoverLink === 'home' || $route.path === '/' }">
            <i class="link-icon home-icon"></i>
            <span>Accueil</span>
            <span class="link-hover-effect"></span>
          </router-link>
          
          <router-link to="/services" class="navbar-link" @mouseover="hoverLink = 'services'" @mouseout="hoverLink = null" :class="{ 'link-hover': hoverLink === 'services' || $route.path === '/services' }">
            <i class="link-icon services-icon"></i>
            <span>Services</span>
            <span class="link-hover-effect"></span>
          </router-link>
          
          
        </div>
        
        <div class="nav-actions">
          <!-- Bouton de connexion avec effet de gradient -->
          <router-link to="/login" class="login-btn pulse-effect" v-if="!authStore.isAuthenticated">
            <span>Connexion</span>
            <div class="btn-shine"></div>
          </router-link>
          
          <!-- Bouton de déconnexion avec effet de pulsation -->
          <button 
            v-if="authStore.isAuthenticated" 
            @click="handleLogout" 
            class="navbar-logout"
            :class="{ 'logout-pulse': isLoggingOut }"
          >
            <i class="logout-icon"></i>
            <span>Déconnexion</span>
          </button>
        </div>
      </div>
      
      <!-- Menu burger amélioré -->
      <div class="menu-toggle" @click="toggleMenu" :class="{ 'active': menuOpen }">
        <div class="burger-icon">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
    
    <!-- Progress bar pour indiquer le défilement de la page -->
    <div class="scroll-progress-container">
      <div class="scroll-progress" :style="{ width: scrollProgress + '%' }"></div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../store/authStore';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

// États réactifs
const scrolled = ref(false);
const scrollProgress = ref(0);
const menuOpen = ref(false);
const isLogoAnimated = ref(false);
const hoverLink = ref(null);
const isLoggingOut = ref(false);

// Méthode pour la déconnexion avec animation
const handleLogout = () => {
  isLoggingOut.value = true;
  
  // Simuler un délai pour l'animation
  setTimeout(() => {
    authStore.logout();
    isLoggingOut.value = false;
    router.push('/login');
  }, 800);
};

// Calcul du pourcentage de défilement de la page
const calculateScrollProgress = () => {
  const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  const scrolled = window.scrollY;
  
  scrollProgress.value = windowHeight ? (scrolled / windowHeight) * 100 : 0;
};

// Gestion du scroll pour les effets de navbar
const handleScroll = () => {
  scrolled.value = window.scrollY > 50;
  calculateScrollProgress();
};

// Toggle du menu mobile
const toggleMenu = () => {
  menuOpen.value = !menuOpen.value;
  document.body.style.overflow = menuOpen.value ? 'hidden' : '';
};

// Animation du logo
const animateLogo = () => {
  isLogoAnimated.value = true;
};

const resetLogo = () => {
  isLogoAnimated.value = false;
};

// Gestion des écouteurs d'événements
onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  
  // Initialiser la barre de progression
  calculateScrollProgress();
});

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
/* Styles de base */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 70px;
  z-index: 1000;
  background: linear-gradient(90deg, rgba(9,121,108,0.95) 0%, rgba(35,155,86,0.95) 100%);
  transition: all 0.4s ease;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.navbar-scrolled {
  height: 60px;
  background: linear-gradient(90deg, rgba(9,121,108,0.98) 0%, rgba(35,155,86,0.98) 100%);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
}

.navbar-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Logo styling */
.navbar-logo {
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: transform 0.3s ease;
  margin-right: 20px;
}

.navbar-logo:hover {
  transform: scale(1.05);
}

.logo-container {
  position: relative;
  margin-right: 10px;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #4CAF50, #2196F3);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 18px;
  transition: all 0.5s ease;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
}

.logo-icon.logo-animated {
  box-shadow: 0 5px 15px rgba(76, 175, 80, 0.6);
  transform: translateY(-3px) rotate(5deg);
}

.logo-shadow {
  position: absolute;
  bottom: -5px;
  left: 5px;
  width: 30px;
  height: 5px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  filter: blur(3px);
  transition: all 0.5s ease;
}

.logo-animated + .logo-shadow {
  width: 36px;
  opacity: 0.6;
}

.logo-particles .particle {
  position: absolute;
  width: 6px;
  height: 6px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 50%;
  animation: particle-animation 1s ease-out forwards;
}

.logo-particles .particle:nth-child(1) { top: 20%; left: 10%; animation-delay: 0.1s; }
.logo-particles .particle:nth-child(2) { top: 15%; right: 10%; animation-delay: 0.2s; }
.logo-particles .particle:nth-child(3) { bottom: 20%; left: 10%; animation-delay: 0.15s; }
.logo-particles .particle:nth-child(4) { bottom: 15%; right: 10%; animation-delay: 0.25s; }
.logo-particles .particle:nth-child(5) { top: 50%; left: 0; animation-delay: 0.3s; }
.logo-particles .particle:nth-child(6) { top: 50%; right: 0; animation-delay: 0.35s; }

@keyframes particle-animation {
  0% {
    transform: scale(0);
    opacity: 1;
  }
  100% {
    transform: scale(2) translate(15px, -10px) rotate(45deg);
    opacity: 0;
  }
}

.navbar-brand {
  font-size: 24px;
  font-weight: 700;
  text-decoration: none;
  color: white;
  letter-spacing: 0.5px;
  position: relative;
  transition: all 0.3s ease;
}

.brand-eco {
  color: #e0f7fa;
  transition: color 0.3s ease;
}

.brand-deli {
  color: #b2dfdb;
  transition: color 0.3s ease;
}

.text-animated .brand-eco {
  color: #ffffff;
  text-shadow: 0 0 15px rgba(255, 255, 255, 0.8);
}

.text-animated .brand-deli {
  color: #e0f7fa;
}

/* Navigation links */
.navbar-links {
  display: flex;
  align-items: center;
  height: 100%;
}

.nav-group {
  display: flex;
  align-items: center;
  height: 100%;
}

.navbar-link {
  position: relative;
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 20px;
  color: #e0f7fa;
  text-decoration: none;
  font-weight: 500;
  font-size: 16px;
  transition: all 0.3s ease;
  overflow: hidden;
}

.navbar-link:hover {
  color: white;
}

.link-icon {
  margin-right: 8px;
  font-size: 18px;
  transition: transform 0.3s ease;
}

.home-icon::before {
  content: "🏠";
}

.services-icon::before {
  content: "🛍️";
}

.how-icon::before {
  content: "❓";
}

.link-hover .link-icon {
  transform: translateY(-3px);
}

.link-hover-effect {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, #4CAF50, #2196F3);
  transform: scaleX(0);
  transform-origin: center;
  transition: transform 0.4s ease;
}

.link-hover .link-hover-effect {
  transform: scaleX(1);
}

/* Highlight active route */
.router-link-active .link-hover-effect {
  transform: scaleX(1);
}

/* Nav actions */
.nav-actions {
  display: flex;
  align-items: center;
  margin-left: 20px;
}

/* Login button */
.login-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px 20px;
  background: linear-gradient(135deg, #4CAF50, #2196F3);
  border: none;
  border-radius: 30px;
  color: white;
  font-weight: 600;
  text-decoration: none;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.4s ease;
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(33, 150, 243, 0.4);
}

.btn-shine {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    to right,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.3) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  transform: rotate(45deg);
  animation: shine 3s infinite;
}

@keyframes shine {
  0% {
    transform: translateX(-100%) rotate(45deg);
  }
  20%, 100% {
    transform: translateX(100%) rotate(45deg);
  }
}

.pulse-effect {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(76, 175, 80, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0);
  }
}

/* Logout button */
.navbar-logout {
  display: flex;
  align-items: center;
  padding: 8px 20px;
  background: linear-gradient(135deg, #FF9800, #F44336);
  border: none;
  border-radius: 30px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.3);
}

.navbar-logout:hover {
  background: linear-gradient(135deg, #FF5722, #E53935);
  transform: translateY(-2px);
}

.logout-icon {
  margin-right: 8px;
  font-size: 16px;
}

.logout-icon::before {
  content: "🚪";
}

.logout-pulse {
  animation: logout-pulse 0.8s ease-in-out;
}

@keyframes logout-pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(0.9);
    opacity: 0.7;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Mobile menu */
.menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 40px;
  height: 40px;
  cursor: pointer;
  z-index: 1001;
}

.burger-icon {
  position: relative;
  width: 30px;
  height: 22px;
}

.burger-icon span {
  position: absolute;
  height: 3px;
  width: 100%;
  background-color: white;
  border-radius: 3px;
  left: 0;
  transition: all 0.3s ease;
}

.burger-icon span:nth-child(1) {
  top: 0;
}

.burger-icon span:nth-child(2) {
  top: 9px;
}

.burger-icon span:nth-child(3) {
  top: 18px;
}

.menu-toggle.active .burger-icon span:nth-child(1) {
  transform: translateY(9px) rotate(45deg);
}

.menu-toggle.active .burger-icon span:nth-child(2) {
  opacity: 0;
}

.menu-toggle.active .burger-icon span:nth-child(3) {
  transform: translateY(-9px) rotate(-45deg);
}

/* Scroll progress bar */
.scroll-progress-container {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: rgba(255, 255, 255, 0.2);
  overflow: hidden;
}

.scroll-progress {
  height: 100%;
  background: linear-gradient(90deg, #4CAF50, #2196F3, #03A9F4);
  width: 0;
  transition: width 0.1s ease;
  position: relative;
  overflow: hidden;
}

.scroll-progress::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100px;
  background: rgba(255, 255, 255, 0.3);
  animation: progress-shine 2s infinite;
}

@keyframes progress-shine {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(400%);
  }
}

/* Responsive design */
@media (max-width: 1024px) {
  .navbar-links {
    display: none;
  }
  
  .menu-toggle {
    display: flex;
  }
  
  .navbar-links.active {
    display: flex;
    flex-direction: column;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(9,121,108,0.98) 0%, rgba(35,155,86,0.98) 100%);
    z-index: 1000;
    padding-top: 70px;
    overflow-y: auto;
    animation: slide-in 0.3s ease forwards;
  }
  
  @keyframes slide-in {
    from {
      opacity: 0;
      transform: translateY(-20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .nav-group {
    flex-direction: column;
    width: 100%;
    height: auto;
    padding: 20px 0;
  }
  
  .navbar-link {
    width: 100%;
    height: 60px;
    justify-content: center;
    padding: 15px 0;
  }
  
  .nav-actions {
    flex-direction: column;
    margin: 20px 0;
    width: 100%;
    align-items: center;
  }
  
  .login-btn, .navbar-logout {
    width: 80%;
    justify-content: center;
    margin: 10px 0;
  }
  
  .link-hover-effect {
    height: 2px;
  }
}
</style>