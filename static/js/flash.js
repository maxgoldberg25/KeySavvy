document.addEventListener('DOMContentLoaded', function() {
    var flashMessage = document.querySelector('.flash-message');
    if (flashMessage) {
        setTimeout(function() {
            flashMessage.remove();
        }, 2000);
    }
});

function clearCart() {
    // Add logic to clear the cart here, such as making an AJAX request to the server
    alert('Cart cleared!'); // Placeholder for demonstration
}