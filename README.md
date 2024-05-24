# Dropbox Auto SSH Hardener and Ngrok Tunnel

This tool automates the process of changing the SSH connection settings, hardening them, and creating an Ngrok tunnel. The login information is then sent to a specified Telegram group. The tool continuously checks for an internet connection every 10 seconds. Once a connection is established, it performs the necessary actions.

## Features

- Waits for an internet connection (checks every 10 seconds)
- Changes and hardens the SSH connection
- Creates an Ngrok tunnel
- Sends login information to a Telegram group
- Configurable via `.env` file

## Installation

git clone https://github.com/sxyrxyy/Raspberry-pie_ngrok_tunnel_dropbox.git
cd Raspberry-pie_ngrok_tunnel_dropbox
pip install -r requirements.txt

### Setting Up a Cron Job
sudo crontab -e
@reboot sudo python /path/to/your/Raspberry-pie_ngrok_tunnel_dropbox/ngrok.py
