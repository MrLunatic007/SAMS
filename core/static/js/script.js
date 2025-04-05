// Wait for DOM to be fully loaded
document.addEventListener("DOMContentLoaded", () => {
  // Theme toggler functionality
  const themeToggler = document.querySelector(".theme-toggler");
  const lightMode = document.querySelector(".theme-toggler span:nth-child(1)");
  const darkMode = document.querySelector(".theme-toggler span:nth-child(2)");

  if (themeToggler) {
    themeToggler.addEventListener("click", () => {
      document.body.classList.toggle("dark-theme");

      // Toggle active class
      lightMode.classList.toggle("active");
      darkMode.classList.toggle("active");

      // Save theme preference to localStorage
      if (document.body.classList.contains("dark-theme")) {
        localStorage.setItem("theme", "dark");
      } else {
        localStorage.setItem("theme", "light");
      }
    });

    // Check for saved theme preference
    if (localStorage.getItem("theme") === "dark") {
      document.body.classList.add("dark-theme");
      lightMode.classList.remove("active");
      darkMode.classList.add("active");
    } else {
      lightMode.classList.add("active");
      darkMode.classList.remove("active");
    }
  }

  // Mobile menu toggle
  const menuToggle = document.querySelector(".menu-toggle");
  const navbar = document.querySelector(".navbar");

  if (menuToggle && navbar) {
    menuToggle.addEventListener("click", () => {
      navbar.classList.toggle("show");
    });
  }

  // Profile button functionality
  const profileBtn = document.getElementById("profile-btn");
  if (profileBtn) {
    profileBtn.addEventListener("click", () => {
      // Redirect to profile page
      window.location.href = "/profile/";
    });
  }

  // Notification toggle functionality
  const notificationBtn = document.getElementById("notification-btn");
  const notificationsContainer = document.querySelector(
    ".notifications-container"
  );

  if (notificationBtn && notificationsContainer) {
    notificationBtn.addEventListener("click", () => {
      notificationsContainer.classList.toggle("show");
    });

    // Close notifications when clicking outside
    document.addEventListener("click", (e) => {
      if (
        !notificationBtn.contains(e.target) &&
        !notificationsContainer.contains(e.target)
      ) {
        notificationsContainer.classList.remove("show");
      }
    });
  }

  // Set active nav item based on current URL
  setActiveNavItem();

  // Smooth scrolling for navigation links
  const navLinks = document.querySelectorAll(".page-scroll");
  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      // Add active class to clicked link
      navLinks.forEach((l) => l.classList.remove("active"));
      this.classList.add("active");

      // Add subtle animation to the link
      this.style.animation = "pulse 0.5s";
      setTimeout(() => {
        this.style.animation = "";
      }, 500);
    });
  });

  // Form toggle functionality for assignment and notice forms
  const assignBtn = document.getElementById("openbtn");
  const assignForm = document.getElementById("assign-form");

  if (assignBtn && assignForm) {
    assignBtn.addEventListener("click", () => {
      if (
        assignForm.style.display === "none" ||
        assignForm.style.display === ""
      ) {
        assignForm.style.display = "block";
        assignBtn.textContent = "Close Form";

        // Smooth scroll to form
        assignForm.scrollIntoView({ behavior: "smooth" });
      } else {
        assignForm.style.display = "none";
        assignBtn.textContent = "Create Assignment";
      }
    });
  }

  // Add animation to cards on page load
  const cards = document.querySelectorAll(
    ".assignment-card, .assignment-card-1, .notice-card-1, .eg"
  );
  cards.forEach((card, index) => {
    // Stagger the animation for a nice effect
    setTimeout(() => {
      card.style.animation = "fadeIn 0.5s ease forwards";
    }, index * 100);
  });

  // Add hover effect to table rows
  const tableRows = document.querySelectorAll("tbody tr");
  tableRows.forEach((row) => {
    row.addEventListener("mouseenter", () => {
      row.style.transition = "background-color 0.3s ease";
    });
  });

  // Form validation
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", (e) => {
      const requiredFields = form.querySelectorAll("[required]");
      let isValid = true;

      requiredFields.forEach((field) => {
        if (!field.value.trim()) {
          isValid = false;
          field.style.borderColor = "red";

          // Add shake animation to invalid fields
          field.style.animation = "shake 0.5s";
          setTimeout(() => {
            field.style.animation = "";
          }, 500);
        } else {
          field.style.borderColor = "";
        }
      });

      if (!isValid) {
        e.preventDefault();
      }
    });
  });

  // Add keyframe animation for shake effect
  const style = document.createElement("style");
  style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }
    `;
  document.head.appendChild(style);
});

// Function to set active nav item based on current URL
function setActiveNavItem() {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll(".navbar a");

  navLinks.forEach((link) => {
    // Remove active class from all links
    link.classList.remove("active");

    // Get the href attribute
    const href = link.getAttribute("href");

    // Check if the current path includes the href (excluding root path)
    if (href !== "/" && currentPath.includes(href)) {
      link.classList.add("active");
    } else if (
      href === "/" &&
      (currentPath === "/" || currentPath === "/index.html")
    ) {
      link.classList.add("active");
    }
  });

  // Special case for dashboard pages
  if (currentPath.includes("dash")) {
    const homeLink = document.querySelector('.navbar a[href*="dash"]');
    if (homeLink) homeLink.classList.add("active");
  }
}

// Function to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Function to handle notice form toggle (used in notice.html)
function Notification_Open() {
  const btn = document.getElementById("openbtn");
  const n_form = document.getElementById("notice-form");

  if (n_form.style.display === "none" || n_form.style.display === "") {
    // Show the form with animation
    n_form.style.display = "block";
    n_form.style.animation = "fadeIn 0.5s ease";
    btn.innerHTML = "Close Notice";
  } else {
    // Hide the form
    n_form.style.display = "none";
    btn.innerHTML = "Create Notice";
  }
}

// Function to handle assignment form toggle (used in assignment.html)
function Assignment_Open() {
  const btn = document.getElementById("open_btn");
  const a_form = document.getElementById("assign-form");

  if (a_form.style.display === "none" || a_form.style.display === "") {
    // Show the form with animation
    a_form.style.display = "block";
    a_form.style.animation = "fadeIn 0.5s ease";
    btn.innerHTML = "Close Assignment";
  } else {
    // Hide the form
    a_form.style.display = "none";
    btn.innerHTML = "Create Assignment";
  }
}
  