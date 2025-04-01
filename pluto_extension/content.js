// content.js

const username = document.querySelector('input[autocomplete*="username"]');
const password = document.querySelector('input[autocomplete*="current-password"]');

if (username && password) {
    const ws = new WebSocket('ws://localhost:8765');

    ws.addEventListener('open', () => {
        const message = {
            type: "login_form_detected",
            domain: window.location.hostname
        };
        ws.send(JSON.stringify(message));
        ws.close();
    });

    ws.addEventListener('error', () => {
        console.warn("SecureKeyVault WebSocket not available. Is the Python app running?");
    });
}