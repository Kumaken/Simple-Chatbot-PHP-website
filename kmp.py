def KMP(text, pattern):
	n = len(text)
	m = len(pattern)
	fail = computeFail(pattern)
	i = 0
	j = 0

	while(i < n):
		if (pattern[j] == text[i]):
			if (j == m-1):
				return i - m + 1
			i += 1
			j += 1
		elif (j > 0):
			j = fail[j - 1]
		else:
			i += 1

	return -1

def computeFail(pattern):
	m = len(pattern)
	fail = [0]*m
	fail[0] = 0
	j = 0
	i = 1

	while (i < m):
		if (pattern[j] == pattern[i]):
			fail[i] = j + 1
			i += 1
			j += 1
		elif (j > 0):
			j = fail[j - 1]
		else:
			fail[i] = 0
			i += 1

	return fail

def KMPFail(text, pattern):
	n = len(text)
	m = len(pattern)
	p = pattern.split(" ")
	t = text
	percent = 0
	res = 0;

	for i in p:
		res = KMP(text, i)
		if (res != -1):
			percent = percent + len(i) + 1
			if len(t) > res :
				t = t[0: 0:] + t[res + 1::]
	print (percent)
	return percent/len(pattern)
		
	


def kmpcall(text,pattern):
	#print("KMP : ")
	#text = input()
	#pattern = "hai kamu cantik"
	pos = KMP(text, pattern)
	if (pos == -1):
		print("salah")
		return KMPFail(text, pattern)
	else:
		return 1
