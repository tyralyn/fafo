# Perform basic string compression using counts of repeated characters
#
# input: "bbbaaaaa jk."
# output: "b3a5 1j1k1.1"


def stringCompression(s):
	result=s[0]
	cur=s[0]
	count=1
	for ch in s:
		if ch==cur:
			count+=1
		else:
			result+=str(count)
			count=1
			cur=ch
	result+=ch+str(count)
	return result


print(stringCompression("bbaaaaa jk."))