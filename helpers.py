import sys
def getCategory(word):
	if word == "cum":
		return "attachment"
	if word in SUBSTRATE_STEMS or word[:-1] in SUBSTRATE_STEMS or word[:-2] in SUBSTRATE_STEMS or word[:-3] in SUBSTRATE_STEMS or word[:-4] in SUBSTRATE_STEMS:
		return "substrate"
	elif word in COLOR_STEMS or word[:-1] in COLOR_STEMS or word[:-2] in COLOR_STEMS or word[:-3] in COLOR_STEMS or word[:-4] in COLOR_STEMS:
		return "color"
	elif word in ACCESSORY_STEMS or word[:-1] in ACCESSORY_STEMS or word[:-2] in ACCESSORY_STEMS or word[:-3] in ACCESSORY_STEMS or word[:-4] in ACCESSORY_STEMS:
		return "accessory"
	elif word in CONTENTS or word in CONTENTS_STEMS or word[:-1] in CONTENTS_STEMS or word[:-2] in CONTENTS_STEMS or word[:-3] in CONTENTS_STEMS or word[:-4] in CONTENTS_STEMS:
		return "contents"
	elif word in STYLES or word in STYLE_STEMS or word[:-1] in STYLE_STEMS or word[:-2] in STYLE_STEMS or word[:-3] in STYLE_STEMS or word[:-4] in STYLE_STEMS:
		return "style"
	elif  word in NUMBER_STEMS or word[:-1] in NUMBER_STEMS or word[:-2] in NUMBER_STEMS or word[:-3] in NUMBER_STEMS or word[:-4] in NUMBER_STEMS:
		return "number"
	else:
		return "other"

# http://stackoverflow.com/questions/7036277/how-to-optimize-edit-distance-code
def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space.
        # Not really important to the algorithm anyway.
        a,b = b,a
        n,m = m,n

    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]

def closestWord(testWord, words):
	minDistance = sys.maxint
	minWord = ""
	for word in words:
		if len(testWord) > 0 and len(word) > 0:
			if testWord[0] == testWord[0]:
				distance = levenshtein(word, testWord)
				if distance < minDistance:
					minDistance = distance
					minWord = word
	return [minWord, minDistance]
