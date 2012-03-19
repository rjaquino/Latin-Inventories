import re
from constants import *
from helpers import *

f = open('sample.txt', 'r')
text = f.read()
lines = text.splitlines()
m = re.search('Sex:\t(.*)\n', text)
sex =  m.group(1)+'\n'

line_num = 0
for line in lines:
	line_num = line_num + 1
	substrates = []
	colors = []
	accessories = []
	contents = []
	styles = []
	numbers = []
	others = []
	attachment = ""
	phrase = ""

	m = re.search('\tItem(.*)', line)
	if not m is None:
		item = m.group(1);
		words = item.split();
		for idx, word in enumerate(words):
			if word == "cum":
				attachment = " ".join(words[idx:])

				# remove /fol from end of attachment
				pos = attachment.find('/')
				if pos != -1:
					attachment = attachment[:pos-1]
				break;
			if word == "de":
				phrase = "de"
				continue
			if word in SUBSTRATE_STEMS or word[:-1] in SUBSTRATE_STEMS or word[:-2] in SUBSTRATE_STEMS or word[:-3] in SUBSTRATE_STEMS or word[:-4] in SUBSTRATE_STEMS:
#				print "Line " + str(line_num) + ", Substrate: " + word
				if phrase != "":
					substrates.append(phrase + " " + word)
					phrase = ""
				else:	
					substrates.append(word)			
			elif word in COLOR_STEMS or word[:-1] in COLOR_STEMS or word[:-2] in COLOR_STEMS or word[:-3] in COLOR_STEMS or word[:-4] in COLOR_STEMS:
#				print "Line " + str(line_num) + ", Color: " + word
				if phrase != "":
					colors.append(phrase + " " + word)
					phrase = ""
				else:	
					colors.append(word)			
			elif word in ACCESSORY_STEMS or word[:-1] in ACCESSORY_STEMS or word[:-2] in ACCESSORY_STEMS or word[:-3] in ACCESSORY_STEMS or word[:-4] in ACCESSORY_STEMS:
#				print "Line " + str(line_num) + ", Accessory: " + word
				if phrase != "":
					accessories.append(phrase + " " + word)
					phrase = ""
				else:	
					accessories.append(word)			
			elif word in CONTENTS or word in CONTENTS_STEMS or word[:-1] in CONTENTS_STEMS or word[:-2] in CONTENTS_STEMS or word[:-3] in CONTENTS_STEMS or word[:-4] in CONTENTS_STEMS:
#				print "Line " + str(line_num) + ", Contents: " + word
				if phrase != "":
					contents.append(phrase + " " + word)
					phrase = ""
				else:	
					contents.append(word)			
			elif word in STYLES or word in STYLE_STEMS or word[:-1] in STYLE_STEMS or word[:-2] in STYLE_STEMS or word[:-3] in STYLE_STEMS or word[:-4] in STYLE_STEMS:
#				print "Line " + str(line_num) + ", Style: " + word
				if phrase != "":
					styles.append(phrase + " " + word)
					phrase = ""
				else:	
					styles.append(word)			
			elif  word in NUMBER_STEMS or word[:-1] in NUMBER_STEMS or word[:-2] in NUMBER_STEMS or word[:-3] in NUMBER_STEMS or word[:-4] in NUMBER_STEMS:
#				print "Line " + str(line_num) + ", Style: " + word
				if phrase != "":
					numbers.append(phrase + " " + word)
					phrase = ""
				else:	
					numbers.append(word)			
			elif word.find('/') != -1:
				continue
			else:
#				print "Line " + str(line_num) + ", Other: " + word
				if phrase != "":
					others.append(phrase + " " + word)
					phrase = ""
				else:	
					others.append(word)
		print line
		print "Line: "+str(line_num)
		print "\tSubtrates: " + str(sorted(substrates))
		print "\tColors: " + str(sorted(colors))
		print "\tAccessories: " + str(sorted(accessories))
		print "\tContents: " + str(sorted(contents))
		print "\tStyles " + str(sorted(styles))
		print "\tNumbers: " + str(sorted(numbers))
		print "\tOthers: " + str(sorted(others))
		print "\tAttachment: " + attachment
		print ""
		# r = re.search('(un[ua][ms]?|du[oae]s?|tr(es|ia|ibus)|quattuor|quinque|sex|septem|octo|novem|decem|ali(um|a|o)s?|qu(i|a|o)dam) ([a-zA-Z]*) ', line)
		# if not r is None:
		# 	print "Number = "+r.group(1)+'\n'
		# 	print "Object = "+r.group(5)+'\n'

			#ideas: build a better regular expression, or build classes for case, gender, etc, and handle each word at a time?