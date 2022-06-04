# 深澜认证Python 脚本
国科大校园网深澜认证Python 脚本

旨在方便同学们的日常使用。

## 使用方法
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

保存后润行：

```
python3 srun_login.py
```

如果依赖不全，可以根据报错安装缺失的库，如润行：
```
pip install netifaces
```


## 来源
本项目只是借鉴网络上各位高手代码的缝合怪，各路英雄豪杰：

[huxiaofan1223/jxnu_srun](https://github.com/huxiaofan1223/jxnu_srun)

[DingGuodong/LinuxBashShellScriptForOps](https://github.com/DingGuodong/LinuxBashShellScriptForOps/blob/master/projects/WindowsSystemOps/Network/getNetworkStatus.py)

[Send http request through specific network interface](https://stackoverflow.com/questions/48996494/send-http-request-through-specific-network-interface)
