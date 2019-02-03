#!/usr/bin/env python
import os
import time
import smtplib
from email.mime.text import MIMEText

def emailLog(
	content,
	mailto_list=['**@**.com'], #receiver
	mail_host="smtp.**.com", #smtp ** server
	mail_user="**@**.com", #user name
	mail_pass="***", #security code
	mail_postfix="**.com" # ** postfix
):
	me="sleep program report "+"<"+mail_user+"@"+mail_postfix+">"
	msg = MIMEText(content,_subtype='plain')
	msg['Subject'] = 'server reconnection report'
	msg['From'] = me
	msg['To'] = ";".join(mailto_list) #use ';' to separate different eceivers
	try:
		server = smtplib.SMTP()
		server.connect(mail_host) # connect to server
		server.login(mail_user,mail_pass) # login procedure
		server.sendmail(me, mailto_list, msg.as_string())
		server.close()
		return True
	except(ConnectionRefusedError):
		print(str(e))
		return False

def isConnected():
	return not os.system('ping -c 3 baidu.com > /dev/null')

def reconnect():
	ac = '***' # pku account id
	sn = '***' # pku account security number
	fLog = 'keepconnect_log.txt'
	os.system('connect -u %s -p %s -g >> %s' % (ac, sn, fLog))
	return isConnected()

def printLog(fLog, msg):
	with open(fLog, 'a') as hLog:
		hLog.write(msg + '\n')

def keepconnect():
	fLog = 'keepconnect_log.txt'
	hLog = open(fLog, 'w')
	hLog.close()
	while(1):
		if not isConnected():
			tm = time.localtime()
			tm_s = time.strftime('%Y-%m-%d %H:%M:%S', tm)
			printLog(fLog, 'connection loss at ' + tm_s)
			retry_num = 1
			while(not reconnect()):
				if retry_num == 100:
					printLog(fLog, 'reconnection failed with %d times' % retry_num)
					return
				retry_num += 1
			confirm_msg = 'reconnection succeeded after %d trials.' % retry_num
			printLog(fLog, confirm_msg)
			emailLog(confirm_msg)
		else:
			print('connected.')
			time.sleep(60)

keepconnect()
