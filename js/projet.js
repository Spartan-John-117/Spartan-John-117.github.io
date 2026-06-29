document.addEventListener('DOMContentLoaded', () => {
    // 1. Get Project ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    const projectId = urlParams.get('id');

    const titleEl = document.getElementById('proj-title');
    const domainEl = document.getElementById('proj-domain');
    const techsEl = document.getElementById('proj-techs');
    const contentEl = document.getElementById('proj-content');

    const showError = () => {
        titleEl.textContent = "ACCÈS REFUSÉ";
        titleEl.setAttribute('data-text', "ACCÈS REFUSÉ");
        domainEl.textContent = "Erreur 404 - Archive introuvable";
        contentEl.innerHTML = `
            <div class="error-message">
                <i class="ph ph-warning-octagon" style="font-size: 4rem; display: block; margin-bottom: 20px;"></i>
                Le rapport demandé n'existe pas ou a été classifié.
            </div>
        `;
    };

    // SECURITY: Validate projectId to prevent DOM XSS / Path Traversal
    // Only allow alphanumeric characters and dashes
    const isValidId = /^[a-zA-Z0-9-]+$/.test(projectId);

    if (!projectId || !isValidId) {
        showError();
        return;
    }

    // 2. Load Project Script Dynamically
    const script = document.createElement('script');
    script.src = `js/data/projects/${projectId}.js`;
    
    script.onload = () => {
        // 3. Load Project Data
        const project = window.projectData && window.projectData[projectId];
        if (!project) {
            showError();
            return;
        }

        // Populate Header
        titleEl.textContent = project.title;
        titleEl.setAttribute('data-text', project.title);
        domainEl.textContent = project.domain;

        // Update Back Link to point to specific section
        const domainToSectionId = {
            "Cybersécurité": "cyber",
            "Administration Système": "admin",
            "Développement": "dev",
            "Cryptographie": "crypto",
            "Bases de Données": "bdd",
            "Détection d'Intrusions": "ids"
        };
        
        const backLink = document.querySelector('.back-link');
        if (backLink && domainToSectionId[project.domain]) {
            backLink.href = `projets.html#${domainToSectionId[project.domain]}`;
        }

        // Populate Technologies
        if (project.technologies && project.technologies.length > 0) {
            project.technologies.forEach(tech => {
                const span = document.createElement('span');
                span.className = 'meta-tag';
                span.textContent = tech;
                techsEl.appendChild(span);
            });
        }

        // Populate Content
        if (window.marked) {
            contentEl.innerHTML = marked.parse(project.content);
            if (window.hljs) {
                contentEl.querySelectorAll('pre code').forEach((block) => {
                    hljs.highlightElement(block);
                });
            }
        } else {
            contentEl.innerHTML = `<pre><code>${project.content.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</code></pre>`;
        }
    };

    script.onerror = () => {
        showError();
    };

    document.head.appendChild(script);
});
