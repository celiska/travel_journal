// List to hold added hashtags
let hashtags = [];

// Function to add a hashtag
document.getElementById('add-hashtag-btn').addEventListener('click', function() {
    const hashtagInput = document.getElementById('hashtag-input');
    const hashtagValue = hashtagInput.value.trim();

    // Check if the hashtag is not empty and not a duplicate
    if (hashtagValue && !hashtags.includes(hashtagValue)) {
        hashtags.push(hashtagValue); // Add hashtag to the list

        // Update the hidden field for the POST request
        document.getElementById('hashtags-hidden').value = hashtags.join(',');

        // Visually add the hashtag
        const hashtagList = document.getElementById('hashtag-list');
        const hashtagItem = document.createElement('span');
        hashtagItem.classList.add('badge', 'bg-secondary', 'mr-2', 'mb-2');
        hashtagItem.textContent = '#' + hashtagValue;
        hashtagList.appendChild(hashtagItem);

        // Clear the input field
        hashtagInput.value = '';
    }
});
