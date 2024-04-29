# Given two strings, determine if one is a permutation of the other
# permutation = same letters, different order
#
# question: spaces and punctuation -- ignored?
# assume input is all letters
# 
# question: are two of the same string considerd to be permutation
#
# question: what about cases? is an uppercase A considered to be the same WRT permutations as a lowercase a?
#
# inputs: "abcdefg", "eabcdgf"
# output: True
#
# inputs: "abcde", "abc"
# output: False
#
# TODO: check input validity, for spaces, etc.

def checkPermutation(s1, s2):
	print(f'\n"{s1.casefold()}"", "{s2.casefold()}"')
	return (sorted(s1.casefold()) == sorted(s2.casefold()))

print(checkPermutation("blackout", "outblack"))
print(checkPermutation("hello", "hello"))
print(checkPermutation("blackout", "black out"))
print(checkPermutation("hello", "goodbye"))

print(checkPermutation("HeLLo", "ohell"))
