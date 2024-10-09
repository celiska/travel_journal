document.getElementById('add-place-btn').addEventListener('click', function() {
    var place = document.getElementById('place-input').value;
    var countrySelect = document.getElementById('country-select');
    var country = countrySelect.options[countrySelect.selectedIndex].text;
    var countryId = countrySelect.value;

    if (place && countryId) {
        var badgeContainer = document.createElement('span');
        badgeContainer.classList.add('custom-badge');

        badgeContainer.textContent = place + ' (' + country + ')';

        document.getElementById('place-list').appendChild(badgeContainer);

        var hiddenInput = document.getElementById('places-countries-hidden');
        hiddenInput.value += place + ':' + countryId + ';';

        document.getElementById('place-input').value = '';
    } else {
        alert("Please enter both place and country");
    }
});
