//testovací kód při zjištění funkčnosti napojení statických souborů
const hashtagInput = document.getElementById('hashtagInput');

hashtagInput.addEventListener('input', function (e) {
    console.log('Input event fired');

    setTimeout(() => {
        const words = hashtagInput.value.trim().split(' ');
        console.log('Words:', words);

        if (words[words.length - 1] && !words[words.length - 1].startsWith('#')) {
            words[words.length - 1] = '#' + words[words.length - 1];
            console.log('Updated words:', words);
        }

        hashtagInput.value = words.join(' ');
    }, 0);

    if (e.inputType === 'insertText' && e.data === ' ') {
        e.preventDefault();
        console.log('Space pressed');
    }
});
