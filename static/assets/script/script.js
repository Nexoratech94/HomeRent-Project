const line1 = document.querySelector('.line1');
const line2 = document.querySelector('.line2');
const line3 = document.querySelector('.line3');
const sidebar = document.querySelector('.nav-list');


const showMenu = () => {
    line1.classList.toggle('active');
    line2.classList.toggle('active');
    line3.classList.toggle('active');
    sidebar.classList.toggle("active")

}


TweenMax.from('.na', 1, {
    delay: .3,
    x: -40,
    opacity: 0,
    ease: Expo.easeInOut
})




TweenMax.from('.text', 2, {
    delay: .1,
    y: -100,
    opacity: 0,
    ease: Expo.easeInOut
})
TweenMax.from('.big-button', 3, {
    delay: .1,
    y: 20,
    opacity: 0,
    ease: Expo.easeInOut
})

TweenMax.from('.cta', 4, {
    delay: .3,
    y: 20,
    opacity: 0,
    ease: Expo.easeInOut
})

TweenMax.from('.product-info', 6, {
    delay: 0.3,
    x: -100,
    opacity: 0,
    ease: Expo.easeInOut
})
TweenMax.from('.benefits', 7, {
    delay: 0.01,
    y: 70,
    opacity: 0,
    ease: Expo.easeInOut
})




function animateElements() {
    const elementsToAnimate = document.querySelectorAll('.custom-card, .custom-title, .custom-cart, .custom-summary, .custom-row, .custom-close, .custom-img, .custom-back-to-shop, .custom-h5, .custom-hr, .custom-form, .custom-select, .custom-input, .custom-btn, .custom-a, .custom-code');

    elementsToAnimate.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(-20px)';
    });

    let delay = 0;
    elementsToAnimate.forEach(element => {
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, delay);
        delay += 100; // Adjust this value for the desired animation delay
    });
}

// Call the animateElements function when the page loads
window.onload = animateElements;




//room page animation 

// Calculate delay and duration based on screen width
function animatePropertyContainer() {
    const screenWidth = window.innerWidth;
    let delay = 0.3;
    let duration = 1;

    if (screenWidth <= 768) {
        delay = 0.1;
        duration = 0.8;
    }

    TweenMax.fromTo('.property-container', duration, {
        y: -40,
        opacity: 0
    }, {
        delay: delay,
        y: 0,
        opacity: 1,
        ease: Expo.easeInOut
    });
}

animatePropertyContainer();

// Get all property cards
const propertyCards = document.querySelectorAll('.property-card');

// Add hover effect animation to each card
propertyCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'scale(1.06)';
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'scale(1)';
    });
});





//room page animation
