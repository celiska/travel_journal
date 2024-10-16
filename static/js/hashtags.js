document.addEventListener('DOMContentLoaded', function() {
    let hashtags = [];

    document.getElementById('add-hashtag-btn').addEventListener('click', function() {
        const hashtagInput = document.getElementById('hashtag-input');
        const hashtagValue = hashtagInput.value.trim();

        if (hashtagValue && !hashtags.includes(hashtagValue)) {
            hashtags.push(hashtagValue);

            document.getElementById('hashtags-hidden').value = hashtags.join(',');

            const hashtagList = document.getElementById('hashtag-list');
            const hashtagItem = document.createElement('span');
            hashtagItem.classList.add('badge', 'bg-warning', 'mr-2', 'mb-2');
            hashtagItem.textContent = '#' + hashtagValue;
            hashtagList.appendChild(hashtagItem);

            hashtagInput.value = '';
        }
    });
});
