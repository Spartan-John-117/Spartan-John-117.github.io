/**
 * HALO INFINITE PORTFOLIO - MAIN JS
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Smooth Scrolling for Navigation Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if(targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if(targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // Offset for fixed header
                    behavior: 'smooth'
                });
            }
        });
    });

    // 2. Glitch Effect on Hero Title — layout-stable overlay technique
    const title = document.querySelector('.title-glitch');
    if (title) {
        const originalText = title.getAttribute('data-text');
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&';

        // Build structure: invisible anchor (holds the space) + visible overlay (scrambles)
        title.textContent = '';
        title.style.position = 'relative';

        // Anchor: always contains the original text, invisible — fixes the h1 size
        const anchor = document.createElement('span');
        anchor.textContent = originalText;
        anchor.style.visibility = 'hidden';
        anchor.style.userSelect = 'none';
        anchor.setAttribute('aria-hidden', 'true');

        // Overlay: absolutely positioned on top, shows the scrambled text
        const display = document.createElement('span');
        display.textContent = originalText;
        display.style.position = 'absolute';
        display.style.left = '0';
        display.style.top = '0';
        display.style.width = '100%';

        title.appendChild(anchor);
        title.appendChild(display);

        let iterations = 0;
        setTimeout(() => {
            const interval = setInterval(() => {
                display.textContent = originalText.split('')
                    .map((char, index) => {
                        if (index < iterations) return originalText[index];
                        if (char === ' ') return ' ';
                        return chars[Math.floor(Math.random() * chars.length)];
                    })
                    .join('');

                if (iterations >= originalText.length) {
                    clearInterval(interval);
                    display.textContent = originalText;
                }
                iterations += 1/3;
            }, 30);
        }, 500);
    }

    // 3. System boot up sequence text (Typewriter)
    const subtitle = document.querySelector('.hero-text .subtitle');
    if (subtitle) {
        const text = subtitle.innerText;
        subtitle.innerText = '';
        let i = 0;
        
        function typeWriter() {
            if (i < text.length) {
                subtitle.innerHTML += text.charAt(i);
                i++;
                setTimeout(typeWriter, 50);
            }
        }
        setTimeout(typeWriter, 1500); // Start typing after glitch finishes
    }

    // 4. Reveal elements on scroll (HUD loading effect)
    const revealElements = document.querySelectorAll('.glass-panel, .section-title');

    const revealOptions = {
        threshold: 0.05,
        rootMargin: "0px 0px 0px 0px"
    };

    const revealOnScroll = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add('revealed');
            observer.unobserve(entry.target);
        });
    }, revealOptions);

    revealElements.forEach(el => {
        el.classList.add('reveal-hidden');
        revealOnScroll.observe(el);
    });

    // Fallback : révèle tout ce qui reste caché après 2s
    setTimeout(() => {
        document.querySelectorAll('.reveal-hidden:not(.revealed)').forEach(el => {
            el.classList.add('revealed');
        });
    }, 2000);
});
