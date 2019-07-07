# 本目录存放项目的代码：

voc_unit：voice and unit，存放语音唤醒、语音识别、语音合成、调用unit RESTful API的代码

control：存放控制部分代码

web_ui：存放webUI部分的代码

api_server: 集成所用 flask api的代码
# 使用方法
- 安装所需框架
```
sudo pip3 install django==2.0.7
sudo pip3 install flask==1.0.2
```
- 进入到src/目录下，运行如下命令配置所需环境
```
sh environment_config.sh
```
- 进入到voc_unit目录下，运行如下命令，即可开始喊语音命令：
```
python asrunit.py x.x.x.x
```
注意x.x.x.x为你的树莓派的ip地址
- 此时可以在同局域网下的浏览器访问：http://172.20.10.6:8088/myhome/index/，则可进入HPECL智能家居界面 
注意：其中"172.20.10.6"应为当前树莓派ip。如果树莓派ip有改变，输入网址ip也需要改变，同时替换Smarthome/settings.py文件中的第28行ALLOWED_HOST的ip。然后通过点击按钮控制外部设备。

