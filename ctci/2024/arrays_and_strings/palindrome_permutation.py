# Given a string, write a function to check if it is a permutation of a palindrome
#
# Input: Tact Coa
# Output: True (Permutations: "taco cat", "atco cta", etc.)
#
# question: should we only consider ascii letters?
# answer: only letters count


from collections import Counter
def palindromePermutation(s):
	print(f'\n{s}')
	l = list(filter(lambda x: x.isalpha(), s.casefold()))
	count = list(Counter(l).values())
	filtered_count = list(filter(lambda x: x%2 == 1, count))
	return (len(filtered_count) <= 1)



print(palindromePermutation("Tact Coa"))
print(palindromePermutation("barbecue"))
print(palindromePermutation("race.         car"))
print(palindromePermutation(""))
print(palindromePermutation("g"))