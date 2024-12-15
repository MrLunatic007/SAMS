document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.form-container');
    const inputs = document.querySelectorAll('.u-input');

    // Function to check if any input has value
    const hasInputValue = () => {
        return Array.from(inputs).some(input => input.value.trim() !== '');
    };

    // Handle input changes
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            if (hasInputValue()) {
                form.classList.add('has-value');
            } else {
                form.classList.remove('has-value');
            }
        });
    });

    // Handle clicks outside the form
    document.addEventListener('click', (event) => {
        const isClickInside = form.contains(event.target);
        
        if (!isClickInside && !hasInputValue()) {
            form.classList.remove('has-value');
        }
    });
});