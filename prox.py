import requests
import websocket
import json

# You need to install websockets module first, do pip3 install websockets

# Proxmox API endpoint and credentials
proxmox_url = "https://localhost:8006/api2/json"
username = "your-username"
password = "your-password"

# Authenticate and get the ticket
response = requests.post(f"{proxmox_url}/access/ticket", data={"username": username, "password": password})
if response.status_code == 200:
    ticket = response.json()["data"]["ticket"]
else:
    print("Authentication failed")
    exit(1)

# Get the CSRF token
response = requests.get(f"{proxmox_url}/access/token", headers={"Cookie": f"PVEAuthCookie={ticket}"})
if response.status_code == 200:
    csrf_token = response.json()["data"]["CSRFPreventionToken"]
else:
    print("Failed to get CSRF token")
    exit(1)

# Create a WebSocket connection to the Proxmox console
ws_url = f"wss://{proxmox_url.replace('https', 'wss')}/console"
headers = {"Cookie": f"PVEAuthCookie={ticket}", "CSRFPreventionToken": csrf_token}
ws = websocket.create_connection(ws_url, header=headers)

# Send a command to the console (e.g., list all VMs)
ws.send(json.dumps({"method": "get", "params": {"node": "your-node-name", "type": "vm"}}))

# Receive the response from the console
response = ws.recv()
print(response)

# Close the WebSocket connection
ws.close()
