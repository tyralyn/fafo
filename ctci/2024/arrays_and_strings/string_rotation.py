# Assume you have a method isSubstring, that checks if one work is a substring of another. Given two strings s1 and s2, check if s2 is a rotation of s1 using only one call to isSubstring
#
# Example: "waterbottle" is a rotation of "erbottlewat"
# python has an is substring method using 
#
# substr is in superstr
# 
# so im going to do that

def isStringRotation(s1, s2):
	if len(s1) != len(s2):
		return False
	return(s2 in s1*2)

print(isStringRotation("erbottlewat", "waterbottle"))
print(isStringRotation("erbottlewat", "erbottlewat"))
print(isStringRotation("a", ""))
print(isStringRotation("paper", "planes"))
