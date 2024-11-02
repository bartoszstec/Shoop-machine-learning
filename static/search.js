document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');

    searchInput.addEventListener('input', function() {
        const query = searchInput.value;

        if (query.length === 0) {
            // Wyczyść wyniki wyszukiwania, jeśli nie ma zapytania
            searchResults.innerHTML = '';
            return;
        }

        // Wyślij żądanie AJAX do serwera
        fetch(`/search_products?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(products => {
                // Wyczyść poprzednie wyniki
                searchResults.innerHTML = '';

                // Wyświetl nowe wyniki
                products.forEach(product => {
                    const productDiv = document.createElement('div');
                    productDiv.innerHTML = `
                        <h3>${product.name}</h3>
                        <img src="${product.image_url}" alt="${product.name}" class="product-image">
                        <p>Cena: ${product.price}</p>
                    `;
                    searchResults.appendChild(productDiv);
                });
            })
            .catch(error => console.error('Błąd:', error));
    });

    // Zablokuj domyślne zachowanie formularza (odświeżanie strony)
    document.getElementById('search-form').addEventListener('submit', function(event) {
        event.preventDefault();
    });
});