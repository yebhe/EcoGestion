import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../pages/LoginPage.vue';
import Home from '../pages/Home.vue';
import RegisterPage from '../pages/RegisterPage.vue';
import Activation from '../components/Activation.vue';
import ActivateAccount from '../components/ActivateAccount.vue';
import PageNotFound from '../components/PageNotFound.vue';
import PasswordReset from '../components/PasswordReset.vue';
import { useAuthStore } from '../store/authStore';
import UpdatePassword from '../components/UpdatePassword.vue';
import AdminDashboard from '../components/admin/AdminDashboard.vue';
import UpdateProfile from '../components/UpdateProfile.vue';
import CommercantDashboard from '../components/commercant/CommercantDashboard.vue';
import LivreurDashboard from '../components/Livreur/LivreurDashboard.vue';
import PrestateurDashboard from '../components/prestateur/PrestateurDashboard.vue';
import AnnonceLivreur from '../components/Livreur/AnnonceLivreur.vue';
import CreeAnnonce from '../components/Livreur/CreeAnnonce.vue';
import Justificatifs from '../components/Livreur/Justificatifs.vue';
import Livraisons from '../components/Livreur/Livraisons.vue';
import PaiementLivreur from '../components/Livreur/PaiementLivreur.vue';
import PlaningLivreur from '../components/Livreur/PlaningLivreur.vue';
import AnnonceClient from '../components/client/AnnonceClient.vue';
import ClientDashboard from '../components/client/ClientDashboard.vue';
import SuiviColis from '../components/client/SuiviColis.vue';
import Services from '../pages/Services.vue';
import FactureClient from '../components/client/FactureClient.vue';


const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/services', name: 'services', component: Services },
  { path: '/login', name: 'LoginPage', component: LoginPage },
  { path: '/register', name: 'RegisterPage', component: RegisterPage },
  { path: '/activation/result', name: 'activation', component: Activation },
  { path: '/activate/:uidb64/:token', component: ActivateAccount },
  { path: '/password-reset/:uidb64/:token/', component: PasswordReset },
  { path: '/update-profile', component: UpdateProfile, meta: { requiresAuth: true} },

  { path: '/update-password', component: UpdatePassword, meta: 
    {
     requiresAuth: true,
    }
  },

  { path: '/:pathMatch(.*)*', name: 'NotFound', component: PageNotFound, },

  // les routes admin
  { path: '/admin-dashboard', component: AdminDashboard, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/client-dashboard', component: ClientDashboard, meta: { requiresAuth: true, requiresClient: true } },
  { path: '/commercant-dashboard', component: CommercantDashboard, meta: { requiresAuth: true, requiresCommercant: true } },
  { path: '/livreur-dashboard', component: LivreurDashboard, meta: { requiresAuth: true, requiresLivreur: true } },
  { path: '/prestateur-dashboard', component: PrestateurDashboard, meta: { requiresAuth: true, requiresPrestataire: true } },
  
  
  // Livreur
  { path: '/livreur/cree-annonce', component: CreeAnnonce, meta: { requiresAuth: true, requiresLivreur: true } },
  { path: '/livreur/annonces', component: AnnonceLivreur, meta: { requiresAuth: true, requiresLivreur: true } },
  { path: '/livreur/justificatifs', component: Justificatifs, meta: { requiresAuth: true, requiresLivreur: true } },
  { path: '/livreur/livraisons', component: Livraisons, meta: { requiresAuth: true, requiresLivreur: true } },
  { path: '/livreur/paiements', component: PaiementLivreur, meta: { requiresAuth: true, requiresLivreur: true } },
  { path: '/livreur/planning', component: PlaningLivreur, meta: { requiresAuth: true, requiresLivreur: true } },

  // client
  { path: '/client/annonces', component: AnnonceClient, meta: { requiresAuth: true, requiresClient: true } },
  { path: '/client/factures', component: FactureClient, meta: { requiresAuth: true, requiresClient: true } },
  { path: '/client/suivi', component: SuiviColis, meta: { requiresAuth: true, requiresClient: true } },


];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Si l'utilisateur n'est pas authentifié
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next('/login');
  }

  // Si la route demande un admin
  if (to.meta.requiresAdmin && authStore.userRole !== 'admin') {
    return next('/');
  }

  // Si la route demande un livreur
  if (to.meta.requiresLivreur && authStore.userRole !== 'livreur') {
    return next('/');
  }

  // Si la route demande un client
  if (to.meta.requiresClient && authStore.userRole !== 'client') {
    return next('/');
  }

  // Si la route demande un commerçant
  if (to.meta.requiresCommercant && authStore.userRole !== 'commercant') {
    return next('/');
  }

  // Si la route demande un prestataire
  if (to.meta.requiresPrestataire && authStore.userRole !== 'prestataire') {
    return next('/');
  }

  next();
});

export default router;
