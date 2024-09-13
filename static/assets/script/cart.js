document.addEventListener('DOMContentLoaded', function () {
    const quantityInput = document.getElementById('quantity-input');
    const increaseBtn = document.querySelector('.increase-btn');
    const decreaseBtn = document.querySelector('.decrease-btn');
    const addToCartBtn = document.getElementById('add-to-cart-btn');

    increaseBtn.addEventListener('click', function () {
        let currentQuantity = parseInt(quantityInput.value);
        quantityInput.value = currentQuantity + 1;
    });

    decreaseBtn.addEventListener('click', function () {
        let currentQuantity = parseInt(quantityInput.value);
        if (currentQuantity > 1) {
            quantityInput.value = currentQuantity - 1;
        }
    });

    addToCartBtn.addEventListener('click', function () {
        const medicineId = addToCartBtn.dataset.medicineId;
        const quantity = quantityInput.value;

        // Send AJAX request to update the backend
        fetch(`/update_cart/${medicineId}/${quantity}/`)
            .then(response => {
                if (response.ok) {
                    // Cart updated successfully
                    console.log('Cart updated successfully');
                } else {
                    // Error occurred while updating cart
                    console.error('Error occurred while updating cart');
                }
            })
            .catch(error => {
                console.error('Error occurred:', error);
            });
    });
});



// Path: static/assets/script/checkout.js
// Assuming you have jQuery included
document.addEventListener("DOMContentLoaded", function() {
    const decreaseButtons = document.querySelectorAll(".action-btn.decrease");
    const increaseButtons = document.querySelectorAll(".action-btn.increase");

    decreaseButtons.forEach(button => {
        button.addEventListener("click", function() {
            const quantityElement = button.nextElementSibling;
            let quantity = parseInt(quantityElement.textContent);
            if (quantity > 1) {
                quantity--;
                quantityElement.textContent = quantity;
            }
        });
    });

    increaseButtons.forEach(button => {
        button.addEventListener("click", function() {
            const quantityElement = button.previousElementSibling;
            let quantity = parseInt(quantityElement.textContent);
            quantity++;
            quantityElement.textContent = quantity;
        });
    });
});
