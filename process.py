import re
from constants import *

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
	m = re.search('\tItem(.*)', line)
	if not m is None:
		item = m.group(1);
		words = item.split();
		for word in words:
			if word in SUBSTRATE_STEMS or word[:-1] in SUBSTRATE_STEMS or word[:-2] in SUBSTRATE_STEMS or word[:-3] in SUBSTRATE_STEMS or word[:-4] in SUBSTRATE_STEMS:
#				print "Line " + str(line_num) + ", Substrate: " + word
				substrates.append(word)			
			elif word in COLOR_STEMS or word[:-1] in COLOR_STEMS or word[:-2] in COLOR_STEMS or word[:-3] in COLOR_STEMS or word[:-4] in COLOR_STEMS:
#				print "Line " + str(line_num) + ", Color: " + word
				colors.append(word)			
			elif word in ACCESSORY_STEMS or word[:-1] in ACCESSORY_STEMS or word[:-2] in ACCESSORY_STEMS or word[:-3] in ACCESSORY_STEMS or word[:-4] in ACCESSORY_STEMS:
#				print "Line " + str(line_num) + ", Accessory: " + word
				accessories.append(word)			
			elif word in CONTENTS or word in CONTENTS_STEMS or word[:-1] in CONTENTS_STEMS or word[:-2] in CONTENTS_STEMS or word[:-3] in CONTENTS_STEMS or word[:-4] in CONTENTS_STEMS:
#				print "Line " + str(line_num) + ", Contents: " + word
				contents.append(word)			
			elif word in STYLES or word in STYLE_STEMS or word[:-1] in STYLE_STEMS or word[:-2] in STYLE_STEMS or word[:-3] in STYLE_STEMS or word[:-4] in STYLE_STEMS:
#				print "Line " + str(line_num) + ", Style: " + word
				styles.append(word)			
			elif  word in NUMBER_STEMS or word[:-1] in NUMBER_STEMS or word[:-2] in NUMBER_STEMS or word[:-3] in NUMBER_STEMS or word[:-4] in NUMBER_STEMS:
#				print "Line " + str(line_num) + ", Style: " + word
				numbers.append(word)			
			elif word.find('/') != -1:
				continue
			else:
#				print "Line " + str(line_num) + ", Other: " + word
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
		print ""
		# r = re.search('(un[ua][ms]?|du[oae]s?|tr(es|ia|ibus)|quattuor|quinque|sex|septem|octo|novem|decem|ali(um|a|o)s?|qu(i|a|o)dam) ([a-zA-Z]*) ', line)
		# if not r is None:
		# 	print "Number = "+r.group(1)+'\n'
		# 	print "Object = "+r.group(5)+'\n'

			#ideas: build a better regular expression, or build classes for case, gender, etc, and handle each word at a time?