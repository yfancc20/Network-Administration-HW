# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from lxml import html
import ssl, urllib3
import tesserocr
from PIL import Image, ImageEnhance
import tesserocr, pytesseract


# class CourseCrawler:

# 	def __init__(self, )

""" Basic info """
# some urls
url = 'https://course.nctu.edu.tw'
url_pic = 'https://course.nctu.edu.tw/getSafeCode.asp'
url_pic2 = 'https://course.nctu.edu.tw/function/Safecode.asp'
url_login = 'https://course.nctu.edu.tw/inCheck.asp'
url_table = 'https://course.nctu.edu.tw/adSchedule.asp'

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
	'Content-Type': 'application/x-www-form-urlencoded',
	'Cookie': '',
	'Host': 'course.nctu.edu.tw',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': user_agent,
}

# post data for login
post_data = {
	'ID': '0312236',
	'passwd': 'P6z3L60B',
	'qCode': '',
	'Action': '登入',
}

""" Functions
"""
""" get the captcha and download it """
def getCaptcha(headers):
	print(headers)
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


def send(key, val):
	cookies = dict(key=val)

	# login requests
	result = requests.post(url_login, data=post_data, headers=headers, verify=False)

	# schedule requests
	r = requests.get(url_table, headers=headers, verify=False)
	r.encoding = 'big5'

	soup = BeautifulSoup(r.text, 'lxml')

	# write result to a file
	writeFile('result.html', r.content)


def removeSault(img):
    pixel = img.load()
    w, h = img.size

    dirx = [0, 1, 1, 1, 0, -1, -1, -1]
    diry = [-1, -1, 0, 1, 1, 1, 0, -1]

    for y in range(1, h - 2):
        string = ''
        for x in range(1, w - 2):
            count = 0
            for i in range(0, 8):
                if pixel[x + dirx[i], y + diry[i]] > 254:
                    count += 1

            if count >= 7:
                pixel[x, y] = 255

            if pixel[x, y] > 130:
                pixel[x, y] = 255;
                string += '0'
            else:
                pixel[x, y] = 0;
                string += '1'

    for y in range(1, h - 2):
        string = ''
        for x in range(1, w - 2):
            count = 0
            for i in range(0, 8):
                if pixel[x + dirx[i], y + diry[i]] == 0:
                    count += 1

            if count >= 5:
                pixel[x, y] = 0

    for x in range(0, w):
        pixel[x, 0] = 255
        pixel[x, h - 1] = 255
    for y in range(0, h):
        pixel[0, y] = 255
        pixel[w - 1, y] = 255

    return img


def move(img):
    w, h = img.size
    pixel = img.load()

    for i in range(0, 5):
        offsetx = (i + 1) * 20
        max = 0
        for x in range(offsetx - 20, offsetx - 14 - 1):
            for y in range(0, 50 - 14 - 1):
                count = 0
                for m in range(0, 14):
                    for n in range(0, 14):
                        if  pixel[m + x, n + y] == 0:
                            count += 1

                if count > max:
                     max = count
                     posx, posy = x, y

        # print(posx, posy)

        # offset = posy - 0
        # for x in range(posx, posx + 20):
        #     for y in range(posy, posy + 14):
        #         pixel[x, y - offset] = pixel[x, y]
        #         pixel[x, y] = 255

        if posy + 7 <= 25:
            offset = 25 - (posy + 7)

            if offset > 5:
                for x in range(posx, posx + 14):
                    for y in range(posy + 14 - 1, posy - 1, -1):
                        pixel[x, y + offset] = pixel[x, y]
                        pixel[x, y] = 255

        else:
            offset = (posy + 7) - 25
            if offset > 5:
                for x in range(posx, posx + 14):
                    for y in range(posy, posy + 14):
                        pixel[x, y - offset] = pixel[x, y]
                        pixel[x, y] = 255

    return img

def decode(img):
    replace_char = {
        '\n': '',
        '.': '',
        ' ': '4',
        '(': '6',
        '%': '8',
        '1': '7',
        '$': '9',
        'b': '6',
    }
    code = tesserocr.image_to_text(img)
    for (key, val) in replace_char.items():
        code = code.replace(key, val)

    return code


def decodeCaptcha():
	img = Image.open('captcha.png')
	img = img.convert('L')
	img = removeSault(img)
	img = move(img)
	code = decode(img)

	return code




""" ignore ssl error and warning """
# rewrite ss.match_hostname
ssl.match_hostname = lambda cert, hostname: True
urllib3.disable_warnings()


# set the cookies
result = requests.get(url, verify=False)
for (key, val) in result.cookies.items():
	print(key, val)
	headers['Cookie'] = key + '=' + val

getCaptcha(headers)

code = decodeCaptcha()
post_data['qCode'] = code

send(key, val)

print(code)


