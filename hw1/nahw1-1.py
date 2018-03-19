# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from lxml import html
import ssl, urllib3
import pytesseract
import tesserocr
from PIL import Image, ImageEnhance


""" Basic info """
# some urls
url = 'https://cos.adm.nctu.edu.tw/index.asp'
url_pic = 'https://cos.adm.nctu.edu.tw/getSafeCode.asp'
url_pic2 = 'https://cos.adm.nctu.edu.tw/function/Safecode.asp'
url_login = 'https://cos.adm.nctu.edu.tw/inCheck.asp'
url_table = 'https://cos.adm.nctu.edu.tw/adSchedule.asp'

# user agent for headers
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) ' + \
			'AppleWebKit/537.36 (KHTML, like Gecko) ' + \
			'Chrome/65.0.3325.162 Safari/537.36'

# headers
headers = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-CN;q=0.5',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	# 'Content-Length': '',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Cookie': 'UserID=0312236; ASPSESSIONIDCQADRRRD=DKNEPMADGMKAJEOIKDFAJMFM',
	'Host': 'cos.adm.nctu.edu.tw',
	# 'Origin': 'https://cos.adm.nctu.edu.tw',
	# 'Referer': 'https://cos.adm.nctu.edu.tw/',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': user_agent,
}

# post data for login
post_data = {
	'ID': '0312236',
	'passwd': 'P6z3L60B',
	'qCode': '46373',
	'Action': '登入',
}

""" Functions
"""
""" get the captcha and download it """
def getCaptcha(headers):
	with open('captcha.png', 'wb') as file:
	    # get request
	    # cookie = dict(ASPSESSIONIDCQADRRRD='DKNEPMADGMKAJEOIKDFAJMFM')

	    result = requests.get(url_pic, headers=headers, verify=False)

	    result2 = requests.get(url_pic2, headers=headers, verify=False)

	    file.write(result2.content)

# write to file
def writeFile(filename, content):
	with open(filename, 'wb') as file:
	    file.write(content)


def send():
	# set the cookies
	cookies = dict(ASPSESSIONIDCQADRRRD='DKNEPMADGMKAJEOIKDFAJMFM')

	# login requests
	result = requests.post(url_login, data=post_data, headers=headers, verify=False)

	# schedule requests
	r = requests.get(url_table, cookies=cookies, verify=False)
	r.encoding = 'big5'

	soup = BeautifulSoup(r.text, 'lxml')

	# write result to a file
	writeFile('result.html', r.content)


""" ignore ssl error and warning """
# rewrite ss.match_hostname
ssl.match_hostname = lambda cert, hostname: True
urllib3.disable_warnings()



getCaptcha(headers);
send();