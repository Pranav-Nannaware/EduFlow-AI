// Quiz interaction
document.addEventListener('DOMContentLoaded', function() {
    // Handle quiz option selection
    const quizOptions = document.querySelectorAll('.quiz-option');
    if (quizOptions.length > 0) {
        quizOptions.forEach(option => {
            option.addEventListener('click', function() {
                // Remove selected class from other options in the same question
                const questionId = this.dataset.question;
                document.querySelectorAll(`.quiz-option[data-question="${questionId}"]`).forEach(opt => {
                    opt.classList.remove('selected');
                });
                
                // Add selected class to clicked option
                this.classList.add('selected');
                
                // Set the hidden input value
                document.querySelector(`input[name="q${questionId}"]`).value = this.dataset.answer;
            });
        });
    }

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    if (forms.length > 0) {
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }

    // Auto-scroll chat to bottom
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Course detail tabs
    const courseDetailTabs = document.querySelectorAll('#courseDetailTabs .nav-link');
    if (courseDetailTabs.length > 0) {
        courseDetailTabs.forEach(tab => {
            tab.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Remove active class from all tabs
                courseDetailTabs.forEach(t => t.classList.remove('active'));
                
                // Add active class to clicked tab
                this.classList.add('active');
                
                // Hide all tab content
                document.querySelectorAll('.tab-pane').forEach(pane => {
                    pane.classList.remove('show', 'active');
                });
                
                // Show clicked tab content
                const target = this.getAttribute('href');
                document.querySelector(target).classList.add('show', 'active');
            });
        });
    }

    // Toggle password visibility
    const togglePassword = document.querySelector('#togglePassword');
    if (togglePassword) {
        togglePassword.addEventListener('click', function() {
            const passwordInput = document.querySelector('#password');
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            // Toggle icon
            this.querySelector('i').classList.toggle('fa-eye');
            this.querySelector('i').classList.toggle('fa-eye-slash');
        });
    }

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    if (tooltipTriggerList.length > 0) {
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});

// Animate dashboard cards on scroll
function animateOnScroll() {
    const elements = document.querySelectorAll('.animate-on-scroll');
    
    elements.forEach(element => {
        const position = element.getBoundingClientRect();
        
        // Check if element is in viewport
        if(position.top < window.innerHeight && position.bottom >= 0) {
            element.classList.add('animated');
        }
    });
}

// Add event listener for scroll
window.addEventListener('scroll', animateOnScroll);
// Initial check on page load
document.addEventListener('DOMContentLoaded', animateOnScroll); 