import os
import subprocess

def ssh_config_harden(port, username):
    def backup_ssh_config():
        backup_path = '/etc/ssh/sshd_config.backup'
        subprocess.run(['sudo', 'cp', '/etc/ssh/sshd_config', backup_path], check=True)
        print(f"Backup of the configuration file is saved as {backup_path}")

    def update_ssh_config(port):
        with open('/etc/ssh/sshd_config', 'r') as file:
            config_lines = file.readlines()
        
        updated_lines = []
        directives = {
            'Port': port,
            'PermitEmptyPasswords': 'no',
            'PermitRootLogin': 'no',
            'Protocol': '2',
            'ClientAliveInterval': '300',
            'ClientAliveCountMax': '0',
            'AllowUsers': username,
            'X11Forwarding': 'no',
            'MaxAuthTries': '3'
        }

        for line in config_lines:
            directive, *rest = line.strip().split(' ', 1)
            if directive in directives:
                updated_lines.append(f"{directive} {directives[directive]}\n")
                del directives[directive]
            else:
                updated_lines.append(line)

        # Add any remaining directives not found in the original file
        for directive, value in directives.items():
            updated_lines.append(f"{directive} {value}\n")

        with open('/etc/ssh/sshd_config', 'w') as file:
            file.writelines(updated_lines)
        
        print("SSH configuration has been updated.")

    def restart_ssh_service():
        subprocess.run(['sudo', 'systemctl', 'restart', 'ssh'], check=True)
        print("SSH service restarted.")

    def allow_new_ssh_port(port):
        subprocess.run(['sudo', 'ufw', 'allow', f'{port}/tcp'], check=True)
        subprocess.run(['sudo', 'ufw', 'reload'], check=True)
        print(f"Firewall updated to allow traffic on port {port}.")

    backup_ssh_config()
    update_ssh_config(port)
    #allow_new_ssh_port(port)
    restart_ssh_service()
