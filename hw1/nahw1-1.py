# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from lxml import html
import ssl, urllib3
import pytesseract
from PIL import Image

# rewrite ss.match_hostname
ssl.match_hostname = lambda cert, hostname: True
urllib3.disable_warnings()

""" Basic info """
url = 'https://cos.adm.nctu.edu.tw'
urlPic = 'https://cos.adm.nctu.edu.tw/function/Safecode.asp'
loginUrl = 'https://cos.adm.nctu.edu.tw/inCheck.asp'
username = '0312236'
password = 'P6z3L60B'
# sessionRequest = requests.session()

postData = {
	'ID': username,
	'passwd': password,
	'qcode': '45369',
}



result = requests.get(url, verify=False)
result.encoding = 'big5'
if result.status_code == 200:
	# result = requests.get(urlPic, verify=False)
	with open('captcha.png', 'wb') as file:
	    # get request
	    result = requests.get(urlPic, verify=False)
	    # write to file
	    file.write(result.content)

	img = Image.open('test.png')
	code = pytesseract.image_to_string(img)
	print(code)
	# soup = BeautifulSoup(result.text, 'lxml')
	# div = soup.find(id='img')
# print(div);

# print(soup)

# img = Image.open('https://cos.adm.nctu.edu.tw/images/new.gif')
# print(img)
# print(result.text)
# result = requests.post(loginUrl, params=postData, verify=False)
# print(result.text)
# soup = BeautifulSoup(result, 'lxml')

# result = sessionRequest.post(
# 	loginUrl,
# 	data = postData,
# 	headers = dict(referer=loginUrl)
# )

""" Crawing """
# result = urllib.request.urlopen(url)
# soup = BeautifulSoup(result, 'html.parser')

# with requests.session() as s:
#     s = s.post(loginUrl, params = postData, headers = header, timeout = 5)
#     # response = s.get($dataurl, timeout = 5, verfily=False)

# print(soup.title.encode('big5'))

# webPage = urllib.request.urlopen(url)
# data = webPage.read()
# data = data.decode('UTF-8')

# print(data)
# print(type(webPage))
# print(webPage.geturl())
# print(webPage.info())
# print(webPage.getcode())