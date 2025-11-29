const spotSelect  = document.querySelector('select.search-select[name="spot"]');
const genreSelect = document.querySelector('select.search-select[name="genre"]');
const nameInput   = document.querySelector('input.search-input[name="restaurant_name"]');

const selects = document.querySelectorAll('select.search-select');
const resultsList = document.querySelector('.results-list');

let searchTimer = null;

const runSearch = () => {
  const params = new URLSearchParams();

  if (spotSelect.value) {
    params.append('spot', spotSelect.value);
  }
  if (genreSelect.value) {
    params.append('genre', genreSelect.value);
  }
  if (nameInput.value.trim()) {
    params.append('restaurant_name', nameInput.value.trim());
  }

  const url = '/api/restaurants/?' + params.toString();

  fetch(url)
    .then(response => response.json())
    .then(data => {
      resultsList.innerHTML = renderRestaurtans(data.results);
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });
};

selects.forEach(select => {
  select.addEventListener('change', runSearch);
});

nameInput.addEventListener('input', () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(runSearch, 400);
});

const renderRestaurtans = (results) => {
    return results.map(restaurant => renderCard(restaurant)).join('');
};

const renderCard = (restaurant) => {
    return `
    <li class="restaurant-card">
        <a href="/restaurants/${restaurant.id}/">        
           <img src="${restaurant.image_url}" alt="${restaurant.name}">
            <div class="restaurant-info">
                <h3>${restaurant.name}</h3>
                <p>${restaurant.sub_area.name}</p>
            </div>
        </a>
    </li>
    `;
};
