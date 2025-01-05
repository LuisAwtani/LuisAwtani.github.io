async function handleSubscribe(event) {
    event.preventDefault();
    
    const emailInput = document.getElementById('emailInput');
    const email = emailInput.value;
    const button = event.target.querySelector('button');
    
    try {
        // Disable button and show loading state
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Subscribing...';
        
        const response = await fetch('http://localhost:8000', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Show success message
            emailInput.value = '';
            button.innerHTML = '<i class="fas fa-check"></i> Subscribed!';
            button.style.background = '#27ae60';
        } else {
            throw new Error(data.error);
        }
        
        // Reset button after 3 seconds
        setTimeout(() => {
            button.disabled = false;
            button.innerHTML = '<i class="fas fa-paper-plane"></i> Subscribe';
            button.style.background = '';
        }, 3000);
        
    } catch (error) {
        // Show error state
        button.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Try Again';
        button.style.background = '#e74c3c';
        
        // Reset button after 3 seconds
        setTimeout(() => {
            button.disabled = false;
            button.innerHTML = '<i class="fas fa-paper-plane"></i> Subscribe';
            button.style.background = '';
        }, 3000);
    }
    
    return false;
} 