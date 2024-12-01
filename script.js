// Відкрити модальне вікно для вибору продукту
document.getElementById("getTicketBtn").addEventListener("click", () => {
    document.getElementById("productModal").style.display = "block";
});

// Закрити модальне вікно для вибору продукту
document.getElementById("closeProductModal").addEventListener("click", () => {
    document.getElementById("productModal").style.display = "none";
});

// Відкрити модальне вікно для оплати
document.getElementById("getProductBtn").addEventListener("click", () => {
    const productSelect = document.getElementById("productSelect");
    const selectedOption = productSelect.options[productSelect.selectedIndex].text;

    document.getElementById("selectedProduct").innerText = selectedOption.split('(')[0].trim();
    document.getElementById("paymentAmount").innerText = selectedOption.match(/\(([^)]+)\)/)[1];
    document.getElementById("productModal").style.display = "none";
    document.getElementById("paymentModal").style.display = "block";
});

// Закрити модальне вікно для оплати
document.getElementById("closePaymentModal").addEventListener("click", () => {
    document.getElementById("paymentModal").style.display = "none";
});

// Обробка способу оплати
document.getElementById("confirmPaymentBtn").addEventListener("click", () => {
    const paymentMethod = document.querySelector('input[name="paymentMethod"]:checked');
    if (!paymentMethod) {
        alert("Будь ласка, виберіть спосіб оплати.");
        return;
    }

    if (paymentMethod.value === "card") {
        document.getElementById("paymentModal").style.display = "none";
        document.getElementById("cardPaymentModal").style.display = "block";
    } else if (paymentMethod.value === "paypal") {
        alert("Використовуйте PayPal для оплати.");
        // Тут можна інтегрувати API PayPal
    } else if (paymentMethod.value === "googlepay") {
        alert("Google Pay тимчасово недоступний.");
    }
});

// Закрити модальне вікно для введення карткових даних
document.getElementById("closeCardPaymentModal").addEventListener("click", () => {
    document.getElementById("cardPaymentModal").style.display = "none";
});

// Обробка оплати карткою
document.getElementById("cardPaymentForm").addEventListener("submit", (event) => {
    event.preventDefault();
    alert("Оплата успішно здійснена!");
    document.getElementById("cardPaymentModal").style.display = "none";
});


const themeToggleBtn = document.getElementById("themeToggleBtn");

themeToggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark-theme");
});


const targetDate = new Date("2024-11-20T00:00:00").getTime();

const timerInterval = setInterval(() => {
    const now = new Date().getTime();
    const timeLeft = targetDate - now;

    if (timeLeft <= 0) {
        clearInterval(timerInterval);
        document.getElementById("timer").innerText = "Квитки вже у продажу!";
        return;
    }

    const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

    document.getElementById("timer").innerText = `${days}д ${hours}г ${minutes}хв ${seconds}с`;
}, 1000);


document.getElementById("subscribeForm").addEventListener("submit", (event) => {
    event.preventDefault();
    const email = document.getElementById("emailInput").value;

    if (email) {
        document.getElementById("subscribeMessage").innerText = `Дякуємо за підписку, ${email}!`;
        document.getElementById("subscribeForm").reset();
    } else {
        document.getElementById("subscribeMessage").innerText = "Будь ласка, введіть коректний email.";
    }
});

const searchInput = document.getElementById("searchInput");
const productRows = document.querySelectorAll("tbody tr");

searchInput.addEventListener("input", () => {
    const filter = searchInput.value.toLowerCase();

    productRows.forEach((row) => {
        const productName = row.querySelector("td:first-child").textContent.toLowerCase();
        row.style.display = productName.includes(filter) ? "" : "none";
    });
});


let ticketsSold = 0;

document.getElementById("getProductBtn").addEventListener("click", () => {
    ticketsSold += 1;
    document.getElementById("ticketsSold").innerText = `Продано квитків: ${ticketsSold}`;
});


window.addEventListener("load", () => {
    const progress = document.getElementById("progress");
    let width = 0;

    const interval = setInterval(() => {
        if (width >= 100) {
            clearInterval(interval);
            progress.style.width = "100%";
        } else {
            width += 10;
            progress.style.width = `${width}%`;
        }
    }, 100);
});



const cardPaymentForm = document.getElementById("cardPaymentForm");

cardPaymentForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const cardNumber = document.getElementById("cardNumber").value.trim();
    const expiryDate = document.getElementById("expiryDate").value.trim();
    const cvv = document.getElementById("cvv").value.trim();

    if (!cardNumber || !expiryDate || !cvv) {
        alert("Будь ласка, заповніть усі поля!");
    } else {
        alert("Оплата успішна!");
        cardPaymentForm.reset();
    }
});

const themeToggle = document.getElementById("themeToggle");

themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-theme");
    document.body.classList.toggle("light-theme");
});


function rateConcert(elementId, rating) {
    document.getElementById(elementId).textContent = rating;
}


function rateConcert2(elementId, rating) {
    document.getElementById(elementId).textContent = rating;
}

productSelect.addEventListener('change', () => {
    console.log(`Selected product price: $${productSelect.value}`);
});


paypal.Buttons({
    createOrder: function(data, actions) {
        return actions.order.create({
            purchase_units: [{
                amount: {
                    value: '10.00' // Змінити на потрібну суму
                }
            }]
        });
    },
    onApprove: function(data, actions) {
        return actions.order.capture().then(function(details) {
            alert('Transaction completed by ' + details.payer.name.given_name);
            console.log(details);

            // Показати кнопку Google Pay
            document.getElementById('google-pay-container').style.display = 'block';
            onGooglePayLoaded();
        });
    },
    onError: function(err) {
        console.error(err);
    }
}).render('#paypal-button-container');
