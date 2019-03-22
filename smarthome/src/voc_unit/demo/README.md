# Demo

本文档简要记录了一个调用定制技能的RESTful API的过程。

- 训练一个unit技能
- 获取access_token
- 调用定制的RESTful API

## 训练一个unit技能

训练unit技能比较简单，详细见[官方教程](https://ai.baidu.com/unit/)

## 获取access_token

获取sccess_token,官方有多种语言实现代码，这里给出bash版本,直接在命令行输入以下内容（AK和SK要换成自己的API Key、Secret Key）：

```bash
curl -i -k 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=【百度云应用的AK】&client_secret=【百度云应用的SK】'
```

## 调用定制的RESTful API

我这里调用了我训练的【开灯】的技能，仅仅作为一小的Demo,在命令行运行如下命令：

```
python call_unit.py
```

注意运行前需要先将call_unit.py的access_token和技能id更改为自己的。

返回结果如下：

```bash
{u'intent': u'TURN_ON_THE_LIGHT', u'slots': [], u'intent_confidence': 100, u'domain_confidence': 0}
```

其中，intent表示意图，slots表示词槽。