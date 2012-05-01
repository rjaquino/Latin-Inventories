# a tab got in somehow, see latest output
import re
import sys
import string
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


all_others = dict()
all_other_phrases = dict()
distances = dict()
i = 0
while True:
	try: 
		m = iter.next()
		c = code_iter.next()
		i = i + 1
	except StopIteration:
		# print i
		break

	# should error check group count?
	code = c.group(1)
	inventory = m.group(1)

	lines = inventory.splitlines()

	line_num = 0
	
	house = ""
	room = ""

	for line in lines:
		line_num = line_num + 1
		substrates = []
		colors = []
		accessories = []
		contents = []
		styles = []
		sizes = []
		numbers = []
		functions = []
		conditions = []
		others = []
		object = ""
		phrase = ""
		values = []
		glossary = []
		cur_other = ""

		house_match = re.search('(^[^\t]*?)\.\t(.*)', line)
		if not house_match is None:
			if len(house_match.group(1)) < 10:
				house = house_match.group(2)
		room_match = re.search('^\t([^\t]*?)\.\t(.*)', line)
		if not room_match is None:
			room = room_match.group(2)

		item_match = re.search('^\t\t([^\t]*?)\.\t(.*)', line)
		if not item_match is None:
			item = item_match.group(2);
			for regex in VALUE_REGEXES:
				regex_match = re.search(regex, line)
				if not regex_match is None:
					values.append(regex_match.group(1));
					item = string.replace(item, regex_match.group(1), "")

			words = item.split();
			for idx, word in enumerate(words):
				
				found = False
				# strip out punctuation, from http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
				word  = word.translate(string.maketrans("",""), string.punctuation)
				if word == "Item":
					continue
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
					found = True
					if phrase != "":
						substrates.append(phrase + " " + word)
						phrase = ""
					else:	
						substrates.append(word)			
				elif word in COLOR_STEMS or word[:-1] in COLOR_STEMS or word[:-2] in COLOR_STEMS or word[:-3] in COLOR_STEMS or word[:-4] in COLOR_STEMS:
					found = True
					if phrase != "":
						colors.append(phrase + " " + word)
						phrase = ""
					else:	
						colors.append(word)			
				elif word in ACCESSORY_STEMS or word[:-1] in ACCESSORY_STEMS or word[:-2] in ACCESSORY_STEMS or word[:-3] in ACCESSORY_STEMS or word[:-4] in ACCESSORY_STEMS:
					found = True
					if phrase != "":
						accessories.append(phrase + " " + word)
						phrase = ""
					else:	
						accessories.append(word)			
				elif word in CONTENTS or word in CONTENTS_STEMS or word[:-1] in CONTENTS_STEMS or word[:-2] in CONTENTS_STEMS or word[:-3] in CONTENTS_STEMS or word[:-4] in CONTENTS_STEMS:
					found = True
					if phrase != "":
						contents.append(phrase + " " + word)
						phrase = ""
					else:	
						contents.append(word)			
				elif word in STYLES or word in STYLE_STEMS or word[:-1] in STYLE_STEMS or word[:-2] in STYLE_STEMS or word[:-3] in STYLE_STEMS or word[:-4] in STYLE_STEMS:
					found = True
					if phrase != "":
						styles.append(phrase + " " + word)
						phrase = ""
					else:	
						styles.append(word)			
				elif  word in NUMBER_STEMS or word[:-1] in NUMBER_STEMS or word[:-2] in NUMBER_STEMS or word[:-3] in NUMBER_STEMS or word[:-4] in NUMBER_STEMS:
					found = True
					if phrase != "":
						numbers.append(phrase + " " + word)
						phrase = ""
					else:	
						numbers.append(word)			
				elif  word in FUNCTION_STEMS or word[:-1] in FUNCTION_STEMS or word[:-2] in FUNCTION_STEMS or word[:-3] in FUNCTION_STEMS or word[:-4] in FUNCTION_STEMS:
					found = True
					if phrase != "":
						functions.append(phrase + " " + word)
						phrase = ""
					else:	
						numbers.append(word)
				elif  word in SIZE_STEMS or word[:-1] in SIZE_STEMS or word[:-2] in SIZE_STEMS or word[:-3] in SIZE_STEMS or word[:-4] in SIZE_STEMS:
					found = True
					if phrase != "":
						sizes.append(phrase + " " + word)
						phrase = ""
					else:	
						sizes.append(word)
				elif  word in CONDITION_STEMS or word[:-1] in CONDITION_STEMS or word[:-2] in CONDITION_STEMS or word[:-3] in CONDITION_STEMS or word[:-4] in CONDITION_STEMS:
					found = True
					if phrase != "":
						conditions.append(phrase + " " + word)
						phrase = ""
					else:	
						conditions.append(word)
				elif  word in GLOSSARY_STEMS or word[:-1] in GLOSSARY_STEMS or word[:-2] in GLOSSARY_STEMS or word[:-3] in GLOSSARY_STEMS or word[:-4] in GLOSSARY_STEMS:
					found = True
					if phrase != "":
						glossary.append(phrase + " " + word)
						phrase = ""
					else:	
						glossary.append(word)
				# if the word has a slash in it, it is extraneous		
				elif word.find('/') != -1:
					continue

				#if word has a number in it, it is extraneous
				elif len(re.findall('(.*)[0-9](.*)', word)) > 0:
					continue

				# if none of the above apply, the word is an "Other" word
				else:
					if phrase != "":
						cur_other = cur_other + " " + phrase + " " + word

						others.append(phrase + " " + word)
						if phrase + " " + word in all_others:
							all_others[phrase + " " + word] = all_others[phrase + " " + word]+1
						else:
							all_others[phrase + " " + word] = 1
						phrase = ""

					else:	
						cur_other = cur_other + " " + word

						others.append(word)
						if word in all_others:
							all_others[word] = all_others[word] + 1
						else:
							all_others[word] = 1

				
				# if we found a word, write the current other buffer to the dictionary
				if found:
					if cur_other in all_other_phrases:
				 		all_other_phrases[cur_other] = all_other_phrases[cur_other] + 1
				 	else:
				 		all_other_phrases[cur_other] = 1
				 	cur_other = ""

				 # else calculate the edit distance 
				# else:
				#  	wordDistance = closestWord(word,WORDS)
				#  	if word in distances:
				# 	 	distances[word] = [wordDistance, distances[word][1] + 1]
				# 	else:
				# 		distances[word] = [wordDistance, 1]
			# if, after processing all the words, there is one left over, call it the object
			if len(others) == 1:
				object = others[0]
				others[0] = ""
			
			# Output the results
			print code,                                       # Code
			print "\t" + str(line_num),                       # Line 
			print "\t" + house,                               # House
			print "\t" + room,                                # Room
			print "\t" + str(", ".join(sorted(glossary))),    # Glossary (should be Container)
			print "\t" + object,                              # Object
			print "\t" + str(", ".join(sorted(numbers))),     # Quantity
			print "\t" + str(", ".join(sorted(values))),      # Value
			print "\t" + str(", ".join(sorted(substrates))),  # Substrate
			print "\t" + str(", ".join(sorted(accessories))), # Trim or Accouterments
			print "\t" + str(", ".join(sorted(contents))),    # Contents
			print "\t" + str(", ".join(sorted(sizes))),       # Size
			print "\t" + str(", ".join(sorted(colors))),      # Color
			print "\t" + str(", ".join(sorted(conditions))),  # Condition
			print "\t" + str(", ".join(sorted(functions))),   # Function
			print "\t" + str(", ".join(sorted(styles))),      # Style
			print "\t",                                       # Gender
			print "\t",                                       # Owner
			print "\t" + str(", ".join(sorted(others))),      # Other words
			print "\t" + str(len(others))                     # Number of Other words
print "OTHER INDIVIDUAL WORDS/PHRASES"
for k,v in all_others.iteritems():
	print k + "\t" + str(v)
print "OTHER ENTIRE PHRASES"
for k,v in all_other_phrases.iteritems():
	print k + "\t" + str(v)
print "EDIT DISTANCES"
for k, v in distances.iteritems():
	print k + "\t" + str(v[0][0]) + "\t" + str(v[0][1]) + "\t" + str(v[1])