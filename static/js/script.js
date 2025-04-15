// Main JavaScript file for Gym Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // BMI Calculator functionality (if on add customer page)
    const weightInput = document.getElementById('weight');
    const heightInput = document.getElementById('height');
    const bmiDisplay = document.getElementById('bmi-display');

    if (weightInput && heightInput && bmiDisplay) {
        const calculateBMI = () => {
            const weight = parseFloat(weightInput.value);
            const height = parseFloat(heightInput.value) / 100; // Convert cm to meters
            
            if (weight > 0 && height > 0) {
                const bmi = (weight / (height * height)).toFixed(1);
                let category = '';
                
                if (bmi < 18.5) {
                    category = 'Underweight';
                } else if (bmi < 25) {
                    category = 'Normal weight';
                } else if (bmi < 30) {
                    category = 'Overweight';
                } else {
                    category = 'Obese';
                }
                
                bmiDisplay.textContent = `BMI: ${bmi} (${category})`;
                bmiDisplay.style.display = 'block';
            }
        };
        
        weightInput.addEventListener('input', calculateBMI);
        heightInput.addEventListener('input', calculateBMI);
    }

    // Plan selection affects amount field
    const planSelect = document.getElementById('plan_type');
    const amountInput = document.getElementById('amount');

    if (planSelect && amountInput) {
        planSelect.addEventListener('change', function() {
            const planType = this.value;
            
            // Suggested amounts based on plan type
            if (planType === 'monthly') {
                amountInput.value = '1500';
            } else if (planType === 'quarterly') {
                amountInput.value = '4000';
            } else if (planType === 'yearly') {
                amountInput.value = '12000';
            }
        });
    }

    // Auto close alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.remove('show');
            
            setTimeout(() => {
                alert.remove();
            }, 150);
        }, 5000);
    });
});