import re
import sys
from constants import *
from helpers import *

# Check command line arguments
if len(sys.argv) != 2:
	print "Usage: process filename"
	sys.exit()
try:
	f = open(sys.argv[1], 'r')
except IOError:
	print "Invalid filename"
	sys.exit()

text = f.read()

print "Code\tLine #\tHouse\tRoom\tContainer\tObject\tQuantity\tValue\tSubstrate\tTrim or Accouterments\tContents\tSize and Shape\tColor\tCondition\tFunction\tStyle\tGender\tOwner\tOther words\tNumOther"

code_iter = re.finditer('Code:\s*(.*?)\n', text)
iter = re.finditer("Inventory begins(.*?)Inventory ends", text, re.DOTALL)

while True:
	try: 
		m = iter.next()
		c = code_iter.next()
	except StopIteration:
		break

	# should error check group count?
	code = c.group(1)
	inventory = m.group(1)

	lines = inventory.splitlines()

	line_num = 0

	for line in lines:
		line_num = line_num + 1
		substrates = []
		colors = []
		accessories = []
		contents = []
		styles = []
		numbers = []
		functions = []
		others = []
		object = ""
		phrase = ""


		m = re.search('\tIt[eu]m(.*)', line)
		if not m is None:
			item = m.group(1);
			words = item.split();
			for idx, word in enumerate(words):
				
				# if current word is 'cum', the rest of the line is a phrase
				if word == "cum":
					attachment = " ".join(words[idx:])

					# remove /fol from end of attachment
					pos = attachment.find('/')
					if pos != -1:
						attachment = attachment[:pos-1]
					accessories.append(attachment)
					break

				# if the current word is de or ad or pro, tack it onto the current phrase
				if word == "de" or word == "ad" or word == "pro":
					phrase = phrase + word
					continue

				# check to see if the word is in one of our lists. I am in the process of making a helper function in helpers.py
				if word in SUBSTRATE_STEMS or word[:-1] in SUBSTRATE_STEMS or word[:-2] in SUBSTRATE_STEMS or word[:-3] in SUBSTRATE_STEMS or word[:-4] in SUBSTRATE_STEMS:
					if phrase != "":
						substrates.append(phrase + " " + word)
						phrase = ""
					else:	
						substrates.append(word)			
				elif word in COLOR_STEMS or word[:-1] in COLOR_STEMS or word[:-2] in COLOR_STEMS or word[:-3] in COLOR_STEMS or word[:-4] in COLOR_STEMS:
					if phrase != "":
						colors.append(phrase + " " + word)
						phrase = ""
					else:	
						colors.append(word)			
				elif word in ACCESSORY_STEMS or word[:-1] in ACCESSORY_STEMS or word[:-2] in ACCESSORY_STEMS or word[:-3] in ACCESSORY_STEMS or word[:-4] in ACCESSORY_STEMS:
					if phrase != "":
						accessories.append(phrase + " " + word)
						phrase = ""
					else:	
						accessories.append(word)			
				elif word in CONTENTS or word in CONTENTS_STEMS or word[:-1] in CONTENTS_STEMS or word[:-2] in CONTENTS_STEMS or word[:-3] in CONTENTS_STEMS or word[:-4] in CONTENTS_STEMS:
					if phrase != "":
						contents.append(phrase + " " + word)
						phrase = ""
					else:	
						contents.append(word)			
				elif word in STYLES or word in STYLE_STEMS or word[:-1] in STYLE_STEMS or word[:-2] in STYLE_STEMS or word[:-3] in STYLE_STEMS or word[:-4] in STYLE_STEMS:
					if phrase != "":
						styles.append(phrase + " " + word)
						phrase = ""
					else:	
						styles.append(word)			
				elif  word in NUMBER_STEMS or word[:-1] in NUMBER_STEMS or word[:-2] in NUMBER_STEMS or word[:-3] in NUMBER_STEMS or word[:-4] in NUMBER_STEMS:
					if phrase != "":
						numbers.append(phrase + " " + word)
						phrase = ""
					else:	
						numbers.append(word)			
				elif  word in FUNCTION_STEMS or word[:-1] in FUNCTION_STEMS or word[:-2] in FUNCTION_STEMS or word[:-3] in FUNCTION_STEMS or word[:-4] in FUNCTION_STEMS:
					if phrase != "":
						functions.append(phrase + " " + word)
						phrase = ""
					else:	
						numbers.append(word)

				# if the word has a slash in it, it is extraneous		
				elif word.find('/') != -1:
					continue

				# if none of the above apply, the word is an "Other" word
				else:
					if phrase != "":
						others.append(phrase + " " + word)
						phrase = ""
					else:	
						others.append(word)

			# if, after processing all the words, there is one left over, call it the object
			if len(others) == 1:
				object = others[0]
				others[0] = ""
			
			# Output the results
			print code,                                       # Code
			print "\t" + str(line_num),                       # Line 
			print "\t",                                       # House
			print "\t",                                       # Room
			print "\t",                                       # Container
			print "\t" + object,                              # Object
			print "\t" + str(", ".join(sorted(numbers))),     # Quantity
			print "\t",                                       # Value
			print "\t" + str(", ".join(sorted(substrates))),  # Substrate
			print "\t" + str(", ".join(sorted(accessories))), # Trim or Accouterments
			print "\t" + str(", ".join(sorted(contents))),    # Contents
			print "\t",                                       # Size
			print "\t" + str(", ".join(sorted(colors))),      # Color
			print "\t",                                       # Condition
			print "\t" + str(", ".join(sorted(functions))),   # Function
			print "\t" + str(", ".join(sorted(styles))),      # Style
			print "\t",                                       # Gender
			print "\t",                                       # Owner
			print "\t" + str(", ".join(sorted(others))),      # Other words
			print "\t" + str(len(others))                     # Number of Other words