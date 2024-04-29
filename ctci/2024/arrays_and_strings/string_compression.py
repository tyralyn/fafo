# Perform basic string compression using counts of repeated characters
#
# input: "bbbaaaaa jk."
# output: "b3a5 1j1k1.1"


def stringCompression(s):
	if not s:
		return s
	result = ""
	last_char = ''
	for ch in s:
		if ch == last_char:
			result = result[:-1] + str(int(result[-1]) + 1)
		if ch !=last_char:
			result += ch + '1'
			last_char = ch

	return result


print(stringCompression("bbbaaaaa jk."))
print(stringCompression(""))
print(stringCompression("abcdefg"))