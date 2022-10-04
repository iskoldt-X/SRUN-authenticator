# 深澜认证Python 脚本
国科大校园网深澜认证Python 脚本

旨在方便同学们的日常使用。

本脚本已经支持通过Docker 运行!
最新arm64 架构镜像已成功压缩至73.7MB！

## 用Docker 运行国科大校园网深澜认证Python 脚本

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

## 非Docker 运行国科大校园网深澜认证Python 脚本

编辑如下三个变量，分别是接入校园网的网口名字，用户名和密码。

```
interfacelist = ['']
username=''
password=''
```

非UCAS 用户还要更改：

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


## 来源
本项目只是借鉴网络上各位高手代码的缝合怪，各路英雄豪杰：

[huxiaofan1223/jxnu_srun](https://github.com/huxiaofan1223/jxnu_srun)

[DingGuodong/LinuxBashShellScriptForOps](https://github.com/DingGuodong/LinuxBashShellScriptForOps/blob/master/projects/WindowsSystemOps/Network/getNetworkStatus.py)

[Send http request through specific network interface](https://stackoverflow.com/questions/48996494/send-http-request-through-specific-network-interface)
