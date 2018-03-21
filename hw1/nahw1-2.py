import argparse, re
import sys, time
from collections import OrderedDict

def argumentSet():
	parser = argparse.ArgumentParser(description='Auth log parser')
	parser.add_argument('filename', help='Log file path')
	parser.add_argument('-u', help='Summary failed login log and sort log by user', \
							action='store_true')
	parser.add_argument('-after', help='Filter log after date. format YYYY-MM-DD-HH:MM:SS')
	parser.add_argument('-before', help='Filter log before date. format YYYY-MM-DD-HH:MM:SS')
	parser.add_argument('-n', type=int, help='Show only the user of most N-th times')
	parser.add_argument('-t', type=int, help='Show only the user of attacking equal or more than T times')
	parser.add_argument('-r', help='Sort in reverse order', action='store_true')

	return parser.parse_args()



def validateDatetime(date_string):
	if re.search('....-..-..-..:..:..', date_string) is not None:
		date = date_string[:10]
		times = date_string[-8:]
		try:
			valid_date = time.strptime(date, '%Y-%m-%d')
			valid_times = time.strptime(times, '%H:%M:%S')
		except ValueError:
			print('Invalid date format!')
			sys.exit(1)

		return date_string


def convert(counts):
	tmp_list = []
	for key, val in counts.items():
		tmp_list.append([key, val])

	return tmp_list



def increase(username, counts, max_count):
	# first create the key mapping
	if username not in counts:
		counts[username] = 0

	if max_count == -1:
		counts[username] += 1
	elif max_count >= 0 and counts[username] < max_count:
		counts[username] += 1


def main():

	args = argumentSet()

	dict_month = {
		'Jan': '01', 'Feb': '02', 'Mar': '03',
		'Apr': '04', 'May': '05', 'Jun': '06',
		'Jul': '07', 'Aug': '08', 'Sep': '09',
		'Oct': '10', 'Nov': '11', 'Dec': '12'
	}


	if args.after:
		after_date = validateDatetime(args.after)

	if args.before:
		before_date = validateDatetime(args.after)

	if args.after and args.before and (args.after > args.before):
		print('The date duration is wrong!')
		sys.exit(1)

	if args.n:
		if args.n < 0:
			print('[-n] value, value must > 0')
			sys.exit(1)
		else:
			max_count = args.n
	else:
		max_count = -1


	if args.t:
		if args.t < 0:
			print('[-t] value, value must > 0')
			sys.exit(1)
		else:
			max_retry = args.t
	else:
		max_retry = -1


	counts = {}

	filename = args.filename
	with open(filename, 'r') as f:
		content = f.readlines()

	for line in content:
		words = line.split()
		result = re.search('Invalid user(.*)from', line)

		if result is not None:
			username = result.group(1)
			username = username.strip(' ')

			result = re.search('sshd\[(.*)\]', line)
			if result is not None:
				sshd_num = result.group(1)

			log_date = '2018-' + dict_month[words[0]] + '-' + \
					   '{:02d}'.format(int(words[1])) + '-' + words[2]


			if args.before and log_date > args.before:
				continue
			elif args.after and log_date < args.after:
				continue

			increase(username, counts, max_count)

	# convert the dict to list
	counts = convert(counts)

	# no options
	counts = sorted(counts, key = lambda x : x[1], reverse=True)

	# option -u
	if args.u:
		counts = sorted(counts, key = lambda x : x[0])

	if args.r:
		counts = sorted(counts, key = lambda x : x[1], reverse=False)


	# calculate the length and prepare to print
	max_name_len = 0
	max_cnt_len = 0
	for name, cnt in counts:
		if len(str(name)) > max_name_len:
			max_name_len = len(str(name))

		if len(str(cnt)) > max_cnt_len:
			max_cnt_len = len(str(cnt))

	if len('count') > max_cnt_len:
		max_cnt_len = len('count')


	seperate = '+'
	for x in range(0, max_name_len + 2):
		seperate += '-'
	seperate += '+'
	for x in range(0, max_cnt_len + 2):
		seperate += '-'
	seperate += '+'


	# print title of the table
	print(seperate)
	string = ''
	string += '|' + ('{:^' + str(max_name_len + 2) + '}').format('user') + \
			  '+' + \
			  ('{:^' + str(max_cnt_len + 2) + '}').format('count') + \
			  '+'
	print(string)
	print(seperate)

	# print contents of the table
	for name, cnt in counts:
		string = '|' + ('{:^' + str(max_name_len + 2) + '}').format(name) + \
			  	 '|' + \
			  	 ('{:^' + str(max_cnt_len + 2) + '}').format(cnt) + \
			 	 '|'
		print(string)

	print(seperate)

argumentSet()
main()