import os
import sys
import time
import requests
from pyngrok import ngrok
from dotenv import load_dotenv
from ssh_config import ssh_config_harden

if os.geteuid() != 0:
    print("This script must be run as root. Please use 'sudo'.")
    sys.exit(1)


# Vars
load_dotenv()
bot_token = os.getenv('BOT_TOKEN')
ngrok_auth = os.getenv('NGROK_AUTH')
chat_id = os.getenv('CHAT_ID')
ssh_local_port = os.getenv('SSH_LOCAL_PORT')
missing_vars = []
if not bot_token:
    missing_vars.append('BOT_TOKEN')
if not ngrok_auth:
    missing_vars.append('NGROK_AUTH')
if not chat_id:
    missing_vars.append('CHAT_ID')
if not ssh_local_port:
    missing_vars.append('SSH_LOCAL_PORT')
if missing_vars:
    print(f"The following environment variables are missing in the .env file: {', '.join(missing_vars)}")
    sys.exit(1)

ngrok.set_auth_token(ngrok_auth)
current_username = os.getlogin()
print("Setting SSH")
ssh_config_harden(ssh_local_port, current_username)


def ngrok_tunnel():
    # Set Tunnel
    print("Getting ngrok tunnel")
    ssh_tunnel = ngrok.connect(ssh_local_port, "tcp")
    print(ssh_tunnel)
    ngrok_process = ngrok.get_ngrok_process()

    # Set telegram msg
    ssh_tunnel = str(ssh_tunnel).replace('"', '').split(' ')[1].removeprefix('tcp://').split(':')
    ssh_cmd = f'ssh {current_username}@{ssh_tunnel[0]} -p {ssh_tunnel[1]} -p {ssh_local_port}'
    payload = {"chat_id": chat_id, "text": f'Tunnel is up:\n\n{ssh_cmd}\n'}
    url = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/sendMessage"
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print('Telegram Message Sent.')
    else:
        print(f'Error sending message to telegram:\n{response.text}\n')
    try:
        ngrok_process.proc.wait()
    except KeyboardInterrupt:
        print(" Shutting down server.")
        ngrok.kill()


while True:
    url = "http://www.google.com"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
        print("Connected to the Internet")
        ngrok_tunnel()
    except (requests.ConnectionError, requests.Timeout) as exception:
        print(f"No internet connection.\nTrying Again in few seconds...\n\n")
    time.sleep(10)
