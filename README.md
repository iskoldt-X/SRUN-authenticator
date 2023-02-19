# 深澜认证Python 脚本

<img src="https://img.shields.io/docker/pulls/iskoldt/srunauthenticator.svg"/>

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
    -e INTERFACES=eth0(the interface you plugged in, separate them with a period "." if you have more than one) \
    iskoldt/srunauthenticator:latest
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
