# 语音识别和基于百度unit的语义识别 #
该部分代码分为两部分：语音识别部分和语义识别部分（都写在了asrunit.py中）

# 1.语音识别部分 #
通过调用百度语音识别API（极速版）实现了语音识别

## 百度语音识别API（极速版）简介 ##

将60秒以内的完整音频文件识别为文字，适用于近场短语音交互，如手机语音搜索、聊天输入等场景。输入完整音频文件，输出识别结果文字。

采用流式多级截断注意力模型SMLTA，专有GPU服务集群，识别响应速度及识别准确率极大提升。按调用量计费，免费赠送5万次调用。

该系统目前只支持中文普通话和英文。语音格式只支持：pcm（不压缩）、wav（不压缩，pcm编码）、amr（压缩格式）。推荐pcm 采样率 ：16000 固定值。编码：16bit位深的单声道。但是任意操作系统，任意编程语言，只要可以对百度语音服务器发起http请求的，均可以使用本接口。

关于语音识别极速版API的更多信息，可以查看百度的官方文档[http://ai.baidu.com/docs#/ASR-API-PRO/top](http://ai.baidu.com/docs#/ASR-API-PRO/top "语音识别极速版API")。

## 你可能需要修改的部分： ##
### 根据文档填写PID，选择语言及识别模型 ###
    `DEV_PID = 1537; #  1537 表示识别普通话，使用输入法模型。1536表示识别普通话，使用搜索模型`
测试英语 修改为:
    `DEV_PID = 1737;`
```
#需要识别的文件
AUDIO_FILE = "./16k.pcm";
#文件格式
FORMAT = "pcm"; # 文件后缀 pcm/wav/amr
```
测试收费极速版：
打开下面的注释
```
#收费极速版 DEVPID = 80001 ASRURL = 'https://vop.baidu.com/pro_api' SCOPE = 'brainenhancedasr' # 有此scope表示有收费极速版能力，没有请在网页里开通极速版
```

# 基于unit的语义识别部分 #
## 训练一个unit技能 ##
详细见官方教程unit2.0[https://ai.baidu.com/docs#/UNIT-v2-guide/top](https://ai.baidu.com/docs#/UNIT-v2-guide/top "unit2.0")
## 获取API Key和Secret Key ##
在unit技能训练界面，点击发布到沙盒生产环境，找到获取API Key/Secret Key 的按钮，即可查看。代码里面已经自动生成access_token了，不需要额外获取。将代码中的API Key和Secret Key 改为自己训练好的技能即可调用技能。
## 返回的参数 ##
返回的参数是json格式，具体每一项的含义参考代码内容。我们需要用到的一般是unit解析出来的意图和词槽（代码已将其打印出来）。

*更多关于unit的使用信息可以参考官方文档和demo部分的程序。*
