# encoding:utf-8
from flask import Flask,request
import json
import time
import sys
import sqlite3
import os

app=Flask(__name__) # 创建Flask类的实例
####回复文本格式##########
re={}
result={}
result["type"]="text"
result["content"]=""
re["error_code"]=0
re["error_msg"]=""
re["result"]=result
dic={'温度':'temperature','湿度':'humidity','光照':'light','二氧化碳':'co2_simulation','声音':'noise'}
##########意图对应的语音回复文本字典############
response={'AC1_OC_OPEN':'请稍等，正在为您打开空调，接下来您可以选择调节温度、风速，改变空调模式等选项，如果我没理解您的命令，\
您可以通过“怎样调节”加目标项来获得标准控制命令',
'AC1_OC_CLOSE':'请稍等，正在为您关闭空调',
'AC1_TEMP_UP':'正在帮您升高空调温度，请稍等',
'AC1_TEMP_DOWN':'正在帮您降低空调温度，请稍等',
'AC1_WSPEED_UP':'正在帮您提高空调风速，请稍等',
'AC1_WSPEED_DOWN':'正在帮您降低空调风速，请稍等',
'AC1_SLEEP_OPEN':'好的，正在为您打开睡眠模式，请稍等',
'AC1_SLEEP_CLOSE':'好的，正在为您关闭睡眠模式，请稍等',
'AC1_TIMER_CLOSE':'好的，正在为您取消空调定时，请稍等'}
##############词槽标准化字典#############
normal={'高':'0','中':'1','低':'2','制冷':'0','制热':'1','送风':'2','自动':'3','除湿':'4','关':'close','开':'open','平衡':'0','环保':'1','极致':'2',
'16度':'16','17度':'17','18度':'18','19度':'19','20度':'20','21度':'21','22度':'22','23度':'23','24度':'24','25度':'25',
'26度':'26','27度':'27','28度':'28','29度':'29','30度':'30','降低':'lower','热':'lower','升高':'higher','冷':'higher',
'半小时':'0.5','一小时':'1.0','一个半小时':'1.5','两小时':'2.0','两个半小时':'2.5','三小时':'3.0','温度':'0','湿度':'1','声音':'2','光照':'3','二氧化碳':'4'}
class Response:
	def __init__(self,intent,nom_word):
		self.re=re
		self.intent=intent
		self.nom_word=nom_word
	def json_resp(self,intent,nom_word):
		if intent in response.keys():
			re["result"]["content"]=response[intent]
		elif intent=="AC1_TEMP_TO":
			re["result"]["content"]="好的，正在为您将空调设置为"+nom_word+"，请稍等"
		elif intent=="AC1_WSPEED_TO":
			re["result"]["content"]="好的，正在为您调节风速为"+nom_word+"，请稍等"
		elif intent=="AC1_TIMER_SET":
			re["result"]["content"]="好的，正在为您设置空调定时"+nom_word
		elif intent=="AC1_COMMOD_SELECT"or intent=="AC1_SMARTMOD_SELECT":
			re["result"]["content"]="好的，正在为您调节到"+nom_word+"模式，请稍等"
		elif intent=="ROOM1_ENV_INFO_QUERY":
			conn = sqlite3.connect("db.sqlite3")
			c = conn.cursor()
			############选择查询信息的最新值#########
			c.execute('SELECT '+dic[nom_word]+' FROM myhome_nodedata ORDER BY id desc')
			#########取出查询项对应字段对应数据######
			query_result=c.fetchone()[0]					
			re["result"]["content"]="您当前的室内"+nom_word+"为"+str(query_result)
		else:
			re["result"]["content"]="请求失败，请重试"
		return re

@app.route("/unit/callback",methods=['POST']) # 使用POST方法
def callback():
	########加载json数据并转换为字典形式###########
	#print(request.form)
	data = request.form
	# dic=json.loads(str(request.data,encoding='utf-8'))
	########获取字典中的意图和词槽即“intent”和“normallized_word”字段数据########
	intent = data["intent"]
	# print(intent)
	if intent == '':
	    intent = 'INTENT_ERROR'
	nom_word = data["slots"]
	print('intent: %s, slots: %s' % (intent, nom_word))
	# intent=dic["response"]["schema"]["intent"]
	# nom_word=dic["response"]["schema"]["slots"][0]["normalized_word"]
	######创建回复类对象#######
	# exp1=Response(intent,nom_word)
	########将表征请求中意图、词槽的数据更新存储控制命令的数据库表单（若不存在则先创建）############
	if os.path.exists("db.sqlite3"):
		conn = sqlite3.connect("db.sqlite3")
		c = conn.cursor()
	else:
		conn = sqlite3.connect("db.sqlite3")
		c = conn.cursor()		
		c.execute('''CREATE TABLE myhome_commands(ID integer NOT NULL PRIMARY KEY AUTOINCREMENT,INTENT
		text NOT NULL ,SLOTS text NOT NULL)''')
		c.execute('INSERT INTO myhome_commands VALUES(1,"0","0")')				#插入意图和归一化词槽
	# c.execute("UPDATE myhome_commands SET INTENT=?,SLOTS=? where ID=1",(intent,normal[nom_word]))
	c.execute("UPDATE myhome_commands SET INTENT=?,SLOTS=? where ID=1",(intent,nom_word))
	conn.commit()
	conn.close()
	#######获得答复数据并转换为json格式返回给请求方######
	# json_re=exp1.json_resp(intent,nom_word)
	# json_re=json.dumps(re)
	# return json_re
	return json.dumps({
		"status": "successful!",
		"intent": intent, 
		"slots": nom_word
	})
	
	
	
if __name__=='__main__':
	# app.run(host='172.20.10.12',port=9999,debug=True)
	app.run(host='0.0.0.0',
	 		port=5000,
			debug=True)
