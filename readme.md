# 一键破解云注入python脚本

## 原理

云注入会替换原应用的application,今天我用算法助手看了一下云注入后的软件发现原application被des加密放在dex/com/cloudinject/feature/App里面了

如图

![1](img\1.png)

而且密钥是下面的APP_ID的前8位

加密配置是des的ECB模式加密，输出hex



众所周知破解云注入只需替换Application，然后就可以删除云注入的文件了

于是就有了这个一键破解脚本

`pip install -r requirements.txt`一键安装环境

本机在python310运行无误



**注意，需要自行配置java环境，遇到没有application的应用可能会报错**
