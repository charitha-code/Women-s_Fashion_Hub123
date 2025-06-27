// Product slider functions
function slideLeft() {
    document.getElementById("productContainer").scrollLeft -= 300;
}

function slideRight() {
    document.getElementById("productContainer").scrollLeft += 300;
}

// Add to Cart
function addToCart(productId) {
    fetch(`/add-to-cart/${productId}/`, { method: "GET" })
        .then(response => response.json())
        .then(data => {
            document.getElementById("cart-count").innerText = data.cart_count;
            alert("Added to Cart!");
        })
        .catch(error => console.error("Error:", error));
}

// Add to Wishlist
function addToWishlist(productId) {
    fetch(`/add-to-wishlist/${productId}/`, { method: "GET" })
        .then(response => response.json())
        .then(data => {
            document.getElementById("wishlist-count").innerText = data.wishlist_count;
            alert("Added to Wishlist!");
        })
        .catch(error => console.error("Error:", error));
}

// Category Filter
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.category-btn').forEach(button => {
        button.addEventListener('click', function () {
            let category = this.getAttribute('data-category');

            fetch(`/category-products/?category=${encodeURIComponent(category)}`)
                .then(response => response.text())
                .then(html => {
                    document.getElementById('product-list').innerHTML = html;
                })
                .catch(error => {
                    console.error("Error:", error);
                });
        });
    });
});
