#!/usr/bin/python3

import sys
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts

if not (sys.argv[1] or sys.argv[2] or sys.argv[3]):
	print("Uso: xmlrpc_py.py <IP-VICTIMA> <USER> <PASSWORD>")

url = "http://"+sys.argv[1]+"/xmlrpc.php"

client = Client(url, sys.argv[2], sys.argv[3])
post   = client.call(posts.GetPosts())
print(post[0].content)
