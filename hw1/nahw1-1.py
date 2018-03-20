# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from lxml import html
import ssl, urllib3, urllib, re, math
import tesserocr
from PIL import Image, ImageEnhance
import tesserocr, pytesseract


class CourseCrawler:

	""" Constructor """
	def __init__(self, s_id, password):
		""" Basic info """
		# some urls
		self.url = 'https://course.nctu.edu.tw'
		self.url_pic = 'https://course.nctu.edu.tw/getSafeCode.asp'
		self.url_pic2 = 'https://course.nctu.edu.tw/function/Safecode.asp'
		self.url_login = 'https://course.nctu.edu.tw/inCheck.asp'
		self.url_table = 'https://course.nctu.edu.tw/adSchedule.asp'

		# headers
		self.headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-CN;q=0.5',
			'Cache-Control': 'max-age=0',
			'Connection': 'keep-alive',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Cookie': '',
			'Host': 'course.nctu.edu.tw',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) ' + \
						  'AppleWebKit/537.36 (KHTML, like Gecko) ' + \
						  'Chrome/65.0.3325.162 Safari/537.36',
		}

		# default post data for login
		self.post_data = {
			'ID': s_id,
			'passwd': password,
			'qCode': '',
			'Action': '登入',
		}

		# counting login
		self.login_count = 0

		""" ignore ssl error and warning """
		# rewrite ss.match_hostname
		ssl.match_hostname = lambda cert, hostname: True
		urllib3.disable_warnings()



	def getCookies(self):
		# set the cookies
		if self.headers['Cookie']  == '':
			result = requests.get(self.url, verify=False)
			self.headers['Cookie'] = ''
			for (key, val) in result.cookies.items():
				self.headers['Cookie'] += key + '=' + val + '; '

		return self.headers['Cookie']


	""" get the captcha and download it """
	def getCaptcha(self):
		with open('captcha.png', 'wb') as file:
		    # result = requests.get(self.url_pic, headers=self.headers, verify=False)
		    result2 = requests.get(self.url_pic2, headers=self.headers, verify=False)

		    file.write(result2.content)

		return self.decodeCaptcha()


	def loginSend(self):
		# login requests
		result = requests.post(self.url_login, data=self.post_data, headers=self.headers, verify=False)
		self.login_count += 1

		return result


	""" work for recognizing the captcha """
	def removeSault(self, img):
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


	""" work for recognizing the captcha """
	def move(self, img):
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


	def decode(self, img):
	    replace_char = {
	        '\n': '',
	        '.': '',
	        ' ': '4',
	        '(': '6',
	        '%': '8',
	        '1': '7',
	        '$': '9',
	        'b': '6',
	        'S': '5',
	    }
	    code = tesserocr.image_to_text(img)
	    for (key, val) in replace_char.items():
	        code = code.replace(key, val)

	    return code


	def decodeCaptcha(self):
		img = Image.open('captcha.png')
		img = img.convert('L')
		img = self.removeSault(img)
		img = self.move(img)
		# img.show()
		code = self.decode(img)
		self.post_data['qCode'] = code

		return code


	def getSchedule(self):
		""" schedule requests """
		r = requests.get(self.url_table, headers=self.headers, verify=False)
		r.encoding = 'big5'
		soup = BeautifulSoup(r.text, 'html.parser')
		with open('result.html', 'wb') as file:
			file.write(r.content)

		big_title = soup.find_all('td', class_='headtitle')
		big_title = str(big_title)[:100]


		if big_title.find('0312236') != -1:
			print('Login Sucessfully!')
			print('Try: ' + str(self.login_count) + ' times')
			self.parseSchedule()
		elif big_title.find('Limit') != -1:
			print('Login Limits')
		else:
			self.retry()


	def retry(self):
		self.getCaptcha()
		self.loginSend()
		self.getSchedule()


	def parseSchedule(self):
		""" for local debug """
		local_url = '/Users/yfancc20/School/大四/NA/HW/hw1/result.html'
		file = open(local_url, encoding='big5')
		soup = BeautifulSoup(file, 'html.parser')

		cells_num = 9
		cells_size = []
		cells_content = []
		for i in range(0, cells_num):
			cells_size.append(0)


		table = soup.find('table', {'colspan': '5'})
		i = 0
		for row in table.find_all('tr'):
			# ignore first row
			if i == 0:
				i += 1
				continue

			cells = row.find_all('td')
			string = ''
			content = []
			j = 0
			for cell in cells:
				font = cell.find('font')
				tmp_string = ''
				if font.string == None:
					tmp_string = str(font.text)
					tmp_string = tmp_string.strip(' \t\n\r')
					tmp_string = tmp_string.replace('\n', ' ')
					tmp_string = tmp_string.replace('\t', ' ')
					tmp_string = re.sub(' +', ' ', tmp_string)
				else:
					tmp_string = font.string.strip(' \t\n\r')

				tmp_string = tmp_string.replace('（', '(')
				tmp_string = tmp_string.replace('）', ')')

				length = len(tmp_string)
				for word in tmp_string:
					trans = ord(word)
					if trans > 126:
			   			length += 1

				if length > cells_size[j]:
					cells_size[j] = length

				content.append(tmp_string)
				string += '{:<3}'.format(str(len(tmp_string)))
				j += 1

			cells_content.append(content)


		seperate = '+'
		for x in range(0, len(cells_size)):
			dash_length = cells_size[x] + 2
			for y in range(0, dash_length):
				seperate += '-'

			seperate += '+'



		j = 0
		for row in cells_content:
			string = ''
			if j <= 1:
				print(seperate)
			for i in range(0, cells_num):
				if i == 0:
					string += '|'

					if j == 0:
						string += ' ' + row[i] + ' ' + '|'
					else:
						string += '  ' + row[i] + '   ' + '|'

				elif i == 1:
					if j == 0:
						string += '   ' + row[i] + '  ' + '|'
					else:
						string += ' ' + row[i] + ' ' + '|'

				else:
					if j == 0:
						space_length = cells_size[i] + 1
						space = '{:^' + str(space_length) + '}'
						string += space.format(row[i])

					else:
						length = len(row[i])
						for word in row[i]:
							trans = ord(word)
							if trans > 126:
					   			length += 1

						if length == cells_size[i]:
							string += ' ' + row[i] + ' '

						elif len(row[i]) < 3:
							space_length = cells_size[i] + 2
							space = '{:^' + str(space_length) + '}'
							string += space.format(row[i])
						else:
							space_length = math.floor((cells_size[i] + 2) / 2)
							space = '{:\u3000^' + str(space_length) + '}'
							string += space.format(row[i])

					string += '|'


			j += 1

			print(string)
			if j == 0:
				print(seperate)
		print(seperate)



def main():
	student_id = '0312236'
	password = 'P6z3L60B'

	crawler = CourseCrawler(student_id, password)
	cookies = crawler.getCookies()
	print('Cookies: ' + str(cookies))

	crawler.getCaptcha()
	crawler.loginSend()
	print('Login...')
	crawler.getSchedule()




main()




