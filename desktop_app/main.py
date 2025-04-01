# WebSocket server replacing active_url logic

import asyncio
import websockets
import json
from desktop_app.serial_comms import send_command

seen = set()

async def handle_connection(websocket):
    async for message in websocket:
        try:
            data = json.loads(message)
            print(data)
            if data.get("type") == "login_form_detected":
                domain = data.get("domain")
                domain = domain.replace("www.", "")
                if domain and domain not in seen:
                    print(f"🌐 Login page detected: {domain}")
                    send_command(f"get {domain}")
                    #seen.add(domain)
        except Exception as e:
            print(f"⚠️ Error handling message: {e}")

async def main():
    print("🔐 SecureKeyVault Host WebSocket server running on ws://localhost:8765\n")
    send_command("auth ALOJHOMORE24")
    async with websockets.serve(handle_connection, "localhost", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Server stopped.")
