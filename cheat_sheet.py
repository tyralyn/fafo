# collections (comprenehsions, zip, filter, map, reduce)

def collections():
	l = [1,2,3,4,5,6,7]
	l_strings = ['one', 'two', 'three', 'four', 'five', 'six', 'seven']

	# list comprehensions
	l_doubled = [item * 2 for item in l]
	l_even = [item for item in l if item % 2 == 0]

	# list-of-tuple comprehension from list
	l_tuple_quadruple = [(x, 4*x) for x in l]

	# dict comprehension from list
	d_doubled = {item: 2*item for item in l}

	# dict comprehension from dict
	d_strings = dict(zip(l, l_strings))
	d_strings_odd = { k:v for k,v in d_strings.items() if k%2 ==1}
	d_strings_short = { k:v for k,v in d_strings.items() if len(v) < 4}

	# set comprehension
	s = set(l + [3, 3])

	# combining two dictionaries
	d1 = ...
	d2 = ...
	d = {**d1, **d2}
	d |= d2
	d = dict(d1, **d2) # only if keys of d2 are strings for some reason

	# zipping -- returns zip object
	d_strings = dict(zip(l, l_strings))
	t_strings = list(zip(l, l_strings))

	# converting dict into list of tuples
	l_tuples = [item for item in d_strings.items()]
	l_tuples = list(d_strings.items())

	# unzipping
	k, v = zip(*list(t_strings))

	# map -- returns map object
	# map(fun, iter), and fun does something with each item
	l_tripled = list(map(lambda x: x*3, l))

	# filter
	# filter(fun, iter), and fun is a true/false function
	l_gt_4 = list(filter(lambda x: x > 4, l))

	#from functools import reduce
	sum_l = reduce(lambda a,b:a+b,l)

	# get max dict element
	max(d, key=d.get) #aka max(d, key=lambda k: d.get(k))
	max(d.items(), key=lambda k: k[1])

# named tuple syntax

# file IO
def file_IO():

	# list directory contents (around this file)
	# import os
	root_filepath = "/"
	sample_filename = "/Users/tyralyn/yen/fafo/fafo/README.txt"
	os.listdir()
	os.listdir(root_filepath)
	# alternatively, os.scandir does the same but returns an iterator

	# opening a file
	# file object = open(file_name [, access_mode][, buffering])
	# access modes (read, write, append)
	f = open(sample_filename, 'r')

	# reading the whole file
	f_contents_whole = f.read()

	# go back to the beginning of the file
	# fileObject.seek(offset[, whence])
	f.seek(0)

	# read a single character
	f.seek(0)
	f.read(1)

	# read line by line
	# instead of f.read, use f.readlines()
	f.seek(0)
    lines = f.readlines()
   # for line in lines(): ...

   f.close()

 # enumeration
 def enumeration():
 	for i, el in enumerate('helloo'):
  		print(f'{i}, {el}')

 # any / all
 def any_all():
 	# True if at least one item in collection is truthy, False if empty.
 	any([False, True, False])
 	# True if all items in collection are true
 	all([True,1,3,True])   

# generators
def generators():
	def count(start, step):
    	while True:
        	yield start
        	start += step
    # >>> counter = count(10, 2)
	# >>> next(counter), next(counter), next(counter)
	# results in (10, 12, 14)

# command line args
def command_line_args():
	# import sys
	list_args = sys.argv

# python fstrings
def f_strings():
	name = 'tyralyn'
	company = 'unemployed :('
	n = 11

	# sticking in variables
	print(f"{name} is an {type_of_company} company.")

	# printing numebrs
	print(f"{5 * 5}")

	# printing functon calls
	print(f'My name is {name.upper()}.')

	# escaping quotes
	print(f'Text in {"double-quotes"}.')
	# escaping brackets
	f'{{"Single Braces"}}'

	# formatting datetime
	# import datetime
	date = datetime.date(1991, 10, 12)
	print(f'{date} was on a {date:%A}')
	# '1991-10-12 was on a Saturday'
	print(f'The date is {date:%A, %B %d, %Y}.')
	# 'The date is Saturday, October 12, 1991.'

	# adding space padding
	# 0 Padding -- {variable:0N}
	# Decimal Places -- {variable:.Nf}
	# Date Formatting -- {date : Directive}
	# Space Padding -- {variable:N}
	# Justified string	{variable:>N}
	print(f'The number is {n:4}')

	# hexadecimal
	print(f'{number:x}')
	# octal
	print(f'{number:o}')
	# scientific
	print(f'{number:e}')

# string stuff w/ regex
def string_regex():
	# import re
	log_line="1.2.44.51 \"GET www.url.of.some.kind.com/login=true\" 200 88888 \"contents of the request being some kida shit idk\""
	regex="[0-9]+(.[0-9]+){3} [\"][A-Z]+ [^\"\s]+[\"] [0-9]+ [0-9]+ [\"].+[\"]$"

	p = re.compile(regex)

	# find exact match
	print(re.match(p, log_line).group())

	# search for match
	print(re.search(p, log_line).group())

	# find all matches, return as list of matches
    print(re.findall(re.compile("[a-z]{3,5}"), log_line))
 	# find all matches, return as iterator through match objs
    print(re.finditer(re.compile("[a-z]{3,5}"), log_line))


def bytes():
	firstname='green bay'
	lastname='P@ck3r5'

	# turn a string into bytes
	firstname.encode()

# simple string stuff
def string_utilities():
	firstname='green bay'
	lastname='P@ck3r5'

	# case
	firstname.capitalize()
	firstname.casefold()
	firstname.lower()
	firstname.upper()
	firstname.title()

	# contents?
	firstname.count()
	firstname.find()
	firstname.rfind() # find the last
	firstname.index() # same as find but with error
	firstname.rindex()
	re.findall("y", firstname)
	firstname.startswith("gr")
	firstname.endswith("bay")

	# boolean checks types of characters
	lastname.isalpha()
	lastname.isascii()
	lastname.isdigit()
	lastname.isnumeric()
	lastname.isidentifier()
	lastname.iskeyword()
	lastname.islower()
	lastname.isprintable()
	lastname.isspace()
	lastname.istitle()
	lastname.isupper()

	# splits / removal
	firstname.lstrip("erg")        #'n Bay'
	firstname.rstrip("aByY")       #'green '
	firstname.removeprefix("gre")  #'en Bay'
	firstname.removesuffix("ay")
	firstname.partition("n")       # ('gree', 'n', ' Bay')

	firstname.splitlines()

	firstname.replace("e", "E")    #'grEEn Bay'

	# alphabetizing
	sorted(firstname)
	max(firstname)
	min(firstname)

def string_constants():
	string.ascii_letters
	string.ascii_lowercase
	string.ascii_uppercase
	string.digits
	string.hexdigits
	string.octdigits
	string.punctuation
	string.isprintable
	string.whitespace

def integer_utilities():
	# convert to binary
	bin(5)

	# convert to hex
	hex(22)

	# convert to decimal
	int("0xff", 16)
	int("0b10101", 2)

def random():
	# import random
	l = [1,2,3,4,5,6,7]

	# get a random number in specified range
	random.random(0,100)

	# get a random item(s) from asequence
	random.choice(l)
	random.choices(l, 22)

	# pick multiple random items from a list without repitition or dupes
	random.sample(l, 12)
	random.sample(range(99), 4)
	random.sample(d1.items(), 2)





