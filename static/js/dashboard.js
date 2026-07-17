// static/js/dashboard.js
document.addEventListener('DOMContentLoaded', () => {
    // 1. Progress Bar Animation
    // We use a short timeout to ensure the DOM is painted so the CSS transition triggers
    setTimeout(() => {
        const progressBars = document.querySelectorAll('.custom-progress-bar');
        progressBars.forEach(bar => {
            const targetWidth = bar.getAttribute('data-target');
            if (targetWidth) {
                bar.style.width = targetWidth;
            }
        });
    }, 300);

    // 2. Animated Counters for Metric Cards
    const counters = document.querySelectorAll('.counter-anim');
    counters.forEach(counter => {
        const target = parseFloat(counter.getAttribute('data-count'));
        const isPercentage = counter.hasAttribute('data-percentage');
        const duration = 1500; // Animation duration in milliseconds
        const frames = 60; // Approximate frames
        const stepTime = Math.abs(Math.floor(duration / frames));
        let current = 0;
        const step = target / frames;

        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            
            // Format output
            const displayValue = Math.floor(current);
            if (isPercentage) {
                counter.innerText = displayValue + '%';
            } else {
                counter.innerText = displayValue;
            }
        }, stepTime);
    });
});
