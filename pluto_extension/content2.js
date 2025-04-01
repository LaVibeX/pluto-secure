// content.js – Web Serial integration with Pluto configuration via extension icon click

let port = null;

async function sendCredentials(domain, isFirstTime) {
    const statusBanner = document.createElement("div");
    statusBanner.style.position = "fixed";
    statusBanner.style.bottom = "10px";
    statusBanner.style.right = "10px";
    statusBanner.style.padding = "10px 14px";
    statusBanner.style.backgroundColor = "#1a73e8";
    statusBanner.style.color = "white";
    statusBanner.style.borderRadius = "8px";
    statusBanner.style.fontFamily = "Arial, sans-serif";
    statusBanner.style.zIndex = 9999;
    statusBanner.style.boxShadow = "0 0 8px rgba(0,0,0,0.2)";
    statusBanner.innerText = "🔍 Sending to Pluto...";
    document.body.appendChild(statusBanner);

    try {
        if (!port) {
            statusBanner.innerText = "❌ Pluto not connected. Click the Pluto icon.";
            return;
        }

        if (!port.readable || !port.writable) {
            await port.open({ baudRate: 9600 });
        }

        const encoder = new TextEncoderStream();
        const writableStreamClosed = encoder.readable.pipeTo(port.writable);
        const writer = encoder.writable.getWriter();

        //await writer.write("hello\n");
        

        if (isFirstTime) {
            await writer.write("auth ALOJHOMORE24\n");
            statusBanner.innerText = "✅ Pluto authenticated";
            sessionStorage.setItem(`pluto-sent-${domain}`, "true");
        }
        statusBanner.innerText = `get ${domain}\n`;

        await writer.write(`get ${domain}\n`);
        writer.releaseLock();

        await writableStreamClosed;
        await port.close();
        port = null;

        statusBanner.innerText = `✅ Pluto sent credentials for ${domain}`;
        setTimeout(() => document.body.removeChild(statusBanner), 4000);

    } catch (err) {
        console.error("🔌 Failed to send to Pluto device:", err);
        statusBanner.innerText = "❌ Pluto error: " + err.message;
        setTimeout(() => document.body.removeChild(statusBanner), 5000);
    }
}

// When the page has username and password, and port is available, send command
(async () => {
    const username = document.querySelector('input[autocomplete*="username"]');
    const password = document.querySelector('input[autocomplete*="current-password"]');
    if (!(username && password)) return;

    const domain = window.location.hostname;
    const isFirstTime = !sessionStorage.getItem(`pluto-sent-${domain}`);

    chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
        if (msg.action === "connectPluto") {
            navigator.serial.requestPort().then(async (userPort) => {
                port = userPort;
                await port.open({ baudRate: 9600 });
                await port.close();
                port = userPort;
                alert("✅ Pluto USB connected!");

                // Now we can try sending credentials since we just connected
                sendCredentials(domain, true);
            }).catch((e) => {
                alert("❌ Could not connect to Pluto: " + e.message);
            });
        }
    });
})();
