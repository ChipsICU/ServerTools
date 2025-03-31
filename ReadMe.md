# ServerTools
A toolkit for non-root users on restricted servers.

## v2ray
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

## cuda
Follow the steps([English](https://stackoverflow.com/questions/39379792/install-cuda-without-root)/[Chinese](https://zhuanlan.zhihu.com/p/198161777)) to install cuda without root.