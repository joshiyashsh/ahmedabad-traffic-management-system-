// static/js/login.js
document.addEventListener('DOMContentLoaded', () => {
    // Handling the loading state of the authentication button
    const loginForm = document.getElementById('login-form');
    const submitBtn = document.getElementById('login-btn');

    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            // Apply loading class to trigger CSS spinner and hide text
            submitBtn.classList.add('loading');
        });
    }

    // Dynamic generation of floating background particles
    const particlesContainer = document.querySelector('.particles-container');
    if (particlesContainer) {
        const particleCount = 20; // Number of floating particles
        for (let i = 0; i < particleCount; i++) {
            createParticle(particlesContainer);
        }
    }
});

/**
 * Creates a single randomized particle and appends it to the container.
 * @param {HTMLElement} container - The DOM element to append particles to.
 */
function createParticle(container) {
    const particle = document.createElement('div');
    particle.classList.add('particle');
    
    // Randomize dimensions (size)
    const size = Math.random() * 90 + 30; // Between 30px and 120px
    
    // Randomize starting X position
    const posX = Math.random() * 100; // 0% to 100% of viewport width
    
    // Randomize animation duration for depth effect
    const duration = Math.random() * 25 + 15; // Between 15s and 40s
    
    // Randomize animation delay so they don't all spawn at once
    const delay = Math.random() * 20; // Up to 20s delay
    
    // Apply calculated styles
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    particle.style.left = `${posX}%`;
    particle.style.animationDuration = `${duration}s`;
    particle.style.animationDelay = `${delay}s`;
    
    container.appendChild(particle);
}
