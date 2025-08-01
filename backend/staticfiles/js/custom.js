// Animations JavaScript pour Jazzmin
document.addEventListener('DOMContentLoaded', function() {
    // Animation des éléments au chargement de la page
    const animateOnLoad = () => {
        const elements = document.querySelectorAll('.card, .nav-item, .btn');
        elements.forEach((el, index) => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            setTimeout(() => {
                el.style.transition = 'all 0.5s ease';
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }, index * 100);
        });
    };

    // Animation du menu latéral
    const initSidebarAnimation = () => {
        const toggleBtn = document.querySelector('.nav-link[data-widget="pushmenu"]');
        const body = document.querySelector('body');
        
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                body.classList.toggle('sidebar-open');
            });
        }
    };

    // Animation des notifications
    const createNotification = (message, type = 'success') => {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} notification`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 500);
        }, 3000);
    };

    // Animation des boutons
    const initButtonAnimations = () => {
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(btn => {
            btn.addEventListener('click', function(e) {
                const x = e.clientX - this.offsetLeft;
                const y = e.clientY - this.offsetTop;
                
                const ripple = document.createElement('span');
                ripple.className = 'ripple';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                
                this.appendChild(ripple);
                setTimeout(() => ripple.remove(), 600);
            });
        });
    };

    // Animation de la barre de recherche
    const initSearchAnimation = () => {
        const searchInput = document.querySelector('.form-control-navbar');
        if (searchInput) {
            searchInput.addEventListener('focus', () => {
                searchInput.parentElement.classList.add('search-focused');
            });
            
            searchInput.addEventListener('blur', () => {
                searchInput.parentElement.classList.remove('search-focused');
            });
        }
    };

    // Animation des cartes au défilement
    const initScrollAnimations = () => {
        const cards = document.querySelectorAll('.card');
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('card-visible');
                    }
                });
            },
            { threshold: 0.1 }
        );

        cards.forEach(card => observer.observe(card));
    };

    // Animation des tableaux
    const initTableAnimations = () => {
        const tables = document.querySelectorAll('.table');
        tables.forEach(table => {
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach((row, index) => {
                row.style.opacity = '0';
                row.style.transform = 'translateX(-20px)';
                setTimeout(() => {
                    row.style.transition = 'all 0.3s ease';
                    row.style.opacity = '1';
                    row.style.transform = 'translateX(0)';
                }, index * 50);
            });
        });
    };

    // Initialisation de toutes les animations
    animateOnLoad();
    initSidebarAnimation();
    initButtonAnimations();
    initSearchAnimation();
    initScrollAnimations();
    initTableAnimations();

    // Exposer la fonction de notification pour une utilisation globale
    window.createNotification = createNotification;
});



// ... (code JavaScript précédent) ...

// Animation des menus déroulants
const initDropdownAnimations = () => {
    const dropdowns = document.querySelectorAll('.dropdown');
    
    dropdowns.forEach(dropdown => {
        const menu = dropdown.querySelector('.dropdown-menu');
        const items = dropdown.querySelectorAll('.dropdown-item');
        
        dropdown.addEventListener('show.bs.dropdown', () => {
            // Animation séquentielle des items
            items.forEach((item, index) => {
                item.style.opacity = '0';
                item.style.transform = 'translateX(-10px)';
                setTimeout(() => {
                    item.style.transition = 'all 0.3s ease';
                    item.style.opacity = '1';
                    item.style.transform = 'translateX(0)';
                }, index * 50);
            });
        });
    });
};

// Animation du profil
const initProfileAnimation = () => {
    const userPanel = document.querySelector('.user-panel');
    if (userPanel) {
        userPanel.addEventListener('mouseenter', () => {
            const img = userPanel.querySelector('img');
            if (img) {
                img.style.transform = 'rotate(360deg)';
            }
        });
        
        userPanel.addEventListener('mouseleave', () => {
            const img = userPanel.querySelector('img');
            if (img) {
                img.style.transform = 'rotate(0deg)';
            }
        });
    }
};

// Animation du logo
const initLogoAnimation = () => {
    const logo = document.querySelector('.brand-logo');
    if (logo) {
        let isAnimating = false;
        
        logo.addEventListener('mouseenter', () => {
            if (!isAnimating) {
                isAnimating = true;
                logo.style.transform = 'scale(1.05)';
                
                setTimeout(() => {
                    logo.style.transform = 'scale(1)';
                    isAnimating = false;
                }, 300);
            }
        });
    }
};

// Initialisation des nouvelles animations
document.addEventListener('DOMContentLoaded', function() {
    // ... (initialisation précédente) ...
    initDropdownAnimations();
    initProfileAnimation();
    initLogoAnimation();
});




document.addEventListener('DOMContentLoaded', function() {
    // Animation améliorée des dropdowns
    const initEnhancedDropdowns = () => {
        const dropdowns = document.querySelectorAll('.dropdown');
        
        dropdowns.forEach(dropdown => {
            const menu = dropdown.querySelector('.dropdown-menu');
            const items = dropdown.querySelectorAll('.dropdown-item');
            
            dropdown.addEventListener('show.bs.dropdown', () => {
                // Animation séquentielle avec délai
                items.forEach((item, index) => {
                    item.style.opacity = '0';
                    item.style.transform = 'translateX(-20px)';
                    setTimeout(() => {
                        item.style.transition = 'all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
                        item.style.opacity = '1';
                        item.style.transform = 'translateX(0)';
                    }, index * 80);
                });
            });

            // Effet de hover dynamique
            items.forEach(item => {
                item.addEventListener('mouseenter', () => {
                    const icon = item.querySelector('i');
                    if (icon) {
                        icon.style.transform = 'scale(1.2) rotate(15deg)';
                    }
                });

                item.addEventListener('mouseleave', () => {
                    const icon = item.querySelector('i');
                    if (icon) {
                        icon.style.transform = 'scale(1) rotate(0)';
                    }
                });
            });
        });
    };

    // Animation améliorée du profil
    const initEnhancedProfile = () => {
        const userHeader = document.querySelector('.user-header');
        if (userHeader) {
            const img = userHeader.querySelector('.user-image');
            const name = userHeader.querySelector('.user-name');

            // Animation au survol
            userHeader.addEventListener('mouseenter', () => {
                img.style.transform = 'scale(1.1) rotate(5deg)';
                name.style.transform = 'translateY(-2px)';
            });

            userHeader.addEventListener('mouseleave', () => {
                img.style.transform = 'scale(1) rotate(0)';
                name.style.transform = 'translateY(0)';
            });

            // Animation périodique subtile
            setInterval(() => {
                img.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    img.style.transform = 'scale(1)';
                }, 200);
            }, 5000);
        }
    };

    // Effet de vague pour les clics
    const initRippleEffect = () => {
        const buttons = document.querySelectorAll('.dropdown-item, .user-header');
        
        buttons.forEach(button => {
            button.addEventListener('click', (e) => {
                const ripple = document.createElement('div');
                ripple.className = 'ripple-effect';
                
                const rect = button.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                
                button.appendChild(ripple);
                
                setTimeout(() => ripple.remove(), 600);
            });
        });
    };

    // Initialisation des nouvelles animations
    initEnhancedDropdowns();
    initEnhancedProfile();
    initRippleEffect();
});