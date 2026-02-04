document.getElementById('payment_button').addEventListener('click', function() {
    const paymentCheckbox = document.getElementById('online_payment');
    if (paymentCheckbox.checked) {
        // Show modal if the online payment checkbox is checked
        const paymentModal = new bootstrap.Modal(document.getElementById('paymentModal'));
        paymentModal.show();
    }
});

document.getElementById('confirmPaymentButton').addEventListener('click', function() {
    // Logic to process online payment here
    // For now, let's just log the card details to the console
    const cardNumber = document.getElementById('cardNumber').value;
    const cardExpiry = document.getElementById('cardExpiry').value;
    const cardCVC = document.getElementById('cardCVC').value;

    console.log('Processing payment with the following details:');
    console.log('Card Number:', cardNumber);
    console.log('Expiry Date:', cardExpiry);
    console.log('CVC:', cardCVC);

    // Hide modal after confirmation
    const paymentModal = bootstrap.Modal.getInstance(document.getElementById('paymentModal'));
    paymentModal.hide();
    
    // Show a success alert (you can customize this further)
    alert('Payment details confirmed. Proceeding with the payment...');
});
