const lyricsInput = document.getElementById('lyrics-input');
const lyricsOutput = document.getElementById('lyrics-output');
const pasteButton = document.getElementById('paste-button');
const copyButton = document.getElementById('copy-button');
const messageBox = document.getElementById('message-box');
const messageText = document.getElementById('message-text');

// Function to show a message box
function showMessage(text, duration = 3000) {
    messageText.textContent = text;
    messageBox.classList.remove('scale-0', 'opacity-0');
    messageBox.classList.add('scale-100', 'opacity-100');

    setTimeout(() => {
        messageBox.classList.remove('scale-100', 'opacity-100');
        messageBox.classList.add('scale-0', 'opacity-0');
    }, duration);
}

// Live update the output as the user types
lyricsInput.addEventListener('input', () => {
    const text = lyricsInput.value.trim();
    if (text) {
        lyricsOutput.innerHTML = `<pre class="font-sans font-bold text-2xl sm:text-3xl">${text}</pre>`;
    } else {
        lyricsOutput.innerHTML = '<p class="text-center text-gray-500 text-base">Your beautiful lyrics will be displayed here.</p>';
    }
});

// Handle the paste button click
pasteButton.addEventListener('click', async () => {
    try {
        const text = await navigator.clipboard.readText();
        lyricsInput.value = text;
        lyricsInput.dispatchEvent(new Event('input')); // Trigger the input event to update the output
        showMessage('Lyrics pasted successfully!');
    } catch (err) {
        console.error('Failed to read from clipboard:', err);
        showMessage('Could not paste lyrics. Please click on the text area and press Ctrl+V or Cmd+V.', 5000);
    }
});

// Handle the copy button click
copyButton.addEventListener('click', async () => {
    const textToCopy = lyricsOutput.innerText;
    if (textToCopy && textToCopy !== 'Your beautiful lyrics will be displayed here.') {
        try {
            await navigator.clipboard.writeText(textToCopy);
            showMessage('Lyrics copied to clipboard!');
        } catch (err) {
            console.error('Failed to copy text: ', err);
            showMessage('Could not copy lyrics. Please select the text and press Ctrl+C or Cmd+C.', 5000);
        }
    } else {
        showMessage('There are no lyrics to copy.', 3000);
    }
});