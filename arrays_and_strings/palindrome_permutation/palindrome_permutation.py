"""Check if a string is a permutation of a palindrome.

Given a string, check if permutation of palindrome. Palindrome is the
same forwards and backwards. Permutation is a rearrangement of
letters. Palindrome does not need to be limited to only dictionary
words.

strategy1:
	sort string

strategy2:
* Palindrome has 2 copies of each letter, and up to one letter can 
just one copy
* Make a list that is basically a reference of all the characters
in the list (once), and check the counts to see if they are all
2,2,2,2....1
"""

def is_palindrome_permutation(string):
	no_repeats_list =set(string)
	odd_count = 0
	for c in no_repeats_list:
		if string.count(c) % 2 == 1:
			if odd_count > 0:
				return False;
			odd_count++
	return True





