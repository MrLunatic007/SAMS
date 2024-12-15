document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide icons
    lucide.createIcons();

    const sideMenu = document.querySelector("aside");
    const menuBtn = document.querySelector("#menu-btn");
    const closeBtn = document.querySelector("#close-btn");
    const themeToggler = document.querySelector(".theme-toggler");
    const mainContent = document.querySelector("main");

    // Navigation links
    const navLinks = {
        dashboard: '/pages/dashboard.html',
        students: '/pages/students.html',
        schedule: '/pages/schedule.html',
        assignments: '/pages/assignments.html',
        analytics: '/pages/analytics.html',
        settings: '/pages/settings.html'
    };

    // Show sidebar
    menuBtn?.addEventListener('click', () => {
        if (sideMenu) sideMenu.style.display = 'block';
    });

    // Close sidebar
    closeBtn?.addEventListener('click', () => {
        if (sideMenu) sideMenu.style.display = 'none';
    });

    // Change theme
    themeToggler?.addEventListener('click', () => {
        document.body.classList.toggle('dark-theme-variables');

        const sunIcon = themeToggler.querySelector('i:nth-child(1)');
        const moonIcon = themeToggler.querySelector('i:nth-child(2)');
        
        if (sunIcon && moonIcon) {
            sunIcon.classList.toggle('active');
            moonIcon.classList.toggle('active');
        }
    });

    // Handle navigation
    document.querySelectorAll('.sidebar a').forEach(link => {
        link.addEventListener('click', async (e) => {
            e.preventDefault();
            
            // Remove active class from all links
            document.querySelectorAll('.sidebar a').forEach(l => l.classList.remove('active'));
            
            // Add active class to clicked link
            link.classList.add('active');
            
            // Get the page name from the link's text
            const pageName = link.querySelector('h3').textContent.toLowerCase();
            
            if (navLinks[pageName]) {
                try {
                    const response = await fetch(navLinks[pageName]);
                    const html = await response.text();
                    
                    if (mainContent) {
                        mainContent.innerHTML = html;
                        // Reinitialize Lucide icons for new content
                        lucide.createIcons();
                        
                        // Update page title
                        document.title = `${pageName.charAt(0).toUpperCase() + pageName.slice(1)} - TeachBoard`;
                        
                        // Close sidebar on mobile after navigation
                        if (window.innerWidth <= 768) {
                            sideMenu.style.display = 'none';
                        }
                    }
                } catch (error) {
                    console.error('Error loading page:', error);
                }
            }
        });
    });

    // Update progress circles
    const updateProgressCircles = () => {
        const circles = document.querySelectorAll('.insights .progress svg circle');
        circles.forEach(circle => {
            const percent = circle.parentElement.parentElement.querySelector('.number p').textContent;
            const radius = circle.r.baseVal.value;
            const circumference = radius * 2 * Math.PI;
            const offset = circumference - (parseFloat(percent) / 100 * circumference);
            
            circle.style.strokeDasharray = `${circumference} ${circumference}`;
            circle.style.strokeDashoffset = offset;
        });
    };

    // Call initially and after content updates
    updateProgressCircles();
});