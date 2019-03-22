#encoding:utf-8
import urllib2
import json

access_token = '*****'
url = 'https://aip.baidubce.com/rpc/2.0/unit/bot/chat?access_token=' + access_token
post_data = "{\"bot_session\":\"\",\"log_id\":\"7758521\",\"request\":{\"bernard_level\":1,\"client_session\":\"{\\\"client_results\\\":\\\"\\\", \\\"candidate_options\\\":[]}\",\"query\":\"开灯\",\"query_info\":{\"asr_candidates\":[],\"source\":\"KEYBOARD\",\"type\":\"TEXT\"},\"updates\":\"\",\"user_id\":\"88888\"},\"bot_id\":\"41402\",\"version\":\"2.0\"}"
request = urllib2.Request(url, post_data)
request.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(request)
content = response.read()
# content = content.decode('unicode-escape').encode('utf-8')
if content:
    s = json.loads(content)
    print s['result']['response']['schema']


