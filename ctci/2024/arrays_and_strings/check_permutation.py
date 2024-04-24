# Given two strings, determine if one is a permutation of the other
# permutation = same letters, different order
#
# question: spaces and punctuation -- ignored?
# assume input is all letters
# 
# question: are two of the same string considerd to be permutation
#
# inputs: "abcdefg", "eabcdgf"
# output: True
#
# inputs: "abcde", "abc"
# output: False
#
# TODO: check input validity, for spaces, etc.

def checkPermutation(s1, s2):
	print(f'\n"{s1}"", "{s2}"')
	return (sorted(s1) == sorted(s2))

print(checkPermutation("blackout", "outblack"))
print(checkPermutation("hello", "hello"))
print(checkPermutation("blackout", "black out"))
print(checkPermutation("hello", "goodbye"))

