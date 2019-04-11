# coding=utf-8

import sys
import json
import base64
import time
import urllib, urllib2
import sys


IS_PY3 = sys.version_info.major == 3

if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    timer = time.perf_counter
else:
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode
    if sys.platform == "win32":
        timer = time.clock
    else:
        # On most other platforms the best timer is time.time()
        timer = time.time

API_KEY = 'kVcnfD9iW2XVZSMaLMrtLYIz'
SECRET_KEY = 'O9o1O213UgG5LFn0bDGNtoRN3VWl2du6'

# 需要识别的文件
AUDIO_FILE = './pcm/turnon.wav'  # 只支持 pcm/wav/amr
# 文件格式
FORMAT = AUDIO_FILE[-3:]  # 文件后缀只支持 pcm/wav/amr

CUID = '123456PYTHON'
# 采样率
RATE = 16000  # 固定值

# 免费版

DEV_PID = 1536  # 1537 表示识别普通话，使用输入法模型。1536表示识别普通话，使用搜索模型。根据文档填写PID，选择语言及识别模型
ASR_URL = 'http://vop.baidu.com/server_api'
SCOPE = 'audio_voice_assistant_get'  # 有此scope表示有asr能力，没有请在网页里勾选，非常旧的应用可能没有

# 收费极速版 打开注释的话请填写自己申请的appkey appSecret ，并在网页中开通极速版

# DEV_PID = 80001
# ASR_URL = 'https://vop.baidu.com/pro_api'
# SCOPE = 'brain_enhanced_asr'  # 有此scope表示有收费极速版能力，没有请在网页里开通极速版

# 忽略scope检查，非常旧的应用可能没有
# SCOPE = False

class DemoError(Exception):
    pass


"""  TOKEN start """

TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'


def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode( 'utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    if (IS_PY3):
        result_str =  result_str.decode()

    print(result_str)
    result = json.loads(result_str)
    print(result)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        print(SCOPE)
        if SCOPE and (not SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
            raise DemoError('scope is not correct')
        print('SUCCESS WITH TOKEN: %s  EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')

"""  TOKEN end """

if __name__ == '__main__':
    token = fetch_token()

    speech_data = []
    with open(AUDIO_FILE, 'rb') as speech_file:
        speech_data = speech_file.read()

    length = len(speech_data)
    if length == 0:
        raise DemoError('file %s length read 0 bytes' % AUDIO_FILE)
    speech = base64.b64encode(speech_data)
    if (IS_PY3):
        speech = str(speech, 'utf-8')
    params = {'dev_pid': DEV_PID,
              'format': FORMAT,
              'rate': RATE,
              'token': token,
              'cuid': CUID,
              'channel': 1,
              'speech': speech,
              'len': length
              }
    post_data = json.dumps(params, sort_keys=False)
    # print post_data
    req = Request(ASR_URL, post_data.encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    try:
        begin = timer()
        f = urlopen(req)
        result_str = f.read()
        print ("Request time cost %f" % (timer() - begin))
    except URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()

    if (IS_PY3):
        result_str = str(result_str, 'utf-8')
    print(result_str)
    print(json.loads(result_str)['result'][0])
    with open("result.txt","w") as of:
        of.write(result_str)


    #####################################
    #下面的部分为unit语义识别部分
    # encoding:utf-8


    # print sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding('utf-8')
    # print sys.getdefaultencoding()
    # client_id 为从UNIT的【发布上线】模块进入百度云创建应用后获取的API Key
    client_id='Th4Dsp55EWkU7DZSXqGKtDwZ'
    # client_secret 为从UNIT的【发布上线】模块进入百度云创建应用后获取的Secret Key
    client_secret='p6WNSlxCkTpVt465hoeSlH8ek5TPDoWp'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+client_id+'&client_secret='+client_secret
    # 上面的XXXXXXX 要替换成自己的API Key，YYYYYY要换成自己的Secret Key
    request = urllib2.Request(host)
    request.add_header('Content-Type', 'application/Json_test; charset=UTF-8')
    response = urllib2.urlopen(request)
    access_token = json.load(response)["access_token"]
    # 真实业务中要把access_token 存到redis里，不能频繁的创建access_token（频繁创建会影响性能，导致一些对话失败），access_token默认有效期为30天，要自己写定时任务在30天到期前自动更新
    # print access_token

    url = 'https://aip.baidubce.com/rpc/2.0/unit/bot/chat?access_token=' + access_token
    query1 = str(json.loads(result_str)['result'][0])
    query = query1
    # print('***', str(query1), '\n', query)
    # print(type(query1),type(query))
    # 下面的log_id在真实应用中要自己生成，可是递增的数字
    log_id ='7758521'
    # 下面的user_id在真实应用中要是自己业务中的真实用户id、设备号、ip地址等，方便在日志分析中分析定位问题
    user_id='222333'
    # 下面要替换成自己的bot_id
    bot_id='40296'
    post_data = '{\"bot_session\":\"\",\"log_id\":\"'+log_id+'\",\"request\":{\"bernard_level\":1,\"client_session\":\"{\\\"client_results\\\":\\\"\\\", \\\"candidate_options\\\":[]}\",\"query\":\"' + query + '\",\"query_info\":{\"asr_candidates\":[],\"source\":\"KEYBOARD\",\"type\":\"TEXT\"},\"updates\":\"\",\"user_id\":\"'+user_id+'\"},\"bot_id\":'+bot_id+',\"version\":\"2.0\"}'
    request = urllib2.Request(url, post_data)

    request.add_header('Content-Type', 'application/Json_test;charset=UTF-8')
    response = urllib2.urlopen(request)
    content = response.read()
    # if content:
    #    print content
    data = json.loads(content)
    print '用户问: '+ query
    print 'BOT答复: ' + data['result']['response']['action_list'][0]['say']
    print '意图: ' + data['result']['response']['schema']['intent']
    slots = data['result']['response']['schema']['slots']
    # print '词槽: ' + slot[0]['name'] + " = " +slot[0]['original_word']
    for slot in slots:
        print '词槽: ' + slot['name'] + " = " +slot['original_word']
















