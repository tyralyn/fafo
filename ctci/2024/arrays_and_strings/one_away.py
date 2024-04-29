# Given two strings, check if they are one edit or zero edits away from each other
#
# Edits: insert a character, remove a character, or replace a character
#
# input: "bob", "bob"
# True
#
# input: "sat", "stat"
# True
#
# input: "cup", "bowl"
# False

def oneAway(s1, s2):
	print(f'\n{s1}, {s2}')
	if abs(len(s1) - len(s2) > 1):
		return False
	elif len(s1) == len(s2):
		found_difference = False
		for i in range(len(s1)):
			if s1[i] != s2[i]:
				# print(f'{s1[i]} : {s2[i]}')
				if found_difference:
					return False
				found_difference=True
		return found_difference
	else: # abs(len(s1) - len(s2) == 1):
		longest = s1 if len(s1) > len(s2) else s2
		shortest = s1 if len(s1) < len(s2) else s2

		first_difference = len(shortest)
		for i in range(len(shortest)):
			if shortest[i]!=longest[i]:
				first_difference = i
		# by default we know shortest[:first_difference] == longest[:first_difference]
		print(f'{first_difference}, {shortest[first_difference:]} -- {longest[first_difference+1:]}')
		return shortest[first_difference:] == longest[first_difference+1:]

print(oneAway("", ""))
print(oneAway("", "m"))
print(oneAway("banana", "bananabread"))
print(oneAway("done", "redone"))
print(oneAway("kpop", "kpoop"))
print(oneAway("m", "m1"))
print(oneAway("kpop", "pop"))
print(oneAway("snake", "stake"))



