let allProducts = [];

// Load products on page start
async function init() {
  allProducts = await fetchProducts();
  renderProducts(allProducts);
}

init();


// Render function
function renderProducts(products) {
  const container = document.getElementById("productContainer");
  container.innerHTML = "";

  products.forEach(product => {
    const card = document.createElement("div");
    card.className = "card";

    card.innerHTML = `
      <img src="${product.thumbnail}" class="product-img"/>

      <div class="card-body">
        <h3 class="product-title">${product.title}</h3>
        <p class="product-category">${product.category}</p>

        <div class="price-rating">
          <span class="price">$${product.price}</span>
          <span class="rating">⭐ ${product.rating}</span>
        </div>

        <button class="add-btn">Add to Cart</button>
      </div>
    `;

    container.appendChild(card);
  });
}


// Search
document.getElementById("searchInput")
  .addEventListener("input", (e) => {

    const term = e.target.value.toLowerCase();

    const filtered = allProducts.filter(product =>
      product.title.toLowerCase().includes(term)
    );

    renderProducts(filtered);
});


// Sort
document.getElementById("sortPrice")
  .addEventListener("change", (e) => {

    if (e.target.value === "high") {
      const sorted = [...allProducts]
        .sort((a, b) => b.price - a.price);

      renderProducts(sorted);
    } else {
      renderProducts(allProducts);
    }
});
