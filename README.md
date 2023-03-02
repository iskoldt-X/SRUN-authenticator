# 深澜认证Python 脚本

[![GitHub Stars](https://img.shields.io/github/stars/iskoldt-X/SRUN-authenticator.svg?style=flat-square&label=Stars&logo=github)](https://github.com/iskoldt-X/SRUN-authenticator/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/iskoldt-X/SRUN-authenticator.svg?style=flat-square&label=Forks&logo=github)](https://github.com/iskoldt-X/SRUN-authenticator/fork)
[![Docker Stars](https://img.shields.io/docker/stars/iskoldt/srunauthenticator.svg?style=flat-square&label=Stars&logo=docker)](https://hub.docker.com/r/iskoldt/srunauthenticator)
[![Docker Pulls](https://img.shields.io/docker/pulls/iskoldt/srunauthenticator.svg?style=flat-square&label=Pulls&logo=docker&color=orange)](https://hub.docker.com/r/iskoldt/srunauthenticator)



校园网深澜认证Python 脚本，旨在方便同学们的日常使用。默认国科大，其他学校也可以使用。

本脚本已经支持通过Docker 运行!

## 国科大同学用Docker 运行校园网深澜认证Python 脚本

```
docker run -d \
    --name authenticator \
    --restart unless-stopped \
    --log-opt max-size=1m \
    --network host \
    -e TZ="Asia/Shanghai" \
    -e USERNAME=yourusernamehere \
    -e PASSWORD=yourpasswordhere \
    -e INTERFACES=eth0 \
    iskoldt/srunauthenticator:latest
```


## 国科大同学使用软路由“多拨”校园网可以多插线

使用`23.02.24`版本

```
docker run -d \
    --name authenticator \
    --restart unless-stopped \
    --log-opt max-size=1m \
    --network host \
    -e TZ="Asia/Shanghai" \
    -e USERNAME=yourusernamehere \
    -e PASSWORD=yourpasswordhere \
    -e INTERFACES=eth0.eth1(the interface you plugged in, separate them with a period "." if you have more than one) \
    iskoldt/srunauthenticator:23.02.24
```

[iskoldt/srunauthenticator](https://hub.docker.com/r/iskoldt/srunauthenticator)

## 其他学校的朋友用Docker 运行校园网深澜认证Python 脚本

注意更改这三行：

```
    -e init_url="yours" \
    -e get_challenge_api="yours" \
    -e srun_portal_api="yours" \
```

```
docker run -d \
    --name authenticator \
    --restart unless-stopped \
    --log-opt max-size=1m \
    --network host \
    -e TZ="Asia/Shanghai" \
    -e USERNAME=yourusernamehere \
    -e PASSWORD=yourpasswordhere \
    -e INTERFACES=eth0(the interface you plugged in, separate them with a period "." if you have more than one) \
    -e init_url="yours" \
    -e get_challenge_api="yours" \
    -e srun_portal_api="yours" \
    iskoldt/srunauthenticator:latest
```

[iskoldt/srunauthenticator](https://hub.docker.com/r/iskoldt/srunauthenticator)

## 非Docker 运行校园网深澜认证Python 脚本

编辑如下三个变量，分别是接入校园网的网口名字，用户名和密码。

```
interfacelist = ['']
username=''
password=''
```

用户还要更改：

```
init_url="https://portal.ucas.ac.cn"
get_challenge_api="https://portal.ucas.ac.cn/cgi-bin/get_challenge"
srun_portal_api="https://portal.ucas.ac.cn/cgi-bin/srun_portal"
```

保存后运行：

```
python3 srun_login.py
```

如果依赖不全，可以根据报错安装缺失的库，如运行：
```
pip install netifaces
```

## 声明

SRUN-authenticator 只是一个用于方便同学们上网的工具，请确保您遵守有关隐私和数据保护的法律和法规。


## 来源
本项目只是借鉴网络上各位高手代码的缝合怪，各路英雄豪杰：

[huxiaofan1223/jxnu_srun](https://github.com/huxiaofan1223/jxnu_srun)

[DingGuodong/LinuxBashShellScriptForOps](https://github.com/DingGuodong/LinuxBashShellScriptForOps/blob/master/projects/WindowsSystemOps/Network/getNetworkStatus.py)

[Send http request through specific network interface](https://stackoverflow.com/questions/48996494/send-http-request-through-specific-network-interface)

## Starchart


[![Star History Chart](https://api.star-history.com/svg?repos=iskoldt-X/SRUN-authenticator&type=Date)](https://star-history.com/#iskoldt-X/SRUN-authenticator&Date)
