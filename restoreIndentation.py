import re
import sys
import string
from constants import *
from helpers import *

# STILL SEEMS TO FAIL WHEN THERE ARE PERIODS IN THE LINE, OTHER THAN THE LEADING NUMBER

class digit_string(object):
	def __init__(self):
		self.num = 1
	def __iter__(self):
		return self
	
	def next(self):
		cur, self.num = self.num, self.num+1
		return str(cur)

def letter_string():
	letters = string.lowercase
	for i in xrange(len(letters)):
		yield str(letters[i])

# http://code.activestate.com/recipes/81611-roman-numerals/
def int_to_roman(input):
   if type(input) != type(1):
      raise TypeError, "expected integer, got %s" % type(input)
   if not 0 < input < 4000:
      raise ValueError, "Argument must be between 1 and 3999"   
   ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
   nums = ('m',  'cm', 'd', 'cd','c', 'xc','l','xl','x','ix','v','iv','i')
   result = ""
   for i in range(len(ints)):
      count = int(input / ints[i])
      result += nums[i] * count
      input -= ints[i] * count
   return result


def roman_numeral_string():
	for i in xrange(3999):
		yield int_to_roman(i+1)


def restoreIndentation(inventory):

	lines = inventory.splitlines()


	result = ""

	# GOING TO ASSUME NUMBER, LETTER, ROMAN NUMERAL, NUMBER, and no more than that. There are situations where this breaks (e.g. when ds_next and ds2_next are the same)
	ds_iter = digit_string()
	ls_iter = letter_string()
	rs_iter = roman_numeral_string()
	ds2_iter = digit_string()

	ds_next = ds_iter.next()
	ls_next = ls_iter.next()
	rs_next = rs_iter.next()
	ds2_next = ds2_iter.next()
	count = 0
	for idx,line in enumerate(lines):
		# this RE may be too general, perhaps (.*)\.\t(.*) would be better
		line_match = re.search('(.*?)\.(.*)', line)
		
		# add code to check if this is valid
		if idx + 1 < len(lines):
			next_line_match = re.search('(.*?)\.(.*)', lines[idx+1])
		else:
			next_line_match = None
		
		if not next_line_match is None:
			next_indent_symbol = next_line_match.group(1)
		else:
			next_indent_symbol = ""

		if not line_match is None:

			indent_symbol = line_match.group(1)

			if len(indent_symbol) == 0:
				result = result + line + '\n'
			elif len(indent_symbol) > 10:
				result = result + line + '\n'
				if not(next_indent_symbol != '1' and next_indent_symbol in string.digits):
					ds_iter = digit_string()
					ds_next = ds_iter.next()
			# to handle the cases where the first line is not 1., but instead 2. or 15., etc
			elif (indent_symbol == ds_next and (indent_symbol != ds2_next or indent_symbol == '1')) or count == 0:
				result = result + line + '\n'
				ds_next = ds_iter.next()
				ls_iter = letter_string()
				ls_next = ls_iter.next()
				count = 1

			elif indent_symbol == ls_next and next_indent_symbol != "ii":
				result = result + '\t' + line + '\n'
				ls_next = ls_iter.next()
				rs_iter = roman_numeral_string()
				rs_next = rs_iter.next()

			elif indent_symbol == rs_next:
				result = result + '\t\t' + line + '\n'
				rs_next = rs_iter.next()
				ds2_iter = digit_string()
				ds2_next = ds2_iter.next()

			else:
				result = result + '\t\t\t' + line + '\n'
				ds2_next = ds2_iter.next()
		else:
			if next_indent_symbol == '1':
				ds_iter = digit_string()
				ds_next = ds_iter.next()
			result = result + line + '\n'
	return result


def indent_repl(matchobj):
	text_to_fix = matchobj.group(0)
	text_fixed = restoreIndentation(text_to_fix)
	return text_fixed
# ds_iter = digit_string()
# for i in range(5):
# 	print ds_iter.next()

# ls_iter = letter_string()
# for i in range(5):
# 	print ls_iter.next()

# rn_iter = roman_numeral_string()
# for i in range(5):
# 	print rn_iter.next()	

# Check command line arguments
if len(sys.argv) != 2:
	print "Usage: restoreIndentation filename"
	sys.exit()
try:
	f = open(sys.argv[1], 'r')
except IOError:
	print "Invalid filename"
	sys.exit()

text = f.read()
# iter = re.finditer("Inventory begins(.*?)Inventory ends", text, re.DOTALL)
# inventory_match = iter.next()
# inventory = inventory_match.group(1)

# print restoreIndentation(inventory
print re.sub("Inventory begins(.*?)Inventory ends", indent_repl, text, flags = re.DOTALL)