# ServerTools
A toolkit for non-root users on restricted servers.

## proxy

### use v2ray on server

1. Ready your config.yaml
```
url: xxx # put your vpn address here
dns: yes # if you wanna to bypass system's dns
```
2. Run ss2v2ray.py
```
python v2ray/ss2v2ray.py
```
3. Startup v2ray
```
~/v2ray/v2ray run -config ~/v2ray/config.json
```
4. Check if v2ray is running
```
curl -x socks5h://127.0.0.1:10808 -I http://www.google.com
```
5. Use [this website](https://ip.chinaz.com/) to find your url's real ip(sometimes they will change IP for security)

### docker proxy

1. 在 systemd 为 docker 创建 drop-in 目录并新建配置文件
```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo vim /etc/systemd/system/docker.service.d/http-proxy.conf
```

2. 
```yaml
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:8889/"
Environment="HTTPS_PROXY=http://127.0.0.1:8889/"
Environment="NO_PROXY=localhost,127.0.0.1,*.docker.io,*.docker.com,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"
```

3. 重新加载 systemd 配置并重启 docker，使代理配置生效
```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
sudo systemctl show --property=Environment docker # check if set proxy successfully!
```

### use local proxy as transfer

For example, if you use clash on your local device, follow this step by step.

1. Reverse map the remote server's port 7897 to your local port 7897, 7897 is ***your local proxy port***.
```bash
ssh -R 7897:127.0.0.1:7897 username@servername
```
2. Set environment variables on server, make sure port is correct!
```bash
export https_proxy="http://127.0.0.1:7897"
export http_proxy="http://127.0.0.1:7897"
export all_proxy="http://127.0.0.1:7897"
```
3. Check if v2ray is running
```bash
curl -x http://127.0.0.1:7897 -I http://www.google.com

```
## cuda
Follow the steps([English](https://stackoverflow.com/questions/39379792/install-cuda-without-root)/[Chinese](https://zhuanlan.zhihu.com/p/198161777)) to install cuda without root.

## Install  
aria2c can be installed in conda, **Conda** you're so niubility!
```bash
conda install -c bioconda aria2
```