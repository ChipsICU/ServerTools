import base64
import json
import re
import subprocess
import yaml
import os
import shutil

def decode_ss_uri(uri):
    match = re.match(r'ss://([a-zA-Z0-9+/=]+)@([^:]+):(\d+)#(.+)', uri)
    if match:
        method_password = base64.urlsafe_b64decode(match.group(1)).decode('utf-8')
        method, password = method_password.split(':', 1)
        address = match.group(2)
        port = int(match.group(3))
        remarks = match.group(4)
        return {
            'address': address,
            'port': port,
            'method': method,
            'password': password,
            'remarks': remarks
        }
    return None

def fetch_and_decode_subscription(url):
    try:
        result = subprocess.run(["wget", "-qO-", url], capture_output=True, text=True, check=True)
        content = result.stdout.strip()
        
        decoded = base64.b64decode(content).decode('utf-8')
        return decoded.strip().splitlines()
    except Exception as e:
        print(f"Error when download subscription: {e}")
        return []

def generate_v2ray_config(servers, use_dns):
    config = {
        "inbounds": [
            {
                "port": 1080,
                "listen": "127.0.0.1",
                "protocol": "socks",
                "settings": {
                    "auth": "noauth",
                    "udp": True
                }
            },
            {
                "port": 8888,
                "listen": "127.0.0.1",
                "protocol": "http",
                "settings": {
                    "timeout": 0
                }
            }
        ],
        "outbounds": [],
        "routing": {
            "rules": [
                {
                    "type": "field",
                    "outboundTag": "server2",
                    "domain": ["geosite:geolocation-!cn"]
                }
            ]
        }
    }

    if use_dns:
        config["routing"]["domainStrategy"] = "UseIP"
        config["dns"] = {
            "servers": ["8.8.8.8", "1.1.1.1"]
        }
    for i, server in enumerate(servers):
        outbound = {
            "protocol": "shadowsocks",
            "settings": {
                "servers": [
                    {
                        "address": server['address'],
                        "port": server['port'],
                        "method": server['method'],
                        "password": server['password']
                    }
                ]
            },
            "tag": f"server{i+1}"
        }
        
        config["outbounds"].append(outbound)

    return config

def main():
    v2ray_url = "https://github.com/v2fly/v2ray-core/releases/download/v5.29.3/v2ray-linux-64.zip"
    zip_name = "v2ray-linux-64.zip"
    v2ray_dir = os.path.expanduser("~/v2ray")

    try:
        print("Downloading V2Ray...")
        subprocess.run(["wget", v2ray_url], check=True)

        print("Unzipping V2Ray to ~/v2ray ...")
        os.makedirs(v2ray_dir, exist_ok=True)
        subprocess.run(["unzip", "-o", "-d", v2ray_dir, zip_name], check=True)

        print("Cleaning up downloaded zip...")
        os.remove(zip_name)
    except subprocess.CalledProcessError as e:
        print(f"Failed to setup V2Ray: {e}")
        return

    with open('config.yaml', 'r') as f:
        yaml_data = yaml.safe_load(f)
        subscription_url = yaml_data.get('url')
        use_dns = yaml_data.get('dns', False)

    servers = []
    ss_lines = fetch_and_decode_subscription(subscription_url)
    for line in ss_lines:
        line = line.strip()
        if line:
            server = decode_ss_uri(line)
            if server:
                servers.append(server)

    v2ray_config = generate_v2ray_config(servers, use_dns)

    config_path = os.path.join(v2ray_dir, 'config.json')
    backup_path = config_path + '.bak'
    if os.path.exists(config_path):
        shutil.copy2(config_path, backup_path)
    with open(config_path, 'w') as file:
        json.dump(v2ray_config, file, indent=4)

    print("V2Ray configuration successfully written.")

if __name__ == '__main__':
    main()
